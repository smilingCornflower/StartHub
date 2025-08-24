from domain.exceptions.notification import NotificationNotFounException
from domain.models.notification import Notification
from domain.repositories.notification import NotificationReadRepository, NotificationWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import NotificationFilter
from domain.value_objects.notification import NotificationCreatePayload, NotificationId, NotificationUpdatePayload
from infrastructure.repositories.pagination import apply_pagination


class DjNotificationReadRepository(NotificationReadRepository):
    def get_by_id(self, id_: NotificationId) -> Notification:
        """:raises NotificationNotFounException:"""
        notification: Notification | None = Notification.objects.filter(id=id_.value).first()
        if notification is None:
            raise NotificationNotFounException(f"Notification with id = {id_.value} not found.")
        return notification

    def get_all(self, filter_: NotificationFilter, pagination: Pagination | None = None) -> list[Notification]:
        queryset = Notification.objects.all()

        if pagination is not None:
            return apply_pagination(queryset=queryset, pagination=pagination)

        return list(queryset)


class DjNotificationWriteRepository(NotificationWriteRepository):
    def create(self, data: NotificationCreatePayload) -> Notification:
        return Notification.objects.create(
            user_id=data.user_id.value,
            title=data.title.value,
            message=data.message.value,
        )

    def update(self, data: NotificationUpdatePayload) -> Notification:
        """:raises NotificationNotFounException:"""
        notification: Notification | None = Notification.objects.filter(id=data.id_.value).first()
        if notification is None:
            raise NotificationNotFounException(f"Notification with id = {data.id_.value} not found.")

        if data.is_read is not None:
            notification.is_read = data.is_read

        notification.save()
        return notification

    def delete_by_id(self, id_: NotificationId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")
