# bvillage/core/contracts/joinery.py

"""
bvillage/core/contracts/joinery.py

Neutraler Contract für sichtbare Holzverbindungsmerkmale.

Scope:
- blender-frei
- plan-frei
- keine Mechanik
- nur sichtbare Außenmerkmale
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Literal, Mapping, Protocol, Sequence

FaceId = Literal["front", "back", "left", "right", "top", "bottom", "end_a", "end_b"]
DetailLevel = Literal["none", "low", "medium", "high"]
VisibleMarkKind = Literal["peg", "seam_line", "notch_line", "scarf_line", "wedge_mark", "surface_patch"]


@dataclass(frozen=True, slots=True)
class MemberRef:
    member_id: str
    role: str
    section_w_m: float
    section_h_m: float
    length_m: float


@dataclass(frozen=True, slots=True)
class FaceMask:
    """
    Gibt an, welche Faces eines Members außen sichtbar sind.
    Nur für sichtbare Faces sollen Marks erzeugt werden.
    """
    visible_faces_by_member: Mapping[str, tuple[FaceId, ...]]

    def is_visible(self, member_id: str, face: FaceId) -> bool:
        return face in self.visible_faces_by_member.get(member_id, ())


@dataclass(frozen=True, slots=True)
class JoineryContext:
    """
    Kleiner, vorbereiteter Kontext für viele Verbindungen eines Hauses.
    Kann später erweitert werden, soll im Hot Path aber klein bleiben.
    """
    region_id: str | None = None
    epoch_id: str | None = None
    wealth_id: str | None = None
    craft_tradition_id: str | None = None
    detail_level: DetailLevel = "medium"


@dataclass(frozen=True, slots=True)
class VisibleMark:
    """
    Neutrale Beschreibung eines außen sichtbaren Merkmals.
    Keine Geometrieobjekte, keine Renderinstruktionen.
    """
    kind: VisibleMarkKind
    member_id: str
    face: FaceId
    geometry_local: Mapping[str, object]
    style: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class JoineryRequest:
    """
    Anfrage an wood_joinery für genau eine konkrete Verbindungssituation.
    """
    joinery_id: str
    member_a: MemberRef
    member_b: MemberRef
    face_mask: FaceMask
    context: JoineryContext
    parameters: Mapping[str, object] = field(default_factory=dict)


class VisibleMarksFn(Protocol):
    def __call__(self, request: JoineryRequest) -> tuple[VisibleMark, ...]:
        ...


@dataclass(frozen=True, slots=True)
class JoinerySpec:
    """
    Registrierbarer Verbindungstyp.
    """
    joinery_id: str
    visible_marks_fn: VisibleMarksFn
    parameter_schema: Mapping[str, type] = field(default_factory=dict)
    metadata: Mapping[str, object] = field(default_factory=dict)
