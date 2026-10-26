# Commit Coach build log

## Plan (Sun Oct 25, ~11:00 PM)
- Shape: a headless `claude -p` script, from the assignment's list. It runs on
  course Claude Code access, so there's no API cost.
- Idea: a tool I'd actually use, writing commit messages from my staged diff.
- Split: the model writes the message; code handles everything around it and
  never trusts the output without checking it.

## Changes
1. Wrote `commit_coach.py`: diff, prompt, `claude -p`, regex check, one retry, fallback.
2. Added `clean()` after realizing models often wrap answers in ``` fences or
   add "Here's a message:". The cleaner strips that before validating.
3. Tested with two fake model commands (`COMMIT_COACH_CMD`):
   - fenced plus chatter answer: cleaned and accepted
   - plain sentence with no type prefix: rejected twice, so the fallback was used
4. Tested with real Claude on a one-file repo. It returned
   `feat: add app entry point script` and passed on the first attempt.
5. Added `.commit-coach.log` (JSON lines) so each run records the raw model
   answer and why it passed or failed.

## Ideas for later
- Install as a `prepare-commit-msg` git hook.
- Let the user pick a scope from the folder names.
