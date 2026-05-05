# OPSDB SCHEMA CONSTRUCTION — LLM-COMPACT FORM
# Format: pipe-delimited tables, ID refs.
# Read order: principles → repo-layout → directory-yaml → entity-file → vocab-types → vocab-modifiers → vocab-constraints → forbidden-in-files → json-vocab → json-pattern → cross-field-split → meta-schema → bootstrap → evolution-allowed → evolution-forbidden → type-change → change-application → reconciliation → portability → ddl-mapping → engine-degradation → design-refusals → worked-examples → relationships → sections

# principles(id|principle|rationale)
SC1|Schema is data not code|hierarchical YAML/JSON files in git repo; loader produces both DB structure and API validation metadata from same source
SC2|Single source of truth for schema and validation|conventional approach has DDL+validation-code as two stores that drift; this paper unifies them
SC3|Closed constraint vocabulary|9 types + 3 modifiers + 6 constraints = 18 primitives; adding a primitive is paper revision not user-extensible
SC4|No embedded logic|no expressions+formulas+function calls+conditionals in schema files; loader parses validates applies; never evaluates
SC5|No regex|known DoS vector (catastrophic backtracking)+dialect variation+unpredictable edge cases+adds embedded mini-language
SC6|Repository creates OpsDB initially|loader reads files+generates engine-DDL+populates _schema_* tables; nothing about bootstrap requires running OpsDB to bootstrap one
SC7|Schema evolution governed|changes flow through _schema_change_set with stricter approval rules; specialized executor applies
SC8|Repo and OpsDB stay synchronized by construction|executor is only path to schema changes; reads repo intent + applies to OpsDB; schema_versions match
SC9|Storage engine portable|schema declarations engine-independent; loader generates engine-appropriate DDL; primitives map to standard SQL features
SC10|API stays simple by refusing what doesn't belong|each refusal closes off complexity that would propagate into every consumer
SC11|Discipline costs schema gymnastics buys decade-scale stability|absolute rules enable simple consumers; partial enforcement is worse than full

# repo_layout(directory|purpose|notes)
SR1|opsdb-schema/|root|conventionally named; normal git repo with PR/review/branch-protection/merge discipline
SR2|directory.yaml|master manifest at root|the one authoritative list of imports in dependency order
SR3|conventions/|reserved fields universal across schema|conventions/reserved.yaml declares id+created_time+updated_time+parent_id+is_active+governance fields available
SR4|meta/|the meta-schema|meta/_schema_meta.yaml describes valid schema files; loaded first
SR5|identity/|domain dir|ops_user+ops_group+ops_user_role+memberships
SR6|site/|domain dir|site+location
SR7|substrate/|domain dir|hardware+megavisor+platform+machine
SR8|cloud/|domain dir|cloud_provider+cloud_account+cloud_resource+storage_resource+cloud_resource_types/ subdir per type
SR9|k8s/|domain dir|cluster+namespace+workload+pod+helm+configmap+secret_reference+service
SR10|service/|domain dir|package+service+host_group+site_location+service_level
SR11|authority/|domain dir|authority+authority_pointer+per-entity bridges
SR12|schedule/|domain dir|schedule+schedule_version+target bridges+manual_operation
SR13|policy/|domain dir|policy+security_zone+data_classification+retention_policy+escalation+compliance+target bridges
SR14|documentation/|domain dir|runbook_reference+dashboard_reference+ownership+stakeholder bridges
SR15|runner/|domain dir|runner_spec+capability+machine+instance+job+output_var+target bridges+report_key
SR16|monitoring/|domain dir|monitor+target bridges+prometheus_config+monitor_level+alert+on_call_schedule
SR17|observation/|domain dir|observation_cache_metric+state+config
SR18|configuration/|domain dir|configuration_variable+version
SR19|change_management/|domain dir|change_set+field_change+approval_required+approval+rejection+validation+emergency_review+bulk_membership
SR20|audit/|domain dir|audit_log_entry
SR21|evidence/|domain dir|evidence_record+target bridges+compliance_finding
SR22|schema_metadata/|domain dir|_schema_version+_schema_change_set+_schema_entity_type+_schema_field+_schema_relationship
# rule: directory layout is structural advice for human readers; loader does not infer dependencies from structure; all dependencies declared in directory.yaml
# rule: one file per entity type; bridge tables with substantive fields get own file; bridges with only reserved+FKs may nest in parent's file
# rule: versioning siblings (*_version) NOT separate files; declared as versioned:true on parent; loader generates sibling structure

# directory_yaml(aspect|content|enforcement)
SD1|schema_version field|canonical version of schema as a whole|increments per _schema_change_set apply; format YYYY.MM.DD.NN convention; stored in _schema_version.version_label on apply
SD2|meta list|loaded first|meta-schema describes file format every other file must conform to
SD3|conventions list|loaded second|reserved.yaml declares fields other entity files reference by name
SD4|imports list|entity files in dependency order|each declares one entity OR inline bridge nestings
SD5|explicit ordering not inferred|loader processes in listed order|earlier files cannot reference entities defined in later files
SD6|unresolved reference rejected|loader fails fast with structured error|points at the unresolved reference
SD7|inferring dependencies forbidden|topological sort + cycle detection + edge cases = logic|listing order is data deterministic inspectable
SD8|directory.yaml does NOT contain|field declarations+entity declarations+constraint specs|those live in per-entity files; directory is manifest not schema
SD9|directory.yaml does NOT support|conditional imports+environment-specific imports+per-deployment customization|schema is one schema; deployment varies through OpsDB runtime config not loaded schemas
SD10|directory.yaml maintenance cost|authors maintain when adding entities|benefit: import graph explicit; reading directory.yaml shows schema structure at a glance

# entity_file(field|required|type|purpose)
SE1|entity_type|yes|string DSNC-compliant|table name; must match file name modulo extension
SE2|description|yes|prose|what entity represents and how it fits operational model
SE3|table_category|yes|enum|change_managed|observation_only|append_only|computed
SE4|versioned|yes|boolean|if true loader generates *_version sibling table
SE5|soft_delete|yes|boolean|if true entity uses _delete/_delete_time/_delete_user_id reserved fields
SE6|reserved_fields_apply|yes|list of names|reserved field names this entity opts into; references conventions/reserved.yaml
SE7|fields|yes|list|operational fields with type+constraints
SE8|governance_fields|optional|list|underscore-prefixed governance fields; structurally identical to fields; visual split for clarity
SE9|indexes|optional but encouraged|list|fields covered+unique flag+description; required not optional; engine cannot serve schema if cannot honor index
SE10|approval_rules|optional|list of policy names|references approval_rule policies; loader validates real policy exists
SE11|introduced_in_schema_version|yes|version label|set on initial declaration; never changes
SE12|deprecated_in_schema_version|yes (nullable)|version label or null|set when deprecated; even deprecated entities not deleted
SE13|notes|optional|prose|design rationale+context for human readers; not consumed by loader
# field declaration shape: name+type+nullable+description+type-specific-constraint-properties; flat structure no nested expressions no conditionals no formulas
# governance_fields treated identically to fields by loader; both produce columns + _schema_field rows

# vocab_types(id|type|description|constraint_props|notes)
SV_T1|int|signed integer|min_value+max_value (inclusive)|without bounds engine native integer range applies
SV_T2|float|floating-point number|min_value+max_value+precision_decimal_places|values with more precision rejected at gate
SV_T3|varchar|bounded-length character string|max_length REQUIRED+min_length (default 0)|character-counted not byte-counted when engine and encoding allow
SV_T4|text|long string|max_length optional bounded by engine|for prose where small bound artificially restrictive
SV_T5|boolean|true or false|none beyond nullability|
SV_T6|datetime|high-precision timestamp|none|engine native datetime; precision typically microsecond
SV_T7|date|date without time|none|
SV_T8|json|typed payload|json_type_discriminator REQUIRED|references field whose value selects registered JSON schema; recursive validation §json_vocab
SV_T9|enum|closed set of allowed values|enum_values REQUIRED|values typically strings; engine may use enum types or VARCHAR+CHECK
SV_T10|foreign_key|reference to id field of another entity|references REQUIRED|FK to target's id only; references to other fields not supported

# vocab_modifiers(id|modifier|applies_to|semantics)
SV_M1|nullable|all types|true or false; defaults false; explicit declaration encouraged for clarity
SV_M2|default|int|float|boolean|enum|date|varchar|text|literal value only; computed defaults forbidden; not for foreign_key+datetime+json
SV_M3|unique|all types|true or false; field's values unique across all rows; composite uniqueness via indexes list with unique:true

# vocab_constraints(id|constraint|applies_to|semantics)
SV_C1|min_value|int|float|inclusive numeric lower bound
SV_C2|max_value|int|float|inclusive numeric upper bound
SV_C3|min_length|varchar|text|character length lower bound
SV_C4|max_length|varchar|text|character length upper bound; required for varchar
SV_C5|enum_values|enum|closed list of permitted values
SV_C6|references|foreign_key|target entity name; FK to id field of target
SV_C7|precision_decimal_places|float|maximum number of decimal places
SV_C8|must_be_unique_within|composite uniqueness scope|list of field names defining scope; loader generates composite unique index
# total: 9 types + 3 modifiers + 6 constraints = 18 primitives (constraint count includes precision_decimal_places + must_be_unique_within in addition to 6 listed above as core; total expressive primitives)
# adding a primitive is revision of this paper not user-extensible

# forbidden_in_files(id|refusal|reason|alternative)
SF1|No regex|DoS vector via catastrophic backtracking + dialect variation + unpredictable edge cases + adds embedded mini-language|enum sets for closed alternatives + length bounds + prefix/suffix expressed as enum-of-prefixes; richer matching at API semantic-validation step
SF2|No embedded logic|expressions+formulas+function calls beyond comparison-via-bounds|every value in schema file is literal; loader does not evaluate; defaults are literals only (no now()+no previous_value+1)
SF3|No conditional constraints|cross-field invariants like "if status=active then running_since non-null" not in schema|belong at API semantic-validation step (§cross-field) named in policy data
SF4|No inheritance|no extends directive+no parent entity+no shared base class|two entities with similar fields each declare independently; reserved fields exception controlled (opt-in named expansion no customization)
SF5|No templating|no template variables+no parameterized files+no macros+no per-deployment substitution|variation across environments via OpsDB runtime config not different schemas; one schema per OpsDB
SF6|No imports within entity files|entity files do not import other files|only directory.yaml imports; entity files are leaf-level data
SF7|No deletions of fields/entities|deletion breaks history (version rows+audit log+versioning); forces executor to rewrite history (forbidden) or refuse|deprecate (mark _schema_field deprecated); column remains; data remains queryable; tombstone forever
SF8|No renames|renames break every consumer (runners by field name+audit log+version history)|add new field with new name + deprecate old (§type_change duplication pattern)
# why each refusal matters: closes off category of complexity that would propagate into every consumer; API would have to evaluate+support+process+expand; reviewer+steward would have to govern; refusing keeps schema simple+loader mechanical+API bound-validation-step a lookup

# json_vocab(id|type|properties|bounded_by)
SJ1|list|ordered list|element_type REQUIRED+element-prefixed constraints (element_min_value+element_max_length etc)+min_count+max_count|every list has max count; every element has its own bounds
SJ2|map|key-value map|key_type+value_type with respective constraints+max_entries|every map has max_entries; keys and values have bounds
# JSON-context vocabulary additions only used in JSON payload schemas; same closed vocabulary plus these two collection types
# all other primitives reused from main vocabulary applied recursively to bounded depth

# json_pattern(aspect|content)
SJP1|discriminator declaration|json field declares json_type_discriminator naming field whose value selects validation schema
SJP2|payload schema files|loader expects payload schema at conventional path (e.g. cloud/cloud_resource_types/<type_value>.yaml)
SJP3|payload schema file shape|discriminator_field+discriminator_value+description+json_schema with fields list
SJP4|recursion depth limit|JSON payload schemas one level deep into JSON structure
SJP5|forbidden in JSON|lists of lists+maps of lists+lists of maps+deep nesting|payload needing nested structure is signal to factor into separate entity types with FKs
SJP6|API gate validation|read discriminator field's value+lookup registered JSON schema for that value+validate payload recursively+failures reject with structured errors

# cross_field_split(concern|layer|mechanism)
SX1|per-field bounds|schema|closed vocabulary; mechanical; lookup-time validation
SX2|cross-field invariants|policy data|policy rows of type semantic_invariant; evaluated at API semantic-validation step
SX3|examples cross-field|policy|"if status=X then Y must be set"|"min_replicas <= max_replicas"|"deployment_strategy matches cluster_capability_set"
SX4|policy_data_json shape|registered with API|bounded - typically comparisons across named fields with small operator set; more expressive than schema closed vocab because operates in API evaluation context
SX5|policies reference entity_type|coupling|API consults applicable invariants when validating any change_set touching that entity_type
SX6|why split holds|architectural|schema loaded once rarely changes (hot path bound validation simple); semantic invariants change often as understanding evolves (kept in change-mgmt pipeline); new invariants don't require schema migration just new policy rows

# meta_schema(aspect|content)
SM1|role|schema describing what valid schema files look like; loader's first action is load+validate every other file against it
SM2|self-describing mostly|meta-schema written in same vocabulary as other schemas
SM3|bootstrap exception|meta-schema cannot use FK references to entities not yet loaded (nothing loaded yet); meta-schema's type field is enum of closed type vocab listed inline rather than referenced
SM4|exception bounded|meta-schema is ONLY file with bootstrap exception; every other schema file uses FK references; meta-schema is leaf of recursion
SM5|location|meta/_schema_meta.yaml; loaded before conventions/reserved.yaml and any imports
SM6|validation against hardcoded baseline|loader has hardcoded baseline (smallest possible self-describing structure known well-formed); meta-schema validated against it
SM7|after load immutable|meta-schema not reloaded+recomputed+evaluated against itself again
SM8|two paths to populate _schema_* tables|from YAML files (initial bootstrap or full rebuild) OR from existing database (recovery or migration via introspection)|either path produces same destination state

# bootstrap(step|action|output)
SB1|1|loader loads meta-schema from meta/_schema_meta.yaml|validated against loader's hardcoded baseline
SB2|2|loader loads conventions/reserved.yaml|validated against meta-schema
SB3|3|loader processes imports list from directory.yaml in order|each file validated against meta-schema; FK refs resolved against entities loaded so far; entity added to in-memory schema model
SB4|4|loader generates engine-appropriate DDL|CREATE TABLE for each entity (and *_version sibling if applicable)+CREATE INDEX+FK and CHECK constraints where supported
SB5|5|loader applies DDL to storage engine in dependency order|database structure created
SB6|6|loader inserts rows into _schema_* tables|describing loaded schema; row in _schema_version with schema_version from directory.yaml and is_current=true
SB7|7|OpsDB ready|API can begin serving requests; runners can begin operating

# evolution_allowed(id|change|examples|why_safe)
SX_A1|adding new field|nullable:true|existing rows have no value (fine because nullable)
SX_A2|adding new enum values|enum_values list expansion|existing rows holding previous values remain valid; new writes can choose any expanded values
SX_A3|widening numeric ranges|min_value decreased OR max_value increased|never the reverse
SX_A4|widening length bounds|max_length increased|never decreased
SX_A5|adding new entity types|entirely additive|no impact on existing entities
SX_A6|adding new indexes|improves query performance|does not affect data validity
SX_A7|adding new approval rule references|tightens governance for new changes|existing rows unaffected
# all flow through _schema_change_set; pass validation easily because cannot break consumers

# evolution_forbidden(id|forbidden|why|alternative)
SX_F1|deleting fields|breaks history (version rows reference value+audit log entries reference field changes); forces executor to rewrite history (forbidden) or refuse|deprecate; column+data remain; tombstone forever
SX_F2|renaming fields or entity types|breaks every consumer (runners by name+audit log+version history)|add new field with new name + deprecate old (duplication pattern); names absolute forever
SX_F3|changing field types|int→float+varchar→other+enum_values shrunk all break consumers|duplication+double-write pattern (§type_change)
SX_F4|narrowing numeric ranges|existing rows might hold values now out of range|widening only allowed direction
SX_F5|narrowing length bounds|existing strings might exceed new bound|widening only allowed direction
SX_F6|removing enum values|existing rows might hold removed value|duplication pattern with new field of narrower set
SX_F7|tightening uniqueness|existing rows might violate constraint|duplication pattern
SX_F8|removing indexes|usually a mistake; allowed if no consumer depends on for performance|change steward must verify; validator does not check
# why absolute: partial enforcement is worse than full enforcement; if sometimes-allowed every consumer must be defensive everywhere; absolute rules let consumers be simple

# type_change(step|action|duration|purpose)
ST1|1 Add new field|new field with new type alongside old field|both fields exist in schema and table|both available
ST2|2 Begin double-writing|all code writing to old field updated to also write to new field|N successful release cycles (typical 3-5)|enough that any consumer that hasn't migrated has had time
ST3|3 Migrate readers|code reading from old field updated to read from new field|until reads of old field become rare or zero|consumers progressively switch
ST4|4 Mark old field deprecated|update _schema_field deprecated flag|immediate|signals new code should not use old field
ST5|5 Continue double-writing|values still written for safety; old field becomes tombstone (nothing reads them)|additional cycles until schema steward confident no consumers depend|safety period
ST6|6 Old field never removed|remains as tombstone deprecated with no current operational meaning|indefinitely|storage cost is price of stable history
# pattern handles every type change: int→float|varchar→structured-enum|semantic restructuring (rename+type change)

# change_application(step|actor|mechanism)
SA1|1 Schema change starts as git PR|author|edits files: adds entity file+adds fields+widens enum+adds index
SA2|2 PR review|schema steward+other reviewers|checks structural integrity+DSNC adherence+comprehensiveness (slicing-pie); CI may run loader on PR branch independently before merge
SA3|3 PR merge triggers CI|automated|generates _schema_change_set proposal as diff between current schema (OpsDB _schema_* tables) and new schema (merged repo)
SA4|4 Diff expressed as schema-evolution operations|automated|ADD ENTITY+ADD FIELD+WIDEN ENUM+ADD INDEX+MARK DEPRECATED
SA5|5 _schema_change_set governed by OPSDB-6 change-mgmt|API|stricter approval rules; approvers include schema steward role
SA6|6 Validation runs through standard pipeline|API|validator confirms no operations forbidden by §evolution_forbidden are present; rejected at validation step before approval routing
SA7|7 On approval specialized schema executor applies|schema executor runner|reads approved _schema_change_set+associated field changes+generates DDL+applies to storage engine atomically where possible+updates _schema_* tables+updates _schema_version with new current+marks change_set applied
SA8|8 Failures during DDL halt executor|automated|rolls back what can be rolled back; change_set status=failed; finding filed; operator investigates; schema repo and OpsDB remain pre-change until corrective change_set
SA9|after every applied _schema_change_set|invariant|OpsDB schema metadata tables match repo at corresponding schema_version; synchronized by construction

# reconciliation(scenario|repo_state|opsdb_state|resolution)
SN1|Versions match structures match|directory.yaml.schema_version equals _schema_version.version_label is_current|same|no action; system consistent
SN2|Versions differ executor catches up|repo ahead of OpsDB|approved-not-yet-applied _schema_change_set rows exist|schema executor processes rows in order on next cycle; versions converge
SN3|Structures differ at matching versions|repo claims X|OpsDB has X' (someone hand-edited+restored backup that diverged+executor bug)|reconciliation runner periodically introspects DB+compares to schema metadata claims+writes compliance_finding severity=high; operator investigates+determines benign vs harmful; either DB corrected via _schema_change_set re-applying canonical OR schema updated via _schema_change_set documenting divergence as new canonical; finding closed with resolving change_set
SN4|Repo restored to older state|directory.yaml.schema_version older than OpsDB|finding requiring human review|re-apply missing changes (cherry-pick from history+re-merge missing PRs); OpsDB NOT rolled back to older schema (would violate no-deletion rule)
SN5|OpsDB restored from backup|repo ahead|backup predates some schema changes|schema executor detects missing changes in next cycle (some _schema_change_set rows have applied_time in future of current _schema_version)+re-applies; after processing OpsDB matches repo; works because change_set rows are themselves data and survive backup
# integrity rule: schema repo is SoT for schema; OpsDB schema metadata is runtime cache; where they disagree question is which is correct + answer is whichever change-mgmt process most recently approved; reconciliation always converges to change_set-approved state

# portability(concern|declared_in_schema|engine_chooses)
SP1|relational structure|tables+columns+types+FKs|physical storage layout (row store|column store|hybrid|LSM|B-tree)
SP2|constraints|ranges+lengths+enum sets+FKs+uniqueness|index implementation (B-tree|hash|GIN|GiST|BRIN)
SP3|indexes|what indexes must exist (required not advisory)|replication topology (single primary|multi-primary|sharded|partitioned|geo-replicated)
SP4|relationships|cross-table FK references defining structural connectivity|concurrency control (MVCC|locking|optimistic)
SP5|nothing|backup and recovery (snapshots|WAL shipping|logical dumps)|operational concerns
# engine-independent; Postgres+MySQL+CockroachDB+FoundationDB+MariaDB+SQLite all valid

# ddl_mapping(vocab_type|postgres|constraint_implementation)
DDL1|int|INTEGER or BIGINT based on range bounds|CHECK (field >= min_value AND field <= max_value)
DDL2|float|DOUBLE PRECISION or NUMERIC(precision scale) if precision_decimal_places set|same range CHECK
DDL3|varchar|VARCHAR(max_length)|CHECK (length(field) BETWEEN min_length AND max_length)
DDL4|text|TEXT with optional CHECK constraint on length|same length CHECK
DDL5|boolean|BOOLEAN|none
DDL6|datetime|TIMESTAMPTZ|none
DDL7|date|DATE|none
DDL8|enum|VARCHAR with CHECK listing enum_values OR Postgres ENUM type|CHECK (field IN (...))
DDL9|foreign_key|INTEGER REFERENCES <target>(id)|FK constraint
DDL10|json|JSONB|JSON validation at API; engine validation if supported (Postgres JSONB+MySQL JSON validation functions)
DDL11|indexes|CREATE INDEX or CREATE UNIQUE INDEX|engine-chosen physical index type

# engine_degradation(aspect|behavior)
DG1|API enforcement always|constraint enforced at API gate regardless of engine support; API does not delegate validation entirely to engine
DG2|Engine cannot honor constraint|loader generates table without engine-level constraint+logs gap|deployment proceeds with validation at API only
DG3|Both layers enforce typically|most modern engines+most orgs both API and DB enforce|defense in depth
DG4|Some edge cases API only|graceful degradation|validation still mechanical and bounded just runs in one place
DG5|FK constraint absence|API performs FK existence checks on every write|bounded by index lookups not free but acceptable if fast
DG6|Unique index absence|API performs uniqueness checks under concurrent writes (harder)|uniqueness for important fields effectively requires engine support
DG7|Transactional DDL absence|executor applies DDL changes serially with manual rollback|harder schema migrations
# orgs choosing unusual storage engine inherit corresponding limitations in schema enforceability

# design_refusals(id|not_a|why|belongs_in)
SG1|Not a programming language|vocab not Turing-complete; no expressions+variables+functions+control flow|adding even small features creates evaluation dependency; authors+reviewers+loader would need embedded language; schema no longer inspectable as data
SG2|Not a constraint solver|validates per-field bounds at write time; does not solve cross-field+optimize over multiple fields|constraint solver in schema would expand expressive power but cost bounded validation time; bounded time critical at API gate
SG3|Not a templating system|files not parameterized; no per-environment substitution+per-tenant variation+inheritance from base|templating creates gap between checked-in and loaded; expansion logic hides complexity; what's in file is what gets loaded
SG4|Not a migration engine|loader generates DDL for current schema state; does not migrate data between versions automatically|schema migrations are mechanical (run DDL); data migrations involve domain logic+large volumes+multi-step coordination; keep separate
SG5|Not a permissions system|describes structure not who can read/write|access control is policy data per OPSDB-6 §6 (policy rows of type access_control evaluated at API authorization step); two concerns evolve independently
SG6|Not a runtime API|loader runs to apply schema; not in request path|API queries schema metadata not files at request time; if git repo unreachable API continues serving (metadata fully cached in OpsDB); schema repo consulted only when changes applied
SG7|Not a query language|describes structure for API to enforce; does not describe queries|search API (OPSDB-6 §4) defines querying separately; schema vocab for declaring data exists; search lang for retrieving

# worked_example_service(field|declaration)
WE_S1|entity_type|service
WE_S2|description|operational role in DOS; services compose packages and bind interfaces to concrete endpoints; change-managed every change produces new service_version
WE_S3|table_category|change_managed
WE_S4|versioned|true
WE_S5|soft_delete|true
WE_S6|reserved_fields_apply|id+created_time+updated_time+is_active+_delete+_delete_time+_delete_user_id
WE_S7|fields|site_id:foreign_key references=site nullable=false|name:varchar min=1 max=255 nullable=false|description:text max=4000 nullable=true|service_type:enum [standard|database|k8s_cluster_member|cloud_managed] nullable=false|parent_service_id:foreign_key references=service nullable=true (self-FK for hierarchies)
WE_S8|governance_fields|_requires_group:foreign_key references=ops_group nullable=true|_retention_policy_id:foreign_key references=retention_policy nullable=true
WE_S9|indexes|[site_id+name] unique=true (names unique within site)|[parent_service_id]
WE_S10|approval_rules|production_service_change_two_approvers|compliance_scope_change_compliance_team
WE_S11|introduced_in_schema_version|2026.01.01.01
WE_S12|deprecated_in_schema_version|null
# every line of file is data the loader processes mechanically

# worked_example_json(field|declaration)
WE_J1|discriminator_field|cloud_resource_type
WE_J2|discriminator_value|ec2_instance
WE_J3|description|validation schema for cloud_data_json when cloud_resource_type=ec2_instance
WE_J4|fields:instance_type|enum [t3.micro|t3.small|t3.medium|m5.large|m5.xlarge|...] nullable=false (org-approved instance types)
WE_J5|fields:ami_id|varchar min=12 max=21 nullable=false
WE_J6|fields:vpc_id|varchar min=12 max=21 nullable=false
WE_J7|fields:subnet_id|varchar min=15 max=24 nullable=false
WE_J8|fields:security_group_ids|list element_type=varchar element_min_length=11 element_max_length=20 min_count=1 max_count=10 nullable=false
WE_J9|fields:tags|map key_type=varchar key_max_length=128 value_type=varchar value_max_length=256 max_entries=50 nullable=true
WE_J10|introduced_in_schema_version|2026.01.01.01

# relationships(from|rel|to)
SC1|implements|SC2
SC1|enables|SC9
SC2|prevents|drift-between-DDL-and-validation-code
SC3|implements|SC4
SC3|implements|SC5
SC3|enables|bounded-validation-time
SC4|prevents|knowability-loss
SC5|prevents|DoS+dialect-variation+unpredictable-behavior
SC7|implements|SC8
SC9|implements|engine-portability
SC10|prevents|complexity-in-every-consumer
SD1|increments_per|_schema_change_set apply
SD5|prevents|inferred-dependency-complexity
SD6|enforces|fast-fail-on-unresolved-refs
SE4|triggers|loader-generates-version-sibling-table
SE5|triggers|loader-includes-soft-delete-fields
SE6|references|conventions/reserved.yaml
SE9|enforces|bounded-time-validation-at-API-gate
SE10|references|approval_rule policies; loader validates policy exists
SV_T8|requires|json_type_discriminator
SV_T8|enables|recursive-validation-with-bounded-depth
SV_T9|requires|enum_values
SV_T10|requires|references-to-target-entity
SV_M2|excludes|foreign_key+datetime+json
SV_C4|required_for|varchar
SV_C6|required_for|foreign_key
SF1|equivalent_via|enum-of-prefixes+length-bounds+API-semantic-validation
SF2|enforces|literals-only-in-schema-files
SF3|defers_to|policy-data-at-API-semantic-validation-step
SF4|exception|reserved-fields-via-name-reference (controlled mechanism not general inheritance)
SF7|enforces|tombstone-pattern
SF8|enforces|duplication-pattern
SJ1|recursive_use_of|main-vocabulary-primitives-as-element_type
SJ2|recursive_use_of|main-vocabulary-primitives-as-key_type-and-value_type
SJP4|forbids|deeply-nested-JSON
SJP5|signal_to|factor-into-separate-entity-types-with-FKs
SX1|hot_path|every-write
SX2|change_managed|policy-rows
SX3|kept_out_of_schema|to-prevent-logic-smuggling
SX5|coupling|policies-to-schemas-via-entity_type-names
SM3|bootstrap_exception|meta-schema-only
SM4|bounded|leaf-of-recursion
SM6|hardcoded_floor|in-loader-itself
SM8|two_paths|YAML-files-OR-DB-introspection
SB7|enables|API-and-runners-operational
SX_A1|safe_because|nullable
SX_A3|allowed_direction|widening-only
SX_F1|breaks|history-and-audit-log
SX_F2|breaks|every-consumer
SX_F3|breaks|every-consumer
ST1|step_one_of|type-change-pattern
ST6|enforces|never-deleted
ST_ALL|implements|absolute-rules-via-bounded-pattern
SA3|automated|via-CI
SA5|stricter_approval|than-normal-change-sets
SA7|specialized_executor_role|schema-executor
SA9|invariant|repo-and-OpsDB-synchronized-by-construction
SN_ALL|converges_to|change-set-approved-state
SN3|severity|high
SN4|never|roll-back-OpsDB-to-older-schema (would violate SX_F1)
SN5|works_because|change_set-rows-are-data-survive-backup
SP1|engine_independent|true
SP_ALL|implements|SC9
DDL_ALL|loader_generates|engine-appropriate-syntax
DG1|invariant|API-always-enforces
DG2|graceful_degradation|when-engine-cannot-honor
DG_ALL|defense_in_depth|when-engine-supports
SG1|prevents|schema-becoming-Turing-complete
SG2|preserves|bounded-validation-time
SG3|prevents|gap-between-checked-in-and-loaded
SG4|separates|schema-migrations-from-data-migrations
SG5|separates|structure-from-access-control
SG6|preserves|API-uptime-without-repo
SG7|separates|declaration-from-retrieval
WE_S_ALL|demonstrates|complete-entity-file-shape
WE_J_ALL|demonstrates|complete-JSON-payload-schema-file-shape

# section_index(section|title|ids)
1|Introduction|SC1,SC2,SC3,SC4,SC5,SC6,SC7
2|Conventions|inherited from prior series; SF5 forbids templating per SC10
3|Repository Layout|SR1-SR22
4|directory.yaml Master File|SD1-SD10
5|Entity File Shape|SE1-SE13,WE_S1-WE_S12
6|Closed Constraint Vocabulary|SV_T1-SV_T10,SV_M1-SV_M3,SV_C1-SV_C8
7|What Vocabulary Forbids|SF1-SF8
8|Cross-Field Constraints|SX1-SX6
9|JSON Payload Validation|SJ1,SJ2,SJP1-SJP6,WE_J1-WE_J10
10|Meta-Schema and Bootstrap|SM1-SM8,SB1-SB7
11|Loading and Applying|SA1-SA9
12|Schema Evolution Rules|SX_A1-SX_A7,SX_F1-SX_F8,ST1-ST6
13|Reconciliation|SN1-SN5
14|Storage-Engine Portability|SP1-SP5,DDL1-DDL11,DG1-DG7
15|What Design Refuses|SG1-SG7
16|Closing|SC1-SC11 restated structurally

# decode_legend
table_categories: change_managed|observation_only|append_only|computed
type_primitives: int|float|varchar|text|boolean|datetime|date|json|enum|foreign_key
modifiers: nullable|default|unique
constraints: min_value|max_value|min_length|max_length|enum_values|references|precision_decimal_places|must_be_unique_within
json_collection_types: list|map (only used in JSON payload schemas)
forbidden_patterns: regex|embedded-logic|conditional-constraints|inheritance|templating|imports-within-files|deletions|renames|type-changes|narrowing
allowed_evolutions: add-field|add-enum-value|widen-numeric|widen-length|add-entity|add-index|add-approval-rule
type_change_pattern_steps: 6 (add new field|begin double-write|migrate readers|mark deprecated|continue double-write|never remove)
reconciliation_outcomes: no-action|executor-catches-up|finding-and-resolution|re-apply-missing-changes|executor-re-applies-after-restore
sot_for_schema: schema-repo (OpsDB schema metadata is runtime cache)
rel_types: implements|enables|prevents|enforces|requires|excludes|references|triggers|defers_to|equivalent_via|exception|recursive_use_of|forbids|signal_to|hot_path|change_managed|kept_out_of|coupling|bootstrap_exception|bounded|hardcoded_floor|two_paths|safe_because|allowed_direction|breaks|step_one_of|implements_via|automated|stricter_approval|specialized_executor_role|invariant|converges_to|severity|never|works_because|engine_independent|loader_generates|graceful_degradation|defense_in_depth|preserves|separates|demonstrates
