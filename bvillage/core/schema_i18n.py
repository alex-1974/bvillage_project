# bvillage/core/schema_i18n.py

from __future__ import annotations

from collections import defaultdict
from typing import Any

__all__ = [
    "register_locale_catalog",
    "get_archetype_meta",
    "get_archetype_label",
    "get_archetype_aliases",
    "get_archetype_keywords",
    "find_archetype_ids_by_term",
]


# locale -> archetype_id -> metadata
_LOCALE_CATALOGS: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)

_DEFAULT_LOCALE = "en"


def _normalize_entry(archetype_id: str, data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise RuntimeError(f"Locale entry for {archetype_id!r} must be a mapping")

    name = data.get("name", archetype_id)
    short_name = data.get("short_name", name)
    description = data.get("description", "")
    aliases = data.get("aliases", [])
    keywords = data.get("keywords", [])

    if not isinstance(name, str) or not name.strip():
        raise RuntimeError(f"Locale entry for {archetype_id!r} requires non-empty 'name'")
    if not isinstance(short_name, str) or not short_name.strip():
        raise RuntimeError(f"Locale entry for {archetype_id!r} requires non-empty 'short_name'")
    if not isinstance(description, str):
        raise RuntimeError(f"Locale entry for {archetype_id!r} requires string 'description'")
    if not isinstance(aliases, list) or not all(isinstance(x, str) for x in aliases):
        raise RuntimeError(f"Locale entry for {archetype_id!r} requires 'aliases' as list[str]")
    if not isinstance(keywords, list) or not all(isinstance(x, str) for x in keywords):
        raise RuntimeError(f"Locale entry for {archetype_id!r} requires 'keywords' as list[str]")

    return {
        "name": name.strip(),
        "short_name": short_name.strip(),
        "description": description.strip(),
        "aliases": tuple(x.strip() for x in aliases if x.strip()),
        "keywords": tuple(x.strip() for x in keywords if x.strip()),
    }


def register_locale_catalog(locale: str, catalog: dict[str, dict[str, Any]]) -> None:
    """
    Register one locale catalog provided by a plugin.

    Catalog format
    --------------
    archetype_id -> {
        "name": str,
        "short_name": str,
        "description": str,
        "aliases": list[str],
        "keywords": list[str],
    }
    """
    if not locale or not isinstance(locale, str):
        raise RuntimeError("Locale must be a non-empty string")

    target = _LOCALE_CATALOGS[locale]

    for archetype_id, raw_data in catalog.items():
        if not isinstance(archetype_id, str) or not archetype_id.strip():
            raise RuntimeError("Locale catalog contains invalid archetype_id")

        data = _normalize_entry(archetype_id, raw_data)

        existing = target.get(archetype_id)
        if existing is not None and existing != data:
            raise RuntimeError(
                f"Conflicting locale registration for {archetype_id!r} in locale {locale!r}"
            )

        target[archetype_id] = data


def get_archetype_meta(archetype_id: str, locale: str = "en") -> dict[str, Any]:
    catalog = _LOCALE_CATALOGS.get(locale)
    if catalog and archetype_id in catalog:
        return dict(catalog[archetype_id])

    fallback = _LOCALE_CATALOGS.get(_DEFAULT_LOCALE)
    if fallback and archetype_id in fallback:
        return dict(fallback[archetype_id])

    return {
        "name": archetype_id,
        "short_name": archetype_id,
        "description": "",
        "aliases": (),
        "keywords": (),
    }


def get_archetype_label(archetype_id: str, locale: str = "en", *, short: bool = False) -> str:
    meta = get_archetype_meta(archetype_id, locale=locale)
    key = "short_name" if short else "name"
    value = meta.get(key)
    if isinstance(value, str) and value.strip():
        return value
    return archetype_id


def get_archetype_aliases(archetype_id: str, locale: str = "en") -> tuple[str, ...]:
    meta = get_archetype_meta(archetype_id, locale=locale)
    aliases = meta.get("aliases", ())
    if isinstance(aliases, tuple):
        return aliases
    if isinstance(aliases, list):
        return tuple(x for x in aliases if isinstance(x, str))
    return ()


def get_archetype_keywords(archetype_id: str, locale: str = "en") -> tuple[str, ...]:
    meta = get_archetype_meta(archetype_id, locale=locale)
    keywords = meta.get("keywords", ())
    if isinstance(keywords, tuple):
        return keywords
    if isinstance(keywords, list):
        return tuple(x for x in keywords if isinstance(x, str))
    return ()


def find_archetype_ids_by_term(term: str, locale: str = "en") -> tuple[str, ...]:
    """
    Best-effort reverse lookup for UI/search.

    This is NOT dispatch logic.
    """
    needle = str(term).strip().casefold()
    if not needle:
        return ()

    results: list[str] = []
    catalog = _LOCALE_CATALOGS.get(locale) or {}
    fallback = _LOCALE_CATALOGS.get(_DEFAULT_LOCALE) or {}

    combined: dict[str, dict[str, Any]] = dict(fallback)
    combined.update(catalog)

    for archetype_id, meta in combined.items():
        fields: list[str] = []

        for key in ("name", "short_name", "description"):
            value = meta.get(key)
            if isinstance(value, str):
                fields.append(value)

        for key in ("aliases", "keywords"):
            value = meta.get(key, ())
            if isinstance(value, (list, tuple)):
                fields.extend(x for x in value if isinstance(x, str))

        haystack = " | ".join(fields).casefold()
        if needle in haystack:
            results.append(archetype_id)

    return tuple(sorted(set(results)))
