"""Reference solution for the hidden tests. Never shown to optimizers or the executor.
Exists only to prove the hidden suite is passable (100%) and to feed --dry-run."""

FIELDS = ("name", "email", "phone", "company")


def _email(v):
    v = (v or "").strip().lower()
    return v if "@" in v else ""


def _phone(v):
    d = "".join(c for c in str(v or "") if c.isdigit())
    if len(d) == 11 and d[0] == "1":
        d = d[1:]
    return d if len(d) >= 7 else ""


def dedupe_contacts(rows):
    parent = list(range(len(rows)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    seen = {}
    for i, r in enumerate(rows):
        for key in (("e", _email(r.get("email"))), ("p", _phone(r.get("phone")))):
            if key[1]:
                if key in seen:
                    a, b = find(seen[key]), find(i)
                    if a != b:
                        parent[max(a, b)] = min(a, b)
                else:
                    seen[key] = i

    groups = {}
    for i in range(len(rows)):
        groups.setdefault(find(i), []).append(i)

    out = []
    for root in sorted(groups):
        members = [rows[i] for i in groups[root]]
        ranked = sorted(members, key=lambda r: (sum(1 for f in FIELDS if str(r.get(f) or "").strip()),
                                                r.get("updated_at") or ""), reverse=True)
        merged = dict(ranked[0])
        for r in ranked[1:]:
            for k, v in r.items():
                if not str(merged.get(k) or "").strip() and str(v or "").strip():
                    merged[k] = v
        out.append(merged)
    return out
