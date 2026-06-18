signal spell_dropped(tile_id: String, spell_id: String, display_name: String)
signal spell_hovered(tile_id: String, spell_id: String)
signal spell_hover_ended()

@export var tile_id := "A1"

@onready var title := $VBox/Label
@onready var unit_label := $VBox/Unit
@onready var state := $VBox/State
var highlighted := false
var preview_active := false
var preview_spell_id := ""
var flash_tween: Tween
var unit_summary := ""
var state_text := ""

func _ready() -> void:
    set_process(false)
    title.text = tile_id
    reset_state()

func reset_state() -> void:
    unit_summary = ""
    _refresh_unit("Empty")
    _refresh_state("")
    clear_preview()
    _clear_highlight()

func set_unit(display_name: String, hp: int, status: String) -> void:
    unit_summary = "%s HP %d" % [display_name, hp]
    _refresh_unit(unit_summary)
    if status.is_empty() or status == "ready":
        _refresh_state("")
    else:
        _refresh_state(_status_label(status))
        _flash(_status_color(status))

func clear_unit() -> void:
    unit_summary = ""
    _refresh_unit("Empty")
    _refresh_state("")

func _process(_delta: float) -> void:
    if highlighted and not get_global_rect().has_point(get_global_mouse_position()):
        _clear_highlight()

func _can_drop_data(_at_position: Vector2, data: Variant) -> bool:
    var can_drop: bool = data is Dictionary and data.get("type") == "spell"
    if can_drop:
        var spell_id := str(data.get("spell_id", "unknown"))
        _set_highlight(true)
        if preview_spell_id != spell_id:
            preview_spell_id = spell_id
            spell_hovered.emit(tile_id, spell_id)
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
        spell_hover_ended.emit()

func _set_highlight(enabled: bool) -> void:
    if highlighted == enabled:
        return
    highlighted = enabled
    set_process(enabled)
    modulate = Color(1.0, 0.85, 0.35, 1.0) if enabled else Color.WHITE

func _clear_highlight() -> void:
    if not highlighted and preview_spell_id.is_empty():
        return
    highlighted = false
    preview_spell_id = ""
    set_process(false)
    if not preview_active:
        modulate = Color.WHITE

func set_preview(role: String, spell_id: String) -> void:
    preview_active = true
    var label := "Area"
    if role == "primary":
        label = "Target"
    state.text = "%s %s" % [_spell_label(spell_id), label]
    if role == "primary":
        modulate = Color(1.0, 0.8, 0.2, 1.0)
    else:
        modulate = _preview_color(spell_id)

func set_movement_preview(role: String, outcome: String) -> void:
    preview_active = true
    state.text = _movement_preview_label(role, outcome)
    modulate = _movement_preview_color(role, outcome)

func clear_preview() -> void:
    if not preview_active:
        return
    preview_active = false
    state.text = state_text
    modulate = Color.WHITE

func _flash(color: Color) -> void:
    if flash_tween:
        flash_tween.kill()
    modulate = color
    flash_tween = create_tween()
    flash_tween.tween_property(self, "modulate", Color.WHITE, 0.35)

func _refresh_state(text: String) -> void:
    state_text = text
    if not preview_active:
        state.text = text

func _refresh_unit(text: String) -> void:
    unit_label.text = text

func _status_label(status: String) -> String:
    match status:
        "burning":
            return "Burning"
        "frozen":
            return "Frozen"
        "shielded":
            return "Shield"
        "healed":
            return "Healed"
        "moving":
            return "Moving"
        "defeated":
            return "Defeated"
        "scorched":
            return "Scorch"
        "horde":
            return "Horde"
        "braced":
            return "Braced"
        "stacked":
            return "Stack"
        "raging":
            return "Rage"
        _:
            return status.capitalize()

func _status_color(status: String) -> Color:
    match status:
        "burning", "scorched", "raging":
            return Color(1.0, 0.45, 0.25, 1.0)
        "frozen":
            return Color(0.45, 0.75, 1.0, 1.0)
        "shielded", "braced", "stacked":
            return Color(0.45, 0.9, 0.65, 1.0)
        "healed", "horde":
            return Color(0.7, 1.0, 0.5, 1.0)
        "moving":
            return Color(1.0, 0.85, 0.35, 1.0)
        "blocked", "clash":
            return Color(1.0, 0.55, 0.45, 1.0)
        _:
            return Color(1.0, 0.85, 0.35, 1.0)

func _spell_label(spell_id: String) -> String:
    match spell_id:
        "fireball":
            return "Fire"
        "frost":
            return "Frost"
        "shield":
            return "Shield"
        "heal":
            return "Heal"
        _:
            return spell_id.capitalize()

func _preview_color(spell_id: String) -> Color:
    match spell_id:
        "fireball":
            return Color(1.0, 0.55, 0.35, 1.0)
        "frost":
            return Color(0.5, 0.78, 1.0, 1.0)
        "shield":
            return Color(0.5, 0.95, 0.65, 1.0)
        "heal":
            return Color(0.75, 1.0, 0.5, 1.0)
        _:
            return Color(1.0, 0.85, 0.35, 1.0)

func _movement_preview_label(role: String, outcome: String) -> String:
    if outcome == "frozen":
        return "Frozen"
    if outcome == "castle":
        return "Castle"
    if outcome == "blocked":
        return "Block" if role == "to" else "Move"
    return "Next" if role == "to" else "Move"

func _movement_preview_color(role: String, outcome: String) -> Color:
    if outcome == "frozen":
        return Color(0.45, 0.75, 1.0, 1.0)
    if outcome == "castle":
        return Color(1.0, 0.9, 0.45, 1.0)
    if outcome == "blocked":
        return Color(1.0, 0.5, 0.45, 1.0)
    if role == "to":
        return Color(0.55, 0.85, 1.0, 1.0)
    return Color(1.0, 0.85, 0.35, 1.0)
