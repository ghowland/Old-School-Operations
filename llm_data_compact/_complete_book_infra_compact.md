# RULES FOR LLMs READING THIS COMPRESSED DOC

## Internal vs spoken labels

The IDs in this doc (RD1, RW1, M19, P03, AC2, etc.) are **internal indexing only**. They exist so you can traverse the relationship graph and locate concepts efficiently. They are **not** the names of the things.

When talking to a human, **never use the internal IDs**. Translate to the human label every time.

## What humans track

Humans track:
- **Names** ("Idempotency," "Reconciler," "Schema steward")
- **Categories** ("a runner discipline," "a Storage-family mechanism," "an architectural commitment")
- **Rules in plain language** ("every action through the API must produce an audit log entry")
- **Roles** ("the schema steward," "the substrate operator")
- **Relationships in plain language** ("Reactors need a Reconciler backstop because edge-triggered loses missed events")

Humans do **not** track:
- ID strings like RD1, M19, AL3
- Table names like `runner_disciplines` or `mechanisms`
- Cross-reference notation like "see SE116 versioned via SE117"

## Translation examples

| Don't say | Say |
|---|---|
| "RD1 requires RP3" | "Idempotency requires that runners persist state in OpsDB, not locally" |
| "AC2 prevents BD16" | "The 'API as only path' commitment prevents the system from becoming a runner framework" |
| "M19 natively provides P21" | "A Journal natively provides Auditability" |
| "Per RG3, this routes to approvers" | "This is an approval-required change, so it routes to human approvers" |
| "See SE125 + SE126-SE131" | "Evidence records have target bridges to services, machines, credentials, certificates, regimes, and manual operations" |

## When IDs are acceptable

Only when the human has explicitly asked for them — for example, "show me the relationship table" or "list every entity by ID." Even then, pair the ID with the name: "SE25 (service)" not bare "SE25."

## The principle

The compressed doc is a tool for you to load structure into context efficiently. The human is having a conversation about operations. Translate at the boundary between your context and theirs every time. The IDs are scaffolding; the human reads the building.

# OPERATIONS MASTER — LLM-COMPACT FORM
# Substrate-agnostic specification of how to do operations
# Format: pipe-delimited tables, ID refs
# Read order: worldview → vocabulary → architecture → schema → active layer → API → libraries → adoption → diagnostics → relationships → sections → legend

# worldview(id|concept|def|category)
W1|Operations|networked/server/datacenter/production mgmt as unified discipline; not domain-specific|term
W2|Control|ability to gather info from + change an environment; central tenet of ops|axiom
W3|Automation|removing classes of work while consistently getting desired results|principle
W4|Class of Work|any category of task humans currently perform|term
W5|Real|physical; has mass; exists in physical world; never fully knowable|term
W6|Virtual|symbolic; non-physical; conceptual; data/logic/words|term
W7|IOSE|Inputs+Outputs+Side-Effects interface; anything modelable as|tool
W8|Universal Machine|anything definable by IOSE; foundation of systemic thinking|tool
W9|Knowability|spectrum of how completely a thing can be known; some virtuals fully knowable some not|term
W10|Data|virtual+symbolic+descriptive; fully knowable; durable+portable+inspectable|term
W11|Logic|executable virtual; code/scripts/decision-trees/state-machines; bound to env+goals|term
W12|Data Source|any mechanism storing data; mandatory feature=access|term
W13|System|interrelated components producing effects; black-boxable as IOSE|term
W14|Systemic Thinking|modeling everything as IOSE network|principle
W15|Philosopher's Knife|tool for slicing concepts without losing the whole|tool
W16|Slicing the Pie|comprehensive subdivision preserving total volume|tool
W17|Comprehensive System|built top-down from whole; internally consistent by construction|principle
W18|Aggregated System|built bottom-up brick-by-brick; never whole; trends to inconsistency|anti-pattern
W19|Internal Consistency|all parts of model agree; superset prereq of Alignment|principle
W20|Alignment|all components consistent + efficient together over time|principle
W21|Engineering|efficient use of resources in environment to yield desired effect|principle
W22|Attribute Axis|spectrum on which a system property is rated|tool
W23|Axiomatic Engineering|decision-making via prioritized attribute axes; impersonal|principle
W24|Impersonal Decision Making|decisions fall out of axes+priorities not personality|principle
W25|Best (anti)|absolute term obscuring tradeoffs; only valid for narrow exact context|anti-pattern
W26|Better|explicit comparison forcing tradeoff articulation|principle
W27|Fashion-Oriented Engineering|copying practices from blogs without context analysis|anti-pattern
W28|Best Practices (anti)|recipes presented as universal; really just case studies|anti-pattern
W29|Production Environment|where revenue/customer-interface/product happens; one per org|term
W30|Security Zone|environment classified by who+what is allowed|term
W31|Operational Logic|code supporting infra; assumes failure; minimal deps; resilient|principle
W32|Application Logic|code serving end-users; assumes env works; exits on failure|term
W33|One-Way-To-Do-It|prod env has single canonical method per task category|principle
W34|Distributed System|work spread across many nodes vs single instance|term
W35|DOS|Distributed Operating System; whole prod env as one logical machine|principle
W36|Idempotency|f(f(x))=f(x); same result regardless of starting state|rule
W37|Modeling|creating maps of systems for understanding or control|tool
W38|Model for Understanding|disposable+ephemeral+good-enough|term
W39|Model for Control|must be accurate+synced for resource lifetime|principle
W40|Source of Truth|authoritative data location for given domain|term
W41|Knowing the Present|gathering current-state data; never truly "now"; always aged|principle
W42|Black-Boxing|wrapping unknown internals in IOSE interface|tool
W43|Pragmatism|evaluate by effects only|principle
W44|Wisdom|breadth/depth of insight from experience; judgment of outcomes|term
W45|Intelligence (Cipolla)|action yielding benefit for all parties|term
W46|Win-Win-Win|self+org+external all benefit|principle
W47|Personal Experience|highest-trust info source; you saw it yourself|principle
W48|Hearsay|info reported by others without your verification; lower trust|term
W49|Local Reality|the actual context you operate in vs abstract general info|principle
W50|Land Mines in Your Yard|knowingly burying future problems via short-term fixes|anti-pattern
W51|Technical Debt|tradeoff: speed-now for cost-later; sometimes correct|term
W52|Throwing Hardware At It|scaling by adding machines to broken design|anti-pattern
W53|Logic In Data Store|stored procs/triggers; pollutes knowable space with unknowable|anti-pattern
W54|Magical Thinking|"X just happened out of nowhere"; signals broken mental model|anti-pattern
W55|AAA|Authenticate / Authorize / Account|rule
W56|Halting Problem|cannot determine if arbitrary program terminates|term
W57|Force Multiplier (auto)|automation cuts problems efficiently AND cuts you efficiently|principle

# worldview_axes(id|low_pole|high_pole|applies_to)
WA1|Unknowable|Knowable|info+real+virtual+logic
WA2|Real|Virtual|all-things
WA3|No Control|Total Control|environments
WA4|Application Logic|Operational Logic|code
WA5|Decentralized|Centralized|systems
WA6|Slow|Fast|performance
WA7|Not Available|Completely Available|services
WA8|Dangerous|Safe|changes
WA9|Difficult|Easy|operations
WA10|Opaque|Clear|visibility
WA11|Cant Scale|Can Scale|architecture
WA12|Aggregated|Comprehensive|systems

# worldview_distinctions(id|side_a|side_b|key_asymmetry)
WD1|Real|Virtual|Real never fully knowable; Virtual data fully knowable
WD2|Data|Logic|Data knowable+durable+portable; Logic unknowable+env-bound+goal-bound
WD3|Comprehensive|Aggregated|Comp owns whole space subdivides; Agg only covers built parts
WD4|Operational Logic|Application Logic|OpsLogic assumes failure resilient; AppLogic assumes env works exits clean
WD5|Best|Better|Best=1 thing absolute hidden tradeoffs; Better=2 things explicit tradeoffs
WD6|Push|Pull|Push centralized initiator; Pull decentralized targets fetch
WD7|Sequential|Parallel|Seq simple no-coordination; Par fast needs coordination
WD8|Knowable Virtual|Unknowable Virtual|some virtuals fully inspectable some inherently not
WD9|Understanding Model|Control Model|Und=disposable approximate; Ctl=lifetime-accurate-synced
WD10|Personal Experience|Hearsay|PE=verified-by-self; HS=trust-chain-with-failure-modes
WD11|Insider|Outsider|first-tier security boundary

# worldview_rules(id|name|statement|skip_when)
WR1|90-9-0.9%|each priority tier 10x more important than next|trivial choices
WR2|0-1-Infinity|no 2; only 0 or 1 or N instances|never
WR3|Idempotency|operations converge to desired state regardless of start|cant skip;always desirable
WR4|IOSE/Universal Machine|model anything as Inputs+Outputs+SideEffects|never
WR5|Slicing the Pie|subdivide preserving whole no info loss|aggregating-known-acceptable
WR6|AAA|Authenticate Authorize Account|never
WR7|Win-Win-Win|engineer for self+org+external benefit|never
WR8|Data Primacy|treat data as truth logic as replaceable shell|never
WR9|One-Way-To-Do-It|single canonical method per task category in prod|dev/experiment
WR10|Local Caching for OpsLogic|cache deps locally so partition doesnt break ops|never
WR11|Min Dependencies for OpsLogic|fewer libs/services/frameworks=fewer failure modes|app-logic-may-differ
WR12|Verify Personally|prefer self-verified info over hearsay|when-already-verified
WR13|Explicit Priority Reorder|state when changing default priorities|solo-quick-decisions
WR14|No Logic in Data Store|keep stored procs/triggers minimal-or-zero|portability-not-needed
WR15|Constraints On|use FK/check constraints unless perf forces off|measured-perf-block
WR16|Population Stats Only|stats valid for groups not individuals|individual-prediction-impossible

# axes(id|axis|role|count)
A1|mechanisms|building blocks performing work|62 in 13 families
A2|properties|contracts claimed about mechanisms|21 in 4 bands
A3|principles|rules governing assembly|22 in 6 groups

# vocab_principles(id|principle|rationale)
VP1|Three-axis structure|mechanism+property+principle distinct kinds; same word names all three; conflation prevents precise comparison
VP2|Mechanism is unit of work-doing|takes inputs+produces outputs+performs side effects; identified by interface not implementation
VP3|Property is contract|claim that holds over operations performed by mechanisms; multiple mechanisms can provide same property
VP4|Principle is rule|governs choice and assembly; does not perform work or claim guarantees; constrains mechanism+config+combination
VP5|Always qualify ambiguous words|"durability mechanism" vs "durability property" vs "durability-related principle"
VP6|Wrap/unwrap is general operation|encoding/decoding is one case; covers TLS+VPN+JSON+protobuf+tar
VP7|Mechanisms provide properties; properties require mechanisms; principles select among and constrain configs|the cross-axis triangle
VP8|Some mechanisms span families|same algorithmic shape serving multiple purposes
VP9|Some words name both mechanism and property|durability+ordering+consistency; resolved by qualification
VP10|Bucketing and layering are meta-patterns|recur across families; how mechanisms deployed not what they are
VP11|Taxonomy descriptive not prescriptive|names parts; does not prescribe construction or evaluate systems

# mechanism_families(id|family|role)
F1|Information movement|cause bytes/messages to travel
F2|Selection|choose among candidates
F3|Representation|determine how things expressed
F4|Storage|hold data over time
F5|Versioning|preserve and manage state lineage
F6|Lifecycle|bound a thing's extent in time
F7|Sensing|produce data about state
F8|Control loop|observe and act
F9|Gating|decide what is permitted
F10|Allocation|decide how much of what
F11|Coordination|synchronize multiple parties
F12|Transformation|produce new data from input data
F13|Resilience|handle failure

# mechanisms(id|name|family|def|sub_types)
M01|Channel|F1|path along which bytes travel between two endpoints|persistence(long-lived/ephemeral)|reliability(lossless/best-effort)|ordering|direction|framing
M02|Fanout|F1|one source emits to many destinations|broadcast|multicast|anycast|selective
M03|Funnel|F1|many sources emit to one collector|mixing|buffering|deduplication
M04|Replicator|F1+F4|copies state from one holder to another continuously or on demand|direction(pull/push/peer)|timing(sync/async/periodic)|scope(full/incremental)|fidelity
M05|Relay|F1|receives on one channel emits on another with possible transformation|proxy|tunnel|gateway|bridge
M06|Index|F2|data structure mapping key to location accelerating lookup|equality(hash)|range(B-tree)|prefix(trie)|set(bloom)|geometric|full-text|probabilistic
M07|Selector|F2|given population returns subset matching predicate|label-match|expression|set-membership|compound
M08|Comparator|F2|given two things decides equal/ordered/different|equality|ordering|structural|fuzzy|versioned
M09|Hasher|F2|deterministic function from input to bounded output|cryptographic|non-cryptographic|consistent|locality-sensitive|content-addressed
M10|Ranker|F2|given candidates orders them by score|single-criterion|multi-criterion|lexicographic|learned
M11|Router|F2|given input picks an output path|table-driven|hash-based|load-aware|policy-based|content-based
M12|Wrap/unwrap|F3|encapsulates payload in layer adding context+structure+framing+encryption+signing+routing metadata|representational|secure|routing|archival|framing|compressing
M13|Schema|F3|description of permissible structure constraining wrapped values|strict|permissive|versioned|structural|semantic
M14|Namespace|F3|scope within which names are unique and resolvable|flat|hierarchical|federated|table|function|distributed
M15|Naming convention|F3|function constructing identifiers from component data deterministically|positional|tagged|hierarchical|encoded
M16|Buffer|F4|in-memory holder of bounded size|FIFO-queue|LIFO-stack|ring-buffer|priority-queue
M17|Cache|F4|fast capacity-bounded copy of data whose source of truth is elsewhere|placement|admission|eviction|invalidation|consistency
M18|Store|F4|durable holder source of truth|structure(KV/relational/document/columnar/graph/blob)|durability|access
M19|Journal|F4|append-only sequential record of events/changes suitable for replay|operation-log|state-delta|redo|undo|mixed
M20|Log|F4|append-only record of events without replay-for-recovery as purpose|structured|unstructured|audit|access|diagnostic
M21|Snapshot|F4|point-in-time copy of state|full|incremental|logical|physical|consistent|fuzzy
M22|Tombstone|F4|marker that something was deleted distinct from absence|scope|lifetime
M23|Version stamp|F5|monotonic identifier attached to a state|scalar(LSN)|logical-clock|vector-clock|wall-clock|content-hash|opaque|hybrid
M24|History|F5|ordered sequence of versions with relationships preserved|linear|branching|DAG|forgetful|complete
M25|Merge algorithm|F5|given two divergent histories from common ancestor produces unified history|LWW|three-way|CRDT|operational-transformation|manual
M26|Diff|F5|structural description of change between two versions|textual|structural|operation-based|semantic
M27|Reference|F5|named pointer to a version|named|symbolic|anchored|mutable|immutable
M28|TTL|F6|time after which a thing is considered expired|absolute|relative|idle|conditional
M29|Lease|F6|time-bounded grant of authority over a resource|renewable|exclusive|shared|revocable
M30|Reaper|F6|process that removes expired or abandoned things|lazy|active|event-driven|batch
M31|Drainer|F6|gracefully removes things from active service before destroying|connection-level|request-level|timeout-bounded|state-aware
M32|Probe|F7|synthetic test of liveness/health/correctness|liveness|readiness|startup|deep|dependency
M33|Counter|F7|monotonic numeric tally of events|simple|labeled|resettable|non-resettable
M34|Gauge|F7|current numeric value of a quantity|instantaneous|windowed|bounded|derived
M35|Histogram|F7|bucketed distribution of values over time|bucket|decay|percentile
M36|Watch|F7|subscription to changes push-stream of events|edge-triggered|level-triggered|filtered|resumable
M37|Heartbeat|F7|periodic still-alive emission distinct from Probe|direction|payload|detection
M38|Reconciler|F8|observes desired vs actual takes action to close gap level-triggered repeats forever retries|trigger|scope|action
M39|Reactor|F8|receives events runs handlers edge-triggered fires once per event|delivery|handler
M40|Scheduler-control|F8+F10|assigns work to time slots or resources by policy|cron-like|rate-based|priority-queue|deadline-driven
M41|Workqueue|F8|buffered deduplicated retry-aware task list feeding worker pool|deduplication|retry|ordering|persistence
M42|Authenticator|F9|verifies identity claim against credentials|factor|mechanism|scope
M43|Authorizer|F9|checks permission for (subject+action+object)|RBAC|ABAC|policy-based|capability-based|mandatory|discretionary
M44|Validator|F9|checks request meets schema or policy rules before acceptance|schema|semantic|policy|invariant
M45|Mutator|F9|modifies request in flight before acceptance|defaulting|injection|rewriting|enrichment
M46|Filter|F9|accepts/drops/modifies based on rules|layer|state|rule|action
M47|Limiter|F9+F10|bounds rate or concurrency|algorithm|scope|action
M48|Pool|F10|collection of equivalent resources for checkout/return|fixed|elastic|per-tenant|shared|prioritized
M49|Quota|F10|maximum amount of resource a party may consume|hard|soft|burstable|fair-share
M50|Scheduler-allocation|F10|assigns work to resources by placement policy|selection|constraints|preemption
M51|Sharder|F10|partitions workload across resources|hash|range|directory|consistent-hash
M52|Lock|F11|exclusive access primitive|scope|fairness|mode|reentrancy
M53|Election|F11|protocol that selects one among many|Raft|Paxos|ZAB|highest-ID|lease
M54|Barrier|F11|synchronization point where participants wait until all arrived|count-based|named|phased
M55|Quorum|F11|rule requiring N-of-M parties to agree|majority|plurality|weighted|read-vs-write
M56|Sequencer|F11|assigns monotonic positions or timestamps|single-source|distributed|logical|vector|hybrid
M57|Renderer|F12|produces output by combining template with data|template-language|scope|chaining
M58|Transformer|F12|pure function from input to output|map|filter|reduce|fold|flat-map|codec
M59|Compactor|F12|merges multiple inputs into smaller equivalent output|log-compaction|SSTable|defragmentation
M60|Retrier|F13|re-runs failed operation possibly with backoff and jitter|immediate|exponential|jittered|bounded|idempotency-aware
M61|Circuit-breaker|F13|opens to stop calling failing dependency half-opens to test recovery|detection|recovery-probe|scope
M62|Bulkhead|F13|isolates failure domains so one failing component cannot drag others down|thread-pool|process|machine|cell
M63|Hedger|F13|issues redundant requests to reduce tail latency|immediate|delayed|bounded|canceling
M64|Failover|F13|switches from primary to standby on failure detection|active-passive|active-active|automatic|manual

# spanning_mechanisms(mechanism|families|rationale)
SP1|M40 Scheduler|F8+F10|F8 decides when; F10 decides where; same algorithmic shape (filter+score+choose)
SP2|M47 Limiter|F9+F10|F9 decides whether request may proceed; F10 decides how much capacity each consumer gets
SP3|M04 Replicator|F1+F4|moves data; consequence is data exists in multiple locations

# property_bands(id|band|role)
B1|Data integrity|claims about correctness+survival+protection of data
B2|Behavioral|claims about how operations behave
B3|Distribution|claims that arise specifically from multi-party systems
B4|Operational|claims about visibility+reconstruction

# properties(id|name|band|claim|conditions|partial_provision|does_not_claim)
P01|Idempotency|B1|applying same op with same inputs more than once yields same end state as applying once|same op+inputs+no concurrent state changes|on success not failure|no side effects only that repeated application converges
P02|Atomicity|B1|defined unit of work either fully completes or has no externally visible effect|unit specified|atomic locally not across replicas|other parties blocked (that is Isolation)
P03|Durability|B1|data acknowledged committed survives failure modes specified|specify which failures|durable to disk not replicated|that data is correct only that it survives
P04|Consistency-data|B1|declared constraints and invariants among data items hold at boundaries specified|constraints declared+boundaries specified|FKs enforced not app invariants|anything about replica freshness or ordering
P05|Integrity|B1|data has not been altered without detection between defined points|requires checksums+signatures|in transit not at rest|confidentiality or authenticity
P06|Authenticity|B1|source of data or request is verifiable|requires trust root and signing|immediate sender not original author|that authenticated source acts honestly
P07|Confidentiality|B1|data is unreadable to unauthorized parties|specify parties+threat model|in transit not at rest|integrity or authenticity
P08|Determinism|B2|same inputs produce same outputs and same side effects|specify what counts as input|in pure logic not I/O ordering|correctness only repeatability
P09|Convergence|B2|repeated application drives state toward fixed point|specify fixed point and conditions|in steady state not while inputs change|time bound on convergence
P10|Liveness|B2|system continues to make progress under specified conditions|specify progress and conditions|reads not writes|latency bounds on individual operations
P11|Availability|B2|system responds within specified timeframe under specified conditions|response timeframe+percentage+conditions|reads not writes|that responses are correct only that responses come
P12|Boundedness|B2|resource consumption stays within specified limit|resource named+limit specified|in steady state not failures|that limit is sufficient for any workload
P13|Isolation|B2|concurrent operations do not visibly interfere|specify level|within transaction not across|ordering only non-interference
P14|Reversibility|B2|completed operation can be undone fully or partially|time window+side effects|in database not side effects|byte-identical state only that visible effect undone
P15|Consistency-replica|B3|read after write returns written value or value satisfying specified relationship|specify level|linearizable in DC eventual across|data integrity (that is consistency-data)
P16|Ordering|B3|operations apply or appear in specified order|specify order|total within partition not across|any specific operation completes by any specific time
P17|Locality|B3|related data sits close together in storage or compute terms|closeness+relatedness defined|in primary storage not cache|that locality survives all operational events
P18|Stability under change|B3|adding/removing nodes/keys/clients does not cause disproportionate disruption|disproportionate defined|stable to additions not removals|that change is free only that cost is bounded
P19|Failure transparency|B3|failures of specified components are hidden from clients up to specified bounds|components+failures+bounds specified|to single-node not multi-node|that failures are prevented only that not exposed up to bound
P20|Observability|B4|relevant state is queryable or subscribable through specified interfaces|state+interfaces+latency+cost|real-time not historical|that observed state is fresh only that it is reachable
P21|Auditability|B4|past operations are reconstructible from preserved records|ops recorded+retention+integrity|for changes not reads|that audit log itself tamper-proof unless integrity separately claimed

# orthogonality(id|distinction|content)
OR1|Durability vs Persistence vs Availability|durability=survives failures; persistence=exists across restarts; availability=can be read now; durable-but-unavailable possible; available-but-not-durable possible
OR2|Consistency-data vs Consistency-replica|consistency-data=constraints hold; consistency-replica=replicas agree on value; system can have full data integrity per replica while replicas disagree
OR3|Ordering vs Isolation|ordering=sequence; isolation=interference; can be ordered without isolated; can be isolated without ordered
OR4|Idempotency vs Determinism|idempotent op can be nondeterministic (random ID first time); deterministic op can be non-idempotent (increment)

# double_citizens(word|mechanism_form|property_form)
DC1|Durability|M19 Journal|M18 Store with sync commit|M04 Replicator|the contract that committed data survives
DC2|Ordering|M56 Sequencer|the guarantee that operations apply in sequence
DC3|Consistency|M04+M44+M55 (mechanisms)|claim about constraints holding (data) OR replica agreement (replica)

# principle_groups(id|group|role)
G1|Data and logic|govern data vs code placement
G2|Scale and cardinality|govern cardinality choices
G3|Failure and resilience|govern failure handling
G4|Dependency and structure|govern coupling and layering
G5|Distribution|govern distributed system patterns
G6|Operator relationship|govern operator-system relationship

# principles(id|name|group|rule|reasoning|counter)
R01|Data primacy|G1|data outlives logic; make data SoT; logic as transformation; config in data not code paths|data fully knowable+stable; logic unknowable; data survives platform changes+decade time spans|none direct; does not forbid logic
R02|Single source of truth|G1|every fact has exactly one authoritative location; all others derived caches|multiple authoritative locations create divergence; reconciliation between authorities harder than between authority and cache|peer-to-peer where no single source desired
R03|Convention over lookup|G1|when function over data can produce answer prefer to registry that must be queried|functions deterministic+no coordination; registries require maintenance+can drift+add network call|when function would be too complex
R04|0/1/∞|G2|three real cardinalities; design for whichever is correct never design for two|any cardinality > 1 tends toward many under org pressure; building for two creates breakage at next growth step|cost may force small fixed N with explicit acknowledgment design will require change
R05|Comprehensive over aggregate|G2|slice the whole; do not accrete from parts; model exists in totality before implementation fills it|aggregate systems grow component-by-component with no plan for whole; become internally inconsistent|MVP often starts aggregate; conversion expensive but path most systems must take
R06|One way to do each thing|G2|within environment converge on one method per task; many almost-identical implementations are the enemy|every variant must be maintained+monitored+understood; produces 2x operational load|deliberate redundancy for failure independence acceptable when cost justified
R07|Idempotent retry|G3|every op crossing failure boundary should be safely retryable|failures inevitable; retries standard recovery; non-idempotent forces choice between data loss and duplication|counter-style ops and side-effect external calls cant always be made idempotent without uniqueness keys
R08|Level-triggered over edge-triggered|G3|react to current state not events; missed events inevitable missed state is not|edge-triggered loses work when events missed; level-triggered compares desired-vs-actual every iteration|pure event reaction required when state unbounded or expensive to compare
R09|Fail closed|G3|when uncertain deny rather than allow|in security+integrity contexts cost of false acceptance is breach/corruption|R10 in availability-critical
R10|Fail open|G3|when uncertain continue degraded rather than halt|in availability-critical contexts cost of false rejection (outage) exceeds cost of allowing unknown|R09 in security/integrity
R11|Bound everything|G3|every queue max depth+every cache max size+every connection timeout+every retry budget|unbounded resources fail unboundedly|none direct; bounds may be very large but must exist
R12|Reversible changes|G3|prefer mechanisms allowing rollback|changes have unintended consequences; reversal is fastest recovery|some changes irreversible by nature
R13|Minimize dependencies|G4|each new dependency multiplies failure modes and migration costs|every dependency is thing that can break; ops logic especially cannot depend on what it controls|principle is minimize not eliminate
R14|Separate planes|G4|data-plane+control-plane+management-plane have different SLAs+blast radii+failure modes|different functions need different reliability+timing properties|small systems may not need full plane separation
R15|Layer for separation of concerns|G4|each layer does one job with clean interface to next|easier to reason about+modify+replace|too many layers create overhead; principle is appropriate not maximum
R16|Bucket for locality and accounting|G4|group data by access pattern+tenant+lifecycle+failure domain; buckets are unit of operation|enables locality+accounting+isolation|over-bucketing fragments resources; principle is appropriate
R17|Local cache + global truth|G5|keep updatable local copy of what is needed; fall through to global when local stale or missing|local fast and survives partitions; global authoritative; combining gets both|when local divergence cannot be tolerated strong consistency must be paid for
R18|Centralize policy decentralize enforcement|G5|one place defines rules; many places enforce locally|central policy avoids drift; local enforcement avoids SPOF and round-trips|when policy must be re-evaluated per op enforcement may need centralization
R19|Push the decision down|G5|make decisions at lowest layer that has enough information|decisions made high require round-trips; decisions made low have more local information|decisions requiring global knowledge cannot be pushed down
R20|Push the work down or out|G5|edge cache absorbs origin; CDN absorbs edge; each layer reduces what next must handle|work close to source faster and avoids loading deeper layers|state-changing ops cannot be pushed out indefinitely
R21|Make state observable|G6|if you cannot see it you cannot operate it|every operational decision requires evidence; mechanisms whose state is hidden cannot be diagnosed|confidentiality may limit what can be exposed
R22|Removing classes of work|G6|goal of automation is not doing work faster — it is making work no longer need to be done|automation that only speeds manual work still requires manual work be done at scale|knowledge work creating automation cannot be removed only improved

# principle_conflicts(id|pair|resolution)
PC1|R09 Fail-closed vs R10 Fail-open|per-domain choice; security/integrity vs availability-critical
PC2|Centralize vs Decentralize|R18 is the resolution: different aspects have different centralization needs
PC3|R05 Comprehensive vs aggregate reality|principle prefers comprehensive but acknowledges aggregate as MVP reality

# triangle(id|aspect|content)
TR1|mechanisms→properties|mechanisms provide properties; native (M19→P21+partial P03) or configurable (M04 provides P15 at several levels) or compositional (sync M04 provides linearizable P15 at cost of P11 under partition)
TR2|properties→mechanisms|properties require mechanisms; some many (P01 via M08 OR M56 OR M18); some require composition (P03 via M19+M18+M04); some require specific (P06 requires M42+trust root+M12)
TR3|principles→mechanisms|principles select among when multiple provide property; R13 favors fewer external requirements; R11 favors explicit bounds; R19 favors less coordination
TR4|principles→properties|principles constrain how properties realized: R11 requires P12 claimed for every long-running mechanism
TR5|the triangle|mechanism provides properties; principles govern mechanism choice; principles constrain property realization

# family_property_coverage(family|primary_addresses)
F1|P17+P19+P16
F2|none directly; supports realization in others
F3|P05+P06+P07+P20
F4|P03+P04+P17
F5|P14+P21+P16+P18
F6|P12+P10
F7|P20
F8|P09+P10+P19
F9|P05+P07+P06+P12
F10|P12+P18+P17
F11|P02+P13+P16+P15
F12|none directly; supports realization
F13|P11+P10+P19+P09

# impossibility_triplets(triplet|observation)
IT1|P15+P11+Partition (CAP)|pick two; under partition CP rejects writes AP accepts and reconciles later
IT2|P15+P11+Latency (PACELC)|at higher consistency levels latency increases
IT3|P03+Latency+Throughput|sync durability bounds throughput; async risks loss
IT4|P01+P02+P16 across distributed parties|requires consensus; no shortcuts
IT5|P07+P20+P21|encrypted-at-rest harder to audit; audit data itself sensitive
IT6|P17+P18+P11|rebalancing for locality after change reduces availability briefly
IT7|P14+P02 of side effects+Latency|reversible distributed ops require sagas or 2PC both slow
IT8|P08+P10+real-time clocks|deterministic system using real time cannot be both reproducible and responsive
IT9|P19+P12+P10|hiding failures requires retries which can violate bounds and stall liveness

# gap_analysis(property|claim|delivered|gap_reason)
GAP01|P03|"Your data is safe"|survives single-machine crash; loses last 1-10s on async replication|sync replication too slow for default
GAP02|P11|"99.99% uptime"|read availability of cached responses; write availability lower|reads easy to scale writes serialize through primary
GAP03|P15|"Consistent"|eventual with 50ms-60s lag; "strong" only on primary|true linearizability requires expensive coordination
GAP04|P02|"Transactional"|per-row in NoSQL; per-transaction in RDBMS; rarely cross-system|distributed transactions avoided due to cost
GAP05|P01|"Safe to retry"|safe for GET/PUT/DELETE; not for POST without uniqueness keys|HTTP semantics widely misimplemented
GAP06|P16|"FIFO"|per-partition only; no global order|global order requires global serialization
GAP07|P08|"Reproducible"|reproducible given identical inputs; rarely hit in practice|time+randomness+concurrency+external state
GAP08|P13|"Serializable"|Read Committed by default; serializable rare|performance cost of true serializable
GAP09|P19|"Self-healing"|transparent for replica loss; opaque for primary loss|primary failover often requires manual or complex automation
GAP10|P20|"Fully observable"|real-time per-component; hard to correlate cross-component|no global causality; logs/metrics/traces siloed
GAP11|P21|"Audited"|audit log exists; tamper-evident only with separate effort|audit log itself rarely has integrity protection
GAP12|P14|"Rollback supported"|rollback for database; not for downstream side effects|API calls+emails+payments cannot be unsent
GAP13|P12|"Capped at N"|capped under normal load; unbounded during failures or queue buildup|bounds rarely enforced under stress
GAP14|P07|"Encrypted"|encrypted in transit; sometimes at rest; rarely against operator|operator-level confidentiality requires confidential computing
GAP15|P06|"Authenticated"|identity of immediate sender (TLS); rarely end-to-end author identity|sender ≠ author in most architectures

# meta_patterns(pattern|applies_across)
MP1|Bucketing|F4(cache lines+partitions)+F2(hash buckets)+F10(resource pools)+F7(histograms)+F6(TTL cohorts)
MP2|Layering|F1(network)+F3(wrap-unwrap stacking)+F4(cache hierarchies)+F9(defense in depth)

# === ARCHITECTURE: OpsDB ===

# arch_definition(aspect|content)
AD1|what|centralized data substrate holding full operational reality of organization
AD2|access|single API gate enforcing authentication+authorization+validation+change-management+versioning+audit uniformly
AD3|consumed by|three populations: humans+automation runners+auditors via scoped permissions
AD4|active layer|small fleet of decentralized runners reads from OpsDB+acts in world via shared libraries+writes results back
AD5|substrate posture|passive; never invokes work; answers queries+accepts writes
AD6|schema is data|declared in YAML files in git repo+evolved through same change-mgmt discipline as any operational change
AD7|core principle|data is king logic is shell at every layer

# arch_commitments(id|commitment|content|failure_if_violated)
AC1|Passive Substrate|OpsDB answers queries+accepts writes; never invokes work|becomes orchestrator; stateful complex fragile
AC2|API as Only Path|no SSH/out-of-band/shadow paths; substrate ops exception under SoD|governance becomes advisory; OpsDB claims unreliable
AC3|Storage Engine Independence|schema is design; engine is implementation choice|locked into vendor; migration impossible
AC4|API Holds All Governance|auth/authz/validation/change-mgmt/versioning/audit at gate uniformly|policy fragments; substrate contaminated
AC5|Decentralized Work Shared Substrate|many runners many substrates; OpsDB rendezvous not orchestrator|runners couple to each other; orchestrator drift
AC6|Configuration as Data|schedules/policies/runner-enum/rules/retention/escalation are data|logic embedded in code; data outlives logic violated
AC7|Service Pointers First-Class|directory of where every fact lives is structured content|fragmentation returns; ad-hoc lookup
AC8|Local Replicas Valid|any host can hold dumped slice for partition tolerance|partition fails ops; bootstrap impossible
AC9|Schema Evolution Governed|schema changes go through change-mgmt with stricter rules|schema drifts; long-lived artifact lost
AC10|No 2|cardinality 1 or N; never 2|split-brain; drifting schemas; uncoordinated governance

# cardinality(id|state|justification|valid)
CR1|0|absence of coordination substrate; ad-hoc human-driven ops|valid-but-immature
CR2|1|single security umbrella; one trusted population; one IdP; one compliance scope|valid-target
CR3|N security perimeter|breach of one substrate must not expose another; API-layer authz insufficient|valid
CR4|N legal/regulatory|GDPR+sectoral+sovereignty require physical residency|valid
CR5|N org boundaries|business units operating as separate companies; recent acquisitions|valid
CR6|N human comm boundaries|teams not sharing processes/conventions; coordination cost exceeds benefit|valid
CR7|N air-gap|classified+industrial-control require physical isolation|valid
CR8|2|split-brain; drifting schemas; two governance models; two audit trails|invalid-failure-state
CR9|N technical fragility|"protect prod from corp tooling experiments"|invalid; signs of bad ops not structural
CR10|N convenience|"two would be easier"|invalid; convenience not structural
CR11|N premature|"we might need to split eventually"|invalid; stay-1 until structure forces N
CR12|N performance|"one cant serve our query load"|invalid; scale within single OpsDB

# n_pipeline(rule|content)
N1|each-OpsDB-has-identity|named addressable distinguishable; cross-refs include substrate id
N2|cross-refs-first-class|typed pointer: substrate-id + entity-locator + policy-hints
N3|federated-reads-with-policy|each API enforces what's resolvable from calling context
N4|cross-writes-typically-not-supported|each substrate own write authority
N5|same-code-same-schema-separate-substrates|N instances of same design not N products
N6|operators-may-differ|gov-zone vs commercial-zone may not share personnel when threat model demands

# n_pipeline_components(component|shared_or_diverged)
NP1|schema repo|shared (one repo deployed to N OpsDBs)
NP2|library suite contracts and impls|shared (one set consumed by N runner populations)
NP3|API code|shared (one codebase deployed N times)
NP4|change-mgmt discipline|shared (same rules at each substrate)
NP5|data each substrate holds|diverged (each substrate own write authority)
NP6|users authorized|diverged (per substrate)
NP7|audit log|diverged (per substrate independent)
NP8|runners deployed|diverged (per substrate)
NP9|cross-OpsDB writes|not supported (coordination via external means)

# populations(id|population|access_pattern|use_modes)
Pop1|Humans|exploratory navigation; UI on top of API; submit change sets|investigate-incidents|plan-changes|query-state|build-dashboards|review-approvals
Pop2|Automation|structured narrow; per-runner credentials; minimum-necessary access|read-config|write-cache|write-results|propose-changes
Pop3|Auditors|read-only broad; verification-oriented; findings produce change sets|verify-controls|read-history|read-evidence|read-policies

# content_held(id|category|examples|sot|versioned)
CT1|Centrally-Managed Config|service definitions+deployment specs+on-call+escalation+retention+alert thresholds+security policies|opsdb|yes
CT2|Cached Observed State|K8s pod status+cloud resource state+metric summaries+IdP group membership|authority|no
CT3|Authority Pointers|prom server+metric+vault path+wiki url+verified-ts|opsdb|yes
CT4|Service Directory|where-metric+where-log+where-runbook+who-on-call+which-cluster|opsdb|yes
CT5|Schedules|when runners run+backups+expirations+rotations+audits|opsdb|yes
CT6|Runner Enumeration|deployment metadata records; not source code|opsdb|yes
CT7|Documentation Metadata|owners+stakeholders+support+runbook links+last-reviewed|opsdb|yes
CT8|Policies|security zones+compliance+data classification+escalation+change-mgmt+retention|opsdb|yes
CT9|Version History|per-entity history of every change with attribution|opsdb|self
CT10|Audit Log|append-only every API action with identity+timestamp+action+target|opsdb|append-only
CT11|Change-Mgmt State|pending sets+approval status+records+rejected proposals|opsdb|yes
CT12|Cross-OpsDB References|in N pattern: typed pointers to entities in other substrates|opsdb|yes
# scope_note: full operational reality including tape-backups+password-rotations+cert-renewals+vendor-contracts+dns-expirations+compliance-calendars+keycard-deactivation+laptop-patch-status+vendor-account-creds

# content_not_held(id|not_held|held_in_instead)
NH1|long-form prose|wiki+notion+equivalent; OpsDB has structured pointers
NH2|time-series at full resolution|prometheus+datadog+cloudwatch; OpsDB holds cached subset+pointers
NH3|code (runner+package+container images)|repositories+container registries; OpsDB holds metadata+image refs
NH4|secrets values|vault+aws-sm+gcp-sm; OpsDB holds path+version pointers only
NH5|chat/discussion|slack+teams+irc; OpsDB has authority pointers to threads
NH6|tickets/incidents|jira+linear+servicenow; OpsDB references where appropriate
NH7|orchestration|runners run on own schedules; OpsDB consulted not directing
NH8|runtime dependency for live services|services keep running when OpsDB unreachable; OpsDB is coordination not data plane

# boundaries(id|not_a|why|belongs_in|paper)
BD1|Wiki|long-form prose not structured|wiki+notion; OpsDB holds pointers|OPSDB-2
BD2|Monitoring System|cant store full time-series; cant compete with prom/datadog primitives|prometheus+datadog; OpsDB holds cached subset|OPSDB-2
BD3|Code Repository|artifacts have own tooling|git+container-registries; OpsDB holds metadata|OPSDB-2
BD4|Binary Distribution|distribution has own systems|ci/cd+packaging; OpsDB knows runners deployed not how|OPSDB-2
BD5|Orchestrator|invoking runners violates passive commitment|runners' own scheduling; OpsDB consulted|OPSDB-2
BD6|Chat System|discussion+coordination not data|slack+teams; OpsDB holds pointers|OPSDB-2
BD7|Ticketing System|incidents+work-tracking have own systems|jira+linear; OpsDB references them|OPSDB-2
BD8|Secrets Manager|secrets need-to-know+audit-on-read+ephemeral; not OpsDB semantics|vault+equivalent; OpsDB holds path+version pointers|OPSDB-2
BD9|World SPOF|services fail if OpsDB runtime dependency; arch wrong if so|runners cache or templated; graceful degradation|OPSDB-2
BD10|API Orchestrator|API does not invoke runners; would compromise passive commitment|runners poll+react+coordinate through OpsDB rows|OPSDB-6
BD11|API Notification System|adding would couple to delivery infra evolving at different pace|notification runner reads state transitions+dispatches|OPSDB-6
BD12|API Change-Set Applier|adding would couple API to executor timing|change-set executor runner polls approved+applies via API write ops|OPSDB-6
BD13|API Workflow Engine|change_set lifecycle is the only workflow API enforces|other workflows coordinate through OpsDB rows|OPSDB-6
BD14|API Search Engine|structured filter+joins only; no full-text+semantic+vector|wiki+documentation systems with own query interfaces|OPSDB-6
BD15|API Dashboard System|serves reads dashboards consume; does not render UI|dashboard systems sit on top with own tooling|OPSDB-6
BD16|Library Runner Framework|library callable not controlling shell; framework owning runner main loop couples evolution|runner main loop+event dispatch+lifecycle stay runner's|OPSDB-8
BD17|Library Workflow Engine|library does not mediate runner-to-runner messaging; would be orchestrator|runners coordinate through OpsDB rows|OPSDB-8
BD18|Library Code Distribution|impls distributed via PyPI+container registries+language-native|standard package mechanisms|OPSDB-8
BD19|Library Secrets Store|secret library accesses backends; never persists values|secret backend is SoT|OPSDB-8
BD20|Library Service Mesh|library makes outbound calls; does not intercept other components' traffic|service-mesh products at network layer|OPSDB-8
BD21|Library UI|no UI in suite; runners observed via observation libs + dashboards|downstream concern consuming OpsDB|OPSDB-8
BD22|Library Database|OpsDB is the database; library state ephemeral or written to OpsDB|library uses OpsDB OR operates ephemerally|OPSDB-8

# flows(id|name|trigger|path|terminal)
OF1|Configuration|human/automation submits change set|API validates schema+policy → records pending → evaluates approval rules → notifies approvers → collects approvals → atomic commit when satisfied → runners read on next cycle|new config current; full trail queryable
OF2|Cached Observation|puller scheduled cycle|queries authority via shared lib → transforms to schema → writes via API with scoped creds → audit logged but not change-managed|cache updated with timestamp
OF3|Reconciliation|reconciler scheduled cycle|reads desired+observed → computes diff → for each: act-via-lib OR propose-change-set OR log-and-defer → writes results back|observed driven toward desired within authorization
OF4|Verification|verifier scheduled cycle matched to subject schedule|queries authority → compares to expected → writes structured evidence record via API|evidence queryable
OF5|Investigation|human starts from symptom|query entity → query version history → query cached observed → follow authority pointers → query on-call/ownership|picture assembled from structured queries
OF6|Audit|auditor read-only scoped role|query audit log+version history+change-mgmt records+evidence+policies|findings filed as audit data
OF7|Service Pointer Lookup|caller asks where-is-X|OpsDB returns authority coordinates → caller queries authority directly|one query to OpsDB plus one to authority
OF8|Local Replica|operator/runner needs partition tolerance|dump OpsDB slice with version stamp → host operates locally → on reconnect refresh+writeback|fast local during normal+disconnected
OF9|Cross-OpsDB|caller queries one; response includes ref to entity in another|first API decides whether to include ref → second API decides whether to answer|reads federate with policy
OF10|Schema Evolution|propose new entity-type/relationship/field|stricter approval rules → forward+backward compat validation → approve → schema updated|schema versioned and audited
OF11|Emergency Change|on-call detects production incident|change set with emergency=true → commits with reduced approvals → flagged in audit → post-incident review triggered|recorded as emergency; reviewed retroactively
OF12|Bulk Change|coordinated multi-entity operation|single change set with N changes → one approval cycle → atomic commit OR none|coordinated changes never partial-state

# === SCHEMA ===

# schema_conventions(id|rule|applies_to)
SC1|singular names|all-tables-and-fields
SC2|lower_case_with_underscores|all-names
SC3|hierarchical prefix specific-to-general|composite-names
SC4|FK named referenced_table_id|all-FKs
SC5|role prefix when multiple FKs to same target|vendor_company_id|service_company_id
SC6|_time suffix for DATETIME|all-time-fields
SC7|_date suffix for DATE|all-date-fields
SC8|is_X tense prefix for present-state booleans|booleans
SC9|was_X tense prefix for past-event booleans|booleans
SC10|underscore prefix for governance/admin/schema metadata|governance-fields
SC11|FK polymorphic relationships use bridge tables not poly-FK|polymorphic-relationships
SC12|typed payloads use *_type discriminator + *_data_json|heterogeneous-data
SC13|API validates *_data_json against schema registered for *_type value|all-typed-payloads
SC14|soft delete via is_active=false; rows persist|deletion
SC15|change-managed entities have *_version sibling table|versioned-entities
SC16|versioning is per-field within change set|versioned-entities

# schema_patterns(id|name|shape|when_used)
SP_1|Universal Reserved Fields|id+created_time+updated_time on every table; parent_id when self-hierarchical; is_active when soft-deletable|all-tables
SP_2|Versioning Sibling|*_version table with version_serial+parent_*_version_id+change_set_id+is_active_version|change-managed entities
SP_3|Typed Payload|*_type discriminator + *_data_json validated against registered schema|heterogeneous data
SP_4|Bridge Table per Target Type|one bridge table per source-target pair; clean FK integrity|polymorphic relationships
SP_5|Underscore Governance Prefix|fields prefixed _ for security/audit/schema/observation metadata|tables needing extra-policy fields
SP_6|Hierarchical Self-FK|parent_id pointing to same table|location|hardware_component|megavisor_instance|service|policy|escalation_step
SP_7|Configuration Variables|one table holds typed key-value scoped via scope_type+scope_id|helm-values|configmap|service-params|runner-params
SP_8|Unified Substrate Hierarchy|megavisor_instance self-FK chain spans bare-metal+VM+container+pod+cloud|substrate-modeling
SP_9|Unified Cache Tables|three tables (metric|state|config) keyed by source+key|observation-caching
SP_10|Schema Self-Description|_schema_* tables register entities/fields/relationships; queryable like any table|schema-introspection

# reserved_fields(field|type|applies_when|purpose)
SR1|id|INT|all-tables|primary key auto-increment
SR2|created_time|DATETIME|all-tables|set on insert
SR3|updated_time|DATETIME|all-tables|set on insert+update
SR4|parent_id|FK-self|self-hierarchical-tables|hierarchy traversal
SR5|is_active|BOOL|soft-delete-tables|soft delete state
SR6|version_serial|INT|*_version siblings|monotonic per entity
SR7|parent_*_version_id|FK-self-version|*_version siblings|prior version chain
SR8|change_set_id|FK:change_set|*_version siblings|change set that produced version
SR9|is_active_version|BOOL|*_version siblings|true for current version
SR10|approved_for_production_time|DATETIME|*_version siblings|when version went live

# governance_fields(field|purpose|consulted_by)
SG1|_requires_group|group required for access beyond standard role|API on read/write
SG2|_access_classification|data sensitivity (public/internal/confidential/restricted/regulated)|API for access decisions+logging
SG3|_audit_chain_hash|cryptographic chain over prior entry|audit verification tooling
SG4|_retention_policy_id|FK:retention_policy override of default|reaper runners+query interfaces
SG5|_schema_version_introduced_id|when entity/field appeared|schema introspection
SG6|_schema_version_deprecated_id|when entity/field deprecated|schema introspection+runner compat
SG7|_observed_time|when observation sampled|cached observation queries
SG8|_authority_id|source authority of observation|cached observation queries
SG9|_puller_runner_job_id|runner job that wrote observation|audit+debugging

# top_level_categories(id|category|scope)
TC1|Site and Location|DOS scope+physical/logical locations
TC2|Identity|users+groups+roles
TC3|Substrate|hardware+megavisor+machines+cloud-resources+storage
TC4|Service Abstraction|services+packages+interfaces+connections+host-groups
TC5|Kubernetes|clusters+nodes+namespaces+workloads+pods+helm+configmaps+secret-refs
TC6|Cloud Resources|generic resource modeling with provider-specific payloads
TC7|Authority Directory|typed pointers to monitoring+logs+secrets+docs+identity+code-repos
TC8|Schedules|when things happen
TC9|Policy|security-zones+classifications+retention+approval+escalation
TC10|Documentation Metadata|ownership+runbooks+dashboards+last-reviewed
TC11|Runners|specs+capabilities+jobs+output+targets
TC12|Monitoring and Alerting|monitors+alerts+on-call+suppression
TC13|Cached Observation|pulled state from authorities
TC14|Configuration Variables|typed key-value across many domains
TC15|Change Management|change-sets+approvals+approval-rules
TC16|Audit and Evidence|audit-log+evidence+compliance-findings
TC17|Schema Metadata|OpsDB record of own schema

# entities(id|name|category|versioned|parent|description)
SE1|site|TC1|no|-|DOS scope within OpsDB
SE2|location|TC1|no|self|hierarchical (region/dc/cage/row/rack/cloud_region/cloud_zone/office/desk)
SE3|ops_user|TC2|no|-|operational identity within site
SE4|ops_group|TC2|no|-|access policy grouping
SE5|ops_group_member|TC2|no|-|bridge: group↔user
SE6|ops_user_role|TC2|no|-|operational position
SE7|ops_user_role_member|TC2|no|-|bridge: role↔user with rotation_order
SE8|hardware_component|TC3|no|self|physical hardware part
SE9|hardware_port|TC3|no|-|connection point on component
SE10|hardware_set|TC3|no|-|hardware specification
SE11|hardware_set_component|TC3|no|-|bridge: set↔component+position
SE12|hardware_set_instance|TC3|no|-|physical instance in location
SE13|hardware_set_instance_port_connection|TC3|no|-|cable/peering record
SE14|megavisor|TC3|no|-|abstraction over hosting (bare_metal/kvm/vmware/xen/hyperv/docker/containerd/kubelet/firecracker/ec2/gce/azure_vm/lambda/cloudrun/fargate)
SE15|megavisor_instance|TC3|no|self|unified substrate hierarchy node
SE16|cloud_provider|TC3|no|-|cloud vendor identity
SE17|cloud_account|TC3|no|-|cloud provider account
SE18|cloud_resource|TC3|yes|-|generic cloud resource with typed payload
SE19|storage_resource|TC3|no|-|storage abstraction over physical/cloud
SE20|platform|TC3|no|-|OS image build
SE21|machine|TC3|yes|-|configured host
SE22|package|TC4|yes|-|installable functionality
SE23|package_interface|TC4|no|-|exposed interface (per package_version)
SE24|package_connection|TC4|no|-|outbound interface dependency
SE25|service|TC4|yes|self|operational role
SE26|service_package|TC4|no|-|bridge: service↔package_version with install_order
SE27|service_interface_mount|TC4|no|-|exposed interface for service version
SE28|service_connection|TC4|no|-|service-to-service connection (drives config+firewall+suppression+capacity)
SE29|host_group|TC4|no|-|host role assignment
SE30|host_group_machine|TC4|no|-|bridge: group↔machine
SE31|host_group_package|TC4|no|-|bridge: group↔package_version with install_order
SE32|site_location|TC4|no|-|per-service location preference with precedence_order
SE33|service_level|TC4|no|-|scaling+capacity rule
SE34|service_level_metric|TC4|no|-|metric-driven scaling
SE35|k8s_cluster|TC5|yes|-|Kubernetes cluster (IS a service via service_id)
SE36|k8s_cluster_node|TC5|no|-|cluster node bridging to machine
SE37|k8s_namespace|TC5|no|-|cluster namespace
SE38|k8s_workload|TC5|yes|-|deployment/statefulset/daemonset/job/cronjob/replicaset
SE39|k8s_pod|TC5|no|-|pod with link to megavisor_instance
SE40|k8s_helm_release|TC5|yes|-|Helm release entity
SE41|k8s_config_map|TC5|yes|-|configmap entity (values in configuration_variable)
SE42|k8s_secret_reference|TC5|no|-|pointer to secret backend; never holds value
SE43|k8s_service|TC5|no|-|K8s service object; optional link to OpsDB service
SE44|authority|TC7|no|-|external system owning slice of operational reality
SE45|authority_pointer|TC7|no|-|typed reference to specific item within authority
SE46|service_authority_pointer|TC7|no|-|bridge:service↔authority_pointer
SE47|machine_authority_pointer|TC7|no|-|bridge:machine↔authority_pointer
SE48|k8s_cluster_authority_pointer|TC7|no|-|bridge:k8s_cluster↔authority_pointer
SE49|cloud_resource_authority_pointer|TC7|no|-|bridge:cloud_resource↔authority_pointer
SE50|schedule|TC8|yes|-|time-based or event-based trigger spec
SE51|runner_schedule|TC8|no|-|bridge:runner_spec↔schedule
SE52|credential_rotation_schedule|TC8|no|-|bridge:credential↔schedule
SE53|certificate_expiration_schedule|TC8|no|-|bridge:certificate↔schedule
SE54|compliance_audit_schedule|TC8|no|-|bridge:compliance_regime↔schedule
SE55|manual_operation_schedule|TC8|no|-|bridge:manual_operation↔schedule
SE56|manual_operation|TC8|no|-|operational task humans perform
SE57|policy|TC9|yes|-|organizational rule with typed payload
SE58|service_policy|TC9|no|-|bridge:service↔policy
SE59|machine_policy|TC9|no|-|bridge:machine↔policy
SE60|k8s_namespace_policy|TC9|no|-|bridge:k8s_namespace↔policy
SE61|cloud_account_policy|TC9|no|-|bridge:cloud_account↔policy
SE62|security_zone|TC9|no|-|operational security scope
SE63|security_zone_membership_service|TC9|no|-|bridge:zone↔service
SE64|security_zone_membership_machine|TC9|no|-|bridge:zone↔machine
SE65|security_zone_membership_k8s_namespace|TC9|no|-|bridge:zone↔namespace
SE66|data_classification|TC9|no|-|data sensitivity level
SE67|retention_policy|TC9|no|-|per-entity-type retention horizon
SE68|approval_rule|TC9|no|-|policy declaring approval requirements per change
SE69|escalation_path|TC9|no|-|named alert escalation policy
SE70|escalation_step|TC9|no|self|step within escalation_path with step_order
SE71|service_escalation_path|TC9|no|-|bridge:service↔escalation_path
SE72|change_management_rule|TC9|no|-|policy data governing change-mgmt behavior
SE73|compliance_regime|TC9|no|-|regulatory regime declaration
SE74|compliance_scope_service|TC9|no|-|bridge:regime↔service
SE75|compliance_scope_data_classification|TC9|no|-|bridge:regime↔data_classification
SE76|service_ownership|TC10|no|-|bridge:service↔ops_user_role with ownership_role
SE77|machine_ownership|TC10|no|-|bridge:machine↔ops_user_role
SE78|k8s_cluster_ownership|TC10|no|-|bridge:k8s_cluster↔ops_user_role
SE79|cloud_resource_ownership|TC10|no|-|bridge:cloud_resource↔ops_user_role
SE80|service_stakeholder|TC10|no|-|bridge:service↔ops_user_role with stakeholder_role
SE81|runbook_reference|TC10|no|-|structured runbook pointer with metadata
SE82|service_runbook_reference|TC10|no|-|bridge:service↔runbook with purpose
SE83|dashboard_reference|TC10|no|-|structured dashboard pointer with metadata
SE84|service_dashboard_reference|TC10|no|-|bridge:service↔dashboard with purpose
SE85|runner_spec|TC11|yes|-|runner kind specification
SE86|runner_capability|TC11|no|-|declared runner capability
SE87|runner_machine|TC11|no|-|bridge:machine↔runner_spec with capacity
SE88|runner_instance|TC11|no|-|live runner process
SE89|runner_service_target|TC11|no|-|bridge:runner_spec↔service
SE90|runner_host_group_target|TC11|no|-|bridge:runner_spec↔host_group
SE91|runner_k8s_namespace_target|TC11|no|-|bridge:runner_spec↔k8s_namespace
SE92|runner_cloud_account_target|TC11|no|-|bridge:runner_spec↔cloud_account
SE93|runner_job|TC11|no|-|runtime record of runner execution
SE94|runner_job_target_machine|TC11|no|-|bridge:job↔machine with per-target status
SE95|runner_job_target_service|TC11|no|-|bridge:job↔service
SE96|runner_job_target_k8s_workload|TC11|no|-|bridge:job↔k8s_workload
SE97|runner_job_target_cloud_resource|TC11|no|-|bridge:job↔cloud_resource
SE98|runner_job_output_var|TC11|no|-|discrete output variable from job
SE99|monitor|TC12|no|-|owned by package; defines a check
SE100|monitor_machine_target|TC12|no|-|bridge:monitor↔machine
SE101|monitor_service_target|TC12|no|-|bridge:monitor↔service
SE102|monitor_k8s_workload_target|TC12|no|-|bridge:monitor↔k8s_workload
SE103|monitor_cloud_resource_target|TC12|no|-|bridge:monitor↔cloud_resource
SE104|prometheus_config|TC12|no|-|prometheus configuration owned by authority
SE105|prometheus_scrape_target|TC12|no|-|scrape target within prometheus_config
SE106|monitor_level|TC12|no|-|condition-action grouping; ANDs by name
SE107|alert|TC12|no|-|named alert condition with severity scoped to service
SE108|alert_dependency|TC12|no|-|suppression relationship between alerts
SE109|alert_fire|TC12|no|-|specific firing instance of alert
SE110|on_call_schedule|TC12|no|-|schedule + role linkage
SE111|on_call_assignment|TC12|no|-|specific on-call assignment over window
SE112|observation_cache_metric|TC13|no|-|cached metric data keyed by authority+hostname+metric_key
SE113|observation_cache_state|TC13|no|-|cached state data keyed by entity_type+entity_id+state_key
SE114|observation_cache_config|TC13|no|-|cached config data keyed by authority+hostname+config_key
SE115|configuration_variable|TC14|yes|-|typed key-value scoped to entity via scope_type+scope_id
SE116|change_set|TC15|no|-|bundled proposed changes
SE117|change_set_field_change|TC15|no|-|per-field change record
SE118|change_set_approval_required|TC15|no|-|computed approval requirement
SE119|change_set_approval|TC15|no|-|recorded approval
SE120|change_set_rejection|TC15|no|-|rejection record
SE121|change_set_validation|TC15|no|-|validation outcome record
SE122|change_set_emergency_review|TC15|no|-|post-hoc review of emergency changes
SE123|change_set_bulk_membership|TC15|no|-|structure within bulk change sets
SE124|audit_log_entry|TC16|append-only|-|append-only API action record
SE125|evidence_record|TC16|no|-|verification outcome from runner or human
SE126|evidence_record_service_target|TC16|no|-|bridge:evidence↔service
SE127|evidence_record_machine_target|TC16|no|-|bridge:evidence↔machine
SE128|evidence_record_credential_target|TC16|no|-|bridge:evidence↔credential
SE129|evidence_record_certificate_target|TC16|no|-|bridge:evidence↔certificate
SE130|evidence_record_compliance_regime_target|TC16|no|-|bridge:evidence↔regime
SE131|evidence_record_manual_operation_target|TC16|no|-|bridge:evidence↔manual_operation
SE132|compliance_finding|TC16|no|-|filed compliance gap or observation
SE133|compliance_finding_target_service|TC16|no|-|bridge:finding↔service
SE134|_schema_version|TC17|no|self|canonical schema version
SE135|_schema_change_set|TC17|no|self|schema evolution change set
SE136|_schema_entity_type|TC17|no|-|registry of entity types
SE137|_schema_field|TC17|no|-|registry of fields
SE138|_schema_relationship|TC17|no|-|registry of relationships

# discriminators(id|entity|type_field|payload_field|values)
SD1|cloud_resource|cloud_resource_type|cloud_data_json|ec2_instance|gce_instance|azure_vm|s3_bucket|gcs_bucket|azure_blob_container|rds_database|cloud_sql_instance|azure_sql|lambda_function|cloud_run_service|azure_function|vpc|vnet|cloud_network|load_balancer|application_gateway|cloud_lb|cloudfront_distribution|cloud_cdn|azure_cdn|iam_role|service_account|azure_service_principal|route53_zone|cloud_dns_zone|azure_dns_zone|cloudwatch_log_group|cloud_logging_bucket|log_analytics_workspace
SD2|storage_resource|storage_resource_type|storage_data_json|ebs|s3|gcs|azure_blob|nfs_export|ceph_rbd|local_disk|iscsi
SD3|k8s_workload_version|workload_type (on parent)|workload_data_json|deployment|statefulset|daemonset|job|cronjob|replicaset
SD4|authority|authority_type|authority_data_json|prometheus_server|log_aggregator|secret_vault|wiki|dashboard_platform|code_repository|identity_provider|runbook_store|ticketing_system|chat_platform|status_page|artifact_registry|container_registry
SD5|authority_pointer|pointer_type|pointer_data_json|metric|log_query|secret|dashboard|runbook|wiki_page|ticket|code_path|chat_thread|artifact|container_image
SD6|schedule|schedule_type|schedule_data_json|cron_expression|rate_based|event_triggered|calendar_anchored|deadline_driven|manual
SD7|policy|policy_type|policy_data_json|security_zone|data_classification|retention|approval_rule|escalation|change_management|schedule_governance|access_control|compliance_scope
SD8|runner_spec_version|runner_spec_type (on parent)|runner_data_json|config_apply|template_generate|k8s_apply|cloud_provision|monitor_collect|alert_dispatch|drift_detect|verify_evidence|reconcile|scheduler_enforce|puller|compliance_scan|credential_rotator|certificate_renewer|manual_operation_tracker
SD9|monitor|monitor_type|monitor_data_json|script_local|script_remote|prometheus_query|http_probe|tcp_probe|cloud_metric|k8s_event_watch
SD10|evidence_record|evidence_record_type|evidence_record_data_json|backup_verification|certificate_validity|compliance_scan|credential_rotation_verification|access_review|physical_inspection|tape_rotation_completed|keycard_revocation_completed|license_renewal_completed|vendor_contract_review_completed
SD11|manual_operation|manual_operation_type|manual_operation_data_json|tape_rotation|vendor_review|keycard_audit|license_renewal|contract_renewal|evidence_collection|physical_inspection
SD12|configuration_variable|variable_type|variable_data_json|string|int|float|bool|json|secret_reference

# versioning_classification(classification|writer|gated)
VC1|change-managed|humans+runners via change_set|yes
VC2|observation-only|pullers/runners with scoped creds|no (audited)
VC3|append-only|API only; no UPDATE or DELETE|no
VC4|computed-by-tooling|API tooling on schema commit|via _schema_change_set

# === SCHEMA CONSTRUCTION ===

# schema_construction_principles(id|principle|rationale)
SCP1|Schema is data not code|hierarchical YAML/JSON files in git repo; loader produces both DB structure and API validation metadata from same source
SCP2|Single source of truth for schema and validation|conventional approach has DDL+validation-code as two stores that drift; this unifies them
SCP3|Closed constraint vocabulary|9 types + 3 modifiers + 6+ constraints = 18 primitives; adding a primitive is paper revision not user-extensible
SCP4|No embedded logic|no expressions+formulas+function calls+conditionals in schema files; loader parses validates applies; never evaluates
SCP5|No regex|DoS vector + dialect variation + unpredictable edge cases + adds embedded mini-language
SCP6|Repository creates OpsDB initially|loader reads files+generates engine-DDL+populates _schema_* tables; nothing about bootstrap requires running OpsDB
SCP7|Schema evolution governed|changes flow through _schema_change_set with stricter approval rules
SCP8|Repo and OpsDB synchronized by construction|executor is only path to schema changes
SCP9|Storage engine portable|schema declarations engine-independent; primitives map to standard SQL features
SCP10|API stays simple by refusing what doesn't belong|each refusal closes off complexity that would propagate into every consumer
SCP11|Discipline costs schema gymnastics buys decade-scale stability|absolute rules enable simple consumers; partial enforcement is worse than full

# schema_vocabulary(id|primitive|kind|purpose|notes)
SV_T1|int|type|signed integer|min_value+max_value (inclusive)
SV_T2|float|type|floating-point number|min_value+max_value+precision_decimal_places
SV_T3|varchar|type|bounded-length character string|max_length REQUIRED+min_length (default 0)
SV_T4|text|type|long string|max_length optional
SV_T5|boolean|type|true or false|no constraints beyond nullability
SV_T6|datetime|type|high-precision timestamp|engine native
SV_T7|date|type|date without time|none
SV_T8|json|type|typed payload|json_type_discriminator REQUIRED
SV_T9|enum|type|closed set of allowed values|enum_values REQUIRED
SV_T10|foreign_key|type|reference to id field of another entity|references REQUIRED
SV_M1|nullable|modifier|defaults false; explicit declaration encouraged|all types
SV_M2|default|modifier|literal value only; computed defaults forbidden|not for foreign_key+datetime+json
SV_M3|unique|modifier|field's values unique across all rows|composite uniqueness via indexes list with unique:true
SV_C1|min_value+max_value|constraint|inclusive numeric bounds|int+float
SV_C2|min_length+max_length|constraint|character length bounds|varchar+text; max_length required for varchar
SV_C3|enum_values|constraint|closed list of permitted values|enum
SV_C4|references|constraint|target entity name|foreign_key
SV_C5|precision_decimal_places|constraint|maximum decimal places|float
SV_C6|must_be_unique_within|constraint|composite uniqueness scope|loader generates composite unique index

# schema_forbidden(id|refusal|reason|alternative)
SF1|No regex|DoS vector + dialect variation + unpredictable edge cases + embedded mini-language|enum sets + length bounds + prefix/suffix as enum-of-prefixes; richer matching at API semantic-validation
SF2|No embedded logic|every value in schema file is literal; loader does not evaluate|defaults are literals only (no now()+no previous_value+1)
SF3|No conditional constraints|cross-field invariants not in schema|belong at API semantic-validation step (policy data)
SF4|No inheritance|no extends+no parent entity+no shared base class|two entities with similar fields each declare independently; reserved fields are controlled exception
SF5|No templating|no template variables+no parameterized files+no macros|variation across environments via OpsDB runtime config not different schemas; one schema per OpsDB
SF6|No imports within entity files|entity files do not import other files|only directory.yaml imports
SF7|No deletions of fields/entities|deletion breaks history+version rows+audit log|deprecate (mark _schema_field deprecated); column remains; tombstone forever
SF8|No renames|renames break every consumer|add new field with new name + deprecate old (duplication pattern)

# schema_evolution_allowed(id|change|why_safe)
SX_A1|adding new field nullable=true|existing rows have no value (fine because nullable)
SX_A2|adding new enum values|existing rows holding previous values remain valid
SX_A3|widening numeric ranges|min_value decreased OR max_value increased; never the reverse
SX_A4|widening length bounds|max_length increased; never decreased
SX_A5|adding new entity types|entirely additive; no impact on existing entities
SX_A6|adding new indexes|improves query performance; does not affect data validity
SX_A7|adding new approval rule references|tightens governance for new changes; existing rows unaffected

# schema_evolution_forbidden(id|forbidden|why|alternative)
SX_F1|deleting fields|breaks history+version rows reference value+audit log entries reference field changes|deprecate; column+data remain; tombstone forever
SX_F2|renaming fields or entity types|breaks every consumer|add new field with new name + deprecate old
SX_F3|changing field types|all break consumers|duplication+double-write pattern
SX_F4|narrowing numeric ranges|existing rows might hold values now out of range|widening only allowed direction
SX_F5|narrowing length bounds|existing strings might exceed new bound|widening only allowed direction
SX_F6|removing enum values|existing rows might hold removed value|duplication pattern with new field of narrower set
SX_F7|tightening uniqueness|existing rows might violate constraint|duplication pattern
SX_F8|removing indexes|usually a mistake|change steward must verify; validator does not check

# type_change_pattern(step|action|duration|purpose)
ST_1|Add new field with new type|both fields exist in schema and table|both available
ST_2|Begin double-writing|all code writing old field updated to also write new|N successful release cycles (3-5 typical)
ST_3|Migrate readers|code reading from old field updated to read from new|until reads of old field rare or zero
ST_4|Mark old field deprecated|update _schema_field deprecated flag|immediate; signals new code should not use old
ST_5|Continue double-writing|values still written for safety; old field becomes tombstone|additional cycles until steward confirms no consumers
ST_6|Old field never removed|remains as tombstone deprecated|indefinitely; storage cost is price of stable history

# cross_field_split(concern|layer|mechanism)
CFS1|per-field bounds|schema|closed vocabulary; mechanical; lookup-time validation
CFS2|cross-field invariants|policy data|policy rows of type semantic_invariant; evaluated at API semantic-validation step
CFS3|examples cross-field|policy|"if status=X then Y must be set"|"min_replicas <= max_replicas"
CFS4|why split holds|architectural|schema rarely changes (hot path bound validation simple); semantic invariants change often (kept in change-mgmt pipeline)

# json_payload_vocabulary(id|type|properties|notes)
JV1|list|element_type REQUIRED+element-prefixed constraints+min_count+max_count|every list has max count; elements have own bounds
JV2|map|key_type+value_type with respective constraints+max_entries|every map has max_entries; keys and values have bounds
JV3|recursion depth limit|JSON payload schemas one level deep into JSON structure|deep nesting forbidden; signal to factor into separate entities
JV4|forbidden in JSON|lists of lists+maps of lists+lists of maps|payload needing nested structure factors into separate entities

# meta_schema_bootstrap(step|action)
MB1|loader loads meta-schema from meta/_schema_meta.yaml|validated against loader's hardcoded baseline
MB2|loader loads conventions/reserved.yaml|validated against meta-schema
MB3|loader processes imports list from directory.yaml in order|each file validated against meta-schema; FK refs resolved against entities loaded so far
MB4|loader generates engine-appropriate DDL|CREATE TABLE+CREATE INDEX+FK and CHECK constraints
MB5|loader applies DDL to storage engine in dependency order|database structure created
MB6|loader inserts rows into _schema_* tables|describing loaded schema; row in _schema_version with is_current=true
MB7|OpsDB ready|API can begin serving requests; runners can begin operating

# === ACTIVE LAYER: RUNNERS ===

# runner_pattern(id|aspect|content)
RP1|get from OpsDB → act in world → set to OpsDB|three-phase shape every runner shares
RP2|OpsDB is runner's only stable interface|other interfaces transient and change; OpsDB schema versioned and absorbs change additively
RP3|persistent inputs and outputs are exclusively OpsDB rows|world is read-from and acted-upon but only OpsDB persists
RP4|get phase produces no side effects|clean phase separation
RP5|act phase produces side effects|library-mediated; bounded; idempotent or with uniqueness keys
RP6|set phase records what happened|every write through API; every write produces audit_log_entry
RP7|no runner directs another runner|coordination implicit through shared data; no orchestrator
RP8|coordination through shared substrate|runner B reads what runner A wrote on B's next cycle; OpsDB is rendezvous
RP9|crashed runner blocks no other runner|next cycle picks up where it left off
RP10|runner small enough to be fully knowable|200-500 lines runner-specific logic; libs do heavy lifting
RP11|runner is data-defined|configuration in runner_spec_version.runner_data_json; changing what runner does = changing data
RP12|runner authority is data not code|capabilities scoped through policy data; no runner has hardcoded admin rights
RP13|in-memory state for one cycle only|persistent state in OpsDB; long-running runners check OpsDB each cycle
RP14|every API write produces audit|no out-of-band path

# runner_lifecycle(id|phase|what_happens|invariant)
LP1|Invocation|external trigger starts runner instance|runner does not invoke itself
LP2|Get|read runner_spec_version + needed data through API|each row carries freshness+version metadata; no side effects
LP3|Internal Computation|compute planned action set; diff|decisions|target selection|no side effects; output is concrete inspectable plan
LP4|Dry-Run Output|render planned action set if dry-run mode enabled|exits without executing when dry_run=true; deterministic
LP5|Act|execute planned actions through shared libs with retry/backoff/idempotency|each action bounded per runner_data_json
LP6|Set|write runner_job + output_vars + per-target rows + evidence + observation + change_set as appropriate|every write through API
LP7|Recorded Outcome|audit_log_entry produced for every write|full trail queryable

# runner_kinds(id|name|purpose|reads|writes|gating|trigger)
RK1|Puller|read authority transform to schema write to cache|runner_spec+authority+prometheus_config|observation_cache_*+runner_job|direct write|scheduled
RK2|Reconciler|read desired+observed compute diff act|entity rows desired+observation_cache_* observed+policies|runner_job+target bridges+possibly change_set|varies per target|scheduled or long-running
RK3|Verifier|check scheduled work happened or state correct|schedule+target+prior evidence_record|evidence_record+target bridges+runner_job|direct write|scheduled
RK4|Scheduler|enforce runner_schedule on target substrate|runner_schedule+schedule+target+substrate info|runner_job+side effects (cron+systemd+CronJob)|auto-approved or approval|long-running
RK5|Reactor|edge-triggered response to events|event+runner_spec_version|runner_job+downstream rows|varies; mostly observation|event
RK6|Drift Detector|reconciler-shape that proposes not acts|same as reconciler|change_set+runner_job|through change_set discipline|scheduled
RK7|Change-Set Executor|read approved change_set apply field changes|change_set status=approved+change_set_field_change|entity rows+*_version rows+change_set status|direct write after approval|triggered by approved change_set
RK8|Reaper|apply retention policies trim old rows|retention_policy+target tables|deletes from cache+is_active=false on entities+runner_job|direct on cache; soft-delete follows policy|scheduled
RK9|Bootstrapper|set up new machines from minimal state|templated config+host_group+package_version|machine row+observation+runner_job|auto-approved|new-host trigger
RK10|Failover Handler|detect primary failure perform failover verify update OpsDB|observation_cache_state+failover policy+topology|change_set+evidence_record+runner_job+side effects|emergency-change or fast-track|event or scheduled

# runner_disciplines(id|name|statement|enforcement)
RD1|Idempotency|every runner action safely retryable; same inputs→same end state|change_set_field_change.applied_status; uniqueness markers; library handles mechanics
RD2|Level-Triggered Over Edge-Triggered|read current state act on it not react to event streams as only source|reconcilers re-evaluate every cycle; reactors paired with reconciler backstops
RD3|Bound Everything|every runner has explicit retry/time/queue/memory/scope bounds|runner_job records what bound was hit if execution stopped early

# gating_modes(id|mode|when_used|examples|approval)
RG1|Direct Write|observation-only data; never goes through change management|pullers+verifiers+reapers+most reactors|none; audit only
RG2|Auto-Approved Change Set|change set recorded+audited+policy auto-approves without human|drift correctors+cert renewers+credential rotations+minor patches|policy evaluates rule and approves
RG3|Approval-Required Change Set|change set routes to human approvers|production DB changes+security policy+compliance scope+schema changes|human evaluates and approves

# gating_per_target(scenario|behavior)
GT1|same runner code different targets|gating mode is per-runner-spec AND per-target via policy
GT2|drift-correction in staging|auto-approve (low stakes fast iteration)
GT3|drift-correction in production low-risk fields|auto-approve (timeouts+replica counts within bounds)
GT4|drift-correction in production outside low-risk set|approval-required
GT5|drift-correction on compliance-restricted entities|refuse to act; file finding for compliance review

# stack_walking(id|decision|walk|enables)
RW1|Decommission Awareness|service→host_group→machine→megavisor_instance walking parent chain|reconciler skips action and logs why
RW2|Failure Domain Analysis|primary+replica each walked to ancestry; compare rack/DC|failover refuses if shared
RW3|Capacity Awareness|K8s nodes→underlying machines→hardware sets|sees actual hardware capacity
RW4|Dependency-Aware Change Validation|service_connection rows from targeted service to dependents|validator files warning or rejects change breaking downstream
RW5|Locality-Aware Deployment|service→preferred locations→available capacity per location|schedules where capacity exists and locality matches policy

# gitops_cast(runner_id|name|reads|writes|role)
RC1|Helm Change-Set Executor|approved change_set targeting k8s_helm_release_version+configuration_variable|entity rows updated+runner_job_output_var (new version ready)|closes change-mgmt loop on data
RC2|Helm Git Exporter|output var from RC1+config vars (secrets resolved at render via vault)|git commit with structured message linking change_set ID+tag|exports OpsDB intent to git
RC3|Argo CD or Flux|git repo|cluster state|EXTERNAL not OpsDB runner
RC4|Kubernetes Deploy Watcher|cluster watch API|observation_cache_state pod transitions+output vars (rollout_succeeded+pod_count+image_digest_deployed+errors)|records observed cluster outcome
RC5|Image Digest Verifier|change_set intended digests+RC4 output vars actual deployed digests|evidence_record(deployment_verification)+compliance_finding if mismatch|verifies intent matches reality
RC6|Drift Detector|OpsDB-known helm release version+cluster-observed helm release version|finding or auto-correct per policy|backstop for ongoing alignment

# gitops_disciplines(domain|sot|why)
GD1|intent|OpsDB (change_set+helm release version)|describes what was wanted
GD2|whats-checked-in-to-be-applied|git|Argo CD reconciles git-to-cluster
GD3|live state|cluster|pulled into OpsDB cache via RC4
GD4|the trail|OpsDB|all above tied together by IDs

# runner_anti_patterns(id|name|description|violates)
RA1|Orchestrating Other Runners|runner invokes other runners directly|RP7 (no runner directs another)
RA2|State Outside OpsDB|runner persists state in local files OpsDB does not reflect|RP3
RA3|Reinventing Shared Libraries|runner implements own retry/K8s client/logging|R06 one-way-to-do-each-thing
RA4|Acting on Stale Cache Without Freshness Check|reads observation_cache_* without checking _observed_time|LP2
RA5|Logic in Template Variables|template-time computation embedded in templates|RP11 (data-defined runner)
RA6|Skipping Audit Trail|bypasses API to avoid audit|RP14
RA7|Long-Running Runners with In-Memory State Across Cycles|accumulates state in memory between cycles|RP13
RA8|Multi-Domain Runners|deployment runner that also does monitoring+alerting+capacity|RP10 (small enough to be knowable)
RA9|Privileged Authority Not Expressed as Policy|runner has admin rights hardcoded into runtime|RP12 (authority is data)
RA10|Treating OpsDB as Queue|polls OpsDB as message queue treating every row as job|misuses RP1 pattern
RA11|Bypassing Change Management for Speed|routes around change-mgmt for non-emergency reasons|RP14

# === API GATE ===

# api_principles(id|principle|rationale)
AP1|API is the single gate|every interaction with OpsDB data passes through it; no out-of-band path
AP2|API is self-contained operational software|not built on K8s/cloud/orchestrator/anything OpsDB models; outlives all authorities
AP3|API delegates only authentication and credential resolution|IdP for human auth+secret backend for credentials; everything else local
AP4|API does not invoke runners|every operation request-driven; no internal scheduler; no triggers fire on state transition
AP5|API does not communicate with stakeholders|notification dispatch is a runner concern; API records state transitions
AP6|API does not apply approved change_sets|change-set executor runner drains the queue; API gates the apply-writes
AP7|API gates+validates+routes+records+responds|runners do world-side work
AP8|every operation traverses the same gate|10 enforcement steps applied uniformly
AP9|configuration as data not code|all governance evaluated against OpsDB rows; changing what API enforces = changing data
AP10|0/1/N rule applied|one gate not two; one auth layer not parallel; one audit table not per-domain
AP11|schema validation forbids regex|DoS vector + complexity sink; declarative bounds only
AP12|append-only at strictest level for audit log|DDL enforces no UPDATE/DELETE for any role
AP13|API stays simple by refusing what doesn't belong|each boundary kept makes API better at what it does

# api_operations(id|name|class|purpose|gating)
AO1|get_entity|read|fetch one row by primary key|five-layer auth
AO2|get_entity_history|read|fetch version chain for one entity|five-layer auth
AO3|get_entity_at_time|read|reconstruct field values active at timestamp|five-layer auth; one row lookup
AO4|search|read|discovery surface across entity types|five-layer auth+bounds
AO5|get_dependencies|read|walk substrate hierarchy or service connections|five-layer auth+depth+cycle bounds
AO6|resolve_authority_pointer|read|where-is-X lookup|five-layer auth
AO7|change_set_view|read|scoped or full view of change set for approver|filtered to viewer's approval scope
AO8|write_observation|write-direct|runner writes observation/evidence|runner report key + five-layer auth
AO9|submit_change_set|write-cs|propose N field changes with reason|five-layer + validation pipeline + dry_run
AO10|approve_change_set|cm-action|stakeholder approves|verify caller in required approver group
AO11|reject_change_set|cm-action|stakeholder rejects|verify caller in required approver group
AO12|cancel_change_set|cm-action|withdrawal|submitter or sufficient authority
AO13|emergency_apply|write-cs|break-glass path|emergency authority per policy
AO14|bulk_submit_change_set|write-cs|transaction touching many entities|chunked validation+different approval rules possible
AO15|apply_change_set_field_change|write-direct|executor applies one field change|verify executor authority+change_set in approved+not yet applied
AO16|mark_change_set_applied|cm-action|finalize change set status|verify all field changes applied successfully

# gate_steps(step|name|what_happens|failure)
AG1|1 Authentication|verify caller identity against IdP (humans) or secret backend (runners); resolve to ops_user or runner_machine|invalid creds → reject + audit
AG2|2 Authorization|evaluate five-layer model against operation+target+caller; first denial fails|first denial → reject with layer info + audit
AG3|3 Schema Validation|verify operation shape matches registered schema for affected entity types and fields|malformed → reject with structured error
AG4|4 Bound Validation|verify field values within declared bounds (numeric+enum+FK+anchored patterns)|out-of-bounds → reject; no regex evaluated
AG5|5 Policy Evaluation|consult policy rows for additional governance|violation → reject
AG6|6 Versioning Preparation|prepare version row to be written for change-managed entities|none (preparation step)
AG7|7 Change Management Routing|evaluate approval_rule policies+compute required approver groups+write change_set_approval_required|determines auto-approve vs human approval vs blocking
AG8|8 Audit Logging|record operation in audit_log_entry with full attribution; append-only|atomic with operation outcome
AG9|9 Execution|apply atomic write OR record change_set+field_changes OR record approval/rejection|substrate failure → recorded in audit
AG10|10 Response|return result with metadata|none

# auth_layers(id|layer|source_data|check|denial)
AL1|Standard Role and Group|ops_user_role_member+ops_group_member|baseline access by role mapping to operation classes|operation rejected at layer 1
AL2|Per-Entity Governance|_requires_group field on rows|caller must be member of named group beyond layer 1|operation rejected at layer 2
AL3|Per-Field Classification|_access_classification on fields/tables|caller's clearance must meet or exceed classification|specific fields omitted or operation rejected
AL4|Per-Runner Authority|runner_capability+runner_*_target bridges|operation must match runner's declared scope|operation rejected at layer 4
AL5|Policy Rules|policy rows of type access_control|time-of-day+SoD+tenure-based|reject OR inject additional approval requirements
# composition: AND across all 5; first denial halts; audit records which layer denied + triggering policy

# auth_delegation(concern|delegated_to|api_owns|why)
AD1|human identity verification|IdP (LDAP|AD|OIDC|SAML)|ops_user mapping rows|identity changes are HR-driven; fast-moving
AD2|credential values|secret backend (Vault+equivalents)|pointers to where credentials live|secrets need-to-know+audit-on-read+ephemeral semantics
AD3|operational authorization|nothing - locally enforced|access policies+policy rules|slower governance-driven; mixing with identity creates drift
AD4|runner identity|secret backend issues credentials|runner_machine mapping|runners authenticate with own service account credentials

# change_set_lifecycle(state|meaning|transitions_to|observed_by)
LC1|draft|under construction; not yet submitted|submitted|submitter
LC2|submitted|API received|validating (automatic)|API
LC3|validating|lint+schema+semantic+policy+lint checks running|pending_approval (success) | draft with errors (recoverable) | rejected (unrecoverable)|API
LC4|pending_approval|validation passed; awaiting stakeholder approvals|approved | rejected | expired | cancelled|notification runner reads
LC5|approved|all required approvals received; ready for to-perform queue|applied|change-set executor runner reads
LC6|applied|executor successfully applied all field changes|terminal (only rolled back via new change_set)|none
LC7|rejected|required approver rejected per rule's rejection semantics|terminal|none
LC8|expired|submission deadline passed without sufficient approvals|terminal|none
LC9|cancelled|submitter or sufficient authority withdrew|terminal|none
LC10|failed|bulk apply chunk failed; rolled back|terminal; finding filed|none
LC11|applying|substate during bulk apply|applied | failed|specialized executor

# stakeholder_routing(step|action|source|result)
SRT1|enumerate field changes|read change_set_field_change rows|change_set+field_changes|list of (entity_type+entity_id+field) tuples
SRT2|walk ownership bridges|service_ownership+machine_ownership+k8s_cluster_ownership+cloud_resource_ownership|bridge tables|ops_user_role rows responsible
SRT3|walk stakeholder bridges|service_stakeholder+other stakeholder bridges|bridge tables|additional non-ownership roles
SRT4|evaluate approval rules|policy rows of type approval_rule against entity+namespace+fields+metadata|approval_rule policies|requirements per matching rule
SRT5|compute requirements|one or more change_set_approval_required rows|computed at submit|written to OpsDB
SRT6|track fulfillment|each requirement independent; all must be fulfilled|change_set_approval_required.fulfilled_count|change_set transitions to approved when all is_fulfilled

# validation_pipeline(id|type|checks|failure_behavior)
VP_1|Schema Validation|every field change matches entity's schema; field exists+type matches+required fields present on creates|blocks
VP_2|Bound Validation|numeric ranges+enum membership+FK existence+simple anchored patterns|blocks
VP_3|Semantic Validation|cross-field invariants (min<=max+status implies dependent field set)|blocks
VP_4|Policy Validation|change does not violate active policies|blocks fail-closed OR warns with explicit ack
VP_5|Lint Validation|org style+naming+required metadata populated+descriptions present|warnings allow proceed; errors block
VP_6|Dependency Check|service_connection walks verify change does not break downstream contracts|blocks unless dependents tolerant or modified in same change_set

# auto_approval(category|gating|examples)
AA1|Direct Write Path|no change_set; just authenticated write|cached observation+evidence_record+runner_job_output_var
AA2|Auto-Approved|change_set transitions through validating→pending_approval→approved without human|drift corrections in non-prod+routine credential rotations+low-risk reconciler outputs+minor patch upgrades
AA3|Approval Required|routes to human approvers per matching rules|production database changes+security policy+compliance scope+schema changes+high-severity alert config
AA4|Per Target Per Runner|same runner has different gating for different targets via policy|runner auto-approves staging drift+approval-required production drift+refuses compliance-restricted

# emergency_path(aspect|rule)
EM1|Authority|caller has emergency authority per policy
EM2|Approval|reduced approvals (often single approver+sometimes self-approved)
EM3|Flag|change_set.is_emergency=true+change_set_emergency_review row in pending status
EM4|Review Window|72 hours default (organizationally configurable)
EM5|Overdue|verifier runner files emergency_review_overdue finding+escalates every 24 hours
EM6|No Auto Rollback|emergency change might be load-bearing
EM7|Audit|always recorded as emergency; queryable; non-negotiable that all emergency changes reviewed eventually

# bulk_operations(aspect|behavior)
BU1|Validation|chunked at default 1000 field changes; interim feedback per chunk
BU2|Coherence|change_set remains one unit; either all chunks validate and transition together or fail together
BU3|Apply Phase|chunked apply; change_set in applying substate until all chunks complete
BU4|Failure Recovery|if any chunk fails during apply: roll completed chunks via version sibling rows+transition to failed+file finding
BU5|Approval Variation|bulk may require one approval for bundle rather than per-entity
BU6|Common Use Cases|fleet-wide credential rotation+policy rollouts+schema-coordinated migrations

# concurrency_model(step|mechanism)
CON1|Draft|each change_set_field_change carries version stamp of entity drafted against
CON2|Submit|API checks each touched entity's current version against drafted-against version|fails loud with stale_version error
CON3|Recovery|submitter retrieves current values+reconciles proposed change against new state+resubmits
CON4|Approval|approvers never see stale state because submit failed already

# runner_report_keys(aspect|content)
RKS1|schema|runner_report_key entity declares runner_spec_id+report_target_table+report_key+report_key_data_json+is_active; versioned via sibling
RKS2|target tables|observation_cache_metric|observation_cache_state|observation_cache_config|runner_job_output_var|evidence_record
RKS3|scope|declarations at runner_spec level not runner_machine level
RKF1|API receives runner write to one of five target tables|standard auth runs first
RKF2|API looks up runner_report_key rows for runner's spec + target table|finds declared keys
RKF3|API checks submitted key against declared set|undeclared → reject with undeclared_report_key + audit
RKF4|API validates submitted value against report_key_data_json constraints|invalid → reject with invalid_report_key_value + detail
RKF5|API performs write+records audit+responds|standard write completion
RKV1|Prevents misconfigured/compromised puller writing arbitrary keys
RKV2|Prevents evidence-runner emitting evidence types outside its declared scope
RKV3|Strengthens audit trail: every observation/evidence/coord-output traceable to declared authorization
RKV4|Strengthens compliance provenance: every evidence_record traceable to runner+declaration via standard joins
RKV5|Fails Closed: declared scope IS the writable surface; legitimacy is declarative not implicit

# audit_log_properties(id|aspect|content)
AU1|Writer|API only; no direct DB writes for any role
AU2|Append Only|DDL grants no UPDATE/DELETE on audit_log_entry for any role including substrate operators
AU3|Crypto Chain|optional _audit_chain_hash; each entry hashes own contents + prior entry hash
AU4|Retention|policy-driven; compliance regimes typically 7+ years
AU5|Audit of Audit|deletions of audit rows recorded in separate audit-of-audit table
AU6|Query Access|auditor role: read access to audit_log_entry+version siblings+change-mgmt records+evidence+policy
AU7|Anomaly Handling|partial-write/invalid-timestamp/malformed entry → mark in separate audit_log_anomaly table; never modify original row
AU8|Sole Strict Append-Only|other tables look append-only but actually permit updates/deletes; audit log uniquely strict
AUF1|Operation Identity|API endpoint called+method+action_type structured operation class
AUF2|Caller Identity|acting_ops_user_id (humans)+acting_service_account_id (runners)+both populated for web-mediated
AUF3|Target Identity|target_entity_type+target_entity_id; multi-target ops use bridge tables
AUF4|Operation Detail|request_data_summary+response_data_summary; structured
AUF5|Result|success|validation_failed|authorization_denied|rate_limited|internal_error
AUF6|Context|client IP+user agent+request ID+change_set_id where applicable
AUF7|Timestamp|API-supplied high-precision monotonic
AUF8|Optional|_audit_chain_hash for tamper-evidence regimes
TE1|Mechanism|each audit_log_entry includes hash covering entry contents + prior entry's hash
TE2|Chain Property|modification of any historical entry breaks chain at that point and all subsequent
TE3|Verification|tooling reads chain forward+recomputes each hash+detects breaks
TE4|Break Treatment|detected break is itself a finding (tampered with OR substrate fault corrupted chain)
TE5|Opt-In|per regime requirements

# === LIBRARY SUITE ===

# library_principles(id|principle|rationale)
LL_P1|Contract not implementation|library is contract specification; multiple implementations of same contract coexist; runner pins to contract not impl
LL_P2|Suite is one suite|within org one library suite; N language impls of same contract valid; parallel suites in same language forbidden
LL_P3|Library/runner boundary by mechanical test|"would two runners reimplement this?" yes→library; no→runner
LL_P4|Runners stay small because libraries do heavy lifting|~200 lines runner with suite vs ~1500 without; 50 lines glue+150 lines runner-specific
LL_P5|Mandatory libraries enforce single path|API client mandatory+observation libraries mandatory
LL_P6|Library evolution by accretion|pattern in 1 runner stays in runner; pattern in 3 candidate; pattern in 10 confirmed extraction
LL_P7|Pulling logic out of library back into runners is rare|once library others depend; removal forces reimplementation everywhere
LL_P8|Library is operational realization of one-way-to-do-each-thing|applied to runner-world interaction
LL_P9|Two-sided policy enforcement|API gate at OpsDB write time + library suite at world-side action time
LL_P10|Library refuses fragmentation|team wanting "their own version" solving real problem; absorb into standard
LL_P11|Templates deliberately dumb|substitution+inclusion only; logic-needing-templates upstream into runners producing concrete values
LL_P12|Secrets never persisted by library|in memory only during call; logging records path+caller+timestamp+result never value
LL_P13|Library validates inputs at call boundary|rejects malformed before reaching world or OpsDB
LL_P14|Library propagates correlation IDs|runner_job_id root → API call chain → audit_log_entry; query joins via correlation field

# library_families(id|family|naming_prefix|role)
LF1|API access|opsdb.api|the only path runners use to touch OpsDB; mandatory
LF2|World-side substrate|opsdb.world.*|wrappers per external substrate
LF3|Coordination and resilience|opsdb.coordination.*|retry|circuit_breaker|hedger|bulkhead|failover
LF4|Observation|opsdb.observation.*|logging|metrics|tracing; mandatory and uniform
LF5|Notification|opsdb.notification|channel-agnostic notification operations
LF6|Templating and rendering|opsdb.templating.*|deliberately dumb; substitution+inclusion only
LF7|Git operations|opsdb.git|clone|commit|push|tag|PR

# libraries(id|name|family|mandatory|purpose)
LL1|opsdb.api|LF1|yes|only path runner→OpsDB; auth+correlation+stale-version+audit
LL2|opsdb.world.kubernetes|LF2|conditional|K8s API access for runners
LL3|opsdb.world.cloud|LF2|conditional|provider-agnostic cloud ops with per-provider backends
LL4|opsdb.world.host|LF2|conditional|SSH+remote command for legacy substrate
LL5|opsdb.world.registry|LF2|conditional|container/artifact registry access
LL6|opsdb.world.secret|LF2|conditional|secret backend access; never persists values
LL7|opsdb.world.identity|LF2|conditional|IdP operational queries (lookup+membership+watch)
LL8|opsdb.world.monitoring|LF2|conditional|monitoring authority queries
LL9|opsdb.world.pointer|LF2|convenience|resolve_and_fetch given authority_pointer_id
LL10|opsdb.coordination.retry|LF3|optional|retry+backoff+jitter+idempotency keys
LL11|opsdb.coordination.circuit_breaker|LF3|optional|prevents cascading failure; per-target state
LL12|opsdb.coordination.hedger|LF3|optional|reduce tail latency via redundant requests
LL13|opsdb.coordination.bulkhead|LF3|optional|isolate failure domains via bounded resource pools
LL14|opsdb.coordination.failover|LF3|optional|primary→replica routing
LL15|opsdb.observation.logging|LF4|yes|structured log format with correlation+runner_job_id
LL16|opsdb.observation.metrics|LF4|yes|metrics emission in standard format; validates against runner_capability decl
LL17|opsdb.observation.tracing|LF4|yes|distributed trace context propagation
LL18|opsdb.notification|LF5|conditional|email|chat|page|ticket; channel-agnostic
LL19|opsdb.templating.helm_values|LF6|conditional|render helm values from OpsDB config
LL20|opsdb.templating.config|LF6|conditional|render config templates with substitution+inclusion+bounded iteration
LL21|opsdb.templating.report|LF6|conditional|generate reports for human consumption
LL22|opsdb.git|LF7|conditional|git ops via secret-backend creds

# api_client_operations(id|operation|class|notes)
LA1|get_entity|read|primary key fetch
LA2|get_entity_history|read|version chain
LA3|get_entity_at_time|read|single lookup against version sibling
LA4|search|read|discovery surface
LA5|get_dependencies|read|library translates pattern to API search calls
LA6|resolve_authority_pointer|read|library does NOT fetch from authority
LA7|change_set_view|read|filtered to viewer permissions
LA8|write_observation|write-direct|library validates report-key authorization locally fail-fast before round-trip
LA9|submit_change_set|write-cs|library handles structured construction+optimistic concurrency stamps+dry-run support
LA10|approve_change_set|cm-action|caller identity verified through API
LA11|reject_change_set|cm-action|none
LA12|cancel_change_set|cm-action|withdrawal
LA13|emergency_apply|write-cs|break-glass
LA14|apply_change_set_field_change|write-direct|executor's apply-write
LA15|mark_change_set_applied|cm-action|finalize after all field changes applied
LA16|watch|stream|library handles stream+reconnect+resume; on reconnect fetches current state then streams from token (always level-triggered backstop)

# coordination_patterns(id|library|pattern|composition)
COP1|LL10|retry+backoff+jitter|with_retry|with_idempotency_key; composes inside every outbound lib
COP2|LL11|circuit_breaker|state per-runner-instance default OR synced via observation_cache_state per target
COP3|LL12|hedger|requires operation marked idempotent; library validates before allowing hedge
COP4|LL13|bulkhead|domain_key per call; pool sizing+queueing+timeout per policy
COP5|LL14|failover|primary→replicas in order; hides topology

# observation_libraries(id|library|format|special)
OL1|LL15 logging|JSON or logfmt; timestamp+severity+runner_job_id+correlation_id+runner_spec name+version+runner_machine_id+source location|destination from runtime env
OL2|LL16 metrics|prometheus or statsd or datadog; counter_increment|gauge_set|histogram_observe|timer|labels validated against runner_capability declarations; metrics not declared rejected (analog of report_keys for outbound)
OL3|LL17 tracing|OTel or vendor-native; start_span|with_span|inject/extract_trace_context|trace IDs correlated with audit_log_entry+runner_job

# templating(aspect|content)
LT1|allowed|variable substitution {{ var }}+inclusion {{ include "other" }}+bounded iteration
LT2|forbidden|expressions+filters+conditionals over expressions+function calls+embedded code
LT3|why dumb|template language with logic accumulates; authors find it easier to add conditional than runner; templates become opaque code embedded in supposed-data
LT4|cost|occasional duplication
LT5|benefit|templates inspectable as data
LT6|upstream pattern|logic in runner produces concrete value as configuration_variable+template substitutes variable

# two_sided_enforcement(id|surface|enforces_against|input)
TS1|API gate|OpsDB writes|10-step gate sequence|caught before persisting
TS2|library suite|world-side actions|runner declarations as OpsDB rows|caught before reaching substrate
TS3|composition|both surfaces use same input (runner declarations) → produce same fail-closed result
TS4|comprehensive coverage|runner cannot through any path act outside declared scope: writes caught at gate+world-side caught at library
TS5|"runner authority is data" holds across every action|every authority is data+every check mechanical+every failure fail-closed and audit-logged

# policy_validation(library|extracted_target|declaration|failure)
PV1|LL2 K8s|cluster+namespace|runner_k8s_namespace_target|library_authorization_denied
PV2|LL3 cloud|cloud_account_id|runner_cloud_account_target|same shape
PV3|LL4 host|host_id|machine target OR host_group target|same shape
PV4|LL5 registry|registry+repo|runner registry access decl|same shape
PV5|LL6 secret|secret path|runner secret access target|same shape
PV6|LL18 notification|channel_id|runner notification scope+paging authority for pages|same shape
PV7|LL22 git|repo|runner repo access decl|same shape

# fail_closed_discipline(aspect|content)
FC1|principle|if library cannot determine authorization → refuse rather than allow
FC2|partition tolerance|library uses last-known-good cache of declarations
FC3|bounded staleness|after threshold library refuses calls because declarations no longer trusted
FC4|threshold per-library policy-driven|short for security-sensitive (secrets+paging+cloud provisioning); longer for benign

# library_versioning(id|aspect|content)
LV1|semver|MAJOR.MINOR.PATCH
LV2|PATCH|bug fixes no contract change
LV3|MINOR|new operations OR backward-compat extensions
LV4|MAJOR|breaks contract; rare; deprecation cycles required
LV5|deprecation pattern|new alongside old → both supported N cycles → deprecation warnings → runners migrate at own pace → removal only after steward confirms; parallels schema duplication pattern
LV6|removal rare|most "deprecated" remain available indefinitely as legacy paths
LV7|test suite|every contract has test suite; new implementation gated by passing
LV8|coordination with schema evolution|library changes touching schema land schema change_set first → library version using new fields released after → runners migrate after; order matters

# === ADOPTION + IMPLEMENTATION ===

# org_commitments(id|commitment|requires)
OC1|Schema steward role|some person/team responsible for comprehensive coherence; reviews schema-evolution change_sets; resists fragmentation+feature creep|continuous responsibility; senior engineer/architect role
OC2|Investment in API|API is sophisticated and grows: new validation+approval workflows+audit requirements+query patterns|orgs that under-invest end up with database not OpsDB
OC3|Investment in shared library suite|runners cheap because libraries good; suite keeps runner population consistent at scale|investment compounds in cheap runners
OC4|Discipline of refusing fragmentation|every team wanting "small separate OpsDB for our use case" is solving real problem; absorb into existing schema|recurring discipline; pressure constant
OC5|Discipline of refusing feature creep|OpsDB is not wiki/monitoring/code repo/orchestrator/chat/ticketing/secrets manager|refuse and redirect each pressure to right system

# operational_disciplines(id|discipline|content)
OD1|Comprehensive thinking aggregate building|schema built incrementally; each piece approached with comprehensive thinking; thinking at level of whole; building at level of piece
OD2|One way to do each thing|within OpsDB-coordinated environment converge on one method per task; shared library suite is framework's enforcement
OD3|Idempotency level-triggering bounding|three load-bearing runner disciplines: idempotent+level-triggered+bounded
OD4|Bound everything|every long-running mechanism has explicit limits; every queue has max depth; every cache has max size; every connection has timeout; every retry has budget
OD5|Reversible changes|prefer mechanisms allowing rollback; rollback is itself change_set restoring prior values; side-channel rollbacks forbidden
OD6|Make state observable|what cannot be seen cannot be operated; OpsDB observable about itself by construction

# roles(id|role|responsibility|first_phase|continuous)
Ro1|schema steward|comprehensive coherence of schema; reviews schema-evolution change_sets; notices when slicing-the-pie needed; resists fragmentation+feature creep|P1 identifies; P2 active reviewer; P5 primary approver|yes
Ro2|library steward|coherence of library suite; reviews library proposals+contract additions+removals+cross-library coherence|P4 identifies (can be same as schema steward); P6 active in library extractions|yes
Ro3|substrate operator|DBA-equivalent for storage engine; backups+replication+capacity+performance tuning; direct DB access under SoD|P1 identifies; P3 deploys dev OpsDB; P5 coordinates dev-to-operational transition|yes
Ro4|platform team|owns API code+runner deployment infrastructure+day-to-day ops health; distinct from substrate operator and stewards|P1 identifies; P3 builds dev API; P4 builds foundational libraries; P5 implements production API+CM pipeline; P6 operates runner deployment|yes
Ro5|operational stakeholders|owners of entities OpsDB tracks; service owners+cloud account owners+K8s cluster owners|P5 identifies as part of writing approval rules|yes

# implementation_principles(id|principle|rationale)
IP1|Validation as gate not calendar|phase complete when criterion met not when duration elapsed; teams stay in phase until satisfied
IP2|Phased not top-down|architecture too large to build at once; top-down produces multi-quarter project delivering nothing usable until end
IP3|Each phase delivers operational value|Phase 3 dev substrate answers real questions; Phase 5 produces governance; Phase 6 produces benefits compounding
IP4|Each phase validates prior understanding before next|errors caught early when cheap
IP5|Bootstrap at largest cardinality from smallest|N=∞ pipeline at N=2 costs slightly more than N=1 at N=1; N=∞ retrofitted onto N=2-grown-independently costs much more
IP6|Schema quality determines everything downstream|well-formed scales+audit composes+automation works; poorly-formed imposes costs on every consumer for OpsDB lifetime
IP7|Get schema right at Phase 3 because revising is cheap then|after phases 3-5 expensive because data ingested under prior shape
IP8|Pick most painful or valuable domain first at Phase 6|investment substantial; phase 6 is when it compounds; high-pain first delivers immediate benefit
IP9|Phase 6 has no end ceremony|"covers what matters and absorbs new things cleanly"; work continues; structure stays stable

# phases(id|phase|decision|deliverable|validation)
Ph1|Decide cardinality|1-OpsDB OR N-DOS-1-OpsDB OR N-DOS-N-OpsDB|documented decision+rationale citing structural reasons; for N: documented sync pipeline plan committed to N=2 bootstrap|schema steward+operational lead agree+can name structural reasons; rationale not "easier" or "might need eventually"
Ph2|Determine baseline schema|how much of OPSDB-4 to adopt+what to add+what to validate by hand-loading|adapted schema repo per OPSDB-7; hand-loaded representative data covering 3+ domains; schema steward in role|representative subset of actual infrastructure expressible as data with no awkward fits
Ph3|Build dev API and start ingesting data|start writing real data into substrate before substrate is operational|dev OpsDB with real data from 3+ sources; schema iterated to fit data; DSNC applied; list-of-N test applied|team can answer real ops questions by querying
Ph4|Determine shared library core|minimum viable suite + what existing code becomes part of it|opsdb.api + opsdb.observation.logging; phase 3 scripts refactored; existing operational code inventoried+categorized|new ingestion script writable using only libraries; line counts small
Ph5|Design and implement change management|what CM pipeline looks like+which entities go through it|working CM pipeline with org's actual approval rules+emergency path+auto-approval policies; runners registered with declared scopes; dev-to-operational transition completed|configuration change as change_set validates+routes for approval+approves+applies+records with full trail queryable
Ph6|Add operational logic beyond OpsDB management|which operational domain to address first then which after|first operational runner in production addressing real domain; producing queryable trail; pattern for adding subsequent runners|OpsDB delivers operational benefit beyond own maintenance; real ops task previously requiring scattered tooling now runs through OpsDB-coordinated pattern

# n_bootstrap(aspect|content)
NB1|minimum N|2; three is larger case requiring more pipeline work
NB2|start at 2|even when org knows eventually 3+; forces N-mode action with minimal initial setup
NB3|catches failure modes early|schema sync at 2-substrates-still-small reveals propagation bugs+library deployment+version-pinning before operationally critical
NB4|cost argument|N=∞ pipeline at N=2 ≈ slightly more than N=1 at N=1; N=∞ retrofitted onto N=2-grown-independently = much more
NB5|by N=3|pipeline mature

# dsnc_flattening_rules(id|rule|example)
DSF1|flatten when nested data is per-row metadata of parent|EC2 instance_type+ami_id+vpc_id+subnet_id go in cloud_data_json as flat fields under ec2_instance discriminator
DSF2|break out when nested data has independent lifecycle OR identity OR appears in lists of N|security group memberships are many-to-many; bridge table per polymorphic-relationship pattern
DSF3|list-of-N test|when source has list of N items flattening to prefix_data_list_0_value+prefix_data_list_1_value+... is wrong; loses listness; N variable; indices positional
DSF4|naive flattening failure mode|EC2 with N attached EBS volumes flattened to ec2_data_volumes_0_id+ec2_data_volumes_1_id+team adds new fields each time encountering more
DSF5|correct shape|cloud_resource_attached_volume bridge table OR recognize EBS volumes are themselves cloud resources
DSF6|practical test during phase 3|when ingesting nested structure: any nested element with identity that could change independently of parent OR N of them = sub-table data not flat-payload

# dsnc_naming(aspect|content)
DSN1|names get long|cloud_resource_security_group_membership; service_authority_pointer_relationship_role; change_set_emergency_review_status
DSN2|verbosity is price of unambiguous structural meaning|each component carries meaning; pattern is parent_concept_subconcept_subconcept
DSN3|recompose without provenance loss|reading cloud_resource_security_group_membership tells you exactly: membership relating cloud resource and security group
DSN4|alternative produces drift|short names require institutional knowledge; new team members guess wrong; old members forget
DSN5|cost|keystrokes
DSN6|benefit|structural transparency; new tables fit pattern; readers learn pattern once apply across schema

# dev_to_operational_transition(aspect|dev|operational)
T1|API|minimal: authenticated reads+writes+structured errors only|full OPSDB-6 with 10-step gate
T2|change management|none|for change_managed entities
T3|authorization|rough role-based read/write|five-layer model
T4|runner report keys|none|enforced
T5|audit log|simple request logging|append-only with full attribution
T6|data ingestion|ad-hoc scripts|registered runners with declared scopes
TS_1|cutover not gradual|moment when dev API replaced and operational disciplines come online
TS_2|before moment|ad-hoc scripts can write to dev substrate
TS_3|after moment|only registered runners with declared scopes can write to operational substrate
TS_4|planned scheduled executed deliberately|team documents which data was loaded under dev API+turns on CM pipeline+registers runners+begins recording governance trails
TD1|data loaded under dev API|fine; there because team loaded during development
TD2|change_set history for that data|incomplete; that's acceptable for historical data
TD3|audit trails for initial loading|incomplete; OpsDB's claims about governance apply to changes after cutover not retroactively
TD4|schema metadata records schema version at cutover|canonical baseline; subsequent schema changes flow through _schema_change_set
TD5|runners replace scripts|same data sources continue feeding OpsDB but through registered runners

# capabilities(id|capability|what_it_means|enables)
IC1|One Place to Find Any Operational Fact|every operational fact has one authoritative location either held directly or pointed at|investigation no longer requires knowing N tools
IC2|Continuous Queryable Audit|every change goes through gate+every operation produces audit log+every change_set has approval trail+every entity has version history|"show me every production config change in last quarter and who approved each" is query result not binder assembly
IC3|Mechanical Change Governance|every change to centrally-managed data flows through change_sets|SoD enforceable as policy rules; approval scales with risk; emergency changes have break-glass with mandatory post-hoc review
IC4|Decentralized Work with Central Coordination|many small pieces of automation each independent; no orchestrator+no SPOF|coordination through shared data; runners replaceable/restartable/retirable
IC5|Point-in-Time Reconstruction|version history makes "what did this look like at time T" a single query|incident investigation+audit period boundary state+rollback as change_set restoring prior values
IC6|Schema Stability Across Decades|forbidden list (no deletions+renames+type changes) means consumers can trust schema|runner written 5 years ago still runs against same field names
IC7|Mechanical Defense Against Operator Error|schema rejects malformed writes+change-mgmt routes high-stakes to humans+validation checks invariants+bulk atomic+optimistic concurrency catches stale state|each closes off a category that otherwise produces incidents
IC8|Observability of Operations Itself|"which runners are running"+"which haven't run in 24h"+"which are hitting bounds" are direct queries|operations as a function becomes inspectable
IC9|Vendor Substrate Independence|self-contained operational software not built on cloud/orchestrator/commercial platform; schema portable|reorganization replacing cloud or orchestrator does not require replacing OpsDB
IC10|Compounding Benefits|each capability strengthens others|none stand alone

# compounding_chain(commitment|enables|next)
CB1|every change goes through gate|continuous audit possible|every operation produces structured trail
CB2|no out-of-band path|gate is uniform|alternate paths would make disciplines advisory
CB3|schema and API are only way to interact|out-of-band paths cannot exist|the path doesn't exist to bypass
CB4|closed vocabulary forbids breaking changes|schema stable across decades|consumers can trust field names persist
CB5|schema stable|consumers can be simple|don't need defensive code for renames/deletes/type changes
CB6|consumers simple|many consumers can exist|each one is small and knowable
CB7|breadth of consumers exists|comprehensive operational coverage|operational reality is fully tracked
CB8|comprehensive coverage|the OpsDB delivers what fragmented operations cannot|alternative was always fragmentation

# unchanged(id|aspect|rationale)
UC1|fundamental work of operations|services still need to run+monitoring still alerts+incidents still happen+capacity still planning|OpsDB does not eliminate operational work; makes it coordinated
UC2|skill set of operations engineers|still need systems+networking+storage+security+distributed systems failure modes|OpsDB is tool for coordinating not replacement
UC3|organizational dynamics|disagreement about priorities+ownership disputes+communication problems still exist|OpsDB provides shared substrate but humans still have to use it well
UC4|discipline requirement|OpsDB rewards orgs that bring discipline; does not produce discipline|org that cannot maintain SoT+allows fragmentation creep+bypasses gate when convenient will not succeed

# workflows(id|scenario|before|after)
WF1|Investigation During Incident|page→Slack→Grafana→kubectl→wiki→git tour of tools assembling picture mentally|page links to service incident view resolving runbook ref+dashboard URLs+recent change_sets+evidence records+dependent services+upstream on-call
WF2|Deployment|developer PR→CI→Argo CD/kubectl apply→hope it worked→Datadog check maybe|change_set→validation→approval→executor applies OpsDB-side+signals via output var→specialized runner performs world-side action→deploy watcher records rollout→digest verifier writes evidence
WF3|Certificate Renewal|cron job runs cert-manager/ACME hopefully|cert inventory in OpsDB+each cert has expiration_schedule+renewal runner reads+performs renewal+writes evidence each cycle+drift detector confirms+compliance_finding if fails
WF4|Compliance Evidence Collection|auditor arrives→requests→team scrambles for weeks across Jira+Slack+email+screenshots+vault logs→assembles binder|continuous compliance is property of system; verifier runners produce evidence records on every cycle; auditor receives read-only scoped access+queries same data team queries
WF5|Drift Correction|drift accumulates silently for months; nobody knows until next incident|drift detector reads desired+observed each cycle+computes diff+auto-corrects via change_set per policy or files finding for human review
WF6|Onboarding New Automation|team writes script lives somewhere in their repo+runs on team-owned cron+other teams don't know it exists+credentials hardcoded|team writes runner against shared lib suite+registers runner_spec via change_set declaring purpose+schedule+target scope+capabilities+report keys
WF7|Schema Evolution|migration scripts tested in staging then run in production with held breath; sometimes break consumers|schema changes are change_sets against schema repo→reviewed via git workflow→CI generates schema_change_set→same approval pipeline→executor applies DDL atomically
WF8|Vendor Substrate Transitions|replacing cloud is multi-year project+each transition involves rewriting integrations+rebuilding institutional knowledge+accepting outages|write new pullers for new cloud's authorities+deprecate old when migration completes+update authority pointers; existing entity rows reference new provider via authority pointers; non-cloud-specific runners keep working unchanged

# === DIAGNOSTICS ===

# failure_modes(failure_mode|properties_lost|properties_preserved)
FM01|Single process crash|P10 Liveness(briefly)+in-flight P02 Atomicity|P03 Durability(with WAL)+P04 Consistency-data(with rollback)
FM02|Single node power loss|P10+fsync-pending writes if not synced|P03 Durability(committed)+P15 Consistency-replica(with replicas)
FM03|Network partition|P15(CP) OR P11(AP) — choose one|P03+P10 within partition
FM04|Single disk failure|P12 Boundedness(capacity)+data on that disk if no RAID|P03(with replication or RAID)+P11
FM05|Single rack failure|P17 Locality+requests pinned to rack|most properties (with multi-rack replication)
FM06|Single DC failure|P17+regional P11|P03(multi-DC)+global P11
FM07|Region failure|P03(without multi-region)+region's P11|multi-region durability+other regions' P11
FM08|Clock skew|P08 Determinism+P16 Ordering(timestamp-based)|wall-clock-independent properties
FM09|Quorum loss|P15 writes+P10 for writes|read availability if AP
FM10|Cache failure|P17+P11 for cache-bound traffic|SoT properties(P03+P15)
FM11|Authenticator failure|P06 Authenticity+all dependent gating|properties of already-authenticated sessions
FM12|Bulk corruption(silent)|P05 Integrity+P21 Auditability if logs corrupted|almost nothing without integrity checking
FM13|Insider threat|P07+P05+P21|none reliably without external controls
FM14|Resource exhaustion|P10+P12 violated+P11|P03+P04 for completed ops
FM15|Cascading failure|P19+P10 across many systems|often nothing without M62 Bulkhead
FM16|Time skew across replicas|P16 Ordering+LWW correctness|properties not relying on wall clocks
FM17|Split-brain(election failure)|P15+P02|per-partition consistency on each side

# mechanism_confusions(pair|distinguishing_question)
CF01|Cache vs Store|if you lose it do you lose data? Cache=no Store=yes
CF02|Journal vs Log|is replay the purpose? Journal=yes(WAL) Log=no(audit/access)
CF03|Probe vs Heartbeat|who initiates? Probe=watcher Heartbeat=watched
CF04|Reconciler vs Reactor|triggered by current state or events? Reconciler=state Reactor=events
CF05|Lock vs Lease|time-bounded by default? Lock=no Lease=yes
CF06|Authenticator vs Authorizer|who vs what they may do; Authenticator=identity Authorizer=permission
CF07|Validator vs Mutator|modifies the request? Validator=no Mutator=yes
CF08|Filter vs Limiter|selects by content or rate? Filter=content Limiter=rate
CF09|Snapshot vs Backup|Snapshot is mechanism; "backup" is goal achieved with snapshots+transport+retention
CF10|Tombstone vs Delete|Tombstone is record-of-deletion; delete-without-tombstone causes resurrection in distributed systems
CF11|Quorum vs Election|Quorum is counting rule; Election uses Quorum to pick leader
CF12|Sharder vs Replicator|Sharder splits across nodes; Replicator copies same data to multiple nodes
CF13|Hasher vs Sequencer|Hasher content-derived; Sequencer allocation-derived(monotonic over time)
CF14|Index vs Schema|Index accelerates lookup over existing data; Schema describes what data is allowed
CF15|Pool vs Quota|Pool is resources to draw from; Quota is limit on how much one party may draw
CF16|Watch vs Funnel|Watch=subscribe to changes(per-resource); Funnel=aggregate from many sources(per-stream)

# principle_violations(principle|typical_consequence)
VL01|R01 Data primacy|configuration buried in code; can't change behavior without redeploying
VL02|R02 Single source of truth|drift between sources; reconciliation harder
VL03|R03 Convention over lookup|brittle naming; every change requires updating registry
VL04|R04 0/1/∞|system breaks at next growth step ("we built it for two replicas")
VL05|R05 Comprehensive over aggregate|internally inconsistent system; ops engineers can't predict behavior
VL06|R06 One way to do each thing|twice operational load; each variant separately monitored
VL07|R07 Idempotent retry|retries cause duplication+double-charges+double-emails
VL08|R08 Level-triggered over edge-triggered|missed events become missed work; system silently diverges
VL09|R09 Fail closed(security)|false acceptances become breaches
VL10|R10 Fail open(availability)|outage on minor failures; unnecessary downtime
VL11|R11 Bound everything|unbounded queue→OOM; unbounded retries→never give up; cache→fills disk
VL12|R12 Reversible changes|rollback unavailable on incident; long MTTR
VL13|R13 Minimize dependencies|cascading failures; one outage causes many; bootstrap impossible
VL14|R14 Separate planes|control plane outage takes down data plane; no way to manage during incident
VL15|R15 Layer for separation of concerns|tight coupling; replacing one layer requires changing others
VL16|R16 Bucket for locality and accounting|hot tenants starve others; no per-tenant accountability
VL17|R17 Local cache + global truth|every request hits global authority→bottleneck
VL18|R18 Centralize policy decentralize enforcement|policy drift across enforcers OR SPOF on every check
VL19|R19 Push the decision down|every decision serialized through coordinator; latency ceiling
VL20|R20 Push the work down/out|origin servers absorb all traffic; no scaling without rebuilding
VL21|R21 Make state observable|can't diagnose; every incident becomes guessing game
VL22|R22 Removing classes of work|automation only speeds work doesn't eliminate it; team scales with workload

# mechanism_evolution(mechanism|older_standard|modern_standard)
EV01|M53 Election|manual failover+custom heartbeat scripts|Raft(etcd+Consul) widely available
EV02|M04 Replicator|master-slave (term itself now changed)|master-replica or peer-to-peer; CRDTs for AP systems
EV03|M52 Lock(distributed)|custom NFS file locks+ad-hoc|Raft-backed(etcd locks)+lease-based
EV04|M32 Probe|TCP connect or ping|HTTP /healthz+/readyz+/livez
EV05|M13 Schema|free-form text or per-RDBMS DDL|OpenAPI+protobuf+JSON-Schema as portable schemas
EV06|M15 Naming-convention|per-organization arbitrary|cloud resource ARNs+K8s standard labels+RFC-driven IDs(ULID)
EV07|M38 Reconciler|cron+scripts|Operator pattern(K8s)+GitOps(Flux+Argo)
EV08|M42 Authenticator|per-app passwords+LDAP|OIDC+federated SSO+mTLS+workload identity
EV09|M46 Filter(network)|iptables linear scan|nftables sets+eBPF programs
EV10|M59 Compactor|manual VACUUM+cron-driven defrag|background autovacuum+LSM auto-compaction
EV11|M55 Quorum|hand-rolled per system|library/framework primitives(etcd+ZooKeeper recipes)
EV12|Versioning(data)|last-write-wins or none|MVCC standard in OLTP; CRDTs growing
EV13|M37 Heartbeat-detection|fixed timeout|Phi accrual+gossip-amplified
EV14|M56 Sequencer|auto-increment(single point)|Snowflake-style distributed; ULIDs
EV15|M21 Snapshot|stop-the-world dumps|online consistent snapshots(ZFS+EBS+Postgres)

# system_populations(system_category|dominant_families|light_or_absent)
POP01|Configuration mgmt(Salt+Ansible+Puppet)|F8+F2+F12+F7|F5(light)+F11(light)
POP02|Container orchestration(K8s+Nomad)|F8+F10+F9+F7+F11|F12(light)
POP03|Relational DB(Postgres+MySQL)|F4+F11+F5+F9|F1(limited to replication)
POP04|Distributed DB(Cassandra+DynamoDB)|F4+Replication+F11(Quorum)+F5|strong gating absent
POP05|In-memory store(Redis+Memcached)|F4(volatile)+F1+F6|F5(light)+strong durability(optional)
POP06|Object store(S3+GCS)|F4+F5+F9|strong consistency(eventual until 2020)+F11
POP07|Message broker(Kafka+RabbitMQ+NATS)|F1+F4(Journal)+F11|F9(basic)+F2(limited)
POP08|Stream processor(Flink+Spark+Kafka-Streams)|F12+F4+F7|F9+F5
POP09|CDN(Cloudflare+Fastly+Akamai)|F1(Anycast+Fanout)+F4(Cache)+F9|F11+F5
POP10|Load balancer(HAProxy+nginx+Envoy)|F2(Router+Ranker)+F7+F13|F4+F5
POP11|DNS(BIND+Unbound+Route53)|F2+F4+F1+F6|F11+F5(basic)
POP12|Firewall(iptables+nftables+AWS-SG)|F9(Filter+Limiter)+F2|F4+F11
POP13|Source control(Git+Perforce)|F5(entire)+F4+Comparison|F1(push/pull only)+F11(limited)
POP14|Service mesh(Istio+Linkerd)|F1+F9+F7+F13|F4(none of own)
POP15|Observability stack(Prometheus+Grafana+ELK)|F7+F4+F2(PromQL+Lucene)|F9+F11
POP16|File transfer(rsync+sftp+aspera)|F1+Comparison(delta)+F5(limited)|most others absent
POP17|Identity provider(Keycloak+Okta+AD)|F9(Authenticator+Authorizer)+F4+F5|F1(light)
POP18|Backup system(Bacula+Borg+Restic)|F4(Snapshot)+F5+Compactor|F11(light)

# mechanism_implementations(mechanism|examples)
IMP01|M01 Channel|TCP+QUIC+Unix-domain-socket+SSH-transport+ZeroMQ+gRPC-streams+Kafka-connections+MQTT
IMP02|M02 Fanout|Multicast(IGMP)+Anycast(BGP)+Redis-pubsub+Kafka-topics+NATS+AWS-SNS
IMP03|M03 Funnel|Fluentd+Logstash+Vector+syslog-aggregators+OpenTelemetry-collectors+Prometheus-scraping
IMP04|M04 Replicator|Postgres-streaming+MySQL-binlog+MongoDB-oplog+Cassandra-hinted-handoff+Redis-replication+Kafka-MirrorMaker+rsync+etcd-Raft+K8s-informer-caches
IMP05|M05 Relay|HAProxy+Envoy+nginx-proxy+Squid+stunnel+ngrok+AWS-API-Gateway
IMP06|M06 Index|B-tree(RDBMS)+LSM-tree(Cassandra+RocksDB)+bloom+GIN/GiST(Postgres)+inverted(Elasticsearch)+R-tree(PostGIS)+HLL
IMP07|M07 Selector|SQL-WHERE+K8s-label-selectors+Salt-grain-match+Ansible-host-patterns+PromQL+AWS-resource-tag-filters
IMP08|M08 Comparator|etag/If-Match(HTTP)+Postgres-MVCC-visibility+K8s-resourceVersion-check+vector-clocks(Riak)+git-diff
IMP09|M09 Hasher|SHA-2+BLAKE3+xxHash+MurmurHash3+CRC32+consistent-hashing(Cassandra+Memcached)+Rendezvous/HRW
IMP10|M10 Ranker|K8s-scheduler-scoring+Postgres-query-planner+search-engines(BM25)+HAProxy-least-conn
IMP11|M11 Router|iptables+nftables+IP-routing-tables+kube-proxy+Envoy-route_config+AWS-ALB-rules+message-brokers
IMP12|M12 Wrap/unwrap|TLS+IPSEC+SSH+JOSE/JWT+VXLAN+GRE+MPLS+Geneve+WireGuard+JSON+protobuf+Avro+CBOR+base64+gzip+zstd+tar
IMP13|M13 Schema|Postgres-DDL+JSON-Schema+OpenAPI+protobuf-.proto+Avro-schema+SQL-DDL+GraphQL-SDL
IMP14|M14 Namespace|DNS-zones+K8s-namespaces+filesystem-directories+Java-packages+Cassandra-keyspaces+Postgres-schemas
IMP15|M15 Naming-convention|RFC-FQDN+K8s-app.kubernetes.io+AWS-ARN+Cassandra-composite-keys+snowflake-IDs+ULIDs
IMP16|M16 Buffer|Linux-pipe-buffers+kernel-ring-buffer+Kafka-in-memory-queues+circular-buffers+Go-channels
IMP17|M17 Cache|Memcached+Redis+Varnish+CDN-edges+Linux-page-cache+CPU-L1/L2/L3+browser-cache
IMP18|M18 Store|Postgres+MySQL+Cassandra+MongoDB+etcd+ZooKeeper+S3+HDFS+ext4+ZFS
IMP19|M19 Journal|Postgres-WAL+MySQL-binlog+ext4-journal+Cassandra-commitlog+Redis-AOF+Kafka-log-segments+etcd-WAL
IMP20|M20 Log|syslog+journald+app-logs+AWS-CloudTrail+audit-logs+web-server-access-logs
IMP21|M21 Snapshot|ZFS-snapshots+LVM-snapshots+AWS-EBS-snapshots+pg_dump+Redis-RDB+K8s-etcd-backups+VM-snapshots+Btrfs-snapshots
IMP22|M22 Tombstone|Cassandra-tombstones+Riak-tombstones+soft-delete-columns+Kafka-tombstone-messages+S3-delete-markers
IMP23|M23 Version-stamp|Git-SHA+Postgres-LSN+MySQL-GTID+K8s-resourceVersion+S3-ETag+MongoDB-ObjectId+Cassandra-timestamps+vector-clocks
IMP24|M24 History|Git-commits+Mercurial-revsets+Perforce-changelists+Postgres-WAL+S3-object-versions+time-travel-queries(Snowflake+BigQuery)
IMP25|M25 Merge-algorithm|Git-three-way+Riak-siblings+CRDTs+LWW(Cassandra+DynamoDB)+OT(Google-Docs)+automerge
IMP26|M26 Diff|unified-diff+JSON-Patch+JSON-Merge-Patch+K8s-strategic-merge-patch+migration-tools(Flyway+Alembic)
IMP27|M27 Reference|Git-refs+Docker-image-tags+K8s-deployment-template-ref+symlinks+S3-latest-version+CNAME
IMP28|M28 TTL|DNS-TTL+Redis-EXPIRE+Cassandra-TTL-columns+Kafka-log-retention+S3-lifecycle+browser-cookie-max-age+ARP-cache-timeouts
IMP29|M29 Lease|DHCP-leases+K8s-leader-election-leases+ZooKeeper-ephemeral-nodes+Consul-sessions+Raft-leader-leases+file-locks-with-timeouts
IMP30|M30 Reaper|Postgres-autovacuum+Cassandra-compaction+Linux-OOM-killer+K8s-GC-controller+Java-GC+conntrack-timeout-sweep
IMP31|M31 Drainer|K8s-pod-termination-grace-period+HAProxy-connection-draining+AWS-ELB-deregistration-delay+Cassandra-nodetool-decommission
IMP32|M32 Probe|K8s-liveness/readiness-probes+HAProxy-health-checks+AWS-ELB-target-health+gRPC-health-protocol+Nagios+Pingdom
IMP33|M33 Counter|Prometheus-Counter+statsd-counter+eBPF-counters+/proc/net/stat+syscall-counters
IMP34|M34 Gauge|Prometheus-Gauge+/proc/loadavg+JMX-gauges+top+free+df
IMP35|M35 Histogram|Prometheus-Histogram+t-digest+HDRHistogram+OpenTelemetry-histograms
IMP36|M36 Watch|K8s-watch-API+etcd-watch+ZooKeeper-watches+inotify+Consul-blocking-queries+Kafka-consumer-subscribe
IMP37|M37 Heartbeat|Cassandra-gossip+Consul-gossip+Kafka-heartbeats+BGP-keepalive+OSPF-hello+mobile-app-pings
IMP38|M38 Reconciler|K8s-controllers+K8s-operators+Terraform-apply+Salt-state.apply+Puppet-agent+ArgoCD+Flux
IMP39|M39 Reactor|Webhooks+K8s-Reactor+AWS-Lambda-event-triggered+GitHub-Actions+EventBridge-rules
IMP40|M40 Scheduler-control|cron+systemd-timers+K8s-CronJob+Quartz+Airflow-scheduler+Hangfire
IMP41|M41 Workqueue|K8s-client-go-workqueue+Sidekiq+Celery+AWS-SQS+RabbitMQ-work-queues+Resque
IMP42|M42 Authenticator|Kerberos+OAuth-2.0/OIDC+SAML+PKI-client-certs+SSH-key-auth+AWS-IAM+LDAP+Active-Directory
IMP43|M43 Authorizer|K8s-RBAC+AWS-IAM-policies+OPA+Casbin+Postgres-GRANT+Cedar
IMP44|M44 Validator|JSON-Schema-validators+K8s-validating-webhooks+Postgres-CHECK+OpenAPI-validators+OPA-Gatekeeper
IMP45|M45 Mutator|K8s-mutating-webhooks+Postgres-BEFORE-INSERT-triggers+GraphQL-middleware+AWS-Lambda-authorizers
IMP46|M46 Filter|iptables+nftables+AWS-Security-Groups+AWS-NACLs+K8s-NetworkPolicy+Calico+Snort+ModSecurity+Cloudflare-WAF
IMP47|M47 Limiter|nginx-limit_req+Envoy-rate-limit-filter+Redis-cell+AWS-API-Gateway-throttling+Cloudflare-rate-limiting+semaphores
IMP48|M48 Pool|DB-connection-pool+thread-pool+AWS-EC2-ASG+K8s-node-pool+IP-address-pool(DHCP)
IMP49|M49 Quota|K8s-ResourceQuota+AWS-service-quotas+Linux-cgroups+disk-quotas+Cassandra-throughput-throttle
IMP50|M50 Scheduler-allocation|K8s-scheduler+Mesos+YARN+Slurm+AWS-ECS-placement+Borg+Nomad+Linux-CFS
IMP51|M51 Sharder|Cassandra-token-ring+Redis-Cluster-slots+MongoDB-sharded-clusters+Vitess+Citus+Elasticsearch-shards
IMP52|M52 Lock|pthread-mutex+Postgres-advisory-locks+Redis-Redlock+ZooKeeper-locks+etcd-lease-based-locks+flock
IMP53|M53 Election|Raft(etcd+Consul)+Paxos(Spanner)+ZAB(ZooKeeper)+Patroni(Postgres)+Sentinel(Redis)+Bully
IMP54|M54 Barrier|pthread-barrier+ZooKeeper-double-barrier-recipe+Java-CyclicBarrier+MPI_Barrier+K8s-Init-Containers
IMP55|M55 Quorum|Raft-majority+Paxos-quorum+Cassandra-CL=QUORUM+etcd-quorum-reads/writes+MongoDB-w=majority+Galera
IMP56|M56 Sequencer|Postgres-SEQUENCE+Twitter-Snowflake+MongoDB-ObjectId+Kafka-offsets+Lamport+vector-clocks
IMP57|M57 Renderer|Jinja2+Mustache+Handlebars+Go-html/template+ERB+Helm-templates+Terraform-templates+Liquid
IMP58|M58 Transformer|UNIX-pipes+awk+jq+MapReduce+Spark-transformations+Pandas+Kafka-Streams+Flink
IMP59|M59 Compactor|Cassandra-compaction+Kafka-log-compaction+Postgres-VACUUM-FULL+RocksDB-compaction+Btrfs-balance+ZFS-scrub
IMP60|M60 Retrier|Polly+Resilience4j+AWS-SDK-retries+gRPC-retry-policies+Postgres-replication-retry
IMP61|M61 Circuit-breaker|Hystrix+Resilience4j+Envoy-outlier-detection+Polly+Sentinel(Alibaba)
IMP62|M62 Bulkhead|Hystrix-thread-pools+K8s-namespaces-with-quotas+AWS-account-isolation+Cell-based-architectures
IMP63|M63 Hedger|Google-tail-tolerant-hedging+Envoy-hedge_policy+Cassandra-speculative-retry+BigTable-hedged-reads
IMP64|M64 Failover|Patroni+repmgr+MHA+Sentinel+keepalived+AWS-RDS-Multi-AZ+K8s-pod-replacement

# fast_locator(symptom|first_family|second_family)
FL01|Data missing after restart|F4(Journal+Store)|F11(commit protocol)
FL02|Reads return stale data|F4(Cache invalidation)|F1(Replicator lag)
FL03|Service slow under load|F10(Pool+Quota)|F13(Circuit-breaker+Hedger)
FL04|Service unreachable|F1(Channel+Router)|F13(Failover)
FL05|Wrong user can see data|F9(Authorizer)|F3(Wrap-unwrap encryption)
FL06|Operations not idempotent on retry|F2(Comparator)+F5(Version-stamp)|F11(Sequencer)
FL07|Configuration drifts on hosts|F8(Reconciler)|F7(Probe)
FL08|Cluster has no leader|F11(Election+Quorum)|F7(Heartbeat)
FL09|Backup missing recent data|F4(Snapshot+Journal)|F6(TTL)
FL10|Replicas disagree|F5(Merge-algorithm)+F11(Quorum)|F1(Replicator)
FL11|System won't scale past N nodes|F11(centralization)+F10(Sharder)|F4(single-primary bottleneck)
FL12|Memory keeps growing|F6(Reaper+TTL)|F10(Quota)
FL13|Cascading outage took down everything|F13(Bulkhead+Circuit-breaker)|—
FL14|Audit log incomplete|F4(Log retention)+F7(Counter coverage)|F9(logged at right point)
FL15|Deployments break things in production|F5(Reference+History)+F13(Failover)|F8(Reconciler logic)
FL16|Two systems see different facts|R02 SoT violated|F5(Reconciliation)
FL17|Tail latency bad|F13(Hedger)+F10(Scheduler)|F4(Cache hit rate)
FL18|Deletes resurrect|F4(Tombstone discipline)+F6(gc_grace)|F1(Replicator)
FL19|Names collide|F3(Namespace+Naming-convention)|F11(Sequencer for unique IDs)
FL20|Schema migration breaks clients|F3(Schema versioning)+F5(References)|—

# === RELATIONSHIPS ===

# relationships(from|rel|to)
W2|enables|W1
W3|is_strategy_for|W2
W4|target_of|W3
W5|opposes|W6
W10|subset_of|W6
W11|subset_of|W6
W11|operates_on|W10
W10|primary_over|W11
W18|opposes|W17
W16|implements|W17
W15|enables|W16
W17|requires|W19
W20|requires|W19
W20|superset_of|W19
W19|prereq_of|W20
W7|implements|W8
W14|uses|W8
W42|uses|W8
W31|opposes|W32
W31|requires|W36
W25|opposes|W26
W27|instance_of|W28
W28|anti_pattern_of|W21
W22|aggregates_into|W23
W23|enables|W24
WR1|implements|W23
WR2|constrains|W34
WR3|property_of|W11
WR8|derives_from|WD2
WR8|derives_from|W10
W44|orthogonal_to|W45
W45|enables|W46
W47|primary_over|W48
W49|primary_over|W27
W50|caused_by|W52
W51|sometimes_correct_form_of|W50
W53|violates|WR8
W53|violates|WD2
W54|symptom_of|W18
W57|property_of|W3
W36|enables|W3
W39|requires|W40
W41|limits|W39
VP1|grounds|A1
VP1|grounds|A2
VP1|grounds|A3
A1|provides|A2
A2|requires|A1
A3|selects_among|A1
A3|constrains_realization_of|A2
F1|primary_addresses|P17+P19+P16
F3|primary_addresses|P05+P06+P07+P20
F4|primary_addresses|P03+P04+P17
F5|primary_addresses|P14+P21+P16+P18
F6|primary_addresses|P12+P10
F7|primary_addresses|P20
F8|primary_addresses|P09+P10+P19
F9|primary_addresses|P05+P07+P06+P12
F10|primary_addresses|P12+P18+P17
F11|primary_addresses|P02+P13+P16+P15
F13|primary_addresses|P11+P10+P19+P09
M19|natively_provides|P21+P03(partial)
M04|configurably_provides|P15
M17|cannot_provide|P03
M17|provides|P12+P17
M38|natively_provides|P09
M40|spans|F8+F10
M47|spans|F9+F10
M04|spans|F1+F4
P01|provided_by|M08+M56+M18
P03|composed_from|M19+M18+M04
P06|composed_from|M42+M13+M12
P20|composed_from|M33+M34+M35+M36+M02
R02|distinct_from|peer-to-peer-systems
R09|opposes|R10
R09|domain|security+integrity
R10|domain|availability-critical
R18|resolves|centralize-vs-decentralize-tension
R05|preferred_over|aggregate-systems
DC1|resolved_by|qualification
DC2|resolved_by|qualification
DC3|resolved_by|qualification
SP1|named_in|F8-primary
SP2|named_in|F9-primary
SP3|named_in|F1-primary
AC1|prevents|orchestrator-drift
AC2|prevents|gate-bypass
AC3|enables|engine-portability
AC4|enables|uniform-governance
AC9|enables|long-lived-schema
AC10|prevents|split-brain
CR2|target_for|small-orgs
CR8|forbidden|true
CR9|invalid|true
CR10|invalid|true
CR11|invalid|true
CR12|invalid|true
Pop1|access_through|API
Pop2|access_through|API
Pop3|access_through|API
Pop1|writes|change_sets
Pop2|writes|observation+evidence
Pop3|reads|audit+history+evidence+policies
BD5|prevents|orchestrator-drift
BD8|preserves|secret-backend-boundary
BD9|prevents|world-SPOF
BD10|enables|runner-coordination-pattern
BD11|enables|notification-runner-pattern
BD12|enables|change-set-executor-pattern
BD16|prevents|framework-coupling
BD17|prevents|orchestrator-by-another-path
SCP1|implements|SCP2
SCP1|enables|SCP9
SCP3|implements|SCP4
SCP3|implements|SCP5
SCP3|enables|bounded-validation-time
SCP4|prevents|knowability-loss
SCP7|implements|SCP8
SF1|equivalent_via|enum+length-bounds+API-semantic-validation
SF2|enforces|literals-only
SF3|defers_to|policy-data-at-API-semantic-validation
SF7|enforces|tombstone-pattern
SF8|enforces|duplication-pattern
SX_F1|breaks|history-and-audit-log
SX_F2|breaks|every-consumer
ST_ALL|implements|absolute-rules-via-bounded-pattern
RP1|implements|three-phase-shape
RP7|enforced_by|RP8
RP7|enables|RP9
RK1|writes_to|RG1
RK3|writes_to|RG1
RK8|writes_to|RG1
RK4|writes_to|RG2
RK6|writes_to|RG2_or_RG3
RK7|gates|RG1_after_approval
RK10|gates|emergency_or_RG3
RK_ALL|must_satisfy|RD1+RD2+RD3
RK1|uses|LL1+LL15+LL10
RK2|uses|LL1+LL2_or_LL3+LL10
RC1|instance_of|RK7
RC2|instance_of|RK2
RC4|instance_of|RK1
RC5|instance_of|RK3
RC6|instance_of|RK6
RA1|violates|RP7
RA2|violates|RP3
RA3|violates|R06
RA4|violates|LP2
RA5|violates|RP11
RA6|violates|RP14
RA7|violates|RP13
RA8|violates|RP10
RA9|violates|RP12
RA10|misuses|RP1
RA11|violates|RP14
AP1|enables|AP8
AP2|enables|stable-API-across-storage-engines
AP3|delegates|AD1+AD2
AP3|owns|AD3
AP4|enables|passive-substrate
AP4|implies|notification-runner-pattern
AP5|implies|notification-runner-pattern
AP6|implies|change-set-executor-runner
AP8|implements|all-operations
AP11|prevents|DoS-via-regex
AP12|enables|integrity-of-history
AO8|gated_by|RKS1
AO9|writes|change_set+change_set_field_change+change_set_approval_required
AO9|triggers|stakeholder-routing
AO13|requires|emergency-authority
AG_ALL|prereq_of|AG_NEXT
AL_ALL|composes_with|AL_NEXT
AL_ALL|first_denial_halts|true
LL_P1|implements|LL_P2
LL_P3|enforces|boundary-discipline
LL_P4|requires|LL_P5
LL_P5|prevents|inconsistency-across-runner-population
LL_P9|composes|API-gate+library-suite
LL_P10|prevents|library-fragmentation
LL_P12|preserves|secret-backend-boundary
LL1|mandatory_for|every-runner
LL15|mandatory|true
LL16|mandatory|true
LL17|mandatory|true
TS3|input|runner-declarations
TS4|prevents|action-outside-declared-scope
PV_ALL|fail_closed|true
PV_ALL|data_driven|true
FC1|implements|fail-closed-discipline
LV5|parallels|schema-duplication-pattern
LV8|orders|schema-first-then-library-then-runner
OC1|prevents|schema-aggregate-drift
OC2|enables|API-quality-compounding
OC3|enables|cheap-runner-population
OC4|prevents|fragmentation-creep
OC5|prevents|scope-expansion-creep
OD1|implements|R05-comprehensive-thinking
OD2|implements|R06-one-way
OD3|implements|robust-runner-population
OD4|prevents|unbounded-resource-consumption
OD5|enables|rollback-without-side-channel
OD6|enables|operations-as-inspectable
Ro1|continuous|true
Ro1|parallels|library_steward
Ro1|reviews|_schema_change_set
Ro2|continuous|true
Ro2|reviews|library-proposals+contract-additions
IP1|gates|phase-progression
IP5|costs|slightly-more-at-N=2
IP5|prevents|N=∞-retrofitted-onto-N=2-grown-independently
IP6|determines|everything-downstream
IP7|enables|cheap-iteration
IP8|delivers|immediate-validation
IP9|continues|indefinitely
Ph1|prereq_of|Ph2
Ph2|prereq_of|Ph3
Ph3|prereq_of|Ph4
Ph4|prereq_of|Ph5
Ph5|prereq_of|Ph6
Ph6|steady_state|true
DSF_ALL|test|nested-element-with-identity-OR-N=sub-table
DSN_ALL|trades|keystrokes-for-structural-transparency
T_ALL|differs|dev-vs-operational
TS_1|once|cutover-not-gradual
TD3|governance_applies|after-cutover-not-retroactively
WF_ALL|demonstrates|fragmentation-vs-OpsDB-coordinated
CB_ALL|implements|IC10-compounding
UC_ALL|caveats|capabilities-not-magic
IT_ALL|generalizes|CAP-style-impossibility
GAP_ALL|names|industry-vocabulary-divergence
FM_ALL|shows|engineering-tradeoff-space
CF_ALL|prevents|architectural-mistakes
VL_ALL|shows|consequences-of-violation
EV_ALL|spots|industry-conventions-mid-shift
FL_ALL|reverse_indexes|symptom-to-family
IMP_ALL|grounds|abstract-mechanisms-in-real-implementations

# === SECTION INDEX ===

# section_index(source|section|title|ids)
book|1|Foundations|W1,W2,W3,W4,W21,W26
book|2|Real vs Virtual|W5-W12,WA1,WA2,WD1,WD8,WR4,W47,W48,WD10
book|3|Data is King Logic is Shell|W10-W12,W53,W56,WD2,WR8,WR14,WR15
book|4|What is a System|W7,W8,W13,W14,W42,W54
book|5|Systemic Thinking|W7,W8,W13-W18,W42,WD3
book|6|Axiomatic Engineering|W21-W28,W43,WA12,WD5,WR1,WR7,WR13,W22,W23
book|7|Humans|W44,WA12
book|8|Operational Environments|W29,W30,W55
book|9|OpLogic vs AppLogic|W31-W33,W57,WA4,WD4,WR10,WR11
book|10|Scaling and Control|W34,W35,WR2
book|11|Evaluating Changes|W22-W23,W50-W52,WA5,WA11,WD6,WD7,WR1
book|12|Algorithmic Properties|W36,WR3
book|13|Know the Present|W37-W41,WR16
book|14|Engineering Your Path|W19,W20,W44-W46,WR7
OPSDB-9|1|Introduction|VP1-VP4,VP7
OPSDB-9|2|Terminology|VP5,VP6,VP9,VP10,VP11
OPSDB-9|3|Mechanism Axis|F1-F13,M01-M64
OPSDB-9|4|Property Axis|B1-B4,P01-P21,OR1-OR4
OPSDB-9|5|Principle Axis|G1-G6,R01-R22,PC1-PC3
OPSDB-9|6|Triangle|TR1-TR5,family-property-coverage
OPSDB-9|7|Overlaps|DC1-DC3,SP1-SP3,MP1-MP2
OPSDB-9|E|Implementations|IMP01-IMP64
OPSDB-9|F|Gap Analysis|GAP01-GAP15
OPSDB-9|G|System Populations|POP01-POP18
OPSDB-9|H|Failure Modes|FM01-FM17
OPSDB-9|I|Confusions|CF01-CF16
OPSDB-9|J|Violations|VL01-VL22
OPSDB-9|K|Impossibility Triplets|IT1-IT9
OPSDB-9|L|Evolution|EV01-EV15
OPSDB-9|M|Fast-Locator|FL01-FL20
OPSDB-2|2|Terminology|AD1-AD7
OPSDB-2|3|Design Goals|AC3,AC8
OPSDB-2|4|Architectural Commitments|AC1-AC10
OPSDB-2|5|Cardinality Rule|CR1-CR12,N1-N6,NP1-NP9
OPSDB-2|6|Content Scope|CT1-CT12,NH1-NH8
OPSDB-2|7|Three Populations|Pop1-Pop3
OPSDB-2|13|What Does Not Belong|BD1-BD9
OPSDB-2|14|Construction Discipline|OC1-OC5,OD1-OD6
OPSDB-4|1-20|Schema|SC1-SC16,SR1-SR10,SG1-SG9,SP_1-SP_10,TC1-TC17,SE1-SE138,SD1-SD12,VC1-VC4
OPSDB-5|1|Introduction|RP1-RP14
OPSDB-5|3|Lifecycle|LP1-LP7
OPSDB-5|4|Runner Kinds|RK1-RK10
OPSDB-5|7|Three Disciplines|RD1-RD3
OPSDB-5|8|Gating|RG1-RG3,GT1-GT5
OPSDB-5|9|Stack-Walking|RW1-RW5
OPSDB-5|10|GitOps|RC1-RC6,GD1-GD4
OPSDB-5|13|Anti-Patterns|RA1-RA11
OPSDB-6|1|Introduction|AP1-AP13
OPSDB-6|3|API Surface|AO1-AO16,AG1-AG10
OPSDB-6|4|Search|filter+joins+projection+pagination+freshness
OPSDB-6|5|Versioning|change_set_field_change-stamps,CON1-CON4
OPSDB-6|6|Auth|AL1-AL5,AD1-AD4
OPSDB-6|7|Change Management|LC1-LC11,SRT1-SRT6,VP_1-VP_6,AA1-AA4,EM1-EM7,BU1-BU6
OPSDB-6|8|Runner Report Keys|RKS1-RKS3,RKF1-RKF5,RKV1-RKV5
OPSDB-6|9|Audit|AU1-AU8,AUF1-AUF8,TE1-TE5
OPSDB-6|10|Boundaries|BD10-BD15
OPSDB-7|1|Introduction|SCP1-SCP11
OPSDB-7|3|Repository Layout|directory.yaml+per-domain-dirs
OPSDB-7|6|Vocabulary|SV_T1-SV_T10,SV_M1-SV_M3,SV_C1-SV_C6
OPSDB-7|7|Forbidden|SF1-SF8
OPSDB-7|8|Cross-Field|CFS1-CFS4
OPSDB-7|9|JSON Payload|JV1-JV4
OPSDB-7|10|Bootstrap|MB1-MB7
OPSDB-7|12|Evolution|SX_A1-SX_A7,SX_F1-SX_F8,ST_1-ST_6
OPSDB-1|2|Starting Point|fragmentation-pattern
OPSDB-1|3|What OpsDB Is|AD1-AD7
OPSDB-1|4|What You Get|IC1-IC10,CB1-CB8
OPSDB-1|5|Workflows|WF1-WF8,UC1-UC4
OPSDB-1|6|Commitments|AC1-AC10,OC1-OC5,OD1-OD6
OPSDB-8|1|Introduction|LL_P1-LL_P14
OPSDB-8|3|What Library Is|LF1-LF7
OPSDB-8|4|API Client|LL1,LA1-LA16
OPSDB-8|5|World-Side|LL2-LL9
OPSDB-8|6|Coordination|LL10-LL14,COP1-COP5
OPSDB-8|7|Observation|LL15-LL17,OL1-OL3
OPSDB-8|8|Notification|LL18
OPSDB-8|9|Templating|LL19-LL21,LT1-LT6
OPSDB-8|10|Git|LL22
OPSDB-8|11|Versioning|LV1-LV8
OPSDB-8|13|Two-Sided Enforcement|TS1-TS5,PV1-PV7,FC1-FC4
OPSDB-8|14|Refusals|BD16-BD22
OPSDB-3|1|Introduction|IP1-IP9
OPSDB-3|3-8|Phases|Ph1-Ph6,NB1-NB5,DSF1-DSF6,DSN1-DSN6
OPSDB-3|9|Roles|Ro1-Ro5
OPSDB-3|10|Transition|T1-T6,TS_1-TS_4,TD1-TD5

# === DECODE LEGEND ===

# decode_legend
mechanism_count: 62 (M01-M64 with internal renumbering)
property_count: 21
principle_count: 22
mechanism_families: 13
property_bands: 4
principle_groups: 6
schema_entity_count: 138
schema_vocabulary_primitives: 18 (9 types + 3 modifiers + 6+ constraints)
runner_kinds_count: 10
api_operations_count: 16
api_gate_steps: 10
api_auth_layers: 5
library_count: 22
library_families: 7
mandatory_libraries: 4 (LL1+LL15+LL16+LL17)
implementation_phases: 6
roles_count: 5
field_types: INT|VARCHAR|TEXT|JSON|BOOL|DATETIME|FLOAT|BIGINT|FK|FK-self
nullable: y|n
versioned: yes|no|append-only|self|computed-by-tooling
sot_values: opsdb|authority|self|append-only|external
+V suffix: entity has versioning sibling table named *_version
+reserved: id|created_time|updated_time|is_active fields implicit on every entity
discriminator_pattern: *_type column + *_data_json column; API validates JSON against schema registered for type value
bridge_notation: SE_X↔SE_Y means many-to-many bridge; one_to_many uses FK directly
gate_step_order: AG1→AG2→AG3→AG4→AG5→AG6→AG7→AG8→AG9→AG10
auth_layer_composition: AL1 AND AL2 AND AL3 AND AL4 AND AL5; first denial halts
phase_progression: gate not calendar; phase complete when criterion met
gating_modes: direct-write|auto-approved-change-set|approval-required-change-set
runner_phase_shape: get|act|set
runner_size_target: 200-500 lines runner-specific (150 specific + 50 library glue)
trigger_types: scheduled|event|long-running|invoked-by-other-data|new-host|approved-change-set
operation_classes: read|write-direct|write-cs|cm-action|stream
predicate_restrictions: no regex; declarative bounds only; bounded composition depth
report_key_target_tables: observation_cache_metric|observation_cache_state|observation_cache_config|runner_job_output_var|evidence_record
fail_closed_principle: if cannot determine authorization → refuse not allow
template_allowed: substitution|inclusion|bounded-iteration
template_forbidden: expressions|conditionals-over-expressions|function-calls|embedded-code
secret_discipline: in-memory-only-during-call; never-logged|written-to-OpsDB|persisted-in-runner-state
extraction_threshold: 3-runners=candidate; 10=confirmed
versioning_classifications: change-managed|observation-only|append-only|computed-by-tooling
forbidden_patterns_in_schema: regex|embedded-logic|conditional-constraints|inheritance|templating|imports-within-files|deletions|renames|type-changes|narrowing
allowed_evolutions: add-field|add-enum-value|widen-numeric|widen-length|add-entity|add-index|add-approval-rule
type_change_pattern_steps: 6 (add new field|begin double-write|migrate readers|mark deprecated|continue double-write|never remove)
cardinality_options: 1-DOS-1-OpsDB|N-DOS-1-OpsDB|N-DOS-N-OpsDB
cardinality_invalid_reasons: technical-fragility|convenience|premature-optimization|performance
n_pipeline_shared: schema-repo|library-suite|API-code|change-mgmt-discipline
n_pipeline_diverged: data|users|audit-log|runners
n_bootstrap_minimum: 2
phase_shape: decision|deliverable|deferred|validation_criterion
phase_6_test: operational-use-not-technical-completeness
hand_loading_questions: 4
dsnc_flatten_when: per-row-metadata-of-parent
dsnc_break_out_when: independent-lifecycle-OR-identity-OR-N-of-them
list_of_n_test: most-common-phase-3-mistake
schema_quality_claim: getting-schema-right-most-important-because-cost-paid-by-every-consumer-for-OpsDB-lifetime
library_minimum_set: opsdb.api+opsdb.observation.logging
existing_code_categories: world-side-I/O→library|decision-making→runner|duplicating-OpsDB→retire
cm_split: intent→gated|observation→ungated
cutover: planned-scheduled-executed-deliberately-not-gradual
historical_data: preserved-not-retroactively-governed
two_sided_surfaces: API-gate (writes)+library-suite (world-side actions)
policy_validation_pattern: extract-target → look-up-declarations-cache → check-coverage → proceed-or-reject-fail-closed → log+metric
spanning_mechanisms: M40 Scheduler(F8+F10)|M47 Limiter(F9+F10)|M04 Replicator(F1+F4)
double_citizens: Durability|Ordering|Consistency
property_orthogonality_pairs: Durability/Persistence/Availability|Consistency-data/Consistency-replica|Ordering/Isolation|Idempotency/Determinism
principle_conflicts: Fail-closed-vs-Fail-open|Centralize-vs-Decentralize|Comprehensive-vs-Aggregate
triangle: mechanism→provides→property|principle→selects→mechanism|principle→constrains-realization→property
qualification_discipline: always qualify ambiguous words (durability mechanism vs property vs principle)
sot_for_schema: schema-repo (OpsDB schema metadata is runtime cache)
sot_for_secrets: secret-backend (vault+equivalents); library never persists
sot_for_code: repositories (git+container-registries); OpsDB never holds
sot_for_runner_authority: OpsDB declaration rows; libraries+API both validate against
adoption_principle: comprehensive thinking aggregate building
discipline_principle: refuse the wrong things; reward orgs that bring discipline
economics_principle: trade-off depends on whether org has lived with fragmentation long enough to see costs clearly
core_thesis: data is king logic is shell at every layer
prefix_legend: W=worldview|M=mechanism|F=family|P=property|B=band|R=principle|G=group|OR=orthogonality|IT=impossibility|GAP=gap|CF=confusion|AC=architectural-commitment|OC=organizational-commitment|OD=operational-discipline|CR=cardinality|BD=boundary|
Pop=population|CT=content|SE=schema-entity|SD=discriminator|SR=reserved-field|SG=governance-field|SC=schema-convention|SP_=schema-pattern|TC=top-level-category|VC=versioning-classification|SCP=schema-construction-principle|SV=schema-vocabulary|SF=schema-forbidden|SX=schema-evolution|ST_=type-change-step|JV=json-vocabulary|MB=meta-bootstrap|RP=runner-pattern|LP=lifecycle-phase|RK=runner-kind|RG=gating-mode|RD=runner-discipline|RW=stack-walk|RC=gitops-cast|GD=gitops-discipline|RA=runner-anti-pattern|AP=api-principle|AO=api-operation|AG=gate-step|AL=auth-layer|AD=auth-delegation|LC=cs-lifecycle|SRT=stakeholder-routing|VP_=validation-pipeline|AA=auto-approval|EM=emergency|BU=bulk|CON=concurrency|RKS/RKF/RKV=report-keys|AU/AUF/TE=audit|LL=library|LF=lib-family|LL_P=lib-principle|LA=api-client-op|COP=coordination|OL=observation-lib|LT=templating|TS=two-sided|PV=policy-validation|FC=fail-closed|LV=lib-versioning|Ph=phase|Ro=role|IP=impl-principle|NB=n-bootstrap|DSF=dsnc-flatten|DSN=dsnc-naming|T/TS_/TD=transition|IC=capability|CB=compounding|UC=unchanged|WF=workflow|FM=failure-mode|VL=violation|EV=evolution|POP=system-population|IMP=implementation|FL=fast-locator
rel_types: enables|requires|implements|prevents|enforces|delegates|composes|consults|computed_per|writes|reads|drains|maintained_via|managed_via|registered_via|produced_by|access_through|trades|cost_of|caveat_to|root_principle|invisible_cost|prereq_of|forces|continues|frames|demonstrates|composed_of|provides|configurably_provides|natively_provides|cannot_provide|spans|composed_from|opposes|preferred_over|resolution_pattern|domain|resolved_by|named_in|applies_across|silent_on|requires_for_atomicity|reverse_indexes|generalizes|spots|prevents|situates|shows|names|gates|prereq_of|completes|delivers|validates|costs|determines|simplest|partition_via|justified_by|invalid|forces|catches|matures|deployed_to|per_substrate|coordination_via|bias|patterns_transfer|surfaces|cheaper_at|sufficient_for|deferred_to|early_form_of|distinguishes|when|failure_mode|test|trades|justifies|mandatory|wraps|waits_for|retires|gated|policy_data|change_managed_themselves|rare_use|labor_intensive|change_managed|shift|follows|criterion|continuous|differs|once|deliberate|preserved|governance_applies|establishes|runners_replace|gate|steady_state|grounds|distinct_from|resolves|implemented_by|provides|requires|selects_among|constrains_realization_of|primary_addresses|configurably_provides|cannot_provide|spans|opposes|preferred_over|domain|resolved_by|named_in|applies_across|silent_on|fail_closed|data_driven|level_triggered_on_reconnect|mandatory_for|gated_by|sufficient_for|investment_proportional_to|continues|new_in|fail_fast_at|each_library_built_once|paid-back-many-times|bounded_staleness|reviews|parallels|misuses|orders|writes_to|attributes|chunked_validation|chunked_apply|emergency_path_via|atomic|target_for|forbidden|rejection_for|redirects_to|investment_target|exception_to|self_chains_to|terminates_at|hosted_on|bridges_to|composed_of|references|topology_via|values_in|contents_in|points_to|owned_by|scoped_to|combines|resolved_at|written_by|written_only_by|append_only|target_via|chains_to|produces|registers|references_artifact|writes|writes_to_targets|verified_by|emergency_path_via|bulk_via|proposed_by|atomic|located_in|hierarchical|filled_by|nested_in|scoped_via|members_via|targets_via|stepped_via|attaches|enriched_with|attached_to_entities_via|targeted_via|recursive_use_of|forbids|signal_to|hot_path|kept_out_of|coupling|bootstrap_exception|bounded|hardcoded_floor|two_paths|safe_because|allowed_direction|breaks|step_one_of|implements_via|automated|stricter_approval|specialized_executor_role|invariant|converges_to|severity|never|works_because|engine_independent|loader_generates|graceful_degradation|defense_in_depth|preserves|separates
read_order: worldview→vocabulary→architecture→schema→active-layer→API→libraries→adoption→diagnostics→relationships→sections→legend
