import re

_NUM = re.compile(r"[0-9]+\Z")
_ID = re.compile(r"[0-9A-Za-z-]+\Z")


def _parse(s):
    if not isinstance(s, str):
        raise TypeError("version must be a string")
    s = s.strip()
    if s[:1] in ("v", "V"):
        s = s[1:]
    if "+" in s:
        s, build = s.split("+", 1)
        if not build:
            raise ValueError("empty build metadata")
    pre = None
    if "-" in s:
        s, pre = s.split("-", 1)
    parts = s.split(".")
    if not all(_NUM.match(p) for p in parts):
        raise ValueError("bad release part")
    rel = [int(p) for p in parts]
    while rel and rel[-1] == 0:
        rel.pop()
    ids = None
    if pre is not None:
        ids = pre.split(".")
        if not all(_ID.match(i) for i in ids):
            raise ValueError("bad prerelease")
    return rel, ids


def _key(i):
    return (0, int(i), "") if _NUM.match(i) else (1, 0, i)


def compare_versions(a, b):
    ra, pa = _parse(a)
    rb, pb = _parse(b)
    if ra != rb:
        return -1 if ra < rb else 1
    if pa is None or pb is None:
        return 0 if pa is pb else (1 if pa is None else -1)
    ka, kb = [_key(i) for i in pa], [_key(i) for i in pb]
    return 0 if ka == kb else (-1 if ka < kb else 1)
