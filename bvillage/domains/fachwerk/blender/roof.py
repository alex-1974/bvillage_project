# bvillage/domains/fachwerk/blender/roof.py

from math import tan, radians
from mathutils import Vector
from .timber import make_beam_rect


def build_roof_per_field(
    *,
    axes_u,
    half_width: float,
    z_plate: float,
    roof_pitch_deg: float = 50.0,
    kehl_frac: float = 0.58,
    col_roof=None,
    profiles=None,
):
    """
    Build roof timbers per longitudinal field:
      - 1 rafter pair per field at xmid
      - 1 collar tie (Kehlbalken) per field
      - 1 continuous ridge purlin (Firstpfette)

    axes_u: list of x positions (len >= 2)
    half_width: W/2 (e.g. 3.45)
    z_plate: wall plate height (e.g. 2.2)

    profiles: dict with sizes in meters:
      {
        "ridge": (w,d),
        "rafter": (w,d),
        "collar": (w,d),
      }
    """
    if profiles is None:
        profiles = {
            "ridge": (0.18, 0.22),
            "rafter": (0.10, 0.16),
            "collar": (0.12, 0.16),
        }

    if not axes_u or len(axes_u) < 2:
        raise ValueError("axes_u must contain at least 2 values")

    # ridge height from pitch and half span
    h = tan(radians(roof_pitch_deg)) * half_width
    z_ridge = z_plate + h

    # collar height by fraction along the roof height
    kehl_frac = max(0.50, min(0.70, kehl_frac))
    z_kehl = z_plate + kehl_frac * (z_ridge - z_plate)

    # y at collar height along the rafter line
    y_kehl = (z_kehl - z_plate) / tan(radians(roof_pitch_deg))

    # ridge purlin, continuous
    make_beam_rect(
        "Firstpfette",
        Vector((axes_u[0], 0.0, z_ridge)),
        Vector((axes_u[-1], 0.0, z_ridge)),
        width=profiles["ridge"][0],
        depth=profiles["ridge"][1],
        collection=col_roof,
    )

    # per field: rafter pair + collar tie
    for i in range(len(axes_u) - 1):
        xmid = 0.5 * (axes_u[i] + axes_u[i + 1])

        make_beam_rect(
            f"Rafter_L_{i:02d}",
            Vector((xmid, -half_width, z_plate)),
            Vector((xmid, 0.0, z_ridge)),
            width=profiles["rafter"][0],
            depth=profiles["rafter"][1],
            collection=col_roof,
        )

        make_beam_rect(
            f"Rafter_R_{i:02d}",
            Vector((xmid, +half_width, z_plate)),
            Vector((xmid, 0.0, z_ridge)),
            width=profiles["rafter"][0],
            depth=profiles["rafter"][1],
            collection=col_roof,
        )

        make_beam_rect(
            f"Kehlbalken_{i:02d}",
            Vector((xmid, -y_kehl, z_kehl)),
            Vector((xmid, +y_kehl, z_kehl)),
            width=profiles["collar"][0],
            depth=profiles["collar"][1],
            collection=col_roof,
        )

    return {"z_ridge": z_ridge, "z_kehl": z_kehl, "y_kehl": y_kehl}
