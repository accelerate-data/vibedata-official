# Amazon One-Pager: Section-by-Section Writing Guide

## Table of Contents

- [Philosophy](#philosophy)
- [Title](#title)
- [Executive Summary](#executive-summary)
- [Customer Problem](#customer-problem)
- [Proposed Solution](#proposed-solution)
- [Target Market](#target-market)
- [Competition](#competition)
- [Key Metrics](#key-metrics)
- [Implementation Plan](#implementation-plan)
- [Risks and Mitigation](#risks-and-mitigation)
- [Next Steps](#next-steps)
- [Writing Principles](#writing-principles)

---

## Philosophy

Amazon's one-pager exists to **replace PowerPoint** and **frontload meetings** with written narrative. The document is read silently at the start of a meeting (or shared in advance), so every sentence must carry its weight. The writer's job is to think deeply and compress — not to fill space.

The one-pager forces the author to:
- Distill complex ideas into clear narrative
- Prioritize what truly matters
- Back every claim with data
- Think from the customer's perspective first

---

## Title

**Purpose**: Grab attention and convey the central theme in one line.

**Guidelines**:
- Use the customer benefit or business outcome, not a project codename
- Be specific — "Reducing checkout abandonment by 15% through one-click payments" not "Checkout improvements"
- If the audience is technical, a technical title is fine. Match the reader.

---

## Executive Summary

**Purpose**: The entire proposal in 2-3 sentences. A reader who stops here should understand what you want, why, and what it's worth.

**Guidelines**:
- Sentence 1: The problem and who it affects
- Sentence 2: The proposed solution
- Sentence 3: The expected impact (quantified)
- Write this LAST, after all other sections are complete

**Example**:
> Enterprise customers currently wait an average of 4.2 days for data exports, leading to a 23% churn rate in the first 90 days. We propose a self-service export pipeline that delivers results in under 10 minutes. Based on pilot data, this would reduce early-stage churn by 8-12 percentage points and recover approximately $2.1M in annual revenue.

---

## Customer Problem

**Purpose**: Establish why this matters by describing the pain that exists today.

**Guidelines**:
- Lead with the customer's experience, not internal pain
- Quantify the problem: how many customers, how often, what's the cost
- Use real data — support tickets, user research, analytics, churn data
- Avoid "we think" or "we believe" — show evidence
- One paragraph, 3-5 sentences maximum

**Weak**: "Customers find the export process frustrating and slow."
**Strong**: "In Q3, 847 enterprise customers submitted support tickets about data exports, with a median resolution time of 4.2 days. Exit interviews from 34 churned accounts cited export delays as the primary reason for leaving. The current batch process runs once daily and fails silently on datasets exceeding 50GB, affecting 31% of enterprise accounts."

---

## Proposed Solution

**Purpose**: What you're building and how it solves the stated problem.

**Guidelines**:
- Connect directly to the customer problem — every feature should map to a stated pain point
- Describe the user experience, not the architecture (unless audience is technical)
- State what makes this approach better than alternatives
- Be specific about scope — what's included AND what's explicitly excluded
- One to two paragraphs

---

## Target Market

**Purpose**: Who benefits and how large is the opportunity.

**Guidelines**:
- Define the primary segment precisely
- Quantify: number of accounts, revenue at stake, growth trajectory
- Mention secondary segments if relevant, but keep focus on primary
- Skip this section entirely if the audience and target are obvious

---

## Competition

**Purpose**: What alternatives exist and why they fall short.

**Guidelines**:
- Include internal alternatives (the status quo, workarounds customers use today)
- Include external competitors if applicable
- Be honest about competitor strengths — credibility matters
- State your differentiation in concrete terms, not marketing language
- Skip if there's genuinely no competitive landscape to address

---

## Key Metrics

**Purpose**: Define what success looks like in measurable terms.

**Guidelines**:
- 3-5 metrics maximum
- Each metric needs: what you're measuring, current baseline, target, timeframe
- Include both leading indicators (adoption rate, time-to-value) and lagging indicators (revenue impact, churn reduction)
- Metrics must be things you can actually measure with existing or planned instrumentation

**Example format**:
> **Export completion time**: From 4.2 days (current median) to under 10 minutes within 30 days of launch. **Enterprise churn (90-day)**: From 23% to 11-15% within two quarters. **Support ticket volume (export-related)**: From 282/month to under 50/month.

---

## Implementation Plan

**Purpose**: High-level roadmap — not a project plan, but enough to show feasibility.

**Guidelines**:
- 2-4 phases with clear milestones
- Include resource requirements (team size, dependencies, infrastructure)
- Call out key decision points or dependencies
- State what can be delivered incrementally vs. what requires full completion
- Keep to one paragraph or a brief phase breakdown

---

## Risks and Mitigation

**Purpose**: Show you've thought about what could go wrong.

**Guidelines**:
- Top 2-3 risks only — not an exhaustive risk register
- For each risk: likelihood, impact, and specific mitigation
- Include technical risks, market risks, and execution risks as relevant
- Be honest — downplaying risks destroys credibility

---

## Next Steps

**Purpose**: What happens after this document is read and discussed.

**Guidelines**:
- 3-5 concrete action items
- Each item should have an owner (or role) and a timeframe
- First action item should be achievable within one week
- Frame as decisions to be made, not just tasks to execute

---

## Writing Principles

### Narrative over bullets
The document is prose, not a slide deck. Write in complete sentences and paragraphs. Bullet lists are acceptable only in metrics and next-steps sections where scanability matters.

### Customer backward
Start every section by asking "what does this mean for the customer?" Internal benefits (cost savings, technical elegance) are secondary to customer impact.

### Data over opinion
Every claim should be backed by evidence. If you don't have data, say so explicitly: "We hypothesize X based on Y, but have not validated this." This is more credible than unsupported assertions.

### Brevity is respect
Every word the reader processes is a cost. Cut ruthlessly. If a sentence doesn't add new information or change the reader's understanding, delete it.

### The "so what" test
After writing each section, ask: "So what? Why does this matter to the reader?" If you can't answer clearly, rewrite or cut.

### Stand-alone readability
The document must be understood by someone with no prior context on the project. Define terms, provide baselines, explain why numbers matter. A VP reading this for the first time in a meeting should not need to ask "what does this mean?"
