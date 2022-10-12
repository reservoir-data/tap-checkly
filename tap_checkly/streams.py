"""Stream type classes for tap-checkly."""

from __future__ import annotations

from tap_checkly.client import ChecklyStream


class AlertChannels(ChecklyStream):
    """Alert channels."""

    name = "alert_channels"
    path = "/alert-channels"
    primary_keys = ["id"]
    # replication_key = "updated_at"
    openapi_ref = "AlertChannel"


class AlertNotifications(ChecklyStream):
    """Alert notification.

    Alert notifications that have been sent for your account.
    """

    name = "alert_notifications"
    path = "/alert-notifications"
    primary_keys = ["id"]
    replication_key = "timestamp"
    openapi_ref = "AlertNotification"


class CheckAlerts(ChecklyStream):
    """Check alerts."""

    name = "check_alerts"
    path = "/check-alerts"
    primary_keys = ["id"]
    openapi_ref = "CheckAlert"


class Checks(ChecklyStream):
    """Checks."""

    name = "checks"
    path = "/checks"
    primary_keys = ["id"]
    # replication_key = "updated_at"
    openapi_ref = "Check"


class Dashboards(ChecklyStream):
    """Dashboards.

    All current dashboards in your account.
    """

    name = "dashboards"
    path = "/dashboards"
    primary_keys = ["dashboardId"]
    openapi_ref = "Dashboard"


class CheckGroups(ChecklyStream):
    """Check groups."""

    name = "check_groups"
    path = "/check-groups"
    primary_keys = ["id"]
    openapi_ref = "CheckGroup"


class EnvironmentVariables(ChecklyStream):
    """Environment variables."""

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


class MaintenanceWindows(ChecklyStream):
    """Maintenance windows."""

    name = "maintenance_windows"
    path = "/maintenance-windows"
    primary_keys = ["id"]
    openapi_ref = "MaintenanceWindow"


class Runtimes(ChecklyStream):
    """Runtimes."""

    name = "runtimes"
    path = "/runtimes"
    primary_keys = ["name"]
    openapi_ref = "Runtime"


class Snippets(ChecklyStream):
    """Snippets."""

    name = "snippets"
    path = "/snippets"
    primary_keys = ["id"]
    replication_key = "updated_at"
    openapi_ref = "Snippet"
