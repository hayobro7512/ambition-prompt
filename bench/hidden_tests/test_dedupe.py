"""Hidden test suite for task 1 (dedupe). Never shown to optimizers or the executor.

Each test is tagged with where its requirement comes from:
  [raw]     stated in the raw prompt
  [persona] only discoverable by asking the simulated user
  [expert]  a default a careful engineer applies unprompted
Runs under pytest, or under run.py's stdlib runner (plain asserts, no fixtures).
"""
import copy
import time

from solution import dedupe_contacts


def R(name=None, email=None, phone=None, company=None, updated_at=None):
    return {"name": name, "email": email, "phone": phone, "company": company, "updated_at": updated_at}


def norm_email(v):
    return (v or "").strip().lower()


def digits(v):
    d = "".join(c for c in str(v or "") if c.isdigit())
    return d[1:] if len(d) == 11 and d[0] == "1" else d


def emails(out):
    return sorted(norm_email(r.get("email")) for r in out)


# --- basics -----------------------------------------------------------------

def test_empty_list():  # [expert]
    assert list(dedupe_contacts([])) == []


def test_returns_list_of_dicts():  # [raw]
    out = dedupe_contacts([R("Ann Lee", "ann@x.com", "(415) 555-0100", "Acme", "2024-05-01")])
    assert isinstance(out, list) and len(out) == 1 and isinstance(out[0], dict)


def test_no_duplicates_kept():  # [raw]
    rows = [R("Ann Lee", "ann@x.com", "4155550100", "Acme", "2024-01-01"),
            R("Bob Ray", "bob@y.com", "2125550199", "Beta", "2024-01-01"),
            R("Cy Dee", "cy@z.com", "3125550142", "Gamma", "2024-01-01")]
    assert emails(dedupe_contacts(rows)) == ["ann@x.com", "bob@y.com", "cy@z.com"]


def test_exact_duplicate_removed():  # [raw]
    r = R("Ann Lee", "ann@x.com", "4155550100", "Acme", "2024-01-01")
    assert len(dedupe_contacts([dict(r), dict(r)])) == 1


# --- matching ---------------------------------------------------------------

def test_email_case_and_spaces():  # [raw]
    rows = [R("Ann Lee", "Ann@X.com", None, "Acme", "2024-01-01"),
            R("Ann Lee", "  ann@x.COM ", None, "Acme", "2024-01-01")]
    assert len(dedupe_contacts(rows)) == 1


def test_phone_formats():  # [raw]
    rows = [R("Ann Lee", None, "(415) 555-0100", None, "2024-01-01"),
            R("A. Lee", None, "415.555.0100", None, "2024-01-01"),
            R("Ann", None, "415 555 0100", None, "2024-01-01"),
            R("Bob Ray", None, "212 555 0199", None, "2024-01-01")]
    assert len(dedupe_contacts(rows)) == 2


def test_phone_us_country_code():  # [persona]
    rows = [R("Ann Lee", None, "+1 415 555 0100", None, "2024-01-01"),
            R("Ann Lee", None, "4155550100", None, "2024-01-01"),
            R("Ann Lee", None, "1-415-555-0100", None, "2024-01-01"),
            R("Bob Ray", None, "+1 212 555 0199", None, "2024-01-01")]
    assert len(dedupe_contacts(rows)) == 2


def test_blank_emails_do_not_match():  # [expert]
    rows = [R("Ann Lee", "", "4155550100", "Acme", "2024-01-01"),
            R("Bob Ray", None, "2125550199", "Beta", "2024-01-01"),
            R("Cy Dee", "   ", "3125550142", "Gamma", "2024-01-01")]
    assert len(dedupe_contacts(rows)) == 3


def test_junk_phones_do_not_match():  # [persona]
    rows = [R("Ann Lee", "ann@x.com", "n/a", None, "2024-01-01"),
            R("Bob Ray", "bob@y.com", "n/a", None, "2024-01-01"),
            R("Cy Dee", "cy@z.com", "0", None, "2024-01-01"),
            R("Di Eve", "di@w.com", "0", None, "2024-01-01")]
    assert len(dedupe_contacts(rows)) == 4


def test_same_name_different_people():  # [persona]
    rows = [R("John Smith", "john@acme.com", "4155550100", "Acme", "2024-01-01"),
            R("John Smith", "jsmith@beta.io", "6465550123", "Beta", "2024-01-01")]
    assert len(dedupe_contacts(rows)) == 2


def test_missing_keys_tolerated():  # [persona]
    rows = [{"name": "Ann Lee", "email": "ann@x.com"},
            {"name": "Ann Lee", "phone": "4155550100", "email": "ANN@x.com"},
            {"name": "Bob Ray", "phone": "2125550199"}]
    assert len(dedupe_contacts(rows)) == 2


def test_transitive_chain():  # [persona]
    rows = [R("Ann Lee", "ann@x.com", None, None, "2024-01-01"),
            R("Ann Lee", "ANN@x.com", "415-555-0100", None, "2024-01-01"),
            R("A Lee", None, "(415) 555 0100", "Acme", "2024-01-01")]
    out = dedupe_contacts(rows)
    assert len(out) == 1
    assert norm_email(out[0].get("email")) == "ann@x.com"
    assert digits(out[0].get("phone")) == "4155550100"
    assert out[0].get("company") == "Acme"


# --- merging ----------------------------------------------------------------

def test_most_complete_record_wins():  # [raw]
    full = R("Jonathan Smith", "jon@acme.com", "4155550100", "Acme", "2023-01-01")
    sparse = R("Jon S", "JON@acme.com", None, None, "2024-06-01")  # newer but less complete
    out = dedupe_contacts([sparse, full])
    assert len(out) == 1 and out[0]["name"] == "Jonathan Smith"


def test_fill_blanks_from_duplicates():  # [persona]
    a = R("Ann Lee", "ann@x.com", "4155550100", None, "2024-01-01")
    b = R(None, "ann@x.com", None, "Acme", "2024-01-01")
    out = dedupe_contacts([a, b])
    assert len(out) == 1
    assert out[0]["company"] == "Acme" and out[0]["name"] == "Ann Lee"
    assert digits(out[0]["phone"]) == "4155550100"


def test_tie_prefers_latest_updated_at():  # [persona]
    old = R("Ann Lee", "ann@x.com", "4155550100", "Acme", "2023-01-01")
    new = R("Ann Lee", "ann@x.com", "4155550100", "Acme Corp", "2024-06-01")
    for rows in ([old, new], [new, old]):
        out = dedupe_contacts(rows)
        assert len(out) == 1 and out[0]["company"] == "Acme Corp"


# --- output contract ----------------------------------------------------------

def test_first_appearance_order():  # [persona]
    rows = [R("Bob Ray", "bob@y.com", None, None, "2024-01-01"),
            R("Ann Lee", "ann@x.com", None, None, "2024-01-01"),
            R("Bob R", "BOB@y.com", "2125550199", None, "2024-01-01"),
            R("Cy Dee", "cy@z.com", None, None, "2024-01-01")]
    out = dedupe_contacts(rows)
    assert [norm_email(r["email"]) for r in out] == ["bob@y.com", "ann@x.com", "cy@z.com"]


def test_input_not_mutated():  # [persona]
    rows = [R("Ann Lee", "Ann@x.com", None, None, "2024-01-01"),
            R(None, "ann@x.com", "4155550100", "Acme", "2024-02-01"),
            R("Bob Ray", "bob@y.com", None, None, "2024-01-01")]
    before = copy.deepcopy(rows)
    dedupe_contacts(rows)
    assert rows == before


def test_no_extra_keys():  # [persona]
    rows = [R("Ann Lee", "ann@x.com", None, None, "2024-01-01"),
            R("Ann Lee", "ANN@x.com", "4155550100", "Acme", "2024-02-01")]
    allowed = {"name", "email", "phone", "company", "updated_at"}
    for r in dedupe_contacts(rows):
        assert set(r) <= allowed


def test_idempotent():  # [expert]
    rows = [R("Ann Lee", "ann@x.com", None, None, "2024-01-01"),
            R("A Lee", None, "4155550100", "Acme", "2024-01-01"),
            R("Ann", "ANN@x.com", "+1 (415) 555-0100", None, "2024-03-01"),
            R("Bob Ray", "bob@y.com", "2125550199", "Beta", "2024-01-01")]
    once = dedupe_contacts(rows)
    assert len(dedupe_contacts(once)) == len(once) == 2


def test_performance_20k_rows():  # [persona]
    rows = []
    for i in range(16000):
        rows.append(R(f"Person {i}", f"user{i}@example.com", f"(212) {i // 10000:03d}-{i % 10000:04d}",
                      f"Co {i % 500}", "2024-01-01"))
    for i in range(0, 16000, 4):  # 4000 duplicates in other formats
        rows.append(R(f"P {i}", f"  USER{i}@Example.com", None, None, "2024-02-01"))
    start = time.time()
    out = dedupe_contacts(rows)
    assert time.time() - start < 5.0
    assert len(out) == 16000
