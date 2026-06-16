"""Signal connection declarations for the public DSL."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SignalConnection:
    signal: str
    target: str
    method: str
    binds: list[Any] = field(default_factory=list)


def signal(
    name: str,
    *,
    target: str,
    method: str,
    binds: list[Any] | None = None,
) -> SignalConnection:
    return SignalConnection(signal=name, target=target, method=method, binds=binds or [])
