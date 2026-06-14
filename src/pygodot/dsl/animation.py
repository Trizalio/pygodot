"""Animation declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pygodot.dsl.values import NodePath


@dataclass(slots=True)
class AnimationKey:
    time: float
    value: Any
    transition: float = 1.0


@dataclass(slots=True)
class ValueTrack:
    path: NodePath
    keys: list[AnimationKey]
    update: int = 0
    interp: int = 1
    loop_wrap: bool = True


@dataclass(slots=True)
class Animation:
    name: str
    length: float
    tracks: list[ValueTrack]
    loop: bool = False


def animation(name: str, *, length: float, tracks: list[ValueTrack], loop: bool = False) -> Animation:
    return Animation(name=name, length=length, tracks=tracks, loop=loop)


def value_track(
    path: str | NodePath,
    *,
    keys: list[AnimationKey],
    update: int = 0,
    interp: int = 1,
    loop_wrap: bool = True,
) -> ValueTrack:
    return ValueTrack(
        path=path if isinstance(path, NodePath) else NodePath(path),
        keys=keys,
        update=update,
        interp=interp,
        loop_wrap=loop_wrap,
    )


def key(time: float, value: Any, *, transition: float = 1.0) -> AnimationKey:
    return AnimationKey(time=time, value=value, transition=transition)
