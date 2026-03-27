# README Template for Review Packages

Use this template when creating the README for a review package. Replace all `{PLACEHOLDER}` values with actual content. Remove any sections that do not apply (e.g., "Decisions We Need to Make" if there are no decisions).

---

```markdown
# {PACKAGE_TITLE}

{ONE_LINE_SUMMARY — what this package contains and why it exists}

---

## Start Here

**[{ONE_PAGER_FILENAME}]({ONE_PAGER_FILENAME})** — {One sentence describing the one-pager. Example: "The full proposal in one page. Read this first. It links to the supporting documents below for anyone who wants to dig deeper."}

---

## Decisions We Need to Make

{PREAMBLE — e.g., "These are in [{RELEVANT_DOC}]({RELEVANT_DOC}#section-anchor):"}

1. {Decision 1}?
2. {Decision 2}?
3. {Decision 3}?

---

## How We Got Here

{PARAGRAPH 1 — What question started the research. What was the initial trigger or hypothesis. Why it mattered.}

{PARAGRAPH 2 — What the first analysis found. How that finding raised the next question. What the second step discovered.}

{PARAGRAPH 3 — How the findings accumulated into the proposal. What the overall arc is. What was validated and what remains open.}

{OPTIONAL PARAGRAPH 4 — Any additional context about the research path. Only include if the chain was long enough to warrant it.}

---

## Supporting Documents

If the one-pager raises questions, the supporting evidence is below. Each document builds on the previous one — they follow the research path that led to the proposal.

| Step | File | What It Contains | When to Read |
|---|---|---|---|
| 1 | [{FILE_1}]({FILE_1}) | {Brief description of content and key finding} | {When a reader would need this — e.g., "If you question whether X is really Y"} |
| 2 | [{FILE_2}]({FILE_2}) | {Brief description} | {When to read} |
| 3 | [{FILE_3}]({FILE_3}) | {Brief description} | {When to read} |
| ... | ... | ... | ... |

## Prompts Used

Each analysis was generated with a specific prompt. These are included for transparency — anyone can re-run or modify the analysis.

| File | Prompt |
|---|---|
| {DELIVERABLE_1} | [{DELIVERABLE_1_PROMPT}]({DELIVERABLE_1_PROMPT}) |
| {DELIVERABLE_2} | [{DELIVERABLE_2_PROMPT}]({DELIVERABLE_2_PROMPT}) |
| ... | ... |

---

## Key Numbers

- **{NUMBER_1}** {what it means}
- **{NUMBER_2}** {what it means}
- **{NUMBER_3}** {what it means}
- ...
```

---

## Writing Guidelines

- **"How We Got Here" is the second most important section** after the one-pager link. Do not skip it or compress it to a single sentence. A reader who reads only the one-pager and "How We Got Here" should understand both WHAT is being proposed and WHY.
- **"When to Read" column** in the supporting documents table is critical for busy readers. It tells them: "You do not need to read this unless you have this specific question." This respects their time.
- **"We" voice throughout** — decisions are framed as "Decisions we need to make", not "Decisions for you". The author is part of the team.
- **Research sequence, not alphabetical** — the supporting documents table follows the logical chain (Step 1, 2, 3...) so a reader who does want to go deeper can follow the same path.
