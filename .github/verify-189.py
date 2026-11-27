#!/usr/bin/env python3
"""Temporary #189 product qualification: switch saved SolidCraft rows only."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile

OUTPUT = Path("/output")
PLAN = OUTPUT / "build-plan.json"

EXPECTED_ROWS = {
    "Small": {
        "mid_size": 60.0,
        "mid_wall": 2.0,
        "mid_base": 2.0,
        "mid_guide": 4.0,
    },
    "Medium": {
        "mid_size": 80.0,
        "mid_wall": 4.0,
        "mid_base": 3.0,
        "mid_guide": 6.0,
    },
    "Large": {
        "mid_size": 100.0,
        "mid_wall": 6.0,
        "mid_base": 4.0,
        "mid_guide": 10.0,
    },
}
EXPECTED_CELLS = {
    "Small": {
        "mid_size": "60 mm",
        "mid_wall": "2 mm",
        "mid_base": "2 mm",
        "mid_guide": "4 mm",
    },
    "Medium": {
        "mid_size": "80 mm",
        "mid_wall": "4 mm",
        "mid_base": "3 mm",
        "mid_guide": "6 mm",
    },
    "Large": {
        "mid_size": "100 mm",
        "mid_wall": "6 mm",
        "mid_base": "4 mm",
        "mid_guide": "10 mm",
    },
}
SUPPRESS_VARIANTS = {
    "hub75-frame-coupler-edge",
    "hub75-frame-coupler-corner-right",
    "hub75-frame-coupler-edge-tube",
    "hub75-frame-coupler-corner-right-tube",
    "hub75-frame-coupler-edge-tube-receiver",
    "hub75-frame-coupler-corner-right-tube-receiver",
}


def run(*args: str) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run(args, check=True)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_command(path: Path, command: str, params: dict) -> None:
    path.write_text(
        json.dumps({"commands": [{"command": command, "params": params}]}, indent=2)
        + "\n",
        encoding="utf-8",
    )


def evaluate(model: Path, destination: Path):
    run("solidcraft-cli", "eval", str(model), "--json-out", str(destination))
    return load(destination)


def inspect_table(model: Path, command: Path, destination: Path):
    run(
        "solidcraft-cli",
        "run",
        str(command),
        "--in",
        str(model),
        "--param-check",
        "strict",
        "--results",
        "--json-out",
        str(destination),
    )
    result = load(destination)
    assert isinstance(result, list) and len(result) == 1, result
    table = result[0]
    assert isinstance(table, dict), table
    return table


def activate(model: Path, command: Path, destination: Path) -> None:
    run(
        "solidcraft-cli",
        "run",
        str(command),
        "--in",
        str(model),
        "--param-check",
        "strict",
        "--save",
        str(destination),
    )
    assert destination.is_file() and destination.stat().st_size > 0


def parameters(evaluation: dict) -> dict[str, float]:
    return {
        row["name"]: float(row["value"])
        for row in evaluation["params"]
        if row["name"] in EXPECTED_ROWS["Medium"]
    }


def geometry_signature(evaluation: dict):
    rows = []
    for body in evaluation["bodies"]:
        bbox = body["bbox"]
        rows.append(
            (
                body.get("name"),
                tuple(round(float(value), 6) for value in bbox["min"]),
                tuple(round(float(value), 6) for value in bbox["max"]),
                round(float(body["volume_mm3"]), 6),
            )
        )
    return tuple(sorted(rows, key=lambda row: str(row[0])))


def verify_table(variant: str, table: dict, active: str) -> None:
    assert table["active"] == active, (variant, table["active"], active)
    assert table.get("matches") is True, (variant, table.get("matches"))
    rows = table["rows"]
    assert [row["name"] for row in rows] == ["Small", "Medium", "Large"], variant
    expected_column_count = 5 if variant in SUPPRESS_VARIANTS else 4
    assert len(table["columns"]) == expected_column_count, (
        variant,
        len(table["columns"]),
        expected_column_count,
    )

    suppress_key = None
    for row in rows:
        name = row["name"]
        values = row["values"]
        for parameter, expected in EXPECTED_CELLS[name].items():
            actual = values[f"param:{parameter}"]
            assert actual == expected, (variant, name, parameter, actual, expected)

        suppress_keys = sorted(
            key for key in values
            if isinstance(key, str) and key.startswith("suppress:")
        )
        if variant in SUPPRESS_VARIANTS:
            assert len(suppress_keys) == 1, (variant, name, suppress_keys)
            if suppress_key is None:
                suppress_key = suppress_keys[0]
            assert suppress_keys[0] == suppress_key, (variant, suppress_keys, suppress_key)
            expected = "false" if name == "Large" else "true"
            assert str(values[suppress_key]).lower() == expected, (
                variant,
                name,
                values[suppress_key],
                expected,
            )
        else:
            assert suppress_keys == [], (variant, name, suppress_keys)


def verify_variant(row: dict, work: Path, table_command: Path, commands: dict[str, Path]) -> None:
    variant = row["id"]
    model = OUTPUT / row["native"]["sc"]
    assert model.is_file(), model

    print(f"\n=== {variant} ===", flush=True)
    baseline_eval = evaluate(model, work / f"{variant}-medium-eval.json")
    baseline_table = inspect_table(
        model,
        table_command,
        work / f"{variant}-medium-table.json",
    )
    verify_table(variant, baseline_table, "Medium")
    assert parameters(baseline_eval) == EXPECTED_ROWS["Medium"], (
        variant,
        parameters(baseline_eval),
    )
    medium_geometry = geometry_signature(baseline_eval)

    switched = {}
    for name in ("Small", "Large"):
        saved = work / f"{variant}-{name.lower()}.sc"
        activate(model, commands[name], saved)
        evaluation = evaluate(saved, work / f"{variant}-{name.lower()}-eval.json")
        table = inspect_table(
            saved,
            table_command,
            work / f"{variant}-{name.lower()}-table.json",
        )
        verify_table(variant, table, name)
        actual_parameters = parameters(evaluation)
        assert actual_parameters == EXPECTED_ROWS[name], (
            variant,
            name,
            actual_parameters,
            EXPECTED_ROWS[name],
        )
        geometry = geometry_signature(evaluation)
        assert geometry != medium_geometry, (
            variant,
            name,
            "geometry did not change from saved Medium design",
        )
        switched[name] = geometry

    assert switched["Small"] != switched["Large"], (
        variant,
        "Small and Large geometry are identical",
    )
    print(f"PASS {variant}: saved Medium -> Small/Large switching is associative", flush=True)


def main() -> None:
    plan = load(PLAN)
    rows = [
        row
        for row in plan["models"]
        if row.get("owner") == "hub75-frame-coupler"
    ]
    assert len(rows) == 10, [row.get("id") for row in rows]

    with tempfile.TemporaryDirectory(prefix="verify-189-") as raw:
        work = Path(raw)
        table_command = work / "table.json"
        write_command(table_command, "config.table", {})
        commands = {}
        for name in ("Small", "Large"):
            path = work / f"{name.lower()}.json"
            write_command(path, "config.activate", {"row": name})
            commands[name] = path

        for row in rows:
            verify_variant(row, work, table_command, commands)

    print("\n#189 saved-design qualification passed for all 10 public coupler variants.")


if __name__ == "__main__":
    main()
