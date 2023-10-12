"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

from typing import Any

from singer_sdk.testing import get_tap_test_class

from tap_checkly.tap import TapCheckly

SAMPLE_CONFIG: dict[str, Any] = {}

TestTapCheckly = get_tap_test_class(TapCheckly, config=SAMPLE_CONFIG)
