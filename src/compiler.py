from __future__ import annotations

import argparse
import importlib.util
import inspect
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ----------------------------
# DSL / IR
# ----------------------------

@dataclass(slots=True)
class SignalConnection:
    signal: str
    target: str
    method: str


@dataclass(slots=True)
class Script:
    path: str
    extends: str
    body: str


@dataclass(slots=True)
class Node:
    name: str
    type: str
    props: dict[str, Any] = field(default_factory=dict)
    children: list["Node"] = field(default_factory=list)
    script: Script | None = None
    signals: list[SignalConnection] = field(default_factory=list)

    def add(self, *children: "Node") -> "Node":
        self.children.extend(children)
        return self


@dataclass(slots=True)
class Scene:
    path: str
    root: Node


def signal(name: str, *, target: str, method: str) -> SignalConnection:
    return SignalConnection(signal=name, target=target, method=method)


def Node2D(name: str, *, children: list[Node] | None = None, script: Script | None = None, **props: Any) -> Node:
    return Node(name=name, type="Node2D", props=props, children=children or [], script=script)


def Control(name: str, *, children: list[Node] | None = None, script: Script | None = None, **props: Any) -> Node:
    return Node(name=name, type="Control", props=props, children=children or [], script=script)


def Label(name: str, *, children: list[Node] | None = None, script: Script | None = None, **props: Any) -> Node:
    return Node(name=name, type="Label", props=props, children=children or [], script=script)


def Button(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Button",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
    )


# ----------------------------
# Godot value serialization
# ----------------------------

class ExtResourceRef:
    def __init__(self, resource_id: str) -> None:
        self.resource_id = resource_id


def gd_string(value: str) -> str:
    # Minimal escaping for MVP.
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def gd_value(value: Any) -> str:
    if isinstance(value, ExtResourceRef):
        return f'ExtResource({gd_string(value.resource_id)})'

    if isinstance(value, str):
        return gd_string(value)

    if isinstance(value, bool):
        return "true" if value else "false"

    if value is None:
        return "null"

    if isinstance(value, int | float):
        return repr(value)

    # MVP convention:
    #   (x, y) -> Vector2
    #   (x, y, z) -> Vector3
    if isinstance(value, tuple):
        if len(value) == 2:
            return f"Vector2({gd_value(value[0])}, {gd_value(value[1])})"
        if len(value) == 3:
            return f"Vector3({gd_value(value[0])}, {gd_value(value[1])}, {gd_value(value[2])})"

    if isinstance(value, list):
        return "[" + ", ".join(gd_value(v) for v in value) + "]"

    if isinstance(value, dict):
        items = ", ".join(f"{gd_value(k)}: {gd_value(v)}" for k, v in value.items())
        return "{" + items + "}"

    raise TypeError(f"Unsupported Godot value: {value!r} ({type(value).__name__})")


# ----------------------------
# Compiler
# ----------------------------

@dataclass(slots=True)
class ExternalResource:
    type: str
    path: str
    id: str


class Compiler:
    def __init__(self, project_dir: Path) -> None:
        self.project_dir = project_dir
        self.ext_resources: dict[str, ExternalResource] = {}

    def compile_scene(self, scene: Scene) -> None:
        self._validate_scene(scene)
        self._write_project_file(scene)
        self._write_scripts(scene.root)

        scene_rel_path = self._res_to_rel(scene.path)
        scene_abs_path = self.project_dir / scene_rel_path
        scene_abs_path.parent.mkdir(parents=True, exist_ok=True)
        scene_abs_path.write_text(self._emit_tscn(scene), encoding="utf-8")

    def _validate_scene(self, scene: Scene) -> None:
        if not scene.path.startswith("res://"):
            raise ValueError(f"Scene path must start with res://, got {scene.path!r}")

        if "/" in scene.root.name:
            raise ValueError("Root node name must not contain '/'")

        self._validate_node(scene.root)

    def _validate_node(self, node: Node) -> None:
        if not node.name:
            raise ValueError("Node name must not be empty")

        if "/" in node.name:
            raise ValueError(f"Node name must not contain '/': {node.name!r}")

        seen: set[str] = set()
        for child in node.children:
            if child.name in seen:
                raise ValueError(f"Duplicate child node name {child.name!r} under {node.name!r}")
            seen.add(child.name)
            self._validate_node(child)

    def _write_project_file(self, scene: Scene) -> None:
        project_file = self.project_dir / "project.godot"
        project_file.parent.mkdir(parents=True, exist_ok=True)

        content = f"""\
; Generated by pygodot prototype.

config_version=5

[application]

config/name="GeneratedGame"
run/main_scene="{scene.path}"
"""
        project_file.write_text(content, encoding="utf-8")

    def _write_scripts(self, node: Node) -> None:
        if node.script is not None:
            script_rel_path = self._res_to_rel(node.script.path)
            script_abs_path = self.project_dir / script_rel_path
            script_abs_path.parent.mkdir(parents=True, exist_ok=True)

            body = inspect.cleandoc(node.script.body)
            content = f"extends {node.script.extends}\n\n{body}\n"
            script_abs_path.write_text(content, encoding="utf-8")

            resource_id = self._resource_id_for_path(node.script.path, prefix="Script")
            self.ext_resources[node.script.path] = ExternalResource(
                type="Script",
                path=node.script.path,
                id=resource_id,
            )

        for child in node.children:
            self._write_scripts(child)

    def _emit_tscn(self, scene: Scene) -> str:
        self.ext_resources.clear()
        self._collect_ext_resources(scene.root)

        lines: list[str] = []

        load_steps = len(self.ext_resources) + 1
        if self.ext_resources:
            lines.append(f"[gd_scene load_steps={load_steps} format=3]")
        else:
            lines.append("[gd_scene format=3]")
        lines.append("")

        for resource in self.ext_resources.values():
            lines.append(
                f'[ext_resource type={gd_string(resource.type)} '
                f'path={gd_string(resource.path)} '
                f'id={gd_string(resource.id)}]'
            )

        if self.ext_resources:
            lines.append("")

        self._emit_node(lines, scene.root, parent_path=None)

        connections: list[str] = []
        self._emit_connections(connections, scene.root, current_path=".")

        if connections:
            lines.append("")
            lines.extend(connections)

        return "\n".join(lines).rstrip() + "\n"

    def _collect_ext_resources(self, node: Node) -> None:
        if node.script is not None:
            resource_id = self._resource_id_for_path(node.script.path, prefix="Script")
            self.ext_resources[node.script.path] = ExternalResource(
                type="Script",
                path=node.script.path,
                id=resource_id,
            )

        for child in node.children:
            self._collect_ext_resources(child)

    def _emit_node(self, lines: list[str], node: Node, parent_path: str | None) -> None:
        if parent_path is None:
            lines.append(f'[node name={gd_string(node.name)} type={gd_string(node.type)}]')
        else:
            lines.append(
                f'[node name={gd_string(node.name)} '
                f'type={gd_string(node.type)} '
                f'parent={gd_string(parent_path)}]'
            )

        if node.script is not None:
            resource_id = self.ext_resources[node.script.path].id
            lines.append(f"script = {gd_value(ExtResourceRef(resource_id))}")

        for key, value in node.props.items():
            lines.append(f"{key} = {gd_value(value)}")

        lines.append("")

        child_parent_path = "." if parent_path is None else (
            node.name if parent_path == "." else f"{parent_path}/{node.name}"
        )

        for child in node.children:
            self._emit_node(lines, child, parent_path=child_parent_path)

    def _emit_connections(self, lines: list[str], node: Node, current_path: str) -> None:
        for conn in node.signals:
            lines.append(
                f'[connection signal={gd_string(conn.signal)} '
                f'from={gd_string(current_path)} '
                f'to={gd_string(conn.target)} '
                f'method={gd_string(conn.method)}]'
            )

        for child in node.children:
            child_path = child.name if current_path == "." else f"{current_path}/{child.name}"
            self._emit_connections(lines, child, current_path=child_path)

    def _res_to_rel(self, path: str) -> Path:
        if not path.startswith("res://"):
            raise ValueError(f"Expected res:// path, got {path!r}")
        return Path(path.removeprefix("res://"))

    def _resource_id_for_path(self, path: str, *, prefix: str) -> str:
        # Stable enough for MVP. For production use hash/path registry.
        safe = (
            path.removeprefix("res://")
            .replace("/", "_")
            .replace(".", "_")
            .replace("-", "_")
        )
        return f"{prefix}_{safe}"


# ----------------------------
# Loading user DSL module
# ----------------------------

def load_scene_from_py(path: Path) -> Scene:
    spec = importlib.util.spec_from_file_location("user_game_module", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")

    module = importlib.util.module_from_spec(spec)

    # Expose DSL symbols to the module if user wants:
    module.Scene = Scene
    module.Node = Node
    module.Node2D = Node2D
    module.Control = Control
    module.Label = Label
    module.Button = Button
    module.Script = Script
    module.signal = signal

    sys.modules["user_game_module"] = module
    spec.loader.exec_module(module)

    scene = getattr(module, "__scene__", None)
    if not isinstance(scene, Scene):
        raise TypeError(f"{path} must define __scene__: Scene")

    return scene


# ----------------------------
# CLI
# ----------------------------

def build(input_file: Path, out_dir: Path) -> None:
    if out_dir.exists():
        shutil.rmtree(out_dir)

    scene = load_scene_from_py(input_file)
    compiler = Compiler(out_dir)
    compiler.compile_scene(scene)


def run_godot(out_dir: Path, godot_bin: str, scene_path: str | None = None) -> None:
    cmd = [godot_bin, "--path", str(out_dir)]
    if scene_path is not None:
        cmd.append(scene_path)
    subprocess.run(cmd, check=True)


def import_godot(out_dir: Path, godot_bin: str) -> None:
    subprocess.run([godot_bin, "--headless", "--path", str(out_dir), "--import"], check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    build_parser = sub.add_parser("build")
    build_parser.add_argument("input", type=Path)
    build_parser.add_argument("--out", type=Path, default=Path("./build/godot_project"))

    run_parser = sub.add_parser("run")
    run_parser.add_argument("input", type=Path)
    run_parser.add_argument("--out", type=Path, default=Path("./build/godot_project"))
    run_parser.add_argument("--godot", default="godot")
    run_parser.add_argument("--no-import", action="store_true")

    args = parser.parse_args()

    if args.command == "build":
        build(args.input, args.out)
        print(f"Generated Godot project: {args.out}")

    elif args.command == "run":
        build(args.input, args.out)
        if not args.no_import:
            import_godot(args.out, args.godot)

        scene = load_scene_from_py(args.input)
        run_godot(args.out, args.godot, scene.path)


if __name__ == "__main__":
    main()