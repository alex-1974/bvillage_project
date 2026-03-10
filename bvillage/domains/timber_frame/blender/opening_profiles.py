# bvillage/domains/timber_frame/blender/opening_profiles.py

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OpeningProfilePolicy:
    """
    Historisch plausible Querschnitte (meters)
    Norddeutsches Hallenhaus, 15.-16. Jh.
    """

    # Laibungsständer (tragend)
    jamb_post: tuple[float, float] = (0.18, 0.18)

    # Fenster
    window_lintel: tuple[float, float] = (0.16, 0.18)
    window_sill: tuple[float, float] = (0.16, 0.16)

    # Tor
    gate_lintel: tuple[float, float] = (0.20, 0.20)

    # Schwelle optional
    threshold: tuple[float, float] = (0.20, 0.22)
