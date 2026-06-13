"""Keyboard key names supported by pygodot's minimal InputMap emitter."""

KEYCODES: dict[str, int] = {
    **{chr(code): code for code in range(ord("A"), ord("Z") + 1)},
    **{str(number): ord(str(number)) for number in range(10)},
    "SPACE": 32,
    "ESC": 4194305,
    "ESCAPE": 4194305,
    "ENTER": 4194309,
    "LEFT": 4194319,
    "UP": 4194320,
    "RIGHT": 4194321,
    "DOWN": 4194322,
}


def normalize_key_name(key: str) -> str:
    return key.strip().upper()


def keycode_for(key: str) -> int | None:
    return KEYCODES.get(normalize_key_name(key))
