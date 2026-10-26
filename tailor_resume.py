#!/usr/bin/env python3
"""Resume Tailor: Claude tailors my resume to a job posting; plain code
makes sure it never invents anything.

Usage:
    python tailor_resume.py job.txt          # job posting in a text file
    pbpaste | python tailor_resume.py        # or pipe it in
Writes tailored_resume.md (print it or save as PDF).

The model's ONLY job: given my resume facts and a job posting, pick the
most relevant bullets, reword them toward the posting, choose skills,
and write a 1-2 sentence summary, returned as JSON.
The code: loads my facts, builds the prompt, parses and checks the JSON
against resume.json, retries once, falls back to keyword matching,
writes the file, and logs every run.
"""
import json, os, re, shlex, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
RESUME = json.load(open(os.path.join(HERE, "resume.json")))
CLAUDE_CMD = shlex.split(os.environ.get("TAILOR_CMD", "claude -p"))
MAX_POSTING = 6000
MAX_BULLETS = 8
LOG_FILE = os.path.join(HERE, "tailor.log")

PROMPT = """You tailor a student's resume to a job posting.
Use ONLY facts in RESUME. Never add employers, titles, dates, numbers,
tools, or achievements that are not in the original bullet.
Return ONLY JSON, no code fences, in exactly this shape:
{{"summary": "1-2 sentences aimed at this job",
  "bullets": [{{"id": "<id from RESUME>", "text": "reworded bullet"}}],
  "skills": ["skills from RESUME skills list, most relevant first"]}}
Pick at most {max_b} bullets, most relevant first. Always include "edu".
{feedback}
RESUME:
{resume}

JOB POSTING:
{posting}"""

WORD = re.compile(r"[A-Za-z][A-Za-z+#.]{2,}")


def ask_claude(posting, feedback=""):
    prompt = PROMPT.format(max_b=MAX_BULLETS, feedback=feedback,
                           resume=json.dumps(RESUME, indent=1),
                           posting=posting)
    r = subprocess.run(CLAUDE_CMD, input=prompt, capture_output=True,
                       text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "claude exited non-zero")
    return r.stdout


def parse(raw):
    raw = re.sub(r"^```\w*\n?|\n?```$", "", raw.strip()).strip()
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0:
        raise ValueError("no JSON object in answer")
    return json.loads(raw[start:end + 1])


def check(out):
    """Return a list of problems; empty means the answer is trustworthy."""
    facts = {b["id"]: b for b in RESUME["bullets"]}
    skills = {s.lower() for s in RESUME["skills"]}
    problems = []
    if not isinstance(out.get("summary"), str) or not out["summary"].strip():
        problems.append("missing summary")
    bullets = out.get("bullets")
    if not isinstance(bullets, list) or not bullets:
        return problems + ["no bullets"]
    if len(bullets) > MAX_BULLETS:
        problems.append(f"{len(bullets)} bullets (max {MAX_BULLETS})")
    ids = [b.get("id") for b in bullets]
    if "edu" not in ids:
        problems.append('education bullet "edu" missing')
    if len(set(ids)) != len(ids):
        problems.append("duplicate bullet ids")
    for b in bullets:
        src = facts.get(b.get("id"))
        if not src:
            problems.append(f'unknown bullet id "{b.get("id")}" (invented?)')
            continue
        # numbers (dates, counts, percentages) must come from the original
        for num in re.findall(r"\d+", b.get("text", "")):
            if num not in src["text"] and num not in src["section"]:
                problems.append(f'bullet "{b["id"]}" adds number {num}')
    for s in out.get("skills", []):
        if s.lower() not in skills:
            problems.append(f'skill "{s}" is not on my resume')
    return problems


def fallback(posting):
    """No model: rank original bullets by words shared with the posting."""
    words = {w.lower() for w in WORD.findall(posting)}
    def score(b):
        return len(words & {w.lower() for w in WORD.findall(b["text"])})
    ranked = sorted(RESUME["bullets"], key=score, reverse=True)
    picked = [b for b in ranked if b["id"] == "edu"] + \
             [b for b in ranked if b["id"] != "edu"][:MAX_BULLETS - 1]
    sk = [s for s in RESUME["skills"] if s.lower() in posting.lower()] or \
         RESUME["skills"]
    return {"summary": RESUME["headline"],
            "bullets": [{"id": b["id"], "text": b["text"]} for b in picked],
            "skills": sk}


def render(out, source):
    facts = {b["id"]: b for b in RESUME["bullets"]}
    lines = [f"# {RESUME['name']}", "", out["summary"].strip(), "",
             "**Skills:** " + ", ".join(out["skills"]), ""]
    current = None
    for b in out["bullets"]:
        sec = facts[b["id"]]["section"]
        if sec != current:
            lines += ["", f"## {sec}"]
            current = sec
        lines.append(f"- {b['text'].strip()}")
    lines += ["", f"<!-- tailored by {source}, {time.strftime('%Y-%m-%d %H:%M')} -->"]
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) > 1:
        posting = open(sys.argv[1]).read()
    else:
        posting = sys.stdin.read()
    if not posting.strip():
        print("Give me a job posting: python tailor_resume.py job.txt")
        return 1
    posting = posting[:MAX_POSTING]

    entry = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "attempts": []}
    result, feedback = None, ""
    for _ in (1, 2):                            # one retry
        try:
            raw = ask_claude(posting, feedback)
        except Exception as e:
            entry["attempts"].append({"error": str(e)[:200]})
            break
        try:
            out = parse(raw)
            problems = check(out)
        except Exception as e:
            out, problems = None, [f"bad JSON: {e}"]
        entry["attempts"].append({"raw": raw[:400], "problems": problems})
        if not problems:
            result = out
            break
        feedback = "Your last answer was rejected: " + "; ".join(problems) + \
                   ". Fix these and use only RESUME facts.\n"

    source = "claude" if result else "fallback (keyword match)"
    result = result or fallback(posting)
    entry["source"] = source
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    md = render(result, source)
    with open("tailored_resume.md", "w") as f:
        f.write(md)
    print(md)
    print(f"[saved tailored_resume.md, written by {source}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
