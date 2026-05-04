# INFRASTRUCTURE TAXONOMY — LLM-COMPACT FORM
# Format: pipe-delimited tables, ID refs.
# Read order: principles → axes → families → mechanisms → bands → properties → groups → principle-rules → orthogonality → conflicts → triangle → coverage → double-citizens → spanning → excluded → meta-patterns → limits → implementations → gap-analysis → populations → failure-modes → confusions → violations → impossibility → evolution → fast-locator → relationships → sections

# principles(id|principle|rationale)
T1|Three-axis structure|mechanism+property+principle are distinct kinds of thing; same word commonly names all three; conflation prevents precise comparison and inspectable decisions
T2|Mechanism is unit of work-doing|takes inputs+produces outputs+performs side effects; identified by interface not implementation
T3|Property is a contract|claim that holds over operations performed by mechanisms; across operations+failures+time; multiple mechanisms can provide same property
T4|Principle is a rule|governs choice and assembly; does not perform work or make claims about specific guarantees; constrains which mechanism+how to configure+how to combine
T5|Always qualify ambiguous words|"durability mechanism" vs "durability property" vs "durability-related principle"; central separation
T6|Real vs Virtual|Real=physical; Virtual=non-physical; mechanisms in this paper are virtual unless noted
T7|Wrap/unwrap is general operation|encoding/decoding is one case; covers TLS+IPSEC+VPN+base64+JSON+protobuf+tar+HTTP-body
T8|Mechanisms provide properties; properties require mechanisms; principles select among mechanisms and constrain configurations|the cross-axis triangle is the load-bearing claim
T9|Some mechanisms genuinely span families|Scheduler in Control-loop AND Allocation; Limiter in Gating AND Allocation; Replicator in Information-movement AND Storage; same algorithmic shape serving multiple purposes
T10|Some words name both mechanism and property|durability+ordering+consistency; resolved by qualification
T11|Bucketing and layering are meta-patterns|recur across all families; not separate families; how mechanisms are deployed not what mechanisms are
T12|Taxonomy is descriptive not prescriptive|names the parts; does not prescribe construction+recommend implementations+evaluate systems
T13|Three-axis structure is load-bearing|contents of each axis revisable; structural claim is the separation

# axes(id|axis|role|populated_with)
A1|mechanisms|building blocks performing work|62 mechanisms in 13 families
A2|properties|contracts claimed about mechanisms|21 properties in 4 bands
A3|principles|rules governing assembly|22 principles in 6 groups

# mechanism_families(id|family|role|section)
F1|Information movement|cause bytes/messages to travel|3.1
F2|Selection|choose among candidates|3.2
F3|Representation|determine how things are expressed|3.3
F4|Storage|hold data over time|3.4
F5|Versioning|preserve and manage state lineage|3.5
F6|Lifecycle|bound a thing's extent in time|3.6
F7|Sensing|produce data about state|3.7
F8|Control loop|observe and act|3.8
F9|Gating|decide what is permitted|3.9
F10|Allocation|decide how much of what|3.10
F11|Coordination|synchronize multiple parties|3.11
F12|Transformation|produce new data from input data|3.12
F13|Resilience|handle failure|3.13

# mechanisms(id|name|family|def|sub_types|composes_with|boundary)
M01|Channel|F1|path along which bytes travel between two endpoints|persistence(long-lived/ephemeral)|reliability(lossless/best-effort)|ordering(preserves/reorders)|direction(uni/bi/half-duplex)|framing(stream/discrete)|encoders+authenticators+limiters+filters|transports not decides; routing is Router
M02|Fanout|F1|one source emits to many destinations|broadcast|multicast|anycast|selective|channels+selectors+sequencers|duplicates emission; aggregation is Funnel
M03|Funnel|F1|many sources emit to one collector|mixing(interleave/merge-by-key)|buffering(immediate/accumulate)|deduplication(collapse/preserve)|channels+comparators+buffers|collects not selects; selection is Selector
M04|Replicator|F1|copies state from one holder to another continuously or on demand|direction(pull/push/peer)|timing(sync/async/periodic)|scope(full/incremental/on-demand)|fidelity(byte/semantic/eventual)|stores+journals+version-stamps+sequencers|maintains copies; arbitration is Election/Quorum; durability beyond underlying Stores not provided
M05|Relay|F1|receives on one channel emits on another with possible transformation|proxy|tunnel|gateway|bridge|channels+wrap-unwrap+filters+mutators|forwards; target decision is Router
M06|Index|F2|data structure mapping key to location accelerating lookup|equality(hash)|range(B-tree)|prefix(trie)|set(bloom-exact)|geometric(R-tree)|full-text(inverted)|probabilistic(HLL+countmin)|stores+hashers+comparators|accelerates lookup; does not store primary data; does not decide which keys to look up
M07|Selector|F2|given population returns subset matching predicate|label-match|expression|regex|set-membership|compound|indexes+comparators+stores|returns whole subset; picking one is Ranker/Router
M08|Comparator|F2|given two things decides equal/ordered/different|equality|ordering|structural|fuzzy|versioned|indexes+selectors+mergers|answers about two; selecting from many is Selector
M09|Hasher|F2|deterministic function from input to bounded output|cryptographic|non-cryptographic|consistent|locality-sensitive|content-addressed|indexes+sharders+comparators+bloom|produces summary; does not decide what to do with result
M10|Ranker|F2|given candidates orders them by score|single-criterion|multi-criterion|lexicographic|learned|selectors+sensing-mechanisms|produces order; picking top-N is Router
M11|Router|F2|given input picks an output path|table-driven|hash-based|load-aware|policy-based|content-based|selectors+rankers|picks one path per input; multiple is Fanout
M12|Wrap/unwrap|F3|encapsulates payload in layer adding context+structure+framing+encryption+signing+routing metadata|representational(JSON+protobuf+base64)|secure(TLS+IPSEC)|routing(VPN+GRE+VXLAN+MPLS)|archival(tar+zip)|framing(HTTP-chunked)|compressing(gzip+zstd)|channels+schemas+authenticators|converts forms of same logical content; does not change meaning
M13|Schema|F3|description of permissible structure constraining wrapped values|strict|permissive|versioned|structural|semantic|validators+encoders+versioning|describes; enforcement is Validator
M14|Namespace|F3|scope within which names are unique and resolvable|structure(flat/hierarchical/federated)|resolution(table/function/distributed)|scope(local/org/global)|naming-conventions+indexes|defines uniqueness; does not produce names
M15|Naming convention|F3|function constructing identifiers from component data deterministically|positional|tagged|hierarchical|encoded|namespaces+hashers+schemas|produces names; resolution is Namespace
M16|Buffer|F4|in-memory holder of bounded size|FIFO-queue|LIFO-stack|ring-buffer|priority-queue|channels+workqueues+limiters|volatile; restart-survival is Store/Journal/Snapshot
M17|Cache|F4|fast capacity-bounded copy of data whose source of truth is elsewhere|placement(in-process/sidecar/remote/tiered)|admission(every/threshold)|eviction(LRU/LFU/FIFO/TTL/random/weighted)|invalidation(TTL/explicit/versioned/write-through/event)|consistency(eventual/sync)|stores+TTL+comparators+hashers|rebuildable from source; if losing it loses data it is Store
M18|Store|F4|durable holder source of truth|structure(KV/relational/document/columnar/graph/blob)|durability(sync-fsync/async/replicated)|access(random/sequential/append-only)|indexes+journals+snapshots+replicators|authoritative location; not a Cache even if implemented similarly
M19|Journal|F4|append-only sequential record of events/changes suitable for replay|operation-log|state-delta|redo|undo|mixed|stores+replicators+snapshots+sequencers|intended for replay; without replay-intent it is Log
M20|Log|F4|append-only record of events without replay-for-recovery as purpose|structured|unstructured|audit|access|diagnostic|funnels+filters+buffers|records for inspection; replay is Journal
M21|Snapshot|F4|point-in-time copy of state|full|incremental|logical|physical|consistent|fuzzy|stores+journals+replicators|frozen copy; not live state
M22|Tombstone|F4|marker that something was deleted distinct from absence|scope(per-row/column/range)|lifetime(forever/GC/acked-by-replicas)|stores+replicators+reapers|exists because absence is ambiguous in distributed; unnecessary in single-node no-replication
M23|Version stamp|F5|monotonic identifier attached to a state|scalar(LSN)|logical-clock(Lamport)|vector-clock|wall-clock|content-hash|opaque(etag)|hybrid|histories+comparators+sequencers|identifies state; does not preserve states (that is History)
M24|History|F5|ordered sequence of versions with relationships preserved|linear|branching|DAG|forgetful|complete|version-stamps+stores+references|preserves lineage; identifying current is Reference
M25|Merge algorithm|F5|given two divergent histories from common ancestor produces unified history|last-write-wins|three-way|CRDT|operational-transformation|manual|histories+comparators+diffs|reconciles divergence; detection is Comparator
M26|Diff|F5|structural description of change between two versions|textual|structural|operation-based|semantic|histories+replicators+merge-algorithms|describes change; applying is separate
M27|Reference|F5|named pointer to a version|named|symbolic|anchored|mutable|immutable|histories+naming-conventions|points; not the version itself
M28|TTL|F6|time after which a thing is considered expired|absolute|relative|idle|conditional|reapers+caches+stores|marks expiration; does not remove (Reaper does)
M29|Lease|F6|time-bounded grant of authority over a resource|renewable|non-renewable|exclusive|shared|revocable|non-revocable|locks+elections+reapers|conditional expiring authority; permanent grants not Leases
M30|Reaper|F6|process that removes expired or abandoned things|lazy|active|event-driven|batch|TTLs+stores+caches+tombstones|removes; does not decide what is expired
M31|Drainer|F6|gracefully removes things from active service before destroying|connection-level|request-level|timeout-bounded|state-aware|health-probes+reapers+failover|transitions out of service; final removal separate
M32|Probe|F7|synthetic test of liveness/health/correctness|liveness|readiness|startup|deep|dependency|by-mechanism(HTTP/TCP/exec/gRPC)|channels+workqueues+counters+gauges|asks; acting on answer is consumer's job
M33|Counter|F7|monotonic numeric tally of events|simple|labeled|resettable|non-resettable|histograms+gauges+limiters|counts; rates derived elsewhere
M34|Gauge|F7|current numeric value of a quantity|instantaneous|windowed|bounded|derived|histograms+rankers+limiters|reports current; history separate
M35|Histogram|F7|bucketed distribution of values over time|bucket(linear/exponential/custom)|decay(cumulative/sliding/EWMA)|percentile(exact/t-digest/HDR)|counters+gauges|describes distribution; does not retain individual samples generally
M36|Watch|F7|subscription to changes push-stream of events|edge-triggered|level-triggered|filtered|resumable|channels+reactors+reconcilers|reports changes; reaction is subscriber's
M37|Heartbeat|F7|periodic still-alive emission distinct from Probe|direction(push/pull-respond)|payload(presence/presence+state)|detection(timeout/Phi-accrual/gossip)|failure-detectors+channels+counters+gauges|emitted by watched (Probe initiated by watcher)
M38|Reconciler|F8|observes desired vs actual takes action to close gap level-triggered repeats forever retries|trigger(event/periodic/both)|scope(per-object/namespace/cluster)|action(CRUD/declarative/custom)|watches+workqueues+stores+sensing|converges; does not guarantee time bound (that is property claim)
M39|Reactor|F8|receives events runs handlers edge-triggered fires once per event|delivery(at-most-once/at-least-once/exactly-once-dedup)|handler(callback/child-process/dispatch)|watches+channels+filters|reacts; missed events = missed reactions; convergence requires Reconciler
M40|Scheduler (control loop)|F8|assigns work to time slots or resources by policy|cron-like|rate-based|priority-queue|deadline-driven|workqueues+reactors+limiters|decides when; what to do is the work; same name spans F8+F10
M41|Workqueue|F8|buffered deduplicated retry-aware task list feeding worker pool|deduplication(key/none)|retry(immediate/backoff/dead-letter)|ordering(FIFO/priority/none)|persistence(memory/durable)|buffers+reconcilers+retriers|holds pending work; doing work is worker's
M42|Authenticator|F9|verifies identity claim against credentials|factor(known/held/inherent)|mechanism(password/cert/token/signed/biometric)|scope(single/federated)|authorizers+channels+wrap-unwrap|establishes who; permission is Authorizer
M43|Authorizer|F9|checks permission for (subject+action+object)|RBAC|ABAC|policy-based|capability-based|mandatory|discretionary|authenticators+filters+validators|answers yes/no; enforcement is consumer's
M44|Validator|F9|checks request meets schema or policy rules before acceptance|schema|semantic|policy|invariant|schemas+mutators+filters|accepts/rejects; does not modify (that is Mutator)
M45|Mutator|F9|modifies request in flight before acceptance|defaulting|injection|rewriting|enrichment|validators+schemas+wrap-unwrap|modifies; acceptance is Validator's decision
M46|Filter|F9|accepts/drops/modifies based on rules|layer(L2/L3/L4/L7)|state(stateless/stateful)|rule(linear/set/tuple-space/compiled)|action(accept/drop/reject/log/redirect/mark/rate-limit)|channels+counters+authorizers|operates per-message; conversation state requires stateful Filter
M47|Limiter|F9|bounds rate or concurrency|algorithm(token-bucket/leaky/window/semaphore)|scope(per-source/target/global/tuple)|action(drop/queue/reject/throttle)|counters+authorizers+buffers|constrains volume; not by content (that is Filter/Authorizer); spans F9+F10
M48|Pool|F10|collection of equivalent resources for checkout/return|fixed-size|elastic|per-tenant|shared|prioritized|quotas+limiters+drainers|provides resources; does not perform work
M49|Quota|F10|maximum amount of resource a party may consume|hard|soft|burstable|fair-share|counters+limiters+authorizers|states limit; enforcement is Limiter
M50|Scheduler (allocation)|F10|assigns work to resources by placement policy|selection(filter+score+bind)|constraints(affinity/anti-affinity/spread/gravity)|preemption|pools+selectors+rankers+sensing|picks where; when is control-loop Scheduler
M51|Sharder|F10|partitions workload across resources|hash-based|range-based|directory-based|consistent-hash|hashers+pools+routers+replicators|decides which shard; replication within shard separate
M52|Lock|F11|exclusive access primitive|scope(in-process/cross-process/distributed)|fairness(FIFO/none)|mode(exclusive/shared/upgradable)|reentrancy|leases+quorums+elections|serializes access; does not ensure correctness under lock
M53|Election|F11|protocol that selects one among many|algorithm(Raft/Paxos/ZAB/highest-ID/lease)|scope(single-leader/per-shard/per-key)|failover(manual/auto/semi)|heartbeats+leases+quorums|picks leader; what leader does separate
M54|Barrier|F11|synchronization point where participants wait until all arrived|count-based|named|phased|workqueues+sensing|meeting point; does not specify before/after
M55|Quorum|F11|rule requiring N-of-M parties to agree|majority|plurality|weighted|read-vs-write|replicators+elections+stores|counting rule; thing being agreed about separate
M56|Sequencer|F11|assigns monotonic positions or timestamps|single-source|distributed(snowflake)|logical(Lamport)|vector|wall-clock|hybrid|version-stamps+journals+replicators|assigns order; enforcing in execution is consumers'
M57|Renderer|F12|produces output by combining template with data|template-language(Jinja/Mustache/Go/custom)|scope(per-field/whole-document)|chaining(single/pipeline)|stores+schemas+wrap-unwrap|produces representation; does not interpret/execute result
M58|Transformer|F12|pure function from input to output|map|filter|reduce|fold|flat-map|codec|channels+workqueues|pure; side effects elsewhere
M59|Compactor|F12|merges multiple inputs into smaller equivalent output|log-compaction|SSTable|defragmentation|incremental|stop-the-world|stores+journals+reapers|reduces redundancy without semantic change
M60|Retrier|F13|re-runs failed operation possibly with backoff and jitter|immediate|exponential|jittered|bounded|deadline-bounded|idempotency-aware|workqueues+circuit-breakers+limiters|re-attempts; safety depends on operation's idempotency property upstream
M61|Circuit breaker|F13|opens to stop calling failing dependency half-opens to test recovery|detection(error-rate/latency/both)|recovery-probe(single/gradual)|scope(per-target/call-site/global)|counters+retriers+hedgers|stops calls; recovery is dependency's responsibility
M62|Bulkhead|F13|isolates failure domains so one failing component cannot drag others down|thread-pool|process|machine|cell|pools+quotas+limiters|separates; does not improve any single component
M63|Hedger|F13|issues redundant requests to reduce tail latency|immediate|delayed|bounded|canceling|channels+comparators+limiters|trades load for latency; assumes idempotency
M64|Failover mechanism|F13|switches from primary to standby on failure detection|active-passive|active-active|automatic|manual|planned|unplanned|elections+drainers+heartbeats+leases|transfers role; actual work separate

# property_bands(id|band|role)
B1|Data integrity|claims about correctness+survival+protection of data
B2|Behavioral|claims about how operations behave
B3|Distribution|claims that arise specifically from multi-party systems
B4|Operational|claims about visibility+reconstruction

# properties(id|name|band|claim|conditions|partial_provision|does_not_claim)
P01|Idempotency|B1|applying same operation with same inputs more than once yields same end state as applying once|same op+same inputs+no concurrent state changes interleaved; some require uniqueness keys/version checks vs retries|idempotent on success but not failure (partial mid-update)|idempotent against itself but not other ops touching same state|that operation has no side effects; only that repeated application converges to same end state
P02|Atomicity|B1|defined unit of work either fully completes or has no externally visible effect|unit must be specified (op/transaction/batch); visibility boundary specified|atomic locally not across replicas|atomic per-row not per-batch|atomic on success not partial-visible on failure|that other parties are blocked during the op (that is Isolation)
P03|Durability|B1|data acknowledged as committed survives the failure modes specified|must specify which failures (process/power/disk/DC/region); stronger costs latency|durable to disk not replicated|durable to one replica not quorum|durable in primary region not after region failure|that data is correct only that it survives
P04|Consistency-data|B1|declared constraints and invariants among data items hold at boundaries specified|constraints declared (FK+uniqueness+CHECK+app invariants); boundaries specified (transaction/eventual)|FKs enforced not app invariants|deferred until commit checked there|relaxed under specific ops|anything about replica freshness or ordering
P05|Integrity|B1|data has not been altered without detection between defined points|requires checksums+signatures+attested storage; points specified|integrity in transit not at rest|integrity at rest not against malicious storage operators|within system not across|confidentiality or authenticity
P06|Authenticity|B1|source of data or request is verifiable|requires trust root and signing/proof; verifier must trust root|authenticity of immediate sender (TLS) not original author (end-to-end signing)|of data not of when authored|that authenticated source acts honestly only that source is who they claim
P07|Confidentiality|B1|data is unreadable to unauthorized parties|specify which parties authorized; specify threat model|in transit not at rest|from network observers not from storage operators|external attackers not insiders|integrity or authenticity
P08|Determinism|B2|same inputs produce same outputs and same side effects|specify what counts as input; time+randomness+concurrency+external state are potential sources of nondeterminism|deterministic in pure logic not in I/O ordering|per-thread not across threads|given identical clocks not with skew|correctness only repeatability
P09|Convergence|B2|repeated application drives state toward fixed point|specify fixed point and conditions (no input changes/no failures)|converges in steady state not while inputs change|to set of valid states not unique|given enough retries with no time bound|time bound on convergence
P10|Liveness|B2|system continues to make progress under specified conditions|specify "progress" (op completes/queue drains/throughput threshold) and "conditions"|liveness for reads not writes|for some clients not others under load|latency bounds on individual operations
P11|Availability|B2|system responds within specified timeframe under specified conditions|response timeframe+percentage+conditions of normal operation must be specified|reads not writes|in region not globally|cached not fresh|that responses are correct or recent only that responses come
P12|Boundedness|B2|resource consumption stays within specified limit|resource named; limit specified|in steady state not failures|per-tenant not aggregate|that limit is sufficient for any particular workload
P13|Isolation|B2|concurrent operations do not visibly interfere|specify level (read-uncommitted/read-committed/repeatable-read/snapshot/serializable)|within transaction not across|reads not writes|allows specific anomalies at lower levels|ordering only non-interference
P14|Reversibility|B2|completed operation can be undone fully or partially|time window; side effects (external API calls cannot be unmade); auto vs operator-driven|in database not side effects|within window not after|by operator not user|byte-identical state only that visible effect is undone
P15|Consistency-replica|B3|read after write returns written value or value satisfying specified relationship|specify level (linearizable/sequential/causal/eventual/monotonic-read/RYW/bounded-staleness); levels not all comparable|linearizable in DC eventual across|RYW per session not across|bounded staleness with worst-case longer|data integrity (declared constraints holding); that is consistency-data
P16|Ordering|B3|operations apply or appear in specified order|specify order (program-per-client/total/causal/partial); may hold for some observers not others|total within partition not across|FIFO per producer interleaved across|causal not total|any specific operation completes by any specific time
P17|Locality|B3|related data sits close together in storage or compute terms|closeness defined (page/node/rack/DC); relatedness defined (key prefix/partition/tenant)|in primary storage not cache|at write degraded after rebalancing|within shard not across|that locality survives all operational events
P18|Stability under change|B3|adding/removing nodes/keys/clients does not cause disproportionate disruption|"disproportionate" defined (>1/N keys remap/>X% cache lost/>Y latency)|stable to additions not removals|to fewer than K simultaneous changes|in absence of specific failure patterns|that change is free only that cost is bounded
P19|Failure transparency|B3|failures of specified components are hidden from clients up to specified bounds|which components+failure types+bounds (latency/error rate/timeout)|to single-node not multi-node|reads not writes|brief window after which failure surfaces|that failures are prevented only that they are not exposed up to bound
P20|Observability|B4|relevant state is queryable or subscribable through specified interfaces|which state+through which interfaces+latency+cost|real-time not historical|per-component not aggregate|to operators not clients|that observed state is fresh only that it is reachable
P21|Auditability|B4|past operations are reconstructible from preserved records|which ops recorded+retention+integrity protection+who reads|for changes not reads|within retention not before|in summary not detail|that audit log itself is tamper-proof unless integrity separately claimed

# principle_groups(id|group|role|section)
G1|Data and logic|govern data vs code placement|5.1
G2|Scale and cardinality|govern cardinality choices|5.2
G3|Failure and resilience|govern failure handling|5.3
G4|Dependency and structure|govern coupling and layering|5.4
G5|Distribution|govern distributed system patterns|5.5
G6|Operator relationship|govern operator-system relationship|5.6

# principle_rules(id|name|group|rule|reasoning|domains|counter_principles)
R01|Data primacy|G1|data outlives logic; make data SoT; treat logic as transformation; configuration in data not code paths|data fully knowable+stable across env changes; logic unknowable in general (halting); data survives platform migrations+org changes+decade time spans|configuration mgmt+schema+automation+IaC|none direct; does not forbid logic just constrains where state lives
R02|Single source of truth|G1|every fact has exactly one authoritative location; all others are derived caches|when fact in multiple authoritative locations divergence becomes possible; reconciliation between authorities harder than between authority and cache|state mgmt+distributed systems+config+identity|peer-to-peer where no single source desired with Merge algorithm replacing SoT model
R03|Convention over lookup|G1|when function over data can produce answer prefer to registry that must be queried|functions deterministic+no coordination; registries require maintenance+can become inconsistent+add network call|naming+addressing+identifier construction|when function would be too complex (high-cardinality+frequently-changing) registry is correct
R04|0/1/∞|G2|three real cardinalities; design for whichever is correct never design for two|any cardinality > 1 tends toward many under organizational pressure; building for "two" or "few" creates system breaking at next growth step|replication topology+instance counts+multi-region|cost considerations may force small fixed N with explicit acknowledgment design will require change at growth
R05|Comprehensive over aggregate|G2|slice the whole; do not accrete from parts; model exists in totality even before implementation fills it|aggregate systems grow component-by-component with no plan for whole; become internally inconsistent because no whole was ever planned|system design+taxonomy construction+automation architecture|MVP often starts aggregate; conversion expensive but is path most systems must take
R06|One way to do each thing|G2|within environment converge on one method per task; many almost-identical implementations are the enemy|every variant must be maintained+monitored+understood; two systems doing same slightly differently produce twice operational load+confused incident response|production environments+operational tooling+deployment pipelines|deliberate redundancy for failure independence (different vendors+codebases for critical systems) acceptable when cost justified
R07|Idempotent retry|G3|every operation crossing failure boundary should be safely retryable|failures inevitable; retries are standard recovery; non-idempotent forces choice between data loss (no retry) and duplication (blind retry)|distributed systems+message processing+config application|counter-style ops and side-effect external calls cannot always be made idempotent without uniqueness keys or saga patterns
R08|Level-triggered over edge-triggered|G3|react to current state not events; missed events inevitable missed state is not|edge-triggered loses work when events missed (drops+restarts+races); level-triggered compares desired-vs-actual every iteration so missed event = next iteration catches|control loops+config mgmt+replication|pure event reaction required when state unbounded or expensive to compare; hybrid common
R09|Fail closed|G3|when uncertain deny rather than allow|in security+integrity contexts allowing unknown is larger risk; cost of false rejection is failed op; cost of false acceptance is breach/corruption|security+authorization+data validation|Fail open applies in availability-critical contexts where cost of false rejection (outage) exceeds cost of allowing unknown
R10|Fail open|G3|when uncertain continue degraded rather than halt|in availability-critical contexts cost of false rejection (outage) exceeds cost of allowing unknown|availability-critical paths|Fail closed applies in security/integrity contexts; choice is per-domain; both valid
R11|Bound everything|G3|every queue has max depth+every cache max size+every connection timeout+every retry budget|unbounded resources fail unboundedly; unbounded queue grows until OOM; unbounded retry never gives up|every long-running system|none direct; bounds may be very large but must exist
R12|Reversible changes|G3|prefer mechanisms allowing rollback|changes have unintended consequences; ability to revert is fastest recovery mechanism|deployments+schema migrations+config changes|some changes irreversible by nature (data deletion+public API removal); for these principle requires extra care up front since reversal unavailable
R13|Minimize dependencies|G4|each new dependency multiplies failure modes and migration costs|every dependency is thing that can break; operational logic especially cannot depend on what it controls|operational tooling+libraries+frameworks+build pipelines|rebuilding everything from scratch wasteful; principle is "minimize" not "eliminate"
R14|Separate planes|G4|data-plane+control-plane+management-plane have different SLAs+blast radii+failure modes; do not mix|data-plane handles user traffic must be fast HA; control-plane configures data-plane tolerates slower changes; management-plane observes both should survive failures of either|networking+distributed systems+K8s+database systems|small systems may not need full plane separation; principle scales with complexity
R15|Layer for separation of concerns|G4|each layer does one job with clean interface to next|layered systems easier to reason about+modify+replace; each layer can be optimized for its job without compromising others|networking(OSI)+system architecture+app design|too many layers create overhead+obscure data flow; principle is "appropriate" not "maximum"
R16|Bucket for locality and accounting|G4|group data by access pattern+tenant+lifecycle+failure domain; buckets are unit of operation|bucketing enables locality (related things together for performance)+accounting (per-bucket metrics+quotas)+isolation (failure does not propagate)|storage+caching+multi-tenant+network design|over-bucketing fragments resources+increases overhead; principle is "appropriate"
R17|Local cache + global truth|G5|keep updatable local copy of what is needed; fall through to global when local stale or missing|local fast and survives partitions; global authoritative but slow and partition-vulnerable; combining gets both performance and correctness|caching+config distribution+replicated stores|when local divergence cannot be tolerated (financial transactions) strong consistency must be paid for
R18|Centralize policy decentralize enforcement|G5|one place defines rules; many places enforce locally|central policy avoids drift across enforcers; local enforcement avoids SPOF of central enforcement and round-trips on every check|security policy+network policy+config+RBAC|when policy must be re-evaluated on every operation (audit logging+real-time fraud) enforcement may need to be central
R19|Push the decision down|G5|make decisions at lowest layer that has enough information|decisions made high require round-trips and serialize through choke points; decisions made low have more local information and run faster|routing+scheduling+query planning+network design|decisions requiring global knowledge cannot be pushed down; principle requires decision to be locally answerable
R20|Push the work down or out|G5|edge cache absorbs origin traffic; CDN absorbs edge; Anycast absorbs CDN; each layer reduces what next must handle|work close to source faster and avoids loading deeper layers; work at deepest layer should only be work that requires it|traffic handling+caching+computation placement|state-changing ops cannot be pushed out indefinitely; must reach SoT
R21|Make state observable|G6|if you cannot see it you cannot operate it|every operational decision requires evidence; mechanisms whose state is hidden cannot be diagnosed+tuned+trusted|every operational system|confidentiality may limit what can be exposed and to whom; observability and confidentiality must be reconciled not traded
R22|Removing classes of work|G6|goal of automation is not doing work faster — it is making work no longer need to be done|automation that only speeds manual work still requires manual work be done at scale; automation that removes work scales independently of work volume|operational automation+config mgmt|knowledge work creating automation itself cannot be removed only improved

# orthogonality(id|distinction|content)
OR1|Durability vs Persistence vs Availability|durability=data survives failures; persistence=data exists across process restarts; availability=data can be read now; durable-but-unavailable possible (safe but unreachable); available-but-not-durable possible (readable now but won't survive crash)
OR2|Consistency-data vs Consistency-replica|consistency-data=constraints hold; consistency-replica=replicas agree on value; system can have full data integrity on each replica while replicas disagree about which value is current
OR3|Ordering vs Isolation|ordering=sequence; isolation=interference; operations can be ordered without isolated (each sees others' partial state in order) and isolated without ordered (no global sequence exists)
OR4|Idempotency vs Determinism|idempotent op can be nondeterministic (each first-application produces random ID but reapplications produce no further change); deterministic op can be non-idempotent (increment is deterministic but not idempotent)

# principle_conflicts(id|conflicting_pair|resolution)
PC1|Fail-closed vs Fail-open|per-domain: fail-closed for security+integrity; fail-open for availability
PC2|Centralize vs Decentralize|"Centralize policy decentralize enforcement" is itself a resolution: different aspects of same concern have different centralization needs
PC3|Comprehensive vs Aggregate|principle prefers comprehensive but acknowledges aggregate as practical reality of MVP development
# rule: conflicts real and intentional; taxonomy does not resolve them; resolution belongs to construction methodology where specific property requirements determine which principle applies; conflict is signal that two valid approaches exist and choosing requires info beyond taxonomy itself

# triangle(id|aspect|content)
TR1|mechanisms→properties|mechanisms provide properties; native (Journal→Auditability+partial Durability) or configurable (Replicator can provide replica Consistency at several levels via synchronicity) or compositional (sync Replicator can provide linearizable replica Consistency at cost of Availability under partition)
TR2|properties→mechanisms|properties require mechanisms; some many (Idempotency via Comparators OR Sequencers OR Stores with appropriate write semantics); some require composition (Durability via Journals+Stores+Replicators); some require specific mechanisms (Authenticity requires Authenticator+trust root+Wrap-unwrap)
TR3|principles→mechanisms|principles select among mechanisms when multiple can provide required property; minimize-dependencies favors fewer external requirements; bound-everything favors explicit configurable bounds; push-decision-down favors less coordination
TR4|principles→properties|principles also constrain how properties realized: bound-everything requires Boundedness be claimed for every long-running mechanism even when not strictly necessary
TR5|the triangle|mechanism provides properties; principles govern mechanism choice; principles constrain property realization

# family_property_coverage(family|primary_bands)
F1|Locality+Failure-transparency+Ordering
F2|none directly; supports property realization in others
F3|Integrity+Authenticity+Confidentiality+Observability
F4|Durability+Persistence+Consistency-data+Locality
F5|Reversibility+Auditability+Ordering+Stability-under-change
F6|Boundedness+Liveness
F7|Observability
F8|Convergence+Liveness+Failure-transparency
F9|Integrity+Confidentiality+Authenticity+Boundedness
F10|Boundedness+Stability-under-change+Locality
F11|Atomicity+Isolation+Ordering+Consistency-replica
F12|none directly; supports property realization
F13|Availability+Liveness+Failure-transparency+Convergence
# rule: entries describe what family is typically used to address not what every member provides

# double_citizens(word|mechanism_form|property_form)
DC1|Durability|Journal|Store with sync commit|Replicator|the contract that committed data survives
DC2|Ordering|Sequencer|the guarantee that operations apply in sequence
DC3|Consistency|Replicator+Validator+Quorum (mechanisms providing it)|claim about constraints holding (data) OR claim about replica agreement (replica)
# rule: conflation arises because property motivates mechanism; we build journals because we want durability; we build sequencers because we want ordering; resolution is qualification

# spanning_mechanisms(mechanism|family_1|family_2|rationale)
SP1|Scheduler|F8 Control-loop|F10 Allocation|F8 decides when; F10 decides where; same algorithmic shape (filter+score+choose) serves both
SP2|Limiter|F9 Gating|F10 Allocation|F9 decides whether this request may proceed; F10 decides how much capacity each consumer gets; same mechanism family depends on operator's intent
SP3|Replicator|F1 Information-movement|F4 Storage|moves data; consequence is data exists in multiple locations
# convention: name mechanism once in primary family with cross-references where relevant

# excluded(category|excluded|why)
E1|mechanism|application-layer protocols (HTTP+gRPC+message-queue protocols)|compositions of lower-level mechanisms; taxonomy describes components rather than composed protocols
E2|mechanism|specific data structures (B-trees+LSM-trees+skip lists)|implementations of Index and Store mechanisms; taxonomy stops at interface
E3|mechanism|programming-language constructs (futures+channels-as-language-feature+generators)|application-layer concerns out of scope
E4|mechanism|AI-specific operational mechanisms (model rollout+training-pipeline orchestration+inference traffic shaping)|forming as recognizable family but boundaries still shifting
E5|mechanism|edge-compute coordination patterns beyond Replicator+Reconciler|not yet stable enough to name
E6|property|performance properties (throughput+latency percentiles)|quantitative measurements rather than contracts; appear in conditions on other properties
E7|property|compliance properties (HIPAA+PCI-DSS)|bundles of other properties applied to specific data classes; not atomic property claims
E8|property|cost properties|economic not operational
E9|property|verifiability as distinct from authenticity+integrity|expected to mature in zero-knowledge/cryptographic-proof sense
E10|property|tunability as property of mechanisms whose contracts adjust at runtime|expected to mature

# meta_patterns(pattern|applies_across|rationale)
MP1|Bucketing|Storage(cache lines+partitions)+Selection(hash buckets)+Allocation(resource pools)+Sensing(histograms)+Lifecycle(TTL cohorts)|organizing technique applied across mechanisms not single mechanism
MP2|Layering|Information-movement(network layers)+Representation(wrap-unwrap stacking)+Storage(cache hierarchies)+Gating(defense in depth)|how mechanisms deployed not what mechanisms are
# rule: presence/absence of bucketing or layering does not change what mechanism is; flagged here rather than creating "Bucketing family" or "Layering family" because that would mis-describe their nature

# limits(id|limit|content)
LM1|hardware mechanisms|memory hierarchies+bus protocols+instruction-level mechanisms appear as boundary conditions but not enumerated
LM2|application-layer concerns|business logic+UI+app architecture out of scope
LM3|sociotechnical concerns|team structure+on-call practice+communication+change mgmt+org dynamics not addressed; operational success depends heavily on these; taxonomy silent
LM4|domain-specific mechanisms|ML pipelines+blockchain consensus+real-time control+scientific computing may have mechanisms not enumerated; taxonomy aimed at general infrastructure; specialized domains may need extensions
# rule: taxonomy intended as foundation domains can extend not complete description of every system

# implementations(mechanism|common_implementations)
IMP01|Channel|TCP+QUIC+Unix-domain-socket+SSH-transport+ZeroMQ+gRPC-streams+Kafka-connections+MQTT
IMP02|Fanout|Multicast(IGMP)+Anycast(BGP)+Redis-pubsub+Kafka-topics-with-multi-consumer-groups+NATS+AWS-SNS+Salt-master-publish
IMP03|Funnel|Fluentd+Logstash+Vector+syslog-aggregators+OpenTelemetry-collectors+Prometheus-scraping+Salt-returners
IMP04|Replicator|Postgres-streaming+MySQL-binlog+MongoDB-oplog+Cassandra-hinted-handoff+Redis-replication+Kafka-MirrorMaker+rsync+etcd-Raft+K8s-informer-caches
IMP05|Relay|HAProxy+Envoy+nginx-proxy+Squid+stunnel+ngrok+AWS-API-Gateway
IMP06|Index|B-tree(RDBMS)+LSM-tree(Cassandra+RocksDB+LevelDB)+bloom(Cassandra-SSTables+Bitcoin)+GIN/GiST(Postgres)+inverted(Elasticsearch+Lucene)+R-tree(PostGIS)+HLL(Redis-HLL+Presto)
IMP07|Selector|SQL-WHERE+K8s-label-selectors+Salt-grain-match+Ansible-host-patterns+PromQL-{label=value}+AWS-resource-tag-filters
IMP08|Comparator|etag/If-Match(HTTP)+Postgres-MVCC-visibility+K8s-resourceVersion-check+vector-clocks(Riak)+git-diff
IMP09|Hasher|SHA-2+BLAKE3+xxHash+MurmurHash3+CRC32+consistent-hashing(Cassandra+Memcached)+Rendezvous/HRW
IMP10|Ranker|K8s-scheduler-scoring+Postgres-query-planner+search-engines(BM25+learned-to-rank)+HAProxy-least-conn
IMP11|Router|iptables+nftables+IP-routing-tables(FIB)+kube-proxy+Envoy-route_config+AWS-ALB-rules+message-brokers
IMP12|Wrap/unwrap-representational|JSON+protobuf+MessagePack+BSON+Avro+CBOR+base64+gzip+zstd+tar
IMP12s|Wrap/unwrap-secure|TLS-1.2/1.3+IPSEC+SSH-transport+JOSE/JWT/JWS/JWE+signed-URLs
IMP12r|Wrap/unwrap-routing|VXLAN+GRE+MPLS+Geneve+WireGuard+OpenVPN
IMP13|Schema|Postgres-DDL+JSON-Schema+OpenAPI+protobuf-.proto+Avro-schema+SQL-DDL+GraphQL-SDL
IMP14|Namespace|DNS-zones+K8s-namespaces+filesystem-directories+Java-packages+Cassandra-keyspaces+Postgres-schemas
IMP15|Naming-convention|RFC-FQDN+K8s-app.kubernetes.io/*-labels+AWS-ARN+Cassandra-composite-keys+snowflake-IDs+ULIDs
IMP16|Buffer|Linux-pipe-buffers+kernel-ring-buffer(dmesg)+Kafka-in-memory-queues+circular-buffers+Go-channels
IMP17|Cache|Memcached+Redis+Varnish+CDN-edges(Cloudflare+Fastly+Akamai)+Linux-page-cache+CPU-L1/L2/L3+browser-cache
IMP18|Store|Postgres+MySQL+Cassandra+MongoDB+etcd+ZooKeeper+S3+HDFS+ext4+ZFS
IMP19|Journal|Postgres-WAL+MySQL-binlog+ext4-journal+Cassandra-commitlog+Redis-AOF+Kafka-log-segments+etcd-WAL
IMP20|Log|syslog+journald+app-logs+AWS-CloudTrail+audit-logs+web-server-access-logs
IMP21|Snapshot|ZFS-snapshots+LVM-snapshots+AWS-EBS-snapshots+pg_dump+Redis-RDB+K8s-etcd-backups+VM-snapshots+Btrfs-snapshots
IMP22|Tombstone|Cassandra-tombstones+Riak-tombstones+soft-delete-columns+Kafka-tombstone-messages+S3-delete-markers-in-versioned-buckets
IMP23|Version-stamp|Git-SHA+Postgres-LSN+MySQL-GTID+K8s-resourceVersion+S3-ETag+MongoDB-ObjectId+Cassandra-timestamps+vector-clocks(Riak+Voldemort)
IMP24|History|Git-commits+Mercurial-revsets+Perforce-changelists+Postgres-WAL+S3-object-versions+time-travel-queries(Snowflake+BigQuery)
IMP25|Merge-algorithm|Git-three-way+Riak-siblings+CRDTs+LWW(Cassandra+DynamoDB)+OT(Google-Docs)+automerge
IMP26|Diff|unified-diff+JSON-Patch(RFC-6902)+JSON-Merge-Patch(RFC-7396)+K8s-strategic-merge-patch+migration-tools(Flyway+Alembic)
IMP27|Reference|Git-refs(branches+tags+HEAD)+Docker-image-tags+K8s-deployment-template-ref+symlinks+S3-latest-version+CNAME
IMP28|TTL|DNS-TTL+Redis-EXPIRE+Cassandra-TTL-columns+Kafka-log-retention+S3-lifecycle+browser-cookie-max-age+ARP-cache-timeouts
IMP29|Lease|DHCP-leases+K8s-leader-election-leases+ZooKeeper-ephemeral-nodes+Consul-sessions+Raft-leader-leases+file-locks-with-timeouts
IMP30|Reaper|Postgres-autovacuum+Cassandra-compaction(tombstone-GC)+Linux-OOM-killer+K8s-GC-controller+Java-GC+conntrack-timeout-sweep
IMP31|Drainer|K8s-pod-termination-grace-period+HAProxy-connection-draining+AWS-ELB-deregistration-delay+Cassandra-nodetool-decommission
IMP32|Probe|K8s-liveness/readiness-probes+HAProxy-health-checks+AWS-ELB-target-health+gRPC-health-protocol+Nagios+Pingdom
IMP33|Counter|Prometheus-Counter+statsd-counter+eBPF-counters+/proc/net/stat+syscall-counters
IMP34|Gauge|Prometheus-Gauge+/proc/loadavg+JMX-gauges+top+free+df
IMP35|Histogram|Prometheus-Histogram+t-digest+HDRHistogram+OpenTelemetry-histograms+ELK-percentile-aggregations
IMP36|Watch|K8s-watch-API+etcd-watch+ZooKeeper-watches+inotify+Consul-blocking-queries+Kafka-consumer-subscribe
IMP37|Heartbeat|Cassandra-gossip+Consul-gossip+Kafka-heartbeats+BGP-keepalive+OSPF-hello+mobile-app-pings
IMP38|Reconciler|K8s-controllers+K8s-operators+Terraform-apply+Salt-state.apply+Puppet-agent+ArgoCD+Flux
IMP39|Reactor|Webhooks+K8s-Reactor(client-go)+AWS-Lambda-event-triggered+GitHub-Actions+EventBridge-rules
IMP40|Scheduler-control|cron+systemd-timers+K8s-CronJob+Quartz+Airflow-scheduler+Hangfire
IMP41|Workqueue|K8s-client-go-workqueue+Sidekiq+Celery+AWS-SQS+RabbitMQ-work-queues+Resque
IMP42|Authenticator|Kerberos+OAuth-2.0/OIDC+SAML+PKI-client-certs+SSH-key-auth+AWS-IAM+LDAP+Active-Directory
IMP43|Authorizer|K8s-RBAC+AWS-IAM-policies+OPA+Casbin+Postgres-GRANT+Cedar
IMP44|Validator|JSON-Schema-validators+K8s-validating-webhooks+Postgres-CHECK+OpenAPI-validators+OPA-Gatekeeper
IMP45|Mutator|K8s-mutating-webhooks(Istio-sidecar-injection)+Postgres-BEFORE-INSERT-triggers+GraphQL-middleware+AWS-Lambda-authorizers
IMP46|Filter|iptables+nftables+AWS-Security-Groups+AWS-NACLs+K8s-NetworkPolicy+Calico+Snort+ModSecurity+Cloudflare-WAF
IMP47|Limiter|nginx-limit_req+Envoy-rate-limit-filter+Redis-cell+AWS-API-Gateway-throttling+Cloudflare-rate-limiting+semaphores
IMP48|Pool|DB-connection-pool(HikariCP+pgbouncer)+thread-pool+AWS-EC2-ASG+K8s-node-pool+IP-address-pool(DHCP)
IMP49|Quota|K8s-ResourceQuota+AWS-service-quotas+Linux-cgroups+disk-quotas(quotactl)+Cassandra-throughput-throttle
IMP50|Scheduler-allocation|K8s-scheduler+Mesos+YARN+Slurm+AWS-ECS-placement+Borg+Nomad+Linux-CFS
IMP51|Sharder|Cassandra-token-ring+Redis-Cluster-slots+MongoDB-sharded-clusters+Vitess+Citus+Elasticsearch-shards
IMP52|Lock|pthread-mutex+Postgres-advisory-locks+Redis-Redlock+ZooKeeper-locks+etcd-lease-based-locks+flock
IMP53|Election|Raft(etcd+Consul)+Paxos(Spanner)+ZAB(ZooKeeper)+Patroni(Postgres)+Sentinel(Redis)+Bully
IMP54|Barrier|pthread-barrier+ZooKeeper-double-barrier-recipe+Java-CyclicBarrier+MPI_Barrier+K8s-Init-Containers
IMP55|Quorum|Raft-majority+Paxos-quorum+Cassandra-CL=QUORUM+etcd-quorum-reads/writes+MongoDB-w=majority+Galera
IMP56|Sequencer|Postgres-SEQUENCE+Twitter-Snowflake+MongoDB-ObjectId+Kafka-offsets+Lamport+vector-clocks+DynamoDB-versionId
IMP57|Renderer|Jinja2+Mustache+Handlebars+Go-html/template+ERB+Helm-templates+Terraform-templates+Liquid
IMP58|Transformer|UNIX-pipes+awk+jq+MapReduce+Spark-transformations+Pandas+Kafka-Streams+Flink
IMP59|Compactor|Cassandra-compaction+Kafka-log-compaction+Postgres-VACUUM-FULL+RocksDB-compaction+Btrfs-balance+ZFS-scrub
IMP60|Retrier|Polly(.NET)+Resilience4j+AWS-SDK-retries+gRPC-retry-policies+Postgres-replication-retry
IMP61|Circuit-breaker|Hystrix+Resilience4j+Envoy-outlier-detection+Polly+Sentinel(Alibaba)
IMP62|Bulkhead|Hystrix-thread-pools+K8s-namespaces-with-quotas+AWS-account-isolation+Cell-based-architectures
IMP63|Hedger|Google-tail-tolerant-request-hedging+Envoy-hedge_policy+Cassandra-speculative-retry+BigTable-hedged-reads
IMP64|Failover|Patroni+repmgr+MHA+Sentinel+Cluster-IP-failover(keepalived)+AWS-RDS-Multi-AZ+K8s-pod-replacement

# gap_analysis(property|claim|delivered|gap_reason)
GAP01|Durability|"Your data is safe"|survives single-machine crash; loses last 1-10s on async replication|sync replication too slow for default config
GAP02|Availability|"99.99% uptime"|read availability of cached responses; write availability lower|reads easy to scale writes serialize through primary
GAP03|Consistency-replica|"Consistent"|eventual with 50ms-60s lag; "strong" only on primary|true linearizability requires expensive coordination
GAP04|Atomicity|"Transactional"|per-row in NoSQL; per-transaction in RDBMS; rarely cross-system|distributed transactions(XA+2PC) avoided due to cost
GAP05|Idempotency|"Safe to retry"|safe for GET/PUT/DELETE; not for POST without uniqueness keys|HTTP semantics widely misimplemented
GAP06|Ordering|"FIFO"|per-partition only; no global order|global order requires global serialization
GAP07|Determinism|"Reproducible"|reproducible given identical inputs; rarely hit in practice|time+randomness+concurrency+external state
GAP08|Isolation|"Serializable"|Read Committed by default; serializable rare|performance cost of true serializable
GAP09|Failure-transparency|"Self-healing"|transparent for replica loss; opaque for primary loss|primary failover often requires manual or complex automation
GAP10|Observability|"Fully observable"|real-time per-component; hard to correlate cross-component|no global causality; logs/metrics/traces siloed
GAP11|Auditability|"Audited"|audit log exists; tamper-evident only with separate effort|audit log itself rarely has integrity protection
GAP12|Reversibility|"Rollback supported"|rollback for database; not for downstream side effects|API calls+emails+payments cannot be unsent
GAP13|Boundedness|"Capped at N"|capped under normal load; unbounded during failures or queue buildup|bounds rarely enforced under stress
GAP14|Confidentiality|"Encrypted"|encrypted in transit; sometimes at rest; rarely against operator|operator-level confidentiality requires confidential computing
GAP15|Authenticity|"Authenticated"|identity of immediate sender(TLS); rarely end-to-end author identity|sender ≠ author in most architectures

# system_populations(system_category|dominant_families|light_or_absent)
POP01|Configuration mgmt(Salt+Ansible+Puppet)|F8+F2+F12+F7|F5(light)+F11(light)
POP02|Container orchestration(K8s+Nomad)|F8+F10+F9+F7+F11|F12(light)
POP03|Relational DB(Postgres+MySQL)|F4+F11+F5+F9|F1(limited to replication)
POP04|Distributed DB(Cassandra+DynamoDB)|F4+Replication+F11(Quorum)+F5|strong gating absent (no FK/CHECK)
POP05|In-memory store(Redis+Memcached)|F4(volatile)+F1+F6|F5(light)+strong durability(optional)
POP06|Object store(S3+GCS)|F4+F5+F9|strong consistency(eventual until 2020)+F11
POP07|Message broker(Kafka+RabbitMQ+NATS)|F1+F4(Journal)+F11|F9(basic)+F2(limited)
POP08|Stream processor(Flink+Spark-Streaming+Kafka-Streams)|F12+F4+F7|F9+F5
POP09|CDN(Cloudflare+Fastly+Akamai)|F1(Anycast+Fanout)+F4(Cache)+F9|F11+F5
POP10|Load balancer(HAProxy+nginx+Envoy)|F2(Router+Ranker)+F7+F13|F4+F5
POP11|DNS(BIND+Unbound+Route53)|F2+F4+F1+F6|F11+F5(basic)
POP12|Firewall(iptables+nftables+AWS-SG)|F9(Filter+Limiter)+F2|F4+F11
POP13|Source control(Git+Perforce)|F5(entire)+F4+Comparison|F1(push/pull only)+F11(limited)
POP14|Service mesh(Istio+Linkerd)|F1+F9+F7+F13|F4(none of own)
POP15|Observability stack(Prometheus+Grafana+ELK)|F7+F4+F2(PromQL+Lucene)|F9+F11
POP16|File transfer(rsync+sftp+aspera)|F1+Comparison(delta)+F5(limited)|most others absent — single-purpose tool
POP17|Identity provider(Keycloak+Okta+AD)|F9(Authenticator+Authorizer)+F4+F5|F1(light)
POP18|Backup system(Bacula+Borg+Restic)|F4(Snapshot)+F5+Compactor|F11(light)

# failure_modes(failure_mode|properties_lost|properties_preserved)
FM01|Single process crash|Liveness(briefly)+in-flight Atomicity|Durability(with WAL)+Consistency-data(with rollback)
FM02|Single node power loss|Liveness+fsync-pending writes if not synced|Durability(committed)+Consistency-replica(with replicas)
FM03|Network partition|Consistency-replica(CP) OR Availability(AP) — choose one|Durability+Liveness within partition
FM04|Single disk failure|Boundedness(capacity)+data on that disk if no RAID|Durability(with replication or RAID)+Availability
FM05|Single rack failure|Locality+requests pinned to rack|most properties (with multi-rack replication)
FM06|Single DC failure|Locality+regional Availability|Durability(multi-DC)+global Availability
FM07|Region failure|Durability(without multi-region)+region's Availability|multi-region durability+other regions' Availability
FM08|Clock skew|Determinism(time-dependent)+Ordering(timestamp-based)|wall-clock-independent properties
FM09|Quorum loss(>N/2 nodes down)|Consistency-replica writes+Liveness for writes|read availability if AP
FM10|Cache failure|Locality+Availability for cache-bound traffic|SoT properties(Durability+Consistency)
FM11|Authenticator failure|Authenticity+all dependent gating|properties of already-authenticated sessions
FM12|Bulk corruption(silent)|Integrity+Auditability if logs corrupted|almost nothing without integrity checking
FM13|Insider threat|Confidentiality+Integrity+Auditability|none reliably without external controls
FM14|Resource exhaustion(queue full+conn full)|Liveness+Boundedness violated+Availability|Durability+Consistency for completed ops
FM15|Cascading failure|Failure-transparency+Liveness across many systems|often nothing without Bulkhead
FM16|Time skew across replicas|Ordering+LWW correctness|properties not relying on wall clocks
FM17|Split-brain(election failure)|Consistency-replica+Atomicity|per-partition consistency on each side

# confusions(pair|distinguishing_question)
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
CF13|Hasher vs Sequencer|Hasher content-derived(deterministic from input); Sequencer allocation-derived(monotonic over time)
CF14|Index vs Schema|Index accelerates lookup over existing data; Schema describes what data is allowed
CF15|Pool vs Quota|Pool is resources to draw from; Quota is limit on how much one party may draw
CF16|Watch vs Funnel|Watch=subscribe to changes(per-resource); Funnel=aggregate from many sources(per-stream)

# violations(principle|typical_consequence)
VL01|Data primacy|configuration buried in code; can't change behavior without redeploying
VL02|Single source of truth|drift between sources; reconciliation harder than between authority and cache
VL03|Convention over lookup|brittle naming; every change requires updating registry
VL04|0/1/∞|system breaks at next growth step ("we built it for two replicas")
VL05|Comprehensive over aggregate|internally inconsistent system; no plan for whole; ops engineers can't predict behavior
VL06|One way to do each thing|twice operational load; each variant separately monitored and understood
VL07|Idempotent retry|retries cause duplication+double-charges+double-emails
VL08|Level-triggered over edge-triggered|missed events become missed work; system silently diverges from desired state
VL09|Fail closed(security)|false acceptances become breaches
VL10|Fail open(availability)|outage on minor failures; unnecessary downtime
VL11|Bound everything|unbounded queue→OOM; unbounded retries→never give up; cache→fills disk
VL12|Reversible changes|rollback unavailable on incident; long MTTR
VL13|Minimize dependencies|cascading failures; one outage causes many; bootstrap impossible
VL14|Separate planes|control plane outage takes down data plane; no way to manage during incident
VL15|Layer for separation of concerns|tight coupling; replacing one layer requires changing others
VL16|Bucket for locality and accounting|hot tenants starve others; no per-tenant accountability
VL17|Local cache + global truth|every request hits global authority→bottleneck; or no fallback when global partitioned
VL18|Centralize policy decentralize enforcement|policy drift across enforcers OR SPOF on every check
VL19|Push the decision down|every decision serialized through coordinator; latency ceiling
VL20|Push the work down/out|origin servers absorb all traffic; no scaling without rebuilding
VL21|Make state observable|can't diagnose; every incident becomes guessing game
VL22|Removing classes of work|automation only speeds work doesn't eliminate it; team scales with workload

# impossibility_triplets(triplet|observation)
IT01|Consistency-replica + Availability + Partition-tolerance|pick two(CAP); under partition CP rejects writes AP accepts and reconciles later
IT02|Consistency-replica + Availability + Latency|at higher consistency levels latency increases; PACELC
IT03|Durability + Latency + Throughput|sync durability bounds throughput; async durability risks loss
IT04|Idempotency + Atomicity + Ordering|achieving all three across distributed parties requires consensus; no shortcuts
IT05|Confidentiality + Observability + Auditability|encrypted-at-rest harder to audit; audit data itself sensitive
IT06|Locality + Stability-under-change + Availability|rebalancing for locality after change reduces availability briefly
IT07|Reversibility + Atomicity(of side effects) + Latency|reversible distributed ops require sagas or 2PC both slow
IT08|Determinism + Liveness + Real-time-clocks|deterministic system using real time cannot be both reproducible and responsive to wall-clock events
IT09|Failure-transparency + Boundedness + Liveness|hiding failures requires retries which can violate bounds and stall liveness

# evolution(mechanism|older_standard|modern_standard)
EV01|Election|manual failover+custom heartbeat scripts|Raft(etcd+Consul) widely available
EV02|Replicator|master-slave (term itself now changed)|master-replica or peer-to-peer; CRDTs for AP systems
EV03|Lock(distributed)|custom NFS file locks+ad-hoc|Raft-backed(etcd locks)+lease-based
EV04|Probe|TCP connect or ping|HTTP /healthz+/readyz+/livez (K8s convention now industry-wide)
EV05|Schema|free-form text or per-RDBMS DDL|OpenAPI+protobuf+JSON-Schema as portable schemas
EV06|Naming-convention|per-organization arbitrary|cloud resource ARNs+K8s standard labels+RFC-driven IDs(ULID)
EV07|Reconciler|cron+scripts|Operator pattern(K8s)+GitOps(Flux+Argo)
EV08|Authenticator|per-app passwords+LDAP|OIDC+federated SSO+mTLS+workload identity
EV09|Filter(network)|iptables linear scan|nftables sets+eBPF programs+cloud-native security groups
EV10|Compactor|manual VACUUM+cron-driven defrag|background autovacuum+LSM auto-compaction
EV11|Quorum|hand-rolled per system|library/framework primitives(etcd+ZooKeeper recipes)
EV12|Versioning(data)|last-write-wins or none|MVCC standard in OLTP; CRDTs growing in distributed systems
EV13|Heartbeat-detection|fixed timeout|Phi accrual+gossip-amplified
EV14|Sequencer|auto-increment(single point)|Snowflake-style distributed; ULIDs for sortable IDs
EV15|Snapshot|stop-the-world dumps|online consistent snapshots(ZFS+EBS+Postgres)

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
FL11|System won't scale past N nodes|F11(centralization point)+F10(Sharder)|F4(single-primary bottleneck)
FL12|Memory keeps growing|F6(Reaper+TTL)|F10(Quota)
FL13|Cascading outage took down everything|F13(Bulkhead+Circuit-breaker)|—
FL14|Audit log incomplete|F4(Log retention)+F7(Counter coverage)|F9(logged at right point)
FL15|Deployments break things in production|F5(Reference+History)+F13(Failover)|F8(Reconciler logic)
FL16|Two systems see different facts|(SoT principle violated)|F5(Reconciliation)
FL17|Tail latency bad|F13(Hedger)+F10(Scheduler)|F4(Cache hit rate)
FL18|Deletes resurrect|F4(Tombstone discipline)+F6(gc_grace)|F1(Replicator)
FL19|Names collide|F3(Namespace+Naming-convention)|F11(Sequencer for unique IDs)
FL20|Schema migration breaks clients|F3(Schema versioning)+F5(References)|—

# relationships(from|rel|to)
T1|grounds|A1
T1|grounds|A2
T1|grounds|A3
T1|enables|T8
T2|distinct_from|T3
T3|distinct_from|T4
T5|resolves|T10
T8|implemented_by|TR1
T8|implemented_by|TR2
T8|implemented_by|TR3
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
M19|requires_for_atomicity|appropriate-commit-protocols
M04|configurably_provides|P15(via synchronicity)
M17|cannot_provide|P03
M17|provides|P12+P17
M38|natively_provides|P09
M40|spans|F8+F10
M47|spans|F9+F10
M04|spans|F1+F4
P01|provided_by|M08+M56+M18(with appropriate write semantics)
P03|composed_from|M19+M18+M04(in combination)
P06|composed_from|M42+M13(trust root)+M12
P20|composed_from|M33+M34+M35+M36+M02(query protocols)
R02|distinct_from|peer-to-peer-systems-where-no-single-source-desired
R09|opposes|R10
R09|domain|security+integrity
R10|domain|availability-critical
R18|resolves|centralize-vs-decentralize-tension
R05|preferred_over|aggregate-systems
R05|opposes|R05-counter(MVP-aggregate-reality)
PC1|resolution_pattern|per-domain-choice
PC2|resolution_pattern|already-encoded-in-R18
PC3|resolution_pattern|aggregate-as-MVP-comprehensive-as-target
DC1|resolved_by|qualification(durability-mechanism-vs-property)
DC2|resolved_by|qualification
DC3|resolved_by|qualification(consistency-data-vs-replica)
SP1|named_in|F8-primary
SP2|named_in|F9-primary
SP3|named_in|F1-primary
MP1|applies_across|all-families
MP2|applies_across|F1+F3+F4+F9
LM3|silent_on|operational-success-depends-heavily-on-these
IMP_ALL|grounds|abstract-mechanisms-in-real-implementations
GAP_ALL|names|where-industry-vocabulary-diverges-from-contract-reality
POP_ALL|situates|systems-in-taxonomy
FM_ALL|shows|engineering-tradeoff-space
CF_ALL|prevents|architectural-mistakes-from-confused-mechanisms
VL_ALL|shows|consequences-of-violating-each-principle
IT_ALL|generalizes|CAP-style-impossibility-results
EV_ALL|spots|where-industry-conventions-mid-shift
FL_ALL|reverse_indexes|symptom-to-family

# section_index(section|title|ids)
1|Introduction|T1,T2,T3,T4,T5,T8
2|Terminology and Ground Rules|T1-T7,T10
3|Mechanism Axis|F1-F13,M01-M64
3.1|Information Movement|F1,M01,M02,M03,M04,M05
3.2|Selection|F2,M06,M07,M08,M09,M10,M11
3.3|Representation|F3,M12,M13,M14,M15
3.4|Storage|F4,M16,M17,M18,M19,M20,M21,M22
3.5|Versioning|F5,M23,M24,M25,M26,M27
3.6|Lifecycle|F6,M28,M29,M30,M31
3.7|Sensing|F7,M32,M33,M34,M35,M36,M37
3.8|Control loop|F8,M38,M39,M40,M41
3.9|Gating|F9,M42,M43,M44,M45,M46,M47
3.10|Allocation|F10,M48,M49,M50,M51
3.11|Coordination|F11,M52,M53,M54,M55,M56
3.12|Transformation|F12,M57,M58,M59
3.13|Resilience|F13,M60,M61,M62,M63,M64
4|Property Axis|B1,B2,B3,B4,P01-P21
4.1|Data integrity|B1,P01-P07
4.2|Behavioral|B2,P08-P14
4.3|Distribution|B3,P15-P19
4.4|Operational|B4,P20-P21
4.5|Property orthogonality|OR1,OR2,OR3,OR4
5|Principle Axis|G1-G6,R01-R22
5.1|Data and logic|G1,R01,R02,R03
5.2|Scale and cardinality|G2,R04,R05,R06
5.3|Failure and resilience|G3,R07,R08,R09,R10,R11,R12
5.4|Dependency and structure|G4,R13,R14,R15,R16
5.5|Distribution|G5,R17,R18,R19,R20
5.6|Operator relationship|G6,R21,R22
5.7|Principle conflicts|PC1,PC2,PC3
6|Relationships Between Axes|TR1,TR2,TR3,TR4,TR5,family-property-coverage
7|Overlaps Ambiguities Known Issues|DC1,DC2,DC3,SP1,SP2,SP3,E1-E10,MP1,MP2,LM1-LM4
8|Closing|T1-T13 restated structurally
E|Mechanism Implementations|IMP01-IMP64
F|Property Gap Analysis|GAP01-GAP15
G|System Populations|POP01-POP18
H|Properties at Risk Under Failure|FM01-FM17
I|Mechanism Confusions|CF01-CF16
J|Principle Violations|VL01-VL22
K|Impossibility Triplets|IT01-IT09
L|Mechanism Evolution|EV01-EV15
M|Fast-Locator|FL01-FL20

# decode_legend
mechanism_count: 62 (M01-M64 with two skipped numbers from internal restructure: Hedger=M63, Failover=M64)
property_count: 21
principle_count: 22
mechanism_families: 13
property_bands: 4
principle_groups: 6
spanning_mechanisms: Scheduler(F8+F10)|Limiter(F9+F10)|Replicator(F1+F4)
double_citizens: Durability|Ordering|Consistency
property_orthogonality_pairs: Durability/Persistence/Availability|Consistency-data/Consistency-replica|Ordering/Isolation|Idempotency/Determinism
principle_conflicts: Fail-closed-vs-Fail-open|Centralize-vs-Decentralize|Comprehensive-vs-Aggregate
triangle: mechanism→provides→property|principle→selects→mechanism|principle→constrains-realization→property
sub_type_separator: pipe within sub_types column
composes_with_separator: plus
appendix_letters: E=implementations|F=gap-analysis|G=system-populations|H=failure-modes|I=confusions|J=violations|K=impossibility-triplets|L=evolution|M=fast-locator
sot_for_axis_separation: three-axis structure is load-bearing claim; contents revisable
qualification_discipline: always qualify ambiguous words (durability mechanism vs property vs principle)
rel_types: grounds|enables|distinct_from|resolves|implemented_by|provides|requires|selects_among|constrains_realization_of|primary_addresses|natively_provides|configurably_provides|cannot_provide|spans|composed_from|opposes|preferred_over|resolution_pattern|domain|resolved_by|named_in|applies_across|silent_on|requires_for_atomicity|reverse_indexes|generalizes|spots|prevents|situates|shows|names
