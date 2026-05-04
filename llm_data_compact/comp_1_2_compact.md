# IMPLEMENTING TALL-INFRA DATA-ONLY EXECUTION (SILO) + TALL-INFRA DATA-ONLY DEVELOPMENT — LLM-COMPACT FORM
# Combined compaction of COMP-1 (Silo implementation) + COMP-2 (architectural category)
# Format: pipe-delimited tables, ID refs.
# Read order: principles → definition → qualification → historical-walls → distinction → architecture → execution-funnel → shortcuts → entity → state-machine → prolog → utility-ai → logic-blocks → threading → scenes → networking → trace → silo-examples → anti-examples → litmus → when-to-use → disciplines → productivity → performance → memory → bottlenecks → implementation → limitations → comparisons → applicability → relationships → sections

# principles(id|principle|rationale)
T1|Tall-infra data-only inverts traditional development model|behavior resides in data structures infrastructure interprets; infrastructure compiles once+behavior changes involve only editing data tables; running system hot-swaps data and executes new behavior on next frame
T2|Marginal cost of new behavior approaches zero engineering time|comprehensive infrastructure provides all necessary primitives as pre-compiled operations; application developers compose primitives through data configuration never writing infrastructure code
T3|Universal Entity container; difference between dragon and chair is which fields contain data not what type they inherit from|all entities identical in structure differ only in which fields hold meaningful data; infrastructure doesn't check entity_type before executing logic; processes all entities identically
T4|No type hierarchy|no class Dragon extends Entity; entity is bag of bits with enforced structure — structure fixed (all entities same fields) but interpretation flexible (fields can be relabeled)
T5|Wall-less architecture|all fields public; no encapsulation+getters/setters+access control at entity level; any system can read/write any field; gating happens at scene level+via Prolog rules+via UtilityAI+via Logic Blocks
T6|Execution funnel reduces cognitive load at each layer|StateMachine → Prolog → UtilityAI → LogicBlock; each layer filters scope — designers think only about that layer's concerns; separation of concerns through funnel architecture
T7|Pure topology in state machines|states contain name+behavior set reference+transitions+optional forced action; no behavior logic in state machine itself; change behavior set → change combat behavior without touching state machine
T8|Multiplicative scoring with fail-fast|any consideration scoring 0 → entire behavior scores 0; if no weapon (consideration 1=0): 0×0.5×0.8=0
T9|Type safety without compilation|UI enforces structure at edit time+data structure validates+runtime never crashes; can write wrong logic cannot crash; invalid paths return defaults+math operations clamp
T10|DSP model — all workloads as pure data transformations|input array → transform → output array; no function calls between entities+no shared mutable state; perfect divisibility
T11|NUMA-aware threading with barrier synchronization|each thread owns independent data range+no locks+no sharing+no context switches+NUMA local; only sync point in frame is barrier
T12|Geometric security via fixed-size packets and path-based access control|architectural impossibility of buffer overflow+code injection+privilege escalation; achieved without sandboxing
T13|Default deny scene access|empty allow lists deny all access; both scene-id allow AND path-pattern match required; explicit whitelist for any cross-scene access
T14|Tall-infra bug = one-time fix benefits all consumers|vulnerability in infrastructure affects all games but fix once protects all; contrast with traditional where each game has different vulnerabilities and no shared infrastructure to fix once
T15|First-class debugging via decision traces|every decision logged per entity per frame; "why did entity 42 attack instead of flee at frame 1534?" becomes a query over decision history not breakpoints in code
T16|Hot-swap everything in one frame|state machines+behaviors+logic+networking rules all modifiable while running; data changes take effect next frame (16.67ms at 60 FPS)
T17|Tall-infra data-only is the entire vertical stack|from rendering to AI to UI to audio — no exceptions; "data-driven" has been industry standard for decades but always preserved a wall between data (assets+tuning values) and behavior (compiled code); tall-infra data-only eliminates this wall entirely
T18|Litmus test|can a designer add a "living market economy" without engineering? can stat.health be repurposed as bank balance with zero code change? can you swap every texture/sound/rule while executable runs? does the binary know any noun (goblin/sword/quest) exists?
T19|Infrastructure cost front-loaded; productivity multiplier permanent|the 1000th behavior set costs the same as the 10th; complexity remains constant because interactions are data relationships not code dependencies

# definition(aspect|content)
DEF1|data-driven|code owns the types data owns the numbers
DEF2|data-only|the binary forgets what a goblin is; the dataset teaches it every frame
DEF3|tall-infra data-only|the previous sentence is true from renderer to AI to UI to audio — no exceptions across the entire vertical stack
DEF4|core distinction|tall-infra data-only eliminates the wall between data and behavior entirely; behavior itself becomes data

# qualification(id|condition|content)
QC1|Zero gameplay types in binary|no class Goblin+no struct QuestReward+no enum FireSpell; compiled code contains infrastructure only — state machine runners+predicate evaluators+utility scorers+effect processors; does not know what game it is running
QC2|Behavior lives in hot-swappable data tables|state machines+AI decision curves+logic rules+stat modifications+event mappings all stored as table rows; change a row change the behavior; no recompilation+no restart required
QC3|Designers can invent new mechanics without engineers|not "tweak values" but "create new systems"; designer can use equipment-slot table to store camera FOV for security terminal+repurpose health stat as permission bitmap; cross-wiring existing tables creates emergent mechanics
QC4|Every subsystem consumes same uniform data layout|rendering+physics+AI+audio+UI+networking+save/load all read from same column-oriented tables with FK relationships; no special cases+no subsystem-specific formats

# historical_walls(era|engines|what_was_data|what_was_code|wall)
HW1|1990s|Quake+Half-Life|sounds+models+textures|AI routines+weapon behavior+level triggers|present
HW2|2000s|Unreal+Unity|meshes+prefabs+material parameters|gameplay classes+damage calculations+quest logic|present
HW3|2010s|Stingray+Overwatch ECS|entities+component values|AI behaviors+hero-specific abilities+system logic|present
HW4|2020s|Bevy+Unity DOTS|component columns+archetype definitions|systems that process components|present
# pattern: wall moved over decades but never disappeared; somewhere in binary lives compiled behavior — boss attack patterns+damage formulae+pathfinding heuristics+dialogue state machines

# architecture_layers(id|layer|role|position)
AL1|Entity|universal container holding all game objects+UI elements+system resources|input data
AL2|StateMachine|topological graph defining valid states and transitions|funnel layer 1 — what am I doing overall?
AL3|Prolog|declarative rule engine for preconditions and queries|funnel layer 2 — are preconditions met?
AL4|UtilityAI|multiplicative scoring system for behavior selection|funnel layer 3 — which behavior scores highest?
AL5|LogicBlock|stack-based bytecode for execution|funnel layer 4 — how do I execute this behavior?
AL6|Thread|NUMA-aware work distribution for parallel processing|cross-cutting (parallelism)
AL7|Scene|isolated execution context with access control|cross-cutting (isolation)
AL8|Networking|fixed-shape packets with geometric input isolation|cross-cutting (security)

# execution_funnel(step|layer|question|filter|result)
EF1|1|StateMachine|what am I doing overall? (Idle+Combat+Fleeing+Crafting+Dead)|from all possible behaviors → behaviors valid in current state|filtered behavior list
EF2|2|Prolog|are preconditions met? (has weapon? enemy in range? health sufficient?)|from state-valid → precondition-satisfied behaviors|gated behavior list
EF3|3|UtilityAI|which behavior scores highest?|from satisfied → single winning behavior|selected behavior
EF4|4|LogicBlocks|how do I execute this behavior? (set target+path to target+update position)|no filtering; just execution of winner|state mutation
EF5|5|Envelopes|automated stat transformation (DSP)|continuous effects applied|frame complete
# rule: full pipeline optional; state machines can bypass layers via shortcuts

# shortcuts(id|shortcut|bypasses|when)
SH1|force_action: .MeleeAttack|skip UAI, execute directly|simple direct action
SH2|exit_on_event: .PlayerAttacked|skip Prolog, transition immediately|external trigger
SH3|exit_condition_rule_name: "health_critical"|Prolog rule check|condition-based state changes
# rule: designers choose appropriate path based on complexity; simple behaviors use shortcuts; complex behaviors use full pipeline

# entity(aspect|content)
E1|fields|id+entity_type(metadata only)+name+state_machine_id+state+anim_state_machine_id+anim_state+transform+visual+movement+character+combat+container+audio+behavior+network+input+...20+ systems total+silo_field_replacement_id+is_active+is_deleted
E2|all systems optional|optional data fields with defaults; chair has combat=default values (unused); dragon has combat.damage=50
E3|no type hierarchy|all entities identical in structure; differ only in which fields hold meaningful data; infrastructure doesn't check entity_type before executing logic
E4|wall-less|all fields public; no encapsulation; gating happens at scene level+Prolog rules+UAI+Logic Blocks
E5|natural domains not enforced boundaries|animation SM typically modifies visual.current_animation but can also modify character.health if needed (death animation triggers health=0)

# field_replacement(aspect|content)
FR1|silo_field_replacement_id: i32 = -1|when set to valid ID references replacement table mapping field paths to alternative labels
FR2|example mapping|character.health → account.balance+character.stamina → account.credit_limit+character.xp → account.transaction_count+combat.damage → transaction.amount
FR3|same underlying data different semantic meaning|UI reads replacement table+displays "Account Balance: $5000" instead of "Health: 5000"; infrastructure doesn't care — still processes f32 value identically
FR4|use cases|game→business app(health=revenue+stamina=budget)+game→network monitor(health=uptime%)+game→database(stats=table statistics)+testing(rapidly prototype different domains without changing infrastructure)

# multiple_state_machines(aspect|content)
MS1|up to 14 SMs per entity|primary behavior+animation+audio+network+UI etc
MS2|each SM independent but coordinates through shared entity data|primary SM transitions to "Combat" sets entity.combat.attacking=true; animation SM checks entity.combat.attacking in Prolog rule; if true transitions to "Attack_Anim"
MS3|each SM can read/write ANY entity field|natural domains not enforced boundaries
MS4|enables separation of concerns without coupling|animation logic independent of behavior logic but both interact via shared entity data

# state_machine(aspect|content)
SM1|StateMachine fields|id+name+states[]+prolog_rule_set_a_id+prolog_rule_set_b_id (optional A/B testing)
SM2|StateMachineState fields|name+is_entry_state+behavior_set_id+transitions[]+force_action
SM3|StateMachineTransition fields|to+exit_on_event+exit_condition_rule_name+duration_min+delete_entity
SM4|states are pure topology|name identifying state+reference to behavior set (what to execute)+transitions to other states (graph edges)+optional forced action (bypass UAI)
SM5|no behavior logic in state machine|state "Combat" doesn't contain attack code; references behavior_set_id=5 which contains attack/block/flee behaviors
SM6|single function handles all state machines identically|no special cases for different entity types

# transition_mechanisms(mechanism|content|use)
TM1|Event-based|exit_on_event: .PlayerDied|when entity receives this event transition immediately|external triggers (damage received+item picked up)
TM2|Rule-based|exit_condition_rule_name: "enemy_nearby"|every frame evaluate Prolog rule; if all facts match transition|condition-based state changes (health<20%+enemy in range)
TM3|Duration-based|duration_min: 2.0|minimum time in state before any transition allowed|animations that must complete (attack animation 0.5s)
TM4|Combination|all conditions must be satisfied|event fires AND rule passes AND duration elapsed|complex transition gating

# prolog_use_cases(id|use_case|content|example)
PR1|State machine transitions|every frame check if rule passes; if true transition to next state|enemy_nearby :- has_target(X), target_distance(D), D < 100.
PR2|Utility AI considerations|if rule fails consideration scores 0; if passes compute score from distance curve|can_attack :- has_weapon(melee), target_distance(D), D < 5.
PR3|Logic block conditions|execute Prolog query branch based on result|if execute_prolog_rule("health_critical") then [SetValueInt, "state", "Flee"]

# fact_generation(aspect|content)
FG1|facts regenerated every frame from current entity state|generateEntityFacts reads basic facts(entity_type+in_state)+awareness facts(has_target+target_distance)+stat-based facts(health_critical+health_low)+equipment facts+position facts
FG2|Prolog queries match against current facts|ensures decisions based on up-to-date information
FG3|fact set examples|in_state(combat)+has_target(42)+target_distance(5.0)+health_low+has_weapon(melee)+at_position(vec2(100,200))

# prolog_advantages(id|advantage|content)
PA1|Reusable|same rule in state transitions+UAI+logic blocks
PA2|Composable|rules can reference other rules
PA3|Data-driven|rules in database+hot-swappable
PA4|Introspectable|can query "what rules would match if health=50?"
PA5|No syntax errors|rule structure validated+typos impossible

# utility_ai(aspect|content)
UA1|Consideration fields|prolog_rule_set_a_id+execute_logic_block_id+range+score_weight+curve+score_inverted
UA2|Behavior fields|name+considerations[]+execute_logic_block_id+execute_action+force_min_value+temp_score
UA3|BehaviorSet fields|name+behaviors[]+selection_method
UA4|deterministic by default|.top selection; can inject controlled randomness via .weighted_random_top3 for variety without chaos

# scoring_steps(step|action)
SS1|1|check Prolog rules if specified — fail fast (return 0.0) if rule fails
SS2|2|get input value from logic block or direct stat
SS3|3|normalize to [0,1] via (input - range.x) / (range.y - range.x); clamp
SS4|4|apply curve (Linear+InverseLinear+Quadratic+Exponential+Sigmoid+Boolean+...)
SS5|5|apply weight (curved × score_weight)
SS6|6|invert if needed (1.0 - score)
SS7|7|multiply into running score
SS8|8|apply average-and-fixup: count_f=considerations.len; mod_factor = 1.0 - (1.0/count_f); makeup = (1.0-running_score)*mod_factor; running_score = running_score + (makeup * running_score)
SS9|9|apply floor: if running_score < behavior.force_min_value then running_score = force_min_value

# scoring_properties(id|property|content)
SP1|Multiplicative with fail-fast|any 0 score collapses entire behavior to 0; "Attack" behavior with no weapon (consideration=0): 0×0.5×0.8=0
SP2|Average-and-fixup compensates|prevents many considerations from over-penalizing; running_score = running_score + (makeup * running_score)
SP3|Force minimum value floor|behaviors can't drop below specified threshold; gives baseline behaviors a chance
SP4|Curves shape input→score mapping|Linear=proportional+Sigmoid=sharp threshold+Boolean=binary gate

# curves(curve|shape)
CV1|Linear|t (proportional)
CV2|InverseLinear|1.0 - t
CV3|Quadratic|t * t
CV4|Exponential|(exp(t) - 1.0) / (e - 1.0)
CV5|Sigmoid|1.0 / (1.0 + exp(-10.0 * (t - 0.5)))
CV6|Boolean|if (t > 0.5) 1.0 else 0.0
# 20+ curve types total

# selection_methods(method|behavior)
SEL1|.top|deterministic — highest scoring behavior wins
SEL2|.weighted_random_top3|70% top1+25% top2+5% top3
SEL3|.random_reasonable|highest scoring (variation pending)

# logic_blocks(aspect|content)
LB1|stack-based bytecode|stack[256] of Value; each block manipulates stack
LB2|Turing-complete through composition|loops+conditionals+function calls+recursion all possible
LB3|fixed input/output types per block|MathAdd: (float,float)→float; LogicAnd: (bool,bool)→bool; MathVec2Length: (Vector2)→float
LB4|UI shows blocks compatible with current stack state|stack [float,float] enables MathAdd+MathMultiply+MathClamp+LogicEqual; not LogicAnd (needs bool)+not MathVec2Length (needs Vector2)
LB5|cannot construct invalid sequence|may construct sequence that does wrong thing but always type-safe+always executes

# block_categories(category|examples|range)
BC1|Control Flow|If+ElseIf+Else+While+ForEach|1000-9999
BC2|Statements|SetValueInt+SetValueFloat+SetValueBool+Log+ExecuteCommand|10000-999999
BC3|Reporters (return values)|GetValueInt+GetValueFloat+DrGetInt+DrGetFloat|1000000+
BC4|Math|MathAdd+MathMultiply+MathClamp+MathSin+MathVec2+MathVec2Length|1003000+
BC5|Logic|LogicAnd+LogicOr+LogicEqual+LogicLess|1002000+
# 100+ total operations

# type_safety(aspect|content)
TS1|UI enforces structure at edit time|blocks selected from dropdown (only valid types shown)+inputs filled via dropdowns or validated text fields+paths autocompleted from known entity fields+types checked before block added to stack
TS2|Data structure validates|LogicBlock has type(enum always valid)+text(validated string)+value_int+value_float; no free-form code+no parsing
TS3|Runtime never crashes|invalid paths return default values (0+false+empty)+math operations clamp/saturate instead of crashing+array access bounds-checked returns default if out of range
TS4|conclusion|can write wrong logic cannot crash

# path_based_access(aspect|content)
PBA1|operations|DrGetFloat("character.health")+DrGetInt("combat.damage")+DrGetBool("movement.is_moving")
PBA2|infrastructure resolves path at runtime|getFloatByPath parses "character.health" → splits → returns entity.character.health
PBA3|field replacement integration|if entity.silo_field_replacement_id != -1 lookup in replacement table before returning value
PBA4|integrates with other systems|ExecutePrologQuery+ExecuteLogicBlockStack+ApplyDamage+TriggerEvent

# dsp_model(aspect|content)
DSP1|all workloads expressed as pure data transformations|input array → transform → output array
DSP2|workload types|IntegrateVelocity+UpdateAwareness+EvaluateUtilityAI+ExecuteStateMachine+BuildSpriteBatch+30+ workload types
DSP3|no function calls between entities|no shared mutable state
DSP4|each entity modified by one thread only|no contention

# work_distribution(aspect|content)
WD1|WorkBatch fields|data_start_index+data_count+workload_type+input_data_path+input_data_ptr+input_stride+output_data_path+output_data_ptr+output_stride
WD2|Thread fields|id+cpu_core_id+memory_domain+work_batches[]+scratch_memory_ptr
WD3|10000 entities on 8 cores|batch_size=1250; threads 0-7 each handle 1250 entities sequentially within their range

# numa_placement(aspect|content)
NUMA1|MemoryDomain enum|NumaNode0+NumaNode1+NumaNode2+NumaNode3+GPU+SharedCPU
NUMA2|typical 16-core workstation|cores 0-7 NUMA node 0+cores 8-15 NUMA node 1
NUMA3|optimal placement|threads 0-7 cpu_core_id=[0..7] memory_domain=NumaNode0+threads 8-15 cpu_core_id=[8..15] memory_domain=NumaNode1
NUMA4|each thread's scratch memory in its NUMA node|entity data duplicated per NUMA node (input copied local+output written local+merged after barrier)
NUMA5|result|zero cross-NUMA traffic during frame processing

# barrier_sync(aspect|content)
BS1|FrameCoordinator|current_frame+thread_ids+threads_completed+frame_budget_ms (16.67ms)
BS2|frame execution|distribute work to all threads → wait for all to complete (spin or yield) → merge results → advance frame
BS3|only synchronization point in frame|threads run independently from start to barrier with no intermediate coordination

# scaling_results(cores|utilization|speedup)
SR1|1|100% (1 core)|1x (baseline single-threaded)
SR2|8|760% (95% per core)|7.6x
SR3|16|1520% (95% per core)|15.2x
SR4|32|3040% (95% per core)|near-32x
SR5|64|6080% (95% per core)|near-64x
# linear scaling because work perfectly divisible (entities independent)+no contention (no shared state)+barrier cost amortizes (O(cores) cost for O(entities/cores) work)
# traditional threading with locks: 8 cores ≈ 600% utilization (contention overhead)

# scene_isolation(aspect|content)
SCN1|Scene fields|id+name+actors[]+levels[]+state_machines[]+behavior_sets[]+prolog_rule_sets[]+logic_blocks[]+network buffers+game_time+game_frame+delta_time+silo_field_replacement_id
SCN2|each scene is independent execution context|own entity pool+own behavior definitions+own network buffers+own time/frame counter
SCN3|scenes cannot access each other's data|unless explicitly permitted via SceneSetItem rules

# access_control(aspect|content)
AC1|SceneSetItem fields|scene_id+is_maximized+is_minimized+is_floating+floating_rect+z_order+is_focused+update_speed+update_speed_minimized+allow_read_scene_ids+allow_write_scene_ids+allow_write_paths+allow_read_paths
AC2|DEFAULT DENY|empty allow lists deny all access
AC3|sceneCanWrite check|scene must be in allow list AND path must match pattern; both checks required; if either fails return false
AC4|path matching|pathMatches(path, pattern) — pattern matching against allow_write_paths or allow_read_paths
AC5|use cases vary|admin console + game scenes + dev tools + multi-tenant servers all work via same access control

# access_use_cases(id|use_case|configuration)
AU1|Multi-game server|Scene 1-100 player game instances+Scene 101 admin console; admin allow_read_scene_ids:[1..100]+allow_read_paths:[actors.0.transform.pos+actors.0.character.health]+allow_write_paths:[actors.0.access.is_banned]; admin reads+writes ban status but cannot modify game state directly
AU2|Development tools (inspector+monitor)|Scene 0 main game+Scene 1 inspector floating+Scene 2 performance monitor; inspector allow_read_paths:["*"]+monitor allow_read_paths:[game_time+delta_time+actors.len]; tools read game data without modifying+game unaware of tools

# network_packet(aspect|content)
NP1|InboundPacket fields|src_mac+dst_mac+ethertype+src_ip+dst_ip+protocol+ttl+src_port+dst_port+tcp_seq+tcp_ack+tcp_flags+payload_data[2048]+payload_length+checksum_valid+owner_scene_id
NP2|key properties|exactly 2048 bytes payload (no variable length)+no pointers (all values inline)+no nested allocations (flat structure)+preallocated buffers (no runtime allocation)
NP3|security implication|attacker cannot overflow+cannot inject pointers+cannot cause allocation
NP4|Network architecture|system-level rx_raw[64]+tx_ready[64] in Network Scene 0; per-scene inbound[1000]+outbound[1000]

# network_flow(step|content)
NF1|1|NIC → Network Scene (rx_raw)
NF2|2|Network Scene validates packet (checksum+length+routing)
NF3|3|Network Scene routes to Game Scene by dst_port
NF4|4|Network Scene checks: can write to target scene? (sceneCanWrite check)
NF5|5|Network Scene decodes payload to fixed struct (PlayerInput)
NF6|6|Game Scene processes packet (writes ONLY allowed paths e.g. actors.0.input.mouse_x+actors.0.input.button_click)
NF7|7|Game Scene queues response (outbound)
NF8|8|Network Scene reads outbound
NF9|9|Network Scene → NIC (tx_ready)
# isolation: game scenes never touch NIC directly; Network Scene mediates all I/O

# attack_surface(id|attack|result)
AS1|Buffer overflow (send 4096 bytes instead of 2048)|packet rejected (size mismatch)+NIC drops before software sees
AS2|Code injection (put function pointer in payload_data)|field type is u8 array not function pointer; copied as data never executed
AS3|Write to health (encode "character.health = 0" in payload)|path "actors.0.character.health" not in allow_write_paths+write blocked
AS4|Read other player data (request actors[1].character.health)|no read mechanism in input path; cannot trigger outbound packet with data
AS5|Exfiltrate data (modify outbound buffer)|game scene cannot write to network.outbound (not in allow_write_paths)
AS6|Escalate privileges (set is_dev_mode=true)|path "is_dev_mode" not in allow_write_paths+blocked

# malicious_data(aspect|content)
MD1|attacker crafts packet|valid checksum+correct port+passes firewall+contains malicious input values like NaN+MAX_FLOAT+negative values
MD2|written to entity input fields|actors[0].input.mouse_x = NaN+actors[0].input.mouse_y = 3.4e38+actors[0].input.button_click = -1
MD3|next frame entity updates|state machine evaluates Prolog rule is_valid_input(mouse_x, mouse_y) :- X >= 0, X <= 1920, Y >= 0, Y <= 1080; rule fails (NaN not >= 0+MAX_FLOAT > 1080)
MD4|input validation behavior scores 0|entity ignores input continues previous behavior
MD5|result|bad input for 1 frame (16ms)+validation detects+entity behavior unaffected (scores 0 not selected)+next frame normal input resumes
MD6|cannot|crash game (NaN handled gracefully in logic blocks)+corrupt state (only input fields writable)+persist malicious state (overwritten next frame)+escalate (no write access to privileges)+exfiltrate (no read or send capabilities)

# tall_infra_bug(aspect|content)
TIB1|infrastructure has bug example|pathMatches has off-by-one (uses >= instead of ==); attacker accesses "actors.0.input.mouse_xYZ" past allowed prefix
TIB2|exploit consequence|writes to invalid field+potential crash
TIB3|but ONE-TIME FIX|bug discovered in pathMatches (infrastructure code)+fix changes >= to ==+recompile infrastructure+ALL games using Silo benefit (not per-game fix)
TIB4|contrast traditional|game A has SQL injection bug → fix game A; game B has buffer overflow → fix game B; different codebases+different vulnerabilities+no shared infrastructure to fix once
TIB5|tall-infra principle|vulnerability in infrastructure affects all games but fix once protects all games

# trace(aspect|content)
TR1|EntityTrace fields|entity_id+frame+state_before+state_after+behavior_set_name+behaviors_scored[]+behavior_selected_index+logic_blocks_executed[]+stats_before[]+stats_after[]+events_received[]
TR2|BehaviorScore fields|behavior_name+final_score+consideration_scores[]
TR3|LogicBlockExecution fields|block_type+inputs+output+timestamp
TR4|captured per entity per frame|state machine before/after+behavior set+all behaviors scored with consideration breakdowns+selected behavior+logic blocks executed with timing+stats before/after+events received
TR5|query interface|getTrace(entity_id+frame) → complete decision chain in domain terms
TR6|example output|"Entity 42 frame 1534: Combat→Combat; Attack scored 0.852 (has_weapon=1.0+target_distance=0.85+health_sufficient=0.9); Flee scored 0.421; Block scored 0.156 (has_shield=0); Selected Attack; logic blocks DrGetInt+SetTarget+PathToTarget; target.health: 100→85 (-15)"

# replay_workflow(step|action)
RW1|1|Pause at frame 1534
RW2|2|Examine trace (Attack selected)
RW3|3|Modify Prolog rule (e.g. flee_health_threshold from health<20 to health<90)
RW4|4|Replay frame 1534 with modified rules
RW5|5|Compare results: OLD (Attack: 0.852+Flee: 0.421+Selected: Attack); NEW (Attack: 0.852+Flee: 0.950+Selected: Flee)
RW6|6|Accept or reject rule change
# implementation: restore entity state from frame snapshot+apply modified rules if provided+re-execute frame+return new trace
# A/B testing rules in-game instantly

# debugging_comparison(traditional|silo)
DB1|bug occurs|same
DB2|reproduce (often difficult)|query trace (exact frame+exact entity)
DB3|add logging/breakpoints|see complete decision chain
DB4|recompile|identify cause (behavior scored wrong)
DB5|run again|modify Prolog rule or consideration
DB6|examine logs/variables|replay frame
DB7|guess at cause|confirm fix
DB8|modify code|done (no recompilation)
DB9|recompile+test|—
# time saved: minutes to hours per bug; multiplied across development = massive productivity gain

# silo_examples(id|example|what_changes|what_doesnt)
SE1|Dragon vs Chair|entity_type+character.health=500+combat.damage=50+visual.sprite_id=42+movement.speed=3.0 (dragon); transform.pos+visual.sprite_id=15 (chair); other systems default values|infrastructure processes both identically; same struct same fields
SE2|Field replacement game→business|character.health → account.balance; UI displays "$5000" instead of "Health: 5000"|underlying f32 value+infrastructure processing identical
SE3|Equipment slot as bank balance|slot_type=.Backpack+world_item_id=334(player_bank_balance row)+count=50000(balance amount)+health_max=10000(insurance cap)+health=10000(coverage)|same equipment slot infrastructure; different semantic meaning
SE4|Dragon Boss in 4 rows|game.entity (name="Dragon", state_machine_id=97)+game.state_machine (id=97, states=[phase1,phase2,phase3])+game.behavior_set (id=42, behaviors=[breath_attack,tail_swipe,summon_adds])+game.stat (entity_id=dragon, stat_type=9000, value=5000)|binary processes state machine+scores behaviors+applies envelopes; never executes "dragon code" because no such code exists
SE5|Weather/morale/crafting|three apparently unrelated systems all use same state machine runner+utility scoring; weather "current behavior" read as current weather state; morale's behavior triggers AI actions; crafting's state gates recipe availability|one function evaluates transitions+one scores behaviors; semantics differ entirely based on how data is wired

# anti_examples(id|system|claim|reality|wall)
AE1|Unity ScriptableObjects|"our data is in ScriptableObjects we're data-driven!"|still write class Goblin : MonoBehaviour with void Attack() methods; ScriptableObject holds stats+behavior is compiled|present — new enemy types require new classes
AE2|Unreal Data Tables|"we use Data Tables for everything!"|damage calculations are Blueprint or C++; quest branches are Blueprint or C++; AI behavior trees have compiled task nodes|present — new mechanics require new nodes
AE3|Overwatch ECS|"pure ECS all data in components!"|hero-specific systems contain compiled logic; Reinhardt's charge+Tracer's blink+Mercy's resurrect all have dedicated code paths|present — new heroes require new systems
AE4|Factorio Prototypes|"everything defined in prototype data!"|combat AI compiled+train pathfinding compiled+electric network solving compiled; prototypes define what exists+code defines how it behaves|present — new transport types require new code

# litmus_test(id|question)
LT1|1|Can a designer add a "living market economy" without asking engineering?
LT2|2|Can stat.health be repurposed as "bank account balance" with zero code change?
LT3|3|Can you swap every texture+sound+behavioral rule while the executable keeps running?
LT4|4|Does the compiled binary know that any noun (goblin+sword+quest+fireball) exists?
# rule: if any answer is "no" you have a wall; you may be data-driven; you are not data-only

# when_to_use(id|category|conditions)
WU1|Strong fit|Live service games with continuous content updates+multi-SKU studios amortizing infrastructure across projects+games with heavy modding support+large content volume (hundreds of enemy types+thousands of items)+long development cycles where requirements will change
WU2|Weak fit|Game jams (no time to build infrastructure)+prototypes (exploration over architecture)+single-ship titles with small teams and fixed scope+games where performance requires hand-tuned compiled code paths
# rule: infrastructure cost is front-loaded; productivity multiplier is permanent

# learning_disciplines(discipline|content)
LD1|Data-relational thinking|everything is foreign keys and columns; a "dragon" is a row that references other rows
LD2|Predicate logic|conditions are rules unified against facts not if/else chains
LD3|Utility curve design|behaviors emerge from scored considerations not scripted sequences
LD4|Envelope-based effects|modifications are time-bounded stat transformations not imperative mutations
LD5|Trace-driven debugging|problems are queries over decision history not breakpoints in code
# rule: learnable; better mental models than "write code for each thing"; designer who thinks in curves and predicates expresses more with less

# productivity(metric|traditional|tall_infra)
PD1|New enemy type|Code+data+test|Data only
PD2|New mechanic|Design+code+iterate|Data wiring
PD3|Balance pass|Rebuild or hot-reload values|Hot-swap tables
PD4|Multi-project reuse|Fight the old architecture|Same binary new dataset
PD5|Live service patch|Risk regression in compiled behavior|Zero code risk
# rule: marginal cost of new content approaches zero engineering time; 1000th behavior set costs same as 10th

# performance(workload|hardware|result)
PF1|Single-threaded baseline|Ryzen 9 5950X (16 cores) 64GB RAM; 10000 entities each with 3-state SM+3-behavior set+10 logic blocks|Frame: 32ms; FPS: 31; Bottleneck: sequential entity updates
PF2|8 threads|same hardware|Frame: 4.2ms; FPS: 238; CPU: 760% (95% per core); Speedup: 7.6x
PF3|16 threads|same hardware|Frame: 2.1ms; FPS: 476; CPU: 1520% (95% per core); Speedup: 15.2x
PF4|Per-frame breakdown (10000 entities 16 threads)|Work distribution: 0.05ms+Entity updates: 1.50ms (state machines: 0.30+Prolog: 0.40+UAI: 0.50+Logic blocks: 0.30)+Barrier sync: 0.10ms+Render prep: 0.45ms+Total: 2.10ms|Headroom at 60 FPS: 16.67ms - 2.10ms = 14.57ms free (87% headroom)
PF5|Hot-swap performance|edit behavior set+save (writes to SQLite)+next frame loads new data+entities use new behavior|Total time: 16.67ms (one frame); no restart+no recompilation+no interruption

# memory(category|content)
MM1|Per entity|Entity struct ~2KB+Trace 1 frame ~1KB+state machine data shared+behavior set data shared; Total per entity ~3KB
MM2|10000 entities|~30MB
MM3|Shared data|State machines ~100KB (20 machines)+Behavior sets ~500KB (50 sets)+Prolog rule sets ~200KB (30 sets)+Logic block stacks ~1MB (100 stacks); Total shared ~2MB
MM4|Total|~32MB for 10000 entities + behavior data

# bottlenecks(bottleneck|problem|solution|result)
BN1|Prolog evaluation|complex rules with deep recursion slow per-entity|limit rule depth to 5 levels+cache common queries|0.40ms → 0.25ms (37% reduction)
BN2|Cache misses|entity array not sorted by position+poor spatial locality|sort entities by screen-space position before frame|1.50ms → 1.20ms (20% reduction)
BN3|Barrier overhead|spinning wastes cycles|yield after 1000 spins|0.10ms → 0.08ms (marginal)
# current bottleneck: Prolog evaluation; future work: GPU-accelerated unification

# minimum_viable_system(step|component|lines)
MV1|1|Entity structure (id+entity_type+state fields+transform system+single character system with health field)|100 lines
MV2|2|Simple state machine (3 states: Idle+Moving+Dead+event-based transitions only+no Prolog yet)|50 lines
MV3|3|Single behavior set (2 behaviors: DoNothing+MoveToTarget+1 consideration each constant score+no Prolog yet)|75 lines
MV4|4|Basic logic blocks (10 block types: GetValue+SetValue+MathAdd+If+Else+Log+stack machine executor+path-based field access)|200 lines
MV5|5|Single-threaded update loop (for each entity: updateStateMachine+if not dead executeBehaviorSet; render)|100 lines
# target: 500 lines total; runs at 60 FPS with 100 entities
# validates: Entity updates correctly+state machines transition+behaviors execute+logic blocks modify entity

# incremental_path(phase|additions|validates)
IP1|Adding Prolog|implement core structures (Term+Fact+Rule+KnowledgeBase 150 lines)+generate entity facts (100 lines)+use in state transitions (50 lines)+expand to UAI considerations (25 lines)|Prolog rules match entity facts+state transitions use rules+UAI uses rules for gating
IP2|Adding parallel execution|identify independent workloads (entity updates+behavior scoring+logic block execution)+implement work distribution (200 lines)+thread workers (150 lines)+barrier synchronization (100 lines)|work distributed evenly+threads execute independently+barrier waits for all+results correct (same as single-threaded)+>90% CPU utilization per core
IP3|Adding scene isolation|Scene structure (100 lines)+SceneSetItem with access control (100 lines)+access enforcement (50 lines)|scenes cannot access each other by default+explicit whitelist required+path matching works correctly
IP4|Adding network security|fixed packet structures (150 lines)+network scene (200 lines)+firewall integration (100 lines)|packets cannot overflow (fixed size)+only allowed paths writable+game scenes cannot access NIC+malicious input contained

# validation_checklist(id|test)
VC1|Hot-swap test|modify behavior set while running+verify takes effect next frame (16ms)
VC2|Scalability test|add new behavior to set+verify existing behaviors unaffected
VC3|Trace test|query trace for specific frame/entity+see complete decision chain
VC4|Parallel test|run on 8 cores+measure >90% utilization per core
VC5|Isolation test|Scene A cannot read Scene B data without explicit permission
VC6|Security test|network packet cannot write to non-whitelisted path
VC7|Field replacement test|change silo_field_replacement_id+verify UI labels change
VC8|Performance test|10000 entities update in <10ms per frame

# limitations(id|limitation|content)
LM1|2D only|3D rendering requires additional visual systems (skeletal animation+materials+lighting); same architecture+just more data in Entity.visual; planned for future releases
LM2|Prolog performance|degrades with >100 rules per query; no indexing or optimization currently; naïve unification algorithm
LM3|Fixed buffer sizes|all buffers preallocated (entities+packets+envelopes); configurable but not dynamic; tradeoff: performance vs flexibility
LM4|No garbage collection|all memory management manual; entities reused (is_deleted flag not freed); requires discipline to avoid leaks

# future_work(id|extension|content)
FW1|3D rendering integration|skeletal animation+PBR material system+shadow mapping; same execution path more visual data
FW2|GPU-accelerated Prolog|parallel unification on GPU; 1000x speedup potential for complex rules; research phase
FW3|Distributed scenes|scenes on different machines+network synchronization of shared data; maintain same scene isolation model
FW4|Code generation from Logic Blocks|compile logic block stacks to native code+fallback to interpretation for development; best of both: iteration speed + runtime performance
FW5|Research questions|Can Prolog be replaced with learned models?+Can logic blocks be generated from natural language?+Can scenes coordinate without central authority?

# comparison_engines(aspect|unity_unreal|silo)
CE1|Iteration|30-300s (compile+restart)|0s (next frame)
CE2|Type safety|Compiler-enforced|Structural (data validation)
CE3|Hot-swap|Limited (assets only not code)|Everything (state machines+behaviors+logic+rules)
CE4|CPU utilization|60-70% (lock contention)|95%+ (no contention)
CE5|Debugging|Breakpoints+stack traces|Decision traces+frame replay
CE6|Tradeoffs|Mature ecosystems+3D rendering+large teams|Faster iteration+simpler debugging+solo/small teams

# comparison_ecs(aspect|bevy_flecs|silo)
CECS1|Data layout|Array-of-structs (cache-friendly)|Array-of-structs (cache-friendly)
CECS2|Behavior|Code in systems|Data in tables
CECS3|Hot-swap|Components only|Everything
CECS4|Parallelism|System dependency graph|Independent entity ranges
CECS5|Learning curve|Archetypes+world queries|State machines+Prolog+UAI
# similarities: both optimize for cache locality+both enable parallel execution
# differences: ECS behavior in compiled code; Silo behavior in data tables

# comparison_bt(aspect|behavior_trees|silo)
CBT1|Execution|Tree-walk|Tree-walk
CBT2|Composition|Priority-based|Utility-based (multiplicative scoring)
CBT3|Extensibility|Insert in tree|Add to set
CBT4|Debug|Node visualization|Full trace
CBT5|When to use BT|Well-understood behavior patterns+priority-based decision making+visual tree editing preferred|—
CBT6|When to use Silo|Rapid iteration required+emergent behavior desired (utility scoring)+hot-swapping needed|—

# applicability_beyond_games(domain|scene_meaning)
AB1|Web apps|Scene per request
AB2|Database|Scene per query
AB3|OS|Scene per process
AB4|Real-time constraints (embedded+robotics+simulation)|Scene per simulation context
AB5|Multi-tenant systems|Scene per tenant
AB6|Data processing/analytics|Scene per workload
# rule: same infrastructure+different data; the future of software may not be writing more code but composing more primitives through data configuration

# relationships(from|rel|to)
T1|implements|T2
T1|requires|T17
T2|enables|T19
T3|grounds|E2+E3+E4
T4|prevents|class-Goblin-extends-Entity
T5|enables|FR1+access-via-other-layers
T6|implements|EF1+EF2+EF3+EF4
T6|reduces|cognitive-load-at-each-layer
T7|enables|behavior-set-swap-without-touching-state-machine
T8|enables|fail-fast-scoring
T9|prevents|crash-from-wrong-logic
T10|enables|T11
T11|implements|T10
T11|achieves|SR2+SR3+SR4+SR5
T12|prevents|AS1+AS2+AS3+AS4+AS5+AS6
T13|enforces|AC2+AC3
T14|grounds|TIB1+TIB2+TIB3+TIB4+TIB5
T15|enables|RW1+RW2+RW3+RW4+RW5+RW6
T16|enables|hot-swap-everything
T17|distinguishes|tall-infra-data-only-from-mere-data-driven
T18|tests|whether-architecture-qualifies
T19|justifies|infrastructure-investment
DEF1|distinct_from|DEF2
DEF2|distinct_from|DEF3
DEF3|requires|QC1+QC2+QC3+QC4
DEF4|consequence_of|all-four-QC-conditions
QC_ALL|together_required|for-tall-infra-data-only-classification
HW_ALL|demonstrate|every-era-preserved-the-wall
HW_ALL|grounds|T17
AL1|consumed_by|AL2+AL3+AL4+AL5
AL2|references|AL3+AL4
AL3|gates|AL2-transitions+AL4-considerations+AL5-conditions
AL4|consumes|AL3-rules+entity-stats
AL5|executes|via-stack-machine
AL6|distributes|AL1-updates
AL7|isolates|AL1-pools
AL8|enforces|AL7-access-rules
EF1|filters_to|EF2
EF2|filters_to|EF3
EF3|filters_to|EF4
EF4|results_in|state-mutation
EF5|applies|continuous-effects-after-EF4
SH_ALL|bypass|EF-layers
E1|implements|T3
E2|illustrates|T4
E3|enforces|T3-uniformity
E4|enables|T5
E5|requires|MS3
FR1|implements|T5
FR2|illustrates|semantic-relabeling
FR3|preserves|infrastructure-invariance
FR4|enables|cross-domain-prototyping
MS1|enables|MS2
MS2|implements|coordination-via-shared-data
MS3|implements|T5-wall-less
MS4|implements|separation-of-concerns
SM1|enables|A/B-testing-via-rule-set-b
SM2|references|behavior-set
SM3|references|exit-conditions
SM4|implements|T7-pure-topology
SM5|enables|behavior-swap
SM6|implements|T3-uniform-processing
TM1|distinct_from|TM2
TM2|distinct_from|TM3
TM4|combines|TM1+TM2+TM3
PR1|enabled_by|FG1
PR2|gates|UA-considerations
PR3|enables|conditional-logic-in-blocks
FG1|inputs|PR-evaluation
FG2|ensures|decisions-on-up-to-date-information
PA_ALL|justify|Prolog-over-imperative-conditions
UA1|gates|via-PR1
UA2|composes|considerations
UA3|holds|behaviors-for-selection
UA4|enables|deterministic-default+controlled-randomness
SS1|implements|T8-fail-fast
SS3|prevents|out-of-range-scores
SS4|shapes|input-to-score-mapping
SS7|implements|multiplicative-scoring
SS8|compensates|over-penalization
SS9|provides|baseline-floor
SP1|implements|T8
SP2|prevents|over-penalization
CV_ALL|provide|input-to-score-shaping
SEL1|default|deterministic
SEL2|enables|variety-without-chaos
LB1|implements|T9
LB2|enables|Turing-completeness
LB3|enables|TS1
LB4|prevents|invalid-stack-states
LB5|implements|T9-cannot-crash
BC_ALL|compose|into-Turing-complete-system
TS1|implements|T9
TS2|validates|at-data-level
TS3|prevents|crashes-via-defaults+clamps
TS4|grounds|T9
PBA1|enables|path-based-data-access
PBA3|implements|FR3
PBA4|integrates|with-other-systems
DSP1|enables|T10
DSP3|enables|T11-no-locks
DSP4|enables|T11-no-sharing
WD1|distributes|via-batches
WD3|illustrates|even-distribution
NUMA4|implements|T11-NUMA-local
NUMA5|achieves|zero-cross-NUMA-traffic
BS1|coordinates|frame-execution
BS2|implements|barrier-pattern
BS3|implements|T11-only-sync-point
SR_ALL|demonstrate|linear-scaling
SR_traditional|baseline_for|comparison
SCN1|provides|isolated-execution-context
SCN2|implements|isolation
SCN3|requires|explicit-permission
AC1|fields_for|access-control
AC2|implements|T13-default-deny
AC3|implements|T13-both-checks-required
AC5|enables|AU1+AU2
AU1|exemplifies|multi-tenant-server
AU2|exemplifies|read-only-dev-tools
NP1|implements|T12-fixed-shape
NP2|prevents|buffer-overflow+pointer-injection+allocation
NP3|grounds|T12
NP4|isolates|game-scenes-from-NIC
NF_ALL|implement|isolation-pattern
AS_ALL|prevented_by|T12+T13
MD_ALL|demonstrate|T12-graceful-degradation
TIB_ALL|demonstrate|T14-one-time-fix-protects-all
TR1|captures|complete-decision-chain
TR4|enables|T15
TR5|provides|domain-aware-debugging
TR6|exemplifies|trace-output
RW_ALL|implement|in-game-A/B-testing
DB_ALL|demonstrate|productivity-improvement
SE1|illustrates|T3
SE2|illustrates|FR1
SE3|illustrates|FR4
SE4|illustrates|behavior-as-data
SE5|illustrates|infrastructure-reuse-across-domains
AE_ALL|fail|litmus-test
AE_ALL|preserve|the-wall
LT_ALL|test|T17
WU_ALL|inform|adoption-decision
LD_ALL|required|for-mastery
PD_ALL|demonstrate|T19
PF_ALL|measure|implementation-results
MM_ALL|characterize|memory-footprint
BN_ALL|identify|optimization-targets
MV_ALL|provide|incremental-bootstrap-path
IP_ALL|expand|MVP-incrementally
VC_ALL|verify|implementation-completeness
LM_ALL|name|current-boundaries
FW_ALL|name|planned-extensions
CE_ALL|distinguish|Silo-from-Unity-Unreal
CECS_ALL|distinguish|Silo-from-ECS
CBT_ALL|distinguish|Silo-from-behavior-trees
AB_ALL|extend|architecture-beyond-games

# section_index(paper|section|title|ids)
COMP-1|1|Introduction|T1+T2+AL1+AL2+AL3+AL4+AL5+AL6+AL7+AL8
COMP-1|2|Entity Universal Container|T3+T4+T5+E1+E2+E3+E4+E5+FR1+FR2+FR3+FR4+MS1+MS2+MS3+MS4
COMP-1|3|Execution Path Funnel|T6+EF1+EF2+EF3+EF4+EF5+SH1+SH2+SH3
COMP-1|4|State Machines Pure Topology|T7+SM1+SM2+SM3+SM4+SM5+SM6+TM1+TM2+TM3+TM4
COMP-1|5|Prolog Declarative Logic|PR1+PR2+PR3+FG1+FG2+FG3+PA1+PA2+PA3+PA4+PA5
COMP-1|6|Utility AI Multiplicative Behavior Scoring|T8+UA1+UA2+UA3+UA4+SS1+SS2+SS3+SS4+SS5+SS6+SS7+SS8+SS9+SP1+SP2+SP3+SP4+CV1+CV2+CV3+CV4+CV5+CV6+SEL1+SEL2+SEL3
COMP-1|7|Logic Blocks Stack-Based Bytecode|T9+LB1+LB2+LB3+LB4+LB5+BC1+BC2+BC3+BC4+BC5+TS1+TS2+TS3+TS4+PBA1+PBA2+PBA3+PBA4
COMP-1|8|Parallel Execution NUMA Threading|T10+T11+DSP1+DSP2+DSP3+DSP4+WD1+WD2+WD3+NUMA1+NUMA2+NUMA3+NUMA4+NUMA5+BS1+BS2+BS3+SR1+SR2+SR3+SR4+SR5
COMP-1|9|Scene Isolation Access Control|T13+SCN1+SCN2+SCN3+AC1+AC2+AC3+AC4+AC5+AU1+AU2
COMP-1|10|Network Security Geometric Input Isolation|T12+NP1+NP2+NP3+NP4+NF1+NF2+NF3+NF4+NF5+NF6+NF7+NF8+NF9+AS1+AS2+AS3+AS4+AS5+AS6+MD1+MD2+MD3+MD4+MD5+MD6+T14+TIB1+TIB2+TIB3+TIB4+TIB5
COMP-1|11|Trace System First-Class Debugging|T15+TR1+TR2+TR3+TR4+TR5+TR6+RW1+RW2+RW3+RW4+RW5+RW6+DB1+DB2+DB3+DB4+DB5+DB6+DB7+DB8+DB9
COMP-1|12|Implementation Guide|MV1+MV2+MV3+MV4+MV5+IP1+IP2+IP3+IP4+VC1+VC2+VC3+VC4+VC5+VC6+VC7+VC8
COMP-1|13|Performance Characteristics|PF1+PF2+PF3+PF4+PF5+MM1+MM2+MM3+MM4+BN1+BN2+BN3
COMP-1|14|Limitations and Future Work|LM1+LM2+LM3+LM4+FW1+FW2+FW3+FW4+FW5
COMP-1|15|Comparison to Existing Systems|CE1+CE2+CE3+CE4+CE5+CE6+CECS1+CECS2+CECS3+CECS4+CECS5+CBT1+CBT2+CBT3+CBT4+CBT5+CBT6
COMP-1|16|Conclusion|T1-T19 restated structurally
COMP-2|1|Core Distinction|DEF1+DEF2+DEF3+DEF4+T17
COMP-2|2|Historical Context|HW1+HW2+HW3+HW4
COMP-2|3|Definition Tall-Infra Data-Only|QC1+QC2+QC3+QC4
COMP-2|4|Architecture Stack|AL1+AL2+AL3+AL4+AL5
COMP-2|5|Concrete Example Dragon Boss|SE4
COMP-2|6|Concrete Example Equipment Slot|SE3
COMP-2|7|Concrete Example Weather Morale Crafting|SE5
COMP-2|8|Anti-Examples|AE1+AE2+AE3+AE4
COMP-2|9|Litmus Test|LT1+LT2+LT3+LT4
COMP-2|10|Debugging and Observability|TR1+TR2+TR3+TR4+TR5+TR6
COMP-2|11|Performance|PF1+PF2+PF3+PF4
COMP-2|12|Productivity Implications|PD1+PD2+PD3+PD4+PD5+T19
COMP-2|13|Learning Curve|LD1+LD2+LD3+LD4+LD5
COMP-2|14|When to Use|WU1+WU2
COMP-2|15|Conclusion|T1-T19 restated structurally
COMP-2|Appendix|Glossary|covered in main tables

# decode_legend
papers_combined: COMP-1+COMP-2
canonical_distinction: data-driven (code owns types data owns numbers) vs data-only (binary forgets what goblin is) vs tall-infra-data-only (entire vertical stack)
qualification_count: 4 (zero gameplay types in binary+behavior in hot-swappable tables+designers create new mechanics+all subsystems same data layout)
historical_eras: 1990s|2000s|2010s|2020s — every era preserved the wall
silo_layers: Entity|StateMachine|Prolog|UtilityAI|LogicBlock|Thread|Scene|Networking
execution_funnel: StateMachine→Prolog→UtilityAI→LogicBlock (4 stages with shortcut paths)
funnel_questions: what-am-I-doing|preconditions-met|highest-score|how-execute
shortcut_paths: force_action(skip-UAI)|exit_on_event(skip-Prolog)|exit_condition_rule(Prolog-only)
state_machines_per_entity: up-to-14
transition_mechanisms: event|rule|duration|combination
prolog_use_cases: state-machine-transitions|UAI-considerations|logic-block-conditions
prolog_advantages: reusable|composable|data-driven|introspectable|no-syntax-errors
scoring_steps: 9 (rules→input→normalize→curve→weight→invert→multiply→avg-fixup→floor)
scoring_property: multiplicative-with-fail-fast (any 0 collapses behavior)
selection_methods: top|weighted_random_top3|random_reasonable
logic_block_categories: control-flow|statements|reporters|math|logic
type_safety_layers: UI-enforces|data-validates|runtime-defaults
dsp_model: pure-data-transformations (input array → transform → output array)
numa_layout: each-thread-pinned-to-core+scratch-in-NUMA-node+entity-data-duplicated-per-node
scaling: linear-95%-per-core (8=760%+16=1520%+32=3040%+64=6080%)
vs_traditional: traditional-with-locks ≈ 600% on 8 cores
scene_access: DEFAULT-DENY+scene-id+path-pattern-both-required
packet_size: fixed-2048-bytes-no-pointers-no-allocations
attack_outcomes: all-prevented-via-fixed-shape+access-control
malicious_data_outcome: bad-input-1-frame+validation-rejects+normal-resumes
tall_infra_bug_pattern: vulnerability-in-infra-affects-all+fix-once-protects-all
trace_capture: per-entity-per-frame-complete-decision-chain
replay_workflow: pause+modify-rule+replay-frame+compare+accept-or-reject
hot_swap_time: 16.67ms (one frame)
debugging_speedup: minutes-to-hours-per-bug
silo_lines: minimum-viable=500 + full-system=5000
performance_baseline: 10000-entities-at-4.2ms-on-8-threads (95%+ utilization)
memory: ~32MB-for-10000-entities-plus-behavior-data
litmus_questions: 4 — designer-adds-economy?+repurpose-stat?+swap-while-running?+binary-knows-noun?
strong_fit: live-service+multi-SKU+modding+large-content+long-cycles
weak_fit: jams+prototypes+single-ship+performance-tuned
learning_disciplines: data-relational+predicate-logic+utility-curves+envelopes+trace-debugging
productivity_metrics: new-enemy|new-mechanic|balance-pass|reuse|live-service-patch
limitations: 2D-only|Prolog-naïve|fixed-buffers|manual-memory
future_work: 3D|GPU-Prolog|distributed-scenes|codegen|research-questions
comparison_baselines: Unity-Unreal|ECS-Bevy-Flecs|behavior-trees
beyond_games: web|database|OS|embedded|multi-tenant|data-processing
sot_for_behavior: data-tables (not compiled code)
sot_for_intent: configuration (not source files)
sot_for_correctness: type-safety-via-UI+data+runtime (not compiler)
canonical_summary: axioms-first+data-only+ship-faster
rel_types: implements|requires|enables|grounds|prevents|distinct_from|consequence_of|together_required|demonstrate|consumed_by|references|gates|consumes|distributes|isolates|enforces|filters_to|results_in|applies|bypass|illustrates|enabled_by|gates|inputs|ensures|justify|composes|holds|provides|prevents|fields_for|identifies|name|extend|extends|distinguish|inform|required|measure|characterize|verify|expand|provide|fail|test|tests|preserve|reduces|reduces|distributes|distinct_from|coordinates|prevents|inputs|integrates|achieves|exemplifies|baseline_for|combines|enables|justifies
