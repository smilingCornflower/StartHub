from domain.enums.event import EventTypeEnum
from domain.ports.event import AbstractEventBus, AbstractEventHandler
from domain.value_objects.event import DomainEvent
from infrastructure.utils.singleton import singleton
from loguru import logger


@singleton
class DjEventBus(AbstractEventBus[DomainEvent]):
    _handlers: dict[EventTypeEnum, list[AbstractEventHandler]] = dict()

    def subscribe(self, event_type: EventTypeEnum, handler: AbstractEventHandler) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: DomainEvent) -> None:
        handlers = self._handlers.get(event.event_type, [])

        for handler in handlers:
            try:
                handler.handle(event)
            except Exception as e:
                logger.error(f"Error handling event {event.event_type}: {e} \n" f"Handler: {handler}")
                raise e
