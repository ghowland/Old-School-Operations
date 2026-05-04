# WHAT ENGINEERING IS + WHAT ENGINEERING TRUE COST IS — LLM-COMPACT FORM
# Combined compaction of ENG-1 and ENG-2; one structural argument across two papers
# Format: pipe-delimited tables, ID refs.
# Read order: principles → definition → clauses → removal-tests → true-cost → adjacent → paxos-raft → substrate-arg → software-examples → industry-implications → org-tests → tc-domains → traditional-credentialing → software-substrate → substrate-churn → credentialing-problems → cost-magnitude → crossover → crossover-structural → internal-vs-external → thousand-engineers → certifier → regimes → two-role → three-tiers → tier-examples → resolved-confusions → practical-consequences → relationships → sections

# principles(id|principle|rationale)
T1|Engineering identified by what activity does not who performs+tools+credentials|structural definition; lets reader walk into any role and ask small set of questions to determine if work is engineering
T2|Five clauses+True Cost qualifier are minimal|each clause necessary; removing any admits non-engineering or excludes real engineering
T3|True Cost asymmetry is structural|engineer makes decisions on behalf of people who pay if decisions are wrong; this asymmetry creates the ethical obligation
T4|Most "software engineers" are not doing engineering by this definition|skilled trades work — execution against forgiving substrates with internal cost surfaces; valuable but title borrows prestige of word that meant something specific elsewhere
T5|True Cost is not one thing|harm lands in different domains with structurally different properties; binary treatment sufficient for boundary not for credentialing question
T6|Credentialing follows cost domain not activity|where cost is physical/civilizational society credentials person+output; where bounded+reversible market handles; where software produces traditional-tier costs society certifies system via domain expert
T7|Substrate stability is what makes person-credentialing work|stable body of knowledge testable+portable competence+accumulated formal codes; all three required
T8|Software substrate is engineered by other software engineers who keep changing it|no stable body of knowledge+no portable competence+no formal codes; person-level credentialing structurally impossible for general software work
T9|Software is internally consistent first crossover-to-reality second|inverse of bridge engineering; certification must attach to system not person because system is unit that has internal consistency
T10|Two engineering activities in crossover work|software engineer builds system+domain engineer certifies output; both real engineering; different bodies of knowledge required
T11|Same engineer crosses tiers across career|tier follows the work not the person; framework handles this because activity not role is the unit
T12|Calling things by their right names lets organizations make better decisions|engineering is specific activity; conflation produces dysfunction; precise definition is a tool

# definition(aspect|content)
DEF1|canonical|Engineering is evaluating trade-offs to find alignment of variables and constants that efficiently meet goals against externalities where failure has a True Cost
DEF2|qualifier|True Cost is harm borne by goal-seekers and users when the engineered system fails
DEF3|status|every word load-bearing; two sentences are entire definition; remainder is exposition

# clauses(id|clause|role|excludes_if_dropped)
CL1|evaluating trade-offs|the activity proper; distinguishes from execution|becomes execution — skilled trades work applying decisions made by others
CL2|alignment of variables and constants|what evaluation seeks; configuration of system parameters such that system actually achieves goals under constraints|no mechanism connecting decisions to outcomes; activity becomes opinion or preference
CL3|efficiently|optimization criterion under resource constraints|brute force qualifies; throwing more hardware at problem until it goes away counts
CL4|meet goals|direction; teleology; engineering serves goals set by others|activity has no direction; structure-fitting without purpose
CL5|against externalities|substrate that pushes back; reality that activity must contend with|self-contained; pure mathematics qualifies
CL6|where failure has True Cost|qualifier excluding academic work; loads consequences onto parties outside the activity|academic work qualifies; simulation+textbook+research-prototype with bounded internal consequences

# removal_tests(clause|removed|becomes)
RT1|CL1|drop evaluating trade-offs|execution / skilled trades work
RT2|CL2|drop alignment|opinion / preference
RT3|CL3|drop efficiently|brute force qualifies
RT4|CL4|drop goals|structure-fitting without direction
RT5|CL5|drop externalities|pure mathematics
RT6|CL6|drop True Cost|academic work
# rule: five clauses+qualifier together pick out engineering precisely; none removable without admitting non-engineering or excluding real engineering

# true_cost(aspect|content)
TC1|definition|harm borne by goal-seekers and users when engineered system fails
TC2|asymmetry|cost lands outside engineering activity itself on parties who did not do the work and cannot fix it
TC3|engineer's exposure|reputation+employment+legal liability — but secondary; defining cost is borne by goal-seekers and users
TC4|ethical anchor|every traditional engineering discipline built professional ethics codes around this asymmetry; software has mostly avoided having such codes partly because industry has avoided admitting True Cost applies
TC5|canonical illustration|Therac-25 — software bugs in input handling interacted with physical machine state to deliver fatal radiation overdoses; misalignment of variables (interlock logic+race conditions) against externalities (machine state+patient bodies); True Cost paid by patients

# adjacent_activities(id|activity|distinction|example)
AA1|Math|open at level of theorems; no externalities+no True Cost|Lamport's Paxos+logical clocks+Byzantine generals — theorems about distributed computation proven in proof-space with internal-only consequences
AA2|Academic work generally|self-contained in consequences; wrong proof harms proof; wrong paper harms author's reputation; discipline corrects itself in own space|the academy is deliberate construction of environment where ideas can be wrong without external harm
AA3|Trades and craft|execution of decisions made by engineers; trade-offs not live for executor|cabler in datacenter+concrete pourer+rebar tier — skilled valuable often dangerous; accountable to specifications not externalities directly
AA4|Design|not separate category — design applied to substrate with True Cost is engineering; design applied abstractly is math; design applied to human aesthetic experience is its own thing|interior design+level design+graphic design — craft+skill+trade-offs but no substrate that pushes back with True Cost
AA5|Applied math|borderline that most clearly illustrates distinction|pure cryptography(math) vs applied cryptography(engineering — TLS+key management+Signal protocol); math doesn't change between two; activity around it does

# paxos_raft(aspect|content)
PR1|Paxos as published by Lamport|closer to math; proof object demonstrating consensus is possible under specific failure models
PR2|Raft by Ongaro and Ousterhout|engineering; same problem class; explicit goals were understandability+implementability with externality being human cognition+messiness of real implementations
PR3|why redesign|bad Paxos implementations had shipped and corrupted data; engineers were getting it wrong
PR4|both excellent|different activities; cleanest live example of math/engineering distinction in software
PR5|same protocol implemented in production|engineering again; possibly performed by someone who has never read academic literature but is responsible for system not corrupting customer data

# substrate_argument(aspect|content)
SA1|claim|substrate is necessary but not sufficient
SA2|textbook bridge problem|has substrate in problem statement but no one builds it+no one falls into river
SA3|Paxos for class|has substrate but if never deployed no decisions depend on correctness
SA4|both involve substrate|neither is engineering
SA5|True Cost closes gap|substrate has to bite; parties outside activity must pay if work is wrong; work must be done with that accountability in mind

# software_examples(id|example|what_engineered|externalities|true_cost|illustrates)
SE1|Engelbart NLS (1968 Mother of All Demos)|input device design+screen geometry+command structure+network protocols on SDS 940|human cognition+hardware limits(memory+latency+display bandwidth)+physics of remote video over leased lines|funding-level — if system did not work in front of audience research program lost credibility and support|engineering content sits behind the demo; choices about how to build a system humans could use to do real work
SE2|Mike Acton data-oriented design|data layout+access patterns+batch sizes aligned with cache lines+memory bandwidth|hardware as externality; 16ms frame budget|frame time; players experience stutter; hardware+human visual system bites|software designed to be elegant by programmer's taste rather than aligned with substrate is misaligned and pays True Cost; three lies(software is platform+code designed around model is good+code more important than data) are academic-style framings mistaken for engineering
SE3|Carmack Quake 1996 netcode|client-side prediction+lag compensation+snapshot delta encoding|modem latency+packet loss+dialup jitter|unplayable game and no sales|substrate(consumer dial-up) unforgiving and varied wildly across users; design choices have shaped game networking ever since
SE4|Dean+Ghemawat at Google (MapReduce+Bigtable+Spanner)|programming model aligned against thousands of commodity machines that fail constantly; transactional consistency model against clock skew across global datacenters via TrueTime|commodity-hardware failure rates+global clock skew|index does not get built+search degrades+revenue stops|academic version looks like Lamport; engineering version is deliberate restriction on what can be expressed chosen so system can recover from machine failures automatically
SE5|Thompson+Ritchie Unix and C|process model+file abstraction+syscall interface+language semantics|PDP-11 capabilities+Bell Labs workload+future hardware that did not yet exist|system has to be useful enough that Bell Labs keeps project alive+wider research community adopts|portability-via-C is textbook engineering trade-off — accept performance loss to align "what hardware can run this" against "hardware will keep changing"
SE6|Therac-25 (negative example)|interlock logic+input handling|physical machine state+patient bodies|patient deaths|misalignment of variables against externalities; canonical illustration of failed engineering when True Cost is large and visible

# industry_implications(id|implication|content)
IM1|Most "software engineers" are not engineering|skilled trades work — execution of patterns against forgiving substrates with internal cost surfaces; framework+language+architecture decided by others; daily work is implementing features within fixed walls; valuable but title borrows prestige
IM2|Senior ops actually engineering|substrate (production hardware+networks+real user load+real adversaries) bites; externalities real and fail constantly; True Cost lands directly on goal-seekers (business losing revenue) and users (people unable to access services); engineering whether or not person has degree
IM3|SWE velocity vs ops stability conflict|conflict between internal cost optimization and True Cost optimization; ops gates on True Cost; SWE leadership often optimizes against internal pressures (quarterly targets+productivity perception+manager career incentives) that don't connect to True Cost; ops position is engineering-correct by default
IM4|Engineering competence cannot be transmitted by coursework alone|controlling externalities under True Cost can only be learned where externalities punish error and consequences are visible; apprenticeship under cost pressure is historical mechanism; software has mostly skipped this with predictable results

# org_tests(id|test_subject|test_question)
OT1|is a role engineering?|is there a substrate+are trade-offs live+does failure cost goal-seekers or users? all three required
OT2|is a decision an engineering decision?|made against True Cost or against internal pressure laundered through engineering vocabulary? "we have to ship faster" rarely engineering; "ship faster or users leave for competitor" is — now real external cost to slowness
OT3|is org treating engineering as engineering?|does it staff+structure work so True Cost shapes priorities or does internal velocity override? orgs that consistently choose internal velocity over external stability have decided users' True Cost is acceptable collateral; free to make that decision but should make it knowingly

# tc_domains(id|domain|manifestation|reversibility|examples)
TCD1|Physical and civilizational True Cost|physical harm+civilizational disruption; people die directly(bridge+building+pressure-vessel+medical-device+aircraft) or indirectly(power-fail→hospitals+water-treatment-fail+transportation-fail+communications-fail); civilization itself disrupted(trains+work+supply-chains)|largely irreversible; dead people stay dead; starvation event leaves permanent damage; week-without-power has accumulated harm|asymmetry severe and structural — engineering decision in minutes by one person; cost in lives across populations across time
TCD2|Financial and service-availability True Cost|financial harm to organizations+degradation of services to users; companies die(Friendster+MySpace+Digg+startups); services degrade(outage cost per minute+slow pages drive users to competitors+broken flows damage trust); data loss catastrophic per-user but usually recoverable|largely reversible; businesses recover from outages+users re-acquired+data restored+trust rebuilt; partial reversibility(business that dies stays dead+lost user hard to win back)|nobody dies because req/s went up

# traditional_credentialing_substrate(id|condition|content)
TR_S1|stable body of knowledge testable|PE exam in 1995 tests largely same competence as 2026 because underlying engineering hasn't changed; new chapters added to codes but foundation intact
TR_S2|portable competence|licensed structural engineer designs bridge in California and different bridge in Texas using same skills; competence transfers because substrate is shared; license certifies skill genuinely the engineer's not tied to specific project or employer
TR_S3|accumulated formal codes|IBC+ACI+AISC+ASCE-7+NEC+IEC+ASHRAE+ASME and dozens others; written standards codifying body of knowledge; engineers tested against them; outputs evaluated; failures investigated; codes are formal anchor

# traditional_credentialing_must(aspect|content)
TR_M1|cost-magnitude argument|society credentials professions when cost magnitude justifies overhead of credentialing
TR_M2|apparatus is expensive|licensure boards+examination bodies+continuing education+professional liability+disciplinary boards+code-development orgs+peer review+insurance regimes+legal frameworks assigning liability
TR_M3|why society pays|alternative is worse — without credentialing asymmetric+irreversible nature of physical/civilizational True Cost falls on public without mechanism to anchor accountability; with credentialing licensed engineer has skin in the game
TR_M4|conditions all hold for traditional engineering|do not hold for software in general

# substrate_churn(year|stack)
SCH1|1999|Solaris+Linux 2.2+Windows NT+Perl+C++ +Java 1.2+PHP 4+mod_perl+Apache 1.3+MySQL 3.23+MS SQL Server 7+raw sockets+CGI+IRC+mailing lists+manual deploys+FTP+Slackware
SCH2|2010|Linux 2.6+Solaris dying+Windows Server 2008+Python 2.6+Ruby on Rails+Java 6+PHP 5.3+Nginx+MySQL 5+PostgreSQL 9+EC2+S3+Memcached+jQuery+IRC+Skype+Subversion fading to Git+REST APIs+JSON
SCH3|2026|Linux 6.x+Windows Server still around+Rust+Go+TypeScript+Python 3.13+Kubernetes+AWS+GCP+Azure+Terraform+gRPC+Kafka+Slack+Git+GitHub Actions+language models in toolchain+ephemeral containers+serverless functions
# observation: 1999 engineer's Perl mod_perl+Apache module expertise essentially worthless in 2026; 2010 engineer's Rails 3 plugins+EC2 classic networking largely obsolete; 2026 engineer's Kubernetes+AWS service catalog will be substantially obsolete by 2035; not unusual amount of churn — normal pace

# credentialing_problems(id|problem|content)
SC1|No stable body of knowledge to test against|credential earned against 1999 substrate substantially obsolete by 2010 and almost completely obsolete by 2026; whatever credential tested would not predict competence at later dates; not flaw in credential design but structural fact about software substrate
SC2|Fundamentals tested only|some attempts test algorithms+data structures+software design principles+computer organization; stable but nearly useless as measure of professional competence at building current systems; necessary but nowhere near sufficient
SC3|Stack-specific certifications|AWS Solutions Architect+Kubernetes Certified Administrator+vendor certifications useful as job-market signals but go obsolete on faster timescale than credentials they're supposed to be analogous to; PE doesn't have this problem because steel doesn't deprecate; Kubernetes does
SC4|Non-portable competence|same engineer in same role at same company in 1999/2010/2026 was doing different work; competence at one moment doesn't transfer cleanly to another within same person's career; two software engineers with same years of experience often have entirely non-overlapping skill sets
SC5|Why hiring relies on interviews|market figured out credentials don't predict performance; body of knowledge has moved by time credential is being relied on
SC6|No formal codes|civil has IBC+ACI+AISC+ASCE-7; electrical has NEC+IEC; mechanical has ASME; software has books+conference talks+blog posts+tribal knowledge+fragmented landscape of style guides that often contradict; no equivalent of "wiring must conform to NEC 2023" for software architecture; can't exist in same form because substrate too fluid

# cost_magnitude_argument(aspect|content)
CM1|other half of the case|even if software credentialing could be made to work technically society doesn't need it for most software work because costs don't justify overhead
CM2|most software work in business tier|failed startup is economic loss+degraded SaaS is inconvenience+buggy mobile app annoys+slow website costs page views+broken e-commerce loses sales; real but bounded+mostly reversible+not mortality-bearing
CM3|market handles competence assessment|reputation+interview performance+code samples+portfolios+track records+references+employment history+GitHub+open source+trial periods+probationary employment+performance reviews+firing; messy and unfair but calibrated to cost magnitudes involved
CM4|consistent pattern|society credentials physicians+lawyers+civil engineers because errors kill or imprison or impoverish; does not credential web developers because failed websites are economic problem not mortality problem; credentialing follows mortality and severe civilizational cost
CM5|not deficiency in field|accurate match between field's actual cost structure and social infrastructure that makes sense around it; software engineers not denied credentials because field immature — not credentialed because costs don't justify overhead and substrate won't support model anyway

# crossover(id|domain|failure_mode)
CO1|Autonomous vehicles|deciding between collision outcomes — when crash unavoidable software is choosing who gets hit and how; failure mode is mortality
CO2|Medical devices|pacemakers+infusion pumps+insulin pumps+implantable defibrillators+surgical robots+radiation therapy controllers; failure mode is patient harm or death
CO3|Avionics software|flight systems+navigation+autopilot+fly-by-wire; failure mode is aircraft loss with passengers and crew
CO4|Industrial control systems|chemical processes+refineries+power generation+water treatment; failure mode is industrial accidents that kill workers and surrounding populations
CO5|Grid management software|dispatching power+balancing load+managing failover; failure mode is blackouts cascading into hospital backup failures+traffic system failures+broader civilizational disruption
CO6|Industrial process control|manufacturing systems whose failure can level facilities or release toxic materials

# crossover_structural(id|reason|content)
CS1|Software competence not portable across crossover domains|engineer with automotive collision-avoidance experience not by virtue of that qualified for pacemaker firmware; substrates+failure modes+regulatory contexts+timing constraints+validation methods all different; two crossover-tier domains share less than two civil engineering specialties because underlying substrate of each is the specific engineered substrate of specific product not shared physical reality
CS2|Software internally consistent first crossover-to-reality second|inverse of bridge engineering; bridge's engineering fundamentally about relationship with physical reality+internal structure exists in service of external interface; software internal consistency dominates external interface in terms of where engineering effort goes — pacemaker firmware spends most complexity on state machines+error handling+protocols+config+diagnostics+telemetry+update mechanisms+watchdogs+fault tolerance+redundancy management; only small fraction touches actual cardiac pacing decision
CS3|Certification has to attach to system not person|system is unit that has internal consistency; system is what crosses to reality at specific points; system is what makes specific decisions in specific contexts; certifying person is certifying something that doesn't predict next system's correctness

# internal_vs_external(aspect|bridge|software)
IE1|primary engineering concern|relationship with physical reality (loads+wind+soil)|internal consistency (state machines+protocols+error handling)
IE2|where complexity lives|external interface dominates|internal logic dominates; external interface is small fraction
IE3|substrate constraint|underlying physics constrains solution space heavily|internal consistency demands choices that don't generalize
IE4|implication|internal organization follows from external relationship; bridge that matches loads is right and internal structure follows|engineer's competence at making that specific system internally consistent determines correctness
IE5|certification target|person (PE) — competence portable across bridges|system — competence not portable across systems

# thousand_engineers(aspect|content)
TH1|civil case|thousand civil engineers designing same bridge for same site converge on similar broad shapes because underlying physics constrains solution space heavily; bridge from one engineer recognizably similar to bridge from another
TH2|software case|thousand software engineers designing same crossover system would produce thousand wildly different architectures with different state representations+error handling philosophies+module decompositions+testing approaches+concurrency models+update strategies
TH3|why variation|not sign of immaturity or lack of discipline; structural feature of software as substrate; internal consistency demands choices that don't generalize and choice space enormous
TH4|consequence|two competent software engineers presented with same problem will produce systems differing in ways that matter for correctness because their internal-consistency choices were different from start

# certifier(aspect|content)
CR1|certifier must be domain-credentialed traditional engineer|not a software engineer
CR2|crossover certification asks|does this system make correct decisions when it touches reality at this point?
CR3|answering requires domain expertise|knowing what "correct" means in domain — correct cardiac pacing across patient populations+correct collision-avoidance across road conditions+correct process management across input variations
CR4|software engineer can verify internal consistency|run tests+formal methods+simulations+fuzzing+property-based testing; verify code does what they meant; cannot reliably verify whether what they meant is correct in domain
CR5|domain expertise lives in traditional engineering credential|biomedical engineer/cardiac physiologist who built medical devices for decades knows correct pacemaker behavior; aerospace engineer with avionics experience knows correct autopilot behavior; chemical engineer with process control knows safe operation
CR6|why not software engineer|certifying crossover software is being asked to certify something outside their competence; can certify code is well-constructed+well-tested+internally consistent; cannot certify decisions are correct in medical/chemical/civil domain
CR7|inefficiency of teaching SWEs domain|would have to teach medicine+chemistry+traffic engineering; more efficient to take existing domain expert and give them software systems literacy than to take SWE and teach domain expertise from scratch

# regimes(regime|domain|certifier|certifies)
ER1|DO-178C|avionics|aerospace engineers+human-factors specialists with software engineers contributing to technical review|software development process+verification artifacts+resulting code; airworthiness call by domain experts
ER2|FDA 510(k)+PMA|medical devices|physicians+biomedical engineers|device including its software for specific indications
ER3|ISO 26262|automotive functional safety|safety engineers credentialed in functional safety+automotive systems|system+development process; final call by domain experts
ER4|IEC 61508|general industrial functional safety|domain-credentialed safety engineers|system+development process
# pattern: domain experts certify with software expertise contributing; regulatory regimes already converged on output-certification model for crossover work and on domain-engineer-as-certifier; framework names what they discovered

# two_role(role|activity|competence|accountability)
TM1|Software engineer|builds the system; evaluates trade-offs in software construction against externalities (system behavior+performance+failure modes+operating environment+validation requirements) with True Cost on whether system works|internal-consistency knowledge — language+framework+system design+validation methods+testing+debugging+deployment+maintenance|professional accountability flows through employment+professional standing; faces consequences if work fails but does not hold formal regulatory accountability for safety claim
TM2|Domain engineer|certifies the system; evaluates trade-offs in domain risk against externalities (substrate the system touches — patient population+road conditions+process dynamics+airframe — and failure modes at software-substrate boundary) with True Cost on whether certification is sound|substrate knowledge — physics+biology+chemistry+physiology of domain+failure modes+operating conditions+codes+standards|PE or equivalent credential is formal anchor of certification; license on the line if certification is wrong
# both real engineering by structural definition; different engineering activities; require different bodies of knowledge; together produce certified output
# accountability chain runs through certifier — when system fails in production and causes harm certifier (domain-credentialed engineer who signed off) and manufacturer (whose process produced system) are formally accountable
# software engineer claim narrower — "this code does what I intended it to do" — may have been correct even when system failed because intent was wrong in domain

# three_tiers(tier|cost_domain|substrate|credentialing_target)
TI1|Traditional engineering|physical and civilizational|stable|the person then the output via stamps; chain of accountability runs through licensed engineer
TI2|Business engineering|financial and service-availability|unstable rapidly evolving|none; market handles competence assessment via reputation+interviews+employment; correct because substrate moves too fast to support credentialing+cost magnitudes don't justify overhead+market handles adequately
TI3|Crossover engineering|traditional (mortality+civilizational disruption) reached via software|the specific engineered system with its own internal consistency requirements|the output (system) certified by domain-credentialed traditional engineer with software systems literacy; SWE who built system is doing real engineering but not individually credentialed for safety claim; domain engineer holds formal accountability through domain credential

# tier_examples(aspect|content)
TX1|same engineer crosses tiers|Tuesday writing Django web app — business tier no credential needed; Wednesday writing pacemaker firmware — crossover tier working within domain-engineer certification regime; Thursday back on Django app
TX2|tier follows the work not the person|framework handles this because activity not role is the unit
TX3|where general SWE credentialing has structurally failed|substrate doesn't support+cost structure doesn't warrant; will continue to fail
TX4|where regulated software domains evolved|toward output certification by domain experts; only credentialing model that fits structural facts

# resolved_confusions(id|question|resolution)
RC1|Why don't software engineers have a PE?|substrate doesn't support PE-style person-level credentialing for general software work and costs don't warrant it; where software is at PE-cost magnitudes (crossover) appropriate target is system not person and credentialed person is domain engineer not software engineer; absence of software PE is structurally correct
RC2|Should software engineers have professional ethics codes like other engineers?|codes that matter follow True Cost; for business tier ethics bounded by employment+contract+reputation; for crossover ethics flows through certification regime (DO-178C+FDA+ISO 26262 carry ethical weight); SWEs need to operate within existing domain-specific ethics frameworks when work crosses; for most work normal professional+contractual ethics suffice
RC3|Why have IEEE certifications and ABET-accredited SWE programs failed to achieve PE-equivalent status?|trying to credential something that can't be person-credentialed at level of rigor a PE represents; substrate moves too fast+competence not portable+codes don't exist in formal sense; credentialing bodies attempting structurally impossible task; credentials they produce weak because what they're trying to certify isn't right unit
RC4|Should self-driving car SWEs be licensed?|system should be certified not engineers; certifier should be domain-credentialed traditional engineer (automotive functional-safety engineer+transportation engineer+vehicle dynamics specialist+hybrid) with adequate software systems literacy; SWEs building system doing real engineering held to high standards but formal safety claim about output belongs to domain certifier; ISO 26262 already implements this model
RC5|Should AI safety engineers be licensed as field grows?|where AI systems make decisions at traditional-tier cost magnitudes systems should be certified by domain-credentialed engineers in relevant domains (medical AI by physicians+biomedical engineers; autonomous-systems AI by relevant domain engineers); AI software engineers building systems doing real engineering at crossover magnitudes when work touches these domains but not right party to hold safety claim; claim belongs to domain engineer who can evaluate whether system's behavior is correct in their substrate
RC6|Why do tech-industry comp systems pay "software engineers" so well if most aren't doing real engineering?|market paying for what SWEs actually produce — business engineering+crossover engineering value — not because title accurately describes what most do; compensation reflects financial value work creates and protects which is real even when work in business tier; title carries borrowed prestige; compensation calibrated to market value not to title accuracy; both can be true

# practical_consequences(id|situation|consequence)
PC1|Typical web/mobile/backend/application work|business tier; may or may not be engineering in strict sense (depends on whether evaluating live trade-offs against substrates that push back with True Cost on parties outside work); often you are; sometimes closer to skilled trades work; either way no credentialing needed and none meaningfully available; market handles competence via interviews+performance reviews+employment+reputation; not failing profession by not having license; nothing to license
PC2|Crossover work (automotive+medical+aerospace+industrial control+grid+anything mortality-or-civilizational)|real engineering at traditional-tier cost magnitudes; held to structural criterion; code participates in certification regime where domain-credentialed engineer signs off on system's correctness in their domain; you are not person making safety claim and that's structurally correct because safety claim too big for any one SWE to make on own authority; depends on domain knowledge you don't have at level certifier has; your job is build system rigorously enough that certifier can do their job; you are an engineer in strict sense; you also do not personally hold safety claim; both are true
PC3|Considering whether SWE as profession should pursue PE-style credentialing|shouldn't and structurally can't for general software work; energy spent on these efforts could be better spent on tightening certification regimes that already exist for crossover work+improving software systems literacy of domain engineers who certify+developing better structural understanding of where software does and doesn't fit in broader engineering landscape
PC4|Working on software moving into traditional cost domains (AI medical diagnoses+critical infrastructure control+autonomous-system decision logic)|recognize you are entering crossover territory; work needs domain-engineer certification; if project doesn't have certification structure in place you are working without accountability anchor that should exist; structural problem with project not with you but problem to advocate to fix because absence of certification doesn't make True Cost smaller — just means cost being absorbed by users without protective infrastructure society normally builds around traditional-tier engineering

# relationships(from|rel|to)
T1|grounds|DEF1
T2|grounds|CL1+CL2+CL3+CL4+CL5+CL6
T2|implements|RT1+RT2+RT3+RT4+RT5+RT6
T3|grounds|TC2+TC3+TC4
T4|implies|IM1
T5|unfolds|TCD1+TCD2
T6|grounds|TI1+TI2+TI3
T7|requires|TR_S1+TR_S2+TR_S3
T7|justifies|TR_M1+TR_M2+TR_M3
T8|prevents|software-PE
T8|implies|SC1+SC4+SC6
T9|grounds|CS3
T9|grounds|IE1+IE2+IE3+IE4+IE5
T10|grounds|TM1+TM2
T11|enables|TX1+TX2
T12|frames|RC1+RC2+RC3+RC4+RC5+RC6
DEF1|composed_of|CL1+CL2+CL3+CL4+CL5+CL6
DEF2|qualifies|DEF1
CL1|distinguishes|engineering-from-execution
CL2|requires|alignment-mechanism
CL3|excludes|brute-force
CL4|requires|teleology
CL5|differentiates_from|AA1
CL6|differentiates_from|AA2
RT_ALL|prove|minimality-of-definition
TC1|equals|DEF2
TC2|creates|ethical-obligation
TC4|absent_in|software-historically
TC5|illustrates|failed-engineering-with-large-True-Cost
AA1|distinct_from|engineering-via-no-externalities-and-no-True-Cost
AA2|distinct_from|engineering-via-self-contained-consequences
AA3|distinct_from|engineering-via-trade-offs-not-live
AA4|conditional|design-with-substrate-and-True-Cost-IS-engineering
AA5|borderline|pure-math-vs-applied-engineering
PR1|exemplifies|AA1
PR2|exemplifies|engineering-with-human-cognition-as-externality
PR3|illustrates|why-redesign-was-engineering
SA1|grounds|SA5
SA5|distinguishes|engineering-from-exercise+simulation+study
SE1|illustrates|engineering-content-behind-vision
SE2|illustrates|substrate-alignment-as-primary-engineering-concern
SE3|illustrates|substrate-unforgiving-and-varied
SE4|illustrates|deliberate-restriction-as-engineering-choice
SE5|illustrates|trade-off-against-future-substrate-change
SE6|illustrates|TC5
IM1|consequence_of|T4
IM2|consequence_of|T1+CL5+CL6
IM3|consequence_of|TC1
IM4|consequence_of|substrate-cannot-be-learned-from-coursework
OT1|tests|whether-role-is-engineering
OT2|tests|whether-decision-is-engineering
OT3|tests|whether-org-treats-engineering-as-engineering
TCD1|magnitude_warrants|TR_M1
TCD2|magnitude_does_not_warrant|credentialing-overhead
TR_S1|enables|stable-PE-exam
TR_S2|enables|portable-license
TR_S3|enables|formal-anchoring
TR_M1|justifies|credentialing-apparatus-cost
TR_M3|absent|alternative-is-worse
SCH_ALL|demonstrates|substrate-churn
SC1|grounds|SC2+SC3
SC4|consequence_of|substrate-churn
SC6|grounds|no-formal-anchoring
SC_ALL|compound|to-make-software-credentialing-structurally-impossible
CM1|complements|SC1-substrate-impossibility
CM4|consistent_pattern|across-credentialed-professions
CM5|reframes|absence-of-software-credential-as-correct-not-deficient
CO_ALL|qualify|crossover-engineering
CS1|grounds|TI3-target-is-system-not-person
CS2|inverts|bridge-engineering-pattern
CS3|implements|T9
IE_ALL|elaborate|CS2
TH1|grounds|TR_S2
TH2|grounds|CS3
TH4|consequence_of|TH3
CR1|consequence_of|T9+CR3+CR4
CR4|distinguishes|internal-consistency-from-domain-correctness
CR6|grounds|CR1
CR7|justifies|domain-engineer-with-software-literacy-vs-SWE-with-domain-training
ER_ALL|exemplify|CR1
ER_ALL|converged_on|output-certification-by-domain-experts
TM1|requires|software-construction-competence
TM2|requires|domain-substrate-competence
TM_BOTH|together_produce|certified-output
TM2|holds|formal-regulatory-accountability
TI1|model|person-then-output
TI2|model|none
TI3|model|output-via-domain-certifier
TX1|illustrates|T11
TX2|implements|T11
RC1|resolved_via|T8+CS3
RC2|resolved_via|TC4+regime-specific-ethics
RC3|resolved_via|T8
RC4|resolved_via|CR1+TI3+ER3
RC5|resolved_via|CR1-extended-to-AI
RC6|resolved_via|market-pays-for-value-not-title-accuracy
PC1|placement|TI2
PC2|placement|TI3
PC2|implements|TM1
PC3|consequence_of|T8+SC_ALL
PC4|advocates|certification-structure-where-absent

# section_index(paper|section|title|ids)
ENG-1|1|Why this paper exists|T1
ENG-1|2|The definition|DEF1+DEF2+DEF3
ENG-1|3|Clause by clause|CL1+CL2+CL3+CL4+CL5+CL6
ENG-1|4|True Cost|TC1+TC2+TC3+TC4+TC5
ENG-1|5|Removal tests|RT1+RT2+RT3+RT4+RT5+RT6
ENG-1|6|Engineering versus adjacent activities|AA1+AA2+AA3+AA4+AA5+PR1+PR2+PR3+PR4+PR5
ENG-1|7|Why substrate alone is not enough|SA1+SA2+SA3+SA4+SA5
ENG-1|8|Examples in software|SE1+SE2+SE3+SE4+SE5+SE6
ENG-1|9|Implications for software|IM1+IM2+IM3+IM4
ENG-1|10|Implications for organizations|OT1+OT2+OT3
ENG-1|11|Closing|DEF1-restated-structurally
ENG-2|1|Why this paper exists|T5+T6
ENG-2|2|True Cost is not one thing|TCD1+TCD2
ENG-2|3|Why traditional engineering can be credentialed|TR_S1+TR_S2+TR_S3
ENG-2|4|Why traditional engineering must be credentialed|TR_M1+TR_M2+TR_M3+TR_M4
ENG-2|5|Why software engineering cannot be credentialed at person level|T8+SCH1+SCH2+SCH3+SC1+SC2+SC3+SC4+SC5+SC6
ENG-2|6|Why software engineering doesn't need credentialing|CM1+CM2+CM3+CM4+CM5
ENG-2|7|Crossover engineering|CO1+CO2+CO3+CO4+CO5+CO6+CS1+CS2+CS3+IE1+IE2+IE3+IE4+IE5+TH1+TH2+TH3+TH4
ENG-2|8|Who certifies crossover engineering|CR1+CR2+CR3+CR4+CR5+CR6+CR7+ER1+ER2+ER3+ER4
ENG-2|9|The two-role model|TM1+TM2+T10
ENG-2|10|The complete three-tier credentialing model|TI1+TI2+TI3
ENG-2|11|Why this resolves long-standing confusions|RC1+RC2+RC3+RC4+RC5+RC6
ENG-2|12|What this means for software engineers|PC1+PC2+PC3+PC4
ENG-2|13|Closing|T6+TI1+TI2+TI3-restated-structurally

# decode_legend
papers_combined: ENG-1+ENG-2
canonical_definition: Engineering is evaluating trade-offs to find alignment of variables and constants that efficiently meet goals against externalities where failure has a True Cost
true_cost_definition: True Cost is harm borne by goal-seekers and users when the engineered system fails
clause_count: 5 + 1 qualifier (True Cost)
tc_domains: physical-and-civilizational | financial-and-service-availability
tc_reversibility: physical=largely-irreversible | financial=largely-reversible
adjacent_activities: math|academic|trades|design|applied-math
software_examples: Engelbart-NLS|Acton-DOD|Carmack-Quake|Dean-Ghemawat-Google|Thompson-Ritchie-Unix-C|Therac-25(negative)
canonical_math_vs_engineering_example: Paxos(math) vs Raft(engineering) — same problem class different activity
substrate_stability: traditional=stable(50+yrs)|software=unstable(churn-every-decade)
credentialing_conditions: stable-body-of-knowledge|portable-competence|accumulated-formal-codes
crossover_domains: autonomous-vehicles|medical-devices|avionics|industrial-control|grid-management|industrial-process-control
existing_regimes: DO-178C|FDA-510(k)+PMA|ISO-26262|IEC-61508
two_roles: software-engineer-builds | domain-engineer-certifies
three_tiers: traditional|business|crossover
credentialing_targets: traditional=person-then-output | business=none(market) | crossover=output-via-domain-certifier
internal_vs_external_inversion: bridge=external-relational-first | software=internal-consistency-first
thousand_engineers: civil=converge(physics-constrains) | software=diverge(internal-consistency-choices)
unifying_principle: credentialing follows cost domain not activity
not_a_diminishment: trades+math+academic+design all valuable; engineering is one specific activity among many
software_pe_status: structurally impossible for general software; structurally inappropriate for crossover (output-certification by domain expert is correct model)
sot_for_engineering_identity: the activity not the title or credential
sot_for_safety_claim_in_crossover: domain engineer who certifies system not software engineer who built it
rel_types: grounds|implements|implies|requires|justifies|prevents|enables|frames|composed_of|qualifies|distinguishes|differentiates_from|exemplifies|illustrates|consequence_of|tests|magnitude_warrants|magnitude_does_not_warrant|absent|complements|consistent_pattern|reframes|qualify|inverts|elaborate|converged_on|together_produce|holds|model|advocates|placement|resolved_via|distinct_from|conditional|borderline|prove|equals|creates|absent_in|unfolds|requires_for_anchoring|reframes
