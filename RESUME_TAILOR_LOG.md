# Resume Tailor build log (Artifact 3)

## Plan (Sun Oct 25, 11:00 PM)
- My original Artifact 3 idea was a static Resume & Projects Showcase page. That
  doesn't meet "a model does real work every time it runs," so I put AI inside it.
- Shape: a headless `claude -p` script, so there's no API cost.
- Split: Claude chooses and rewords. Code owns the facts and rejects anything
  not backed by `resume.json`.

## Changes
1. Briefly built a different tool (Commit Coach), then switched back to the
   resume idea because that's the artifact I'd planned and will actually use.
2. Moved my resume facts from the site into `resume.json` (13 bullets + skills).
3. Wrote `tailor_resume.py`: prompt, JSON parse, checks, one retry,
   keyword fallback, Markdown output, run log.
4. Fake-model test (`TAILOR_CMD`) with an invented employer, number, and skill:
   all three flagged and the fallback was used.
5. Real Claude test with a Cloud Support internship posting: it picked
   education, AWS cert, the Amazon troubleshooting bullets, and cloud/Python
   projects, ordered AWS/Linux/Python first, and passed every check on the
   first try.

## What I noticed
- The rewording is the risky part. A model will happily "improve" a bullet with
  numbers that aren't real, so the number check matters more than the format check.

## Ideas for later
- A button on the portfolio page (needs an API key or a hosted runner).
- A check that rewording keeps the meaning, not just the numbers.
