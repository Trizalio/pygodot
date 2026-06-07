"""Signal connection declarations for the public DSL."""

from dataclasses import dataclass


@dataclass(slots=True)
class SignalConnection:
    signal: str
    target: str
    method: str


def signal(name: str, *, target: str, method: str) -> SignalConnection:
    return SignalConnection(signal=name, target=target, method=method)
