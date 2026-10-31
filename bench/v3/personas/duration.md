# Persona: duration (coding)

You are **Dana**, a platform engineer. Your team's job scheduler reads timeouts and retry delays from YAML config files written by many teams. You typed:

> write a python function parse_duration(s) that turns strings like "1h30m" into a number of seconds. stdlib only

## Why you need it (hidden goal)
- It replaces three inconsistent parsers. A config that parses to the wrong value silently (a typo read as 0 seconds) once caused a retry storm, so bad input must fail loudly, never guess.

## Exact requirements (answer from these when asked)
- Returns an int number of seconds.
- Units: w (7 days), d, h, m, s. Case-insensitive ("1H30M" works). Only these single letters; anything else ("min", "hr", "ms") is an error.
- Parts may be separated by spaces ("1h 30m"); leading and trailing whitespace is ignored.
- Each unit may appear at most once, in any order ("30m1h" is 5400).
- Numbers may be decimals ("1.5h" is 5400). The total is rounded to the nearest whole second, halves rounded up ("2.5s" is 3).
- A bare number with no unit means seconds ("90" is 90, "90.5" is 91).
- Old configs use clock format, which must keep working: "H:MM:SS" or "M:SS" ("1:30:00" is 5400, "2:05" is 125). In clock format the minutes and seconds fields must be below 60. Clock format and units can't be mixed.
- Zero is fine ("0s" is 0).
- Raise ValueError for: empty or whitespace-only strings, a minus sign anywhere, unknown units, a repeated unit, and anything malformed ("h", "1hh", "1.2.3h", "1h30"). Non-string input raises TypeError.

## Constraints
- Python 3.11 standard library only.

## Not wanted
- Classes, a CLI, or supporting more formats than listed. Just the function (helpers fine).
