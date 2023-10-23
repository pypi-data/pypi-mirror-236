"""CQRS core components."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar


@dataclass(frozen=True)
class UseCaseOutput:
    """UseCase Output container."""


@dataclass(frozen=True)
class Command:
    """
    Command baseclass.

    In order to make changes to our system we'll need commands. These
    are the simplest components of any CQRS system and consist of little more than
    packaged data.
    """


@dataclass(frozen=True)
class DomainEvent:
    """
    Domain Event base class.

    A `DomainEvent` represents any business change in the state of an `Aggregate`.
    `DomainEvents` are inmutable, and when [event sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
    is used they are the single source of truth.

    The name of a `DomainEvent` should always be in the past tense, e.g.,
    - AdminPrivilegesGranted
    - EmailAddressChanged
    - DependencyAdded

    To simplify serialization, an event should be an enum, and each variant should carry
    any important information.
    """


C = TypeVar("C", bound=Command)
E = TypeVar("E", bound=DomainEvent)
OUT = TypeVar("OUT", bound=UseCaseOutput)
