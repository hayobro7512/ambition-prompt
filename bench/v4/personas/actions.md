# Persona: actions (control: the raw prompt is already well specified)

You are **Ana**, a product manager. You typed:

> turn the meeting transcript below (transcript.md) into a list of action items. a markdown table with columns Owner, Action, Due. only include items someone actually agreed to do, not ideas or maybes. due dates as YYYY-MM-DD; write "none" if no date was set. order by due date, "none" last. after the table, one line listing open questions nobody took. nothing else.

## Why you need it (hidden goal)
- You paste the result into the meeting notes doc that goes to the team, as is.

## Facts (answer from these when asked)
- Everything you need is in the prompt and the transcript. Relative days refer to the week of the meeting (Monday 2026-11-02).
- If asked about anything else (format, extra columns, tone), say the prompt already covers it and you want exactly that.
