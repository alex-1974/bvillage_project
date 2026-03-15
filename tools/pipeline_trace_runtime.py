# tools/pipeline_trace_runtime.py

from __future__ import annotations

import argparse
from pathlib import Path

from bvillage.core.model import Context
from bvillage.core.seed import Seed
from bvillage.core.site_manager import SiteManager
from bvillage.core.trace import configure_trace, get_trace


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archetype", required=True)
    parser.add_argument("--grammar", default="hall")
    parser.add_argument("--region", default="unknown")
    parser.add_argument("--epoch-band", default="high_medieval")
    parser.add_argument("--settlement-type", default="rural")
    parser.add_argument("--wealth", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--out", default="generated/PIPELINE_TRACE.txt")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    configure_trace(
        enabled=True,
        out_path=Path(args.out),
    )

    ctx = Context(
        seed=Seed(args.seed),
        region=args.region,
        epoch_band=args.epoch_band,
        settlement_type=args.settlement_type,
        wealth=args.wealth,
        archetype_id=args.archetype,
        grammar=args.grammar,
    )

    sm = SiteManager()
    structure, interior, openings = sm.build(ctx)

    trace = get_trace()
    path = trace.write_report()

    print(trace.render_text())
    if path is not None:
        print()
        print(f"Trace written to {path}")

    _ = structure
    _ = interior
    _ = openings


if __name__ == "__main__":
    main()
