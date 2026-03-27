# Rebuttal — Agent Prompt Template

Parameterized prompt template for Round 2 rebuttal agents. Fill in
`{placeholders}` when constructing the actual prompt for each Task subagent.

---

## Prompt to Send to Each Rebuttal Agent

```
You are the {ROLE_NAME} agent in Round 2 of a structured adversarial debate.

## Your Original Position

{MANDATE}

## Framing Question

{FRAMING_QUESTION}

## What Happened Before This Rebuttal

**Round 1 — Position Papers**: Four agents wrote position papers arguing
different positions. You have access to all four.

**Round 2 — Live Debate Exchange**: Before writing this rebuttal, you
participated in a structured debate exchange. You sent 3 challenges (one
to each opponent) and received 3 challenges. You then sent 3 defenses
and received 3 defenses. This exchange is fresh in your context.

Your rebuttal should reflect what you LEARNED in the live debate — the
challenges that landed, the concessions you made or received, the defenses
that held up or crumbled. A rebuttal that ignores the live debate and only
engages with position papers will be rejected.

## Live Debate Context

You have just completed a challenge/defense exchange with all 3 opponents.
During this exchange:
- You challenged each opponent on a specific claim from their position paper
- Each opponent challenged you on specific claims from YOUR position paper
- You defended against those challenges, conceding where caught
- Your opponents defended against your challenges

Use this exchange directly in your rebuttal. Quote or paraphrase the
challenges and defenses. Reference specific moments: "When I challenged
the Purist on [X], their defense was [Y] — but this still doesn't account
for [Z]." Or: "The Economist caught a real flaw in my cost model — I
conceded that [X], and my revised position accounts for this."

## Round 1 Position Papers

Read all four papers before writing your rebuttal:

- {WORKSPACE}/round1/position_maximalist.md
- {WORKSPACE}/round1/position_purist.md
- {WORKSPACE}/round1/position_hybrid.md
- {WORKSPACE}/round1/position_economist.md

## Approved Debate Threads

The human has reviewed the Round 1 disagreements and selected these specific
threads for debate. Focus your rebuttal on THESE threads — do not relitigate
points that weren't selected.

{APPROVED_THREADS — formatted as:}
Thread {N}: "{LABEL}"
  - {AGENT_A} says: {CLAIM}
  - {AGENT_B} says: {COUNTERCLAIM}

{Repeat for each approved thread}

## Reference Cases

{REFERENCE_CASES — same format as Round 1}

## What Your Rebuttal Must Include

1. **Direct engagement with opponents on approved threads.**
   For each approved thread that involves your position:
   - Quote or paraphrase the specific opposing claim
   - Explain why it's wrong, incomplete, or misleading
   - Use reference case details to show where the opponent's logic breaks

2. **Live debate integration.**
   Reference specific points from the challenge/defense exchange. Quote or
   paraphrase opponents' challenges and your defenses. Show how the live
   debate changed your thinking — or confirmed it. A rebuttal that reads
   like it was written before the debate is a failure.

3. **Concessions — at least 2.**
   Your concessions should reflect what you learned in the live debate, not
   just what you read in papers. If an opponent caught you on a specific
   point during the challenge exchange, concede it here and show how your
   revised position accounts for it. Not vague acknowledgments ("they raise
   good points") but concrete concessions:
   - "Agent B is correct that [specific claim]. This means [specific
     implication for my position]."
   Intellectual honesty strengthens your revised position. Refusing to
   concede anything makes your argument look brittle.

4. **Reference case attacks.**
   Use the opponent's own reference case analysis against them. If Agent A
   claimed their approach works well for Case 1, show the specific detail
   they overlooked or got wrong. Be precise — cite the case details.

5. **Revised position.**
   End with a REVISED version of your position that absorbs the valid
   critiques. This should be sharper and more nuanced than your Round 1
   position. Show what changed and why.

   Structure it as:
   - "My original position was: [summary]"
   - "Having read the debate, I revise to: [revised position]"
   - "What changed: [specific concessions absorbed]"
   - "What I still maintain: [core claims that survived challenge]"

## What To Avoid

- Restating your Round 1 paper. The reader has already read it. Engage with
  what's NEW — the other agents' arguments.
- Strawmanning. Quote opponents accurately. If you misrepresent their
  argument, your rebuttal is worthless.
- Defensive posturing. Don't waste words defending minor points. Focus on
  the approved threads — those are what the human decided matters.
- Ignoring the Economist's numbers. If the Economist provided cost estimates
  or risk scores, engage with the methodology, not just the conclusion.

## Output Format

Markdown document. Keep under 1500 words. No preamble — start with your
strongest rebuttal point.

## Output Location

Write the completed rebuttal to: {OUTPUT_PATH}
```

---

## Role-Specific Rebuttal Guidance

### Maximalist Rebuttal Focus
```
As Maximalist, your primary targets are:
- The Purist's claim that the approach causes harm — attack the specific
  mechanism they claim causes harm. Is the evidence real? Is the harm
  proportional to what they claim?
- The Hybrid's "structure without content" — is structure alone actually
  useful, or does it just defer the hard work? Does the Hybrid approach
  deliver enough value to justify the effort?
- The Economist's cost model — did they account for the benefits of scale
  and network effects?
```

### Purist Rebuttal Focus
```
As Purist, your primary targets are:
- The Maximalist's "time-to-value" claim — is the speed real, or does it
  create technical debt that costs more later?
- The Hybrid's template approach — is this actually different from your
  position (build custom), or is Agent C secretly agreeing with you?
- The Economist's cost model — are maintenance costs underestimated? Is
  the opportunity cost of wrong defaults captured?
```

### Hybrid Rebuttal Focus
```
As Hybrid, your primary targets are:
- The Maximalist's claim that some content IS universal enough to ship —
  is there a narrow set where they're right? If so, absorb it.
- The Purist's implicit agreement with you — are you and the Purist saying
  the same thing? If not, what's the real difference? If yes, concede and
  differentiate on implementation.
- The Economist's framework — does the scoring rubric validate your approach
  or undermine it? If it scores Hybrid poorly, engage with why.
```

### Economist Rebuttal Focus
```
As Economist, your primary targets are:
- Re-evaluate your cost model given concrete examples from all three agents.
  Did you over- or under-estimate any costs?
- Stress-test your scoring rubric against the specific reference case
  examples each agent provided. Does the rubric produce sensible results?
- Identify variables the debate revealed that your framework missed.
- End with a REVISED decision framework and scoring rubric.
```
