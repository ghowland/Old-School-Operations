# OPSDB DESIGN — LLM-COMPACT FORM
# Format: pipe-delimited tables, ID refs.
# Read order: concepts → commitments → content → populations → flows → boundaries → cardinality → compliance → audit → disciplines → relationships → sections

# concepts(id|name|def|category)
O1|OpsDB|centralized passive data substrate; single source of truth for operational reality across DOS|term
O2|DOS|Distributed Operating System; environment operated as one coordinated system across heterogeneous nodes|term
O3|Authority|system owning a slice of operational reality (K8s for workloads, vault for secrets, monitoring for metrics)|term
O4|Source of Truth|OpsDB for owned data; cited authority for everything else; OpsDB always SoT for directory-of-authorities|term
O5|Change Set|bundle of N proposed changes with reason; routed for approval; committed atomically|term
O6|Runner|small single-purpose automation; consults OpsDB; performs work via shared libs; writes results back|term
O7|Shared Library|standardized capability runners use to act in world; enforces one-way-to-do-each-thing|term
O8|Schema Steward|person/team responsible for comprehensive coherence of schema across all domains|role
O9|Pulled State|cached observed state from authorities|term
O10|Authority Pointer|typed structured pointer to where a fact lives when not held locally|term
O11|Service Directory|specialized authority pointers; structured lookup returning right coordinate for any operational question|term
O12|Local Replica|dumped slice of OpsDB on host/pod for partition tolerance; cache with explicit freshness|term
O13|Schedule|when runners run, backups happen, certs expire, rotations occur, audits due|content-type
O14|Calendar|aggregated view across schedules; queryable temporal projection|term
O15|Policy|declarative data: security zones, compliance, escalation, change-mgmt rules, retention, schedule|content-type
O16|Approval Rule|policy expressed against schema; computed by API per change set|term
O17|Version|prior state of versioned entity; retention configurable per type|term
O18|Audit Log|append-only record of every API action; identity+timestamp+action+target+result|term
O19|Tamper Evidence|append-only audit log; optional cryptographic chaining for stricter regimes|term
O20|Attribution|every action tied to authenticated identity; no shared accounts|principle
O21|Segregation of Duties|change-mgmt rules forbidding self-approval; enforced at API|principle
O22|Evidence Record|verifier-runner-produced structured record proving control operated|term
O23|Continuous Compliance|audit posture as continuous queryable property, not periodic project|principle
O24|Emergency Change|break-glass path: reduced approvals, flagged in audit, post-incident reviewed|term
O25|Bulk Change|single change set expressing N changes; atomic; one approval for many entities|term
O26|Schema Evolution|additive; new types/fields/relationships via change-managed sets with stricter rules|term
O27|Backward Compatibility|new optional fields; existing data and readers remain valid|principle
O28|Reaper|runner that applies retention policy; removes versions past horizon|term
O29|Puller|runner type: scrapes authority, transforms to schema, writes to cache|term
O30|Verifier|runner type: checks scheduled work happened or state correct; emits evidence|term
O31|Reconciler|runner type: compares desired vs observed; performs or proposes corrective work|term
O32|Polling Pattern|runner queries OpsDB at runtime each cycle|term
O33|Templated Pattern|runner config baked at deploy time; partition-tolerant|term
O34|Hybrid Pattern|templated defaults plus runtime poll for updates|term
O35|Level Triggered|reacts to current state on every cycle; missed events caught next cycle|principle
O36|Tenant-Aware Cache|API cache keyed by access scope; prevents cross-scope leakage|term
O37|Federated Read|cross-OpsDB query mediated by each substrate's API policy|term
O38|Cross-OpsDB Reference|typed pointer: substrate-id + entity-locator; resolvable when authorized|term
O39|Cross-OpsDB Write|typically not supported; each substrate is own write authority|principle
O40|API Versioning|contract changes managed; old versions supported until consumers migrate|principle
O41|Schema Independence|substrate portable across storage engines; schema is the long-lived artifact|principle
O42|Defense of 1|refuse second OpsDB requests; absorb use case into existing substrate|discipline
O43|Comprehensive Thinking Aggregate Building|hold whole in mind while adding pieces; never aggregate-think|discipline
O44|Resist Fragmentation|absorb special cases into schema; reject side-tables|discipline
O45|Resist Feature Creep|refuse orchestration/ticketing/monitoring/chat additions; redirect to right system|discipline
O46|API Investment|sophistication earns its place; new validation/workflows/queries compound leverage|discipline
O47|Library Investment|library quality determines runner quality; new domain triggers new lib|discipline
O48|Self-Describing|querying OpsDB surfaces structured info about itself: types, relationships, runners, policies|principle
O49|Wiki Anti-Pattern|holding long-form prose, design docs, narratives in OpsDB|anti-pattern
O50|Monitoring Replacement Anti-Pattern|trying to replace Prometheus/Datadog by storing all time-series in OpsDB|anti-pattern
O51|Code Repo Anti-Pattern|storing runner source code or binaries in OpsDB|anti-pattern
O52|Orchestrator Drift|building push/trigger/invoke into OpsDB; compromises passive commitment|anti-pattern
O53|Secrets Manager Anti-Pattern|storing secret values in OpsDB instead of pointers to vault|anti-pattern
O54|Runtime Dependency Anti-Pattern|services failing because OpsDB unreachable; runners must tolerate|anti-pattern
O55|Unstructured Dumping|free-text fields used as content store instead of structured typed data|anti-pattern
O56|Privileged Population Anti-Pattern|API for machines without human surfaces, or vice versa|anti-pattern
O57|Side Table|team-specific store granted as exception; first step toward fragmentation|anti-pattern
O58|Side Channel|out-of-band path bypassing API; makes governance advisory not enforced|anti-pattern
O59|Shared Account|multiple humans using one credential; defeats attribution|anti-pattern
O60|Aggregate-Built Schema|added piece-by-piece without holding whole; reaches breaking-change ceiling|anti-pattern
O61|Two-OpsDB State|cardinality 2; split-brain ops; failure state between 1 and N|anti-pattern
O62|Documentation Metadata|structured layer over wiki: owners, support, runbook links, last-reviewed|content-type
O63|Runner Metadata|deployment record: identity, purpose, substrate, schedule, targets, owner, support, history|content-type
O64|Centrally-Managed Config|configuration org chose to coordinate via OpsDB rather than fragment|content-type
O65|Change-Mgmt State|pending sets, approval status, approval records, expired/rejected proposals|content-type
O66|Cross-OpsDB Refs Content|in N pattern: structured pointers to entities in other substrates|content-type
O67|SSO Mediation|API delegates auth to identity provider; consumes assertions about caller|principle
O68|Scoped Service Account|per-runner credentials with minimum-necessary access|principle
O69|Read Scaling|read-heavy queries served from cache layer between API and substrate|principle
O70|Rate Limiting|per-identity/per-endpoint limits; abuse detection on anomalous query volume|principle
O71|API as Only Path|single gate; no out-of-band; disciplines enforced not advisory|commitment
O72|Substrate Operator|DBA/infra-eng with audited direct access for maintenance only|role
O73|Schema as Long-Lived Artifact|persists across storage engines, APIs, runner rewrites, library upgrades|principle
O74|Stable Data Churning Logic|architectural layering: schema slow, libs medium, runners fast, integrations fastest|principle

# commitments(id|name|statement|violation_consequence)
OC1|Passive Substrate|OpsDB answers queries+accepts writes; never invokes work|becomes orchestrator; stateful complex fragile
OC2|API as Only Path|no SSH/out-of-band/shadow paths; substrate ops exception under separation-of-duties|governance becomes advisory; OpsDB claims unreliable
OC3|Storage Engine Independence|schema is design; engine is implementation choice|locked into vendor; migration impossible
OC4|API Holds All Governance|auth/authz/validation/change-mgmt/versioning/audit at gate uniformly|policy fragments; substrate contaminated; non-uniform enforcement
OC5|Decentralized Work Shared Substrate|many runners many substrates; OpsDB rendezvous not orchestrator|runners couple to each other; orchestrator drift
OC6|Configuration as Data|schedules/policies/runner-enum/rules/retention/escalation are data|logic embedded in code; data outlives logic principle violated
OC7|Service Pointers First-Class|directory of where every fact lives is structured content|fragmentation returns; ad-hoc lookup
OC8|Local Replicas Valid|any host can hold dumped slice for partition tolerance|partition fails ops; bootstrap impossible
OC9|Schema Evolution Governed|schema changes go through change-mgmt with stricter rules|schema drifts; long-lived artifact lost
OC10|No 2|cardinality 1 or N; never 2|split-brain; drifting schemas; uncoordinated governance

# content(id|category|what_it_is|sot|versioned)
CT1|Centrally-Managed Config|org's coordinated configuration: network, deploy, on-call, escalation, retention, alerts, security, scheduling|opsdb|yes
CT2|Cached Observed State|pulled snapshots from authorities; sized to DOS; freshness varies by populator|authority|no
CT3|Authority Pointers|typed pointers to where facts live: prom server+metric, vault path+version, wiki url+verified-ts|opsdb|yes
CT4|Service Directory|structured lookup for operational questions: where-metric, where-log, where-runbook, who-on-call, which-cluster|opsdb|yes
CT5|Schedules and Calendars|when runners/backups/expirations/rotations/audits happen; aggregated calendar views|opsdb|yes
CT6|Runner Enumeration|deployment metadata records; not source code|opsdb|yes
CT7|Documentation Metadata|owners, stakeholders, support, runbook links, last-reviewed, dashboards|opsdb|yes
CT8|Policies|security zones, compliance, data classification, escalation, change-mgmt, retention, schedule|opsdb|yes
CT9|Version History|per-entity history of every change with attribution; retention per type|opsdb|self
CT10|Audit Log|append-only every API action with identity/timestamp/action/target|opsdb|append-only
CT11|Change-Mgmt State|pending sets, approval status, records, expired/rejected proposals|opsdb|yes
CT12|Cross-OpsDB References|in N pattern: typed pointers to entities in other substrates|opsdb|yes
# scope_note: full operational reality not just server/network/cloud
# includes: tape-backups|password-rotations|cert-renewals|vendor-contracts|dns-expirations|compliance-calendars|on-call|keycard-deactivation|laptop-patch-status|internal-ssl-inventory|playbook-refs|vendor-account-creds|any-org-followup-work

# populations(id|name|access_pattern|use_modes|scope)
P1|Humans|exploratory navigation; UI on top of API; submit change sets|investigate-incidents|plan-changes|query-state|build-dashboards|review-approvals|scoped-rw-by-domain
P2|Automation|structured narrow; per-runner credentials; minimum-necessary access|read-config|write-cache|write-results|propose-changes|narrow-per-runner-scope
P3|Auditors|read-only broad; verification-oriented; findings produce change sets|verify-controls|read-history|read-evidence|read-policies|read-only-comprehensive

# flows(id|name|trigger|path|terminal)
OF1|Configuration|human/automation submits change set|API validates schema+policy → records pending → evaluates approval rules → notifies approvers → collects approvals → atomic commit when satisfied → runners read on next cycle|new config current; full trail queryable
OF2|Cached Observation|puller scheduled cycle|queries authority via shared lib → transforms to schema → writes via API with scoped creds → audit logged but not change-managed|cache updated with timestamp; consumers decide if fresh enough
OF3|Reconciliation|reconciler scheduled cycle|reads desired+observed from OpsDB → computes diff → for each diff: act-via-lib OR propose-change-set OR log-and-defer → writes results back|observed driven toward desired within authorization
OF4|Verification|verifier scheduled cycle matched to subject schedule|queries authority → compares to expected → writes structured evidence record (pass/fail with detail) via API|evidence queryable by auditors and operators
OF5|Investigation|human starts from symptom (alert/report/anomaly)|query entity → query version history → query cached observed → follow authority pointers → query on-call/ownership|picture assembled in operator's head from structured queries
OF6|Audit|auditor read-only scoped role|query audit log+version history+change-mgmt records+evidence+policies (with time/type filters)|findings filed as audit data; corrective change sets through standard discipline
OF7|Service Pointer Lookup|caller asks where-is-X|OpsDB returns authority coordinates → caller queries authority directly with coords|one query to OpsDB plus one to authority; OpsDB stays out of live-data path
OF8|Local Replica|operator/runner needs partition tolerance|dump OpsDB slice with version stamp → host operates against local replica during partition → on reconnect: refresh+writeback any changes made|fast local during normal+disconnected; partition-tolerant ops
OF9|Cross-OpsDB|caller queries one OpsDB; response includes ref to entity in another|first API decides whether to include ref → second API decides whether to answer based on caller identity → caller queries second if authorized|reads federate with policy; writes typically separate per substrate
OF10|Schema Evolution|propose new entity-type/relationship/field|stricter approval rules → forward+backward compat validation → approve → schema updated → existing data conforms or migrates|schema versioned and audited; readers continue working
OF11|Emergency Change|on-call detects production incident|change set with emergency=true → commits with reduced approvals → flagged in audit log → post-incident review triggered → corrective change sets if needed|recorded as emergency; reviewed retroactively; not abused
OF12|Bulk Change|coordinated multi-entity operation needed|single change set with N changes → one approval cycle → atomic commit OR none|coordinated changes don't pass through partial state

# boundaries(id|not_a|why_not|belongs_in)
B1|Wiki|long-form prose/design rationale/diagrams not structured|wiki+notion+equivalent; OpsDB holds pointers
B2|Monitoring System|cant store full time-series at every interval; cant compete with prom/datadog primitives|prometheus+datadog; OpsDB holds cached subset+pointers
B3|Code Repository|artifacts have own tooling: ci/cd+registries+package-repos|git+container-registries; OpsDB holds metadata
B4|Binary Distribution|distribution has its own systems|ci/cd+packaging; OpsDB knows runners deployed not how
B5|Orchestrator|invoking runners violates passive commitment; turns into control plane|runners' own scheduling; OpsDB consulted not directing
B6|Chat System|discussion+coordination not data; OpsDB holds pointers to threads|slack+teams+equivalent
B7|Ticketing System|incidents+work-tracking+pm have own systems|jira+linear+equivalent; OpsDB references them
B8|Secrets Manager|secrets need-to-know+audit-on-read+ephemeral; not OpsDB semantics|vault+equivalent; OpsDB holds path+version pointers
B9|World SPOF|services fail if OpsDB runtime dependency; arch wrong if so|runners cache or templated; graceful degradation built in
B10|Unstructured Store|free-text fields are bounded; not dumping ground|wiki+document-store+search-index; OpsDB references
B11|Single-Population System|privileging machines or humans misses point|both first-class; same API both consume

# cardinality(id|state|justification|valid)
CR1|0|absence of coordination substrate; ad-hoc human-driven ops|valid-but-immature
CR2|1|single security umbrella; one trusted population; one identity provider; one compliance scope|valid-target
CR3|N-security-perimeter|breach of one substrate must not expose another; API-layer authz insufficient|valid
CR4|N-legal-regulatory|GDPR+sectoral+sovereignty require physical residency|valid
CR5|N-org-boundaries|business units operating as separate companies; recent acquisitions; federated structures|valid
CR6|N-human-comm-boundaries|teams not sharing processes/conventions; coordination cost exceeds benefit|valid
CR7|N-air-gap|classified+industrial-control require physical isolation|valid
CR8|2|split-brain; drifting schemas; two governance models; two audit trails|invalid-failure-state
CR9|N-technical-fragility|"protect prod from corp tooling experiments"|invalid; signs of bad ops not structural
CR10|N-convenience|"two would be easier"|invalid; convenience not structural; overhead exceeds gain
CR11|N-premature|"we might need to split eventually"|invalid; stay-1 until structure forces N
CR12|N-performance|"one cant serve our query load"|invalid; scale within single OpsDB via replicas/sharding/cache

# n_architecture(rule|content)
N1|each-OpsDB-has-identity|named addressable distinguishable; cross-refs include substrate id
N2|cross-refs-first-class|typed pointer: substrate-id + entity-locator + policy-hints
N3|federated-reads-with-policy|each API enforces what's resolvable from calling context
N4|cross-writes-typically-not-supported|each substrate own write authority
N5|same-code-same-schema-separate-substrates|N instances of same design not N products
N6|operators-may-differ|gov-zone vs commercial-zone may not share personnel when threat model demands

# api_layers(layer|enforces|notes)
AL1|Authentication|SSO+identity-provider integration; service accounts per runner|delegates to IdP; consumes assertions
AL2|Authorization|group/role-based; per-entity-type/per-namespace/per-field|access policies are themselves OpsDB data
AL3|Validation|schema+value-constraints+referential-integrity+semantic-checks|cross-field invariants; policy-driven; conflict detection
AL4|Change Management|proposal→routing→approval→atomic commit|insufficient approvals expire after deadline
AL5|Versioning|automatic version on every committed change|retention per entity type
AL6|Audit|every action recorded append-only|optional cryptographic chaining
AL7|Rate Limiting|per-identity+per-endpoint limits; anomaly detection|limits themselves are policy data
AL8|Read Scaling|tenant-aware cache between API and substrate|cache key includes access scope
AL9|API Versioning|contract changes managed; old supported until migration|distinct from schema versioning

# what_versioned(item|versioned|reason)
WV1|Centrally-managed config|yes|primary source-of-truth data
WV2|Policies|yes|expressed against schema; query-as-of-time needed
WV3|Schedules|yes|change history matters for audit
WV4|Documentation metadata|yes|owner changes need attribution
WV5|Schema|yes|stricter approval; forward+backward compat
WV6|Access control rules|yes|who-had-access-when answerable
WV7|Cached observed state|no|too high-volume; authority is SoT
WV8|Audit log|no|append-only by construction; not modified
WV9|Runner result writes|no|append-only evidence; modification defeats purpose

# change_mgmt_scope(item|gated|reason)
CM1|Configuration changes|yes|expresses intent
CM2|Schedule changes|yes|expresses intent
CM3|Runner registration|yes|expresses intent
CM4|Policy changes|yes|expresses intent
CM5|Metadata changes|yes|expresses intent
CM6|Schema changes|yes|stricter rules; expresses intent
CM7|Access control changes|yes|expresses intent
CM8|Cached observation writes by pullers|no|records observation; world changed
CM9|Runner result writes|no|records event; not change of intent
CM10|Audit log entries|no|created automatically by API
# pattern: intent→gated; observation→ungated

# compliance_map(regime|requirement|opsdb_provides)
CP1|SOC2-Security|access control records|access policies+audit log+change mgmt
CP2|SOC2-Availability|scheduled maintenance+incident records|schedules+observed state history
CP3|SOC2-Processing-Integrity|validation+change approval|api validation rules+approval records
CP4|SOC2-Confidentiality|data classification+access policies|policy data+access policies
CP5|SOC2-Privacy|residency+retention|substrate location+retention policies
CP6|ISO27001-A.5|infosec policies|policy data
CP7|ISO27001-A.6|org of infosec|ownership+accountability data
CP8|ISO27001-A.8|asset management|entity registry
CP9|ISO27001-A.9|access control|access policies+audit log
CP10|ISO27001-A.12|operations security|change mgmt+monitoring
CP11|ISO27001-A.16|incident management|incident records+response actions
CP12|PCI-DSS-7|restrict access by need-to-know|access policy data
CP13|PCI-DSS-10|track and monitor access|audit log
CP14|PCI-DSS-11|regularly test security|scheduled scan records+evidence
CP15|HIPAA-Security|technical safeguards|data classification+access controls+audit logging+operational records
CP16|HIPAA-Privacy|same|same
CP17|GDPR-Article-30|records of processing activities|entity records: what data+purpose+systems+retention+jurisdiction
CP18|SOX-IT-General-Controls|change mgmt+SoD+control operation evidence|change records+SoD rules+enforcement records+audit log

# audit_properties(audit_need|opsdb_property)
AP1|Tamper-evident records|versioning+audit log+optional cryptographic chaining
AP2|Attribution of every action|API authentication on every write
AP3|Authorization trail|change management approval records
AP4|Point-in-time reconstruction|version history per entity
AP5|Control effectiveness evidence|runner-produced verification records
AP6|Segregation of duties enforcement|change mgmt rules + approval records
AP7|Access review|SSO+groups+queryable access policies
AP8|Data residency proof|substrate location + (N-pattern) physical separation
AP9|Retention policy|configurable per-entity-type history retention
AP10|Read-only auditor access|scoped read role in API
# native_consequence: not bolted on; same disciplines serving humans+automation produce audit-grade properties

# disciplines(id|name|statement|failure_if_skipped)
D1|Comprehensive Thinking Aggregate Building|hold whole in mind while adding pieces; never aggregate-think|schema reaches breaking-change ceiling
D2|Top-Level Cuts Done Early|major axes identified before populating; entity classes/relationships/schedules/policies/evidence/history|forces costly refactoring later
D3|Slicing the Pie Ongoing|every new domain examined for fit; refine schema when needed not fragment|schema drifts to aggregate
D4|Schema as Long-Lived Investment|decade-scale consequences; ongoing artifact|treated as deliverable; ages poorly
D5|Adding Without Breaking|additive when possible; deprecation cycles for breaking changes|breaks consumer migrations; long deprecation periods
D6|Versioning Schema Itself|schema changes go through change mgmt|drift; loss of decision history
D7|Resist Fragmentation|absorb special cases via new entity types/namespaces/permissions|drift to bag-of-stores
D8|Resist Feature Creep|refuse orchestration/ticketing/monitoring/chat additions|violates boundaries; compromises design
D9|Invest in API|sophistication compounds: validation/workflows/queries|stays simple but becomes inadequate; pressure to bypass
D10|Invest in Shared Library Suite|library quality determines runner quality|runners reinvent basics inconsistently
D11|Documentation as System Component|self-describing through schema; prose lives in wiki referenced from OpsDB|prose drifts from reality
D12|Schema Steward Role Defined|continuous responsibility for whole|schema drifts to aggregate without owner

# starting_points(step|action|purpose)
SP1|1|top-level taxonomy first|get shape sliced before populating
SP2|2|pick painful/valuable domain|not greenfield; real operational stake
SP3|3|slice that domain|entities+relationships+schedules+policies+evidence+authorities
SP4|4|build substrate and API with disciplines|portable across engines; auth+validation+change+versioning+audit
SP5|5|build a runner or two|forces schema to be useful not just elegant
SP6|6|do another domain|second domain refines top-level taxonomy
SP7|7|keep going|each domain refines schema; each runner confirms usefulness
# no_ceremony: no "schema finished"; just "covers what matters absorbs new things cleanly"

# runner_layering(layer|churn|examples)
RL1|Schema|slow|entity types+relationships+fields; decade-scale
RL2|Shared Libraries|medium|k8s lib+cloud lib+vault lib+opsdb client+log/metrics+retry+idempotency+ssh+notification
RL3|Runners|fast|pvc-repair+credential-rotator+tape-verifier+cert-checker+drift-reconciler
RL4|Integrations|fastest|specific authority adapters and dashboard glue

# runner_examples(id|kind|behavior)
RX1|Tape Backup Verifier|matches backup schedule; queries storage api+IMAP for confirmation email; compares to expected backup id; writes pass/fail evidence
RX2|Credential Rotator|on schedule rotates credential C; records new id+systems updated; bulk change set if many consumers
RX3|Compliance Scanner|checks policy P against entity set E; writes M-pass+N-fail evidence with failure list
RX4|PVC Repair Runner|~200 lines: 150 specific logic + 50 glue using shared libs; small enough to audit
RX5|Drift Reconciler|reads desired+observed; computes diff; corrects via shared lib OR proposes change set OR logs-and-defers

# relationships(from|rel|to)
O1|enforces|OC1
O1|enforces|OC2
O1|enforces|OC3
O1|enforces|OC4
O1|enforces|OC5
O1|enforces|OC6
O1|enforces|OC7
O1|enforces|OC8
O1|enforces|OC9
O1|enforces|OC10
OC1|prevents|O52
OC2|prevents|O58
OC1|prevents|O54
O41|enables|OC3
O44|prevents|O57
O44|prevents|O60
O45|prevents|O49
O45|prevents|O50
O45|prevents|O51
O45|prevents|O52
O42|prevents|O61
O20|prevents|O59
OC10|prevents|O61
O6|reads_from|O1
O6|writes_to|O1
O6|uses|O7
O6|enumerated_in|O63
O29|subtype_of|O6
O30|subtype_of|O6
O31|subtype_of|O6
O28|subtype_of|O6
O29|writes|O9
O30|writes|O22
O31|reads|CT1
O31|reads|CT2
O22|read_by|P3
O18|read_by|P3
O17|read_by|P3
O11|specialization_of|O10
O10|stored_in|CT3
O11|stored_in|CT4
O3|pointed_to_by|O10
O7|enforces_principle|RL2
O73|requires|D4
O74|describes|RL1
O74|describes|RL2
O74|describes|RL3
O74|describes|RL4
P1|access_through|AL1
P2|access_through|AL1
P3|access_through|AL1
P1|submits|O5
P2|submits|O5
O5|gated_by|AL4
O5|atomic|true
O25|instance_of|O5
O24|instance_of|O5
O16|computed_by|AL4
O21|enforced_by|AL4
O8|maintains|D12
O67|implements|AL1
O68|implements|AL2
O69|implements|AL8
O70|implements|AL7
O36|component_of|O69
O35|property_of|O31
O32|deployment_of|O6
O33|deployment_of|O6
O34|deployment_of|O6
O12|enables|OF8
O37|enables|OF9
O38|component_of|O37
O39|constrains|OF9
O26|gated_by|OC9
O27|property_of|O26
O40|distinct_from|O26
O23|enabled_by|AP1
O23|enabled_by|AP4
O19|implements|AP1
O20|implements|AP2
O21|implements|AP6
O22|implements|AP5
CR2|target_for|small-orgs
CR8|forbidden|true
CR9|rejection_for|technical-fragility
CR10|rejection_for|convenience
CR11|rejection_for|premature-optimization
CR12|rejection_for|performance
B1|redirects_to|wiki
B2|redirects_to|prometheus-datadog
B5|prevents|O52
B8|redirects_to|vault
B9|prevents|O54
D1|prevents|O60
D7|prevents|O57
D8|prevents|O45
D8|prevents|O49
D8|prevents|O50
D8|prevents|O51
D9|investment_target|api
D10|investment_target|libraries
SP1|prereq_of|SP3
SP4|enables|SP5
SP5|enables|SP6
WV7|exception_to|O17
WV8|exception_to|O17
WV9|exception_to|O17
CM8|exception_to|O5
CM9|exception_to|O5
CM10|exception_to|O5
RX1|instance_of|O30
RX2|instance_of|O6
RX3|instance_of|O30
RX4|instance_of|O31
RX5|instance_of|O31

# section_index(section|title|ids)
2|Terminology and Context|O1,O2,O3,O4,O5,O6
3|Design Goals|O4,O41,O73,O27,OC8
4|Architectural Commitments|OC1,OC2,OC3,OC4,OC5,OC6,OC7,OC8,OC9,OC10
5|Cardinality Rule|CR1,CR2,CR3,CR4,CR5,CR6,CR7,CR8,CR9,CR10,CR11,CR12,N1,N2,N3,N4,N5,N6,O42,O61
6|Content Scope|CT1,CT2,CT3,CT4,CT5,CT6,CT7,CT8,CT9,CT10,CT11,CT12,O62,O63,O64,O65,O66
7|Three Consumer Populations|P1,P2,P3
8|API as Governance Perimeter|AL1,AL2,AL3,AL4,AL5,AL6,AL7,AL8,AL9,O67,O68,O69,O70,O71,O72
9|Versioning and Change Management|WV1,WV2,WV3,WV4,WV5,WV6,WV7,WV8,WV9,CM1,CM2,CM3,CM4,CM5,CM6,CM7,CM8,CM9,CM10,O5,O17,O24,O25,O26
10|Audit and Compliance|CP1,CP2,CP3,CP4,CP5,CP6,CP7,CP8,CP9,CP10,CP11,CP12,CP13,CP14,CP15,CP16,CP17,CP18,AP1,AP2,AP3,AP4,AP5,AP6,AP7,AP8,AP9,AP10,O18,O19,O20,O21,O22,O23
11|Runners and Shared Libraries|O6,O7,O29,O30,O31,O32,O33,O34,O35,O63,RL1,RL2,RL3,RL4,RX1,RX2,RX3,RX4,RX5
12|Data Flow Patterns|OF1,OF2,OF3,OF4,OF5,OF6,OF7,OF8,OF9,OF10,OF11,OF12
13|What Does Not Belong|B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,B11,O49,O50,O51,O52,O53,O54,O55,O56
14|Construction Discipline|D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,D11,D12,O8,O42,O43,O44,O45,O46,O47,O48,SP1,SP2,SP3,SP4,SP5,SP6,SP7

# decode_legend
categories: term|principle|commitment|content-type|population|flow|anti-pattern|role|discipline
rel_types: enforces|prevents|enables|requires|implements|reads_from|writes_to|uses|enumerated_in|subtype_of|specialization_of|stored_in|pointed_to_by|read_by|component_of|property_of|deployment_of|gated_by|computed_by|enforced_by|maintains|distinct_from|enabled_by|target_for|forbidden|rejection_for|redirects_to|investment_target|prereq_of|exception_to|instance_of|writes|reads|describes|atomic
sot_values: opsdb|authority|self|append-only
versioned_values: yes|no|self|append-only
valid_values: valid|valid-target|valid-but-immature|invalid-failure-state|invalid
