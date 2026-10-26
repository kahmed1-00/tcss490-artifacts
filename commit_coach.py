#!/usr/bin/env python3
"""Commit Coach: Claude writes the commit message, plain code checks it.

Usage (inside any git repo, after `git add`):
    python commit_coach.py            # print a suggested message
    python commit_coach.py --commit   # suggest, confirm, then commit

The model's ONLY job: read the staged diff and write one commit message.
Everything else (getting the diff, trimming it, validating the format,
retrying, falling back, committing, logging) is plain code.
"""
import json, os, re, shlex, subprocess, sys, time

MAX_DIFF_CHARS = 12000          # keep the prompt small and cheap
TIMEOUT_S = 90
TYPES = "feat|fix|docs|style|refactor|test|chore|build|ci|perf"
PATTERN = re.compile(rf"^({TYPES})(\([\w\-./]+\))?: \S.{{0,70}}$")
CLAUDE_CMD = shlex.split(os.environ.get("COMMIT_COACH_CMD", "claude -p"))
LOG_FILE = ".commit-coach.log"

PROMPT = """You write git commit messages in Conventional Commits format.
Rules:
- Line 1: <type>(<optional scope>): <summary>, max 72 characters total.
- <type> is one of: {types}.
- Summary is imperative ("add", not "added"), no trailing period.
- Optionally a blank line, then up to 3 short "- " bullet lines.
- Output ONLY the message. No code fences, no quotes, no explanation.
{feedback}
Staged diff:
{diff}"""


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


def ask_claude(diff, feedback=""):
    prompt = PROMPT.format(types=TYPES.replace("|", ", "), diff=diff,
                           feedback=feedback)
    r = subprocess.run(CLAUDE_CMD, input=prompt, capture_output=True,
                       text=True, timeout=TIMEOUT_S)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "claude exited non-zero")
    return r.stdout


def clean(text):
    """Strip the usual model wrapping: fences, quotes, leading chatter."""
    text = re.sub(r"^```\w*\n?|\n?```$", "", text.strip()).strip()
    lines = text.splitlines()
    # drop chatter like "Here's a commit message:" before the real line
    while lines and not PATTERN.match(lines[0].strip().strip('"\'`')):
        if len(lines) == 1:
            break
        lines.pop(0)
    if lines:
        lines[0] = lines[0].strip().strip('"\'`')
    return "\n".join(lines).strip()


def check(msg):
    """Return a list of problems; empty list means the message passes."""
    if not msg:
        return ["message was empty"]
    first = msg.splitlines()[0]
    problems = []
    if len(first) > 72:
        problems.append(f"first line is {len(first)} chars (max 72)")
    if not PATTERN.match(first):
        problems.append("first line is not '<type>(scope): summary' "
                        f"with type in [{TYPES}]")
    if first.endswith("."):
        problems.append("summary ends with a period")
    return problems


def fallback(files):
    n = len(files)
    return f"chore: update {n} file{'s' if n != 1 else ''}"


def log(entry):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    diff = git("diff", "--cached")
    if not diff.strip():
        print("Nothing staged. Run `git add` first.")
        return 1
    files = git("diff", "--cached", "--name-only").split()
    trimmed = diff[:MAX_DIFF_CHARS]
    if len(diff) > MAX_DIFF_CHARS:
        trimmed += f"\n[diff truncated; {len(files)} files: {', '.join(files)}]"

    entry = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "files": len(files),
             "attempts": []}
    msg, feedback = None, ""
    for attempt in (1, 2):                      # one retry, then give up
        try:
            raw = ask_claude(trimmed, feedback)
        except Exception as e:                  # timeout, not logged in, etc.
            entry["attempts"].append({"error": str(e)[:200]})
            break
        candidate = clean(raw)
        problems = check(candidate)
        entry["attempts"].append({"raw": raw[:300], "problems": problems})
        if not problems:
            msg = candidate
            break
        feedback = ("Your last answer was rejected: " + "; ".join(problems)
                    + ". Fix it.\n")

    source = "claude" if msg else "fallback"
    msg = msg or fallback(files)
    entry["source"], entry["message"] = source, msg
    log(entry)

    print(f"--- suggested by {source} ---\n{msg}\n---")
    if "--commit" in sys.argv:
        if input("Commit with this message? [y/N] ").lower().startswith("y"):
            subprocess.run(["git", "commit", "-m", msg])
    return 0


if __name__ == "__main__":
    sys.exit(main())
