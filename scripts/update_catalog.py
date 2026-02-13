#!/usr/bin/env -S uv run

"""Update the Singer tap catalog using the OpenAPI specification from Checkly."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, cast

import requests
from singer_sdk.schema.source import OpenAPISchemaNormalizer
from singer_sdk.singerlib import resolve_schema_references
from toolz import assoc_in, get_in

from tap_checkly.tap import TapCheckly

if TYPE_CHECKING:
    from tap_checkly.client import ChecklyStream

SCHEMAS_DIR = "tap_checkly/schemas"
OPENAPI_URL = "https://www.checklyhq.com/docs/api-reference/openapi.json"


def main() -> None:  # noqa: C901, PLR0912
    """Main function."""
    response = requests.get(OPENAPI_URL, timeout=60)
    response.raise_for_status()
    spec = response.json()

    tap = TapCheckly(config={"include_paid_streams": True}, validate_config=False)
    normalizer = OpenAPISchemaNormalizer()

    for name, stream in tap.streams.items():
        stream = cast("ChecklyStream", stream)
        ref = stream.openapi_ref
        unresolved = {
            "$ref": f"#/components/schemas/{ref}",
            "components": spec.get("components", {}),
            "x-alt-definitions": spec.get("x-alt-definitions", {}),
        }
        resolved_schema = resolve_schema_references(unresolved)
        resolved_schema.pop("components")
        resolved_schema.pop("x-alt-definitions")

        if name == "check_alerts":
            path = [
                "properties",
                "created_at",
                "format",
            ]
            if get_in(path, resolved_schema) == "date":  # type: ignore[no-untyped-call]
                resolved_schema = assoc_in(resolved_schema, path, "date-time")  # type: ignore[no-untyped-call]

        if name == "status_pages":
            path = [
                "properties",
                "created_at",
                "format",
            ]
            if get_in(path, resolved_schema) == "date":  # type: ignore[no-untyped-call]
                resolved_schema = assoc_in(resolved_schema, path, "date-time")  # type: ignore[no-untyped-call]

            path = [
                "properties",
                "updated_at",
                "format",
            ]
            if get_in(path, resolved_schema) == "date":  # type: ignore[no-untyped-call]
                resolved_schema = assoc_in(resolved_schema, path, "date-time")  # type: ignore[no-untyped-call]

            path = [
                "properties",
                "cards",
                "items",
                "properties",
                "created_at",
                "format",
            ]
            if get_in(path, resolved_schema) == "date":  # type: ignore[no-untyped-call]
                resolved_schema = assoc_in(resolved_schema, path, "date-time")  # type: ignore[no-untyped-call]

            path = [
                "properties",
                "cards",
                "items",
                "properties",
                "updated_at",
                "format",
            ]
            if get_in(path, resolved_schema) == "date":  # type: ignore[no-untyped-call]
                resolved_schema = assoc_in(resolved_schema, path, "date-time")  # type: ignore[no-untyped-call]

            path = [
                "properties",
                "cards",
                "items",
                "properties",
                "services",
                "items",
                "properties",
                "created_at",
                "format",
            ]
            if get_in(path, resolved_schema) == "date":  # type: ignore[no-untyped-call]
                resolved_schema = assoc_in(resolved_schema, path, "date-time")  # type: ignore[no-untyped-call]

            path = [
                "properties",
                "cards",
                "items",
                "properties",
                "services",
                "items",
                "properties",
                "updated_at",
                "format",
            ]
            if get_in(path, resolved_schema) == "date":  # type: ignore[no-untyped-call]
                resolved_schema = assoc_in(resolved_schema, path, "date-time")  # type: ignore[no-untyped-call]

        if name == "status_page_incidents":
            paths = [
                ["properties", "created_at", "format"],
                ["properties", "updated_at", "format"],
                ["properties", "services", "items", "properties", "created_at", "format"],
                ["properties", "services", "items", "properties", "updated_at", "format"],
                ["properties", "incidentUpdates", "items", "properties", "created_at", "format"],
            ]
            for path in paths:
                if get_in(path, resolved_schema) == "date":  # type: ignore[no-untyped-call]
                    resolved_schema = assoc_in(resolved_schema, path, "date-time")  # type: ignore[no-untyped-call]
        if name == "status_page_services":
            path = [
                "properties",
                "created_at",
                "format",
            ]
            if get_in(path, resolved_schema) == "date":  # type: ignore[no-untyped-call]
                resolved_schema = assoc_in(resolved_schema, path, "date-time")  # type: ignore[no-untyped-call]

            path = [
                "properties",
                "updated_at",
                "format",
            ]
            if get_in(path, resolved_schema) == "date":  # type: ignore[no-untyped-call]
                resolved_schema = assoc_in(resolved_schema, path, "date-time")  # type: ignore[no-untyped-call]

        resolved_schema = normalizer.preprocess_schema(resolved_schema, key_properties=stream.primary_keys)

        content = json.dumps(resolved_schema, indent=2)
        with open(f"{SCHEMAS_DIR}/{name}.json", "w") as f:  # noqa: PTH123
            f.write(content + "\n")


if __name__ == "__main__":
    main()
