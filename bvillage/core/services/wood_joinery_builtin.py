# bvillage/core/services/wood_joinery_builtin.py

"""
bvillage/core/services/wood_joinery.py

Offene, kleine Registry für sichtbare Holzverbindungsmerkmale.

Scope:
- registriert JoinerySpecs
- löst sichtbare Marks deterministisch auf
- blender-frei
- plan-frei
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable

from bvillage.core.contracts.joinery import (
    FaceId,
    JoineryRequest,
    JoinerySpec,
    MemberRef,
    VisibleMark,
)


class JoineryRegistrationError(ValueError):
    pass


class JoineryResolutionError(KeyError):
    pass


def _freeze_parameters(parameters: dict | object) -> tuple[tuple[str, object], ...]:
    if not isinstance(parameters, dict):
        if hasattr(parameters, "items"):
            return tuple(sorted(parameters.items()))
        return ()
    return tuple(sorted(parameters.items()))


def _member_section_class(member: MemberRef) -> tuple[int, int]:
    """
    Grobe Querschnittsklasse in mm, cache-freundlich.
    """
    return (round(member.section_w_m * 1000), round(member.section_h_m * 1000))


@dataclass(slots=True)
class _RuntimeSpec:
    spec: JoinerySpec


class WoodJoineryService:
    def __init__(self) -> None:
        self._registry: dict[str, _RuntimeSpec] = {}

    def register(self, spec: JoinerySpec) -> None:
        if not spec.joinery_id:
            raise JoineryRegistrationError("joinery_id must not be empty.")
        if spec.joinery_id in self._registry:
            raise JoineryRegistrationError(f"joinery_id already registered: {spec.joinery_id}")
        self._registry[spec.joinery_id] = _RuntimeSpec(spec=spec)
        self._resolve_cached.cache_clear()

    def is_registered(self, joinery_id: str) -> bool:
        return joinery_id in self._registry

    def list_joinery_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._registry.keys()))

    def resolve_visible_marks(self, request: JoineryRequest) -> tuple[VisibleMark, ...]:
        runtime = self._registry.get(request.joinery_id)
        if runtime is None:
            raise JoineryResolutionError(f"Unknown joinery_id: {request.joinery_id}")

        if request.context.detail_level == "none":
            return ()

        return self._resolve_cached(
            request.joinery_id,
            request.member_a.member_id,
            request.member_b.member_id,
            _member_section_class(request.member_a),
            _member_section_class(request.member_b),
            tuple(sorted(
                (member_id, faces)
                for member_id, faces in request.face_mask.visible_faces_by_member.items()
            )),
            request.context.region_id,
            request.context.epoch_id,
            request.context.wealth_id,
            request.context.craft_tradition_id,
            request.context.detail_level,
            _freeze_parameters(dict(request.parameters)),
            request,
        )

    @lru_cache(maxsize=2048)
    def _resolve_cached(
        self,
        joinery_id: str,
        member_a_id: str,
        member_b_id: str,
        member_a_section_class: tuple[int, int],
        member_b_section_class: tuple[int, int],
        visible_faces_key: tuple[tuple[str, tuple[str, ...]], ...],
        region_id: str | None,
        epoch_id: str | None,
        wealth_id: str | None,
        craft_tradition_id: str | None,
        detail_level: str,
        parameters_key: tuple[tuple[str, object], ...],
        request: JoineryRequest,
    ) -> tuple[VisibleMark, ...]:
        runtime = self._registry[joinery_id]
        return runtime.spec.visible_marks_fn(request)


wood_joinery = WoodJoineryService()
