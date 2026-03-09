# bvillage/domains/fachwerk/validation/frameplan_checks.py

from __future__ import annotations

from typing import Any

from bvillage.core.model import Issue


def run_arch_checks(frameplan: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []

    schema = int(frameplan.get("schema_version", 0) or 0)
    members = frameplan.get("members") or {}
    posts = members.get("posts") or []
    rails = members.get("rails") or []
    braces = members.get("braces") or []

    # --- HARD: must have members-first basics ---
    if schema != 4:
        issues.append(
            Issue(
                code="SCHEMA",
                severity="HARD",
                message=f"Expected schema_version=4, got {schema}.",
            )
        )
        return issues

    if not posts:
        issues.append(
            Issue(
                code="NO_POSTS",
                severity="HARD",
                message="members.posts is empty.",
            )
        )
    if not rails:
        issues.append(
            Issue(
                code="NO_RAILS",
                severity="HARD",
                message="members.rails is empty.",
            )
        )

    # --- SOFT: brace density ---
    if len(braces) < 6:
        issues.append(
            Issue(
                code="LOW_BRACING",
                severity="SOFT",
                message=f"Brace count is low ({len(braces)}).",
            )
        )

    return issues


def log_arch_checks(logger: Any, frameplan: dict[str, Any], issues: list[Issue]) -> None:
    members = frameplan.get("members") or {}
    posts = members.get("posts") or []
    rails = members.get("rails") or []
    braces = members.get("braces") or []

    hard = [i for i in issues if i.severity == "HARD"]
    soft = [i for i in issues if i.severity == "SOFT"]

    logger.info(
        "\n=== ARCH CHECKS (TIMBER FRAME) ===\n"
        "schema_version      : %s\n"
        "posts               : %d\n"
        "beams/rails         : %d\n"
        "braces              : %d\n"
        "issues              : hard=%d soft=%d\n"
        "===============================\n",
        frameplan.get("schema_version"),
        len(posts),
        len(rails),
        len(braces),
        len(hard),
        len(soft),
    )

    for i in hard:
        logger.error("ARCH CHECK [HARD] %s: %s", i.code, i.message)
    for i in soft:
        logger.warning("ARCH CHECK [SOFT] %s: %s", i.code, i.message)
