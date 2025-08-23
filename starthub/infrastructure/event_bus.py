from typing import Any

from loguru import logger

from domain.enums.event import AnyEventType
from domain.ports.event import AbstractEvent, AbstractEventBus, AbstractEventHandler
from infrastructure.utils.singleton import singleton


@singleton
class EventBus(AbstractEventBus):
    _handlers: dict[AnyEventType, list[AbstractEventHandler[AbstractEvent]]] = dict()

    def subscribe(self, event_type: AnyEventType, handler: AbstractEventHandler[Any]) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: AbstractEvent) -> None:
        logger.debug(f"Publishing event {event.event_type}")
        handlers = self._handlers.get(event.event_type, [])

        for handler in handlers:
            try:
                logger.info(f"Started handling event '{event.event_type}' with handler {handler.__class__.__name__}")
                handler.handle(event)

            except Exception as e:
                logger.error(f"Error handling event {event.event_type}: {e} \n" f"Handler: {handler}")
                raise e
