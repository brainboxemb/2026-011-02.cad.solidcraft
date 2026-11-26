"""Fixed Medium geometry data extracted from the retained native SolidCraft source.

Generated from reference/hub75-screen-2panel-couplers.json for the initial
Medium-only port. Forge configuration-table support is tracked by
lib.py.solidcraft.forge#216; do not add Small/Large branching here.
"""

MEDIUM = {
  "name": "Medium",
  "size": 80,
  "wall": 4,
  "fit": 0.25,
  "base": 3,
  "guide": 6,
  "datum": 14.5,
  "row": 160,
  "screw_x": 8,
  "edge_screw_in": 8,  # source edge_screw_in: mounting axis inset from edge
  "screw_d": 3.4,
  "bushing_z": 11,
  "bushing_r": 7,
  "bushing_gap": 0.45,
  "tube_r": 4.25,
  "tube_gap": 0.45,
  "tube_depth": 0.9,
  "pad_r": 4.7,
  "pad_h": 2.4,
  "pin_r": 1.05,
  "pin_h": 2,
  "seam": 2.8,
  "key_h": 4,
  "inset": 1.25,
  "rib_x": 12.6265625,
  "rib_z": 9.9909375,
  "edge_end_rear": 1.395,
  "edge_end_inner": 10.8852578125,
  "corner_out": 19.5
}

SUPPRESSED_MEDIUM_FEATURES = [
  "Edge coupler doorvoer paneelpen",
  "Corner coupler rechts doorvoer paneelpen"
]

BASE_PROFILES = {
  "middle": [
    {
      "start": [
        -16.8765625,
        34
      ],
      "segments": [
        {
          "kind": "arc",
          "end": [
            -10.8765625,
            40
          ],
          "center": [
            -10.8765625,
            34
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            10.8765625,
            40
          ]
        },
        {
          "kind": "arc",
          "end": [
            16.8765625,
            34
          ],
          "center": [
            10.8765625,
            34
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            16.8765625,
            24.2409375
          ]
        },
        {
          "kind": "arc",
          "end": [
            26.8765625,
            14.2409375
          ],
          "center": [
            26.8765625,
            24.2409375
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            34,
            14.2409375
          ]
        },
        {
          "kind": "arc",
          "end": [
            40,
            8.2409375
          ],
          "center": [
            34,
            8.2409375
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            40,
            -8.2409375
          ]
        },
        {
          "kind": "arc",
          "end": [
            34,
            -14.2409375
          ],
          "center": [
            34,
            -8.2409375
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            26.8765625,
            -14.2409375
          ]
        },
        {
          "kind": "arc",
          "end": [
            16.8765625,
            -24.2409375
          ],
          "center": [
            26.8765625,
            -24.2409375
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            16.8765625,
            -34
          ]
        },
        {
          "kind": "arc",
          "end": [
            10.8765625,
            -40
          ],
          "center": [
            10.8765625,
            -34
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -10.8765625,
            -40
          ]
        },
        {
          "kind": "arc",
          "end": [
            -16.8765625,
            -34
          ],
          "center": [
            -10.8765625,
            -34
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -16.8765625,
            -24.2409375
          ]
        },
        {
          "kind": "arc",
          "end": [
            -26.8765625,
            -14.2409375
          ],
          "center": [
            -26.8765625,
            -24.2409375
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -34,
            -14.2409375
          ]
        },
        {
          "kind": "arc",
          "end": [
            -40,
            -8.2409375
          ],
          "center": [
            -34,
            -8.2409375
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -40,
            8.2409375
          ]
        },
        {
          "kind": "arc",
          "end": [
            -34,
            14.2409375
          ],
          "center": [
            -34,
            8.2409375
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -26.8765625,
            14.2409375
          ]
        },
        {
          "kind": "arc",
          "end": [
            -16.8765625,
            24.2409375
          ],
          "center": [
            -26.8765625,
            24.2409375
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -16.8765625,
            34
          ]
        }
      ]
    }
  ],
  "edge": [
    {
      "start": [
        -16.8765625,
        34
      ],
      "segments": [
        {
          "kind": "arc",
          "end": [
            -10.8765625,
            40
          ],
          "center": [
            -10.8765625,
            34
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            10.8765625,
            40
          ]
        },
        {
          "kind": "arc",
          "end": [
            16.8765625,
            34
          ],
          "center": [
            10.8765625,
            34
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            16.8765625,
            12.855
          ]
        },
        {
          "kind": "arc",
          "end": [
            26.8765625,
            2.855
          ],
          "center": [
            26.8765625,
            12.855
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            34,
            2.855
          ]
        },
        {
          "kind": "arc",
          "end": [
            40,
            -3.145
          ],
          "center": [
            34,
            -3.145
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            40,
            -9.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            34,
            -15.135257813
          ],
          "center": [
            34,
            -9.135257812
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            26.8765625,
            -15.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            16.8765625,
            -25.135257813
          ],
          "center": [
            26.8765625,
            -25.135257813
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            16.8765625,
            -34
          ]
        },
        {
          "kind": "arc",
          "end": [
            10.8765625,
            -40
          ],
          "center": [
            10.8765625,
            -34
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -10.8765625,
            -40
          ]
        },
        {
          "kind": "arc",
          "end": [
            -16.8765625,
            -34
          ],
          "center": [
            -10.8765625,
            -34
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -16.8765625,
            -25.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            -26.8765625,
            -15.135257813
          ],
          "center": [
            -26.8765625,
            -25.135257813
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -34,
            -15.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            -40,
            -9.135257813
          ],
          "center": [
            -34,
            -9.135257813
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -40,
            -3.145
          ]
        },
        {
          "kind": "arc",
          "end": [
            -34,
            2.855
          ],
          "center": [
            -34,
            -3.145
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -26.8765625,
            2.855
          ]
        },
        {
          "kind": "arc",
          "end": [
            -16.8765625,
            12.855
          ],
          "center": [
            -26.8765625,
            12.855
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -16.8765625,
            34
          ]
        }
      ]
    }
  ],
  "corner_left": [
    {
      "start": [
        -2.85,
        13.5
      ],
      "segments": [
        {
          "kind": "arc",
          "end": [
            3.15,
            19.5
          ],
          "center": [
            3.15,
            13.5
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            10.8765625,
            19.5
          ]
        },
        {
          "kind": "arc",
          "end": [
            16.8765625,
            13.5
          ],
          "center": [
            10.8765625,
            13.5
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            16.8765625,
            12.855
          ]
        },
        {
          "kind": "arc",
          "end": [
            26.8765625,
            2.855
          ],
          "center": [
            26.8765625,
            12.855
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            34,
            2.855
          ]
        },
        {
          "kind": "arc",
          "end": [
            40,
            -3.145
          ],
          "center": [
            34,
            -3.145
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            40,
            -9.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            34,
            -15.135257813
          ],
          "center": [
            34,
            -9.135257812
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            26.8765625,
            -15.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            16.8765625,
            -25.135257813
          ],
          "center": [
            26.8765625,
            -25.135257813
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            16.8765625,
            -34
          ]
        },
        {
          "kind": "arc",
          "end": [
            10.8765625,
            -40
          ],
          "center": [
            10.8765625,
            -34
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            3.15,
            -40
          ]
        },
        {
          "kind": "arc",
          "end": [
            -2.85,
            -34
          ],
          "center": [
            3.15,
            -34
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -2.85,
            -25.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            -12.85,
            -15.135257813
          ],
          "center": [
            -12.85,
            -25.135257813
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -13.5,
            -15.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            -19.5,
            -9.135257813
          ],
          "center": [
            -13.5,
            -9.135257813
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -19.5,
            -3.145
          ]
        },
        {
          "kind": "arc",
          "end": [
            -13.5,
            2.855
          ],
          "center": [
            -13.5,
            -3.145
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -12.85,
            2.855
          ]
        },
        {
          "kind": "arc",
          "end": [
            -2.85,
            12.855
          ],
          "center": [
            -12.85,
            12.855
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -2.85,
            13.5
          ]
        }
      ]
    }
  ],
  "corner_right": [
    {
      "start": [
        2.85,
        13.5
      ],
      "segments": [
        {
          "kind": "arc",
          "end": [
            -3.15,
            19.5
          ],
          "center": [
            -3.15,
            13.5
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -10.8765625,
            19.5
          ]
        },
        {
          "kind": "arc",
          "end": [
            -16.8765625,
            13.5
          ],
          "center": [
            -10.8765625,
            13.5
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -16.8765625,
            12.855
          ]
        },
        {
          "kind": "arc",
          "end": [
            -26.8765625,
            2.855
          ],
          "center": [
            -26.8765625,
            12.855
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -34,
            2.855
          ]
        },
        {
          "kind": "arc",
          "end": [
            -40,
            -3.145
          ],
          "center": [
            -34,
            -3.145
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -40,
            -9.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            -34,
            -15.135257813
          ],
          "center": [
            -34,
            -9.135257813
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -26.8765625,
            -15.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            -16.8765625,
            -25.135257813
          ],
          "center": [
            -26.8765625,
            -25.135257813
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -16.8765625,
            -34
          ]
        },
        {
          "kind": "arc",
          "end": [
            -10.8765625,
            -40
          ],
          "center": [
            -10.8765625,
            -34
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -3.15,
            -40
          ]
        },
        {
          "kind": "arc",
          "end": [
            2.85,
            -34
          ],
          "center": [
            -3.15,
            -34
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            2.85,
            -25.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            12.85,
            -15.135257813
          ],
          "center": [
            12.85,
            -25.135257813
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            13.5,
            -15.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            19.5,
            -9.135257813
          ],
          "center": [
            13.5,
            -9.135257812
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            19.5,
            -3.145
          ]
        },
        {
          "kind": "arc",
          "end": [
            13.5,
            2.855
          ],
          "center": [
            13.5,
            -3.145
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            12.85,
            2.855
          ]
        },
        {
          "kind": "arc",
          "end": [
            2.85,
            12.855
          ],
          "center": [
            12.85,
            12.855
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            2.85,
            13.5
          ]
        }
      ]
    }
  ]
}

MIDDLE_GUIDE_PROFILES = [
  {
    "start": [
      -36.828427125,
      -10.2409375
    ],
    "segments": [
      {
        "kind": "arc",
        "end": [
          -37.771236166,
          -12.907604167
        ],
        "center": [
          -36.828427125,
          -11.7409375
        ],
        "clockwise": False
      },
      {
        "kind": "arc",
        "end": [
          -34,
          -14.2409375
        ],
        "center": [
          -34,
          -8.2409375
        ],
        "clockwise": False
      },
      {
        "kind": "line",
        "end": [
          -26.8765625,
          -14.2409375
        ]
      },
      {
        "kind": "arc",
        "end": [
          -16.8765625,
          -24.2409375
        ],
        "center": [
          -26.8765625,
          -24.2409375
        ],
        "clockwise": True
      },
      {
        "kind": "line",
        "end": [
          -16.8765625,
          -34
        ]
      },
      {
        "kind": "arc",
        "end": [
          -15.543229167,
          -37.771236166
        ],
        "center": [
          -10.8765625,
          -34
        ],
        "clockwise": False
      },
      {
        "kind": "arc",
        "end": [
          -12.8765625,
          -36.828427125
        ],
        "center": [
          -14.3765625,
          -36.828427125
        ],
        "clockwise": False
      },
      {
        "kind": "line",
        "end": [
          -12.8765625,
          -14.9815625
        ]
      },
      {
        "kind": "arc",
        "end": [
          -17.6171875,
          -10.2409375
        ],
        "center": [
          -17.6171875,
          -14.9815625
        ],
        "clockwise": False
      },
      {
        "kind": "line",
        "end": [
          -36.828427125,
          -10.2409375
        ]
      }
    ]
  },
  {
    "start": [
      -36.828427125,
      10.2409375
    ],
    "segments": [
      {
        "kind": "arc",
        "end": [
          -37.771236166,
          12.907604167
        ],
        "center": [
          -36.828427125,
          11.7409375
        ],
        "clockwise": True
      },
      {
        "kind": "arc",
        "end": [
          -34,
          14.2409375
        ],
        "center": [
          -34,
          8.2409375
        ],
        "clockwise": True
      },
      {
        "kind": "line",
        "end": [
          -26.8765625,
          14.2409375
        ]
      },
      {
        "kind": "arc",
        "end": [
          -16.8765625,
          24.2409375
        ],
        "center": [
          -26.8765625,
          24.2409375
        ],
        "clockwise": False
      },
      {
        "kind": "line",
        "end": [
          -16.8765625,
          34
        ]
      },
      {
        "kind": "arc",
        "end": [
          -15.543229167,
          37.771236166
        ],
        "center": [
          -10.8765625,
          34
        ],
        "clockwise": True
      },
      {
        "kind": "arc",
        "end": [
          -12.8765625,
          36.828427125
        ],
        "center": [
          -14.3765625,
          36.828427125
        ],
        "clockwise": True
      },
      {
        "kind": "line",
        "end": [
          -12.8765625,
          14.9815625
        ]
      },
      {
        "kind": "arc",
        "end": [
          -17.6171875,
          10.2409375
        ],
        "center": [
          -17.6171875,
          14.9815625
        ],
        "clockwise": True
      },
      {
        "kind": "line",
        "end": [
          -36.828427125,
          10.2409375
        ]
      }
    ]
  },
  {
    "start": [
      36.828427125,
      -10.2409375
    ],
    "segments": [
      {
        "kind": "arc",
        "end": [
          37.771236166,
          -12.907604167
        ],
        "center": [
          36.828427125,
          -11.7409375
        ],
        "clockwise": True
      },
      {
        "kind": "arc",
        "end": [
          34,
          -14.2409375
        ],
        "center": [
          34,
          -8.2409375
        ],
        "clockwise": True
      },
      {
        "kind": "line",
        "end": [
          26.8765625,
          -14.2409375
        ]
      },
      {
        "kind": "arc",
        "end": [
          16.8765625,
          -24.2409375
        ],
        "center": [
          26.8765625,
          -24.2409375
        ],
        "clockwise": False
      },
      {
        "kind": "line",
        "end": [
          16.8765625,
          -34
        ]
      },
      {
        "kind": "arc",
        "end": [
          15.543229167,
          -37.771236166
        ],
        "center": [
          10.8765625,
          -34
        ],
        "clockwise": True
      },
      {
        "kind": "arc",
        "end": [
          12.8765625,
          -36.828427125
        ],
        "center": [
          14.3765625,
          -36.828427125
        ],
        "clockwise": True
      },
      {
        "kind": "line",
        "end": [
          12.8765625,
          -14.9815625
        ]
      },
      {
        "kind": "arc",
        "end": [
          17.6171875,
          -10.2409375
        ],
        "center": [
          17.6171875,
          -14.9815625
        ],
        "clockwise": True
      },
      {
        "kind": "line",
        "end": [
          36.828427125,
          -10.2409375
        ]
      }
    ]
  },
  {
    "start": [
      36.828427125,
      10.2409375
    ],
    "segments": [
      {
        "kind": "arc",
        "end": [
          37.771236166,
          12.907604167
        ],
        "center": [
          36.828427125,
          11.7409375
        ],
        "clockwise": False
      },
      {
        "kind": "arc",
        "end": [
          34,
          14.2409375
        ],
        "center": [
          34,
          8.2409375
        ],
        "clockwise": False
      },
      {
        "kind": "line",
        "end": [
          26.8765625,
          14.2409375
        ]
      },
      {
        "kind": "arc",
        "end": [
          16.8765625,
          24.2409375
        ],
        "center": [
          26.8765625,
          24.2409375
        ],
        "clockwise": True
      },
      {
        "kind": "line",
        "end": [
          16.8765625,
          34
        ]
      },
      {
        "kind": "arc",
        "end": [
          15.543229167,
          37.771236166
        ],
        "center": [
          10.8765625,
          34
        ],
        "clockwise": False
      },
      {
        "kind": "arc",
        "end": [
          12.8765625,
          36.828427125
        ],
        "center": [
          14.3765625,
          36.828427125
        ],
        "clockwise": False
      },
      {
        "kind": "line",
        "end": [
          12.8765625,
          14.9815625
        ]
      },
      {
        "kind": "arc",
        "end": [
          17.6171875,
          10.2409375
        ],
        "center": [
          17.6171875,
          14.9815625
        ],
        "clockwise": False
      },
      {
        "kind": "line",
        "end": [
          36.828427125,
          10.2409375
        ]
      }
    ]
  }
]

RAIL_RELIEF_PROFILES = {
  "edge": [
    {
      "start": [
        -100,
        -1.145
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            100,
            -1.145
          ]
        },
        {
          "kind": "line",
          "end": [
            100,
            -11.135257813
          ]
        },
        {
          "kind": "line",
          "end": [
            17.6171875,
            -11.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            12.8765625,
            -15.875882812
          ],
          "center": [
            17.6171875,
            -15.875882812
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            12.8765625,
            -100
          ]
        },
        {
          "kind": "line",
          "end": [
            -12.8765625,
            -100
          ]
        },
        {
          "kind": "line",
          "end": [
            -12.8765625,
            -15.875882812
          ]
        },
        {
          "kind": "arc",
          "end": [
            -17.6171875,
            -11.135257813
          ],
          "center": [
            -17.6171875,
            -15.875882812
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -100,
            -11.135257813
          ]
        },
        {
          "kind": "line",
          "end": [
            -100,
            -1.145
          ]
        }
      ]
    }
  ],
  "corner_left": [
    {
      "start": [
        1.15,
        -1.145
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            100,
            -1.145
          ]
        },
        {
          "kind": "line",
          "end": [
            100,
            -11.135257813
          ]
        },
        {
          "kind": "line",
          "end": [
            17.6171875,
            -11.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            12.8765625,
            -15.875882812
          ],
          "center": [
            17.6171875,
            -15.875882812
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            12.8765625,
            -100
          ]
        },
        {
          "kind": "line",
          "end": [
            1.15,
            -100
          ]
        },
        {
          "kind": "line",
          "end": [
            1.15,
            -1.145
          ]
        }
      ]
    }
  ],
  "corner_right": [
    {
      "start": [
        -1.15,
        -1.145
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -100,
            -1.145
          ]
        },
        {
          "kind": "line",
          "end": [
            -100,
            -11.135257813
          ]
        },
        {
          "kind": "line",
          "end": [
            -17.6171875,
            -11.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            -12.8765625,
            -15.875882812
          ],
          "center": [
            -17.6171875,
            -15.875882812
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -12.8765625,
            -100
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.15,
            -100
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.15,
            -1.145
          ]
        }
      ]
    }
  ]
}

SEAM_PROFILES = {
  "middle": [
    {
      "start": [
        -1.15,
        39
      ],
      "segments": [
        {
          "kind": "arc",
          "end": [
            -0.15,
            40
          ],
          "center": [
            -0.15,
            39
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            0.15,
            40
          ]
        },
        {
          "kind": "arc",
          "end": [
            1.15,
            39
          ],
          "center": [
            0.15,
            39
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            1.15,
            -39
          ]
        },
        {
          "kind": "arc",
          "end": [
            0.15,
            -40
          ],
          "center": [
            0.15,
            -39
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -0.15,
            -40
          ]
        },
        {
          "kind": "arc",
          "end": [
            -1.15,
            -39
          ],
          "center": [
            -0.15,
            -39
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -1.15,
            39
          ]
        }
      ]
    }
  ],
  "edge": [
    {
      "start": [
        -1.15,
        -1
      ],
      "segments": [
        {
          "kind": "arc",
          "end": [
            -0.15,
            0
          ],
          "center": [
            -0.15,
            -1
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            0.15,
            0
          ]
        },
        {
          "kind": "arc",
          "end": [
            1.15,
            -1
          ],
          "center": [
            0.15,
            -1
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            1.15,
            -39
          ]
        },
        {
          "kind": "arc",
          "end": [
            0.15,
            -40
          ],
          "center": [
            0.15,
            -39
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -0.15,
            -40
          ]
        },
        {
          "kind": "arc",
          "end": [
            -1.15,
            -39
          ],
          "center": [
            -0.15,
            -39
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -1.15,
            -1
          ]
        }
      ]
    }
  ]
}

# Source loft end-sections used to replace the phase-1 prismatic rail cut.
RAIL_RELIEF_END_PROFILES = {
  "edge": [
    {
      "start": [
        -100,
        -0.54
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            100,
            -0.54
          ]
        },
        {
          "kind": "line",
          "end": [
            100,
            -11.135257813
          ]
        },
        {
          "kind": "line",
          "end": [
            17.6171875,
            -11.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            12.8765625,
            -15.875882812
          ],
          "center": [
            17.6171875,
            -15.875882812
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            12.8765625,
            -100
          ]
        },
        {
          "kind": "line",
          "end": [
            -12.8765625,
            -100
          ]
        },
        {
          "kind": "line",
          "end": [
            -12.8765625,
            -15.875882812
          ]
        },
        {
          "kind": "arc",
          "end": [
            -17.6171875,
            -11.135257813
          ],
          "center": [
            -17.6171875,
            -15.875882812
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            -100,
            -11.135257813
          ]
        },
        {
          "kind": "line",
          "end": [
            -100,
            -0.54
          ]
        }
      ]
    }
  ],
  "corner_left": [
    {
      "start": [
        0.545,
        -0.54
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            100,
            -0.54
          ]
        },
        {
          "kind": "line",
          "end": [
            100,
            -11.135257813
          ]
        },
        {
          "kind": "line",
          "end": [
            17.6171875,
            -11.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            12.8765625,
            -15.875882812
          ],
          "center": [
            17.6171875,
            -15.875882812
          ],
          "clockwise": False
        },
        {
          "kind": "line",
          "end": [
            12.8765625,
            -100
          ]
        },
        {
          "kind": "line",
          "end": [
            0.545,
            -100
          ]
        },
        {
          "kind": "line",
          "end": [
            0.545,
            -0.54
          ]
        }
      ]
    }
  ],
  "corner_right": [
    {
      "start": [
        -0.545,
        -0.54
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -100,
            -0.54
          ]
        },
        {
          "kind": "line",
          "end": [
            -100,
            -11.135257813
          ]
        },
        {
          "kind": "line",
          "end": [
            -17.6171875,
            -11.135257813
          ]
        },
        {
          "kind": "arc",
          "end": [
            -12.8765625,
            -15.875882812
          ],
          "center": [
            -17.6171875,
            -15.875882812
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -12.8765625,
            -100
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.545,
            -100
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.545,
            -0.54
          ]
        }
      ]
    }
  ]
}

# Late native source features 145–164. Coordinates are normalized to each
# reusable coupler's local XZ frame; off-body suppression placeholders from
# the source sketches are intentionally omitted.
REFERENCE_MARK_LOOPS = {
  "middle": [
    {
      "start": [
        -3,
        0.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -0.4,
            0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            3
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            3
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            3,
            0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            3,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            -3
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            -3
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -3,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -3,
            0.4
          ]
        }
      ]
    },
    {
      "start": [
        -15.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -14.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -14.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -15.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -15.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -20.4,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -19.6,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            -19.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -20.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -20.4,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -25.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -24.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -24.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -25.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -25.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -30.4,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -29.6,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            -29.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -30.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -30.4,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -35.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -34.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -34.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -35.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -35.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        14.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            15.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            15.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            14.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            14.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        19.6,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            20.4,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            20.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            19.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            19.6,
            2
          ]
        }
      ]
    },
    {
      "start": [
        24.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            25.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            25.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            24.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            24.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        29.6,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            30.4,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            30.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            29.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            29.6,
            2
          ]
        }
      ]
    },
    {
      "start": [
        34.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            35.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            35.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            34.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            34.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        5.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            5.4
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            4.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            4.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            5.4
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        10.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            10.4
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            9.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            9.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            10.4
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        15.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            15.4
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            14.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            14.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            15.4
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        20.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            20.4
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            19.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            19.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            20.4
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        25.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            25.4
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            24.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            24.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            25.4
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        30.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            30.4
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            29.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            29.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            30.4
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        35.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            35.4
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            34.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            34.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            35.4
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -4.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -4.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -5.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -5.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -4.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -9.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -9.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -10.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -10.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -9.6
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -14.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -14.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -15.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -15.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -14.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -19.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -19.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -20.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -20.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -19.6
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -24.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -24.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -25.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -25.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -24.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -29.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -29.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -30.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -30.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -29.6
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -34.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -34.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -35.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -35.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -34.6
          ]
        }
      ]
    }
  ],
  "edge": [
    {
      "start": [
        -3,
        0.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -0.4,
            0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            3
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            3
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            3,
            0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            3,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            -3
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            -3
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -3,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -3,
            0.4
          ]
        }
      ]
    },
    {
      "start": [
        -5.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -4.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -4.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -5.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -5.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -10.4,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -9.6,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            -9.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -10.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -10.4,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -15.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -14.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -14.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -15.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -15.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -20.4,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -19.6,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            -19.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -20.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -20.4,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -25.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -24.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -24.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -25.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -25.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -30.4,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -29.6,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            -29.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -30.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -30.4,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -35.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -34.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -34.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -35.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -35.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -40.4,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -39.6,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            -39.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -40.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -40.4,
            2
          ]
        }
      ]
    },
    {
      "start": [
        4.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            5.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            5.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            4.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            4.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        9.6,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            10.4,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            10.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            9.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            9.6,
            2
          ]
        }
      ]
    },
    {
      "start": [
        14.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            15.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            15.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            14.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            14.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        19.6,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            20.4,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            20.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            19.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            19.6,
            2
          ]
        }
      ]
    },
    {
      "start": [
        24.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            25.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            25.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            24.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            24.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        29.6,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            30.4,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            30.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            29.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            29.6,
            2
          ]
        }
      ]
    },
    {
      "start": [
        34.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            35.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            35.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            34.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            34.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        39.6,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            40.4,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            40.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            39.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            39.6,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        5.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            5.4
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            4.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            4.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            5.4
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        10.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            10.4
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            9.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            9.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            10.4
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -4.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -4.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -5.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -5.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -4.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -9.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -9.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -10.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -10.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -9.6
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -14.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -14.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -15.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -15.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -14.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -19.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -19.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -20.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -20.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -19.6
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -24.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -24.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -25.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -25.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -24.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -29.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -29.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -30.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -30.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -29.6
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -34.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -34.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -35.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -35.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -34.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -39.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -39.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -40.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -40.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -39.6
          ]
        }
      ]
    }
  ],
  "corner_left": [
    {
      "start": [
        -3,
        0.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -0.4,
            0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            3
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            3
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            3,
            0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            3,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            -3
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            -3
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -3,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -3,
            0.4
          ]
        }
      ]
    },
    {
      "start": [
        -5.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -4.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -4.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -5.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -5.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -10.4,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -9.6,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            -9.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -10.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -10.4,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -15.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -14.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -14.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -15.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -15.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -20.4,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -19.6,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            -19.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -20.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -20.4,
            2
          ]
        }
      ]
    },
    {
      "start": [
        4.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            5.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            5.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            4.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            4.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        9.6,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            10.4,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            10.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            9.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            9.6,
            2
          ]
        }
      ]
    },
    {
      "start": [
        14.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            15.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            15.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            14.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            14.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        19.6,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            20.4,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            20.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            19.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            19.6,
            2
          ]
        }
      ]
    },
    {
      "start": [
        24.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            25.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            25.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            24.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            24.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        29.6,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            30.4,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            30.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            29.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            29.6,
            2
          ]
        }
      ]
    },
    {
      "start": [
        34.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            35.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            35.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            34.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            34.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        39.6,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            40.4,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            40.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            39.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            39.6,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        5.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            5.4
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            4.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            4.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            5.4
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        10.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            10.4
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            9.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            9.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            10.4
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        15.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            15.4
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            14.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            14.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            15.4
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        20.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            20.4
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            19.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            19.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            20.4
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -4.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -4.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -5.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -5.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -4.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -9.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -9.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -10.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -10.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -9.6
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -14.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -14.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -15.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -15.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -14.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -19.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -19.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -20.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -20.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -19.6
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -24.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -24.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -25.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -25.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -24.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -29.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -29.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -30.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -30.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -29.6
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -34.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -34.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -35.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -35.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -34.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -39.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -39.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -40.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -40.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -39.6
          ]
        }
      ]
    }
  ],
  "corner_right": [
    {
      "start": [
        3,
        0.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            0.4,
            0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            3
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            3
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -3,
            0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -3,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -0.4,
            -3
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            -3
          ]
        },
        {
          "kind": "line",
          "end": [
            0.4,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            3,
            -0.4
          ]
        },
        {
          "kind": "line",
          "end": [
            3,
            0.4
          ]
        }
      ]
    },
    {
      "start": [
        4.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            5.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            5.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            4.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            4.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        9.6,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            10.4,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            10.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            9.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            9.6,
            2
          ]
        }
      ]
    },
    {
      "start": [
        14.6,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            15.4,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            15.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            14.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            14.6,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        19.6,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            20.4,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            20.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            19.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            19.6,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -5.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -4.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -4.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -5.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -5.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -10.4,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -9.6,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            -9.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -10.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -10.4,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -15.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -14.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -14.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -15.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -15.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -20.4,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -19.6,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            -19.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -20.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -20.4,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -25.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -24.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -24.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -25.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -25.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -30.4,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -29.6,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            -29.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -30.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -30.4,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -35.4,
        1.1
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -34.6,
            1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -34.6,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -35.4,
            -1.1
          ]
        },
        {
          "kind": "line",
          "end": [
            -35.4,
            1.1
          ]
        }
      ]
    },
    {
      "start": [
        -40.4,
        2
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            -39.6,
            2
          ]
        },
        {
          "kind": "line",
          "end": [
            -39.6,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -40.4,
            -2
          ]
        },
        {
          "kind": "line",
          "end": [
            -40.4,
            2
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        5.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            5.4
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            4.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            4.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            5.4
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        10.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            10.4
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            9.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            9.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            10.4
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        15.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            15.4
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            14.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            14.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            15.4
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        20.4
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            20.4
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            19.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            19.6
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            20.4
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -4.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -4.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -5.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -5.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -4.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -9.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -9.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -10.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -10.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -9.6
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -14.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -14.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -15.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -15.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -14.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -19.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -19.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -20.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -20.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -19.6
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -24.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -24.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -25.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -25.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -24.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -29.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -29.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -30.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -30.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -29.6
          ]
        }
      ]
    },
    {
      "start": [
        -1.1,
        -34.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            1.1,
            -34.6
          ]
        },
        {
          "kind": "line",
          "end": [
            1.1,
            -35.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -35.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -1.1,
            -34.6
          ]
        }
      ]
    },
    {
      "start": [
        -2,
        -39.6
      ],
      "segments": [
        {
          "kind": "line",
          "end": [
            2,
            -39.6
          ]
        },
        {
          "kind": "line",
          "end": [
            2,
            -40.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -40.4
          ]
        },
        {
          "kind": "line",
          "end": [
            -2,
            -39.6
          ]
        }
      ]
    }
  ]
}

REFERENCE_HOLE_CENTERS = {
  "middle": [
    [
      -20,
      7.5
    ],
    [
      -20,
      -7.5
    ],
    [
      20,
      7.5
    ],
    [
      20,
      -7.5
    ],
    [
      -30,
      7.5
    ],
    [
      -30,
      -7.5
    ],
    [
      30,
      7.5
    ],
    [
      30,
      -7.5
    ],
    [
      -7.5,
      20
    ],
    [
      7.5,
      20
    ],
    [
      -7.5,
      -20
    ],
    [
      7.5,
      -20
    ],
    [
      -7.5,
      30
    ],
    [
      7.5,
      30
    ],
    [
      -7.5,
      -30
    ],
    [
      7.5,
      -30
    ]
  ],
  "edge": [
    [
      -20,
      -5.758695312
    ],
    [
      20,
      -5.758695312
    ],
    [
      -30,
      -5.758695312
    ],
    [
      30,
      -5.758695312
    ],
    [
      -7.5,
      -20
    ],
    [
      7.5,
      -20
    ],
    [
      -7.5,
      -30
    ],
    [
      7.5,
      -30
    ]
  ],
  "corner_left": [
    [
      20,
      -7.5
    ],
    [
      30,
      -7.5
    ],
    [
      9.241304687,
      -20
    ],
    [
      9.241304687,
      -30
    ]
  ],
  "corner_right": [
    [
      -20,
      -7.5
    ],
    [
      -30,
      -7.5
    ],
    [
      -9.241304687,
      -20
    ],
    [
      -9.241304687,
      -30
    ]
  ]
}

REFERENCE_PATTERN = {
  "mark_depth": 0.4,
  "mark_cut_depth": 0.45,
  "hole_d": 3.0,
  "tip_d": 2.0,
  "straight_h": 1.5,
  "tip_h": 0.5,
  "rear_offset": 0.05,
}

# Exact native tip sections for the tapered seam-guide joins (features 80/140).
SEAM_TIP_PROFILES = {
  "middle": [
    {
      "start": [
        -0.75,
        39.26
      ],
      "segments": [
        {
          "kind": "arc",
          "end": [
            -0.01,
            40
          ],
          "center": [
            -0.01,
            39.26
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            0.01,
            40
          ]
        },
        {
          "kind": "arc",
          "end": [
            0.75,
            39.26
          ],
          "center": [
            0.01,
            39.26
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            0.75,
            -39.26
          ]
        },
        {
          "kind": "arc",
          "end": [
            0.01,
            -40
          ],
          "center": [
            0.01,
            -39.26
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -0.01,
            -40
          ]
        },
        {
          "kind": "arc",
          "end": [
            -0.75,
            -39.26
          ],
          "center": [
            -0.01,
            -39.26
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -0.75,
            39.26
          ]
        }
      ]
    }
  ],
  "edge": [
    {
      "start": [
        -0.75,
        -0.74
      ],
      "segments": [
        {
          "kind": "arc",
          "end": [
            -0.01,
            0
          ],
          "center": [
            -0.01,
            -0.74
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            0.01,
            0
          ]
        },
        {
          "kind": "arc",
          "end": [
            0.75,
            -0.74
          ],
          "center": [
            0.01,
            -0.74
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            0.75,
            -39.26
          ]
        },
        {
          "kind": "arc",
          "end": [
            0.01,
            -40
          ],
          "center": [
            0.01,
            -39.26
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -0.01,
            -40
          ]
        },
        {
          "kind": "arc",
          "end": [
            -0.75,
            -39.26
          ],
          "center": [
            -0.01,
            -39.26
          ],
          "clockwise": True
        },
        {
          "kind": "line",
          "end": [
            -0.75,
            -0.74
          ]
        }
      ]
    }
  ]
}

# Exact Edge guide-end rounding cut (features 137–138), normalized to Edge XZ.
EDGE_GUIDE_END_CUTS = [
  {
    "start": [
      -36.828427125,
      -11.135257813
    ],
    "segments": [
      {
        "kind": "line",
        "end": [
          -39.656854249,
          -11.135257813
        ]
      },
      {
        "kind": "arc",
        "end": [
          -37.771236166,
          -13.801924479
        ],
        "center": [
          -34,
          -9.135257813
        ],
        "clockwise": False
      },
      {
        "kind": "arc",
        "end": [
          -36.828427125,
          -11.135257813
        ],
        "center": [
          -36.828427125,
          -12.635257813
        ],
        "clockwise": True
      }
    ]
  },
  {
    "start": [
      36.828427125,
      -11.135257813
    ],
    "segments": [
      {
        "kind": "line",
        "end": [
          39.656854249,
          -11.135257813
        ]
      },
      {
        "kind": "arc",
        "end": [
          37.771236166,
          -13.801924479
        ],
        "center": [
          34,
          -9.135257813
        ],
        "clockwise": True
      },
      {
        "kind": "arc",
        "end": [
          36.828427125,
          -11.135257813
        ],
        "center": [
          36.828427125,
          -12.635257813
        ],
        "clockwise": False
      }
    ]
  },
  {
    "start": [
      -12.8765625,
      -36.828427125
    ],
    "segments": [
      {
        "kind": "line",
        "end": [
          -12.8765625,
          -39.656854249
        ]
      },
      {
        "kind": "arc",
        "end": [
          -15.543229167,
          -37.771236166
        ],
        "center": [
          -10.8765625,
          -34
        ],
        "clockwise": True
      },
      {
        "kind": "arc",
        "end": [
          -12.8765625,
          -36.828427125
        ],
        "center": [
          -14.3765625,
          -36.828427125
        ],
        "clockwise": False
      }
    ]
  },
  {
    "start": [
      12.8765625,
      -36.828427125
    ],
    "segments": [
      {
        "kind": "line",
        "end": [
          12.8765625,
          -39.656854249
        ]
      },
      {
        "kind": "arc",
        "end": [
          15.543229167,
          -37.771236166
        ],
        "center": [
          10.8765625,
          -34
        ],
        "clockwise": False
      },
      {
        "kind": "arc",
        "end": [
          12.8765625,
          -36.828427125
        ],
        "center": [
          14.3765625,
          -36.828427125
        ],
        "clockwise": True
      }
    ]
  },
  {
    "start": [
      -36.828427125,
      -1.145
    ],
    "segments": [
      {
        "kind": "line",
        "end": [
          -39.656854249,
          -1.145
        ]
      },
      {
        "kind": "arc",
        "end": [
          -37.771236166,
          1.521666667
        ],
        "center": [
          -34,
          -3.145
        ],
        "clockwise": True
      },
      {
        "kind": "arc",
        "end": [
          -36.828427125,
          -1.145
        ],
        "center": [
          -36.828427125,
          0.355
        ],
        "clockwise": False
      }
    ]
  },
  {
    "start": [
      36.828427125,
      -1.145
    ],
    "segments": [
      {
        "kind": "line",
        "end": [
          39.656854249,
          -1.145
        ]
      },
      {
        "kind": "arc",
        "end": [
          37.771236166,
          1.521666667
        ],
        "center": [
          34,
          -3.145
        ],
        "clockwise": False
      },
      {
        "kind": "arc",
        "end": [
          36.828427125,
          -1.145
        ],
        "center": [
          36.828427125,
          0.355
        ],
        "clockwise": True
      }
    ]
  }
]

# Final active tube-frame Edge additions from assembly source features 226–230.
# Coordinates are normalized from the top Edge occurrence to physical local XZ
# (source world Z=320 -> local Z=0). These are retained source contours, like
# the accepted Medium profiles above; the production model does not expose
# these solver-resolved points as user parameters.
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
# REFERENCE_MARK_LOOPS["edge"] ordering these are exactly entries 21 and 22.
TUBE_EDGE_REAR_REFERENCE_MARK_INDICES = (21, 22)

