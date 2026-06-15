from __future__ import annotations

import unittest

from pygodot.build.manifest import BuildManifest, ManifestResource


class BuildManifestTests(unittest.TestCase):
    def test_manifest_serializes_resources_with_explicit_ownership(self) -> None:
        manifest = BuildManifest(
            generated_files=["scenes/main.tscn", "project.godot"],
            generated_resources=["ui/title_label_settings.tres"],
            generated_scenes=["scenes/main.tscn"],
            generated_scripts=[],
            external_resources=[
                ManifestResource(
                    type="Script",
                    path="res://manual/player.gd",
                    id="Script_manual_player_gd",
                    copied=False,
                    ownership="referenced",
                ),
                ManifestResource(
                    type="Font",
                    path="res://assets/display.ttf",
                    id="Font_assets_display_ttf",
                    copied=True,
                    ownership="copied",
                ),
                ManifestResource(
                    type="LabelSettings",
                    path="res://ui/title_label_settings.tres",
                    id="LabelSettings_ui_title_label_settings_tres",
                    copied=False,
                    ownership="generated",
                ),
            ],
        )

        self.assertEqual(
            manifest.to_json(),
            """{
  "external_resources": [
    {
      "copied": true,
      "id": "Font_assets_display_ttf",
      "ownership": "copied",
      "path": "res://assets/display.ttf",
      "type": "Font"
    },
    {
      "copied": false,
      "id": "LabelSettings_ui_title_label_settings_tres",
      "ownership": "generated",
      "path": "res://ui/title_label_settings.tres",
      "type": "LabelSettings"
    },
    {
      "copied": false,
      "id": "Script_manual_player_gd",
      "ownership": "referenced",
      "path": "res://manual/player.gd",
      "type": "Script"
    }
  ],
  "generated_files": [
    "project.godot",
    "scenes/main.tscn"
  ],
  "generated_resources": [
    "ui/title_label_settings.tres"
  ],
  "generated_scenes": [
    "scenes/main.tscn"
  ],
  "generated_scripts": []
}
""",
        )
