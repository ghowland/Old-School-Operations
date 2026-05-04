# OLD SCHOOL OPERATIONS — LLM-COMPACT FORM
# Source: Howland, 25yr ops/SRE. Format: pipe-delimited tables, ID refs.
# Read order: concepts → axes → distinctions → rules → claims → examples → relationships → chapters

# concepts(id|name|def|category)
C1|Operations|networked/server/datacenter/production mgmt as unified discipline|term
C2|Control|ability to gather info from + change an environment; central tenet of ops|principle
C3|Automation|removing classes of work while consistently getting desired results|principle
C4|Class of Work|any category of task humans currently perform|term
C5|Real|physical, has mass/properties, exists in physical world|term
C6|Virtual|symbolic, un-real, conceptual; data/logic/words|term
C7|Knowability|spectrum of how completely a thing can be known|term
C8|Data|virtual, symbolic, descriptive; fully knowable|term
C9|Logic|executable virtual; code/scripts/decision-trees/state-machines|term
C10|Data Source|any mechanism storing data; mandatory feature=access|term
C11|System|interrelated components producing effects; black-boxable IOSE|term
C12|Universal Machine|anything definable by Inputs/Outputs/Side-Effects|tool
C13|IOSE|Inputs+Outputs+Side-Effects interface|tool
C14|Systemic Thinking|modeling everything as IOSE network|principle
C15|Philosopher's Knife|tool for slicing concepts without losing the whole|tool
C16|Slicing the Pie|comprehensive subdivision preserving total volume|tool
C17|Comprehensive System|built top-down from whole, internally consistent|principle
C18|Aggregated System|built bottom-up brick-by-brick, never whole|anti-pattern
C19|Engineering|efficient use of resources in environment to yield desired effect|principle
C20|Attribute Axis|spectrum on which a system property is rated|tool
C21|Axiomatic Engineering|decision-making via prioritized attribute axes|principle
C22|Alignment|all components consistent + efficient together over time|principle
C23|Internal Consistency|all parts of model agree; superset prereq of Alignment|principle
C24|Impersonal Decision Making|decisions fall out of axes+priorities, not personality|principle
C25|Best (anti)|absolute term obscuring tradeoffs; only valid for narrow exact context|anti-pattern
C26|Better|explicit comparison forcing tradeoff articulation|principle
C27|Fashion Oriented Engineering|copying practices from blogs without context analysis|anti-pattern
C28|Best Practices (anti)|recipes presented as universal; really just case studies|anti-pattern
C29|Production Environment|where revenue/customer-interface/product happens; one per org|term
C30|Security Zone|environment classified by who+what is allowed|term
C31|Operational Logic|code supporting infra; assumes failure; minimal deps; resilient|principle
C32|Application Logic|code serving end-users; assumes env works; exits on failure|term
C33|One-Way-To-Do-It|prod env should have single canonical method per task category|principle
C34|Distributed System|work spread across many nodes vs single instance|term
C35|DOS|Distributed Operating System; whole prod env as one logical machine|principle
C36|Idempotency|f(f(x))=f(x); same result regardless of starting state|rule
C37|Modeling|creating maps of systems for understanding or control|tool
C38|Model for Understanding|disposable, ephemeral, "good enough"|term
C39|Model for Control|must be accurate + synced for resource lifetime|principle
C40|Source of Truth|authoritative data location for given domain|term
C41|Knowing the Present|gathering current-state data; never truly "now", always aged|principle
C42|Black-Boxing|wrapping unknown internals in IOSE interface|tool
C43|Pragmatism|evaluate by effects only|principle
C44|Wisdom|breadth/depth of insight from experience; judgment of outcomes|term
C45|Intelligence (Cipolla)|action yielding benefit for all parties|term
C46|Win-Win-Win|self+org+external all benefit|principle
C47|Personal Experience|highest-trust info source; you saw it yourself|principle
C48|Hearsay|info reported by others without your verification; lower trust|term
C49|Local Reality|the actual context you operate in vs abstract general info|principle
C50|Generation Levels of Experience|multi-generation iteration needed to mature a discipline|term
C51|Land Mines in Your Yard|knowingly burying future problems via short-term fixes|anti-pattern
C52|Technical Debt|tradeoff: speed-now for cost-later; sometimes correct|term
C53|Throwing Hardware At It|scaling by adding machines to broken design|anti-pattern
C54|Logic In Data Store|stored procs/triggers; pollutes knowable space with unknowable|anti-pattern
C55|Magical Thinking|"X just happened out of nowhere"; signals broken mental model|anti-pattern
C56|AAA|Authenticate / Authorize / Account|rule
C57|Stupidity (Cipolla)|action causing harm to others without benefit to self|term
C58|Halting Problem|cannot determine if arbitrary program terminates|term
C59|Persistent Storage|survives power loss|term
C60|Consistency|data not corrupted under failure|term
C61|Transaction|atomic multi-change unit|term
C62|Replication|copies of data to other nodes|term
C63|SLO|service level objective; ideal=100%|term
C64|SLA|service level agreement; ideal=no downtime|term
C65|SLI|service level indicator; alert thresholds incl degraded|term
C66|Force Multiplier (auto)|automation cuts problems efficiently AND cuts you efficiently|principle

# axes(id|low_pole|high_pole|applies_to)
A1|Unknowable|Knowable|info,real-things,virtual-things,logic
A2|Real|Virtual|all-things
A3|No Control|Total Control|environments
A4|Generalization|Specificity|communication
A5|Application Logic|Operational Logic|code
A6|Decentralized|Centralized|systems
A7|Not Atomic|Atomic|operations
A8|Slow|Fast|performance
A9|Not Available|Completely Available|services
A10|Dangerous|Safe|changes
A11|Difficult|Easy|operations
A12|Opaque|Clear|visibility
A13|Cant Scale|Can Scale|architecture
A14|Aggregated|Comprehensive|systems
A15|Wisdom|Intelligence|judgment(orthogonal,not-spectrum)

# distinctions(id|name|side_a|side_b|key_asymmetry)
D1|Real-vs-Virtual|Real|Virtual|Real never fully knowable; Virtual data fully knowable
D2|Data-vs-Logic|Data|Logic|Data knowable+durable+portable; Logic unknowable+env-bound+goal-bound
D3|Comprehensive-vs-Aggregated|Comprehensive|Aggregated|Comp owns whole space subdivides; Agg only covers built parts
D4|OpsLogic-vs-AppLogic|Operational|Application|OpsLogic assumes failure resilient; AppLogic assumes env works exits clean
D5|Best-vs-Better|Best|Better|Best=1 thing absolute hidden tradeoffs; Better=2 things explicit tradeoffs
D6|Push-vs-Pull|Push|Pull|Push centralized initiator; Pull decentralized targets fetch
D7|Centralized-vs-Decentralized|Centralized|Decentralized|Cent=control single-failure; Decent=resilience N-failure
D8|Sequential-vs-Parallel|Sequential|Parallel|Seq simple no-coordination; Par fast needs coordination
D9|Knowable-vs-Unknowable|Knowable Virtual|Unknowable Virtual|some virtuals fully inspectable some inherently not
D10|Understanding-vs-Control-Model|Understanding|Control|Und=disposable approximate; Ctl=lifetime-accurate-synced
D11|Personal-vs-Hearsay|Personal Experience|Hearsay|PE=verified-by-self; HS=trust-chain-with-failure-modes
D12|Insider-vs-Outsider|Member|Non-member|first-tier security boundary

# rules(id|name|statement|apply_when|skip_when)
R1|90-9-0.9%|each priority tier 10x more important than next|making prioritized decisions|trivial choices
R2|0-1-Infinity|no 2; only 0 or 1 or N instances|architecture decisions|never
R3|Idempotency|operations converge to desired state regardless of start|writing automation|cant skip;always desirable
R4|IOSE/Universal Machine|model anything as Inputs+Outputs+SideEffects|systemic analysis|never
R5|Slicing the Pie|subdivide preserving whole no info loss|comprehensive design|aggregating-known-acceptable
R6|AAA|Authenticate Authorize Account|access control|never
R7|Win-Win-Win|engineer for self+org+external benefit|all decisions|never
R8|Data Primacy|treat data as truth logic as replaceable shell|architecture|never
R9|One-Way-To-Do-It|single canonical method per task category in prod|prod environment|dev/experiment
R10|Local Caching for OpsLogic|cache deps locally so partition doesnt break ops|operational logic|never
R11|Min Dependencies for OpsLogic|fewer libs/services/frameworks=fewer failure modes|operational logic|app-logic-may-differ
R12|Verify Personally|prefer self-verified info over hearsay|troubleshooting+decisions|when-already-verified
R13|Explicit Priority Reorder|state when youre changing default priorities|team decisions|solo-quick-decisions
R14|No Logic in Data Store|keep stored procs/triggers minimal-or-zero|schema design|portability-not-needed
R15|Constraints On|use FK/check constraints unless perf forces off|relational schema|measured-perf-block
R16|Population Stats Only|stats valid for groups not individuals|capacity planning|individual-prediction-impossible

# claims(id|claim|type|deps)
K1|Operations is fundamentally about control|axiom|C2
K2|Without control no other efficiency possible|derivation|C2
K3|Reality is not fully knowable; virtual data is|axiom|C5,C6,A1
K4|Data is more trustworthy than Logic|axiom|D2,A1
K5|Logic without Data context is meaningless|derivation|C8,C9
K6|Goals change frequently; Logic dies with goals; Data survives|observation|C8,C9
K7|Tool-Logic outlives goal-Logic because data drives it|derivation|K6,C9
K8|Aggregated systems trend toward inconsistency|observation|C18,C23
K9|Comprehensive systems trend toward consistency|observation|C17,C23
K10|No 2 in scaling; either 0 or 1 or N|axiom|R2
K11|Best is rarely valid; Better is the working unit|prescription|D5,C25,C26
K12|Operational Logic and Application Logic differ in priorities not quality|observation|D4
K13|Production Environment is logically one machine (DOS)|reframe|C35,C29
K14|Idempotency makes automation safe to re-run|axiom|R3
K15|All monitoring data is aged; never truly Now|observation|C41
K16|You can predict population stats not individual events|observation|R16
K17|Models for control must stay synced with reality forever|prescription|C39
K18|Personal verification beats hearsay even from authoritative sources|prescription|C47,C48,R12
K19|Each Class of Work removed eliminates a scaling tax|prescription|C3,C4
K20|Manual data-entry breeds errors regardless of vigilance|observation|C3
K21|Automation amplifies both fixes and failures|observation|C66
K22|Press-release engineering blogs are not engineering|prescription|C27,C28
K23|Internal Consistency is prereq for Alignment; not equivalent|distinction|C22,C23
K24|Best Practices should be read as Example Implementations|reframe|C28
K25|Putting Logic into Data Source corrupts the Knowable space|prescription|C54,D2
K26|Ops staffing/priority lags revenue-criticality of ops|observation|C29,C1
K27|Generic advice fails unique contexts|axiom|C49
K28|Less work tomorrow than today is the discipline|prescription|C3,C19

# examples(id|domain|setup|key_lesson|illustrates)
E1|HTTP-alert-triage|alert=HTTP test failure; team guesses causes|verify personally before deprioritizing|R12,C47,C48
E2|stored-X=5|X=5 then check X==5|virtual data fully knowable|K3,C8
E3|word-idea|trace etymology+usage of "idea"|some virtuals never fully knowable|K3,C6
E4|halting-int-main|return 1; from main|some logic high-confidence-halts|C58
E5|Python-decorator|@decorator changes Hello to Goodbye|logic complexity hides behavior|C9,K3
E6|temp-sensors-on-server|N sensors approximate but never full state|real things only approximated|K3,C5
E7|rack-vibration|no sensors=no data even if data matters|unknown unknowns in real|C5
E8|password-file-as-music|/etc/passwd→audio frequencies|data is repurposable|C8
E9|FK-constraint-broken-by-Logic|valid 5000 in 0-4B field; Logic expected 0-100|valid data can break logic|D2,K4
E10|JVM-heap-50x|misread field→50x memory→service fail|Logic-Data drift consequences|E9,K4
E11|log-rotation-missing|disk fills→HTTP fails|systemic chain visible to good model|C11,C55,K9
E12|seq-SCP-100-servers|sequential push doesnt scale|R2 0-1-Infinity in practice|R2,E13
E13|push-vs-pull-deploy|parallel-push vs LB+HTTP-pull|axes-based decision: pull scales 0.75 push 0.5|R1,C20,A6,A13
E14|Master-Replica-failover|app fails until ops fixes IP/DNS|AppLogic priorities differ from OpsLogic|D4,C32,C31
E15|disk-MTBF-population|cant predict this disk; can predict N disks/month|stats valid only for populations|R16,K16
E16|ensure-directory-yaml|YAML→ensure path+mode+user+group|idempotent state-convergence|R3,C36
E17|iterate-yaml-list|loop+EnsureDir per file|composing idempotent ops|R3
E18|Black-White-vs-Duck-Goose|opposites can be more similar than unrelated pairs|knife reveals diffs hides similarities|C15
E19|kernel-vs-user-vs-firmware|same OS sliced differently|multiple valid slicings of same system|C15,C11
E20|recursive-scales-imagery|nested balance scales for decisions|impersonal weighing of axes|C24,R1
E21|availability-100-vs-perf-90|10% gap→5x perf can flip decision|10x gap needed for unambiguous priority|R1
E22|availability-90-vs-perf-9|10x gap; 100x perf needed to flip|caching-tier emerges from analysis|R1,E21
E23|book-word-section-stats|self-tracking convergence to estimate|stats useful even on personal-population|R16

# relationships(from|rel|to)
C2|enables|C1
C3|is_strategy_for|C2
C4|target_of|C3
C5|opposes|C6
C8|subset_of|C6
C9|subset_of|C6
C9|operates_on|C8
C8|primary_over|C9
C18|opposes|C17
C16|implements|C17
C15|enables|C16
C17|requires|C23
C22|requires|C23
C22|superset_of|C23
C23|prereq_of|C22
C12|implements|C13
C14|uses|C12
C42|uses|C12
C31|opposes|C32
C31|requires|C36
C31|requires|R10
C31|requires|R11
C29|instance_of|C30
C35|reframe_of|C29
C33|property_of|C29
C25|opposes|C26
C27|instance_of|C28
C28|anti_pattern_of|C19
C20|aggregates_into|C21
C21|enables|C24
R1|implements|C21
R2|constrains|C34
R3|property_of|C9
R8|derives_from|D2
R8|derives_from|K4
C44|orthogonal_to|C45
C45|enables|C46
C47|primary_over|C48
C49|primary_over|C27
C51|caused_by|C53
C52|sometimes_correct_form_of|C51
C54|violates|R8
C54|violates|D2
C55|symptom_of|C18
C66|property_of|C3
C36|enables|C3
C39|requires|C40
C41|limits|C39
C58|instance_of|A1
D1|grounds|D2
D2|grounds|D4
D3|grounds|R5
D5|grounds|R13
D6|instance_of|D7
D8|instance_of|D7
K1|root_of|book
K3|grounds|K4
K4|grounds|R8
K6|grounds|K7
K10|grounds|R2
K12|grounds|D4
K17|grounds|R3
K20|grounds|K19
K21|grounds|R11
K23|clarifies|C22

# chapter_index(ch|title|concepts)
1|Foundations of Operational Thinking|C1,C2,C3,C4,C26,K1,K2,K26
2|Real vs Virtual|C5,C6,C7,C8,C9,C47,C48,C49,A1,A2,D1,D9,D11,K3,E2,E3,E6,E7
3|Data is King Logic is Shell|C8,C9,C10,C54,C58,C59,C60,C61,C62,D2,K4,K5,K6,K7,K25,R8,R14,R15,E4,E5,E9,E10
4|What is a System|C11,C12,C13,C14,C55,E11,E19
5|Systemic Thinking|C12,C13,C14,C15,C16,C17,C18,C42,D3,K8,K9,E18
6|Axiomatic Engineering|C19,C20,C21,C24,C25,C26,C27,C28,C43,A4,D5,K11,K22,K24,R1,R7,R13,E20,E21,E22
7|Humans|C50,A4
8|Operational Environments|C29,C30,C56,R6
9|OpLogic vs AppLogic|C31,C32,C33,C66,A5,D4,K12,R10,R11,E14
10|Scaling and Control|C34,C35,K10,K13,R2,E12
11|Evaluating Changes|C20,C21,C51,C52,C53,A6,A13,D6,D7,D8,R1,R13,E13
12|Algorithmic Properties|C36,R3,E16,E17
13|Know the Present|C37,C38,C39,C40,C41,K15,K16,K17,R16,E15,E23
14|Engineering Your Path|C22,C23,C44,C45,C46,C63,C64,C65,K23,R7,E11

# decode_legend
rel_types: enables|opposes|grounds|subset_of|superset_of|prereq_of|requires|operates_on|primary_over|implements|reframe_of|instance_of|property_of|symptom_of|caused_by|violates|orthogonal_to|root_of|aggregates_into|constrains|limits|target_of|is_strategy_for|anti_pattern_of|clarifies|sometimes_correct_form_of|uses
claim_types: axiom|derivation|observation|prescription|reframe|distinction
concept_categories: principle|axis|rule|distinction|tool|anti-pattern|term
