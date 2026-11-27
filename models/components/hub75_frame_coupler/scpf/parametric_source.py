"""Parametric source recipes for the HUB75 frame-coupler owner.

The retained SolidCraft JSON remains the authority. This module reads only the
parameter expressions and sketch topology needed by the Forge owner so the
Small/Medium/Large table drives real geometry without duplicating source data
or three Python histories.
"""

import ast
import json
from pathlib import Path
import re

from scpf import cadmath


_SOURCE_FILE = (
    Path(__file__).resolve().parents[1]
    / "reference"
    / "hub75-screen-2panel-couplers.json"
)
_SOURCE_SKETCH_IDS = (
    65, 67, 79, 80, 87, 92, 96, 100, 101, 104, 105, 108, 109,
    121, 135, 137, 139, 140, 145, 147, 149, 151, 153, 156, 159, 162,
)


def _load_source():
    document = json.loads(_SOURCE_FILE.read_text(encoding="utf-8"))
    by_id = {
        feature["id"]: feature
        for feature in document["features"]
        if isinstance(feature, dict) and "id" in feature
    }
    missing = [feature_id for feature_id in _SOURCE_SKETCH_IDS if feature_id not in by_id]
    if missing:
        raise ValueError(f"retained HUB75 source misses sketches: {missing}")

    # Project exactly the fields used by the evaluator. This is equivalent to
    # the former embedded extraction, but leaves the retained JSON single-owned.
    params = [
        {
            "name": item["name"],
            "expr": item["expr"],
            "unit": item["unit"],
            "model": item["model"],
        }
        for item in document["params"]
    ]
    sketches = {
        str(feature_id): {
            "id": by_id[feature_id]["id"],
            "name": by_id[feature_id]["name"],
            "sketch": by_id[feature_id]["sketch"],
        }
        for feature_id in _SOURCE_SKETCH_IDS
    }
    return {"params": params, "sketches": sketches}


_SOURCE = _load_source()
_UNIT_RE = re.compile(r"(?<=\d)\s+(?:mm|deg)\b")


def _expression(text, values):
    text = _UNIT_RE.sub("", text).replace("^", "**")
    node = ast.parse(text, mode="eval").body

    def unitless_clamp(item):
        """Return X from the retained dimensionless min(1,max(0,X)) gate."""
        if not (
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and item.func.id == "min"
            and len(item.args) == 2
            and isinstance(item.args[0], ast.Constant)
            and item.args[0].value == 1
        ):
            return None
        maximum = item.args[1]
        if not (
            isinstance(maximum, ast.Call)
            and isinstance(maximum.func, ast.Name)
            and maximum.func.id == "max"
            and len(maximum.args) == 2
            and isinstance(maximum.args[0], ast.Constant)
            and maximum.args[0].value == 0
        ):
            return None
        return maximum.args[1]

    def unitless_clamp_complement(item):
        return (
            isinstance(item, ast.BinOp)
            and isinstance(item.op, ast.Sub)
            and isinstance(item.left, ast.Constant)
            and item.left.value == 1
            and unitless_clamp(item.right) is not None
        )

    def visit_dimensionless(item):
        """Evaluate a source subtree whose numeric literals are unitless."""
        one = values["mid_size"] / values["mid_size"]
        zero = one - one

        if isinstance(item, ast.Constant):
            if isinstance(item.value, (int, float)) and not isinstance(item.value, bool):
                return zero + one * item.value
            raise ValueError(f"unsupported source literal {item.value!r}")
        if isinstance(item, ast.Name):
            try:
                return values[item.id]
            except KeyError as exc:
                raise ValueError(f"unknown source parameter {item.id!r}") from exc
        if isinstance(item, ast.UnaryOp):
            value = visit_dimensionless(item.operand)
            if isinstance(item.op, ast.USub):
                return -value
            if isinstance(item.op, ast.UAdd):
                return value
            raise ValueError(
                f"unsupported source unary operator {type(item.op).__name__}"
            )
        if isinstance(item, ast.BinOp):
            if isinstance(item.op, ast.Div):
                # Ratios such as (length expression)/(length expression) are
                # dimensionless even though their individual operands are not.
                return visit(item.left) / visit(item.right)
            if isinstance(item.op, ast.Mult):
                left_is_number = isinstance(item.left, ast.Constant)
                right_is_number = isinstance(item.right, ast.Constant)
                if left_is_number or right_is_number:
                    return visit_dimensionless(item.left) * visit_dimensionless(item.right)
                return visit(item.left) * visit(item.right)
            left = visit_dimensionless(item.left)
            right = visit_dimensionless(item.right)
            if isinstance(item.op, ast.Add):
                return left + right
            if isinstance(item.op, ast.Sub):
                return left - right
            if isinstance(item.op, ast.Pow):
                return left ** right
            raise ValueError(
                f"unsupported source binary operator {type(item.op).__name__}"
            )
        if isinstance(item, ast.Call) and isinstance(item.func, ast.Name):
            functions = {
                "min": cadmath.min,
                "max": cadmath.max,
                "round": cadmath.round,
                "floor": cadmath.floor,
                "abs": cadmath.abs,
            }
            try:
                function = functions[item.func.id]
            except KeyError as exc:
                raise ValueError(
                    f"unsupported dimensionless source function {item.func.id!r}"
                ) from exc
            return function(*(visit_dimensionless(arg) for arg in item.args))
        return visit(item)

    def visit(item):
        if isinstance(item, ast.Constant):
            if isinstance(item.value, (int, float)) and not isinstance(item.value, bool):
                return item.value
            raise ValueError(f"unsupported source literal {item.value!r}")
        if isinstance(item, ast.Name):
            try:
                return values[item.id]
            except KeyError as exc:
                raise ValueError(f"unknown source parameter {item.id!r}") from exc
        if isinstance(item, ast.UnaryOp):
            value = visit(item.operand)
            if isinstance(item.op, ast.USub):
                return -value
            if isinstance(item.op, ast.UAdd):
                return value
            raise ValueError(f"unsupported source unary operator {type(item.op).__name__}")
        if isinstance(item, ast.BinOp):
            right = visit(item.right)
            if unitless_clamp_complement(item):
                # Forge numeric +/- literals are length-valued by default.
                # Build the source's dimensionless 1 from an existing native
                # length dependency so SolidCraft keeps this clamp unitless.
                one = values["mid_size"] / values["mid_size"]
                return one - right
            left = visit(item.left)
            if isinstance(item.op, ast.Add):
                return left + right
            if isinstance(item.op, ast.Sub):
                return left - right
            if isinstance(item.op, ast.Mult):
                return left * right
            if isinstance(item.op, ast.Div):
                return left / right
            if isinstance(item.op, ast.Pow):
                return left ** right
            raise ValueError(f"unsupported source binary operator {type(item.op).__name__}")
        if isinstance(item, ast.Call) and isinstance(item.func, ast.Name):
            clamp_value = unitless_clamp(item)
            if clamp_value is not None:
                one = values["mid_size"] / values["mid_size"]
                zero = one - one
                return cadmath.min(
                    one,
                    cadmath.max(zero, visit_dimensionless(clamp_value)),
                )
            functions = {
                "min": cadmath.min,
                "max": cadmath.max,
                "sqrt": cadmath.sqrt,
                "abs": cadmath.abs,
                "round": cadmath.round,
                "floor": cadmath.floor,
                "atan": cadmath.atan,
            }
            try:
                function = functions[item.func.id]
            except KeyError as exc:
                raise ValueError(f"unsupported source function {item.func.id!r}") from exc
            return function(*(visit(arg) for arg in item.args))
        raise ValueError(f"unsupported source expression node {type(item).__name__}")

    return visit(node)


def source_parameters(*, mid_size, mid_wall, mid_base, mid_guide):
    """Resolve the retained source parameter graph with four configured inputs."""
    overrides = {
        "mid_size": mid_size,
        "mid_wall": mid_wall,
        "mid_base": mid_base,
        "mid_guide": mid_guide,
    }
    values = {}
    zero_length = mid_size - mid_size
    literal_length = re.compile(
        r"^\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))\s+mm\s*$"
    )
    for item in _SOURCE["params"]:
        name = item["name"]
        if name in overrides:
            values[name] = overrides[name]
            continue

        match = literal_length.fullmatch(item["expr"])
        if item.get("unit") == "mm" and match is not None:
            # A plain Python number is fine as a geometry argument, but once it
            # participates in a native expression SolidCraft needs to know it
            # is a length.  Anchor the fixed source value to a cancelling
            # configured length dependency: its value stays constant in every
            # row and it does not become an extra editable CAD parameter.
            values[name] = zero_length + float(match.group(1))
        else:
            values[name] = _expression(item["expr"], values)
    return values


def _frame_offsets(frame, values):
    if frame == "middle":
        return 0.0, values["mid_row"]
    if frame == "edge":
        return 0.0, values["panel_h"]
    if frame == "corner_left":
        return values["panel_w"], values["panel_h"]
    if frame == "corner_right":
        return -values["panel_w"], values["panel_h"]
    raise ValueError(f"unsupported source frame {frame!r}")


def _point(feature, index, frame, values):
    point = feature["sketch"]["points"][index]
    exprs = point.get("exprs", {})
    x = _expression(exprs["x"], values) if "x" in exprs else point["pos"][0]
    y = _expression(exprs["y"], values) if "y" in exprs else point["pos"][1]
    x_offset, y_offset = _frame_offsets(frame, values)
    # Retained source sketches use SolidCraft XZ coordinates. Normalize to the
    # physical local (X, Z) convention consumed by family.py.
    return (x + x_offset, -(y + y_offset))


def _raw_point(feature, index, frame):
    point = feature["sketch"]["points"][index]["pos"]
    if frame == "middle":
        return (point[0], -(point[1] + 160.0))
    if frame == "edge":
        return (point[0], -(point[1] + 320.0))
    if frame == "corner_left":
        return (point[0] + 160.0, -(point[1] + 320.0))
    if frame == "corner_right":
        return (point[0] - 160.0, -(point[1] + 320.0))
    raise ValueError(f"unsupported source frame {frame!r}")


def _same(left, right, tolerance=1e-8):
    return (
        abs(left[0] - right[0]) <= tolerance
        and abs(left[1] - right[1]) <= tolerance
    )


def source_profiles(feature_id, *, frame, values):
    """Return closed physical-local profile recipes for one retained sketch."""
    feature = _SOURCE["sketches"][str(feature_id)]
    curves = [
        curve for curve in feature["sketch"].get("curves", [])
        if not curve.get("construction", False) and curve["type"] in {"line", "arc"}
    ]

    loops = []
    current = None
    start_raw = None
    start_index = None
    segments = []

    for curve_index, curve in enumerate(curves):
        a = curve["a"]
        b = curve["b"]
        raw_a = _raw_point(feature, a, frame)
        raw_b = _raw_point(feature, b, frame)

        if current is None:
            # Source arcs may store their endpoint pair opposite the ordered
            # profile walk.  Orient the first curve by connectivity to the
            # following curve instead of relying on curve.a/curve.b order.
            next_curve = curves[curve_index + 1] if curve_index + 1 < len(curves) else None
            if next_curve is not None:
                next_a = _raw_point(feature, next_curve["a"], frame)
                next_b = _raw_point(feature, next_curve["b"], frame)
                if _same(raw_b, next_a) or _same(raw_b, next_b):
                    curve_start, curve_end = a, b
                    start_raw = raw_a
                elif _same(raw_a, next_a) or _same(raw_a, next_b):
                    curve_start, curve_end = b, a
                    start_raw = raw_b
                else:
                    curve_start, curve_end = a, b
                    start_raw = raw_a
            else:
                curve_start, curve_end = a, b
                start_raw = raw_a
            start_index = curve_start
            current = start_raw
        elif _same(current, raw_a):
            curve_start, curve_end = a, b
        elif _same(current, raw_b):
            curve_start, curve_end = b, a
        else:
            raise ValueError(
                f"feature {feature_id}: disconnected curve {curve['id']!r}"
            )

        if curve["type"] == "line":
            segment = {
                "kind": "line",
                "end": _point(feature, curve_end, frame, values),
            }
        else:
            # SolidCraft stores the solved center at curve['c']; the preceding
            # authored point is the source three-point arc's through point and
            # retains its symbolic expressions.
            segment = {
                "kind": "arc_through",
                "end": _point(feature, curve_end, frame, values),
                "through": _point(feature, curve["c"] - 1, frame, values),
            }

        segments.append(segment)
        current = _raw_point(feature, curve_end, frame)

        if _same(current, start_raw):
            loops.append({
                "start": _point(feature, start_index, frame, values),
                "segments": segments,
            })
            current = None
            start_raw = None
            start_index = None
            segments = []

    if current is not None or segments:
        raise ValueError(f"feature {feature_id}: source profile did not close")
    return loops

def source_circle_centers(feature_id, *, frame, values):
    """Return physical-local centers for all authored circles in a sketch."""
    feature = _SOURCE["sketches"][str(feature_id)]
    return [
        _point(feature, curve["c"], frame, values)
        for curve in feature["sketch"].get("curves", [])
        if not curve.get("construction", False) and curve["type"] == "circle"
    ]
