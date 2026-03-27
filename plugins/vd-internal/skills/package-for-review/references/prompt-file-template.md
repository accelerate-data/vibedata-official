# Prompt File Template

Use this template when creating `{name}-prompt.md` files for each deliverable in the package. Replace all `{PLACEHOLDER}` values.

---

```markdown
# Prompt Used: {DELIVERABLE_TITLE}

## Context loaded
- {List each document, file, or prior analysis that was in context when this deliverable was generated}
- {Be specific: file names, not "various documents"}
- {If context was from conversation (not files), note "Prior conversation analysis of X"}

## User instruction

> {The user's original instruction, verbatim if available.}
> {If the exact wording was lost to context compaction, reconstruct it and note: "[Reconstructed — original wording was compacted]"}

{If there were follow-up clarifications that changed the direction, include them as separate blockquotes:}

Follow-up:

> {Follow-up instruction}

## How the output was generated

{Narrative description of how the deliverable was produced. Include:}
- {What steps were taken (e.g., "Read the architecture doc, then mapped each source against the 12 gap items")}
- {Whether subagents were used and how they were structured}
- {What tools were invoked (e.g., "3 parallel Agent subagents, one per persona")}
- {Any post-processing or consolidation done after initial generation}

## Key design decisions
- {Decision 1: what was chosen and why (e.g., "Source resolution intentionally omitted per user instruction — scenarios define WHAT, not WHERE")}
- {Decision 2: what was chosen and why}
```

---

## Writing Guidelines

- **Verbatim over reconstructed**: Always prefer the user's exact words. Only reconstruct if context compaction has removed the original.
- **Context loaded must be specific**: "vibedata-strategy.md (L1 product vision)" not "strategy document". A reader re-running the prompt needs to know exactly what to load.
- **How the output was generated should be reproducible**: Another person reading this should be able to follow the same steps and get a similar result.
- **Key design decisions capture the judgment calls**: Not every choice needs to be listed — only the ones where a different choice would have produced a meaningfully different output.
