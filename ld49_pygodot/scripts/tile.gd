signal spell_dropped(tile_id: String, spell_id: String, display_name: String)

@export var tile_id := "A1"

@onready var title := $VBox/Label
@onready var state := $VBox/State
var highlighted := false
var flash_tween: Tween
var unit_summary := ""

func _ready() -> void:
    set_process(false)
    title.text = tile_id
    reset_state()

func reset_state() -> void:
    unit_summary = ""
    _refresh_state("Empty")
    _clear_highlight()

func set_unit(display_name: String, hp: int, status: String) -> void:
    unit_summary = "%s:%d" % [display_name.substr(0, 3), hp]
    if not status.is_empty() and status != "ready":
        unit_summary = "%s %s" % [unit_summary, _status_abbrev(status)]
    _refresh_state(unit_summary)

func clear_unit() -> void:
    unit_summary = ""
    _refresh_state("Empty")

func _process(_delta: float) -> void:
    if highlighted and not get_global_rect().has_point(get_global_mouse_position()):
        _clear_highlight()

func _can_drop_data(_at_position: Vector2, data: Variant) -> bool:
    var can_drop: bool = data is Dictionary and data.get("type") == "spell"
    if can_drop:
        _set_highlight(true)
    return can_drop

func _drop_data(_at_position: Vector2, data: Variant) -> void:
    var spell_id := str(data.get("spell_id", "unknown"))
    var display_name := str(data.get("display_name", spell_id))
    _clear_highlight()
    _refresh_state(display_name)
    _flash(Color(1.0, 0.45, 0.25, 1.0))
    spell_dropped.emit(tile_id, spell_id, display_name)

func _notification(what: int) -> void:
    if what == NOTIFICATION_DRAG_END:
        _clear_highlight()

func _set_highlight(enabled: bool) -> void:
    if highlighted == enabled:
        return
    highlighted = enabled
    set_process(enabled)
    modulate = Color(1.0, 0.85, 0.35, 1.0) if enabled else Color.WHITE

func _clear_highlight() -> void:
    highlighted = false
    set_process(false)
    modulate = Color.WHITE

func _flash(color: Color) -> void:
    if flash_tween:
        flash_tween.kill()
    modulate = color
    flash_tween = create_tween()
    flash_tween.tween_property(self, "modulate", Color.WHITE, 0.35)

func _refresh_state(text: String) -> void:
    state.text = text

func _status_abbrev(status: String) -> String:
    match status:
        "burning":
            return "Brn"
        "frozen":
            return "Frz"
        "shielded":
            return "Shd"
        "healed":
            return "Hld"
        "moving":
            return "Mov"
        "defeated":
            return "Def"
        _:
            return status.substr(0, 3)
