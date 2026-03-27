---
name: debating-it-out
description: Orchestrates a structured multi-agent adversarial debate on any strategic question. Four agents (Maximalist, Purist, Hybrid, Economist) write position papers, debate through rebuttals, and produce a synthesized recommendation. Activates when the user wants to analyze a strategic decision from multiple angles, run a red team analysis, or get a rigorous recommendation on any topic where reasonable people disagree. Triggers on debate, adversarial analysis, red team, argue both sides, tradeoffs, position paper, devil's advocate, or help me think through / decide on a topic with genuine tension.
tools: Read, Write, Glob, Bash, Agent, TeamCreate, SendMessage, AskUserQuestion
---

# Debate It Out

Structured adversarial analysis: 4 agents debate a strategic question, then
synthesis produces a decision framework with concrete recommendations.

## Why This Exists

Single-perspective analysis misses blind spots. This skill forces genuine
intellectual tension by assigning agents positions they must defend with
evidence and reference cases. The rebuttal round forces engagement with
opposing arguments. Synthesis preserves disagreement where it exists rather
than averaging into mush.

## The Four Agents

| Agent | Role | What They Defend |
|-------|------|-----------------|
| **Maximalist** | Go all in | "Do X fully, invest heavily, maximize coverage" |
| **Purist** | Reject / status quo | "X is a trap — don't do it, here's why" |
| **Hybrid** | Middle path | "Do X structurally, not substantively" |
| **Economist** | ROI arbiter | "Here's what the numbers actually say" |

Maximalist vs. Purist is the core axis. Hybrid triangulates. Economist
stress-tests all three. This works because most strategic decisions decompose
into "do more / do less / do differently / what does it cost."

## Orchestration — 7 Phases

```
Phase 0  Intake ─────────────────────── collect inputs
Phase 1  Research Ingestion ─────────── read & map tensions
Phase 2  Mandate Generation ─────────── HUMAN GATE (confirm positions)
Phase 3  Round 1: Position Papers ───── 4 parallel agents
Phase 4  Debate Thread Extraction ───── HUMAN GATE (prune threads)
Phase 5  Round 2: Live Debate + Rebuttals  (team-based)
         5a: Team creation & agent spawning
         5b: Challenge exchange (12 DMs)
         5c: Defense exchange (12 DMs)
         5d: Rebuttal writing (4 files)
Phase 6  Synthesis ──────────────────── main agent
Phase 7  Consolidation ─────────────── single doc output
```

Copy this checklist and update as you progress:

```
Debate Progress:
- [ ] Phase 0: Intake — collected framing question, research docs, reference cases
- [ ] Phase 1: Research ingestion — read all docs, built tension map
- [ ] Phase 2: Mandate generation — presented 4 mandates, user approved
- [ ] Phase 3: Round 1 — spawned 4 position paper agents, verified outputs
- [ ] Phase 4: Debate threads — extracted threads, user approved subset
- [ ] Phase 5a: Created debate team, spawned 4 fresh agents with debate protocol
- [ ] Phase 5b: Challenge exchange — 12 challenges sent (each agent → 3 opponents)
- [ ] Phase 5c: Defense exchange — 12 defenses sent (each agent → 3 challengers)
- [ ] Phase 5d: Rebuttal writing — all 4 agents wrote final rebuttals
- [ ] Phase 6: Synthesis — shut down team, wrote synthesis.md
- [ ] Phase 7: Consolidation — wrote consolidated_analysis.md, presented to user
```

---

### Phase 0: Intake

Collect from the user (extract from conversation if already provided, otherwise
use AskUserQuestion for missing pieces):

1. **Framing question** — Single sentence stating the decision.
   Example: "Should Vibedata pre-seed domain skills or build per customer?"

2. **Research documents** — File paths to background material. Minimum 1.

3. **Reference cases** — Minimum 2 concrete examples. Each needs:
   - **Name**: Short label (e.g., "Customer Alpha")
   - **Context**: 1-2 sentences (industry, system, use case)
   - **Specifics**: Domain-relevant details agents need for reasoning

4. **Constraints** (optional) — Scoping like "focus on cost," "6-month horizon."

**Validation**: Research docs must exist and be readable. Reference cases must
have enough detail for concrete reasoning — if too thin, push back before
proceeding. Thin cases produce abstract arguments, which defeats the purpose.

---

### Phase 1: Research Ingestion

Read all research documents yourself (main agent). Do NOT delegate — you need
full context to generate good mandates in Phase 2.

Build an internal tension map as you read:
- Key disagreements and tradeoffs
- Claims with evidence vs. unsupported assertions
- Value tensions (speed vs. quality, cost vs. coverage)
- Open questions the research leaves unresolved

Do not output the tension map. It feeds Phase 2.

---

### Phase 2: Mandate Generation → HUMAN GATE

Read `references/position-discovery.md` for mandate generation guidance.

For each of the 4 agents, generate a mandate paragraph (3-5 sentences):
- What specific position this agent defends on THIS topic
- What sub-questions they must address
- How they must use the reference cases
- What research arguments they should engage with

Present all 4 mandates to the user via AskUserQuestion:
- "Here are the 4 debate positions. Approve, edit, or flag overlaps?"

If the tension map doesn't support 4 genuinely distinct positions, say so:
"This topic may not have enough disagreement for 4 agents. [Maximalist and
Hybrid overlap because...]. Want to proceed, reframe, or drop to 3?"

---

### Phase 3: Round 1 — Position Papers

Read `references/position-paper-template.md` to construct agent prompts.

**Workspace setup** — Create the output directory. Default location:
`{research-docs-parent}/debate-workspace/`. Confirm with user.

```
{workspace}/
├── round1/
└── round2/
```

**Spawn 4 Task subagents in a single message** (parallel). Each gets:
- Research document file paths (agent reads them itself)
- Its mandate from Phase 2
- All reference cases with full details
- User constraints (if any)
- Word limit: 2000
- Output path: `{workspace}/round1/position_{role}.md`
  where role is: maximalist, purist, hybrid, economist

After all 4 complete, verify all position papers exist and are non-empty.
If a subagent fails, retry once. If still fails, continue with remaining agents.

---

### Phase 4: Debate Thread Extraction → HUMAN GATE

Read all 4 position papers yourself.

Extract 5-8 specific debate threads. A thread is a concrete disagreement,
not a vague topic. Format:

```
Thread N: "[Short label]"
  - Maximalist says: [specific claim]
  - Purist says: [specific counterclaim]
  - Evidence status: [what would resolve this]
```

Not every thread needs all 4 agents. Some are between 2.

Present threads to user via AskUserQuestion (multi-select to deselect).
This gate prunes the debate to what the user actually cares about.

---

### Phase 5: Round 2 — Live Debate + Rebuttals

This phase uses **TeamCreate + Agent + SendMessage** instead of isolated Task
subagents. Fresh agents debate each other directly before writing rebuttals.

Read `references/debate-protocol.md` before constructing agent prompts.
Read `references/rebuttal-template.md` for the rebuttal writing phase.

#### Phase 5a: Team Creation & Agent Spawning

1. Create the debate team:
   ```
   TeamCreate { team_name: "debate-{topic-slug}" }
   ```

2. Spawn 4 Agents in a single message, each with `team_name` and `name`:
   ```
   Agent { team_name: "debate-{slug}", name: "maximalist", prompt: "..." }
   Agent { team_name: "debate-{slug}", name: "purist", prompt: "..." }
   Agent { team_name: "debate-{slug}", name: "hybrid", prompt: "..." }
   Agent { team_name: "debate-{slug}", name: "economist", prompt: "..." }
   ```

3. Each agent's spawn prompt includes:
   - Its mandate from Phase 2
   - Approved debate threads from Phase 4
   - All 4 position paper file paths (agent reads them itself)
   - All reference cases with full details
   - The debate protocol rules (from `references/debate-protocol.md`)
   - Initial instruction: "Read all 4 position papers. Then challenge all 3
     opponents — send a separate 200-300 word DM to each via SendMessage.
     Follow the debate protocol."

**Why fresh agents?** An agent that *wrote* a position paper is invested in
defending it. Fresh agents read all 4 papers with clean eyes and engage more
critically. They know the mandate and the position, but they didn't spend
tokens constructing the argument.

#### Phase 5b: Challenge Exchange (12 DMs)

Each agent wakes up, reads all 4 position papers, and sends 3 challenges
(one per opponent) via SendMessage in a single turn.

```
maximalist ──DM──> purist, hybrid, economist    (3 msgs)
purist     ──DM──> maximalist, hybrid, economist (3 msgs)
hybrid     ──DM──> maximalist, purist, economist (3 msgs)
economist  ──DM──> maximalist, purist, hybrid    (3 msgs)
```

**Total**: 12 SendMessage calls. Each challenge is 200-300 words following
the debate protocol format: quote a specific claim, explain why it's wrong
using reference case details, end with a pointed question.

Wait until all 4 agents are idle (all 12 challenges sent). The team lead
receives peer DM summaries via idle notifications.

#### Phase 5c: Defense Exchange (4 + 12 DMs)

Team lead sends 4 prompts via SendMessage:
```
SendMessage { to: "maximalist", message: "You've received 3 challenges.
  Respond to each challenger with a separate 200-300 word defense DM.
  Follow the debate protocol defense format." }
(repeat for purist, hybrid, economist)
```

Each agent wakes up (has all 3 challenges in context from 5b), sends 3
defenses (one per challenger) via SendMessage:

```
maximalist ──DM──> purist, hybrid, economist    (3 defenses)
purist     ──DM──> maximalist, hybrid, economist (3 defenses)
hybrid     ──DM──> maximalist, purist, economist (3 defenses)
economist  ──DM──> maximalist, purist, hybrid    (3 defenses)
```

**Total**: 4 lead prompts + 12 defense DMs = 16 SendMessage calls.
Wait until all 4 agents are idle (all 12 defenses sent).

#### Phase 5d: Rebuttal Writing (4 DMs → 4 files)

Team lead sends 4 prompts via SendMessage:
```
SendMessage { to: "maximalist", message: "Write your final rebuttal
  incorporating the live debate. Follow the rebuttal template structure
  (references/rebuttal-template.md). Write to
  {workspace}/round2/rebuttal_maximalist.md. Keep under 1500 words." }
(repeat for purist, hybrid, economist)
```

Each agent writes its rebuttal file, incorporating the challenges and
defenses from the live exchange. The rebuttal template requires:
- Direct engagement with opponents on approved threads
- Live debate integration (quote/reference the challenge/defense exchange)
- At least 2 concessions reflecting what was learned in the live debate
- Reference case attacks using opponent analysis against them
- Revised position absorbing valid critiques

After all 4 agents complete, verify all rebuttals exist:
- `{workspace}/round2/rebuttal_maximalist.md`
- `{workspace}/round2/rebuttal_purist.md`
- `{workspace}/round2/rebuttal_hybrid.md`
- `{workspace}/round2/rebuttal_economist.md`

**Phase 5 message flow summary**:
```
5a:  (4 agents spawn, begin reading papers)
5b:  12 challenge DMs (3 per agent)
5c:   4 lead prompts + 12 defense DMs
5d:   4 lead prompts → 4 rebuttal files written
      ─────────────────────────────────
      Total: 32 SendMessage calls, 0 broadcasts
```

---

### Phase 6: Synthesis

**First**: Shut down all 4 debate agents. The team is no longer needed —
all rebuttals are written and the debate exchange context is in your
idle notifications. Do not leave orphaned agents running.

Read `references/synthesis-template.md` for structure and rules.

Do this yourself (main agent). You have full context: the original question,
reference cases, approved threads, why the user pruned certain threads,
AND the debate exchange summaries from Phase 5b/5c idle notifications.

Read all 8 documents (4 positions + 4 rebuttals). Produce:

1. **Debate arc (with exchange highlights)** — Where each agent started vs. ended,
   plus a ~500 word sub-section highlighting key moments from the live debate
2. **Convergence map** — What all agents agreed on
3. **Residual disagreements** — What's unresolved, why
4. **Decision framework** — Economist's revised rubric + evidence from debate
5. **Reference case application** — Framework applied to each case
6. **Recommendations** — Categorized: what to do fully, what to do partially,
   what to avoid, what needs more data
7. **Prioritized action list**

**Anti-flattening rule**: For each recommendation, state which agents agree,
which disagree, and what evidence would resolve the disagreement.

Write to `{workspace}/synthesis.md`.

---

### Phase 7: Consolidation

Read `references/consolidation-format.md` for document layout.

Write `{workspace}/consolidated_analysis.md` as a lightweight wrapper:
- Executive summary (~500 words, new writing distilled from synthesis)
- Table of contents with relative links to all workspace files

Do not copy position papers, rebuttals, or synthesis inline — they live in
their own files. The consolidated doc is a navigation layer, not a duplicate.

Present to the user:
- `consolidated_analysis.md` — executive summary + links for reading/sharing
- `{workspace}/` directory — full debate record

---

## Handling Large Research Corpora

If total research material exceeds ~50 pages, subagents may struggle to
ingest everything. Strategy:
1. Produce a structured summary of each doc (~500 words) during Phase 1
2. Give subagents both summaries and original file paths
3. Instruct agents: read summaries first, consult originals for specific claims

---

## Reference Files

| File | Read When | Purpose |
|------|-----------|---------|
| `references/position-discovery.md` | Phase 2 | Mandate generation from tensions |
| `references/position-paper-template.md` | Phase 3 | Parameterized prompt for position agents |
| `references/debate-protocol.md` | Phase 5a | Challenge/defense format, tone rules, anti-patterns |
| `references/rebuttal-template.md` | Phase 5d | Parameterized prompt for rebuttal writing |
| `references/synthesis-template.md` | Phase 6 | Synthesis structure, exchange highlights, anti-flattening |
| `references/consolidation-format.md` | Phase 7 | Consolidated document layout (incl. section 2.5) |
