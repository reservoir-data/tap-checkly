"""REST client handling, including ChecklyStream base class."""

from __future__ import annotations

import json
import sys
from abc import ABCMeta, abstractmethod
from functools import lru_cache
from typing import Any

from singer_sdk import RESTStream
from singer_sdk._singerlib import resolve_schema_references
from singer_sdk.authenticators import BearerTokenAuthenticator

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


@lru_cache(maxsize=None)
def load_openapi() -> dict[str, Any]:
    """Load the OpenAPI specification from the package.

    Returns:
        The OpenAPI specification as a dict.
    """
    with importlib_resources.files("tap_checkly").joinpath("openapi.json").open() as f:
        return json.load(f)


class ChecklyStream(RESTStream, metaclass=ABCMeta):
    """Checkly stream class."""

    url_base = "https://api.checklyhq.com/v1"
    records_jsonpath = "$[*]"  # Or override `parse_response`.

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        token: str = self.config["token"]
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=token,
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {
            "User-Agent": f"{self.tap_name}/{self._tap.plugin_version}",
            "X-Checkly-Account": self.config["account_id"],
        }
        return headers

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        params: dict = {}
        return params

    def _resolve_openapi_ref(self) -> dict[str, Any]:
        schema = {"$ref": f"#/components/schemas/{self.openapi_ref}"}
        openapi = load_openapi()
        schema["components"] = openapi["components"]
        return resolve_schema_references(schema)

    @property
    @lru_cache(maxsize=None)
    def schema(self) -> dict[str, Any]:
        """Return the schema for this stream.

        Returns:
            The schema for this stream.
        """
        return self._resolve_openapi_ref()

    @property
    @abstractmethod
    def openapi_ref(self) -> str:
        """Return the OpenAPI component name for this stream.

        Returns:
            The OpenAPI reference for this stream.
        """
        ...
