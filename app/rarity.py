import math

MAX_UNITS = 40_000_000
EXPONENT = 2.0

def rarity_from_units(units_produced: int) -> float:
    if units_produced <= 0:
        return 100.0

    ratio = math.log10(units_produced) / math.log10(MAX_UNITS)
    rarity = 100.0 - ((ratio ** EXPONENT) * 100.0)

    rarity = max(0.0, min(100.0, rarity))
    return round(rarity, 2)