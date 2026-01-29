# ======================================================
# MEDICINE TYPE SNAPSHOT LOADER
# ======================================================

from .alias_registry import build_alias_lookup


def load_medicine_type_snapshot():
    alias_lookup, token_map = build_alias_lookup()

    return {
        "alias_lookup": alias_lookup,
        "token_map": token_map,
        "canonical_types": sorted(set(alias_lookup.values()))
    }
