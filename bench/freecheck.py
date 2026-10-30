# Free n-sample check (NVIDIA executor only): completion rate for churn, hidden tests for dedupe.
# Usage: python3 freecheck.py runs/<id> <n> <arms, e.g. BD> <scratch dir with a cache/ subdir>. Outputs stay local (NVIDIA terms).
import json, sys, re
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '.'); import run
rd, n, arms = sys.argv[1], int(sys.argv[2]), sys.argv[3]
llm = run.LLM(sys.argv[4], False)
cfg = json.load(open(f'{rd}/config.json'))
WORKING = re.compile(r"^(let me|i need to|we are going to|okay|first, let me|we need to)", re.I)
def one(job):
    task, arm, i = job
    p = json.load(open(f'{rd}/optimize/{task}_{arm}.json'))['final_prompt']
    t = llm.chat('nv', cfg['executor'], [{'role': 'user', 'content': p + run.attachment(task)}], f'free/{task}/{arm}/{i}', temperature=0.7)
    r = {'task': task, 'arm': arm, 'i': i, 'chars': len(t), 'working_leak': bool(WORKING.match(t.strip()))}
    if task == 'dedupe':
        r['passed'] = run.run_hidden_tests(t)['passed']
    return r
jobs = [(t, a, i) for t in ('dedupe', 'churn') for a in arms for i in range(n)]
with ThreadPoolExecutor(6) as ex:
    res = list(ex.map(one, jobs))
json.dump(res, open(f'{sys.argv[4]}/free_{arms}.json', 'w'), indent=1)
for t in ('dedupe', 'churn'):
    for a in arms:
        rs = [r for r in res if r['task'] == t and r['arm'] == a]
        leak = sum(r['working_leak'] for r in rs)
        extra = f", tests {sum(r['passed'] for r in rs)}/{20*len(rs)} = {sum(r['passed'] for r in rs)/(20*len(rs)):.0%}" if t == 'dedupe' else ''
        print(f"{t} {a}: finished answers {len(rs)-leak}/{len(rs)}{extra}")
