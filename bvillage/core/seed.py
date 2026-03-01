# bvillage/core/seed.py

from __future__ import annotations

from dataclasses import dataclass
import hashlib


@dataclass(frozen=True, slots=True)
class Seed:
    """Deterministic seed wrapper.

    `derive(component)` returns a stable integer seed for sub-components.
    Component strings are stable API: changing them changes output.
    """
    base: int

    def derive(self, component: str) -> int:
        key = f"{self.base}:{component}".encode("utf-8")
        # 32-bit is enough for random.Random; stable across platforms.
        return int.from_bytes(hashlib.blake2s(key, digest_size=4).digest(), "big")
