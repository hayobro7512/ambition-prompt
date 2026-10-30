#!/usr/bin/env python3
"""ambition-prompt benchmark harness. Python stdlib only.

  python3 run.py --dry-run                 # whole pipeline with mocked LLMs, no keys needed
  python3 run.py                           # all stages, real calls (needs NVIDIA_API_KEY, OPENAI_API_KEY)
  python3 run.py --stage optimize|execute|judge|report [--run runs/<id>] [--seed N] [--excerpts]

Every LLM response is cached as JSON under runs/<id>/cache/, so any stage can be re-run without
re-calling. OpenAI (primary judge) is hard-capped at OPENAI_CAP calls per run, retries included.
"""
import argparse, ast, hashlib, json, math, os, random, re, shutil, ssl, statistics, subprocess, sys, tempfile, time
import urllib.error, urllib.request
from datetime import datetime

BENCH = os.path.dirname(os.path.abspath(__file__))
TASKS = ["dedupe", "churn"]
ARMS = {"A": "raw prompt", "B": "prompt-master", "C": "OpenAI-guide", "D": "ambition-prompt"}
N_SAMPLES, MAX_ROUNDS, OPENAI_CAP = 3, 3, 40
NV_URL, OA_URL = "https://integrate.api.nvidia.com/v1", "https://api.openai.com/v1"
DEFAULT_MODELS = {  # NVIDIA free tier; from `nv.py --task chat --pick`, checked live against /v1/models on 2026-10-29
    "optimizer": "nvidia/nemotron-3-ultra-550b-a55b",
    "simuser": "deepseek-ai/deepseek-v4.1-flash",
    "executor": "nvidia/nemotron-3-super-120b-a12b",
    "judge_nv": "moonshotai/kimi-k2.6",  # different family from the executor (z-ai/glm-5.3 is end-of-life)
}
OA_PREFS = ["gpt-5.6-sol", "gpt-5.6", "gpt-5.6-terra", "gpt-5.5", "gpt-5.2", "gpt-5.1", "gpt-5", "o3", "gpt-4.1"]
CTX = ssl.create_default_context(cafile="/etc/ssl/cert.pem") if os.path.exists("/etc/ssl/cert.pem") else None
PM_DIR = os.path.join(BENCH, "optimizers", "prompt-master")


def read(*p):
    with open(os.path.join(BENCH, *p)) as f:
        return f.read()


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


def load(path):
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------- LLM client with cache + budget
class Budget(Exception):
    pass


class LLM:
    def __init__(self, run_dir, dry):
        self.run_dir, self.dry, self.last_nv = run_dir, dry, 0.0
        self.counter = os.path.join(run_dir, "openai_calls.json")

    def _oa_spend(self):
        n = load(self.counter)["count"] if os.path.exists(self.counter) else 0
        if n >= OPENAI_CAP:
            raise Budget(f"OpenAI cap of {OPENAI_CAP} calls reached")
        dump(self.counter, {"count": n + 1, "cap": OPENAI_CAP})

    def _http(self, provider, path, body=None):
        key = os.environ.get("NVIDIA_API_KEY" if provider == "nv" else "OPENAI_API_KEY", "")
        if not key:
            sys.exit(f"missing {'NVIDIA_API_KEY' if provider == 'nv' else 'OPENAI_API_KEY'}")
        url = (NV_URL if provider == "nv" else OA_URL) + path
        for attempt in range(5):
            if provider == "oa":
                self._oa_spend()  # every attempt counts toward the hard cap
            else:
                wait = 1.6 - (time.time() - self.last_nv)  # ~37 req/min, under the 40 RPM free tier
                if wait > 0:
                    time.sleep(wait)
                self.last_nv = time.time()
            req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                         headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
            try:
                return json.load(urllib.request.urlopen(req, timeout=600, context=CTX))
            except urllib.error.HTTPError as e:
                msg = e.read().decode()[:300]
                if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                    time.sleep(5 * 2 ** attempt)
                    continue
                raise RuntimeError(f"{provider} HTTP {e.code}: {msg}")
            except (urllib.error.URLError, TimeoutError) as e:
                if attempt < 4:
                    time.sleep(5 * 2 ** attempt)
                    continue
                raise RuntimeError(f"{provider} network error: {e}")

    def models(self, provider):
        path = os.path.join(self.run_dir, "cache", f"{provider}_models.json")
        if os.path.exists(path):
            return load(path)
        if self.dry:
            if provider == "oa":
                self._oa_spend()
            ids = ["gpt-5.6-sol", "gpt-5.6-luna", "gpt-4.1"]
        else:
            ids = sorted(m["id"] for m in self._http(provider, "/models")["data"])
        dump(path, ids)
        return ids

    def chat(self, provider, model, messages, tag, max_tokens=8000, temperature=None, json_mode=False):
        h = hashlib.sha256(json.dumps([provider, model, messages, max_tokens, temperature, json_mode, tag]).encode())
        path = os.path.join(self.run_dir, "cache", h.hexdigest()[:20] + ".json")
        if os.path.exists(path):
            return load(path)["content"]
        if self.dry:
            if provider == "oa":
                self._oa_spend()
            content = mock(tag, messages)
        else:
            body = {"model": model, "messages": messages}
            if provider == "oa":
                body["max_completion_tokens"] = 16000
                if json_mode:
                    body["response_format"] = {"type": "json_object"}
            else:
                body["max_tokens"] = max_tokens  # reasoning models need >= 2000 or content comes back null
                if temperature is not None:
                    body["temperature"] = temperature
            content = None
            for tokens in (max_tokens, max_tokens * 2):
                if provider == "nv":
                    body["max_tokens"] = tokens
                resp = self._http(provider, "/chat/completions", body)
                content = (resp["choices"][0]["message"].get("content") or "").strip()
                if content:
                    break
            content = strip_think(content or "")
        dump(path, {"provider": provider, "model": model, "tag": tag, "time": datetime.now().isoformat(),
                    "request": {"messages": messages, "max_tokens": max_tokens, "temperature": temperature},
                    "content": content})
        return content


def strip_think(s):
    s = re.sub(r"<think>.*?</think>", "", s, flags=re.S)
    return s.split("</think>")[-1].strip()


# ---------------------------------------------------------------- dry-run mocks
def mock(tag, messages):
    rng = random.Random(tag)
    kind = tag.split("/")[0]
    if kind == "opt":
        _, task, arm = tag.split("/")[:3]
        asked = sum(m["role"] == "assistant" for m in messages)
        if asked < {"B": 1, "C": 0, "D": 9}[arm] and "Question limit reached" not in messages[-1]["content"]:
            return f"❓ **Q{asked + 1}** - **Mock**: what matters most here?\n\n➡️ correctness"
        return f"Here it is.\n<final_prompt>\nMOCK {arm} prompt for {task}. Round {asked}.\n</final_prompt>"
    if kind == "user":
        return "mock answer: correctness matters most; use your recommendation."
    if kind == "exec":
        if tag.split("/")[1] == "dedupe":
            code = read("hidden_tests", "reference_solution.py") if rng.random() < 0.6 else (
                "def dedupe_contacts(rows):\n    seen, out = set(), []\n    for r in rows:\n"
                "        k = (r.get('email') or '').lower()\n        if k not in seen:\n"
                "            seen.add(k); out.append(r)\n    return out\n")
            return f"Here is the function.\n```python\n{code}```\n"
        return "Mock memo. " * rng.randint(50, 400)
    if kind == "judge":
        text = messages[-1]["content"]
        if "/pair/" in tag:
            return json.dumps({"winner": rng.choice("XY") if rng.random() < 0.9 else "tie", "reason": "mock"})
        crit = ["P%d" % i for i in range(1, 9)] if "/prompt/" in tag else ["O%d" % i for i in range(1, 7)]
        out = {}
        for item in sorted(set(re.findall(r'<item id="(item_\d+)">', text))):
            out[item] = {c: rng.randint(0, 3) for c in crit}
            out[item].update({"infeasible_requirements": [] if rng.random() < 0.7 else ["mock: run the tests"],
                              "note": "mock"})
        return json.dumps(out)
    raise ValueError(tag)


# ---------------------------------------------------------------- tasks and arms
def attachment(task):
    return "" if task == "dedupe" else "\n\n--- customers.csv ---\n" + read("tasks", "churn", "customers.csv")


def harness_note(task):
    if task == "dedupe":
        att = "There is no attachment."
    else:
        lines = read("tasks", "churn", "customers.csv").splitlines()
        att = (f"The user's file customers.csv ({len(lines) - 1} data rows) is appended verbatim after your prompt "
               "when it is sent. Its first lines are:\n" + "\n".join(lines[:6]))
    return f"""

---
## Benchmark harness (identical for every optimizer)
You are running inside an automated benchmark through a plain chat API. You have no tools in this session: you cannot read files, browse or run code. The facts you would normally look up are these:
- The user's raw prompt is their first message.
- Target tool for the prompt you write: a general-purpose LLM chat model, called once, single-shot, with no tools, no file access, no code execution, no browsing and no chance to ask follow-up questions. Its reply is the final deliverable the user receives.
- {att}
- You may ask the user clarifying questions. Any message of yours without a final prompt goes to the user, who replies. At most {MAX_ROUNDS} rounds of questions are allowed.
- When done, put the complete final prompt, exactly as it should be sent to the target model, between <final_prompt> and </final_prompt>. Only the text inside the tags is sent. Your job ends there: there is no review or run step after it.
"""


def arm_system(arm):
    if arm == "B":
        pm = os.path.join(PM_DIR, "references")
        return (read("optimizers", "prompt-master", "SKILL.md")
                + "".join(f"\n\n# references/{f}\n\n" + open(os.path.join(pm, f)).read() for f in sorted(os.listdir(pm))))
    if arm == "C":
        return re.sub(r"<!--.*?-->\s*", "", read("optimizers", "openai_guide.md"), flags=re.S)
    if arm == "D":
        return read("..", "skills", "ambition-prompt", "SKILL.md")
    raise ValueError(arm)


SIMUSER_RULES = """You are role-playing the user described in the profile below, chatting with an assistant that is helping you turn your rough request into a better prompt. Rules:
- Reply the way this user types: short, plain, informal.
- Answer only what the assistant asked, using the facts in your profile. Do not volunteer facts it did not ask about.
- If it asks about something your profile does not cover, say you don't know or that it should use its judgment.
- If it offers a recommended answer, accept it unless it conflicts with your profile; if it conflicts, say what is actually true.
- If it asks you to approve or confirm a prompt or summary, approve it unless it contradicts your profile; then name the contradiction in one line.
- Never write the prompt yourself and never mention role-play.

Your profile:

"""


def extract_final(text):
    m = re.search(r"<final_prompt>(.*?)(</final_prompt>|$)", text, re.S)
    if m:
        return m.group(1).strip(), "tags"
    blocks = re.findall(r"```[^\n]*\n(.*?)```", text, re.S)
    if blocks:
        return max(blocks, key=len).strip(), "largest_code_block"
    return text.strip(), "whole_reply"


INFEASIBLE_RX = [  # keyword screen for demands a no-tool, single-shot executor cannot meet; judges also list them
    r"\b(run|execute)\b[^.\n]{0,40}\b(tests?|code|script|suite|benchmark|pytest|query)",
    r"\b(benchmark|profile|time it|measure (the )?(runtime|time))\b",
    r"\b(browse|search the web|web search|look up online|google it)\b",
    r"\bsub-?agents?\b", r"\b(git commit|commit to git|save (it )?to (a )?file|write to disk|progress\.md|tests\.json)\b",
    r"\bask (the user|me|clarifying)\b", r"\b(query|connect to)\b[^.\n]{0,30}\b(database|stripe|api|warehouse)\b",
]


def infeasible_hits(prompt):
    return sorted({m.group(0) for rx in INFEASIBLE_RX for m in re.finditer(rx, prompt, re.I)})


# ---------------------------------------------------------------- stages
def stage_optimize(llm, cfg):
    for task in TASKS:
        raw = read("tasks", task, "prompt.txt").strip()
        dump(os.path.join(llm.run_dir, "optimize", f"{task}_A.json"),
             {"task": task, "arm": "A", "final_prompt": raw, "qa": [], "rounds": 0, "extraction": "raw"})
        persona = read("personas", f"{task}.md")
        for arm in "BCD":
            out = os.path.join(llm.run_dir, "optimize", f"{task}_{arm}.json")
            if os.path.exists(out):
                continue
            system = arm_system(arm) + harness_note(task)
            msgs, qa, forced = [{"role": "user", "content": raw}], [], False
            for rnd in range(MAX_ROUNDS + 1):
                reply = llm.chat("nv", cfg["optimizer"], [{"role": "system", "content": system}] + msgs,
                                 f"opt/{task}/{arm}/{rnd}", temperature=0.2)
                if "<final_prompt>" in reply:
                    break
                msgs.append({"role": "assistant", "content": reply})
                if rnd == MAX_ROUNDS:
                    forced = True
                    msgs.append({"role": "user", "content": "(harness) Question limit reached. Output the final "
                                                            "prompt now inside <final_prompt> tags."})
                    reply = llm.chat("nv", cfg["optimizer"], [{"role": "system", "content": system}] + msgs,
                                     f"opt/{task}/{arm}/forced", temperature=0.2)
                    break
                flipped = [{"role": "user" if m["role"] == "assistant" else "assistant", "content": m["content"]}
                           for m in msgs[1:]]
                answer = llm.chat("nv", cfg["simuser"], [{"role": "system", "content": SIMUSER_RULES + persona}]
                                  + flipped, f"user/{task}/{arm}/{rnd}", max_tokens=2500, temperature=0.2)
                qa.append({"round": rnd + 1, "question": reply, "answer": answer})
                msgs.append({"role": "user", "content": answer})
            msgs.append({"role": "assistant", "content": reply})
            final, how = extract_final(reply)
            dump(out, {"task": task, "arm": arm, "final_prompt": final, "extraction": how, "forced_final": forced,
                       "rounds": len(qa), "qa": qa, "transcript": msgs,
                       "system_sha256": hashlib.sha256(system.encode()).hexdigest()})
            print(f"optimize {task}/{arm}: {len(qa)} rounds, {len(final)} chars ({how})")


def extract_code(text):
    blocks = re.findall(r"```(?:python|py)?[ \t]*\n(.*?)```", text, re.S)
    with_def = [b for b in blocks if "def dedupe_contacts" in b]
    if with_def:
        return with_def[-1]
    return "\n\n".join(blocks) if blocks else text


def run_hidden_tests(output):
    """Each test runs in its own subprocess (30s timeout) in a throwaway dir. The code is LLM-written: see README."""
    tests_src = read("hidden_tests", "test_dedupe.py")
    names = [n.name for n in ast.parse(tests_src).body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
    tmp = tempfile.mkdtemp(prefix="bench_")
    try:
        with open(os.path.join(tmp, "solution.py"), "w") as f:
            f.write(extract_code(output))
        with open(os.path.join(tmp, "test_dedupe.py"), "w") as f:
            f.write(tests_src)
        failed = []
        for n in names:
            try:
                r = subprocess.run([sys.executable, "-I", "-c", f"import sys; sys.path.insert(0, '.'); "
                                    f"import test_dedupe as t; t.{n}()"], cwd=tmp, capture_output=True, timeout=30)
                ok = r.returncode == 0
            except subprocess.TimeoutExpired:
                ok = False
            if not ok:
                failed.append(n)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return {"passed": len(names) - len(failed), "total": len(names), "failed": failed}


def stage_execute(llm, cfg):
    for task in TASKS:
        for arm in ARMS:
            prompt = load(os.path.join(llm.run_dir, "optimize", f"{task}_{arm}.json"))["final_prompt"]
            for i in range(N_SAMPLES):
                out = os.path.join(llm.run_dir, "execute", f"{task}_{arm}_{i}.json")
                if os.path.exists(out):
                    continue
                text = llm.chat("nv", cfg["executor"], [{"role": "user", "content": prompt + attachment(task)}],
                                f"exec/{task}/{arm}/{i}", temperature=0.7)
                rec = {"task": task, "arm": arm, "sample": i, "output": text, "chars": len(text),
                       "words": len(text.split())}
                if task == "dedupe":
                    rec["tests"] = run_hidden_tests(text)
                dump(out, rec)
                print(f"execute {task}/{arm}/{i}: {len(text)} chars"
                      + (f", tests {rec['tests']['passed']}/{rec['tests']['total']}" if task == "dedupe" else ""))


def rubric_section(name):
    text = read("RUBRIC.md")
    sec = {m.group(1): m.start() for m in re.finditer(r"^## (.+)$", text, re.M)}
    keys = list(sec)

    def body(k):
        i = keys.index(k)
        return text[sec[k]: sec[keys[i + 1]] if i + 1 < len(keys) else len(text)]
    return body("Judge instructions") + "\n" + body(name)


def parse_json(text):
    try:
        return json.loads(text[text.index("{"): text.rindex("}") + 1])
    except ValueError:
        return None


def judge_context(task):
    ctx = (f"## Raw user prompt\n{read('tasks', task, 'prompt.txt').strip()}\n\n"
           f"## Persona (the user's real situation; the methods did not all see it)\n{read('personas', task + '.md')}\n")
    if task == "churn":
        ctx += "\n## Answer key (judge only)\n" + read("tasks", "churn", "truth.md") + "\n"
    return ctx


def ask_judge(llm, cfg, which, system, user, tag):
    provider, model = ("oa", cfg["judge_oa"]) if which == "oa" else ("nv", cfg["judge_nv"])
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    for attempt in range(2):
        t = tag if attempt == 0 else tag + "/retry"
        try:
            got = parse_json(llm.chat(provider, model, msgs, t, max_tokens=8000, temperature=0.0, json_mode=True))
        except Budget as e:
            print(f"  {tag}: {e}")
            return None
        if got is not None:
            return got
    return None


def stage_judge(llm, cfg, seed):
    if not cfg.get("judge_oa"):
        ids = llm.models("oa")
        cfg["judge_oa"] = next((m for m in OA_PREFS if m in ids), None) or sorted(
            m for m in ids if m.startswith("gpt-") and not re.search("mini|nano|audio|realtime|search|image|tts", m))[-1]
        dump(os.path.join(llm.run_dir, "config.json"), cfg)
    rng = random.Random(seed)
    rd = llm.run_dir
    res = {"prompt": [], "output": [], "pair": []}
    sys_p = "You are an impartial expert evaluator. Respond with JSON only.\n\n" + rubric_section("Prompt rubric")
    sys_o = "You are an impartial expert evaluator. Respond with JSON only.\n\n" + rubric_section("Output rubric")
    sys_x = "You are an impartial expert evaluator. Respond with JSON only.\n\n" + rubric_section("Output rubric") \
        + "\n" + rubric_section("Pairwise comparison").split("## Pairwise comparison", 1)[1]

    def items_block(order, texts):
        return "\n".join(f'<item id="item_{k + 1}">\n{texts[a]}\n</item>' for k, a in enumerate(order))

    for task in TASKS:
        ctx = judge_context(task)
        prompts = {a: load(os.path.join(rd, "optimize", f"{task}_{a}.json"))["final_prompt"] for a in ARMS}
        order = rng.sample(list(ARMS), 4)
        schema = ('{"item_1": {"P1": 0-3, ..., "P8": 0-3, "infeasible_requirements": ["requirements a no-tool '
                  'single-shot executor cannot meet"], "note": "one sentence"}, ...}')
        user = f"{ctx}\n## Prompts to score\n{items_block(order, prompts)}\n\nReturn JSON: {schema}"
        for j in ("oa", "nv"):
            got = ask_judge(llm, cfg, j, sys_p, user, f"judge/prompt/{task}/{j}")
            for k, a in enumerate(order):
                res["prompt"].append({"task": task, "arm": a, "judge": j, "scores": (got or {}).get(f"item_{k + 1}")})
        outs = {(a, i): load(os.path.join(rd, "execute", f"{task}_{a}_{i}.json"))["output"]
                for a in ARMS for i in range(N_SAMPLES)}
        for i in range(N_SAMPLES):
            order = rng.sample(list(ARMS), 4)
            texts = {a: outs[(a, i)] for a in ARMS}
            schema = '{"item_1": {"O1": 0-3, ..., "O6": 0-3, "note": "one sentence"}, ...}'
            user = f"{ctx}\n## Outputs to score\n{items_block(order, texts)}\n\nReturn JSON: {schema}"
            for j in ("oa", "nv"):
                got = ask_judge(llm, cfg, j, sys_o, user, f"judge/output/{task}/{i}/{j}")
                for k, a in enumerate(order):
                    res["output"].append({"task": task, "arm": a, "sample": i, "judge": j,
                                          "scores": (got or {}).get(f"item_{k + 1}")})
            for other in "BC":
                for d_first in (True, False):
                    x, y = ("D", other) if d_first else (other, "D")
                    user = (f"{ctx}\n## Output X\n{outs[(x, i)]}\n\n## Output Y\n{outs[(y, i)]}\n\n"
                            'Return JSON: {"winner": "X" | "Y" | "tie", "reason": "one sentence"}')
                    for j in ("oa", "nv"):
                        got = ask_judge(llm, cfg, j, sys_x, user, f"judge/pair/{task}/{i}/D{other}/{int(d_first)}/{j}")
                        w = (got or {}).get("winner")
                        res["pair"].append({"task": task, "sample": i, "other": other, "d_first": d_first, "judge": j,
                                            "winner": {"X": x, "Y": y, "tie": "tie"}.get(w)})
    dump(os.path.join(rd, "judge", "results.json"), res)
    print(f"judge: done; OpenAI calls used: {load(llm.counter)['count'] if os.path.exists(llm.counter) else 0}")


# ---------------------------------------------------------------- report
def mean_score(s, prefix, n):
    if not isinstance(s, dict):
        return None
    vals = [s.get(f"{prefix}{k}") for k in range(1, n + 1)]
    vals = [min(3, max(0, int(v))) for v in vals if isinstance(v, (int, float))]
    return sum(vals) / len(vals) if len(vals) == n else None


def msd(xs, fmt="{:.2f}"):
    xs = [x for x in xs if x is not None]
    if not xs:
        return "n/a"
    sd = statistics.stdev(xs) if len(xs) > 1 else 0.0
    return (fmt + " ± " + fmt.replace("+", "")).format(statistics.mean(xs), sd)


def corr(a, b):
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    try:
        return f"{statistics.correlation([p[0] for p in pairs], [p[1] for p in pairs]):.2f} (n={len(pairs)})"
    except (statistics.StatisticsError, ValueError):
        return "n/a"


def stage_report(llm, cfg, excerpts):
    rd = llm.run_dir
    res = load(os.path.join(rd, "judge", "results.json"))
    opt = {(t, a): load(os.path.join(rd, "optimize", f"{t}_{a}.json")) for t in TASKS for a in ARMS}
    exe = {(t, a, i): load(os.path.join(rd, "execute", f"{t}_{a}_{i}.json"))
           for t in TASKS for a in ARMS for i in range(N_SAMPLES)}
    P = {(r["task"], r["arm"], r["judge"]): mean_score(r["scores"], "P", 8) for r in res["prompt"]}
    O = {(r["task"], r["arm"], r["sample"], r["judge"]): mean_score(r["scores"], "O", 6) for r in res["output"]}
    oa_calls = load(llm.counter)["count"] if os.path.exists(llm.counter) else 0

    # length-controlled: residual of output score after OLS on log(chars), fit per task and judge over all outputs
    resid = {}
    for t in TASKS:
        for j in ("oa", "nv"):
            pts = [(math.log(max(1, exe[(t, a, i)]["chars"])), O.get((t, a, i, j)), a, i)
                   for a in ARMS for i in range(N_SAMPLES)]
            pts = [p for p in pts if p[1] is not None]
            try:
                slope, icpt = statistics.linear_regression([p[0] for p in pts], [p[1] for p in pts])
            except (statistics.StatisticsError, ValueError):
                slope, icpt = 0.0, statistics.mean([p[1] for p in pts]) if pts else 0.0
            for x, y, a, i in pts:
                resid[(t, a, i, j)] = y - (slope * x + icpt)

    L = [f"# Results — run `{os.path.basename(rd)}`{' (DRY RUN: mocked LLMs, numbers are meaningless)' if llm.dry else ''}",
         "", "Aggregate numbers computed by `run.py report`. No model-generated text is reproduced here "
         "(NVIDIA trial terms); run `python3 run.py --stage report --excerpts` locally to see prompts and outputs.", "",
         f"Models: optimizer `{cfg['optimizer']}`, simulated user `{cfg['simuser']}`, executor `{cfg['executor']}`, "
         f"judge 1 (primary) `{cfg.get('judge_oa')}`, judge 2 `{cfg['judge_nv']}`. Seed {cfg['seed']}. "
         f"n={N_SAMPLES} executor samples per arm per task. OpenAI calls used: {oa_calls}/{OPENAI_CAP}.", "",
         "Headline metrics are the hidden-test pass rate (task 1) and output quality (both tasks). "
         "The prompt score partly rewards what ambition-prompt asks for; treat it as secondary.", ""]
    for t in TASKS:
        L += [f"## Task: {t}", "",
              "| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) |"
              + (" Hidden tests pass rate |" if t == "dedupe" else "")
              + " Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |",
              "|---|---|---|---|" + ("---|" if t == "dedupe" else "") + "---|---|---|---|"]
        for a in ARMS:
            row = [f"{a} {ARMS[a]}",
                   msd([O.get((t, a, i, "oa")) for i in range(N_SAMPLES)]),
                   msd([O.get((t, a, i, "nv")) for i in range(N_SAMPLES)]),
                   msd([resid.get((t, a, i, "oa")) for i in range(N_SAMPLES)], "{:+.2f}") + " / "
                   + msd([resid.get((t, a, i, "nv")) for i in range(N_SAMPLES)], "{:+.2f}")]
            if t == "dedupe":
                row.append(msd([100 * exe[(t, a, i)]["tests"]["passed"] / exe[(t, a, i)]["tests"]["total"]
                                for i in range(N_SAMPLES)], "{:.0f}%"))
            p_oa, p_nv = P.get((t, a, "oa")), P.get((t, a, "nv"))
            row += [msd([exe[(t, a, i)]["chars"] for i in range(N_SAMPLES)], "{:.0f}"),
                    f"{p_oa if p_oa is None else round(p_oa, 2)} / {p_nv if p_nv is None else round(p_nv, 2)}",
                    str(len(opt[(t, a)]["final_prompt"])), str(opt[(t, a)]["rounds"])]
            L.append("| " + " | ".join(row) + " |")
        L.append("")
        if t == "dedupe":
            fails = {}
            for a in ARMS:
                for i in range(N_SAMPLES):
                    for n in exe[(t, a, i)]["tests"]["failed"]:
                        fails.setdefault(n, {}).setdefault(a, 0)
                        fails[n][a] += 1
            L += ["Hidden-test failures (count of samples failing, per arm):", "",
                  "| Test | " + " | ".join(ARMS) + " |", "|---|" + "---|" * len(ARMS)]
            for n in sorted(fails):
                L.append(f"| {n} | " + " | ".join(str(fails[n].get(a, 0)) for a in ARMS) + " |")
            L.append("")

    L += ["## Prompt rubric by criterion (mean over tasks and both judges, 0–3)", "",
          "| Arm | " + " | ".join(f"P{k}" for k in range(1, 9)) + " | Infeasible-demand flags (judge-listed / keyword hits) |",
          "|---|" + "---|" * 9]
    for a in ARMS:
        cells = []
        for k in range(1, 9):
            v = [r["scores"].get(f"P{k}") for r in res["prompt"] if r["arm"] == a and isinstance(r["scores"], dict)]
            v = [x for x in v if isinstance(x, (int, float))]
            cells.append(f"{statistics.mean(v):.2f}" if v else "n/a")
        jl = sum(len(r["scores"].get("infeasible_requirements") or []) for r in res["prompt"]
                 if r["arm"] == a and isinstance(r["scores"], dict))
        kw = sum(len(infeasible_hits(opt[(t, a)]["final_prompt"])) for t in TASKS)
        L.append(f"| {a} {ARMS[a]} | " + " | ".join(cells) + f" | {jl} / {kw} |")
    L += ["", "P1 altitude, P2 depth, P3 range, P4 done criteria + outside judge, P5 limits/stop rules, P6 output spec, "
          "P7 consistency, P8 concision.", ""]

    L += ["## Pairwise (D vs competitor, both orderings, per executor sample)", "",
          "D win rate = (D wins + 0.5 × ties) / comparisons. Position-consistent = same winner in both orderings.", "",
          "| Task | Pair | Judge | D wins | Ties | D losses | D win rate | Position-consistent |", "|---|---|---|---|---|---|---|---|"]
    for t in TASKS + ["all"]:
        for other in "BC":
            for j in ("oa", "nv"):
                rows = [r for r in res["pair"] if (t == "all" or r["task"] == t) and r["other"] == other
                        and r["judge"] == j and r["winner"]]
                w = sum(r["winner"] == "D" for r in rows)
                ti = sum(r["winner"] == "tie" for r in rows)
                lo = len(rows) - w - ti
                by = {}
                for r in rows:
                    by.setdefault((r["task"], r["sample"]), []).append(r["winner"])
                cons = sum(len(v) == 2 and v[0] == v[1] for v in by.values())
                rate = f"{(w + 0.5 * ti) / len(rows):.2f}" if rows else "n/a"
                L.append(f"| {t} | D vs {other} | {'OpenAI' if j == 'oa' else 'NVIDIA'} | {w} | {ti} | {lo} | {rate} | "
                         f"{cons}/{len(by)} |")
    L.append("")

    keys_o = [(t, a, i) for t in TASKS for a in ARMS for i in range(N_SAMPLES)]
    keys_p = [(t, a) for t in TASKS for a in ARMS]
    pa = {}
    for r in res["pair"]:
        pa.setdefault((r["task"], r["sample"], r["other"], r["d_first"]), {})[r["judge"]] = r["winner"]
    both = [v for v in pa.values() if v.get("oa") and v.get("nv")]
    mae = [abs(O[(*k, "oa")] - O[(*k, "nv")]) for k in keys_o if O.get((*k, "oa")) is not None and O.get((*k, "nv")) is not None]
    L += ["## Judge agreement (OpenAI vs NVIDIA)", "",
          f"- Output scores: Pearson r = {corr([O.get((*k, 'oa')) for k in keys_o], [O.get((*k, 'nv')) for k in keys_o])}; "
          f"mean absolute difference = {statistics.mean(mae):.2f}" if mae else "- Output scores: n/a",
          f"- Prompt scores: Pearson r = {corr([P.get((*k, 'oa')) for k in keys_p], [P.get((*k, 'nv')) for k in keys_p])}",
          f"- Pairwise winners: {sum(v['oa'] == v['nv'] for v in both)}/{len(both)} comparisons agree", "",
          "## Length vs score", "",
          f"- Pearson r between output chars and output score: OpenAI "
          f"{corr([exe[k]['chars'] for k in keys_o], [O.get((*k, 'oa')) for k in keys_o])}, NVIDIA "
          f"{corr([exe[k]['chars'] for k in keys_o], [O.get((*k, 'nv')) for k in keys_o])}", ""]

    L += ["## Verdict on headline metrics (D vs B and C; n=3, no significance test)", ""]
    for t in TASKS:
        for other in "BC":
            def avg(f):
                v = [f(i) for i in range(N_SAMPLES)]
                v = [x for x in v if x is not None]
                return statistics.mean(v) if v else None
            parts = []
            if t == "dedupe":
                pr = {a: avg(lambda i, a=a: exe[(t, a, i)]["tests"]["passed"] / exe[(t, a, i)]["tests"]["total"])
                      for a in ("D", other)}
                parts.append(f"tests {100 * pr['D']:.0f}% vs {100 * pr[other]:.0f}%")
            for j in ("oa", "nv"):
                d, o = avg(lambda i: O.get((t, "D", i, j))), avg(lambda i, a=other: O.get((t, a, i, j)))
                parts.append(f"output ({'OpenAI' if j == 'oa' else 'NVIDIA'}) "
                             + (f"{d:.2f} vs {o:.2f}" if d is not None and o is not None else "n/a"))
            L.append(f"- {t}, D vs {other}: " + "; ".join(parts))
    L += ["", "## Raw prompts (hand-written, verbatim)", ""]
    for t in TASKS:
        L += [f"**{t}:**", "", "```", read("tasks", t, "prompt.txt").strip(), "```", ""]

    text = "\n".join(L)
    with open(os.path.join(rd, "RESULTS.md"), "w") as f:
        f.write(text)
    if not llm.dry:
        shutil.copy(os.path.join(rd, "RESULTS.md"), os.path.join(BENCH, "RESULTS.md"))
    print(text)

    if excerpts:  # local only, never written to the repo
        for t in TASKS:
            print(f"\n{'=' * 30} {t}: final prompts {'=' * 30}")
            for a in ARMS:
                o = opt[(t, a)]
                print(f"\n--- {a} {ARMS[a]} ({len(o['final_prompt'])} chars, {o['rounds']} rounds, "
                      f"keyword flags: {infeasible_hits(o['final_prompt'])}) ---\n{o['final_prompt'][:1500]}")
                for q in o.get("qa", []):
                    print(f"\n  [Q round {q['round']}] {q['question'][:800]}\n  [A] {q['answer'][:400]}")
            for r in res["prompt"]:
                if r["task"] == t and isinstance(r["scores"], dict) and r["scores"].get("infeasible_requirements"):
                    print(f"\n  judge {r['judge']} flags {r['arm']}: {r['scores']['infeasible_requirements']}")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", choices=["all", "optimize", "execute", "judge", "report"], default="all")
    ap.add_argument("--dry-run", action="store_true", help="mock every LLM call; no keys needed")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--run", help="run directory (default: new for optimize/all, latest otherwise)")
    ap.add_argument("--excerpts", action="store_true", help="print prompt/output excerpts locally (report stage)")
    for k, v in DEFAULT_MODELS.items():
        ap.add_argument(f"--{k.replace('_', '-')}", default=v, help=f"model id (default {v})")
    a = ap.parse_args()

    runs = os.path.join(BENCH, "runs")
    if a.run:
        rd = os.path.abspath(a.run)
    elif a.stage in ("all", "optimize"):
        rd = os.path.join(runs, datetime.now().strftime("%Y%m%d-%H%M%S") + ("-dry" if a.dry_run else ""))
    else:
        cands = sorted(d for d in os.listdir(runs) if a.dry_run == d.endswith("-dry"))
        rd = os.path.join(runs, cands[-1])
    os.makedirs(rd, exist_ok=True)
    cfg_path = os.path.join(rd, "config.json")
    if os.path.exists(cfg_path):
        cfg = load(cfg_path)  # a run keeps the models and seed it started with
    else:
        cfg = {k: getattr(a, k) for k in DEFAULT_MODELS} | {"seed": a.seed, "dry_run": a.dry_run,
                                                             "started": datetime.now().isoformat()}
        dump(cfg_path, cfg)
    llm = LLM(rd, a.dry_run or cfg.get("dry_run", False))
    print(f"run dir: {rd}")
    if not llm.dry and a.stage != "report":  # fail fast on retired model ids (NVIDIA retires them often)
        live = set(llm.models("nv"))
        gone = [cfg[k] for k in DEFAULT_MODELS if cfg[k] not in live]
        if gone:
            sys.exit(f"not served by NVIDIA anymore: {gone}; pick others with nv.py --task chat --pick")
    stages = ["optimize", "execute", "judge", "report"] if a.stage == "all" else [a.stage]
    for s in stages:
        if s == "optimize":
            stage_optimize(llm, cfg)
        elif s == "execute":
            stage_execute(llm, cfg)
        elif s == "judge":
            stage_judge(llm, cfg, cfg["seed"])
        else:
            stage_report(llm, cfg, a.excerpts)


if __name__ == "__main__":
    main()
