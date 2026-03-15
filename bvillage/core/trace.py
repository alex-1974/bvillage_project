# bvillage/core/trace.py

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

__all__ = [
    "TraceEvent",
    "NullTrace",
    "ActiveTrace",
    "configure_trace",
    "get_trace",
    "trace_enabled_from_env",
]


@dataclass(slots=True)
class TraceEvent:
    name: str
    start_s: float
    end_s: float | None = None
    data: dict[str, Any] = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        if self.end_s is None:
            return 0.0
        return (self.end_s - self.start_s) * 1000.0


class NullTrace:
    enabled = False

    def enter(self, name: str, **data: Any) -> None:
        _ = name
        _ = data
        return None

    def exit(self, ev: None, **data: Any) -> None:
        _ = ev
        _ = data
        return None

    @contextmanager
    def stage(self, name: str, **data: Any) -> Iterator[None]:
        _ = name
        _ = data
        yield None

    def add_data(self, ev: None, **data: Any) -> None:
        _ = ev
        _ = data
        return None

    def write_report(self) -> Path | None:
        return None

    def render_text(self) -> str:
        return ""


@dataclass(slots=True)
class ActiveTrace:
    enabled: bool = True
    out_path: Path | None = None
    events: list[TraceEvent] = field(default_factory=list)

    def enter(self, name: str, **data: Any) -> TraceEvent:
        ev = TraceEvent(
            name=name,
            start_s=time.perf_counter(),
            data=dict(data),
        )
        self.events.append(ev)
        return ev

    def exit(self, ev: TraceEvent | None, **data: Any) -> None:
        if ev is None:
            return
        if data:
            ev.data.update(data)
        ev.end_s = time.perf_counter()

    @contextmanager
    def stage(self, name: str, **data: Any) -> Iterator[TraceEvent]:
        ev = self.enter(name, **data)
        try:
            yield ev
        finally:
            self.exit(ev)

    def add_data(self, ev: TraceEvent | None, **data: Any) -> None:
        if ev is None or not data:
            return
        ev.data.update(data)

    def render_text(self) -> str:
        lines: list[str] = []
        lines.append("BVILLAGE PIPELINE TRACE")
        lines.append("======================")
        lines.append("")

        if not self.events:
            lines.append("(no events)")
            return "\n".join(lines)

        width = max(len(ev.name) for ev in self.events)
        for ev in self.events:
            lines.append(f"{ev.name:<{width}}  {ev.duration_ms:8.3f} ms")
            if ev.data:
                for key in sorted(ev.data):
                    lines.append(f"  - {key}: {ev.data[key]}")
        return "\n".join(lines)

    def write_report(self) -> Path | None:
        if self.out_path is None:
            return None
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        self.out_path.write_text(self.render_text(), encoding="utf-8")
        return self.out_path


_NULL_TRACE = NullTrace()
_TRACE: NullTrace | ActiveTrace = _NULL_TRACE


def trace_enabled_from_env() -> bool:
    return os.getenv("BVILLAGE_TRACE", "0") == "1"


def configure_trace(*, enabled: bool, out_path: str | Path | None = None) -> None:
    global _TRACE
    if not enabled:
        _TRACE = _NULL_TRACE
        return
    _TRACE = ActiveTrace(
        enabled=True,
        out_path=Path(out_path) if out_path is not None else None,
    )


def get_trace() -> NullTrace | ActiveTrace:
    return _TRACE
