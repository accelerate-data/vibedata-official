# Synthesis Template

Instructions for the main agent producing the final synthesis after both
debate rounds complete.

---

## Context You Have

As the main agent, you have:
- The user's original framing question
- All reference cases with full details
- The tension map from Phase 1 (your own research reading)
- All 4 position papers from Round 1
- The debate threads you extracted and the user approved/pruned
- The live debate exchange context (challenge/defense summaries from idle
  notifications during Round 2's team-based debate)
- All 4 rebuttals from Round 2
- Understanding of WHY the user pruned certain threads

This context advantage is why synthesis must be done by you, not a subagent.

## Synthesis Structure

Write the synthesis as a markdown document with these sections:

### 1. Debate Arc (including Exchange Highlights)

For each agent, summarize in 2-3 sentences:
- Where they started (Round 1 core position)
- Where they ended (Round 2 revised position)
- What changed and why

The arc shows the MOVEMENT in thinking. If an agent didn't move at all,
note that — it either means their position was very strong or they didn't
engage honestly with opposing arguments.

**Debate Exchange Highlights** (~500 words): After the per-agent arcs,
include a sub-section with the most consequential moments from the live
challenge/defense exchange. Focus on:
- Challenges that landed — where an agent was caught on a specific claim
  and couldn't adequately defend it
- Concessions that changed the debate — where an agent admitted a flaw
  that shifted their rebuttal
- Surprising agreements — where opponents found common ground on an
  unexpected point

Quote or paraphrase specific exchanges. This section bridges the position
papers and rebuttals — it explains WHY the rebuttals look different from
the position papers. It also feeds into the consolidated document's
section 2.5.

### 2. Convergence Map

List the specific claims or conclusions that ALL FOUR agents agreed on by
the end of Round 2. These are high-confidence findings.

Format:
```
**Convergence 1: [Statement]**
All agents agree. Maximalist cited [X], Purist conceded [Y],
Hybrid incorporated [Z], Economist scored [W].
```

If there are no convergence points, say so. That itself is a finding.

### 3. Residual Disagreements

List specific disagreements that survived both rounds. For each:
- What the disagreement is (precisely)
- Which agents are on which side
- What evidence would resolve it (is it testable?)
- Whether it's empirical (can be resolved with data) or values-based
  (depends on priorities)

This section is critical. Do NOT paper over disagreements. If reasonable
people can disagree after seeing the same evidence, the synthesis should
make that visible, not pretend a consensus was reached.

### 4. Decision Framework

Extract and refine the Economist's scoring rubric from Round 2. Annotate
each dimension with evidence from the full debate:

```
**Dimension: [Name]**
- Scoring criteria: [How to evaluate]
- Maximalist evidence: [What supports a high score here]
- Purist evidence: [What supports a low score here]
- Weight: [How important is this dimension, informed by debate]
```

If the Economist's rubric was challenged effectively by other agents, revise
it. The framework should reflect the strongest version that survived debate,
not necessarily the Economist's original.

### 5. Reference Case Application

Apply the decision framework to each reference case. Show the work:

```
**Case: [Name]**
- Dimension 1: Score [X] — because [specific case detail]
- Dimension 2: Score [Y] — because [specific case detail]
- ...
- Overall recommendation: [Approach] — because [scoring rationale]
```

Different cases may get different recommendations. That's expected and
valuable — it shows the framework is discriminating, not just rubber-stamping
one approach.

### 6. Concrete Recommendations

Categorize recommendations into:

**Do fully:** Things the debate strongly supports doing comprehensively.
List which agents agree, what evidence supports this.

**Do partially / conditionally:** Things that make sense in specific contexts.
State the conditions. Reference which cases triggered this.

**Avoid:** Things the debate shows are risky or not worth the effort.
State which agents identified the risks, what the failure modes are.

**Needs more data:** Things the debate couldn't resolve because the evidence
is insufficient. State what data would resolve it.

For EACH recommendation: state which agents agree, which disagree, and what
evidence would change the recommendation. This is the anti-flattening rule.

### 7. Prioritized Action List

Convert recommendations into a sequenced action list. For each item:
- What to do (specific action)
- Why (which recommendation it implements)
- Dependencies (what must happen first)
- Decision point (what information would change this action)

## Anti-Flattening Rules

These rules exist because synthesis naturally tends toward mushy centrism.
The whole point of the adversarial debate is to surface genuine tension.
Flattening that tension into "it depends" wastes the entire exercise.

1. **Never average positions.** "Do some of X" is not a synthesis — it's
   giving up on the question. If the answer is conditional, state the
   specific conditions.

2. **Preserve minority dissent.** If one agent had a strong argument that
   the other three didn't adequately address, call it out. The synthesis
   should flag unresolved challenges, not majority-vote them away.

3. **Distinguish empirical from values-based disagreements.** "We don't
   have the data" is different from "we disagree on what matters." Both are
   valid residual disagreements but they need different resolution paths.

4. **Quote specific agent claims.** When stating a recommendation, include
   the specific agent argument that supports it. "The Purist showed that
   for Case 1, [specific mechanism] causes [specific failure]" is better
   than "there are risks."

5. **Show the Economist's numbers.** If the Economist provided cost
   estimates, risk scores, or a scoring rubric, include them in the
   synthesis even if other agents challenged the methodology. Then note
   the challenges.

## Output

Write the complete synthesis to `{workspace}/synthesis.md`.
