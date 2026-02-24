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
    def compute_rarity(units_produced: int) -> float:
    """
    Devuelve un % de rareza (0-100). Cuantas menos unidades, más raro.
    """
    if units_produced is None:
        return 50.0

    try:
        u = int(units_produced)
    except Exception:
        return 50.0

    if u <= 0:
        return 100.0

    # Escala simple: 1M o más => casi nada raro, 10k o menos => muy raro
    if u >= 1_000_000:
        return 5.0
    if u <= 10_000:
        return 95.0

    # Interpolación lineal entre 10k y 1M
    # 10k -> 95%, 1M -> 5%
    t = (u - 10_000) / (1_000_000 - 10_000)
    return round(95.0 + (5.0 - 95.0) * t, 2)