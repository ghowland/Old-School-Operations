# OPSDB INTRODUCTION — LLM-COMPACT FORM
# Format: pipe-delimited tables, ID refs.
# Read order: definition → fragmentation → content → boundaries → gate → runners → populations → schema → capabilities → workflows → unchanged → compounding → arch-commitments → org-commitments → ops-disciplines → starting → economics → series-guide → relationships → sections

# definition(aspect|content)
DEF1|what|centralized data substrate holding full operational reality of organization
DEF2|access|single API gate enforcing authentication+authorization+validation+change-management+versioning+audit uniformly
DEF3|consumed by|three populations: humans+automation runners+auditors via scoped permissions
DEF4|active layer|small fleet of decentralized runners reads from OpsDB+acts in world via shared libraries+writes results back
DEF5|substrate posture|passive; never invokes work; answers queries+accepts writes
DEF6|schema is itself data|declared in YAML files in git repo+evolved through same change-management discipline as any operational change
DEF7|core principle|data is king logic is shell at every layer

# fragmentation(id|aspect|manifestation|cost)
IF1|configuration scattered|cloud consoles+K8s manifests in git+Salt/Ansible inventories+vault paths+DNS providers+Prometheus YAML+Datadog UI+IdP admin consoles|operator updates one tool and tries to remember to update others; drift between tools
IF2|observed state scattered|monitoring stacks per team+per domain|no unified picture of system health
IF3|documentation scattered|wikis+Notion+README+shared drives+screenshots|stale runbooks; unknown ownership
IF4|audit evidence scattered|tickets+Slack threads+email archives+screenshots|audit response is multi-week binder assembly project
IF5|investigation pattern|operator opens PagerDuty→Slack→Grafana→kubectl→wiki→git mentally assembling picture|operator holds picture in head; high cognitive load; longer MTTR
IF6|configuration drift|Salt correct but wiki stale; cloud console updated but capacity sheet not; alert added but runbook missing|silent divergence accumulates until incident reveals it
IF7|automation duplication|teams build similar scripts independently because no way to know other teams' work|wasted effort+inconsistent failure modes
IF8|natural cost framing|orgs live in this state long enough that costs feel natural|architectural choice that could be different becomes invisible

# content_held(id|category|examples)
IH1|centrally-managed configuration|service definitions+deployment specs+on-call rotations+escalation+retention+alert thresholds+security policies
IH2|cached observed state|K8s pod status+cloud resource state+recent metric summaries+IdP group memberships|with timestamps so consumers know age
IH3|authority pointers|which Prometheus server holds which metric+which cluster runs which service+which vault path holds which secret+which wiki page documents which service
IH4|schedules|when runners run+backups happen+certs expire+credentials rotate+compliance audits due+manual tasks scheduled (tape rotation+vendor review+license renewal)
IH5|runner enumeration metadata|what automation exists+what each runner does+where it runs+what it affects+who owns it (NOT runner code)
IH6|structured documentation metadata|owners+stakeholders+support teams+runbook references+dashboard references+last-reviewed dates
IH7|policies|security zones+compliance scopes+data classifications+escalation paths+change-mgmt rules+retention policies
IH8|version history|every prior state of every centrally-managed entity reconstructible to retention horizon
IH9|audit log|every API action recorded with identity+timestamp+action+target; append-only at strictest level
IH10|change-management state|pending change_sets+approval status+approval records+rejected proposals
IH11|evidence records|outcomes of verification work (did backup happen+did cert renew+did compliance scan pass)
# scope: comprehensive operational reality including tape rotations+vendor contracts+cert inventories+keycard deactivation+laptop patch status+CA cert renewals+DR restoration tests; not just server/network/cloud

# content_not_held(id|not_held|held_in_instead)
IB1|long-form prose (wiki pages+design docs+rationale narratives)|wiki+document store; OpsDB has structured pointers with last-reviewed metadata
IB2|time-series at full resolution|Prometheus+Datadog+CloudWatch; OpsDB holds enough cached recent state for operational reasoning
IB3|code (runner+package+container images)|repositories+registries; OpsDB holds image references+repo URLs+version tags
IB4|secrets|Vault+equivalents; OpsDB holds pointers to vault paths never values
IB5|discussion|Slack+Teams+chat; OpsDB has authority pointers to threads where context needed
IB6|tickets|Jira+Linear+ServiceNow; OpsDB references tickets where appropriate
IB7|orchestration|runners run on own schedules through own scheduling primitives; OpsDB consulted by them not directing them
IB8|runtime dependency for live services|already-running services keep running when OpsDB unreachable; runners with cached/templated config continue; OpsDB is coordination substrate not data plane
# rule: each boundary kept makes OpsDB better at what it does and lets each external system do what it does well; crossing weakens both

# gate_enforces(id|enforcement|content)
GE1|Authentication|humans via IdP+runners via secret backend; every action attributable
GE2|Authorization|five layers compose: standard role/group+per-entity governance+per-field classification+per-runner declared scope+policy rules; all five must pass
GE3|Validation|schema match+bounds within declared+referenced entities exist+no semantic invariant policy violation
GE4|Change Management|for changes to centrally-managed data; API computes who must approve+records change_set in pending state+waits
GE5|Versioning|when data updated prior state preserved in version history; reconstruction at any past time is one query
GE6|Audit|every action successful or rejected produces audit log entry with full attribution
# substrate underneath API is simple: relational database stores what API hands it; complexity lives in API where uniform and inspectable; substrate stays portable across storage engines because not contaminated with policy logic

# runner_pattern(id|aspect|content)
RP1|one sentence|get from OpsDB+act in world+set to OpsDB
RP2|each runner|small single-purpose 200-500 lines runner-specific logic; shared libraries do heavy lifting
RP3|reads|configuration from runner_spec_version+desired state+observed state+target lists+policies
RP4|acts|in world via standardized shared libs (K8s client+cloud SDKs+vault+OpsDB API client+retry+logging+notifications+SSH+git)
RP5|writes|runner_job rows+output_var rows+evidence_record rows+change_set proposals
RP6|coordinates implicitly|through OpsDB rows; runner A writes row+runner B reads on next cycle; OpsDB is rendezvous
RP7|loose coupling|crashed runner blocks no other runner; can be replaced+restarted+retired without affecting others
RP8|shared library suite|enforces one-way-to-do-each-thing; without it every runner reinvents basics inconsistently (same fragmentation problem at runner layer)

# runner_kinds(id|kind|role)
RK1|Pullers|read from authorities (Prometheus+K8s API+cloud control planes+IdP) write cached state into OpsDB; most numerous in mature OpsDB
RK2|Reconcilers|compare desired vs observed and act to close gap; K8s operator pattern generalized across all operational domains
RK3|Verifiers|check scheduled work happened or scheduled state correct; produce evidence records
RK4|Drift Detectors|compare desired vs observed and propose corrections via change_set rather than acting directly
RK5|Change-Set Executors|read approved change_sets and apply field changes through API
RK6|Reapers|apply retention policies trimming past-horizon data
RK7|Schedulers|read schedule data and enforce on whatever substrate target runs on (cron+systemd timer+K8s CronJob)

# populations(id|population|access_pattern|use)
P1|Humans|exploratory; UIs sitting on API|investigate incidents+plan changes+query state+build dashboards+propose changes+review approvals
P2|Automation runners|structured per-runner narrow scope|read OpsDB to know what to do+write back to record what they did
P3|Auditors|read-only scoped|verify controls operating; broad scope; read-heavy focused on history and structure
# soft power: same data through same gate with scoped access; disciplines applied for one population produce benefits for others as side effect
# change-mgmt for humans → audit evidence for auditors
# versioning for rollback → point-in-time reconstruction for auditors
# schedule data for runners → compliance task tracking for auditors
# structured ownership for human routing → accountability evidence for auditors

# schema(id|aspect|content)
S1|schema is data|YAML files in git repo
S2|loader produces|both relational database structure AND API validation metadata from same source
S3|closed bounded vocabulary|9 types (int+float+varchar+text+boolean+datetime+date+json+enum+foreign_key) + 3 modifiers (nullable+default+unique) + constraints (range bounds+length bounds+enum sets+FK references)
S4|forbids|regex+embedded logic+conditional constraints+inheritance+templating
S5|evolution flows through change management|new entities+new fields+widened ranges all change_sets reviewed via git workflow+applied through schema_change_set
S6|forbidden in evolution|no field deletions+no renames+no type changes; type changes via duplication and double-write+old field becomes tombstone never removed
S7|why discipline|consumers can trust fields read by name will always exist; audit log entries from years ago remain interpretable; version history rows reference fields that still mean what they meant; cost is occasional schema gymnastics+benefit is decade-scale stability

# capabilities(id|capability|what_it_means|enables)
IC1|One Place to Find Any Operational Fact|every operational fact has one authoritative location either held directly or pointed at|investigation no longer requires knowing N tools; mental load of "where does this live" collapses to one query
IC2|Continuous Queryable Audit|every change goes through gate+every operation produces audit log+every change_set has approval trail+every entity has version history|"show me every production config change in last quarter and who approved each" is query result not binder assembly project; compliance becomes property of system not quarterly fire drill
IC3|Mechanical Change Governance|every change to centrally-managed data flows through change_sets; validation+approval+record+executor application|SoD enforceable as policy rules; approval scales with risk; emergency changes have break-glass with mandatory post-hoc review; discipline mechanically enforced not maintained through process docs and tribal knowledge
IC4|Decentralized Work with Central Coordination|many small pieces of automation each independent; no orchestrator+no SPOF+no fragile in-memory coordination|coordination through shared data; runners replaceable/restartable/retirable without affecting others; 50-runner and 500-runner orgs structurally similar
IC5|Point-in-Time Reconstruction|version history makes "what did this look like at time T" a single query|incident investigation+audit period boundary state+rollback as change_set restoring prior values
IC6|Schema Stability Across Decades|forbidden list (no deletions+renames+type changes) means consumers can trust schema|runner written 5 years ago still runs against same field names; audit log entries from any past point remain interpretable
IC7|Mechanical Defense Against Operator Error|schema rejects malformed writes+change-mgmt routes high-stakes to humans+validation checks invariants+bulk atomic+optimistic concurrency catches stale state+runner report keys reject undeclared|none prevent every error but each closes off a category that otherwise produces incidents
IC8|Observability of Operations Itself|"which runners are running"+"which haven't run in 24h"+"which are hitting bounds"+"which change_sets pending longer than expected" are direct queries|operations as a function becomes inspectable; patterns become visible (runner hitting retry budget points at unhealthy authority etc)
IC9|Vendor Substrate Independence|self-contained operational software not built on cloud/orchestrator/commercial platform; schema portable across storage engines|reorganization replacing cloud or swapping orchestrator does not require replacing OpsDB; the OpsDB persists as tools and platforms come and go on multi-year cycles
IC10|Compounding Benefits|each capability strengthens others|continuous audit possible because every change goes through gate; gate is uniform because no out-of-band path; lack of out-of-band paths enforceable because schema and API are only way to interact; schema stable because closed vocabulary forbids breaking changes; consumers simple because schema stable; many consumers exist because they're simple; breadth of consumers produces comprehensive coverage; none stand alone

# workflows(id|scenario|before|after|key_change)
W1|Investigation During Incident|page→Slack→Grafana→kubectl→wiki→git tour of tools assembling picture mentally|page links to service incident view resolving runbook ref+dashboard URLs+recent change_sets+evidence records+dependent services+upstream on-call|trail composes itself; next person investigating similar incident next quarter has queryable record
W2|Deployment|developer PR→CI→Argo CD/kubectl apply→hope it worked→Datadog check maybe|change_set→validation→approval→executor applies OpsDB-side+signals via output var→specialized runner performs world-side action→deploy watcher records rollout→digest verifier writes evidence|trail is one query joining several tables; auditor querying "every prod deployment last quarter" gets structured result with digests+approvers+timestamps+verification outcomes
W3|Certificate Renewal|cron job runs cert-manager/ACME hopefully|cert inventory in OpsDB+each cert has expiration_schedule+renewal runner reads+performs renewal+writes evidence each cycle+drift detector confirms in place+compliance_finding if fails|cert inventory queryable; "show me every cert expiring in next 90 days" is direct query; failure pattern that fails silently becomes routine query
W4|Compliance Evidence Collection|auditor arrives→requests→team scrambles for weeks across Jira+Slack+email+screenshots+vault logs→assembles binder→auditor accepts on faith samples a few items|continuous compliance is property of system; verifier runners produce evidence records on every cycle; auditor receives read-only scoped access+queries same data team queries|audit moves from quarterly project to routine query; same vocabulary because same schema; verification of mechanism not assembly of evidence
W5|Drift Correction|drift accumulates silently for months; nobody knows until next incident or manual audit|drift detector reads desired+observed each cycle+computes diff+auto-corrects via change_set per policy or files finding for human review|drift never accumulates past one detection cycle; structured visibility into "what is currently drifted and why"
W6|Onboarding New Automation|team writes script lives somewhere in their repo+runs on team-owned cron+other teams don't know it exists+credentials hardcoded+logs to own destination+failures only owning team notices|team writes runner against shared lib suite+registers runner_spec via change_set declaring purpose+schedule+target scope+capabilities+report keys; deployed via normal CI/CD|adding new automation is structurally additive; doesn't disturb existing runners; contributes to comprehensive coverage rather than becoming yet another disconnected slice
W7|Schema Evolution|migration scripts tested in staging then run in production with held breath; sometimes break consumers in non-apparent ways; DDL is one SoT+validation logic in API is another+they drift|schema changes are change_sets against schema repo→reviewed via git workflow→CI generates schema_change_set→same approval pipeline→executor applies DDL atomically+updates schema metadata|schema repo and OpsDB stay synchronized by construction; forbidden list means changes mechanically additive; consumers written against older schema continue working
W8|Vendor Substrate Transitions|replacing cloud is multi-year project+replacing config-mgmt tool multi-quarter+replacing monitoring stack involves rewriting dashboards+each transition involves rewriting integrations+rebuilding institutional knowledge+accepting outages|write new pullers for new cloud's authorities+deprecate old when migration completes+update authority pointers as resources move; typed payload pattern accommodates both providers; existing entity rows reference new provider via authority pointers; non-cloud-specific runners keep working unchanged|scope of transition bounded; OpsDB+audit history+most of runner population persists; only world-side adapters change

# unchanged(id|aspect|rationale)
UC1|fundamental work of operations|services still need to run+monitoring still alerts+incidents still happen+capacity still planning+vendors still managed|OpsDB does not eliminate operational work; makes it coordinated
UC2|skill set of operations engineers|still need systems+networking+storage+security+distributed systems failure modes|OpsDB is tool for coordinating not replacement
UC3|organizational dynamics|disagreement about priorities+ownership disputes+communication problems still exist|OpsDB provides shared substrate but humans still have to use it well
UC4|discipline requirement|OpsDB rewards orgs that bring discipline; does not produce discipline|org that cannot maintain SoT+allows fragmentation creep+bypasses gate when convenient will not succeed; OpsDB amplifies capability rather than substituting

# compounding(commitment|enables|next_capability)
CB1|every change goes through gate|continuous audit possible|because every operation produces structured trail
CB2|no out-of-band path|gate is uniform|because alternate paths would make disciplines advisory
CB3|schema and API are only way to interact|out-of-band paths cannot exist|because the path doesn't exist to bypass
CB4|closed vocabulary forbids breaking changes|schema stable across decades|because consumers can trust field names persist
CB5|schema stable|consumers can be simple|because they don't need defensive code for renames/deletes/type changes
CB6|consumers simple|many consumers can exist|because each one is small and knowable
CB7|breadth of consumers exists|comprehensive operational coverage|because operational reality is fully tracked
CB8|comprehensive coverage|the OpsDB delivers what fragmented operations cannot|because the alternative was always fragmentation
# none of the benefits stand alone; each is what makes the next mechanically possible

# arch_commitments(id|commitment|content|failure_if_violated)
AC1|One OpsDB per scope|either one (typical) or N for genuinely structural reasons (security perimeter+legal/regulatory zone+org-boundary independent units)|adding second for convenience or technical fragility is first step toward fragmentation; no stable "two OpsDBs" state
AC2|API is the only path|no SSH-into-database+no out-of-band tools+no shadow paths; direct DB access for substrate operators only under SoD controls narrowly scoped audited|alternate paths make all governance disciplines advisory rather than enforced
AC3|OpsDB is passive|does not invoke runners+fire triggers+push changes+initiate any activity in world; runners drive timing|becomes orchestrator; stateful complex fragile; loses single-gate property
AC4|Substrate is portable|schema does not depend on engine-specific features+API does not expose engine semantics|locked into vendor; migration becomes impossible
AC5|Schema evolution governed|no deletions+no renames+no type changes; closed vocabulary; forbidden list; duplication-and-double-write pattern when types must change|consumers cannot trust schema; long-lived runners break; audit history becomes uninterpretable
AC6|Comprehensive scope|covers all operational data org wants coordinated including domains conventionally left to spreadsheets+tribal knowledge (vendor contracts+manual operations+cert inventories)|partial coverage means partial benefits; fragmentation persists in uncovered domains

# org_commitments(id|commitment|requires)
OC1|Schema steward role|some person/team responsible for comprehensive coherence of schema; reviews schema-evolution change_sets; notices when slicing-the-pie needed; resists fragmentation+feature creep; holds whole in mind across many domains|continuous responsibility (not full-time job in most orgs); senior engineer/architect role; without it schema drifts to aggregate
OC2|Investment in API|API is sophisticated and grows: new validation rules+approval workflows+audit requirements+query patterns; substrate stays simple+API earns complexity|orgs that under-invest end up with database not OpsDB
OC3|Investment in shared library suite|runners cheap because libraries good; suite keeps runner population consistent at scale; new operational domain is candidate for new lib capabilities|investment compounds in cheap runners
OC4|Discipline of refusing fragmentation|every team wanting "small separate OpsDB for our use case" is solving real problem; right response is usually to absorb into existing schema|recurring discipline; pressure for fragmentation is constant
OC5|Discipline of refusing feature creep|OpsDB is not wiki/monitoring/code repo/orchestrator/chat/ticketing/secrets manager; each pressure has real motivation; each is bad idea|refuse and direct each pressure to right system; OpsDB points at it through structured pointers

# ops_disciplines(id|discipline|content)
OD1|Comprehensive thinking aggregate building|schema built incrementally; each piece approached with comprehensive thinking (slicing pie at level being added+asking what's missing+refining when new things don't fit); thinking at level of whole; building at level of piece
OD2|One way to do each thing|within OpsDB-coordinated environment converge on one method per task; shared library suite is framework's enforcement; many almost-identical implementations are failure mode
OD3|Idempotency level-triggering bounding|three load-bearing runner disciplines: idempotent (same inputs same end state); level-triggered where possible (re-evaluate current state on every cycle not depending on event delivery); bounded in every dimension (retry budget+execution time+scope per cycle+queue depth+memory)
OD4|Bound everything|every long-running mechanism has explicit limits; every queue has max depth; every cache has max size; every connection has timeout; every retry has budget; bounds may be very large but must exist
OD5|Reversible changes|prefer mechanisms allowing rollback; rollback is itself change_set restoring prior values; side-channel rollbacks forbidden+everything goes through same pipeline
OD6|Make state observable|what cannot be seen cannot be operated; OpsDB observable about itself by construction; runners produce structured records; audit log queryable; schema metadata describes what exists

# starting_moves(step|action|purpose)
SM1|Top-level taxonomy first|five or six top-level concepts; get shape sliced thoughtfully before populating; comprehensive cuts (substrate+services+runners+schedules+policies+observation+audit) reasonable starting point
SM2|Pick a domain that matters|most painful or most valuable operational domain; could be K8s coordination+cloud resource governance+tape backup tracking+cert inventory; depends on what org actually struggles with
SM3|Slice that domain|entities+relationships+schedules+policies+evidence types+authorities; get schema right for this domain; declare in schema repo
SM4|Build the substrate and API|pick storage engine; build API with disciplines (auth+validation+change mgmt+versioning+audit); build to be portable across storage engines from start
SM5|Build a runner or two in the domain|real runners doing real work reading from and writing to OpsDB; forces schema to be useful not just elegant
SM6|Do another domain|repeat; notice where second domain's needs overlap first; that's where top-level taxonomy gets refined
SM7|Keep going|each domain refines schema+each runner confirms schema useful; eventually OpsDB covers most operational reality; no ceremony of "schema finished"; just "covers what matters and absorbs new things cleanly"
# discipline unchanged from start: comprehensive thinking+aggregate building+slicing-pie when domains added+resistance to fragmentation+feature creep+investment in API+shared libs

# economics(aspect|content)
EC1|Cost is real|building OpsDB is engineering investment; maintaining it is ongoing investment; discipline of refusing wrong things is constant; schema steward is continuous responsibility; investment in API+shared libs compounds over years
EC2|Benefit is real|operations becomes inspectable; compliance becomes continuous; audit becomes query rather than project; new automation is additive rather than fragmenting; schema persists across decades while everything around it evolves
EC3|Trade-off depends|whether costs of fragmentation org currently absorbing (often invisible because absorbed as natural cost) exceed costs of building+maintaining discipline
EC4|For orgs that have lived with fragmentation long enough|to see its costs clearly+the trade is usually obvious

# series_guide(paper|role|when_to_read)
SG1|OPSDB-9|taxonomy of operational mechanisms+properties+principles the OpsDB design draws on|foundational; gives vocabulary for talking about operations in general; explains why OpsDB makes structural choices it does
SG2|OPSDB-2|OpsDB design itself: architectural commitments+cardinality rule (1 or N never 2)+content scope+three consumer populations+API as governance perimeter+construction discipline|the design document; reader who only wants architectural intuition can read this alone
SG3|OPSDB-4|concrete schema demonstration; ~150 entity types across all operational domains|one example schema; org adopting design adapts to specific operational reality but structural patterns transfer
SG4|OPSDB-5|runner pattern in detail: kinds+shared library suite+coordination through shared substrate+three load-bearing disciplines+per-runner change-mgmt gating|how the active layer works
SG5|OPSDB-6|API gate: 10-step gate sequence+five-layer authorization+field-level versioning+optimistic concurrency+change_set lifecycle+runner report keys+audit logging|the active layer where governance happens
SG6|OPSDB-7|how schema itself is constructed: closed constraint vocabulary+schema repo as YAML+forbidden list (no deletions/renames/type changes)+duplication-and-double-write pattern+evolution through change mgmt|how the long-lived artifact is governed
# six papers ordered as they are because each builds on prior; reader serious about implementing should read in order; reader wanting architectural intuition can read OPSDB-2 alone

# relationships(from|rel|to)
DEF1|enables|IC1
DEF2|enables|IC2+IC3
DEF3|enables|continuous-audit-via-shared-data
DEF4|enables|IC4
DEF5|enables|AC3
DEF6|enables|IC6
DEF7|root_principle|all-architectural-choices
IF1|cost_of|IF6
IF1|cost_of|IF7
IF4|cost_of|W4_before
IF5|cost_of|W1_before
IF8|invisible_cost|architectural-alternative-not-considered
IH1|managed_via|change_set_pipeline
IH2|written_by|RK1
IH3|maintained_by|verifier-runners
IH4|read_by|RK7+humans
IH5|registered_via|change_set_pipeline
IH6|maintained_via|change_set_pipeline
IH7|evaluated_at|API-gate
IH8|produced_by|GE5
IH9|produced_by|GE6
IH10|produced_by|GE4
IH11|produced_by|RK3
IB1|prevents|wiki-replacement
IB2|prevents|monitoring-replacement
IB3|prevents|code-distribution-via-OpsDB
IB4|prevents|secrets-store-creep
IB5|prevents|chat-system-creep
IB6|prevents|ticketing-replacement
IB7|prevents|orchestrator-drift
IB8|prevents|world-SPOF
GE1|delegates|IdP+secret-backend
GE2|composes|five-layers-AND
GE3|consults|schema+semantic-invariant-policies
GE4|computed_per|approval_rule-policies
GE5|enables|IC5
GE6|enforces|IC2
RP1|implements|R1
RP6|implements|coordination-through-shared-substrate
RP7|implements|IC4
RP8|enforces|one-way-to-do-each-thing
RK1|writes|cached-observation
RK2|reads|desired+observed
RK3|writes|evidence
RK4|proposes_via|change_set
RK5|drains|approved-not-yet-applied-queue
RK6|enforces|retention
RK7|enforces|schedules
P1|access_through|API
P2|access_through|API
P3|access_through|API
P1|writes|change_sets
P2|writes|observation+evidence
P3|reads|audit+history+evidence+policies
S1|implements|configuration-as-data
S2|prevents|drift-between-DDL-and-validation-code
S3|enforces|bounded-validation-time
S4|prevents|complexity-in-every-consumer
S5|implements|change-mgmt-discipline-on-schema
S6|enables|IC6
S7|trades|short-term-expressiveness-for-long-term-durability
IC1|requires|AC1+AC2
IC2|requires|AC2+GE6
IC3|requires|GE4
IC4|requires|RP6+RP7
IC5|requires|GE5
IC6|requires|S6
IC7|requires|GE3+OD3+OD4
IC8|requires|comprehensive-runner-population
IC9|requires|AC4
IC10|composed_of|all-prior-capabilities
W1|demonstrates|IC1
W2|demonstrates|IC2+RP6
W3|demonstrates|comprehensive-scope+continuous-evidence
W4|demonstrates|IC2-strongest-case
W5|demonstrates|IC7+RP7
W6|demonstrates|IC4-additive-scaling
W7|demonstrates|S5+S6
W8|demonstrates|IC9
UC1|caveat_to|all-capabilities
UC2|caveat_to|skill-replacement-claims
UC3|caveat_to|organizational-determinism
UC4|caveat_to|the-OpsDB-as-magic
CB_ALL|implements|IC10
AC1|prevents|fragmentation-via-OpsDB-multiplication
AC2|prevents|gate-bypass
AC3|prevents|orchestrator-drift
AC4|enables|long-lived-substrate
AC5|enables|long-lived-schema
AC6|enables|comprehensive-benefits
OC1|prevents|schema-aggregate-drift
OC2|enables|API-quality-compounding
OC3|enables|cheap-runner-population
OC4|prevents|fragmentation-creep
OC5|prevents|scope-expansion-creep
OD1|implements|comprehensive-thinking
OD2|implements|one-way-to-do-each-thing
OD3|implements|robust-runner-population
OD4|prevents|unbounded-resource-consumption
OD5|enables|rollback-without-side-channel
OD6|enables|operations-as-inspectable-system
SM1|prereq_of|SM2
SM4|enables|SM5
SM5|forces|schema-usefulness-not-just-elegance
SM6|enables|taxonomy-refinement
SM7|continues|indefinitely-no-ceremony
EC4|frames|adoption-decision

# section_index(section|title|ids)
1|What This Paper Is For|series-context
2|Starting Point Today|IF1-IF8
3|What the OpsDB Is|DEF1-DEF7
3.1|What OpsDB Holds|IH1-IH11
3.2|What OpsDB Does Not Hold|IB1-IB8
3.3|Single API Gate|GE1-GE6
3.4|Runner Pattern|RP1-RP8,RK1-RK7
3.5|Three Populations|P1,P2,P3
3.6|Schema as Data|S1-S7
4|What You Get|IC1-IC10,CB1-CB8
5|How Workflows Change|W1-W8
5.9|What Stays the Same|UC1-UC4
6.1|Architectural Commitments|AC1-AC6
6.2|Organizational Commitments|OC1-OC5
6.3|Operational Disciplines|OD1-OD6
6.4|Starting Move|SM1-SM7
6.5|What This Asks of Org|EC1-EC4
7|Where to Go From Here|SG1-SG6
8|Closing|DEF1-DEF7 restated structurally

# decode_legend
populations: humans|automation|auditors
runner_kinds: puller|reconciler|verifier|drift-detector|change-set-executor|reaper|scheduler
gate_steps: authentication|authorization|validation|change-management|versioning|audit
content_categories: configuration|cached-state|authority-pointers|schedules|runner-metadata|documentation|policies|version-history|audit-log|change-mgmt|evidence
boundaries: prose-in-wiki|time-series-in-monitoring|code-in-repos|secrets-in-vault|discussion-in-chat|tickets-in-ticketing|no-orchestration|no-runtime-dependency
arch_commitment_count: 6
org_commitment_count: 5
ops_discipline_count: 6
starting_step_count: 7
capability_count: 10
workflow_scenario_count: 8
unchanged_count: 4
prior_paper_count: 6
sot_principle: data is king logic is shell at every layer
adoption_principle: comprehensive thinking aggregate building
discipline_principle: refuse the wrong things; reward orgs that bring discipline
economics_principle: trade-off depends on whether org has lived with fragmentation long enough to see costs clearly
rel_types: enables|requires|implements|prevents|enforces|delegates|composes|consults|computed_per|writes|reads|drains|maintained_via|managed_via|registered_via|produced_by|access_through|trades|cost_of|caveat_to|root_principle|invisible_cost|prereq_of|forces|continues|frames|demonstrates|composed_of
