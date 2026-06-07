# pygodot — ближайший роадмап

## Назначение документа

Этот документ фиксирует ближайшие цели разработки `pygodot` после появления базового library-first API, DSL, IR, прямого `.tscn` emitter, генерации `project.godot`, генерации GDScript и минимального примера.

Главная ближайшая цель — не «сделать игру», а проверить фреймворк на достаточно игровом, но контролируемом примере. Для этого выбран пример **Pong**.

## Текущая архитектурная позиция

Зафиксированные решения остаются в силе:

- Python используется как build-time DSL и orchestration layer.
- Runtime-логика игры остаётся на стороне Godot / GDScript.
- Python subset transpiler не входит в ближайший план.
- Python GDExtension runtime не входит в ближайший план.
- Основной API — library-first через объект `Game`.
- CLI, если появится, должен быть тонкой обёрткой над library API.
- Основной compiler path: Python DSL → internal IR → direct emitters.
- JSON/YAML не используются как основной промежуточный формат.
- Для простых сцен используется быстрый прямой `.tscn` emitter.
- Сложные Godot resources и Godot-assisted generation откладываются до появления реальной необходимости.

## Ближайшая стратегическая цель

Сделать `examples/pong` как первый нетривиальный пример, который проверяет:

- создание полноценной сцены через Python DSL;
- вложенность нод;
- arbitrary Godot node types через generic `Node` или новый helper;
- `Vec2`, `Color`, строки, числа, bool и другие сериализуемые значения;
- generated GDScript;
- работу `Game.build()` и `Game.run()`;
- читаемость generated `.tscn`;
- snapshot-тестируемость generated output;
- ограничения текущего DSL без преждевременного расширения ядра.

## Анти-цели ближайшего этапа

В ближайшем этапе не делать:

- полноценный Python → GDScript transpiler;
- Python runtime inside Godot;
- physics DSL;
- resource/subresource DSL для `CollisionShape2D`, `RectangleShape2D`, `AnimationPlayer`, `TileSet`, `ShaderMaterial`;
- автоматическую генерацию wrappers для всего Godot API;
- визуальный editor replacement;
- ECS;
- asset pipeline beyond simple external resource copy;
- Godot-assisted emitter;
- сложную игру уровня Flappy Bird с физикой, spawning и collision resources.

Эти направления допустимы позже, но сейчас они слишком сильно расширят поверхность проекта.

---

# Milestone 1 — Pong v1 на текущих возможностях

## Цель

Создать пример `examples/pong`, максимально используя уже существующие возможности `pygodot`, без крупных изменений ядра.

## Ожидаемая структура

```text
examples/pong/
  game.py
  README.md
```

Generated output не должен коммититься, если в проекте уже принята политика не хранить build artifacts:

```text
examples/pong/build/
```

## Сцена

Одна сцена:

```text
res://scenes/pong.tscn
```

Дерево сцены:

```text
Main: Node2D
  Background: ColorRect
  LeftPaddle: ColorRect
  RightPaddle: ColorRect
  Ball: ColorRect
  LeftScore: Label
  RightScore: Label
  HelpText: Label
```

## Runtime-логика

Один generated script:

```text
res://scripts/pong.gd
```

Скрипт висит на `Main`.

Логика в GDScript:

- `_ready()`;
- `_process(delta)`;
- движение левой ракетки;
- движение правой ракетки;
- движение мяча;
- ручная проверка столкновений мяча с ракетками и границами экрана;
- обновление счёта;
- reset ball после гола;
- restart по клавише.

## Управление в Pong v1

Для первой версии допустимо использовать прямую проверку клавиш в GDScript:

```gdscript
Input.is_key_pressed(KEY_W)
Input.is_key_pressed(KEY_S)
Input.is_key_pressed(KEY_UP)
Input.is_key_pressed(KEY_DOWN)
Input.is_key_pressed(KEY_SPACE)
```

Это временное решение. Нормальный InputMap DSL выделен в отдельный milestone.

## Рекомендуемый DSL в `examples/pong/game.py`

Пока можно использовать низкоуровневый `Node` для Godot classes, для которых ещё нет convenience constructors:

```python
Node(
    name="Ball",
    type="ColorRect",
    props={
        "position": Vec2(392, 292),
        "size": Vec2(16, 16),
        "color": Color(1, 1, 1),
    },
)
```

Если текущий DSL уже поддерживает `**props` только через specialized helpers, не расширять всё сразу. Лучше сначала явно увидеть боль generic `Node`, потом принять минимальное улучшение.

## Tasks

- [ ] Создать `examples/pong/game.py`.
- [ ] Создать `examples/pong/README.md`.
- [ ] Описать в README запуск через Python-модуль примера.
- [ ] Сгенерировать одну сцену `res://scenes/pong.tscn`.
- [ ] Сгенерировать один скрипт `res://scripts/pong.gd`.
- [ ] Использовать только простые ноды: `Node2D`, `ColorRect`, `Label`.
- [ ] Не добавлять physics bodies и collision shape resources.
- [ ] Не добавлять InputMap DSL в этом milestone.
- [ ] Проверить, что `game.build()` успешно генерирует проект.
- [ ] Проверить, что `game.run()` запускает Godot-проект при наличии Godot binary.

## Acceptance criteria

Milestone считается готовым, если:

- `examples/pong/game.py` читается как декларативное описание проекта;
- generated `.tscn` открывается Godot 4;
- generated scene запускается;
- Pong playable: две ракетки двигаются, мяч отскакивает, счёт обновляется;
- нет новых крупных абстракций, добавленных только ради гипотетического будущего;
- все существующие тесты проходят;
- добавлены минимальные тесты или snapshot на generated Pong output, если инфраструктура snapshot-тестов уже есть.

## Codex prompt suggestion

```text
Implement examples/pong as a single-scene playable Pong example using the existing pygodot public API. Prefer using the current DSL and generic Node declarations instead of expanding the framework. Do not add physics resources, InputMap DSL, Python-to-GDScript transpilation, or broad Godot API wrappers. Add a README explaining how to build and run the example. Keep generated build artifacts out of version control.
```

---

# Milestone 2 — Минимальное улучшение generic node UX

## Цель

Упростить описание arbitrary Godot node classes после того, как Pong v1 покажет неудобство низкоуровневого `Node(..., props={...})`.

## Вариант API

Предпочтительный минимальный helper:

```python
node(
    "Ball",
    "ColorRect",
    position=Vec2(392, 292),
    size=Vec2(16, 16),
    color=Color(1, 1, 1),
)
```

Сигнатура:

```python
def node(
    name: str,
    type: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    **props: Any,
) -> Node:
    ...
```

## Причина

Не нужно сразу генерировать wrappers для всех Godot classes. Generic helper даёт 80% удобства при почти нулевой архитектурной цене.

## Tasks

- [ ] Добавить public helper `node(...)`.
- [ ] Экспортировать `node` из `pygodot.dsl` и `pygodot`.
- [ ] Добавить unit-тесты на `node(...)`.
- [ ] Переписать `examples/pong` с `Node(..., props={...})` на `node(...)`, если это улучшает читаемость.
- [ ] Не удалять старый `Node`, он остаётся низкоуровневой dataclass-моделью.

## Acceptance criteria

- `node(...)` создаёт тот же DSL object, что и ручной `Node(...)`.
- `node(...)` поддерживает `children`, `script`, `signals`, `**props`.
- Public API остаётся простым.
- Pong DSL становится заметно короче и читабельнее.

## Codex prompt suggestion

```text
Add a minimal public helper function node(name, type, *, children=None, script=None, signals=None, **props) to reduce boilerplate for arbitrary Godot node declarations. Export it from pygodot.dsl and pygodot. Add tests. Update examples/pong only if it improves readability. Do not generate wrappers for all Godot classes.
```

---

# Milestone 3 — Snapshot-тесты generated output

## Цель

Защитить прямой `.tscn` emitter и generated GDScript от случайных изменений формата.

## Что тестировать

Минимальные snapshots:

```text
tests/snapshots/minimal_scene.tscn
```

Желательные snapshots после Pong:

```text
tests/snapshots/pong_scene.tscn
```

Если generated GDScript стабилен:

```text
tests/snapshots/pong_script.gd
```

## Политика snapshot-тестов

Snapshot должен проверять deterministic output:

- порядок properties;
- порядок external resources;
- stable resource ids;
- parent paths;
- signal connections;
- trailing newline;
- absence of nondeterministic timestamps or absolute paths.

## Tasks

- [ ] Добавить простой snapshot testing helper, если его ещё нет.
- [ ] Добавить snapshot для минимальной сцены.
- [ ] Добавить snapshot для Pong scene.
- [ ] Добавить snapshot для generated Pong script, если script generation deterministic.
- [ ] Убедиться, что tests не требуют установленного Godot binary.

## Acceptance criteria

- Unit tests проходят без Godot.
- Изменение emitter output явно ломает snapshot.
- Snapshot update делается осознанно.
- Generated output остаётся deterministic.

## Codex prompt suggestion

```text
Add snapshot tests for deterministic generated output. Cover at least a minimal scene and the Pong example scene. Tests must not require a Godot binary. Focus on stable .tscn output, resource ids, parent paths, property ordering, and trailing newline behavior.
```

---

# Milestone 4 — InputMap DSL

## Цель

Перевести управление Pong с прямых `KEY_*` проверок на Godot InputMap, генерируемый в `project.godot`.

## Предлагаемый API

```python
game.add_input_action("left_up", keys=["W"])
game.add_input_action("left_down", keys=["S"])
game.add_input_action("right_up", keys=["UP"])
game.add_input_action("right_down", keys=["DOWN"])
game.add_input_action("restart", keys=["SPACE"])
```

В GDScript:

```gdscript
Input.is_action_pressed("left_up")
Input.is_action_pressed("left_down")
Input.is_action_pressed("right_up")
Input.is_action_pressed("right_down")
Input.is_action_just_pressed("restart")
```

## Ограничения v1

Поддержать только keyboard keys.

Не поддерживать пока:

- mouse buttons;
- joypad buttons;
- axis;
- deadzones;
- multiple event types;
- input presets;
- platform-specific bindings.

## Вероятные изменения модели

Добавить DSL/model:

```python
@dataclass(slots=True, frozen=True)
class InputAction:
    name: str
    keys: tuple[str, ...]
```

Добавить в `Game`:

```python
input_actions: list[InputAction]
```

Добавить в `IRProject`:

```python
input_actions: tuple[IRInputAction, ...]
```

Расширить `ProjectEmitter` генерацией секции `[input]`.

## Tasks

- [ ] Добавить DSL-модель input actions.
- [ ] Добавить `Game.add_input_action(...)`.
- [ ] Протащить input actions через normalize/IR/validate.
- [ ] Расширить `ProjectEmitter`.
- [ ] Добавить tests на emitted `project.godot`.
- [ ] Обновить Pong: заменить `KEY_*` на `Input.is_action_pressed(...)`.
- [ ] Обновить README Pong.

## Acceptance criteria

- `project.godot` содержит корректные input actions.
- Pong работает через `Input.is_action_pressed`.
- Некорректные имена actions и keys валидируются.
- Tests не требуют Godot binary.

## Codex prompt suggestion

```text
Add a minimal keyboard-only InputMap DSL. Implement Game.add_input_action(name, keys=[...]), normalize it into IRProject, validate it, and emit the [input] section in project.godot. Update examples/pong to use Input.is_action_pressed instead of direct KEY_* checks. Keep scope limited to keyboard keys only.
```

---

# Milestone 5 — Pong v2: Menu scene + Game scene

## Цель

Проверить multi-scene project generation и переходы между сценами.

## Новая структура сцен

```text
res://scenes/menu.tscn
res://scenes/pong.tscn
```

`main_scene` должен указывать на menu:

```text
res://scenes/menu.tscn
```

## Menu scene

```text
Menu: Control
  Title: Label
  StartButton: Button
  ExitButton: Button
```

Menu script:

- start → `get_tree().change_scene_to_file("res://scenes/pong.tscn")`;
- exit → `get_tree().quit()`.

## Pong scene

Существующая Pong scene остаётся game scene.

Можно добавить возврат в menu по `ESC`, если InputMap уже есть.

## Tasks

- [ ] Добавить `menu.tscn` scene declaration.
- [ ] Добавить generated `menu.gd`.
- [ ] Использовать signals для `Button.pressed`.
- [ ] Проверить, что `Game` поддерживает несколько сцен без дополнительных изменений.
- [ ] Обновить README Pong.
- [ ] Добавить snapshot на menu scene.
- [ ] Добавить test, что `main_scene` зарегистрирована среди scenes.

## Acceptance criteria

- `game.build()` генерирует две сцены.
- `project.godot` указывает menu как main scene.
- Кнопка Start открывает Pong scene.
- Кнопка Exit закрывает игру.
- Signal connections в generated `.tscn` корректны.

## Codex prompt suggestion

```text
Extend examples/pong to use two scenes: a menu scene as the main scene and the existing pong scene as the game scene. Use Button.pressed signal connections for Start and Exit. Do not introduce new framework abstractions unless strictly necessary. Add or update snapshots for generated menu and pong scenes.
```

---

# Milestone 6 — Минимальные convenience constructors

## Цель

Добавить только те convenience node constructors, необходимость которых доказана примерами.

## Кандидаты

После Pong естественные кандидаты:

```python
ColorRect(...)
```

Возможно позже:

```python
Timer(...)
Area2D(...)
CollisionShape2D(...)
```

Но `Timer`, `Area2D`, `CollisionShape2D` не добавлять до Flappy Bird или другого примера, где они реально нужны.

## API pattern

Следовать существующему стилю:

```python
def ColorRect(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    **props: Any,
) -> Node:
    ...
```

## Tasks

- [ ] Добавить `ColorRect(...)`, если Pong всё ещё содержит много generic `node(..., "ColorRect")`.
- [ ] Экспортировать `ColorRect` из public API.
- [ ] Добавить tests.
- [ ] Обновить examples/pong.
- [ ] Не добавлять constructors без usage в examples/tests.

## Acceptance criteria

- Convenience constructor уменьшает boilerplate.
- API остаётся маленьким.
- Нет попытки покрыть весь Godot API вручную.

## Codex prompt suggestion

```text
Add only the convenience node constructors that are directly justified by existing examples, starting with ColorRect if it simplifies examples/pong. Follow the existing Node2D/Label/Button constructor pattern. Do not add broad Godot API wrappers.
```

---

# Milestone 7 — Документация по generated/manual boundary

## Цель

Явно зафиксировать, какие файлы принадлежат generator’у, какие — пользователю, и что можно безопасно редактировать руками.

## Что описать

- `source_root` содержит user-owned source files and assets.
- `build_dir` содержит generated Godot project.
- Generated files могут перезаписываться.
- Manual scripts должны подключаться явно и не иметь generated body.
- External resources copied from `source_root` should be treated as source-owned.
- Manifest хранит generated files and external resources.

## Tasks

- [ ] Добавить `docs/GENERATED_BOUNDARY.md`.
- [ ] Описать generated files.
- [ ] Описать manual files.
- [ ] Описать external resource copy behavior.
- [ ] Описать manifest.
- [ ] Добавить ссылку из README.

## Acceptance criteria

- Пользователь понимает, какие файлы нельзя править руками.
- Codex получает явную политику и не начинает патчить generated output как source of truth.

## Codex prompt suggestion

```text
Document the generated/manual boundary for pygodot. Explain source_root, build_dir, generated files, manual scripts, copied external resources, and manifest semantics. Make it clear that generated build artifacts are not the source of truth.
```

---

# После ближайшего роадмапа

Следующие примеры после Pong:

## Snake

Цель: показать минимальную игру, где сцена почти пустая, а rendering идёт через `_draw()`.

Полезно для проверки:

- generated script body;
- input actions;
- timers or manual tick accumulator;
- minimal scene style.

## Flappy Bird

Брать только после того, как появятся:

- InputMap DSL;
- generic node helper;
- хотя бы базовая resource/subresource strategy;
- понимание, как описывать collision shapes;
- возможно `Timer` и scene instancing.

Flappy Bird станет хорошим тестом physics/resource/spawning pipeline, но сейчас слишком рано.

---

# Приоритеты по порядку

Рекомендуемый порядок выполнения:

1. `examples/pong` v1 на текущем API.
2. Minimal generic `node(...)` helper, если Pong подтвердит боль.
3. Snapshot-тесты generated `.tscn`.
4. Keyboard-only InputMap DSL.
5. Pong v2 с menu scene.
6. Minimal convenience constructors, только по фактической необходимости.
7. Документация generated/manual boundary.

Не менять этот порядок без причины. Он специально построен так, чтобы каждый следующий шаг был обоснован болью из предыдущего, а не гипотетической архитектурой.
