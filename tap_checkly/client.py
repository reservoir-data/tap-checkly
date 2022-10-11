"""REST client handling, including ChecklyStream base class."""

from __future__ import annotations

from typing import Any

from singer_sdk import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator


class ChecklyStream(RESTStream):
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
