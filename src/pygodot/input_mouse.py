"""Supported Godot mouse button names for InputMap generation."""

from __future__ import annotations


_MOUSE_BUTTONS = {
    "LEFT": 1,
    "RIGHT": 2,
    "MIDDLE": 3,
    "WHEEL_UP": 4,
    "WHEEL_DOWN": 5,
    "WHEEL_LEFT": 6,
    "WHEEL_RIGHT": 7,
    "XBUTTON1": 8,
    "XBUTTON2": 9,
}


def normalize_mouse_button_name(name: str) -> str:
    return name.strip().upper().replace(" ", "_").replace("-", "_")


def mouse_button_index_for(name: str) -> int | None:
    return _MOUSE_BUTTONS.get(normalize_mouse_button_name(name))
