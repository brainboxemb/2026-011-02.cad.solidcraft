"""Fixed guide-rail cross-section variants."""

from . import festool, makita

PROFILES = {
    "festool": festool,
    "makita": makita,
}


def get_profile(name):
    key = "festool" if name is None else name
    if not isinstance(key, str):
        raise TypeError("guide rail profile must be text")
    try:
        return PROFILES[key.lower()]
    except KeyError as exc:
        supported = ", ".join(sorted(PROFILES))
        raise ValueError(
            f"unknown guide rail profile {name!r}; expected one of: {supported}"
        ) from exc
