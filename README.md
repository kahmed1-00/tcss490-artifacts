# Resume Tailor (TCSS 490, Artifact 3: AI Inside It)

My Resume & Projects Showcase, with a model inside it. Give it a job posting and
Claude tailors my resume to that job. Plain code makes sure Claude never
invents experience. It runs Claude Code headless (`claude -p`), so it uses
course Claude Code access with no paid API key.

## Use it
```bash
python tailor_resume.py job.txt     # job posting saved as a text file
```
Output: `tailored_resume.md`, ready to print or save as a PDF. Needs Python 3
and a logged-in `claude` CLI.

## What the model is responsible for
Given my resume facts (`resume.json`) and the posting, Claude:
- picks the most relevant bullets (at most 8)
- rewords them toward the job
- orders my skills by relevance
- writes a 1-2 sentence summary

It returns all of this as JSON.

## What the plain code does (and checks)
| Step | Done by code |
|---|---|
| Facts | Loads `resume.json`, the only source of truth |
| Parse | Strips code fences and pulls out the JSON object |
| No invented bullets | Every bullet id must exist in `resume.json` |
| No invented numbers | Any number (date, count, %) must appear in the original bullet |
| No invented skills | Every skill must be on my skills list |
| Limits | At most 8 bullets, no duplicates, education always included |
| Retry | On any problem, asks once more and tells Claude exactly what was wrong |
| Fall back | Still bad, or claude fails: ranks my original bullets by keyword overlap |
| Log | Every run goes to `tailor.log` (raw answer, problems, which path won) |

## Testing without the model
Set `TAILOR_CMD` to any command that prints JSON. I tested it with a fake model
that invented a Google internship, "500 customers", and Kubernetes. The checks
caught all three and the fallback was used.

Build log: `RESUME_TAILOR_LOG.md`.
