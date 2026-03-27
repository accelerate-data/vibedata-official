# Consolidation Format

How to produce the consolidated wrapper document after synthesis completes.

---

## Document Structure

The consolidated document is a lightweight navigation layer — not a copy of
the workspace files. It contains two sections: an executive summary and a
table of contents linking to the individual workspace files.

```markdown
# [Framing Question as Title]

## Executive Summary

[~500 words. Distill the synthesis into a standalone summary. Someone reading
only this section should understand: what was debated, what was agreed, what
wasn't, and what to do. Pull from synthesis.md — convergence map, key
recommendations, and prioritized action list.]

---

## Debate Record

### Round 1: Position Papers

- [Maximalist: [Position Label]](round1/position_maximalist.md)
- [Purist: [Position Label]](round1/position_purist.md)
- [Hybrid: [Position Label]](round1/position_hybrid.md)
- [Economist: [Position Label]](round1/position_economist.md)

### Round 2: Rebuttals

- [Maximalist Rebuttal](round2/rebuttal_maximalist.md)
- [Purist Rebuttal](round2/rebuttal_purist.md)
- [Hybrid Rebuttal](round2/rebuttal_hybrid.md)
- [Economist Rebuttal](round2/rebuttal_economist.md)

### Synthesis

- [Full Synthesis](synthesis.md) — debate arc, convergence map, residual
  disagreements, decision framework, recommendations, and prioritized actions
```

## Assembly Rules

1. **Executive summary is new writing.** It distills the synthesis into a
   standalone summary. Someone reading only the executive summary should
   understand: what was debated, what was agreed, what wasn't, and what
   to do.

2. **Links use relative paths.** All links point to files within the same
   workspace directory. The consolidated doc sits at the workspace root
   alongside `synthesis.md`.

3. **Position labels in links.** Each position paper link includes a short
   label derived from the agent's core position (e.g., "Maximalist: Invest
   in Full Seed Library").

4. **No inline content beyond the executive summary.** Do not copy position
   papers, rebuttals, or synthesis into this document. They live in their
   own files.

5. **No commentary between sections.** Do not add editorial transitions.
   The document structure speaks for itself.

## Output

Write to `{workspace}/consolidated_analysis.md`.
