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
