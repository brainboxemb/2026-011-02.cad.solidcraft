"""Resolved late tube-interface contours for the HUB75 coupler owner.

Configured base, guide, reference and seam geometry is derived directly from
the retained SolidCraft JSON in parametric_source.py. Only the final active
Edge tube additions whose supplied source is solver-resolved remain here.
"""

# Final active tube-frame Edge additions from SolidCraft features 226–230.
# Coordinates are normalized from the top Edge occurrence to physical local XZ
# (source world Z=320 -> local Z=0). These late tube-interface contours are
# solver-resolved in the supplied design and are intentionally not size-table
# parameters. The configurable base/guide geometry is read from the retained
# JSON by parametric_source.py.
TUBE_EDGE_REAR_SUPPORT_PROFILES = [
  {
    "start": [-33.99584408607707, 2.6],
    "segments": [
      {"kind": "line", "end": [-25.0, 3.1]},
      {"kind": "line", "end": [25.0, 3.1]},
      {"kind": "line", "end": [33.99584408607707, 2.6]},
      {"kind": "line", "end": [33.99584408607707, 2.855]},
      {
        "kind": "arc",
        "end": [29.023234609242117, 7.3323576836624],
        "center": [33.995844086079515, 7.85499999999547],
        "clockwise": True,
      },
      {"kind": "line", "end": [28.372609476841365, 13.52264231633825]},
      {
        "kind": "arc",
        "end": [23.4, 18.0],
        "center": [23.39999999999553, 12.9999999999968],
        "clockwise": False,
      },
      {"kind": "line", "end": [16.6, 18.0]},
      {
        "kind": "arc",
        "end": [12.269872981077809, 15.5],
        "center": [16.599999999998015, 13.0000000000026],
        "clockwise": False,
      },
      {"kind": "line", "end": [12.15440292723989, 15.3]},
      {
        "kind": "arc",
        "end": [7.824275908317697, 12.80000000000365],
        "center": [7.824275908317821, 17.80000000000706],
        "clockwise": True,
      },
      {"kind": "line", "end": [-7.824275908317697, 12.8]},
      {
        "kind": "arc",
        "end": [-12.154402927239536, 15.30000000000024],
        "center": [-7.8242759083156495, 17.80000000000274],
        "clockwise": True,
      },
      {"kind": "line", "end": [-12.269872981077809, 15.5]},
      {
        "kind": "arc",
        "end": [-16.6, 18.0],
        "center": [-16.599999999995845, 13.0000000000026],
        "clockwise": False,
      },
      {"kind": "line", "end": [-23.4, 18.0]},
      {
        "kind": "arc",
        "end": [-28.372609476841365, 13.52264231633825],
        "center": [-23.39999999999553, 12.9999999999968],
        "clockwise": False,
      },
      {"kind": "line", "end": [-29.0232346092357, 7.3323576836617]},
      {
        "kind": "arc",
        "end": [-33.99584408607707, 2.8549999999969],
        "center": [-33.995844086077845, 7.8549999999974],
        "clockwise": True,
      },
      {"kind": "line", "end": [-33.99584408607707, 2.6]},
    ],
  },
]

TUBE_EDGE_BASE_PLATE_PROFILES = [
  {
    "start": [26.25, 17.10822346032927],
    "segments": [
      {
        "kind": "arc",
        "end": [28.372609476842673, 13.52264231633836],
        "center": [23.399999999997178, 12.9999999999965],
        "clockwise": True,
      },
      {"kind": "line", "end": [29.0232346092357, 7.3323576836617]},
      {
        "kind": "arc",
        "end": [33.99584408607707, 2.85500000000004],
        "center": [33.995844086077845, 7.8549999999974],
        "clockwise": False,
      },
      {"kind": "line", "end": [33.99584408607707, 2.6]},
      {"kind": "line", "end": [26.25, 3.065956502017]},
      {"kind": "line", "end": [26.25, 17.10822346032927]},
    ],
  },
  {
    "start": [-13.75, 3.1],
    "segments": [
      {"kind": "line", "end": [13.75, 3.1]},
      {"kind": "line", "end": [13.75, 17.10822346032927]},
      {
        "kind": "arc",
        "end": [12.269872981077809, 15.5],
        "center": [16.5999999999783, 13.00000000003513],
        "clockwise": False,
      },
      {"kind": "line", "end": [12.15440292723989, 15.3]},
      {
        "kind": "arc",
        "end": [7.824275908317697, 12.80000000000365],
        "center": [7.824275908317821, 17.80000000000706],
        "clockwise": True,
      },
      {"kind": "line", "end": [-7.824275908317697, 12.8]},
      {
        "kind": "arc",
        "end": [-12.154402927239536, 15.30000000000024],
        "center": [-7.8242759083156495, 17.80000000000274],
        "clockwise": True,
      },
      {"kind": "line", "end": [-12.269872981077809, 15.5]},
      {
        "kind": "arc",
        "end": [-13.75, 17.10822346032927],
        "center": [-16.5999999999783, 13.00000000003513],
        "clockwise": False,
      },
      {"kind": "line", "end": [-13.75, 3.1]},
    ],
  },
  {
    "start": [-26.25, 17.1082234603282],
    "segments": [
      {
        "kind": "arc",
        "end": [-28.372609476841365, 13.52264231633825],
        "center": [-23.399999999997178, 12.9999999999965],
        "clockwise": False,
      },
      {"kind": "line", "end": [-29.0232346092357, 7.3323576836617]},
      {
        "kind": "arc",
        "end": [-33.99584408607707, 2.8549999999969],
        "center": [-33.995844086077845, 7.8549999999974],
        "clockwise": True,
      },
      {"kind": "line", "end": [-33.99584408607707, 2.6]},
      {"kind": "line", "end": [-26.25, 3.065956502017]},
      {"kind": "line", "end": [-26.25, 17.1082234603282]},
    ],
  },
]

# Feature 230 selects sketch-147 loops l93–l96 and l97–l100. In the retained
# sketch-147 profile ordering these are exactly entries 21 and 22.
TUBE_EDGE_REAR_REFERENCE_MARK_INDICES = (21, 22)

