var selected_action := ""

@onready var status_label := $Panel/VBox/Footer/StatusLabel

func _ready() -> void:
    status_label.text = "Ready for LD49 scene flow"

func _on_menu_action(action: String) -> void:
    selected_action = action
    status_label.text = "Selected: %s" % action

func _on_exit_pressed() -> void:
    get_tree().quit()
