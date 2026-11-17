"""Native CAD mutation cases.

Keep saved-design mutations as data. The workflow/runner executes them; the
validator checks the resulting native evidence.
"""

NATIVE_MUTATIONS = {
    "hub75-wood-frame": (
        {
            "name": "height-400",
            "changes": {"opening_height": "400 mm"},
        },
        {
            "name": "width-1000",
            "changes": {"opening_width": "1000 mm"},
        },
        {
            "name": "panel-recess-35",
            "changes": {"panel_recess_depth": "35 mm"},
        },
        {
            "name": "glazing-depth-16",
            "changes": {"glazing_wood_depth": "16 mm"},
        },
        {
            "name": "bracket-params",
            "changes": {
                "bracket_width": "30 mm",
                "corner_radius": "6 mm",
            },
        },
        {
            "name": "depth-120",
            "changes": {"cabinet_depth": "120 mm"},
        },
    ),
}
