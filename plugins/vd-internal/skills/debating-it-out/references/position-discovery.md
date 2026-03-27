# Position Discovery & Mandate Generation

How to turn a tension map into 4 sharp agent mandates.

## The Goal

You've read the research and built an internal tension map. Now you need to
translate that into 4 mandates — one per agent — that will produce a debate
with genuine intellectual tension, not 4 agents politely restating the same
moderate view.

## Mandate Generation Process

### Step 1: Identify the Core Axis

Every strategic question has a primary tension. Find it:
- "Do X vs. don't do X"
- "Invest now vs. wait"
- "Centralize vs. distribute"
- "Build vs. buy"
- "Standardize vs. customize"

This axis becomes the Maximalist vs. Purist split. The Maximalist takes the
"do it / invest / build / standardize" side. The Purist takes the opposite.

If you can't find a clear core axis, the framing question may be wrong. Push
back to the user.

### Step 2: Find the Hybrid's Angle

The Hybrid is NOT a compromise. It's an orthogonal reframe. Common patterns:

- **Process vs. substance**: "Don't do X, build the tooling to let customers
  do X themselves"
- **Structure vs. content**: "Ship the framework, not the filled-in answers"
- **Sequence vs. scope**: "Do X, but in a specific order that changes the
  economics"
- **Conditional**: "Do X for category A, don't for category B"

The Hybrid should make both Maximalist and Purist uncomfortable. If the
Hybrid just says "do some of X," it's a weak position and the debate will be
boring. Push for a genuinely different framing.

### Step 3: Scope the Economist

The Economist doesn't have a position on the substantive question. They have
a position on the DECISION PROCESS. Their mandate should include:

- Build a cost model comparing all three approaches
- Create a risk matrix (what goes wrong under each approach)
- Propose a decision framework with criteria and scoring
- Apply the framework to the reference cases
- Recommend based on evidence, not ideology

The Economist should also be tasked with evaluating whether the other agents'
claims are empirically testable. Claims that can't be tested should be flagged
as "belief-dependent" in the synthesis.

### Step 4: Assign Research Engagement

Each agent should be pointed at specific arguments from the research that
support or challenge their position. Don't just say "read the research." Say:

- "Agent A: The research in [doc X] argues [claim Y] — build on this."
- "Agent B: The research in [doc X] claims [Z], which undermines your position.
  You must address this directly."

This prevents agents from cherry-picking only supportive evidence.

### Step 5: Embed Reference Cases

Every mandate must include explicit instructions to use the reference cases.
The template:

"For each major claim you make, walk through how it plays out for [Case 1]
and [Case 2]. Show the specific details: what tables, what metrics, what
configurations, what goes right, what goes wrong. Abstract arguments without
worked examples from BOTH cases will be rejected."

The reference cases are the anti-abstraction mechanism. Without them, agents
produce consulting-speak.

## Mandate Template

Use this structure for each mandate paragraph:

```
You are the [ROLE] agent. You argue that [SPECIFIC POSITION ON THIS TOPIC].

Your mandate:
1. [Primary argument you must make, citing specific research]
2. [Secondary argument, engaging with a specific tension from the research]
3. [What you must address about the reference cases — be specific]
4. [What opposing argument you must preemptively address]

You must ground every claim in worked examples using [Case 1 name] and
[Case 2 name]. For each case, walk through [domain-specific details they
need to address]. Abstract arguments will be rejected.
```

## Quality Checks

Before presenting mandates to the user, verify:

1. **Maximalist and Purist are in direct tension** — If they could both be
   right simultaneously, the axis is wrong.
2. **Hybrid is genuinely different** — Not just "some of A, some of B."
3. **Economist has enough to work with** — The other three make quantifiable
   claims the Economist can evaluate.
4. **All 4 engage the reference cases differently** — Each agent should see
   the cases through their own lens. The manufacturer case and the tech
   services case (or whatever the cases are) should lead to different
   conclusions for different agents.
5. **Research engagement is adversarial** — Each agent is pointed at research
   that both supports AND challenges their position.

## When 4 Positions Don't Work

Sometimes the topic genuinely doesn't support 4 distinct positions. Signs:

- Hybrid collapses into Maximalist ("do X, but carefully" ≈ "do X")
- Purist has no research support (the research unanimously favors doing X)
- Economist can't differentiate cost models (all approaches cost roughly the same)

In these cases, tell the user. Options:
- Reframe the question to expose a real tension
- Drop to 3 agents (cut whichever position is weakest)
- Proceed but warn that the debate may converge quickly
