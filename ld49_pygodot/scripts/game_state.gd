extends Node

var port_stage := "skeleton"
var last_event := ""

func reset() -> void:
    last_event = "reset"

func describe_state() -> String:
    if last_event.is_empty():
        return "LD49 skeleton ready"
    return "LD49 skeleton: %s" % last_event
