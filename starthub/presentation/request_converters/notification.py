from django.http import QueryDict
from domain.value_objects.notification import NotificationGetCommand
from rest_framework.request import Request


def request_to_notification_get_command(request: Request) -> NotificationGetCommand:
    params: QueryDict = request.query_params
    is_read_raw: str | None = params.get("is_read")

    is_read: bool | None = None
    if is_read_raw == "true":
        is_read = True
    if is_read_raw == "false":
        is_read = False

    return NotificationGetCommand(is_read=is_read)
