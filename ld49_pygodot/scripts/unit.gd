@export var unit_id := "unit"
@export var display_name := "Unit"
@export var faction := "neutral"
@export var cell_id := "A1"
@export var hp := 1
@export var status := "ready"

@onready var name_label := $VBox/Name
@onready var stats_label := $VBox/Stats
@onready var status_label := $VBox/Status

func _ready() -> void:
    refresh()

func apply_state(data: Dictionary) -> void:
    display_name = str(data.get("display_name", display_name))
    faction = str(data.get("faction", faction))
    cell_id = str(data.get("cell_id", cell_id))
    hp = int(data.get("hp", hp))
    status = str(data.get("status", status))
    refresh()

func refresh() -> void:
    name_label.text = "%s (%s)" % [display_name, faction]
    stats_label.text = "HP %d @ %s" % [hp, cell_id]
    status_label.text = status
