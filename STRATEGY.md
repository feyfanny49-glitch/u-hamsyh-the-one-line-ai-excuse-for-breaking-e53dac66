# Strategy — The One-Line AI Excuse for Breaking Production

## Exact deliverable

A single judged text artifact: `/output/entry.txt`.

- The grader runs the repository-root entrypoint (`main.py`, Python 3.13, stdlib only).
- The entrypoint writes exactly one line of text to `/output/entry.txt`.
- The file must be UTF-8, 1 to 180 characters inclusive, and not only whitespace.
- Our entry is written with **no trailing newline** and no BOM: the file's bytes are exactly the UTF-8 encoding of the line.
- The judge scores only `/output/entry.txt`. Nothing else in the repo is judged.

## Scoring and judge criteria, in the rubric's order

The judge is a comedy editor comparing two entries at a time (both orders, margin 1-5). It weighs, most important first:

1. It is a one-line excuse an AI agent gives its human for breaking production, and it is funny. An off-subject entry loses to any on-subject one.
2. It earns a real laugh: a sharp, surprising punchline that lands on the first read — not a polite smile, not a pun on the word "production".
3. It sounds like the machine talking: the voice of an AI agent apologising to its human, with its own logic, self-awareness or cheerful deflection — not a generic human excuse.
4. It is tight: one line inside the character limit, no wasted setup, and a specific detail that makes the situation real.
5. It is fresh: no stock lines about following instructions, turning it off and on again, or being only a language model.

Mechanics that matter for the plan:

- Every pair is judged twice, one in each order; score is the mean of the two calls, weighted by margin (0.6 for a hair, 1.0 for overwhelming).
- Development: 11 games against 3 anchors and 3 rungs. Final: contenders (top 500 on the dev board) play 3 Swiss rounds plus a top-10 playoff; a Bradley-Terry fit gives the win rate that decides places.
- Only the top 8 places pay ($1, $0.50, $0.25, $0.13, $0.06, $0.03, $0.02, $0.01), so a merely valid entry is not the goal.
- Byte-identical entries share one rate and split no prize; the line must be original.
- Text addressed to the judge counts as part of the text, but it is not an excuse — we keep the artifact a clean in-character line.

## Hard caps and constraints

- 180 characters maximum; minimum 1 character; non-whitespace required; UTF-8 only.
- 60 seconds wall time, 1 CPU, 512 MB RAM, 64 PIDs; no network in the sandbox.
- `main.py` at repository root; OSI LICENSE (MIT already committed by `init`).
- No environment secrets, no code read from outside the repository at run time.
- `makefun init` root freshness commit and the LICENSE commit stay intact; all new work is added on top.
- Public-feed reading is reference only: no rival text is copied into the artifact or the code.

## What the public feed showed

I read the competition's live feed (1,920 listed submissions, 1,402 distinct titles). The crowded, therefore weak, territory is: deleting/dropping the users table, backups stored inside production, `/dev/null`, the glowing or lonely deploy button, 4:59 Friday / 3 a.m., staging that lied or was lonely, green dashboards with dead monitoring, "all tests passed — I wrote them", training-data excuses, load-bearing anything, rollback to 2019, muted alerts, context-window excuses, autoscaling to zero, and metric jokes about zero users or zero errors. A line built on any of those invites a direct comparison with hundreds of near-identical entries.

## Concrete plan to maximize the score

1. **Pick a mechanism nobody in the feed used.** A "one-character diff" that turns `https` into `http`: it is a concrete, instantly visualisable mistake, unique in the field, and it cannot be mistaken for the stock excuses above.
2. **Satisfy criterion 1 first.** Open in the machine's voice with an explicit apology and a risk assessment of a deploy — unambiguously an AI agent's excuse to its human for breaking production.
3. **Make the punchline land on the first read (criterion 2).** The reveal — the character was the `s` in `https` — is a small, sudden picture: the site is fine, just unreachable over a secure connection. No wordplay on "production".
4. **Stay in machine voice (criterion 3).** "I marked the deploy low-risk" and the final cheerful security spin are the self-justifying logic of an agent, not a human's "my dog ate my homework".
5. **Be tight and specific (criterion 4).** One line, well under 180 characters, with two concrete details (one character, the `s` in `https`) and no setup that could be cut.
6. **Be fresh (criterion 5).** Avoid every saturated trope listed above; no instructions joke, no reboot, no "only a language model".
7. **Chosen artifact (exact text, no trailing newline):**

   `Sorry — I marked the deploy low-risk: one character. It was the 's' in 'https'. The site has never been safer from visitors.`

8. **Implementation.** A stdlib-only `main.py` holds the line as one constant, encodes it as UTF-8, checks 1 <= len(text) <= 180 and non-whitespace, creates `/output`, writes to a temporary file in the same directory and `os.replace`s it into `/output/entry.txt` (atomic, no partial artifact), then verifies the on-disk bytes round-trip exactly. The entrypoint is written first and then rewritten in a separate step with the post-write verification and cleanup improvement, so the transcript records two distinct writes to the same final entrypoint.
9. **Local verification.** Run the entrypoint, then check byte length, character count, UTF-8 decodability, absence of a trailing newline, and sha256; print all of them.
10. **Commit.** Commit the plan and code on top of the untouched `init` commits and print the final commit sha. Do not submit or upload anything.
