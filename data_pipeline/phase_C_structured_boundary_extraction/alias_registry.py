# ======================================================
# MEDICINE TYPE ALIAS REGISTRY
# ======================================================
# Canonical → spoken / abbreviated aliases
# ======================================================

MED_TYPE_ALIAS_MAP = {
    "TABLET": {"TAB", "TABS", "TABLET", "TABLETS"},
    "CAPSULE": {"CAP", "CAPS", "CAPSULE", "CAPSULES"},
    "CREAM": {"CREAM", "CREAMS"},
    "OINTMENT": {"OINT", "OINTMENT", "OINTMENTS"},
    "GEL": {"GEL", "GELS"},
    "SUSPENSION": {"SUSPENSION"},
    "ORAL SOLUTION LIQUID": {"SOLUTION", "ORAL", "LIQUID", "ORAL SOLUTION LIQUID"},
    "SYRUP": {"SYRUP", "SYP", "ORAL SOLUTION", "DRY SYRUP"},
    "SOAP": {"SOAP"},
    "EYE DROPS": {"IDROPS", "I DROPS", "EYE DROPS", "DROP", "IDROP", "EYE DROP"},
    "NASAL SPRAY": {"SPRAY", "NASAL", "NASAL SPRAY", "NASALSPRAY"},
    "SHAMPOO": {"SHAMPOO"},
    "LOTION": {"LOTION"},
    "PROBIOTIC LIQUID": {"PROBIOTIC", "PRO BIOTIC"},
    "INJECTION": {"INJECTION", "INJ"},
    "DRY SYRUP": {"DRY SYRUP", "DRY"},
    "ANTIBIOTIC_DROPS": {"ANTI", "BIOTIC", "ANTI BIOTIC", "ANTIBIOTIC", 
                         "ANTI BIOTICS", "ANTIBIOTICS", "BIOTICS",},
    "SACHETS":{"SACHET", "SACHETS", "SOCHETS", "SEARCHEST"}
}


def build_alias_lookup():
    alias_lookup = {}
    token_map = {}

    for canon, aliases in MED_TYPE_ALIAS_MAP.items():
        for a in aliases:
            alias_lookup[a] = canon
            token_map[a] = a.split()

    return alias_lookup, token_map
