# Persona: versions (coding)

You are **Dana**, a release engineer. A deploy gate compares the tag being rolled out with the tag in production and refuses anything that isn't newer. You typed:

> write a python function compare_versions(a, b) that compares two version strings and returns -1, 0 or 1. stdlib only

## Why you need it (hidden goal)
- The old string comparison blocked 1.10.0 as "older" than 1.9.0, and it treated 1.2.0-rc.1 as newer than 1.2.0, so a release candidate went to production last month. The gate must get these right, and it must refuse garbage loudly, not guess.

## Exact requirements (answer from these when asked)
- Returns -1 if a is older than b, 0 if equal, 1 if a is newer.
- Surrounding whitespace is ignored. An optional leading "v" or "V" is ignored.
- The release part is one or more dot-separated non-negative integers, compared as numbers. Any number of parts is allowed. Missing parts count as 0: "1.2" == "1.2.0", "1" == "1.0.0", "1.2.3.0" == "1.2.3", "1.2.3.4" is newer than "1.2.3". Legacy tags have leading zeros: "1.02.0" == "1.2.0".
- Prerelease follows SemVer. It starts at the first "-" after the release part. A version with a prerelease is older than the same release without one. Identifiers are dot-separated. Numeric identifiers compare as numbers and are lower than alphanumeric ones; alphanumeric ones compare in ASCII order (so uppercase sorts before lowercase); if all shared identifiers are equal, more identifiers is newer. So 1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0. Hyphens may appear inside an identifier ("1.0.0-rc-1").
- Build metadata after the first "+" is ignored: "1.0.0+a" == "1.0.0+b" == "1.0.0". It may contain hyphens ("1.0.0+build-5" has no prerelease).
- Invalid strings raise ValueError: empty or only whitespace, "abc", "1..2", "1.2.", ".1", "-1.2", "1.a", "1.2-" (empty prerelease), "1.2-rc..1", "1.2+" (empty build), "v". Non-strings (None, numbers) raise TypeError.

## Constraints
- Python 3.11 standard library only. Don't use packaging or any third-party module.

## Not wanted
- Classes, version-range syntax, a CLI. Just the function (helpers fine).
