# OPSDB IMPLEMENTATION PATH — LLM-COMPACT FORM
# Format: pipe-delimited tables, ID refs.
# Read order: principles → phase-structure → phases → cardinality → n-pipeline → schema-baseline → hand-loading → dev-api → ingestion → dsnc → library-core → existing-code → change-mgmt → approval → emergency → auto-approval → runner-enum → operational → first-runner → roles → transition → validation → relationships → sections

# principles(id|principle|rationale)
PH1|Validation as gate not calendar|phase complete when criterion met not when duration elapsed; teams stay in phase until satisfied; premature move builds on incomplete foundation
PH2|Phased not top-down|architecture too large to build at once; top-down produces multi-quarter project delivering nothing usable until end; teams lose attention before benefits
PH3|Each phase delivers operational value|Phase 3 dev substrate answers real questions; Phase 5 produces governance; Phase 6 produces benefits compounding from there
PH4|Each phase validates prior understanding before next|errors caught early when cheap; phase N+1 builds on phase N rather than reworking
PH5|Decision-deliverable-validation-deferred shape uniform|every phase has decision (what to choose) + deliverable (what to produce) + validation criterion (when complete) + what next phase will address
PH6|Bootstrap at largest cardinality from smallest|N=∞ pipeline at N=2 costs slightly more than N=1 at N=1; N=∞ retrofitted onto N=2-grown-independently costs much more
PH7|Schema quality determines everything downstream|well-formed schema scales+audit composes+automation works; poorly-formed schema imposes costs on every consumer for OpsDB lifetime
PH8|Get schema right at Phase 3 because revising is cheap then|after phases 3-5 expensive because data ingested under prior shape; rapid iteration only valid before governance pipeline
PH9|Pick most painful or valuable domain first at Phase 6|investment substantial; phase 6 is when it compounds; high-pain first delivers immediate benefit and validates architecture
PH10|Phase 6 has no end ceremony|"covers what matters and absorbs new things cleanly" not "schema finished"; work continues; structure stays stable
PH11|Decision and deliverable are real even before code|Phase 1 deliverable is documented decision+rationale; no code yet; the decision is the deliverable

# phase_structure(component|content)
PS1|decision|what to choose at this phase
PS2|deliverable|what to produce
PS3|deferred|what next phase will address; explicit out-of-scope
PS4|validation criterion|when complete; gate for moving to next phase
PS5|sequential|phases 1-6 not parallel; numbering is order

# phases(id|phase|decision|deliverable|validation)
P1|Decide cardinality|1-OpsDB OR N-DOS-1-OpsDB OR N-DOS-N-OpsDB|documented decision+rationale citing structural reasons; for N: documented sync pipeline plan committed to N=2 bootstrap|schema steward+operational lead agree on cardinality+can name structural reasons; rationale not "easier" or "might need eventually"
P2|Determine baseline schema|how much of INFRA-3 to adopt+what to add+what to validate by hand-loading|adapted schema repo per INFRA-6; hand-loaded representative data covering 3+ domains; schema steward identified+in role; for N: deploys cleanly to 2 test substrates|representative subset of actual infrastructure expressible as data with no awkward fits; relationships connect+typed payloads accommodate real types+substrate walks resolve+operational scenarios modelable
P3|Build dev API and start ingesting data|start writing real data into substrate before substrate is operational|dev OpsDB with real data from 3+ sources; schema iterated to fit data; DSNC applied throughout; list-of-N test applied; team can answer real operational questions|team can answer real ops questions by querying ("show me every running EC2 in production" works); schema covers what matters; data well-shaped; flatten/break-out decisions correct
P4|Determine shared library core|minimum viable suite + what existing code becomes part of it|opsdb.api implementing INFRA-8 §4 + opsdb.observation.logging implementing INFRA-8 §7.1; phase 3 scripts refactored to use both; existing operational code inventoried+categorized|new ingestion script writable using only libraries (no ad-hoc HTTP+no unstructured logging); runner-pattern shape from INFRA-4 §2 emerging; line counts small because libraries do heavy lifting
P5|Design and implement change management|what CM pipeline looks like+which entities go through it|working CM pipeline with org's actual approval rules+emergency path+auto-approval policies; runners registered with declared scopes; dev-to-operational transition completed|configuration change as change_set validates+routes for approval+approves+applies+records with full trail queryable end-to-end; runners' declared scopes enforced
P6|Add operational logic beyond OpsDB management|which operational domain to address first then which after|first operational runner in production addressing real domain; producing queryable trail; library suite grown to include world-side libraries runner needed; pattern for adding subsequent runners|OpsDB delivers operational benefit beyond own maintenance; real ops task previously requiring scattered tooling now runs through OpsDB-coordinated pattern; queryable trail composes for humans+automation+auditors
# rule: phase 6 doesn't end; steady state; new runners added as new domains coordinated; schema grows additively; library suite accretes patterns

# cardinality(id|configuration|when|notes)
C1|1 DOS 1 OpsDB|simplest case; one operational domain one substrate|most orgs under structural-unity threshold from INFRA-2 §5.3
C2|N DOS 1 OpsDB|several operational domains share one substrate|production+corporate-infra+employee-fleet may each be DOS but share OpsDB scoped by site rows; data partitioned; substrate+API+runners+schema+libs unified
C3|N DOS N OpsDB|substrate-level separation per INFRA-2 §5.4|security perimeters where API access control structurally insufficient+legal/regulatory residency+independently-operating units+air-gap

# cardinality_invalid(id|reason|why_invalid)
CI1|technical fragility|"protect prod from corp tooling experiments"; signs of bad ops not structural
CI2|convenience|"two would be easier to manage"; convenience not structural; overhead exceeds gain
CI3|premature optimization|"we might need to split eventually"; stay-1 until structure forces N
CI4|performance|"one cant serve our query load"; scale within single OpsDB via replicas/sharding/cache
# rule: if rationale falls in these categories the decision is wrong; phase 1 not complete; revisit

# n_bootstrap(aspect|content)
NB1|minimum N|2; three is larger case requiring more pipeline work
NB2|start at 2|even when org knows eventually 3+; forces N-mode action with minimal initial setup
NB3|catches failure modes early|schema sync at 2-substrates-still-small reveals propagation bugs+library deployment+version-pinning before operationally critical
NB4|cost argument|N=∞ pipeline at N=2 ≈ slightly more than N=1 at N=1; N=∞ retrofitted onto N=2-grown-independently = much more
NB5|by N=3|pipeline mature

# n_pipeline(aspect|shared_or_diverged|content)
NP1|schema repo|shared|one repo deployed to N OpsDBs
NP2|library suite contracts and impls|shared|one set consumed by N runner populations
NP3|API code|shared|one codebase deployed N times
NP4|change-mgmt discipline|shared|same rules applied at each substrate evaluated against that substrate's data
NP5|data each substrate holds|diverged|each substrate is own write authority per INFRA-2 §5.8
NP6|users authorized at each|diverged|per substrate
NP7|audit log of each|diverged|per substrate independent
NP8|runners deployed against each|diverged|per substrate
NP9|cross-OpsDB writes|not supported|coordination through external means: human filing change_sets at each OR runner with creds at multiple substrates

# schema_baseline(id|sub_decision|guidance)
S1|how much of INFRA-3 to adopt|trim only what you are certain you don't need; trim K8s if not running K8s; trim hardware if cloud-only; declarations carry no operational cost when no rows
S2|what to add for domains INFRA-3 doesn't cover|regulated medical+financial+manufacturing+other domains; comprehensive-thinking-aggregate-building from INFRA-2 §14.1; DSNC+closed vocabulary+typed payloads+polymorphic bridges+versioning siblings transfer; specific entity types are org's decision
S3|what to validate by hand-loading|cheapest validation move; phase 2 must not skip
S4|honest scope enumeration|which domains coordinated? server+cloud+K8s+SaaS+tape+vendors+certs+on-call+compliance+manual ops+office access; each is candidate
S5|err-direction bias|include rather than exclude when uncertain; schema cheap to set up early before data; adding rows to unanticipated domain later more expensive

# hand_loading(id|question|surfaces)
HL1|Does schema describe actual infrastructure?|sample EC2+pod+service+on-call+cert as rows; fields right? missing? present-but-unused?
HL2|Are FK relationships right?|EC2→megavisor_instance→hardware/cloud account; service→service_connection→dependencies; substrate-walking queries from INFRA-4 §9 produce expected results
HL3|Are typed payloads accommodating real types?|INFRA-3 §6.8 lists common cloud_resource_type values; org's actual usage may need new discriminator+JSON schemas for cloud_data_json
HL4|Do relationships compose under realistic queries?|service+packages+hosts+on-call+dependencies+monitors+runbooks; run incident-investigator queries; joins resolve? data model answers ops questions?
# rule: awkward fits = schema needs revision before code written against it; revising at phase 2 cheap; revising after phases 3-5 expensive

# dev_api_minimal(present|deferred)
DA_P|authenticated reads and writes|DA_D
DA_P|structured error reporting|DA_D
DA_D|change_set submission flow|deferred to phase 5
DA_D|five-layer authorization|deferred to phase 5
DA_D|runner report keys|deferred to phase 5
DA_D|emergency apply|deferred to phase 5
DA_D|bulk operations|deferred to phase 5
DA_D|optimistic concurrency|deferred to phase 5
DA_D|audit log infrastructure beyond simple request logging|deferred to phase 5
# rule: dev API replaced/upgraded substantially at phase 5; throwaway by design; serves goal of validating schema and discovering data shape
# rule: adding governance before data is premature; design against incomplete data understanding will need rework

# ingestion(aspect|content)
IN1|by phase 3|team has schema+minimal API
IN2|work|take org's current operational data sources (cloud control planes+K8s+monitoring+vault+IdP+anything producing operational data) and write to dev OpsDB
IN3|puller pattern from INFRA-4 §4.1 in earliest form|without runner discipline
IN4|scripts not runners|no runner_spec rows yet+no runner_machine deployment+no runner_schedule+just scripts on dev machines reading from authorities writing to dev OpsDB
IN5|scrappy by design|demonstrate schema can hold data; do not yet demonstrate runner pattern end-to-end (phase 5)

# dsnc_flattening(id|rule|example)
D1|flatten when nested data is per-row metadata of parent|EC2 instance_type+ami_id+vpc_id+subnet_id go in cloud_data_json as flat fields under ec2_instance discriminator; instance is one row; metadata part of that row
D2|break out when nested data has independent lifecycle OR identity OR appears in lists of N|security group memberships are many-to-many; each membership has identity+lifecycle (added/removed)+typically multiple per instance; bridge table per INFRA-3 §2.5
D3|list-of-N test|when source has list of N items flattening to prefix_data_list_0_value+prefix_data_list_1_value+... is wrong; loses listness; N variable; indices positional not meaningful
D4|naive flattening failure mode|EC2 with N attached EBS volumes flattened to ec2_data_volumes_0_id+ec2_data_volumes_1_id+team adds new fields each time encountering more attached volumes than schema supports
D5|correct shape|cloud_resource_attached_volume bridge table OR recognize EBS volumes are themselves cloud resources and relationship is cloud_resource_to_cloud_resource typed
D6|practical test during phase 3|when ingesting nested structure: any nested element with identity that could change independently of parent OR N of them = sub-table data not flat-payload
# rule: list-of-N is most common phase 3 mistake

# dsnc_naming(aspect|content)
DN1|names get long|cloud_resource_security_group_membership; service_authority_pointer_relationship_role; change_set_emergency_review_status
DN2|verbosity is price of unambiguous structural meaning|each component carries meaning; pattern is parent_concept_subconcept_subconcept
DN3|recompose without provenance loss|reading cloud_resource_security_group_membership tells you exactly: membership relating cloud resource and security group
DN4|alternative produces drift|short names (sg_mem) require institutional knowledge; new team members guess wrong; old members forget; DSNC refuses drift
DN5|cost|keystrokes
DN6|benefit|structural transparency; new tables fit pattern; readers learn pattern once apply across schema
DN7|phase 3 builds the muscle|by phase 5 long names read fluently; by phase 6 consistency makes runners small

# schema_quality(aspect|content)
SQ1|claim|getting schema right is most important thing
SQ2|well-formed enables|runners scale+audit composes+automation works
SQ3|poorly-formed forces|every runner deals with bad data+audit and automation deal with it+cost paid by every consumer in every cycle for OpsDB lifetime
SQ4|right shape pays back|volume-tracking runner small+audit query direct+compliance scanner without special-case logic
SQ5|wrong shape costs forever|every runner touching volumes carries logic to extract+every audit query parses indices+every schema change adds positional field cascading through every consumer
SQ6|why phase 3 iterative+validation-gated not time-gated|team stays in phase 3 until schema right; only then ingestion at scale makes sense
SQ7|iteration cheap at phase 3|no governance pipeline; team edits files+runs loader+continues; after phase 5 schema changes go through schema executor (heavier process)

# library_core(id|library|role)
LC1|opsdb.api|foundational; every subsequent runner uses it; no runner accesses OpsDB any other way; INFRA-8 §4 specifies contract
LC2|opsdb.observation.logging|second foundation; INFRA-8 §7.1 specifies contract; uniform observation surface
# rule: two libraries are floor; other libraries (K8s+cloud+retry+notification+templating+git) added in phase 6 as runner population needs
# validation move: refactor phase 3 scripts to use libraries; if contracts make scripts harder to write than ad-hoc HTTP they replaced contracts are wrong; iterate until ingestion code smaller and clearer
# rule: major contract revisions during phase 4 appropriate; after phase 6 begins library contracts evolve through INFRA-8 §11.2 deprecation discipline

# existing_code(category|becomes|rationale)
EC_C1|world-side I/O code|shared library implementations|existing code doing K8s API calls+cloud API calls+SSH+vault reads mostly reusable as impl backing INFRA-8 contracts; refactor to wrap in contract surface
EC_C2|decision-making code|runner code (in phase 6)|existing code deciding which PVCs to repair+which alerts to escalate+which configs to apply is runner-specific logic; stays runner-specific; phase 6 refactors to use libraries while retaining decisions
EC_C3|code duplicating OpsDB design|thrown out|custom inventories+ad-hoc state stores+scripts maintaining own caches of operational reality compete with OpsDB; retire as OpsDB takes over function
# rule: phase 4 inventories existing operational code and labels each piece by category; library candidates refactored phases 4+6; runner candidates wait phase 6; retirement candidates documented for later

# cm_split(entity_class|gating|rationale)
CM1|expresses intent|change-managed|configuration changes+schedule changes+runner registration+policy changes+metadata changes+schema changes+access control changes
CM2|records observation|not change-managed|cached observation writes by pullers+runner result writes+audit log entries (created automatically by API)
# rule: phase 5 walks every entity type and labels as change_managed|observation_only|append_only|computed per INFRA-3 Appendix D
# rule: most labels match INFRA-3 defaults; some adjust based on org's specifics (compliance demanding approval trails for entity team thought was observation-only OR nothing changes entity except pullers so entity team thought needed governance is actually observation-only)

# approval_rules(id|pattern|content)
AR1|service owners approve changes to their services|change_set touching service routes to role owning that service
AR2|security team approves security-relevant fields|changes to _security_zone+authentication-related fields+firewall-relevant configurations route to security role regardless of entity owner
AR3|compliance team approves changes within compliance scope|entities in compliance_scope_service for active regimes have additional approval requirements
AR4|schema steward approves schema_change_sets|changes to _schema_* tables route to schema steward role
AR5|production operations approves production runtime changes|entities in production namespace with runtime-relevant fields have additional approval from production ops role
# rule: approval rules are policy data change-managed themselves; team writes them in phase 5; evolve through same change_set discipline thereafter

# emergency_path(aspect|content)
EM1|who has break-glass right|on-call engineers with elevated rights OR designated emergency response roles
EM2|post-hoc review cadence|INFRA-5 §7.9 suggests 72 hours; configurable per org
EM3|who reviews after fact|schema steward OR security team OR designated incident review role
EM4|rare use is correct|emergencies real; discipline ensures path not abused

# auto_approval(id|pattern|rationale)
AA1|drift corrections in non-production|action routine+environment non-critical+waiting for human more risky than correction
AA2|scheduled credential rotations|rotation falls within declared schedule
AA3|routine reconciler corrections within declared scopes|change below defined risk threshold (timeouts within range+replica counts within bounds)
AA4|cached observation writes|no change_set; use write_observation directly
# rule: auto-approval policies themselves change-managed; modifying requires approval from governance team; phase 5 writes with bias toward narrow auto-approval initially; broader as confidence builds

# runner_enumeration(aspect|content)
RE1|by phase 5|team has at least few pieces of code that look like runners (phase 3 ingestion scripts refactored phase 4 to use libraries)
RE2|registration|register as runner_spec rows with schedules+target scopes+report key declarations
RE3|declarations explicit|cloud puller declares cloud_account_target rows; K8s pod state puller declares runner_k8s_namespace_target; metrics puller declares runner_report_key per INFRA-5 §8
RE4|labor-intensive|each runner has declared scope; scope must be specified explicitly
RE5|declarations change-managed|per INFRA-8 §13; modifying goes through same approval pipeline as other governance configuration

# runner_polling_choice(mode|when_used)
RP1|polling|reads config from OpsDB at runtime; for runners always having OpsDB connectivity
RP2|templated|config baked into deployment; for runners that must operate during partitions (host-bootstrap+intermittent connectivity)
RP3|hybrid|templated defaults with runtime poll for updates; combines partition tolerance with config freshness
# rule: both polling and templating fine; choice depends on each runner's partition tolerance requirements per INFRA-4 §11.2

# operational(aspect|content)
OP1|structural shift|phases 1-5 produced infrastructure FOR OpsDB; phase 6 produces infrastructure that BENEFITS FROM OpsDB
OP2|runners written in phase 6|operational logic that consumes substrate prior phases built
OP3|runner kinds available|drift detectors+verifiers+reconcilers+notification runners+compliance scanners+GitOps integration+reapers+failover handlers per INFRA-4 §4
OP4|each new runner follows INFRA-4 §12.1 pattern|identify inputs+identify outputs+choose gating+choose trigger+specify bounds+define idempotency+write spec+build using shared libraries+deploy through change management

# first_runner(aspect|content)
FR1|criterion|org's most painful or most valuable operational domain
FR2|"most painful" framing right|building OpsDB pays back fastest when first phase 6 runner addresses pain currently felt
FR3|examples|cert struggle → certificate verifier first; drift in production → drift detector first; quarterly compliance scramble → compliance scanner first
FR4|runner small|200-500 lines of runner-specific logic; rest in libraries; building fast because foundation in place
FR5|validation|against real operational scenarios; observe trail in runner_job rows+evidence_record rows+change_set proposals; confirm operational benefit real
FR6|argument|investment substantial; phase 6 is when it compounds; high-pain first delivers immediately+validates architecture for team and org; subsequent runners easier to justify and build

# roles(id|role|responsibility|first_phase|continuous)
RO1|schema steward|comprehensive coherence of schema; reviews schema-evolution change_sets; notices when slicing-the-pie needed; resists fragmentation+feature creep; holds whole in mind across domains|P1 identifies by name; P2 active reviewer; P5 primary approver for _schema_change_set rows|yes
RO2|library steward|coherence of library suite; reviews library proposals+contract additions+removals+cross-library coherence+impl quality; resists fragmentation at library layer|P4 identifies by name (can be same as schema steward); P6 active in library extractions|yes
RO3|substrate operator|DBA-equivalent for storage engine; backups+replication+capacity+performance tuning; direct DB access under SoD per INFRA-2 §4.2|P1 identifies; P3 deploys dev OpsDB; P5 coordinates dev-to-operational transition|yes
RO4|platform team|owns API code+runner deployment infrastructure+day-to-day ops health; distinct from substrate operator and stewards; owns gate and framework|P1 identifies; P3 builds dev API; P4 builds foundational libraries; P5 implements production API+CM pipeline; P6 operates runner deployment|yes
RO5|operational stakeholders|owners of entities OpsDB tracks; service owners+cloud account owners+K8s cluster owners; each entity has someone responsible operationally|P5 identifies as part of writing approval rules|yes
# rule: most orgs schema/library steward is portion of senior engineer's responsibility; largest orgs or major schema evolution may be full-time

# transition(aspect|dev_substrate|operational_substrate)
T1|API|minimal: authenticated reads+writes+structured errors only|full INFRA-5 with 10-step gate
T2|change management|none|for change_managed entities
T3|authorization|rough role-based read/write|five-layer model
T4|runner report keys|none|enforced
T5|audit log|simple request logging|append-only with full attribution
T6|data ingestion|ad-hoc scripts|registered runners with declared scopes

# transition_steps(step|action)
TS1|cutover not gradual|moment when dev API replaced (or substantially upgraded) and operational disciplines come online
TS2|before moment|ad-hoc scripts can write to dev substrate
TS3|after moment|only registered runners with declared scopes can write to operational substrate
TS4|planned scheduled executed deliberately|team documents which data was loaded under dev API (remains in substrate)+turns on CM pipeline+registers runners that continue ingestion+begins recording governance trails

# transition_data(aspect|content)
TD1|data loaded under dev API|fine; there because team loaded during development
TD2|change_set history for that data|incomplete; that's acceptable for historical data
TD3|audit trails for initial loading|incomplete; OpsDB's claims about governance apply to changes after cutover not retroactively
TD4|schema metadata records schema version at cutover|canonical "schema version 1.0" or whatever team decides; subsequent schema changes flow through _schema_change_set
TD5|earlier dev-iteration schema versions not preserved as canonical|cutover establishes operational schema baseline
TD6|runners replace scripts|same data sources continue feeding OpsDB but through registered runners; runner code largely refactored phase 4 code; what changes is deployment infrastructure (registered runner_machine rows with proper runner_spec) and writes (production API with full validation not dev API with minimal)

# validation_discipline(aspect|content)
VD1|gate not calendar|phase complete when criterion met not when duration elapsed
VD2|teams stay in phase until satisfied|premature move builds subsequent phases on incomplete foundations
VD3|honesty to revisit|when validation criterion not met team revisits phase
VD4|phase 6 special case|technically working but not actually used for daily ops = phase 6 has not started; team still in phase 5; criterion is operational use not technical completeness

# relationships(from|rel|to)
PH1|gates|phase-progression
PH2|prevents|multi-quarter-projects-delivering-nothing-until-end
PH3|enables|architecture-adoptable-rather-than-aspirational
PH4|validates|prior-phase-understanding
PH6|costs|slightly-more-at-N=2-than-N=1
PH6|prevents|N=∞-retrofitted-onto-N=2-grown-independently
PH7|determines|everything-downstream
PH8|enables|cheap-iteration
PH9|delivers|immediate-validation
PH10|continues|indefinitely
P1|prereq_of|P2
P2|prereq_of|P3
P3|prereq_of|P4
P4|prereq_of|P5
P5|prereq_of|P6
P5|completes|dev-to-operational-transition
P6|delivers|architecture-promised-by-prior-papers
P6|steady_state|true
C1|simplest|true
C2|partition_via|site-rows
C3|justified_by|INFRA-2-§5.4-structural-reasons
CI1|invalid|true
CI2|invalid|true
CI3|invalid|true
CI4|invalid|true
NB2|forces|N-mode-action-with-minimal-setup
NB3|catches|failure-modes-while-cheap
NB5|matures|by-N=3
NP_shared|deployed_to|all-N-substrates
NP_diverged|per_substrate|true
NP9|coordination_via|external-means
S1|bias|trim-only-certain-not-needed
S2|patterns_transfer|DSNC+closed-vocab+payloads+bridges+versioning
S5|bias|include-rather-than-exclude-when-uncertain
HL_ALL|surfaces|schema-gaps-before-code
HL_ALL|cheaper_at|phase-2
DA_P|sufficient_for|validating-schema-and-discovering-data-shape
DA_D|deferred_to|phase-5
IN3|early_form_of|INFRA-4-§4.1-puller-pattern
IN4|distinguishes|scripts-from-runners
D1|when|per-row-metadata
D2|when|independent-lifecycle-OR-identity-OR-N
D3|prevents|positional-flattening
D4|failure_mode|naive-list-flattening
D6|test|nested-element-with-identity-OR-N=sub-table
DN2|trades|keystrokes-for-structural-transparency
DN4|prevents|institutional-knowledge-fragmentation
SQ_ALL|justifies|phase-3-iterative-validation-gated-not-time-gated
LC1|mandatory|true
LC2|mandatory|true
LC1|enables|every-runner
LC2|enables|uniform-observation
EC_C1|wraps|existing-code-in-contract-surface
EC_C2|waits_for|phase-6
EC_C3|retires|as-OpsDB-takes-over
CM1|gated|true
CM2|gated|false
AR_ALL|policy_data|true
AR_ALL|change_managed_themselves|true
EM4|rare_use|correct
AA_ALL|change_managed_themselves|true
AA_ALL|bias|narrow-initially-broader-as-confidence-builds
RE_ALL|labor_intensive|true
RE5|change_managed|true
RP1|when|always-have-OpsDB-connectivity
RP2|when|must-operate-during-partitions
RP3|when|combines-partition-tolerance-and-freshness
OP1|shift|infrastructure-FOR-OpsDB-to-infrastructure-BENEFITING-FROM-OpsDB
OP4|follows|INFRA-4-§12.1
FR1|criterion|most-painful-or-valuable
FR6|validates|architecture-for-team-and-org
RO1|continuous|true
RO2|continuous|true
RO3|continuous|true
RO4|continuous|true
RO5|continuous|true
T_ALL|differs|dev-vs-operational
TS1|once|cutover-not-gradual
TS4|deliberate|true
TD1|preserved|true
TD3|governance_applies|after-cutover-not-retroactively
TD4|establishes|operational-schema-baseline
TD6|runners_replace|scripts
VD1|gate|criterion-not-calendar
VD4|criterion|operational-use-not-technical-completeness

# section_index(section|title|ids)
1|Introduction|PH1,PH2,PH3,PH4,PH5
2|Conventions|inherited from prior series; PS5 sequential not parallel
3|Phase 1 Decide Cardinality|P1,C1,C2,C3,CI1-CI4,NB1-NB5,NP1-NP9
4|Phase 2 Determine Baseline Schema|P2,S1-S5,HL1-HL4
5|Phase 3 Build Dev API and Ingest Data|P3,DA_P,DA_D,IN1-IN5,D1-D6,DN1-DN7,SQ1-SQ7,PH8
6|Phase 4 Determine Shared Library Core|P4,LC1,LC2,EC_C1,EC_C2,EC_C3
7|Phase 5 Design and Implement Change Management|P5,CM1,CM2,AR1-AR5,EM1-EM4,AA1-AA4,RE1-RE5,RP1,RP2,RP3
8|Phase 6 Add Operational Logic|P6,OP1-OP4,FR1-FR6,PH9,PH10
9|The Roles|RO1,RO2,RO3,RO4,RO5
10|Development-to-Operational Transition|T1-T6,TS1-TS4,TD1-TD6
11|Closing|PH1-PH11 restated structurally

# decode_legend
phase_count: 6
phase_shape: decision|deliverable|deferred|validation_criterion
cardinality_options: 1-DOS-1-OpsDB|N-DOS-1-OpsDB|N-DOS-N-OpsDB
cardinality_invalid: technical-fragility|convenience|premature-optimization|performance
n_bootstrap_minimum: 2
n_pipeline_shared: schema-repo|library-suite|API-code|change-mgmt-discipline
n_pipeline_diverged: data|users|audit-log|runners
hand_loading_questions: 4
dsnc_flatten_when: per-row-metadata-of-parent
dsnc_break_out_when: independent-lifecycle-OR-identity-OR-N-of-them
list_of_n_test: most-common-phase-3-mistake
schema_quality_claim: getting-schema-right-most-important-thing-because-cost-paid-by-every-consumer-for-OpsDB-lifetime
library_minimum_set: opsdb.api+opsdb.observation.logging
existing_code_categories: world-side-I/O→library|decision-making→runner|duplicating-OpsDB→retire
cm_split: intent→gated|observation→ungated
roles_count: 5
role_continuity: all-roles-continuous-after-first-phase
transition_dimensions: API|change-mgmt|authorization|report-keys|audit-log|ingestion
cutover: planned-scheduled-executed-deliberately-not-gradual
historical_data: preserved-not-retroactively-governed
validation_discipline: criterion-not-calendar
phase_6_test: operational-use-not-technical-completeness
sot_for_decisions: documented-decision+rationale-citing-structural-reasons
sot_for_data_shape: hand-loading-against-real-infrastructure
sot_for_library_quality: refactored-scripts-getting-smaller-and-clearer
sot_for_governance: end-to-end-change_set-with-trail-queryable
sot_for_operational_value: real-task-previously-scattered-now-running-through-OpsDB-coordinated-pattern
rel_types: gates|prereq_of|completes|delivers|prevents|enables|validates|costs|determines|continues|simplest|partition_via|justified_by|invalid|forces|catches|matures|deployed_to|per_substrate|coordination_via|bias|patterns_transfer|surfaces|cheaper_at|sufficient_for|deferred_to|early_form_of|distinguishes|when|failure_mode|test|trades|justifies|mandatory|wraps|waits_for|retires|gated|policy_data|change_managed_themselves|rare_use|labor_intensive|change_managed|shift|follows|criterion|continuous|differs|once|deliberate|preserved|governance_applies|establishes|runners_replace|gate|steady_state
