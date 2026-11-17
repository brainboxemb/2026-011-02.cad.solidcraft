"""Model-specific native SolidCraft validation registry."""
from .basic import (
    validate_corner_bracket,
    validate_guide_rail,
    validate_plastic_enclosure,
    validate_plastic_enclosure_pi,
    validate_sample_plate,
)
from .hub75 import validate_hub75_panel, validate_hub75_screen
from .mft import validate_simple_mft_assembly
from .wood_frame import validate_hub75_wood_frame

VALIDATORS = {
    "hub75-panel": validate_hub75_panel,
    "guide-rail": validate_guide_rail,
    "hub75-screen": validate_hub75_screen,
    "simple-mft-assembly": validate_simple_mft_assembly,
    "corner-bracket": validate_corner_bracket,
    "sample-plate": validate_sample_plate,
    "plastic-enclosure": validate_plastic_enclosure,
    "plastic-enclosure-pi": validate_plastic_enclosure_pi,
    "hub75-wood-frame": validate_hub75_wood_frame,
}
