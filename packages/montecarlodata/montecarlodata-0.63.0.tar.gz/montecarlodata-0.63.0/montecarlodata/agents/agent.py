import json
import uuid
from dataclasses import dataclass
from typing import (
    List,
    Optional,
)
from urllib.parse import urljoin

import click
import questionary
import requests
from dataclasses_json import (
    DataClassJsonMixin,
    Undefined,
    dataclass_json,
)
from tabulate import tabulate

from montecarlodata import settings
from montecarlodata.agents.fields import (
    EXPECTED_CREATE_OR_UPDATE_AGENT_RESPONSE_FIELD,
    EXPECTED_DELETE_AGENT_RESPONSE_FIELD,
    EXPECTED_TEST_AGENT_REACHABILITY,
    EXPECTED_UPGRADE_AGENT_RESPONSE_FIELD,
    GCP_JSON_SERVICE_ACCOUNT_KEY,
    AWS_ASSUMABLE_ROLE,
)
from montecarlodata.common.common import read_as_json_string
from montecarlodata.common.user import UserService
from montecarlodata.config import Config
from montecarlodata.errors import manage_errors, complain_and_abort
from montecarlodata.utils import GqlWrapper
from montecarlodata.queries.agent import (
    CREATE_OR_UPDATE_AGENT_MUTATION,
    DELETE_AGENT_MUTATION,
    QUERY_TEST_AGENT_REACHABILITY,
    UPGRADE_AGENT_MUTATION,
)

DOCKER_HUB_TAGS_PAGE_SIZE = 10
DOCKER_HUB_TAGS_BASE_URL = "https://hub.docker.com/v2/namespaces/"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass()
class DockerTag(DataClassJsonMixin):
    name: str
    last_updated: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass()
class DockerTagsResult(DataClassJsonMixin):
    results: List[DockerTag]


class AgentService:
    _AGENT_FRIENDLY_HEADERS = [
        "Agent ID",
        "Agent Type / Storage Type",
        "DC ID",
        "Endpoint",
        "Created on (UTC)",
        "Is Active",
    ]
    _VALIDATION_RESPONSE_HEADERS = [
        "Message",
        "Cause",
        "Resolution",
    ]

    def __init__(
        self,
        config: Config,
        request_wrapper: Optional[GqlWrapper] = None,
        user_service: Optional[UserService] = None,
    ):
        self._request_wrapper = request_wrapper or GqlWrapper(config)
        self._user_service = user_service or UserService(
            request_wrapper=self._request_wrapper, config=config
        )
        self._image_org = config.mcd_agent_image_org
        self._image_repo = config.mcd_agent_image_repo
        self._image_name = (
            f"{config.mcd_agent_image_host}/{self._image_org}/{self._image_repo}"
        )

    @manage_errors
    def create_agent(
        self, agent_type, platform, storage, auth_type, endpoint, **kwargs
    ) -> None:
        """
        Register an agent by validating connection and creating an AgentModel in the monolith.
        """

        agent_request = {
            "agent_type": agent_type,
            "endpoint": endpoint,
            "storage_type": storage,
            "platform": platform,
            "auth_type": auth_type,
        }

        if kwargs.get("dc_id"):
            agent_request["data_collector_id"] = kwargs["dc_id"]

        if auth_type == GCP_JSON_SERVICE_ACCOUNT_KEY:
            agent_request["credentials"] = read_as_json_string(kwargs["key_file"])
        elif auth_type == AWS_ASSUMABLE_ROLE:
            creds = {"aws_assumable_role": kwargs["assumable_role"]}
            if kwargs["external_id"]:
                creds["external_id"] = kwargs["external_id"]
            agent_request["credentials"] = json.dumps(creds)

        response = self._request_wrapper.make_request_v2(
            query=CREATE_OR_UPDATE_AGENT_MUTATION,
            operation=EXPECTED_CREATE_OR_UPDATE_AGENT_RESPONSE_FIELD,
            variables=agent_request,
        )

        agent_id = response.data.get("agentId")
        validation_result = response.data.get("validationResult")

        self._validate_response(validation_result)

        if agent_id is not None:
            click.echo("Agent successfully registered!\n" f"AgentId: {agent_id}")
        else:
            complain_and_abort("Failed to register agent.")

    @manage_errors
    def delete_agent(self, agent_id) -> None:
        """
        Deregister an Agent (deletes AgentModel from monolith)
        """
        agent_request = {"agentId": agent_id}

        response = self._request_wrapper.make_request_v2(
            query=DELETE_AGENT_MUTATION,
            operation=EXPECTED_DELETE_AGENT_RESPONSE_FIELD,
            variables=agent_request,
        )

        success = response.data.get("success")

        if success:
            click.echo(f"Agent {agent_id} deregistered.")
        else:
            complain_and_abort("Failed to deregister agent.")

    @manage_errors
    def echo_agents(
        self,
        headers: Optional[str] = "firstrow",
        table_format: Optional[str] = "fancy_grid",
    ):
        """
        Display agents in an easy to read table.
        """

        table = [self._AGENT_FRIENDLY_HEADERS]
        for agent in self._user_service.agents:
            is_active = "false" if agent.get("isDeleted") else "true"
            full_name = f"{agent.get('agentType', '')} / {agent.get('storageType', '')}"

            table += [
                [
                    agent.get("uuid", ""),
                    full_name,
                    agent.get("dc_id", ""),
                    agent.get("endpoint", ""),
                    agent.get("createdTime", ""),
                    is_active,
                ]
            ]

        # If the account has no agents, add 1 line of empty values so tabulate() creates a pretty empty table
        if len(table) == 1:
            table += ["" for _ in self._AGENT_FRIENDLY_HEADERS]

        click.echo(
            tabulate(table, headers=headers, tablefmt=table_format, maxcolwidths=100)
        )

    def _validate_response(self, validation_result):
        table = [self._VALIDATION_RESPONSE_HEADERS]
        stack_trace = None

        if validation_result.get("errors"):
            for error in validation_result.get("errors", []):
                stack_trace = (
                    "-----------" + "\n" + error.get("stackTrace", None) + "\n"
                )

                table += [
                    [
                        click.style(
                            f"ERROR: {error.get('friendlyMessage', '')}", fg="red"
                        ),
                        error.get("cause", ""),
                        error.get("resolution", ""),
                    ]
                ]

        if validation_result.get("warnings"):
            for warning in validation_result.get("warnings"):
                table += [
                    [
                        click.style(
                            f"WARNING: {warning.get('friendlyMessage', '')}",
                            fg="yellow",
                        ),
                        warning.get("cause", ""),
                        warning.get("resolution", ""),
                    ]
                ]

        # If there are any errors or warnings returned, display them
        if len(table) > 1:
            click.echo(
                tabulate(
                    table, headers="firstrow", tablefmt="fancy_grid", maxcolwidths=100
                )
            )

        # If Verbose Errors is set as env variable and there was an error stack trace, save trace to a file and print path
        if settings.MCD_VERBOSE_ERRORS and stack_trace:
            stack_trace_filename = f"mcd_error_trace_{uuid.uuid4()}.txt"
            with open(stack_trace_filename, "w") as stack_trace_file:
                stack_trace_file.write(stack_trace)
            click.echo(f"Stack Trace of error(s) saved to /{stack_trace_filename}")

    @manage_errors
    def check_agent_health(self, **kwargs):
        dc = self._user_service.get_collector(kwargs.get("dc_id"))
        variables = {"dcId": dc.uuid}

        if "agent_id" in kwargs:
            variables["agentId"] = kwargs["agent_id"]

        response = self._request_wrapper.make_request_v2(
            query=QUERY_TEST_AGENT_REACHABILITY,
            operation=EXPECTED_TEST_AGENT_REACHABILITY,
            variables=variables,
        )

        success = response.data.get("success")
        additional_data = response.data.get("additionalData", {})
        if success:
            returned_data = additional_data.get("returnedData")
            if returned_data:
                headers = []
                rows = []
                for field, value in returned_data.items():
                    headers.append(field)
                    rows.append(value)
                click.echo(
                    tabulate(
                        [rows], headers=headers, tablefmt="fancy_grid", maxcolwidths=100
                    )
                )
            return click.echo("Agent health check succeeded!")

        return self._validate_response(response.data)

    @manage_errors
    def upgrade_agent(self, **kwargs):
        dc = self._user_service.get_collector(kwargs.get("dc_id"))
        image_tag = self._choose_image_tag(kwargs["image_tag"])
        variables = {
            "dataCollectorId": dc.uuid,
            "image": f"{self._image_name}:{image_tag}",
        }

        response = self._request_wrapper.make_request_v2(
            query=UPGRADE_AGENT_MUTATION,
            operation=EXPECTED_UPGRADE_AGENT_RESPONSE_FIELD,
            variables=variables,
        )
        click.echo("Upgrade succeeded!")
        upgrade_result = response.data.get("upgradeResult").to_dict()
        if upgrade_result:
            headers = []
            rows = []
            for field, value in upgrade_result.items():
                headers.append(field)
                rows.append(value)
            headers = list(upgrade_result.keys())
            rows = upgrade_result.values()
            click.echo(
                tabulate(
                    [rows], headers=headers, tablefmt="fancy_grid", maxcolwidths=100
                )
            )

    def _choose_image_tag(self, image: str) -> str:
        image_path = f"{self._image_org}/repositories/{self._image_repo}"
        url: str = urljoin(DOCKER_HUB_TAGS_BASE_URL, f"{image_path}/tags/{image}")
        response = requests.head(url=url)
        if response.status_code == 200:
            return image

        url = urljoin(
            DOCKER_HUB_TAGS_BASE_URL,
            f"{image_path}/tags?page_size={DOCKER_HUB_TAGS_PAGE_SIZE}&page=1",
        )
        response = requests.get(url=url)
        response.raise_for_status()
        payload: DockerTagsResult = DockerTagsResult.from_json(response.text)
        payload.results.sort(key=lambda t: t.last_updated, reverse=True)
        versions = [tag.name for tag in payload.results if "latest" not in tag.name]
        return questionary.select(
            "Please choose a valid image tag", choices=versions
        ).ask()
