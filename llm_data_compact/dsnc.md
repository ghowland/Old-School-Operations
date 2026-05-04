# DSNC (DASONIC) — LLM-COMPACT FORM
# Database Schema Naming Convention
# Format: pipe-delimited tables, ID refs.
# Read order: meta → principles → core-rules → prefixes → suffixes → tense → composition → fk-naming → fk-disambiguation → reserved → capitalization → stage-tracking → deviations → relationships → sections

# meta(aspect|content)
M1|spec_version|0000
M2|versioning|spec itself versioned so changes can be referenced precisely; clarity of intention across revisions
M3|status|naming convention for database schemas; rules for table+field naming

# principles(id|principle|rationale)
P1|Internal consistency over correctness|specific rules less important than rigid adherence; comprehensibility comes from consistency not from any one rule being optimal
P2|Databases are hierarchies of namespaces|treat as namespace system; strict adherence enables maximum growth+comprehensibility especially at scale (100s-1000s of tables)
P3|Make your own rules for special cases|when current rules don't apply create new rule; design for consequences of rule applied across all situations; new rules become well-integrated through use+adjustment over time
P4|Don't avoid long names|all the context you'll ever have about this data; documentation drifts; schema is self-documenting; short names sacrifice clarity
P5|Names recompose without provenance loss|reading a long composed name tells you exactly what the table/field is; each component carries meaning
P6|Convention dictates the names|developers don't need to look up or guess field names if they know the convention; consistent rules eliminate naming uncertainty
P7|Small databases tolerate informality; large ones require rigid structure|deviation in standardized namespace creates large comprehensibility problems at scale; non-conformity is the failure mode
P8|Conventional rules first; special rules where needed|where language differs from conventions go along with the language; comply with DSNC where not using/overloading base language formats

# core_rules(id|rule|rationale|example_correct|example_wrong)
R01|No plurals ever|developers shouldn't have to remember/look-up singular vs plural; some words don't pluralize predictably (company/companies+squid/squidii+dolphin/pod); thinking of references that could be singular OR plural eliminates the need|company|company_employee|companies|users
R02|All names lower_case_with_underscores|consistent format for table+field names; differentiates from CamelCase classes+UPPER_CASE globals|company_employee|web_site_widget|companyEmployee|company-employee|CompanyEmployee
R03|Compose names specific-to-general|prefixes act like directory structures; alphabetical sorting groups related items; common prefix shows relationship without enforcing hierarchy|web_site|web_widget (sibling)|web_site_widget (child)|widget_web_site (wrong order)
R04|Prefix is the topic; suffix is the detail|topic-first composition reads as namespace traversal|deployment_created_time|deployment_approved_user_id|created_deployment_time|user_id_deployment_approved
R05|Sibling vs child distinguished by prefix presence|web_widget standalone (independent of web_site); web_site_widget is web_site-specific (child in hierarchy)|web_widget|web_site_widget (different things)|same name for both
R06|Underscores separate all internal terms|"web_site" not "website"; allows shared prefix "web_" with web_widget for namespace grouping|web_site|web_widget|website|webwidget
R07|Use common phrases; don't invent synonyms|"_start_"/"_stop_" never "begin/end" or "start/finish"; even when slightly different use the canonical pair|was_activated_start_time|was_activated_stop_time|was_activated_begin_time|was_activated_end_time
R08|Add hierarchical scaling terms when needed|use "_phase_0_" or "_phase_00_" or "_phase_000_" for ordered granularity when many stages exist|was_activated_phase_0_start_time|was_activated_phase_00_stop_time|ad-hoc stage names
R09|Reuse prefix terminology in every relevant location|once "vendor_" is chosen as prefix use it everywhere that context applies; consistent labeling is commenting what is being referenced|vendor_company_id|vendor_employee_id (same prefix in same context)|vendor_company_id+supplier_employee_id (inconsistent)
R10|Resolve prefix collisions by uniqueness even if reads weirdly|namespace cleanliness is highest priority; consistent label usage matters more than smooth reading|context-specific unique prefix|prefix collision unresolved
# rule: when in doubt prefer the rule that produces unambiguous structural meaning over the rule that produces shorter or smoother names

# prefixes(id|prefix|meaning|data_type|tense|example)
PR1|is_|currently true (present-state boolean)|BOOLEAN(0=false+1=true+null=unknown)|present|is_active
PR2|was_|past event (without suffix=boolean; with suffix=event-data)|BOOLEAN by default; other types via suffix|past|was_activated|was_activated_time|was_activated_user_id

# suffixes(id|suffix|column_type|example|notes)
SF1|_time|DATETIME|created_time|deployment_approved_time|always DATETIME-style; provides namespace for related fields
SF2|_date|DATE|effective_date|expiration_date|DATE-style
SF3|_user_id|FK to user.id|created_user_id|deployment_approved_user_id|FK suffix combining table+id; often paired with _time on same prefix
SF4|_id|FK to <table>.id|company_id|service_company_id|standard FK suffix
SF5|_start_time|DATETIME marking start|was_activated_start_time|paired with _stop_time
SF6|_stop_time|DATETIME marking end|was_activated_stop_time|paired with _start_time
SF7|_phase_N_|ordered scaling term|was_activated_phase_0_start_time|use _phase_NN_ or _phase_NNN_ for large numbers

# tense_rules(id|prefix|tense|data_type|example|notes)
TR1|is_|present|BOOLEAN|is_active|current state tracking
TR2|was_|past|BOOLEAN|was_activated|past event flag
TR3|was_*_time|past|DATETIME|was_activated_time|single time-data point for the flag
TR4|was_*_start_time|past|DATETIME|was_activated_start_time|paired
TR5|was_*_stop_time|past|DATETIME|was_activated_stop_time|paired
# rule: tenses must agree across stages within a topic; approved/deployed/started/finished all past-tense agree

# composition(id|rule|content)
CO1|prefix as topic|noun describing what the data is about; "deployment" is topic; "deploy" would be verb-stage of deployment
CO2|specific to general|web_site_widget reads "widget within web_site"; deployment_approved_time reads "time of approval within deployment"
CO3|prefix hierarchy is namespace|each prefix layer narrows scope; sibling vs child relationships visible from prefix structure
CO4|consistent suffix tells type|_time always DATETIME; _date always DATE; _id always FK; immediate visual recognition
CO5|topic-prefix groups related fields|deployment_created_time+deployment_created_user_id+deployment_approved_time+deployment_approved_user_id share topic+stage prefixes; mappings between FKs and times are visually obvious

# fk_naming(id|rule|content|example)
FK1|FK column = referenced_table + referenced_field|standard form|company_id references company.id
FK2|FK to non-id field|table + field name|user_username references user.username
FK3|Multiple FKs to same target use purpose-prefix|prefix the role + standard FK name suffix|vendor_company_id+service_company_id (both → company.id)
FK4|Once role-prefix chosen reuse everywhere|consistent prefix across all contexts where role applies|vendor_company_id+vendor_employee_id (both use "vendor_" prefix)

# fk_disambiguation(aspect|content)
FD1|when prefixes don't collide|use natural role prefix (vendor_+service_+supplier_)
FD2|when prefixes collide across contexts|use the correct terminology in each context as long as no single context requires both
FD3|when single context requires both colliding prefixes|make prefixes unique even if one reads weirder; namespace cleanliness > smooth reading
FD4|principle|consistent label usage gives best namespace; words less unique than integers; field names are mnemonic helpers

# reserved_fields(field|type|purpose|notes)
RF1|id|INT auto_increment (usually)|primary key|every table
RF2|parent|INT FK to same-table.id|hierarchy reference|enables self-referential trees
RF3|created_time|DATETIME|record creation timestamp|set on insert
RF4|updated_time|DATETIME|record update timestamp|set on insert+update

# capitalization(context|convention|rationale|example)
CA1|Classes|CamelCaseFromStart|differentiated from variables by leading caps; rarely accessed in ambiguous ways|UserAccount
CA2|Methods/Functions|CamelCaseFromStart|same as classes because methods/functions outnumber classes; optimize for the more common case|GetUserAccount
CA3|Variables|lower_case_with_underscores|differentiated from classes/functions by leading lowercase; primary label form alongside keywords/builtins|user_account
CA4|Schema table+field names|lower_case_with_underscores|same as variables; database is data namespace not code namespace|user_account_id
CA5|Global variables|UPPER_CASE_WITH_UNDERSCORES|differentiated from local variables by case; visually distinct at use site|MAX_RETRY_COUNT
# rule: lowerCamelCase rejected because user (variable) ≠ User (class) is visible whereas user (camelCase variable) ≠ user (snake_case variable) is invisible at single-word names
# rule: where language differs from these standards comply with the language and apply DSNC where not using/overloading base language formats

# stage_tracking(aspect|content|example)
ST1|topic noun|the over-all topic; usually noun not verb (deployment not deploy; deploy is a stage)|deployment
ST2|stage suffix tense|all stages share same tense (past tense common); approved/deployed/started/finished all agree|deployment_approved_time+deployment_deployed_time
ST3|stage data combinations|each stage gets its own time + responsible user FK + any other stage data|deployment_created_time+deployment_created_user_id+deployment_approved_time+deployment_approved_user_id
ST4|standardized stage vocabulary|created+approved+deployed+started+finished are common stages with shared tense
ST5|new stages additive|adding new stage = adding new <topic>_<stage>_<suffix> fields; doesn't disturb existing stages

# deviations(aspect|content)
DV1|Column-store databases|column names are included in data storage so must be short; create descriptive name map and use short hashes as field names; lookup names externally
DV2|Document databases|same as column-store; field name overhead motivates abbreviation
DV3|exception is bounded|only when storage cost of long field names is structurally significant
DV4|principle elsewhere|don't shorten names just for typing convenience; long names are the documentation
DV5|language conformance|where target language has its own conventions go along with them; apply DSNC where not overloading base language formats

# relationships(from|rel|to)
P1|grounds|all-rules
P2|grounds|R03+R05+R06
P3|enables|spec-evolution
P4|enables|R02+CO1+ST3+stage-tracking-clarity
P5|enables|namespace-comprehension-at-scale
P6|enables|developer-skip-documentation-lookup
P7|justifies|rigid-rules-at-scale
R01|prevents|company-vs-companies-ambiguity
R01|enables|naming-without-language-specific-pluralization-rules
R02|differentiates_from|CA1+CA2+CA5
R03|implements|namespace-as-directory-tree
R04|implements|topic-first-composition
R05|distinguishes|sibling-from-child-via-prefix
R06|enables|prefix-grouping(web_*-family)
R07|prevents|synonym-drift
R08|enables|stage-scaling-with-ordering
R09|implements|consistent-role-labeling
R10|enforces|namespace-cleanliness-over-readability
PR1|always_means|present-state-boolean
PR2|always_means|past-event(boolean default; type via suffix)
SF1|always_type|DATETIME
SF2|always_type|DATE
SF3|combines|FK+conventional_user_reference
SF4|combines|table_name+id
SF5|paired_with|SF6
SF6|paired_with|SF5
SF7|enables|R08
TR1|tense_agrees_with|present-state-tracking
TR2|tense_agrees_with|past-event-tracking
TR3|combines|PR2+SF1
TR4|combines|PR2+SF5
TR5|combines|PR2+SF6
CO1|requires|noun-not-verb-as-topic
CO2|implements|R03
CO3|implements|namespace-hierarchy
CO4|implements|SF1+SF2+SF4
CO5|enables|visual-mapping-of-FKs-to-times
FK1|standard_form|true
FK2|extends|FK1-to-non-id-fields
FK3|disambiguates|multiple-FKs-to-same-target
FK4|implements|R09
FD1|prefers|natural-role-prefix
FD3|enforces|R10
RF1|present_in|every-table
RF2|enables|self-referential-hierarchies
RF3|paired_with|RF4
RF4|paired_with|RF3
CA1|differentiates_from|CA3+CA4
CA2|same_convention_as|CA1
CA3|same_convention_as|CA4
CA4|same_convention_as|CA3
CA5|differentiates_from|CA3+CA4
ST1|requires|topic-as-noun
ST2|requires|tense-agreement-across-stages
ST3|combines|topic+stage+suffix
ST4|standardizes|stage-vocabulary
ST5|implements|additive-evolution
DV1|exception_to|P4
DV2|exception_to|P4
DV4|reaffirms|P4
DV5|defers_to|host-language-conventions

# section_index(section|title|ids)
0|Spec Version|M1,M2,M3
1|No Plurals|R01
2|Capitalization|CA1,CA2,CA3,CA4,CA5
3|Default Tense|PR1,PR2,TR1,TR2,TR3,TR4,TR5
4|Use Common Phrases|R07,R08,SF5,SF6,SF7
5|Databases as Namespaces|P2,P7,R03,R05,R06,CO3
6|Compose Field Names|R03,R04,R05,R06,CO1,CO2,CO3,CO4,CO5
7|Foreign Key Field Names|FK1,FK2,FK3,FK4,FD1,FD2,FD3,FD4
8|Flag Booleans|PR1,PR2,TR1,TR2
9|Prefixes and Suffixes for Stages|ST1,ST2,ST3,ST4,ST5
10|Column Type Suffixes|SF1,SF2,SF3,SF4,CO4
11|Don't Avoid Long Names|P4,DV1,DV2,DV3,DV4
12|Make Your Own Rules|P3,P1
13|Reserved Field Names|RF1,RF2,RF3,RF4

# decode_legend
spec_version: 0000
naming_form: lower_case_with_underscores
plural_policy: never
case_for_classes_methods: CamelCaseFromStart
case_for_variables_schema: lower_case_with_underscores
case_for_globals: UPPER_CASE_WITH_UNDERSCORES
boolean_prefix_present: is_
boolean_prefix_past: was_
datetime_suffix: _time
date_suffix: _date
fk_suffix: _id (combined as table_name+_id)
fk_disambiguation: role_prefix + table_id (vendor_company_id)
hierarchy_axis: parent (FK to same table.id)
reserved_fields: id|parent|created_time|updated_time
stage_pattern: <topic>_<stage>_<suffix> (deployment_approved_time)
canonical_pair: _start_/_stop_ (never begin/end or start/finish)
scaling_axis: _phase_N_ (or _phase_NN_ or _phase_NNN_)
namespace_priority: cleanliness > readability when in conflict
long_names_principle: schema is self-documenting; documentation drifts; long names are the documentation
deviation_exception: column-store/document-store may shorten via name map (storage cost forces it)
language_exception: comply with host language conventions where they conflict; apply DSNC elsewhere
spec_evolution: P3 — make new rules for new cases; refine over time; rules are tools not laws
sot_for_naming: the convention; if convention dictates the name developers don't need to remember or look up
rel_types: grounds|enables|implements|prevents|justifies|prefers|differentiates_from|same_convention_as|always_means|always_type|combines|paired_with|exception_to|reaffirms|defers_to|extends|disambiguates|enforces|requires|tense_agrees_with|standardizes|distinguishes|standard_form|present_in|standardizes
