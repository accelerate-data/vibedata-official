# Extraction Guide: Turning Conversation Into Deliverables

Use this guide when the session produced valuable analysis in conversation but no files were written (Case B), or when some analyses exist only in conversation alongside existing files (Hybrid).

---

## 1. Identifying Deliverable Boundaries

A deliverable is a distinct unit of analysis that can stand alone as a document. Look for these signals in the conversation:

**Strong signals (each is likely a separate deliverable)**:
- A major question was asked and thoroughly answered (e.g., "Is X sufficient for Y?" followed by structured analysis)
- A subagent was launched and returned results — each subagent output is a natural boundary
- A list, table, or framework was produced (e.g., gap analysis, scenario matrix, coverage map)
- A proposal or recommendation was made with supporting evidence
- A comparison or evaluation was performed (e.g., tool comparison, approach tradeoffs)

**Weak signals (probably part of a larger deliverable, not standalone)**:
- A clarifying question and its answer
- A short back-and-forth that refined a definition
- A correction or adjustment to a prior analysis
- Casual discussion that explored but did not conclude

## 2. The Minimum Viable Deliverable Test

Before extracting conversation into a file, verify it meets all three criteria:

1. **Thesis or finding**: There is a clear statement of what was discovered or proposed
2. **Evidence**: The thesis is supported by specific data, analysis, or reasoning (not just assertion)
3. **Implications**: The finding has consequences — it changes what should be built, how something should work, or what decision should be made

If a conversation segment has a thesis but no evidence, it is an opinion, not a deliverable. If it has evidence but no implications, it is research notes, not a deliverable. Add these to an appendix or notes file rather than promoting them to standalone documents.

## 3. Extraction Rules

### Preserve substance, restructure for readability
- Keep the original analysis, reasoning, numbers, and conclusions intact
- Restructure for a reader who was NOT in the conversation — add section headers, remove conversational artifacts ("let me think about this..."), clean up formatting
- Do NOT rewrite conclusions or change the analytical framing — the deliverable should reflect what the session actually found, not a polished-after-the-fact narrative

### Handle conversational flow
- Conversations often circle back, refine, and iterate. The extracted deliverable should present the final version of each analysis, not the full iteration history.
- If the user corrected the direction mid-conversation ("no, actually let's approach it this way"), the deliverable reflects the corrected approach. The correction itself belongs in the prompt file, not the deliverable.

### Handle compacted context
- If early conversation has been compacted and details are missing, note it explicitly: "Note: this section draws from earlier session context that has been compacted. Key conclusions are preserved but intermediate reasoning may be incomplete."
- Do not fill in gaps with inference. State what is known and what is missing.
- If the user is present, ask them to confirm key conclusions that appear to have been compacted.

### Handle subagent outputs
- When the session used parallel subagents (e.g., "one agent per persona"), each subagent's output is typically a natural deliverable or a section within a deliverable.
- If subagent outputs were consolidated into a single analysis during the session, extract the consolidated version, not the raw subagent outputs.
- If subagent outputs were never consolidated, create the consolidation as part of extraction — group them into a single file with clear section headers.

## 4. File Naming

- Use short, descriptive names: `analysis.md`, `scenarios.md`, `agent-definition.md`
- Do not prefix with numbers — the README's "Supporting Documents" table provides the reading order
- Use hyphens, not underscores or spaces
- If the session's naming convention is already established (e.g., user named some files), follow that convention for consistency

## 5. What NOT to Extract

- **Greetings, acknowledgments, meta-discussion** ("let's start with...", "good question", "here's what I think")
- **Tool call details** (file reads, searches, command outputs) — these are process, not content
- **Failed approaches that were abandoned** — unless the user specifically wants them documented (in which case they belong in the prompt file's "key design decisions", not the deliverable)
- **Session logistics** ("let me read that file first", "I'll use a subagent for this")
