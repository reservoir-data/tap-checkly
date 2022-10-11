"""Stream type classes for tap-checkly."""

from __future__ import annotations

from singer_sdk import typing as th

from tap_checkly.client import ChecklyStream

CHANNELS = [
    "EMAIL",
    "SLACK",
    "WEBHOOK",
    "SMS",
    "PAGERDUTY",
    "OPSGENIE",
]
STATUS = ["IN_PROGRESS", "SUCCESS", "FAILURE"]
CHECK_TYPES = ["BROWSER", "API"]

KEY_VALUE_OBJECT = th.ObjectType(
    th.Property("key", th.StringType, required=True),
    th.Property("value", th.StringType, required=True),
    th.Property("locked", th.BooleanType, default=False),
)


class AlertChannels(ChecklyStream):
    """Alert channels."""

    name = "alert_channels"
    path = "/alert-channels"
    primary_keys = ["id"]
    # replication_key = "updated_at"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType, description="The channel's system ID"),
        th.Property(
            "type",
            th.StringType,
            description="The type of alert channel, i.e. EMAIL or SLACK.",
            # enum=CHANNELS,
        ),
        th.Property("config", th.ObjectType()),
        th.Property(
            "subscriptions",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("checkId", th.StringType),
                    th.Property("groupId", th.IntegerType),
                    th.Property("activated", th.BooleanType, required=True),
                ),
            ),
        ),
        th.Property("sendRecovery", th.BooleanType),
        th.Property("sendFailure", th.BooleanType),
        th.Property("sendDegraded", th.BooleanType),
        th.Property("sslExpiry", th.BooleanType),
        th.Property("sslExpiryThreshold", th.IntegerType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()


class AlertNotifications(ChecklyStream):
    """Alert notification.

    Alert notifications that have been sent for your account.
    """

    name = "alert_notifications"
    path = "/alert-notifications"
    primary_keys = ["id"]
    replication_key = "timestamp"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType, description="The notification's system ID"),
        th.Property(
            "type",
            th.StringType,
            description="The type of alert channel (SMS, Slack, Webhook, etc).",
            # enum=CHANNELS,
        ),
        th.Property(
            "status",
            th.StringType,
            description="The status of the alert.",
            # enum=STATUS,
        ),
        th.Property("alertConfig", th.ObjectType()),
        th.Property(
            "notificationResult",
            th.StringType,
            description=(
                "The result of sending the alert notification. For example, this could "
                "be the response body of the Webhook."
            ),
        ),
        th.Property(
            "timestamp",
            th.DateTimeType,
            description="The time that the alert was sent.",
        ),
        th.Property(
            "checkType",
            th.StringType,
            description="The type of the check.",
            # enum=CHECK_TYPES,
        ),
        th.Property("checkId", th.StringType, description="The ID of the check."),
        th.Property(
            "checkAlertId",
            th.StringType,
            description="The ID of the check alert.",
        ),
        th.Property(
            "alertChannelId",
            th.IntegerType,
            description="The ID of the alert channel which this alert was sent to.",
        ),
        th.Property(
            "checkResultId",
            th.StringType,
            description="The ID of the corresponding check result.",
        ),
    ).to_dict()


class CheckAlerts(ChecklyStream):
    """Check alerts."""

    name = "check_alerts"
    path = "/check-alerts"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType, description="The unique ID of this alert."),
        th.Property(
            "name",
            th.StringType,
            description="The name of the check.",
            required=True,
        ),
        th.Property(
            "checkId",
            th.StringType,
            description="The ID of the check this alert belongs to.",
        ),
        th.Property("alertType", th.StringType, description="The type of alert."),
        th.Property(
            "checkType",
            th.StringType,
            description="The type of the check.",
            # enum=CHECK_TYPES,
        ),
        th.Property(
            "runLocation",
            th.StringType,
            description="What data center location this check was triggered from.",
            # example="us-east-1",
        ),
        th.Property(
            "responseTime",
            th.NumberType,
            description=(
                "Describes the time it took to execute relevant parts of this check. "
                "Any setup time or system time needed to start executing this check in "
                "the Checkly backend is not part of this."
            ),
        ),
        th.Property(
            "error",
            th.StringType,
            description=(
                "Any specific error messages that were part of the failing check "
                "triggering the alert."
            ),
        ),
        th.Property(
            "statusCode",
            th.StringType,
            description="The status code of the response. Only applies to API checks.",
        ),
        th.Property(
            "created_at",
            th.DateTimeType,
            description="The date and time this check alert was created.",
        ),
        th.Property(
            "startedAt",
            th.DateTimeType,
            description="The date and time this check alert was started.",
        ),
    ).to_dict()


class Checks(ChecklyStream):
    """Checks."""

    name = "checks"
    path = "/checks"
    primary_keys = ["id"]
    # replication_key = "updated_at"

    schema = th.PropertiesList(
        th.Property("id", th.StringType, description="The check's system ID"),
        th.Property("name", th.StringType, description="The name of the check"),
        th.Property(
            "activated",
            th.BooleanType,
            description="Determines if the check is running or not.",
        ),
        th.Property(
            "muted",
            th.BooleanType,
            description=(
                "Determines if any notifications will be send out when a check fails "
                "and/or recovers."
            ),
        ),
        th.Property(
            "doubleCheck",
            th.BooleanType,
            description=(
                'Setting this to "true" will trigger a retry when a check fails from '
                "the failing region and another, randomly selected region before "
                "marking the check as failed."
            ),
        ),
        th.Property(
            "shouldFail",
            th.BooleanType,
            description=(
                "Allows to invert the behaviour of when a check is considered to fail. "
                "Allows for validating error status like 404."
            ),
        ),
        th.Property(
            "locations",
            th.ArrayType(th.StringType),
            description=(
                "An array of one or more data center locations where to run this check."
            ),
        ),
        th.Property(
            "tags",
            th.ArrayType(th.StringType),
            description="Tags for organizing and filtering checks.",
        ),
        th.Property(
            "alertSettings",
            th.ObjectType(
                th.Property(
                    "escalationType",
                    th.StringType,
                    description="Determines what type of escalation to use.",
                    # enum=["RUN_BASED", "TIME_BASED"],
                ),
                th.Property(
                    "runBasedEscalation",
                    th.ObjectType(
                        th.Property(
                            "failedRunThreshold",
                            th.NumberType,
                            description=(
                                "After how many failed consecutive check runs an alert "
                                "notification should be send."
                            ),
                            # enum=[1, 2, 3, 4, 5],
                        ),
                    ),
                ),
                th.Property(
                    "timeBasedEscalation",
                    th.ObjectType(
                        th.Property(
                            "minutesFailingThreshold",
                            th.NumberType,
                            description=(
                                "After how many minutes after a check starts failing "
                                "an alert should be send."
                            ),
                            # enum=[5, 10, 15, 30],
                        ),
                    ),
                ),
                th.Property(
                    "reminders",
                    th.ObjectType(
                        th.Property(
                            "amount",
                            th.NumberType,
                            description=(
                                "How many reminders to send out after the initial "
                                "alert notification."
                            ),
                            default=0,
                            # enum=[0, 1, 2, 3, 4, 5, 100000],
                        ),
                        th.Property(
                            "interval",
                            th.NumberType,
                            description=(
                                "At what interval the reminders should be send."
                            ),
                            default=5,
                            # enum=[5, 10, 15, 30],
                        ),
                    ),
                ),
            ),
            description="Alert settings.",
            default={},
        ),
        th.Property(
            "useGlobalAlertSettings",
            th.BooleanType,
            description=(
                "When true, the account level alert setting will be used, not the "
                "alert setting defined on this check."
            ),
            default=True,
        ),
        th.Property(
            "groupId",
            th.IntegerType,
            description="The id of the check group this check is part of.",
        ),
        th.Property(
            "groupOrder",
            th.IntegerType,
            description=(
                "The position of this check in a check group. It determines in what "
                "order checks are run when a group is triggered from the API or from "
                "CI/CD."
            ),
        ),
        th.Property(
            "runtimeId",
            th.StringType,
            description=(
                "The runtime version, i.e. fixed set of runtime dependencies, used to "
                "execute this check."
            ),
        ),
        th.Property(
            "alertChannelSubscriptions",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "alertChannelId",
                        th.IntegerType,
                        required=True,
                    ),
                    th.Property(
                        "activated",
                        th.BooleanType,
                        default=True,
                        required=True,
                    ),
                ),
            ),
        ),
        th.Property(
            "checkType",
            th.StringType,
            description="The type of the check.",
            # enum=CHECK_TYPES,
        ),
        th.Property(
            "frequency",
            th.NumberType,
            description="How often the check should run in minutes.",
        ),
        th.Property(
            "frequencyOffset",
            th.IntegerType,
        ),
        th.Property(
            "request",
            th.ObjectType(),
        ),
        th.Property(
            "script",
            th.StringType,
        ),
        th.Property(
            "environmentVariables",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "key",
                        th.StringType,
                        description=(
                            "The key of the environment variable (this value cannot be "
                            "changed)."
                        ),
                        required=True,
                    ),
                    th.Property(
                        "value",
                        th.StringType,
                        description="The value of the environment variable.",
                        required=True,
                    ),
                    th.Property(
                        "locked",
                        th.BooleanType,
                        description=(
                            "Used only in the UI to hide the value like a password."
                        ),
                        default=False,
                    ),
                ),
            ),
        ),
        th.Property(
            "setupSnippetId",
            th.IntegerType,
            description=(
                "An ID reference to a snippet to use in the setup phase of an API "
                "check."
            ),
        ),
        th.Property(
            "tearDownSnippetId",
            th.IntegerType,
            description=(
                "An ID reference to a snippet to use in the teardown phase of an API "
                "check."
            ),
        ),
        th.Property(
            "localSetupScript",
            th.StringType,
            description="A valid piece of Node.js code to run in the setup phase.",
        ),
        th.Property(
            "localTearDownScript",
            th.StringType,
            description="A valid piece of Node.js code to run in the teardown phase.",
        ),
        th.Property(
            "degradedResponseTime",
            th.NumberType,
            description=(
                "The response time in milliseconds where a check should be considered "
                "degraded."
            ),
        ),
        th.Property(
            "maxResponseTime",
            th.NumberType,
            description=(
                "The response time in milliseconds where a check should be considered "
                "failing."
            ),
        ),
        th.Property(
            "alertChannels",
            th.ObjectType(
                th.Property(
                    "email",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("address", th.StringType, required=True),
                        ),
                    ),
                ),
                th.Property(
                    "webhook",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("name", th.StringType),
                            th.Property("url", th.StringType, required=True),
                            th.Property(
                                "method",
                                th.StringType,
                                default="POST",
                                # enum=["GET", "POST", "PUT", "HEAD", "DELETE", "PATCH"],
                            ),
                            th.Property("headers", th.ArrayType(KEY_VALUE_OBJECT)),
                            th.Property(
                                "queryParameters", th.ArrayType(KEY_VALUE_OBJECT)
                            ),
                        ),
                    ),
                ),
                th.Property(
                    "slack",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("url", th.StringType, required=True),
                        ),
                    ),
                ),
                th.Property(
                    "sms",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property(
                                "number",
                                th.StringType,
                                required=True,
                                # example="+1234567890",
                            ),
                            th.Property(
                                "name",
                                th.StringType,
                                # example="SMS Alert",
                            ),
                        ),
                    ),
                ),
            ),
        ),
        th.Property(
            "privateLocations",
            th.ArrayType(th.StringType),
            description=(
                "An array of one or more private locations where to run the check."
            ),
            # example=["data-center-eu"],
        ),
        th.Property(
            "created_at",
            th.DateTimeType,
        ),
        th.Property(
            "updated_at",
            th.DateTimeType,
        ),
    ).to_dict()


class Dashboards(ChecklyStream):
    """Dashboards.

    All current dashboards in your account.
    """

    name = "dashboards"
    path = "/dashboards"
    primary_keys = ["dashboardId"]

    schema = th.PropertiesList(
        th.Property(
            "dashboardId",
            th.StringType,
            description="The dashboards's system ID",
        ),
        th.Property(
            "tags",
            th.ArrayType(th.StringType),
            description=(
                "A list of one or more tags that filter which checks to display on the "
                "dashboard."
            ),
        ),
    ).to_dict()


class Locations(ChecklyStream):
    """Locations."""

    name = "locations"
    path = "/locations"
    primary_keys = ["region"]

    schema = th.PropertiesList(
        th.Property(
            "region",
            th.StringType,
            description="The unique identifier of this location.",
            # example="us-east-1",
        ),
        th.Property(
            "name",
            th.StringType,
            description="Friendly name of this location.",
            # example="N. Virginia",
        ),
    ).to_dict()
