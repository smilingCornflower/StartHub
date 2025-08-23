from contextlib import AbstractContextManager
from types import TracebackType
from typing import Any, Self

from django.db import transaction

from application.ports.uow import AbstractUnitOfWork


class DjangoUnitOfWork(AbstractUnitOfWork):
    _ctx: AbstractContextManager[Any]

    def __enter__(self) -> Self:
        self._ctx = transaction.atomic()
        self._ctx.__enter__()
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        self._ctx.__exit__(exc_type, exc_val, exc_tb)

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        transaction.set_rollback(True)
