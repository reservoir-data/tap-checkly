"""Stream type classes for tap-checkly."""

from __future__ import annotations

from tap_checkly.client import (
    ChecklyIncrementalStream,
    ChecklyPaginatedStream,
    ChecklyStream,
)


class AlertChannels(ChecklyPaginatedStream):
    """Alert channels."""

    name = "alert_channels"
    path = "/alert-channels"
    primary_keys = ["id"]
    # replication_key = "updated_at"
    openapi_ref = "AlertChannel"


class AlertNotifications(ChecklyIncrementalStream):
    """Alert notification.

    Alert notifications that have been sent for your account.
    """

    name = "alert_notifications"
    path = "/alert-notifications"
    primary_keys = ["id"]
    replication_key = "timestamp"
    openapi_ref = "AlertNotification"


class Checks(ChecklyPaginatedStream):
    """Checks."""

    name = "checks"
    path = "/checks"
    primary_keys = ["id"]
    # replication_key = "updated_at"
    openapi_ref = "Check"


class CheckAlerts(ChecklyIncrementalStream):
    """Check alerts."""

    name = "check_alerts"
    path = "/check-alerts"
    primary_keys = ["id"]
    replication_key = "created_at"
    openapi_ref = "CheckAlert"


class CheckGroups(ChecklyPaginatedStream):
    """Check groups."""

    name = "check_groups"
    path = "/check-groups"
    primary_keys = ["id"]
    openapi_ref = "CheckGroup"


class Dashboards(ChecklyPaginatedStream):
    """Dashboards.

    All current dashboards in your account.
    """

    name = "dashboards"
    path = "/dashboards"
    primary_keys = ["dashboardId"]
    openapi_ref = "Dashboard"


class EnvironmentVariables(ChecklyStream):
    """Environment variables.

    Note: Pagination seems to be broken for this endpoint.
    """

    name = "variables"
    path = "/variables"
    primary_keys = ["key"]
    openapi_ref = "EnvironmentVariable"


class Locations(ChecklyStream):
    """Locations."""

    name = "locations"
    path = "/locations"
    primary_keys = ["region"]
    openapi_ref = "Location"


class MaintenanceWindows(ChecklyPaginatedStream):
    """Maintenance windows."""

    name = "maintenance_windows"
    path = "/maintenance-windows"
    primary_keys = ["id"]
    openapi_ref = "MaintenanceWindow"


class PrivateLocations(ChecklyStream):
    """Private locations."""

    name = "private_locations"
    path = "/private-locations"
    primary_keys = ["id"]
    openapi_ref = "privateLocationsSchema"


class Runtimes(ChecklyStream):
    """Runtimes."""

    name = "runtimes"
    path = "/runtimes"
    primary_keys = ["name"]
    openapi_ref = "Runtime"


class Snippets(ChecklyPaginatedStream):
    """Snippets."""

    name = "snippets"
    path = "/snippets"
    primary_keys = ["id"]
    replication_key = "updated_at"
    openapi_ref = "Snippet"
