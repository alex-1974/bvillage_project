# bvillage/core/grid.py

from __future__ import annotations
from typing import List, Tuple
from .model import FieldCell, Grid


def build_rect_grid(length: float, width: float, bays_x: int, bays_y: int) -> Grid:
    """
    length  = building length (x-direction)
    width   = building width (y-direction)
    bays_x  = number of longitudinal fields
    bays_y  = number of transverse fields
    """

    dx = length / bays_x
    dy = width / bays_y

    axes_u = tuple(round(i * dx, 6) for i in range(bays_x + 1))
    axes_v = tuple(round(-width / 2 + i * dy, 6) for i in range(bays_y + 1))

    fields: List[FieldCell] = []

    for ix in range(bays_x):
        for iy in range(bays_y):
            minx = axes_u[ix]
            maxx = axes_u[ix + 1]
            miny = axes_v[iy]
            maxy = axes_v[iy + 1]

            fid = f"F_{ix}_{iy}"
            fields.append(
                FieldCell(
                    id=fid,
                    bbox=(minx, miny, maxx, maxy),
                    tags=("INTERIOR",)
                )
            )

    return Grid(
        axes_u=axes_u,
        axes_v=axes_v,
        fields=tuple(fields)
    )
