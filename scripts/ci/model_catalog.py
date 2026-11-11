"""One source of truth for model locations and website categories.

The slug remains stable for published Pages URLs, while source directories
are organized by their intended role. Use this module from CI, not copies
of a 10-item path mapping in multiple shell scripts.
"""
from pathlib import Path
import sys

SOURCES = {
    "plate": "models/basic/plate/scpf/model.py",
    "csg-cube": "models/basic/csg-cube/scpf/model.py",
    "bracket": "models/basic/bracket/scpf/model.py",
    "sample-plate": "models/basic/sample-plate/scpf/model.py",
    "plastic-enclosure": "models/basic/plastic-enclosure/scpf/model.py",
    "plastic-enclosure-pi": "models/basic/plastic-enclosure-pi/scpf/model.py",
    "corner-bracket": "models/component-examples/corner-bracket/scpf/model.py",
    "hub75-panel": "models/component-examples/hub75-panel/scpf/model.py",
    "hub75-screen": "models/advanced/hub75-screen/scpf/model.py",
    "hub75-wood-frame": "models/advanced/hub75-wood-frame/scpf/model.py",
}
SECTIONS = {
    "basic": ("Basic Models", "Small, transparent models used to develop and verify SCPF features.",
              ("plate", "csg-cube", "bracket", "sample-plate", "plastic-enclosure", "plastic-enclosure-pi")),
    "components": ("Components", "Reusable physical parts; example scripts import the same shared definition.",
                   ("corner-bracket", "hub75-panel")),
    "advanced": ("Advanced Models", "Full designs and nested native assemblies built from reusable components.",
                 ("hub75-screen", "hub75-wood-frame")),
}


def source_path(root, slug):
    return Path(root) / SOURCES[slug]


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in SOURCES:
        raise SystemExit("Usage: python scripts/ci/model_catalog.py <model-slug>")
    print(SOURCES[sys.argv[1]])
