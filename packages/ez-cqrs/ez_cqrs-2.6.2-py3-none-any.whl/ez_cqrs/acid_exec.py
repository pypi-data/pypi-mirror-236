"""ACID execution goodies."""
from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Generic, TypeVar, final

if TYPE_CHECKING:
    from result import Result

    from ez_cqrs.error import DatabaseError


T = TypeVar("T")


@final
@dataclass
class OpsRegistry(Generic[T]):
    """
    Operations registry.

    The intended use case for `OpsRegistry` is to act as an ephemeral
    record of update operations against a database in the execution of a command.

    These update operations would be commited as a single, ACID, transaction agains the
    database before the command execution returns the events recorded.
    """

    max_lenght: int
    _storage: list[T] = field(default_factory=list, init=False)

    def is_empty(self) -> bool:
        """Check `OpsRegistry` storage is empty."""
        return self.storage_length() == 0

    def add(self, value: T) -> None:
        """Add new value to the storage registry."""
        if len(self._storage) >= self.max_lenght:
            msg = "OpsRegistry capacity exceeded."
            raise RuntimeError(msg)
        self._storage.append(value)

    def prune_storage(self) -> None:
        """Prune storage."""
        self._storage.clear()

    def storage_snapshot(self) -> list[T]:
        """Get an snapshot of the storage."""
        return self._storage.copy()

    def storage_length(self) -> int:
        """Get storage length."""
        return len(self._storage)


class ACID(abc.ABC):
    """
    Repository gives acces to the system database layer.

    A database must support transaction operations.

    Besides being the client between the core layer and the persistence layer,
    a system repository is intended to be used right before a command handling
    returns. Before events are returned to the client to be propagated to other
    systems, all update operations recorded during the command execution must be
    commited.
    """

    @abc.abstractmethod
    def commit_as_transaction(
        self,
        ops_registry: OpsRegistry[Any],
    ) -> Result[None, DatabaseError]:
        """
        Commit update operations stored in an `OpsRegistry`.

        The operation is executed as a transaction againts the database.

        After the commit the ops_registry must be pruned.
        """
