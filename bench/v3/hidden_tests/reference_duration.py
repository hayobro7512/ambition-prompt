import re
from decimal import Decimal, ROUND_HALF_UP

UNITS = {"w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
NUM = r"\d+(?:\.\d+)?"


def parse_duration(s):
    if not isinstance(s, str):
        raise TypeError("duration must be a string")
    t = s.strip().lower()
    if not t or "-" in t:
        raise ValueError(f"bad duration: {s!r}")
    if ":" in t:
        m = re.fullmatch(r"(?:(\d+):)?(\d+):(\d\d)", t)
        if not m or int(m.group(2)) >= 60 or int(m.group(3)) >= 60:
            raise ValueError(f"bad clock duration: {s!r}")
        h, mi, se = int(m.group(1) or 0), int(m.group(2)), int(m.group(3))
        return h * 3600 + mi * 60 + se
    if re.fullmatch(NUM, t):
        return int(Decimal(t).quantize(Decimal(1), ROUND_HALF_UP))
    parts = re.findall(rf"({NUM})\s*([a-z]+)", t)
    if not parts or re.sub(rf"\s*{NUM}\s*[a-z]+\s*", "", t):
        raise ValueError(f"bad duration: {s!r}")
    total, seen = Decimal(0), set()
    for num, unit in parts:
        if unit not in UNITS or unit in seen:
            raise ValueError(f"bad unit in {s!r}")
        seen.add(unit)
        total += Decimal(num) * UNITS[unit]
    return int(total.quantize(Decimal(1), ROUND_HALF_UP))
