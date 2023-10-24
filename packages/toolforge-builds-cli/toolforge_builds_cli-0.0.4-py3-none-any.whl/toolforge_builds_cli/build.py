from __future__ import annotations

from typing import Any

import requests
from toolforge_weld.api_client import ConnectionError, ToolforgeClient
from toolforge_weld.errors import ToolforgeError, ToolforgeUserError
from toolforge_weld.kubernetes_config import Kubeconfig

from toolforge_builds_cli.config import Config

USER_AGENT = "toolforge_builds_cli"


class BuildClientError(ToolforgeError):
    """Raised when an HTTP request fails."""

    def __init__(self, message: str, context: dict[str, Any] | None = None) -> None:
        super().__init__(message)

        if context:
            # property is defined in parent class
            self.context = context


class BuildClientUserError(BuildClientError, ToolforgeUserError):
    """Raised when an HTTP request fails with a 4xx status code."""


def handle_http_exception(e: requests.exceptions.HTTPError) -> Exception:
    if e.response is None:
        return BuildClientError(message="Got no response", context={})

    if 400 >= e.response.status_code >= 499:
        error_class = BuildClientError
    else:
        error_class = BuildClientUserError

    context = {}
    message = e.response.text
    try:
        data = e.response.json()
        if isinstance(data, dict):
            if "message" in data:
                message = data["message"]
                context = data
        elif isinstance(data, str):
            message = data
    except requests.exceptions.InvalidJSONError:
        pass

    return error_class(message=message, context=context)


def handle_connection_error(e: ConnectionError) -> Exception:
    context = {}
    if isinstance(e, requests.exceptions.HTTPError):
        context["body"] = e.response.text if e.response else ""

    return BuildClientError(
        message="The build service seems to be down – please retry in a few minutes.", context=context
    )


class BuildClient(ToolforgeClient):
    def __init__(
        self,
        kubeconfig: Kubeconfig,
        server: str,
        endpoint_prefix: str,
        user_agent: str,
    ):
        super().__init__(
            kubeconfig=kubeconfig,
            server=server + endpoint_prefix,
            user_agent=user_agent,
            exception_handler=handle_http_exception,
            connect_exception_handler=handle_connection_error,
        )

    @classmethod
    def from_config(cls, config: Config):
        return cls(
            endpoint_prefix=config.builds.builds_endpoint,
            kubeconfig=Kubeconfig.load(),
            server=config.api_gateway.url,
            user_agent=USER_AGENT,
        )
