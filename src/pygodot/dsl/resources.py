"""Resource declarations for the public DSL."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ExternalResource:
    path: str
    type: str


def ext_resource(path: str, *, type: str) -> ExternalResource:
    return ExternalResource(path=path, type=type)


def external_resource(path: str, *, type: str) -> ExternalResource:
    return ext_resource(path, type=type)


def texture(path: str) -> ExternalResource:
    return ext_resource(path, type="Texture2D")


def audio_stream(path: str) -> ExternalResource:
    return ext_resource(path, type="AudioStream")


def packed_scene(path: str) -> ExternalResource:
    return ext_resource(path, type="PackedScene")
