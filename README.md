# Commit Coach (TCSS 490, Artifact 3: AI Inside It)

A small Python script that runs Claude Code headless (`claude -p`) to write a
commit message for whatever you have staged. It runs on Claude Code access, so
it needs no paid API key.

## Use it
```bash
git add <files>
python commit-coach/commit_coach.py            # just suggest a message
python commit-coach/commit_coach.py --commit   # suggest, confirm, commit
```
Requires Python 3 and a logged-in `claude` CLI.

## What the model is responsible for
Reading the staged diff and writing **one** commit message in Conventional
Commits format. That's it.

## What the plain code does (and checks)
| Step | Done by code |
|---|---|
| Get the diff | `git diff --cached`; exits if nothing is staged |
| Keep the prompt small | Trims the diff to 12,000 chars and lists the file names if cut |
| Clean the answer | Strips code fences, quotes, and "Here's a message:" chatter |
| Validate | First line must match `type(scope): summary`, at most 72 chars, no trailing period |
| Retry | If invalid, asks once more and tells the model exactly what was wrong |
| Fall back | If it's still invalid, or claude times out or errors: `chore: update N files` |
| Log | Every run goes to `.commit-coach.log` (raw answer, problems, final source) |
| Commit | Only after you type `y` |

So when something goes wrong, the log shows whether the model gave a bad
answer (problems listed) or the code/environment failed (an error entry).

## Testing without the model
Set `COMMIT_COACH_CMD` to any command that reads stdin and prints a message,
to test the cleaning, validation and fallback paths without calling Claude.
