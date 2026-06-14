"""Build manifest data and serialization."""

from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass(slots=True)
class ManifestResource:
    type: str
    path: str
    id: str
    copied: bool


@dataclass(slots=True)
class BuildManifest:
    generated_files: list[str] = field(default_factory=list)
    generated_resources: list[str] = field(default_factory=list)
    generated_scenes: list[str] = field(default_factory=list)
    generated_scripts: list[str] = field(default_factory=list)
    external_resources: list[ManifestResource] = field(default_factory=list)

    def to_json(self) -> str:
        data = {
            "generated_files": sorted(self.generated_files),
            "generated_resources": sorted(self.generated_resources),
            "generated_scenes": sorted(self.generated_scenes),
            "generated_scripts": sorted(self.generated_scripts),
            "external_resources": [
                {
                    "type": resource.type,
                    "path": resource.path,
                    "id": resource.id,
                    "copied": resource.copied,
                }
                for resource in sorted(
                    self.external_resources,
                    key=lambda item: (item.type, item.path, item.id),
                )
            ],
        }
        return json.dumps(data, indent=2, sort_keys=True) + "\n"
