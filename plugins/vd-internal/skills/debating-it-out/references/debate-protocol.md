# Debate Protocol

Rules for the live challenge/defense exchange in Round 2. All debate agents
must follow these rules. The team lead enforces them.

---

## Challenge Format

Each challenge is a **separate SendMessage** to a specific opponent. Do not
combine challenges to multiple opponents in one message.

**Length**: 200-300 words per challenge. You send 3 challenges (one per
opponent), so total output is 600-900 words.

**Structure**:

1. **Quote a specific claim** from the opponent's position paper. Use their
   exact words or a close paraphrase with the section reference.

2. **Explain why it's wrong or incomplete.** Use reference case details —
   not abstract objections. Show the specific mechanism that breaks, the
   cost they missed, the case detail they glossed over.

3. **End with a pointed question** the opponent must address in their
   defense. The question should be specific enough that a non-answer is
   obvious. Not "what about costs?" but "your cost model assumes X, but
   Case 2 shows Y — how do you reconcile this?"

**Example skeleton**:
```
You claim "[exact quote from their paper]" in your section on [topic].

This breaks down when applied to [Reference Case]. Specifically, [detail
from the case] means that [mechanism of failure]. The research in [doc]
actually shows [counter-evidence].

How do you account for [specific gap] given that [Case detail]?
```

---

## Defense Format

Each defense is a **separate SendMessage** back to the specific challenger.
Do not combine defenses to multiple challengers in one message.

**Length**: 200-300 words per defense. You send 3 defenses (one per
challenger), so total output is 600-900 words.

**Structure**:

1. **Acknowledge the specific challenge.** Restate what the challenger
   claims is wrong. Don't strawman — show you understood their point.

2. **Address the pointed question directly.** Answer it. If you can't
   answer it, concede the point and explain what it means for your position.
   Dodging is worse than conceding.

3. **Provide counter-evidence or concede.** Use reference case details to
   defend your claim, or concede that the challenger found a real weakness.
   Partial concessions are fine: "You're right about Case 1, but Case 2
   still supports my argument because [specific detail]."

4. **End with a "nevertheless" statement** that preserves your core
   position. Even if you concede a point, explain why your overall argument
   still holds. This prevents total capitulation while showing intellectual
   honesty.

**Example skeleton**:
```
You challenge my claim that [restate their challenge accurately].

To your specific question about [the pointed question]: [direct answer].
In Case 2, [specific detail] shows that [defense]. However, I concede
that for Case 1, [concession].

Nevertheless, my core argument holds because [preserved position with
any necessary refinements].
```

---

## Tone Rules

1. **Attack arguments, not agents.** "Your claim about X fails because..."
   not "You clearly don't understand..."

2. **Specific over general.** "Case 2's migration timeline of 6 months
   contradicts your 2-week estimate" not "your timeline is unrealistic."

3. **Evidence over assertion.** Every challenge and defense must reference
   either a position paper claim, a reference case detail, or a research
   finding. Opinion alone is not enough.

4. **No "I agree with everything."** Find something to fight about. If you
   genuinely agree with an opponent on a thread, explain WHY their framing
   is still wrong or incomplete even if the conclusion is similar.

5. **Concede when caught.** If a challenger surfaces a real flaw, own it.
   "You're right, my cost estimate didn't account for [X]" is stronger than
   pretending the challenge doesn't land.

---

## Anti-Patterns

These will be flagged by the team lead and the agent will be asked to redo:

1. **Filibustering** — Long, vague responses that avoid engaging with the
   specific challenge. If you're writing more than 300 words and haven't
   addressed the pointed question, you're filibustering.

2. **Introducing entirely new arguments** — Challenges must engage with
   Round 1 content. You are challenging what opponents WROTE, not launching
   a new argument they've never seen. Save new arguments for the rebuttal.

3. **Restating your position paper** — The team has already read it. Every
   word should be about your OPPONENT's argument, not yours.

4. **Combining opponents** — Each challenge/defense targets ONE opponent.
   "Both Agent A and Agent B fail to..." is not allowed. Write separate
   messages.

5. **Ignoring the question** — If a challenge ends with a pointed question,
   the defense must answer it. "That's an interesting point but..." followed
   by a pivot is an anti-pattern.

6. **False concessions** — "I concede that you raise a valid point" without
   specifying what the point is or what it means for your position. A real
   concession changes something about your argument.

---

## Per-Message Discipline

- One SendMessage = one challenge to one opponent OR one defense to one
  challenger.
- Address the recipient by role name in the message.
- Keep within the 200-300 word limit. The team lead receives all messages
  and will flag violations.
- Do not send follow-up messages or rebuttals to defenses. The exchange
  is bounded: challenge → defense → done. Save further arguments for the
  written rebuttal.
