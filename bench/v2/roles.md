# Role prompts (verbatim, used for every arm)

`{C}` = `runs/<id>/claude` (absolute path). `{t}` task, `{a}` arm, `{n}` round, `{i}` sample. Every role is a fresh Claude Code subagent (model `sonnet`) unless stated "continue", which means SendMessage to the same subagent.

## Optimizer (start)
```
You are the optimizer in an automated prompt-optimization benchmark. Read your system instructions from {C}/opt_{t}_{a}.system.md and follow them exactly, as if they were your system prompt. The user's first message (their raw prompt) is:

<user_message>
{raw prompt}
</user_message>

Transport rules: write your reply to the user (questions, or the final prompt between <final_prompt> and </final_prompt>) to the file {C}/opt_{t}_{a}.r{n}.md, overwriting it. Use tools only to read your instruction file, read the reply files I point you to, and write your outbox file. Don't read any other file, browse, or run code. When the file is written, reply to me with one word: QUESTIONS if it contains no final prompt, FINAL if it does.
```
## Optimizer (continue, round n)
```
The user's reply is in {C}/sim_{t}_{a}.r{n-1}.md. Read it and write your next reply to {C}/opt_{t}_{a}.r{n}.md. Same transport rules. Reply QUESTIONS or FINAL.
```
After round 3 still QUESTIONS (same text as run.py):
```
(harness) Question limit reached. Output the final prompt now inside <final_prompt> tags, written to {C}/opt_{t}_{a}.r4.md. Reply FINAL.
```
## Simulated user (start / continue)
```
Read your role and profile from {C}/sim_{t}_{a}.system.md and follow it exactly, as if it were your system prompt. The assistant's message to you is in {C}/opt_{t}_{a}.r{n}.md. Write your reply, in character, to {C}/sim_{t}_{a}.r{n}.md. Use tools only to read those two files and write your reply file. Then reply to me with one word: DONE.
```
Continue: `The assistant's next message is in {C}/opt_{t}_{a}.r{n}.md. Write your reply to {C}/sim_{t}_{a}.r{n}.md. Reply DONE.`

## Executor (fresh per sample)
```
You are acting as a plain chat model with no tools. Read the user's message from {C}/exec_{t}_{a}.prompt.md: it is the whole message a user sent you. Compose your complete reply to that message exactly as a chat model would, without running code, browsing or reading any other file. Your only other tool use is writing that reply, and nothing else, to {C}/exec_{t}_{a}_{i}.out.md. Then reply to me with one word: DONE.
```
The orchestrator copies the last optimizer outbox to `opt_{t}_{a}.final.md`, writes `opt_{t}_{a}.qa.json` from the round files, then runs `run.py --suite v2 --run runs/<id> --stage ingest`.
