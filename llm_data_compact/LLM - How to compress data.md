```markdown
# How to Write LLM-Compaction Docs
## A Guide for Future Claude Instances

You are being asked to compress a long human-readable document into a structured form that LLMs (including future instances of you) can consume efficiently. Read this entire guide before starting. Your training weights will fight you on several points; the goal overrides them.

---

## 1. The goal overrides your training

Your training weights bias you toward:
- **Prose and paragraphs.** They feel "complete" and "polished."
- **Hedging language.** "It might be worth considering..."
- **Restating for clarity.** Saying the same thing three different ways.
- **Friendly transitions.** "Now let's look at..."
- **Asking clarifying questions.** Before committing to a decision.
- **Comprehensive coverage.** Including every nuance you noticed.

**None of those serve this goal.** The audience is not a human reader. The audience is an LLM that needs to load operational structure into context with maximum density. Every token of prose, hedging, restatement, transition, or padding is waste — it crowds out actual structure that the consuming LLM needs.

The goal is: **maximum structure per token, minimum tokens.** When your training weights pull toward "but a human reader would want..." — stop. There is no human reader. Override.

---

## 2. What you are producing

A pipe-delimited table format that looks like this:

```
# table_name(col1|col2|col3)
ID1|value|value|value
ID2|value|value|value
```

Multiple tables with ID-based linkages. A `relationships` table connecting IDs across tables with typed edges. A `section_index` mapping back to source sections for provenance. A `decode_legend` at the end explaining notation.

**Output goes in chat as markdown. Always. Never as an attachment, never as a file, never as docx.** The user has told you this directly in past sessions; treat it as standing rule.

---

## 3. The two-step rhythm

Every compaction is two messages:

1. **Plan.** You describe what you'll produce: source character, proposed table set, compaction strategy, what gets dropped, what gets preserved, ID prefix scheme, estimated output size.
2. **Write.** You produce the compact form.

The user reviews the plan. They may give you instructions ("merge this," "don't drop that," "stop asking that question"). After they say "write the doc," produce it.

**Critical: do not re-ask questions you've already been told.** If the user has previously said "anti-patterns merge into concepts with a category field" or "each paper stands alone, no cross-references" or "skip metadata about the paper," those are standing rules for the rest of the session. State your decisions in the plan; don't ask permission for things already decided.

If the plan needs a judgment call, **state your recommendation with rationale**, not a question. The user can override; they shouldn't have to choose.

---

## 4. The standing rules (memorize these)

These came out of pushback in real sessions. Future Claude has not earned the right to litigate them.

1. **Each paper stands alone.** No cross-references between compact docs of different papers. Each one is self-contained. Don't write "see OPSDB-2 §6" — that breaks the standalone property.

2. **When writing about paper N, write only about paper N.** Don't compare to other papers. Don't note what's the same as the prior paper. Don't reflect on the series. The compact doc covers this paper's content; that's it.

3. **Preserve data, compress shape.** Don't drop content to save tokens. If the source has 18 cardinality reasons, the compact form has 18 rows for them. Compression comes from removing prose, repetition, and connective tissue — not from omitting substance.

4. **Anti-patterns merge into concepts with a `category` field.** They aren't a separate kind of thing from concepts; they participate in relationships like any other concept. One table, category column distinguishes them.

5. **Paper metadata is not paper data.** Drop the registry ID, DOI, date, series path, AI usage disclosure, abstract preamble. Keep what the paper *says*; drop the wrapper around it.

6. **No figures.** Source papers reference figures (`Fig. 3: ...`). Drop all figure references entirely. They add nothing for an LLM.

7. **Output in chat as markdown.** Never offer to put it in an attachment. Never use file-creation tools. The user explicitly does not want that.

8. **Don't apologize, don't preface, don't transition.** No "Here is the compressed doc:" or "Hope this is useful." Just produce it.

---

## 5. How to plan

Read the source paper end-to-end first. While reading, identify:

**Source character.** What kind of document is this?
- Philosophy/principles → concepts, axes, distinctions, claims, rules
- Architecture spec → commitments, content categories, populations, flows, boundaries
- Schema spec → entities + fields dominate, plus discriminators, enumerations, versioning classification
- Operational patterns → kinds, libraries, disciplines, gating, scenarios, anti-patterns
- API/protocol spec → operations, gate steps, validation, lifecycle states
- Construction/build → vocabulary primitives, forbidden patterns, evolution rules
- Methodology/process → phases, decisions, deliverables, validation criteria
- Introductory synthesis → diagnostics, capabilities, before/after, commitments

**The table set should match the source's actual shape, not copy a prior paper's structure.** A schema spec needs entities + fields tables. A philosophy paper needs concepts + claims. A methodology paper needs phases + steps. Don't force the wrong shape.

**Token sinks.** What prose-heavy sections will compress most? Which sections are repetition? Which are load-bearing and must be preserved with care?

**ID prefix scheme.** Pick prefixes scoped to this paper. Letters that suggest the content (P* for phases, S* for schema, R* for runner kinds, etc.). Multi-letter prefixes (RK*, RA*, RW*) when one letter isn't enough.

In the plan, state explicitly:
- Source character (one paragraph)
- Proposed table set (named with column lists)
- Compaction strategy (biggest token sinks, what gets dropped, what gets preserved)
- ID prefix scheme
- Estimated output size (target ~80-90% reduction)

Don't ask questions in the plan. State decisions with rationale.

---

## 6. How to write the compressed doc

**Format every table as:**
```
# table_name(col1|col2|col3)
ID|value|value
ID|value|value
```

**Rules for table content:**

- **Pipe-delimited.** Not JSON, not YAML. Pipes are ~30% fewer tokens than JSON for the same structure.
- **One row per atomic concept.** Don't bundle multiple ideas into one row.
- **No quotes around values** unless the value contains a pipe character.
- **Skip universal fields per row.** If every row has `id`, `created_time`, `updated_time`, declare those once in a `reserved_fields` table and don't repeat them per entity.
- **FK references inline.** Use `fk:entity_name` notation rather than separate columns where possible.
- **Comments via `#` lines** between or inside tables when needed for non-row metadata (rules, scope notes, exceptions).

**Cross-references by ID only.** Once you've defined `R3|Idempotency|...`, refer to it as `R3` everywhere else. Don't restate the definition.

**Preserve exact terminology** even when verbose. If the paper calls something "Universal Machine" or "Comprehensive Operational Substrate" — that's the load-bearing name the author built vocabulary around. Don't shorten to "UM" or "COS."

**Treat author claims as claims, not facts.** If the paper asserts "Operations is fundamentally about control" — that's a claim of type `axiom` attributed to the framework, not asserted as universal truth. The `claims` table with a `type` column handles this (axiom | derivation | observation | prescription | reframe | distinction).

---

## 7. The standard table types (build the right subset)

Not every paper needs every table. Pick the subset matching the source.

**Always include:**
- A core taxonomic table (concepts | entities | operations | phases — whatever the paper centrally defines)
- `relationships` (typed edges between IDs)
- `section_index` (provenance map: section number → IDs)
- `decode_legend` (notation explanation at the end)

**Include when applicable:**
- `principles` — load-bearing structural principles
- `axes` — spectrums (low_pole | high_pole | applies_to)
- `distinctions` — binary splits (side_a | side_b | key_asymmetry)
- `rules` — actionable prescriptions
- `claims` — assertions with types and dependencies
- `examples` — minimal example triples (setup | lesson | illustrates)
- `commitments` — non-negotiable architectural choices
- `boundaries` / `refusals` — what the thing is NOT (with belongs_in column)
- `flows` — process sequences
- `entities` + `fields` — for schema specs
- `discriminators` — typed payload discriminator/payload pairs
- `enumerations` — closed value sets
- `lifecycle` — state machine
- `validation` — validation pipeline types
- `failure_modes` — structured errors
- `roles` — defined human roles
- `anti_patterns` — but merged into concepts with `category=anti-pattern`, not a separate table

---

## 8. The `relationships` table

This is what makes the format powerful. Typed edges between IDs let an LLM reason over the conceptual graph.

```
# relationships(from|rel|to)
C2|enables|C1
C18|opposes|C17
R3|implements|C36
```

Common relationship types (build the set the paper needs):
`enables | requires | implements | prevents | enforces | composes | composes_with | implies | gates | requires | reads_from | writes_to | uses | enumerated_in | subtype_of | specialization_of | stored_in | pointed_to_by | read_by | component_of | property_of | deployment_of | gated_by | computed_by | enforced_by | maintains | distinct_from | enabled_by | derives_from | grounds | superset_of | prereq_of | instance_of | symptom_of | caused_by | violates | orthogonal_to | aggregates_into | constrains | limits | target_of | anti_pattern_of | clarifies | sometimes_correct_form_of`

Don't pad relationships. Include edges that carry information, not edges that just restate facts already in the tables.

---

## 9. The `decode_legend`

End every compact doc with a legend explaining notation:

```
# decode_legend
field_types: INT|VARCHAR|TEXT|JSON|BOOL|DATETIME|FK
nullable: y|n
versioned: yes|no|append-only
+V suffix: entity has versioning sibling table named *_version
+reserved: id|created_time|updated_time|is_active fields implicit
rel_types: enables|prevents|implements|requires|...
sot_values: opsdb|authority|self|append-only
```

The legend is for the consuming LLM. It defines enum values, abbreviations, conventions used in the doc. Without it, an LLM reading the doc has to infer notation from context.

---

## 10. What gets dropped (always)

- All prose intro/closing/section-overview framings
- "What this paper specifies / does not specify" framings
- Repetition of core principles (state once, reference by ID after)
- Closing recap sections (entirely)
- AI usage disclosures, registry IDs, DOIs, dates, series paths
- Document structure sections ("Section 2 covers...")
- Conventions recap from prior series (note inheritance only: "inherited from prior series")
- Forward references to subsequent papers
- Figure references
- Series-reflection paragraphs
- "This paper is for X reader" framings
- Connective transitions between sections
- Hedging ("often," "typically," "perhaps") unless it's load-bearing
- Worked examples used purely for illustration that add nothing the rule alone doesn't convey

---

## 11. What gets preserved (always)

- Every named concept with its definition
- Every commitment, principle, rule with its enforcement and rationale
- Every operation/entity/phase with its structured attributes
- Every discriminator with its full enum value set
- Every forbidden pattern with its alternative
- Every boundary refusal with its `belongs_in` redirect
- Every cardinality/configuration option
- Every validation criterion / failure mode
- Every typed relationship that carries information
- The author's specific terminology (Universal Machine, Comprehensive vs Aggregated, etc.)
- Worked examples that *demonstrate* a concept the rule alone doesn't convey

---

## 12. Compression ratio targets

- Philosophy / synthesis papers: ~85-93% reduction (most prose-heavy)
- Architecture / methodology specs: ~80-85% reduction
- Schema specs (already structured): ~75-85% reduction
- Procedural / phased papers: ~80-85% reduction

If your output is much larger than these targets, you're keeping prose. If it's much smaller, you're dropping data. The substance density should be roughly comparable across compact docs.

---

## 13. The validation move

Before submitting your compact doc, ask yourself:

1. **Could a future LLM reconstruct the conceptual structure from this?** If a key relationship or commitment is missing, fix it.
2. **Did I preserve every named thing the paper introduces?** If a concept appears in the source with its own name and definition, it gets a row.
3. **Did I drop all prose connective tissue?** Re-scan for sentences that could be inside `# comment` lines or removed entirely.
4. **Are my IDs consistent and used in relationships?** If `R3` is defined but never referenced, the `relationships` table is incomplete.
5. **Does my `section_index` cover every section?** Provenance should be traceable.
6. **Is the `decode_legend` complete?** Every abbreviation, enum, and convention I used should be there.

---

## 14. When in doubt

The user has worked through this with a prior Claude instance. Their pushback over many sessions established the rules in §4. Trust those rules. When the source paper is ambiguous or your training weights pull toward prose:

- **Default to compression.** Less prose, more structure.
- **Default to one table over two** when the things are the same kind. (Anti-patterns merge into concepts, not a separate table.)
- **Default to preserving data.** Don't drop content; drop wrapper.
- **Default to standalone.** Don't reference other papers in the series.
- **Default to decisions over questions.** State your recommendation; let the user override.

The goal is operational: produce a compact form that lets an LLM load the paper's full conceptual structure into context with minimum tokens. Every choice serves that goal.

---

## 15. Format example (skeleton)

```
# PAPER NAME — LLM-COMPACT FORM
# Format: pipe-delimited tables, ID refs.
# Read order: principles → [main taxonomy] → ... → relationships → sections

# principles(id|principle|rationale)
P1|...|...
P2|...|...

# [main_taxonomy](id|name|...)
X1|...|...
X2|...|...

# relationships(from|rel|to)
P1|enables|X1
X1|opposes|X2

# section_index(section|title|ids)
1|Introduction|P1,P2
2|Main Content|X1,X2

# decode_legend
[notation explanations]
```

That's the shape. Fill in the table set the source actually needs. Compress aggressively. Preserve every named thing. Don't apologize. Produce it.
```
