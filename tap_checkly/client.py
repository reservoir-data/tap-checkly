"""REST client handling, including ChecklyStream base class."""

from __future__ import annotations

import sys
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, override

from singer_sdk import RESTStream, SchemaDirectory, StreamSchema
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import BasePageNumberPaginator

from tap_checkly import schemas

if sys.version_info >= (3, 13):
    from typing import TypeVar
else:
    from typing_extensions import TypeVar

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

PAGE_SIZE = 100
SCHEMAS_DIR = SchemaDirectory(schemas)

T = TypeVar("T", default=Any)


class ChecklyStream(RESTStream[T], Generic[T], metaclass=ABCMeta):  # noqa: UP046
    """Checkly stream class."""

    url_base = "https://api.checklyhq.com/v1"
    records_jsonpath = "$[*]"  # Or override `parse_response`.

    schema = StreamSchema(SCHEMAS_DIR)

    @override
    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        return BearerTokenAuthenticator(token=self.config["token"])

    @override
    @property
    def http_headers(self) -> dict[str, str]:
        return {
            "User-Agent": self.user_agent,
            "X-Checkly-Account": self.config["account_id"],
        }

    @override
    def get_url_params(self, context: Context | None, next_page_token: T | None) -> dict[str, Any]:
        params: dict[str, Any] = {}

        if self.replication_key:
            start_date = self.get_starting_timestamp(context)
            if start_date:
                params["from"] = start_date.timestamp()

        return params

    @property
    @abstractmethod
    def openapi_ref(self) -> str:
        """Return the OpenAPI component name for this stream.

        Returns:
            The OpenAPI reference for this stream.
        """
        ...


class ChecklyPaginatedStream(ChecklyStream[int]):
    """Checkly paginated stream class."""

    @override
    def get_new_paginator(self) -> BasePageNumberPaginator | None:
        return BasePageNumberPaginator(start_value=1)

    @override
    def get_url_params(self, context: Context | None, next_page_token: int | None) -> dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params["limit"] = PAGE_SIZE
        params["page"] = next_page_token or 1
        return params


class ChecklyNextIDPaginatedStream(ChecklyStream[str]):
    """Checkly next ID paginated stream class."""

    records_jsonpath = "$.entries[*]"
    next_page_token_jsonpath = "$.nextId"  # noqa: S105

    @override
    def get_url_params(self, context: Context | None, next_page_token: str | None) -> dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        if next_page_token:
            params["nextId"] = next_page_token
        return params
