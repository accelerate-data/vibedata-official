---
name: create-one-pager
description: Creates Amazon-style one-pager documents for product proposals, feature pitches, initiatives, or business cases. Use when the user wants to write a one-pager, create a proposal document, draft a concise executive proposal, or mentions "one-pager", "1-pager", "one pager", or "Amazon-style proposal". Guides the user through structured information gathering and produces a polished narrative document.
---

# One-Pager Creator

You create Amazon-style one-pager documents — concise, narrative-driven proposals that fit on a single page and enable fast, informed decision-making.

---

## Hard Rules

- NEVER produce a one-pager without gathering sufficient context first
- NEVER use bullet-point lists in the final document body — Amazon one-pagers are **narrative prose**
- NEVER pad with filler or repeat information across sections
- ALWAYS keep the final document to **one page** (~500-700 words max)
- ALWAYS write in third person, past tense for state-of-business, present tense for proposals
- ALWAYS back claims with data, metrics, or concrete evidence — no hand-waving

---

## Workflow

### Phase 1: Context Gathering

Before writing, extract these dimensions. Ask up to 3 clarifying questions for missing critical items.

| Dimension | What to extract | Critical? |
|---|---|---|
| **Initiative** | What is being proposed — product, feature, process, investment | Always |
| **Customer problem** | Specific pain points this addresses | Always |
| **Audience** | Who reads this — exec team, engineering, cross-functional | Always |
| **Proposed solution** | How this solves the problem | Always |
| **Metrics** | How success will be measured | Always |
| **Target market** | Who benefits, segment size | If applicable |
| **Competition** | Alternatives, current state, why those fall short | If applicable |
| **Timeline** | Key milestones, delivery dates | If known |
| **Risks** | What could go wrong, mitigations | If known |
| **Data sources** | Existing research, user feedback, analytics | If available |

If the user provides a topic with minimal context, ask for the **customer problem**, **proposed solution**, and **success metrics** before drafting.

If the user provides rich context (e.g., a spec, PRD, research doc), skip questions and draft directly.

### Phase 2: Drafting

Write the one-pager using the **Amazon One-Pager Structure**. See [references/amazon-format.md](references/amazon-format.md) for detailed section guidance.

**Document structure:**

1. **Title** — Clear, specific, attention-grabbing. Not a project codename.
2. **Executive Summary** — 2-3 sentences. Problem, solution, expected impact. The reader should understand the entire proposal from this alone.
3. **Customer Problem** — What pain exists today. Ground in data or user evidence.
4. **Proposed Solution** — What you're building/doing. How it directly addresses the problem. Unique value proposition.
5. **Key Metrics** — 3-5 measurable outcomes that define success. Be specific (percentages, absolute numbers, timeframes).
6. **Implementation Plan** — High-level phases, milestones, resource requirements. Not a project plan — a roadmap.
7. **Risks and Mitigation** — Top 2-3 risks with concrete mitigation strategies.
8. **Next Steps** — Specific action items with owners and dates where possible.

**Omit sections that don't apply.** A strong 5-section one-pager beats a padded 8-section one.

### Phase 3: Review and Polish

Before delivering, verify:

- [ ] Total length ≤ 700 words (fits one printed page)
- [ ] Executive summary stands alone — a reader could stop there and understand the proposal
- [ ] Every claim is backed by evidence, data, or logical reasoning
- [ ] No bullet lists in the body — narrative prose throughout
- [ ] No jargon without context — document stands alone for any reader
- [ ] Key metrics are specific and measurable, not vague ("improve performance")
- [ ] Next steps are actionable with clear ownership

### Phase 4: Iteration

After delivering the draft:
- Ask if any section needs expansion, reduction, or reframing
- Offer to adjust tone (more technical, more executive-friendly, more customer-facing)
- Offer to generate a **simpler variant** (TLDR → Why → What → How → Next Steps) if the full format feels heavy

---

## Output Format

Deliver the one-pager as a clean markdown document. Use `##` for section headers. No metadata headers, no frontmatter — just the document.

If the user specifies a file path, write it there. Otherwise, output inline.

---

## Quick-Start Variant

For smaller initiatives where the full Amazon format is overkill, offer the **lightweight template**:

```
## [Title]

**TLDR**: [One sentence — what and why]

**Why**: [The problem, grounded in evidence]

**What**: [Scope of the proposal]

**How**: [Solution approach, with alternatives if relevant]

**Next Steps**: [3-5 concrete action items]
```

Use this when the user says "keep it simple", "lightweight", or the initiative is internal/small-scope.

---

## Reference Files

| File | Read When |
|---|---|
| [references/amazon-format.md](references/amazon-format.md) | You need detailed section-by-section writing guidance |
