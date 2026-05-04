# OPSDB SCHEMA — LLM-COMPACT FORM
# Format: pipe-delimited tables, ID refs.
# Read order: conventions → patterns → reserved → governance → top-level → entities → fields → bridges → discriminators → enums → versioning → scope → relationships → sections

# conventions(id|rule|applies_to)
SC1|singular names|all-tables-and-fields
SC2|lower_case_with_underscores|all-names
SC3|hierarchical prefix specific-to-general|composite-names (web_site|web_site_widget)
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

# patterns(id|name|shape|when_used)
SP1|Universal Reserved Fields|id+created_time+updated_time on every table; parent_id when self-hierarchical; is_active when soft-deletable|all-tables
SP2|Versioning Sibling|*_version table with version_serial+parent_*_version_id+change_set_id+is_active_version|change-managed entities
SP3|Typed Payload|*_type discriminator + *_data_json validated against registered schema|heterogeneous data needs (cloud/k8s/policy/runner/etc)
SP4|Bridge Table per Target Type|one bridge table per source-target pair; clean FK integrity; columns specific to bridge possible|polymorphic relationships
SP5|Underscore Governance Prefix|fields prefixed _ for security/audit/schema/observation metadata|tables needing extra-policy fields
SP6|Hierarchical Self-FK|parent_id pointing to same table|location|hardware_component|megavisor_instance|service|policy|escalation_step|schemas
SP7|Configuration Variables Pattern|one table holds typed key-value scoped via scope_type+scope_id|helm-values|configmap|service-params|runner-params
SP8|Unified Substrate Hierarchy|megavisor_instance self-FK chain spans bare-metal+VM+container+pod+cloud|substrate-modeling
SP9|Unified Cache Tables|three tables (metric|state|config) keyed by source+key cover bulk of observation|observation-caching
SP10|Schema Self-Description|_schema_* tables register entities/fields/relationships; queryable like any table|schema-introspection

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

# top_level(id|category|section|scope)
ST1|Site and Location|5|DOS scope+physical/logical locations
ST2|Identity|5|users+groups+roles
ST3|Substrate|6|hardware+megavisor+machines+cloud-resources+storage
ST4|Service Abstraction|7|services+packages+interfaces+connections+host-groups
ST5|Kubernetes|8|clusters+nodes+namespaces+workloads+pods+helm+configmaps+secret-refs
ST6|Cloud Resources|9|generic resource modeling with provider-specific payloads
ST7|Authority Directory|10|typed pointers to monitoring+logs+secrets+docs+identity+code-repos
ST8|Schedules|11|when things happen
ST9|Policy|12|security-zones+classifications+retention+approval+escalation
ST10|Documentation Metadata|13|ownership+runbooks+dashboards+last-reviewed
ST11|Runners|14|specs+capabilities+jobs+output+targets
ST12|Monitoring and Alerting|15|monitors+alerts+on-call+suppression
ST13|Cached Observation|16|pulled state from authorities
ST14|Configuration Variables|17|typed key-value across many domains
ST15|Change Management|18|change-sets+approvals+approval-rules
ST16|Audit and Evidence|19|audit-log+evidence+compliance-findings
ST17|Schema Metadata|20|OpsDB record of own schema

# entities(id|name|section|category|versioned|sibling|parent|description)
SE1|site|5.1|identity|no|-|-|DOS scope within OpsDB
SE2|location|5.2|identity|no|-|self|hierarchical location (region/dc/cage/row/rack/cloud_region/cloud_zone/office/desk)
SE3|ops_user|5.3|identity|no|-|-|operational identity within site
SE4|ops_group|5.4|identity|no|-|-|access policy grouping
SE5|ops_group_member|5.4|identity|no|-|-|bridge: group↔user
SE6|ops_user_role|5.5|identity|no|-|-|operational position
SE7|ops_user_role_member|5.5|identity|no|-|-|bridge: role↔user with rotation_order
SE8|hardware_component|6.1|substrate|no|-|self|physical hardware part
SE9|hardware_port|6.2|substrate|no|-|-|connection point on component
SE10|hardware_set|6.3|substrate|no|-|-|hardware specification
SE11|hardware_set_component|6.3|substrate|no|-|-|bridge: set↔component+position
SE12|hardware_set_instance|6.4|substrate|no|-|-|physical instance in location
SE13|hardware_set_instance_port_connection|6.5|substrate|no|-|-|cable/peering record
SE14|megavisor|6.6|substrate|no|-|-|abstraction over hosting (bare_metal/kvm/vmware/xen/hyperv/docker/containerd/kubelet/firecracker/ec2/gce/azure_vm/lambda/cloudrun/fargate)
SE15|megavisor_instance|6.7|substrate|no|-|self|unified substrate hierarchy node
SE16|cloud_provider|6.8|substrate|no|-|-|cloud vendor identity
SE17|cloud_account|6.8|substrate|no|-|-|cloud provider account
SE18|cloud_resource|6.8|substrate|yes|cloud_resource_version|-|generic cloud resource with typed payload
SE19|storage_resource|6.9|substrate|no|-|-|storage abstraction over physical/cloud
SE20|platform|6.10|substrate|no|-|-|OS image build
SE21|machine|6.11|substrate|yes|machine_version|-|configured host
SE22|package|7.1|service|yes|package_version|-|installable functionality
SE23|package_interface|7.2|service|no|-|-|exposed interface (per package_version)
SE24|package_connection|7.2|service|no|-|-|outbound interface dependency (per package_version)
SE25|service|7.3|service|yes|service_version|self|operational role
SE26|service_package|7.4|service|no|-|-|bridge: service↔package_version with install_order
SE27|service_interface_mount|7.4|service|no|-|-|exposed interface for service version
SE28|service_connection|7.4|service|no|-|-|service-to-service connection (drives config+firewall+suppression+capacity)
SE29|host_group|7.5|service|no|-|-|host role assignment
SE30|host_group_machine|7.5|service|no|-|-|bridge: group↔machine
SE31|host_group_package|7.5|service|no|-|-|bridge: group↔package_version with install_order
SE32|site_location|7.6|service|no|-|-|per-service location preference with precedence_order
SE33|service_level|7.7|service|no|-|-|scaling+capacity rule
SE34|service_level_metric|7.7|service|no|-|-|SLO-driven scaling metric
SE35|k8s_cluster|8.1|k8s|yes|k8s_cluster_version|-|Kubernetes cluster (IS a service via service_id)
SE36|k8s_cluster_node|8.2|k8s|no|-|-|cluster node bridging to machine
SE37|k8s_namespace|8.3|k8s|no|-|-|cluster namespace
SE38|k8s_workload|8.4|k8s|yes|k8s_workload_version|-|deployment/statefulset/daemonset/job/cronjob/replicaset
SE39|k8s_pod|8.5|k8s|no|-|-|pod with link to megavisor_instance
SE40|k8s_helm_release|8.6|k8s|yes|k8s_helm_release_version|-|Helm release entity
SE41|k8s_config_map|8.7|k8s|yes|k8s_config_map_version|-|configmap entity (values in configuration_variable)
SE42|k8s_secret_reference|8.8|k8s|no|-|-|pointer to secret backend; never holds value
SE43|k8s_service|8.9|k8s|no|-|-|K8s service object; optional link to OpsDB service
SE44|authority|10.1|authority|no|-|-|external system owning slice of operational reality
SE45|authority_pointer|10.2|authority|no|-|-|typed reference to specific item within authority
SE46|service_authority_pointer|10.3|authority|no|-|-|bridge:service↔authority_pointer with relationship_role
SE47|machine_authority_pointer|10.3|authority|no|-|-|bridge:machine↔authority_pointer
SE48|k8s_cluster_authority_pointer|10.3|authority|no|-|-|bridge:k8s_cluster↔authority_pointer
SE49|cloud_resource_authority_pointer|10.3|authority|no|-|-|bridge:cloud_resource↔authority_pointer
SE50|schedule|11.1|schedule|yes|schedule_version|-|time-based or event-based trigger spec
SE51|runner_schedule|11.2|schedule|no|-|-|bridge:runner_spec↔schedule
SE52|credential_rotation_schedule|11.2|schedule|no|-|-|bridge:credential↔schedule
SE53|certificate_expiration_schedule|11.2|schedule|no|-|-|bridge:certificate↔schedule with warning_offsets
SE54|compliance_audit_schedule|11.2|schedule|no|-|-|bridge:compliance_regime↔schedule with audit_scope
SE55|manual_operation_schedule|11.2|schedule|no|-|-|bridge:manual_operation↔schedule
SE56|manual_operation|11.3|schedule|no|-|-|operational task humans perform
SE57|policy|12.1|policy|yes|policy_version|-|organizational rule with typed payload
SE58|service_policy|12.2|policy|no|-|-|bridge:service↔policy
SE59|machine_policy|12.2|policy|no|-|-|bridge:machine↔policy
SE60|k8s_namespace_policy|12.2|policy|no|-|-|bridge:k8s_namespace↔policy
SE61|cloud_account_policy|12.2|policy|no|-|-|bridge:cloud_account↔policy
SE62|security_zone|12.3|policy|no|-|-|operational security scope
SE63|security_zone_membership_service|12.3|policy|no|-|-|bridge:zone↔service
SE64|security_zone_membership_machine|12.3|policy|no|-|-|bridge:zone↔machine
SE65|security_zone_membership_k8s_namespace|12.3|policy|no|-|-|bridge:zone↔namespace
SE66|data_classification|12.4|policy|no|-|-|data sensitivity level
SE67|retention_policy|12.5|policy|no|-|-|per-entity-type retention horizon
SE68|approval_rule|12.6|policy|no|-|-|policy declaring approval requirements per change
SE69|escalation_path|12.7|policy|no|-|-|named alert escalation policy
SE70|escalation_step|12.7|policy|no|-|self|step within escalation_path with step_order
SE71|service_escalation_path|12.7|policy|no|-|-|bridge:service↔escalation_path with severity threshold
SE72|change_management_rule|12.8|policy|no|-|-|policy data governing change-mgmt behavior
SE73|compliance_regime|12.9|policy|no|-|-|regulatory regime declaration
SE74|compliance_scope_service|12.9|policy|no|-|-|bridge:regime↔service
SE75|compliance_scope_data_classification|12.9|policy|no|-|-|bridge:regime↔data_classification
SE76|service_ownership|13.1|docs|no|-|-|bridge:service↔ops_user_role with ownership_role
SE77|machine_ownership|13.1|docs|no|-|-|bridge:machine↔ops_user_role
SE78|k8s_cluster_ownership|13.1|docs|no|-|-|bridge:k8s_cluster↔ops_user_role
SE79|cloud_resource_ownership|13.1|docs|no|-|-|bridge:cloud_resource↔ops_user_role
SE80|service_stakeholder|13.2|docs|no|-|-|bridge:service↔ops_user_role with stakeholder_role
SE81|runbook_reference|13.3|docs|no|-|-|structured runbook pointer with metadata
SE82|service_runbook_reference|13.3|docs|no|-|-|bridge:service↔runbook with purpose
SE83|dashboard_reference|13.4|docs|no|-|-|structured dashboard pointer with metadata
SE84|service_dashboard_reference|13.4|docs|no|-|-|bridge:service↔dashboard with purpose
SE85|runner_spec|14.1|runner|yes|runner_spec_version|-|runner kind specification
SE86|runner_capability|14.2|runner|no|-|-|declared runner capability
SE87|runner_machine|14.3|runner|no|-|-|bridge:machine↔runner_spec with capacity
SE88|runner_instance|14.4|runner|no|-|-|live runner process
SE89|runner_service_target|14.5|runner|no|-|-|bridge:runner_spec↔service
SE90|runner_host_group_target|14.5|runner|no|-|-|bridge:runner_spec↔host_group
SE91|runner_k8s_namespace_target|14.5|runner|no|-|-|bridge:runner_spec↔k8s_namespace
SE92|runner_cloud_account_target|14.5|runner|no|-|-|bridge:runner_spec↔cloud_account
SE93|runner_job|14.6|runner|no|-|-|runtime record of runner execution
SE94|runner_job_target_machine|14.6|runner|no|-|-|bridge:job↔machine with per-target status
SE95|runner_job_target_service|14.6|runner|no|-|-|bridge:job↔service
SE96|runner_job_target_k8s_workload|14.6|runner|no|-|-|bridge:job↔k8s_workload
SE97|runner_job_target_cloud_resource|14.6|runner|no|-|-|bridge:job↔cloud_resource
SE98|runner_job_output_var|14.7|runner|no|-|-|discrete output variable from job
SE99|monitor|15.1|monitor|no|-|-|owned by package; defines a check
SE100|monitor_machine_target|15.2|monitor|no|-|-|bridge:monitor↔machine
SE101|monitor_service_target|15.2|monitor|no|-|-|bridge:monitor↔service
SE102|monitor_k8s_workload_target|15.2|monitor|no|-|-|bridge:monitor↔k8s_workload
SE103|monitor_cloud_resource_target|15.2|monitor|no|-|-|bridge:monitor↔cloud_resource
SE104|prometheus_config|15.3|monitor|no|-|-|prometheus configuration owned by authority
SE105|prometheus_scrape_target|15.3|monitor|no|-|-|scrape target within prometheus_config
SE106|monitor_level|15.4|monitor|no|-|-|condition-action grouping; ANDs by name
SE107|alert|15.6|monitor|no|-|-|named alert condition with severity scoped to service
SE108|alert_dependency|15.6|monitor|no|-|-|suppression relationship between alerts
SE109|alert_fire|15.6|monitor|no|-|-|specific firing instance of alert
SE110|on_call_schedule|15.7|monitor|no|-|-|schedule + role linkage
SE111|on_call_assignment|15.7|monitor|no|-|-|specific on-call assignment over window
SE112|observation_cache_metric|16.1|observation|no|-|-|cached metric data keyed by authority+hostname+metric_key
SE113|observation_cache_state|16.1|observation|no|-|-|cached state data keyed by entity_type+entity_id+state_key
SE114|observation_cache_config|16.1|observation|no|-|-|cached config data keyed by authority+hostname+config_key
SE115|configuration_variable|17.1|config-vars|yes|configuration_variable_version|-|typed key-value scoped to entity via scope_type+scope_id
SE116|change_set|18.1|change-mgmt|no|-|-|bundled proposed changes
SE117|change_set_field_change|18.2|change-mgmt|no|-|-|per-field change record
SE118|change_set_approval_required|18.3|change-mgmt|no|-|-|computed approval requirement
SE119|change_set_approval|18.4|change-mgmt|no|-|-|recorded approval
SE120|change_set_rejection|18.5|change-mgmt|no|-|-|rejection record
SE121|change_set_validation|18.6|change-mgmt|no|-|-|validation outcome record
SE122|change_set_emergency_review|18.7|change-mgmt|no|-|-|post-hoc review of emergency changes
SE123|change_set_bulk_membership|18.8|change-mgmt|no|-|-|structure within bulk change sets
SE124|audit_log_entry|19.1|audit|append-only|-|-|append-only API action record
SE125|evidence_record|19.2|audit|no|-|-|verification outcome from runner or human
SE126|evidence_record_service_target|19.3|audit|no|-|-|bridge:evidence↔service
SE127|evidence_record_machine_target|19.3|audit|no|-|-|bridge:evidence↔machine
SE128|evidence_record_credential_target|19.3|audit|no|-|-|bridge:evidence↔credential
SE129|evidence_record_certificate_target|19.3|audit|no|-|-|bridge:evidence↔certificate
SE130|evidence_record_compliance_regime_target|19.3|audit|no|-|-|bridge:evidence↔regime
SE131|evidence_record_manual_operation_target|19.3|audit|no|-|-|bridge:evidence↔manual_operation
SE132|compliance_finding|19.4|audit|no|-|-|filed compliance gap or observation
SE133|compliance_finding_target_service|19.4|audit|no|-|-|bridge:finding↔service
SE134|_schema_version|20.1|schema-meta|no|-|self|canonical schema version
SE135|_schema_change_set|20.2|schema-meta|no|-|self|schema evolution change set
SE136|_schema_entity_type|20.3|schema-meta|no|-|-|registry of entity types
SE137|_schema_field|20.4|schema-meta|no|-|-|registry of fields
SE138|_schema_relationship|20.5|schema-meta|no|-|-|registry of relationships

# fields(entity|field|type|nullable|fk|notes)
# format: only distinguishing fields; reserved (id|created_time|updated_time|is_active) implicit
# +V means versioning sibling fields also apply
SE1|name|VARCHAR|n||
SE1|description|TEXT|y||
SE1|domain|VARCHAR|n||
SE2|site_id|FK|n|SE1|
SE2|name|VARCHAR|n||
SE2|location_type|VARCHAR|n||region|datacenter|cage|row|rack|cloud_region|cloud_zone|office|desk
SE2|latitude|FLOAT|y||resolved by walking up
SE2|longitude|FLOAT|y||resolved by walking up
SE3|site_id|FK|n|SE1|
SE3|username|VARCHAR|n||
SE3|fullname|VARCHAR|n||
SE3|email|VARCHAR|n||
SE4|site_id|FK|n|SE1|
SE4|name|VARCHAR|n||
SE4|description|TEXT|y||
SE5|ops_group_id|FK|n|SE4|
SE5|ops_user_id|FK|n|SE3|
SE6|site_id|FK|n|SE1|
SE6|name|VARCHAR|n||
SE6|description|TEXT|y||
SE7|ops_user_role_id|FK|n|SE6|
SE7|ops_user_id|FK|n|SE3|
SE7|rotation_order|INT|y||for on-call rotation
SE8|name|VARCHAR|n||
SE8|manufacturer|VARCHAR|n||
SE8|model|VARCHAR|n||
SE8|hardware_component_type|VARCHAR|n||chassis|motherboard|cpu|ram|disk|psu|nic|hba|fan|gpu
SE8|parent_hardware_component_id|FK|y|SE8|
SE8|rack_unit_height|INT|y||chassis-class only
SE9|hardware_component_id|FK|n|SE8|
SE9|name|VARCHAR|n||
SE9|media_type|VARCHAR|n||rj45|fiber|sfp|db9|c13|c19|usb|hdmi
SE9|resource_type|VARCHAR|n||network|power_110|power_220|serial|video|kvm|storage|management
SE9|direction|VARCHAR|n||provider|consumer|bidirectional
SE10|name|VARCHAR|n||
SE10|description|TEXT|y||
SE11|hardware_set_id|FK|n|SE10|
SE11|hardware_component_id|FK|n|SE8|
SE11|position_label|VARCHAR|n||cpu_0|ram_slot_3
SE12|hardware_set_id|FK|n|SE10|
SE12|location_id|FK|n|SE2|
SE12|rack_unit_mount_height|INT|n||absolute position in rack
SE12|serial_number|VARCHAR|n||
SE12|asset_tag|VARCHAR|n||
SE12|decommissioned_time|DATETIME|y||
SE13|source_hardware_set_instance_id|FK|n|SE12|
SE13|source_hardware_port_id|FK|n|SE9|
SE13|destination_hardware_set_instance_id|FK|n|SE12|
SE13|destination_hardware_port_id|FK|n|SE9|
SE13|cable_label|VARCHAR|y||
SE14|name|VARCHAR|n||
SE14|megavisor_type|VARCHAR|n||see entity-description
SE14|version|VARCHAR|n||
SE15|parent_megavisor_instance_id|FK|y|SE15|self-FK; nesting
SE15|megavisor_id|FK|n|SE14|
SE15|hardware_set_instance_id|FK|y|SE12|set only at bare-metal root
SE15|cloud_resource_id|FK|y|SE18|set when this instance is cloud compute
SE15|location_id|FK|n|SE2|cached for query speed
SE15|external_id|VARCHAR|n||VM UUID|container ID|pod UID|EC2 ID
SE15|hostname|VARCHAR|n||
SE15|ip_primary|VARCHAR|n||
SE15|is_running|BOOL|n||
SE15|provisioned_time|DATETIME|y||
SE15|decommissioned_time|DATETIME|y||
SE16|name|VARCHAR|n||aws|azure|gcp|digital_ocean|hetzner|oracle
SE17|cloud_provider_id|FK|n|SE16|
SE17|site_id|FK|n|SE1|
SE17|name|VARCHAR|n||
SE17|account_external_id|VARCHAR|n||AWS account ID|Azure tenant|GCP project
SE18|cloud_account_id|FK|n|SE17|
SE18|location_id|FK|n|SE2|cloud_region or cloud_zone
SE18|cloud_resource_type|VARCHAR|n||discriminator; see SD1
SE18|external_id|VARCHAR|n||ARN|resource ID|self-link
SE18|name|VARCHAR|n||
SE18|cloud_data_json|JSON|n||typed by cloud_resource_type
SE18|provisioned_time|DATETIME|y||
SE18|decommissioned_time|DATETIME|y||
SE18|+V|||cloud_resource_version
SE19|cloud_resource_id|FK|y|SE18|set if cloud-backed
SE19|hardware_set_instance_id|FK|y|SE12|set if physical-backed
SE19|storage_resource_type|VARCHAR|n||ebs|s3|gcs|azure_blob|nfs_export|ceph_rbd|local_disk|iscsi
SE19|size_bytes|BIGINT|n||
SE19|storage_data_json|JSON|n||backend-specific (iops|replication)
SE20|name|VARCHAR|n||
SE20|os_family|VARCHAR|n||linux|windows|freebsd|darwin
SE20|os_version|VARCHAR|n||
SE20|architecture|VARCHAR|n||x86_64|arm64|riscv64
SE20|is_approved_for_production|BOOL|n||
SE21|megavisor_instance_id|FK|n|SE15|
SE21|fqdn|VARCHAR|n||
SE21|host_group_id|FK|n|SE29|single host group
SE21|platform_id|FK|n|SE20|
SE21|is_under_management|BOOL|n||kill switch
SE21|bootstrapped_time|DATETIME|y||
SE21|last_converged_time|DATETIME|y||
SE21|+V|||machine_version
SE22|name|VARCHAR|n||nginx|postgres|kubelet|datadog-agent
SE22|package_type|VARCHAR|n||platform|service|sidecar|agent
SE22|description|TEXT|y||
SE22|+V|||package_version with package_data_json
SE23|package_version_id|FK|n|SE22|
SE23|name|VARCHAR|n||http|syslog_listener|metrics_scrape
SE23|interface_type|VARCHAR|n||transaction|message|resource
SE23|protocol|VARCHAR|n||tcp|udp|unix_socket|http|grpc
SE23|default_port|INT|y||
SE23|description|TEXT|y||
SE24|package_version_id|FK|n|SE22|
SE24|name|VARCHAR|n||syslog_upstream|database_primary
SE24|target_interface_name|VARCHAR|n||name of interface to connect to
SE24|is_required|BOOL|n||
SE24|description|TEXT|y||
SE25|site_id|FK|n|SE1|
SE25|name|VARCHAR|n||
SE25|description|TEXT|y||
SE25|service_type|VARCHAR|n||standard|database|k8s_cluster_member|cloud_managed
SE25|parent_service_id|FK|y|SE25|service hierarchies
SE25|+V|||service_version
SE26|service_version_id|FK|n|SE25|
SE26|package_version_id|FK|n|SE22|
SE26|install_order|INT|n||
SE27|service_version_id|FK|n|SE25|
SE27|package_interface_id|FK|n|SE23|
SE27|exposed_name|VARCHAR|n||
SE27|exposed_port|INT|y||override package default
SE27|exposed_protocol|VARCHAR|y||
SE27|is_external|BOOL|n||accepts external traffic
SE28|source_service_version_id|FK|n|SE25|
SE28|destination_service_id|FK|n|SE25|
SE28|destination_service_interface_mount_id|FK|n|SE27|
SE28|source_package_connection_id|FK|n|SE24|
SE28|is_required|BOOL|n||
SE29|site_id|FK|n|SE1|
SE29|name|VARCHAR|n||database|k8s_worker|edge_proxy
SE29|description|TEXT|y||
SE29|domain|VARCHAR|y||FQDN suffix
SE30|host_group_id|FK|n|SE29|
SE30|machine_id|FK|n|SE21|
SE31|host_group_id|FK|n|SE29|
SE31|package_version_id|FK|n|SE22|
SE31|install_order|INT|n||
SE32|site_id|FK|n|SE1|
SE32|service_id|FK|n|SE25|
SE32|location_id|FK|n|SE2|
SE32|precedence_order|INT|n||0 most-preferred
SE33|service_version_id|FK|n|SE25|
SE33|site_location_id|FK|n|SE32|
SE33|hardware_set_id|FK|y|SE10|hardware constraint
SE33|machine_count_minimum|INT|n||
SE33|machine_count_maximum|INT|n||
SE33|service_level_metric_id|FK|y|SE34|SLO-driven scaling
SE34|name|VARCHAR|n||
SE34|metric_query|TEXT|n||PromQL or similar
SE34|threshold_value|FLOAT|n||
SE34|threshold_operator|VARCHAR|n||gt|lt|gte|lte
SE34|rate_change_minimum_time_seconds|INT|n||prevents oscillation
SE35|service_id|FK|n|SE25|cluster IS a service
SE35|site_id|FK|n|SE1|
SE35|name|VARCHAR|n||
SE35|k8s_distribution|VARCHAR|n||vanilla|eks|gke|aks|openshift|rancher|k3s|talos
SE35|k8s_version|VARCHAR|n||
SE35|api_endpoint_fqdn|VARCHAR|n||
SE35|+V|||k8s_cluster_version
SE36|k8s_cluster_id|FK|n|SE35|
SE36|machine_id|FK|n|SE21|underlying machine in substrate
SE36|node_role|VARCHAR|n||control_plane|worker|etcd|ingress
SE36|is_schedulable|BOOL|n||
SE36|joined_time|DATETIME|y||
SE37|k8s_cluster_id|FK|n|SE35|
SE37|name|VARCHAR|n||
SE38|k8s_cluster_id|FK|n|SE35|
SE38|k8s_namespace_id|FK|n|SE37|
SE38|name|VARCHAR|n||
SE38|workload_type|VARCHAR|n||deployment|statefulset|daemonset|job|cronjob|replicaset
SE38|+V|||k8s_workload_version with workload_data_json
SE39|megavisor_instance_id|FK|n|SE15|bridge into unified substrate
SE39|k8s_workload_id|FK|n|SE38|
SE39|k8s_namespace_id|FK|n|SE37|
SE39|k8s_cluster_node_id|FK|n|SE36|
SE39|name|VARCHAR|n||
SE39|pod_uid|VARCHAR|n||
SE39|is_running|BOOL|n||
SE39|scheduled_time|DATETIME|y||
SE40|k8s_cluster_id|FK|n|SE35|
SE40|k8s_namespace_id|FK|n|SE37|
SE40|name|VARCHAR|n||
SE40|chart_name|VARCHAR|n||
SE40|chart_version|VARCHAR|n||
SE40|installed_time|DATETIME|y||
SE40|+V|||k8s_helm_release_version; values stored in configuration_variable
SE41|k8s_cluster_id|FK|n|SE35|
SE41|k8s_namespace_id|FK|n|SE37|
SE41|name|VARCHAR|n||
SE41|+V|||k8s_config_map_version; contents stored in configuration_variable
SE42|k8s_cluster_id|FK|n|SE35|
SE42|k8s_namespace_id|FK|n|SE37|
SE42|name|VARCHAR|n||
SE42|secret_type|VARCHAR|n||opaque|tls|dockerconfigjson|service_account_token|basic_auth
SE42|secret_backend_id|FK|n|SE44|authority typed secret_vault
SE42|secret_backend_path|VARCHAR|n||where actual secret lives
SE43|k8s_cluster_id|FK|n|SE35|
SE43|k8s_namespace_id|FK|n|SE37|
SE43|name|VARCHAR|n||
SE43|k8s_service_type|VARCHAR|n||cluster_ip|node_port|load_balancer|external_name|headless
SE43|service_id|FK|y|SE25|optional link to OpsDB service
SE44|site_id|FK|n|SE1|
SE44|name|VARCHAR|n||
SE44|authority_type|VARCHAR|n||see entity-description
SE44|base_url|VARCHAR|n||
SE44|authority_data_json|JSON|n||typed by authority_type
SE45|authority_id|FK|n|SE44|
SE45|pointer_type|VARCHAR|n||metric|log_query|secret|dashboard|runbook|wiki_page|ticket|code_path|chat_thread|artifact|container_image
SE45|locator|VARCHAR|n||path/identifier within authority
SE45|pointer_data_json|JSON|n||type-specific
SE45|last_verified_time|DATETIME|y||rot tracking
SE46|service_id|FK|n|SE25|
SE46|authority_pointer_id|FK|n|SE45|
SE46|relationship_role|VARCHAR|n||primary_dashboard|runbook|log_query|metric_namespace|status_page|on_call_handoff
SE47|machine_id|FK|n|SE21|
SE47|authority_pointer_id|FK|n|SE45|
SE47|relationship_role|VARCHAR|n||
SE48|k8s_cluster_id|FK|n|SE35|
SE48|authority_pointer_id|FK|n|SE45|
SE48|relationship_role|VARCHAR|n||
SE49|cloud_resource_id|FK|n|SE18|
SE49|authority_pointer_id|FK|n|SE45|
SE49|relationship_role|VARCHAR|n||
SE50|site_id|FK|n|SE1|
SE50|name|VARCHAR|n||
SE50|schedule_type|VARCHAR|n||cron_expression|rate_based|event_triggered|calendar_anchored|deadline_driven|manual
SE50|schedule_data_json|JSON|n||typed by schedule_type
SE50|description|TEXT|y||
SE50|+V|||schedule_version
SE51|runner_spec_id|FK|n|SE85|
SE51|schedule_id|FK|n|SE50|
SE51|service_id|FK|y|SE25|what service scheduling targets
SE52|credential_id|FK|n|external|implies a credential entity (referenced not detailed)
SE52|schedule_id|FK|n|SE50|
SE53|certificate_id|FK|n|external|implies certificate entity
SE53|schedule_id|FK|n|SE50|
SE53|warning_offsets_data_json|JSON|y||
SE54|compliance_regime_id|FK|n|SE73|
SE54|schedule_id|FK|n|SE50|
SE54|audit_scope_data_json|JSON|y||
SE55|manual_operation_id|FK|n|SE56|
SE55|schedule_id|FK|n|SE50|
SE56|site_id|FK|n|SE1|
SE56|name|VARCHAR|n||
SE56|description|TEXT|y||
SE56|manual_operation_type|VARCHAR|n||tape_rotation|vendor_review|keycard_audit|license_renewal|contract_renewal|evidence_collection|physical_inspection
SE56|manual_operation_data_json|JSON|n||typed
SE56|responsible_ops_user_role_id|FK|n|SE6|
SE57|site_id|FK|n|SE1|
SE57|name|VARCHAR|n||
SE57|policy_type|VARCHAR|n||security_zone|data_classification|retention|approval_rule|escalation|change_management|schedule_governance|access_control|compliance_scope
SE57|policy_data_json|JSON|n||typed by policy_type
SE57|description|TEXT|y||
SE57|_requires_group|VARCHAR|y||governance
SE57|+V|||policy_version
SE58|service_id|FK|n|SE25|
SE58|policy_id|FK|n|SE57|
SE59|machine_id|FK|n|SE21|
SE59|policy_id|FK|n|SE57|
SE60|k8s_namespace_id|FK|n|SE37|
SE60|policy_id|FK|n|SE57|
SE61|cloud_account_id|FK|n|SE17|
SE61|policy_id|FK|n|SE57|
SE62|site_id|FK|n|SE1|
SE62|name|VARCHAR|n||production|corp|pci_cardholder|phi_processing|dmz
SE62|description|TEXT|y||
SE62|zone_data_json|JSON|n||required controls+threat model
SE63|security_zone_id|FK|n|SE62|
SE63|service_id|FK|n|SE25|
SE64|security_zone_id|FK|n|SE62|
SE64|machine_id|FK|n|SE21|
SE65|security_zone_id|FK|n|SE62|
SE65|k8s_namespace_id|FK|n|SE37|
SE66|site_id|FK|n|SE1|
SE66|name|VARCHAR|n||public|internal|confidential|restricted|regulated_pci|regulated_phi|regulated_pii
SE66|description|TEXT|y||
SE66|classification_data_json|JSON|y||
SE67|site_id|FK|n|SE1|
SE67|name|VARCHAR|n||production_30_day|compliance_7_year|infinite_history|ephemeral
SE67|retention_type|VARCHAR|n||time_bounded|count_bounded|hybrid|infinite
SE67|retention_data_json|JSON|n||horizon config
SE68|site_id|FK|n|SE1|
SE68|name|VARCHAR|n||
SE68|rule_data_json|JSON|n||matching predicate + approval requirements
SE69|site_id|FK|n|SE1|
SE69|name|VARCHAR|n||
SE69|description|TEXT|y||
SE70|escalation_path_id|FK|n|SE69|
SE70|step_order|INT|n||
SE70|step_type|VARCHAR|n||notify_role|notify_user|page_role|page_user|wait_seconds|branch_on_acknowledge
SE70|step_data_json|JSON|n||
SE71|service_id|FK|n|SE25|
SE71|escalation_path_id|FK|n|SE69|
SE71|trigger_alert_severity_minimum|VARCHAR|n||
SE72|site_id|FK|n|SE1|
SE72|name|VARCHAR|n||
SE72|rule_data_json|JSON|n||when applies+shape+emergency-path+bulk-handling
SE73|site_id|FK|n|SE1|
SE73|name|VARCHAR|n||SOC2_TYPE2|ISO27001|PCI_DSS|HIPAA|FedRAMP_MODERATE|GDPR|SOX_ITGC
SE73|description|TEXT|y||
SE73|regime_data_json|JSON|n||scoping+control mapping+audit cycle
SE74|compliance_regime_id|FK|n|SE73|
SE74|service_id|FK|n|SE25|
SE75|compliance_regime_id|FK|n|SE73|
SE75|data_classification_id|FK|n|SE66|
SE76|service_id|FK|n|SE25|
SE76|ops_user_role_id|FK|n|SE6|
SE76|ownership_role|VARCHAR|n||owner|technical_owner|business_owner|support_owner
SE77|machine_id|FK|n|SE21|
SE77|ops_user_role_id|FK|n|SE6|
SE77|ownership_role|VARCHAR|n||
SE78|k8s_cluster_id|FK|n|SE35|
SE78|ops_user_role_id|FK|n|SE6|
SE78|ownership_role|VARCHAR|n||
SE79|cloud_resource_id|FK|n|SE18|
SE79|ops_user_role_id|FK|n|SE6|
SE79|ownership_role|VARCHAR|n||
SE80|service_id|FK|n|SE25|
SE80|ops_user_role_id|FK|n|SE6|
SE80|stakeholder_role|VARCHAR|n||consumer|dependency_owner|compliance_reviewer|security_reviewer
SE81|authority_pointer_id|FK|n|SE45|points at runbook in wiki
SE81|last_reviewed_time|DATETIME|y||
SE81|last_tested_time|DATETIME|y||
SE81|next_review_due_time|DATETIME|y||
SE81|reviewer_ops_user_id|FK|y|SE3|
SE81|tester_ops_user_id|FK|y|SE3|
SE82|service_id|FK|n|SE25|
SE82|runbook_reference_id|FK|n|SE81|
SE82|runbook_purpose|VARCHAR|n||oncall_response|deployment|disaster_recovery|security_incident|capacity_response
SE83|authority_pointer_id|FK|n|SE45|
SE83|last_reviewed_time|DATETIME|y||
SE84|service_id|FK|n|SE25|
SE84|dashboard_reference_id|FK|n|SE83|
SE84|dashboard_purpose|VARCHAR|n||primary|capacity|error_budget|security|dependency
SE85|site_id|FK|n|SE1|
SE85|name|VARCHAR|n||
SE85|runner_spec_type|VARCHAR|n||see SD12
SE85|description|TEXT|y||
SE85|runner_image_reference|VARCHAR|n||container image|binary path|repo locator
SE85|runner_entrypoint|VARCHAR|y||
SE85|+V|||runner_spec_version with runner_data_json
SE86|runner_spec_id|FK|n|SE85|
SE86|capability_name|VARCHAR|n||yum_install|k8s_apply|ec2_provision|template_render|secret_resolve|prometheus_query|tape_verify|keycard_revoke|license_check
SE86|capability_data_json|JSON|y||
SE87|machine_id|FK|n|SE21|
SE87|runner_spec_id|FK|n|SE85|
SE87|capacity_concurrent_jobs|INT|n||
SE88|runner_machine_id|FK|n|SE87|
SE88|external_id|VARCHAR|n||PID|container ID
SE88|is_running|BOOL|n||
SE88|started_time|DATETIME|y||
SE88|stopped_time|DATETIME|y||
SE89|runner_spec_id|FK|n|SE85|
SE89|service_id|FK|n|SE25|
SE90|runner_spec_id|FK|n|SE85|
SE90|host_group_id|FK|n|SE29|
SE91|runner_spec_id|FK|n|SE85|
SE91|k8s_namespace_id|FK|n|SE37|
SE92|runner_spec_id|FK|n|SE85|
SE92|cloud_account_id|FK|n|SE17|
SE93|runner_spec_id|FK|n|SE85|
SE93|runner_instance_id|FK|n|SE88|
SE93|scheduled_time|DATETIME|y||
SE93|started_time|DATETIME|y||
SE93|finished_time|DATETIME|y||
SE93|job_status|VARCHAR|n||pending|running|succeeded|failed|cancelled|timeout
SE93|job_input_data_json|JSON|n||
SE93|job_output_data_json|JSON|y||
SE93|job_log_text|TEXT|y||stdout/stderr summary
SE94|runner_job_id|FK|n|SE93|
SE94|machine_id|FK|n|SE21|
SE94|per_target_status|VARCHAR|n||
SE94|per_target_data_json|JSON|y||
SE95|runner_job_id|FK|n|SE93|
SE95|service_id|FK|n|SE25|
SE95|per_target_status|VARCHAR|n||
SE95|per_target_data_json|JSON|y||
SE96|runner_job_id|FK|n|SE93|
SE96|k8s_workload_id|FK|n|SE38|
SE96|per_target_status|VARCHAR|n||
SE96|per_target_data_json|JSON|y||
SE97|runner_job_id|FK|n|SE93|
SE97|cloud_resource_id|FK|n|SE18|
SE97|per_target_status|VARCHAR|n||
SE97|per_target_data_json|JSON|y||
SE98|runner_job_id|FK|n|SE93|
SE98|var_name|VARCHAR|n||
SE98|var_value|TEXT|n||
SE98|var_type|VARCHAR|n||string|int|float|bool|json
SE99|package_version_id|FK|n|SE22|monitors owned by packages
SE99|name|VARCHAR|n||
SE99|monitor_type|VARCHAR|n||script_local|script_remote|prometheus_query|http_probe|tcp_probe|cloud_metric|k8s_event_watch
SE99|monitor_data_json|JSON|n||spec for runner
SE99|collection_interval_seconds|INT|n||
SE100|monitor_id|FK|n|SE99|
SE100|machine_id|FK|n|SE21|
SE101|monitor_id|FK|n|SE99|
SE101|service_id|FK|n|SE25|
SE102|monitor_id|FK|n|SE99|
SE102|k8s_workload_id|FK|n|SE38|
SE103|monitor_id|FK|n|SE99|
SE103|cloud_resource_id|FK|n|SE18|
SE104|authority_id|FK|n|SE44|the prometheus server
SE104|service_id|FK|y|SE25|service-scoped if set
SE104|config_data_json|JSON|n||
SE105|prometheus_config_id|FK|n|SE104|
SE105|target_url|VARCHAR|n||
SE105|scrape_interval_seconds|INT|n||
SE105|metrics_path|VARCHAR|n||
SE105|scrape_data_json|JSON|y||
SE106|monitor_id|FK|n|SE99|
SE106|name|VARCHAR|n||AND-grouping name
SE106|condition_expression|TEXT|n||PromQL or comparator
SE106|condition_data_json|JSON|y||
SE106|action_type|VARCHAR|n||set_state|set_trigger|set_alert
SE106|action_target_id|INT|n||polymorphic by action_type
SE107|service_id|FK|n|SE25|
SE107|name|VARCHAR|n||
SE107|description|TEXT|y||
SE107|alert_severity|VARCHAR|n||info|warning|critical|page
SE108|parent_alert_id|FK|n|SE107|if firing child suppressed
SE108|child_alert_id|FK|n|SE107|
SE109|alert_id|FK|n|SE107|
SE109|fired_time|DATETIME|n||
SE109|cleared_time|DATETIME|y||
SE109|is_acknowledged|BOOL|n||
SE109|acknowledging_ops_user_id|FK|y|SE3|
SE109|acknowledged_time|DATETIME|y||
SE109|acknowledge_suppression_until_time|DATETIME|y||
SE109|alert_fire_data_json|JSON|y||
SE110|ops_user_role_id|FK|n|SE6|
SE110|schedule_id|FK|n|SE50|
SE110|rotation_data_json|JSON|y||
SE111|on_call_schedule_id|FK|n|SE110|
SE111|ops_user_id|FK|n|SE3|
SE111|on_call_start_time|DATETIME|n||
SE111|on_call_stop_time|DATETIME|n||
SE112|authority_id|FK|n|SE44|
SE112|hostname|VARCHAR|n||
SE112|metric_key|VARCHAR|n||metric name + labels normalized
SE112|metric_value|FLOAT|n||
SE112|metric_data_json|JSON|y||additional labels+metadata
SE112|_observed_time|DATETIME|n||
SE112|_puller_runner_job_id|FK|n|SE93|
SE113|entity_type|VARCHAR|n||machine|k8s_pod|cloud_resource|etc
SE113|entity_id|INT|n||interpreted with entity_type
SE113|state_key|VARCHAR|n||process_count|disk_pct_used|pod_phase
SE113|state_value|VARCHAR|n||
SE113|state_data_json|JSON|y||
SE113|_observed_time|DATETIME|n||
SE113|_puller_runner_job_id|FK|n|SE93|
SE114|authority_id|FK|n|SE44|
SE114|hostname|VARCHAR|y||host-scoped configs
SE114|config_key|VARCHAR|n||
SE114|config_value|TEXT|n||
SE114|config_data_json|JSON|y||
SE114|_observed_time|DATETIME|n||
SE114|_puller_runner_job_id|FK|n|SE93|
SE115|scope_type|VARCHAR|n||helm_release_version|k8s_config_map_version|service_version|runner_spec_version|package_version|host_group|machine|service|k8s_namespace
SE115|scope_id|INT|n||interpreted with scope_type
SE115|variable_key|VARCHAR|n||
SE115|variable_value|TEXT|n||
SE115|variable_type|VARCHAR|n||string|int|float|bool|json|secret_reference
SE115|variable_data_json|JSON|y||json values too large or secret refs
SE115|is_sensitive|BOOL|n||affects logging+display
SE115|_access_classification|VARCHAR|y||
SE115|+V|||configuration_variable_version
SE116|site_id|FK|n|SE1|
SE116|name|VARCHAR|n||
SE116|description|TEXT|y||
SE116|proposed_by_ops_user_id|FK|y|SE3|set if human-proposed
SE116|proposed_by_runner_job_id|FK|y|SE93|set if runner-proposed
SE116|change_set_status|VARCHAR|n||see SD13
SE116|reason_text|TEXT|n||
SE116|ticket_pointer_authority_pointer_id|FK|y|SE45|
SE116|is_emergency|BOOL|n||
SE116|is_bulk|BOOL|n||
SE116|expected_apply_time|DATETIME|y||
SE116|applied_time|DATETIME|y||
SE116|rolled_back_time|DATETIME|y||
SE117|change_set_id|FK|n|SE116|
SE117|target_entity_type|VARCHAR|n||
SE117|target_entity_id|INT|n||
SE117|target_field_name|VARCHAR|n||
SE117|before_value_text|TEXT|y||null on create
SE117|after_value_text|TEXT|y||null on delete
SE117|before_value_data_json|JSON|y||
SE117|after_value_data_json|JSON|y||
SE117|field_change_type|VARCHAR|n||create|update|delete
SE117|apply_order|INT|n||
SE117|applied_status|VARCHAR|n||pending|applied|failed
SE117|applied_error_text|TEXT|y||
SE118|change_set_id|FK|n|SE116|
SE118|approval_rule_id|FK|n|SE68|
SE118|ops_group_required_id|FK|n|SE4|
SE118|approver_count_required|INT|n||
SE118|fulfilled_count|INT|n||
SE118|is_fulfilled|BOOL|n||
SE119|change_set_id|FK|n|SE116|
SE119|approving_ops_user_id|FK|n|SE3|
SE119|approval_data_json|JSON|y||comments+conditions
SE119|approved_time|DATETIME|n||
SE120|change_set_id|FK|n|SE116|
SE120|rejecting_ops_user_id|FK|n|SE3|
SE120|rejection_reason_text|TEXT|n||
SE120|rejection_data_json|JSON|y||
SE120|rejected_time|DATETIME|n||
SE121|change_set_id|FK|n|SE116|
SE121|validation_type|VARCHAR|n||schema|semantic|policy|lint
SE121|validation_status|VARCHAR|n||passed|failed|warning
SE121|validation_data_json|JSON|y||
SE121|validated_time|DATETIME|n||
SE122|change_set_id|FK|n|SE116|
SE122|reviewing_ops_user_id|FK|n|SE3|
SE122|review_status|VARCHAR|n||pending|approved_post_hoc|findings_filed|requires_corrective_change
SE122|review_text|TEXT|y||
SE122|reviewed_time|DATETIME|y||
SE123|change_set_id|FK|n|SE116|
SE123|member_change_set_id|FK|y|SE116|parent-child structuring
SE123|bulk_role|VARCHAR|n||rotation_step_1|rotation_step_2
SE123|bulk_data_json|JSON|y||
SE124|site_id|FK|n|SE1|
SE124|acting_ops_user_id|FK|y|SE3|set for human actions
SE124|acting_service_account_id|INT|y||set for runner actions
SE124|api_endpoint|VARCHAR|n||
SE124|http_method|VARCHAR|n||
SE124|action_type|VARCHAR|n||read|create|update|delete|approve|reject|change_set_submit|schema_change
SE124|target_entity_type|VARCHAR|n||
SE124|target_entity_id|INT|n||
SE124|request_data_summary|JSON|y||
SE124|response_status|INT|n||
SE124|response_data_summary|JSON|y||
SE124|client_ip_address|VARCHAR|y||
SE124|client_user_agent|VARCHAR|y||
SE124|_audit_chain_hash|VARCHAR|y||tamper-evidence
SE124|acted_time|DATETIME|n||
# audit_log_entry: append-only at DDL level; no UPDATE/DELETE permission for any role
SE125|site_id|FK|n|SE1|
SE125|evidence_record_type|VARCHAR|n||backup_verification|certificate_validity|compliance_scan|credential_rotation_verification|access_review|physical_inspection|tape_rotation_completed|keycard_revocation_completed|license_renewal_completed|vendor_contract_review_completed
SE125|evidence_record_data_json|JSON|n||typed
SE125|produced_by_runner_job_id|FK|y|SE93|
SE125|produced_by_ops_user_id|FK|y|SE3|
SE125|evidence_status|VARCHAR|n||passed|failed|warning|partial
SE125|observed_time|DATETIME|n||
SE125|retention_horizon_time|DATETIME|y||
SE126|evidence_record_id|FK|n|SE125|
SE126|service_id|FK|n|SE25|
SE126|per_target_status|VARCHAR|n||
SE126|per_target_data_json|JSON|y||
SE127|evidence_record_id|FK|n|SE125|
SE127|machine_id|FK|n|SE21|
SE127|per_target_status|VARCHAR|n||
SE127|per_target_data_json|JSON|y||
SE128|evidence_record_id|FK|n|SE125|
SE128|credential_id|FK|n|external|
SE128|per_target_status|VARCHAR|n||
SE128|per_target_data_json|JSON|y||
SE129|evidence_record_id|FK|n|SE125|
SE129|certificate_id|FK|n|external|
SE129|per_target_status|VARCHAR|n||
SE129|per_target_data_json|JSON|y||
SE130|evidence_record_id|FK|n|SE125|
SE130|compliance_regime_id|FK|n|SE73|
SE130|per_target_status|VARCHAR|n||
SE130|per_target_data_json|JSON|y||
SE131|evidence_record_id|FK|n|SE125|
SE131|manual_operation_id|FK|n|SE56|
SE131|per_target_status|VARCHAR|n||
SE131|per_target_data_json|JSON|y||
SE132|site_id|FK|n|SE1|
SE132|compliance_regime_id|FK|n|SE73|
SE132|finding_severity|VARCHAR|n||informational|low|medium|high|critical
SE132|finding_title|VARCHAR|n||
SE132|finding_description|TEXT|n||
SE132|filed_by_ops_user_id|FK|y|SE3|set when human-filed
SE132|filed_by_evidence_record_id|FK|y|SE125|set when automated
SE132|finding_status|VARCHAR|n||open|accepted|mitigating|resolved|accepted_risk
SE132|resolution_change_set_id|FK|y|SE116|
SE132|resolution_text|TEXT|y||
SE132|filed_time|DATETIME|n||
SE132|resolved_time|DATETIME|y||
SE133|compliance_finding_id|FK|n|SE132|
SE133|service_id|FK|n|SE25|
SE134|version_serial|INT|n||monotonic
SE134|version_label|VARCHAR|n||2026.05.03.01
SE134|parent__schema_version_id|FK|y|SE134|
SE134|description|TEXT|y||
SE134|released_time|DATETIME|n||
SE134|is_current|BOOL|n||one row true at a time
SE135|_schema_version_id|FK|n|SE134|version this set produced
SE135|parent__schema_change_set_id|FK|y|SE135|
SE135|proposed_by_ops_user_id|FK|n|SE3|
SE135|approved_by_ops_user_role_id|FK|n|SE6|typically schema steward
SE135|reason_text|TEXT|n||
SE135|applied_time|DATETIME|n||
SE136|table_name|VARCHAR|n||
SE136|description|TEXT|y||
SE136|_schema_version_introduced_id|FK|n|SE134|
SE136|_schema_version_deprecated_id|FK|y|SE134|
SE137|_schema_entity_type_id|FK|n|SE136|
SE137|field_name|VARCHAR|n||
SE137|field_type|VARCHAR|n||int|varchar|text|json|boolean|datetime
SE137|is_nullable|BOOL|n||
SE137|is_primary_key|BOOL|n||
SE137|is_foreign_key|BOOL|n||
SE137|foreign_key_target__schema_entity_type_id|FK|y|SE136|
SE137|default_value_text|TEXT|y||
SE137|constraint_data_json|JSON|y||range|regex|enumeration
SE137|description|TEXT|y||
SE137|_schema_version_introduced_id|FK|n|SE134|
SE137|_schema_version_deprecated_id|FK|y|SE134|
SE138|source__schema_entity_type_id|FK|n|SE136|
SE138|source__schema_field_id|FK|n|SE137|
SE138|target__schema_entity_type_id|FK|n|SE136|
SE138|cardinality|VARCHAR|n||one_to_one|one_to_many|many_to_many
SE138|on_delete_action|VARCHAR|n||cascade|restrict|set_null
SE138|description|TEXT|y||
SE138|_schema_version_introduced_id|FK|n|SE134|
SE138|_schema_version_deprecated_id|FK|y|SE134|

# bridges(id|name|links|role|notes)
SB1|ops_group_member|SE4↔SE3|membership|standard
SB2|ops_user_role_member|SE6↔SE3|membership|with rotation_order
SB3|hardware_set_component|SE10↔SE8|composition|with position_label
SB4|hardware_set_instance_port_connection|SE12↔SE12|cabling|src/dst port pairs
SB5|service_package|SE25↔SE22|composition|with install_order
SB6|service_interface_mount|SE25↔SE23|exposure|with exposed_name/port
SB7|service_connection|SE25↔SE25|topology|drives config+firewall+suppression+capacity
SB8|host_group_machine|SE29↔SE21|denormalized|FK on machine maintained alongside
SB9|host_group_package|SE29↔SE22|composition|with install_order
SB10|site_location|SE25↔SE2|preference|with precedence_order
SB11|*_authority_pointer|various↔SE45|directory|relationship_role per entity type
SB12|*_schedule|various↔SE50|temporal-targeting|one bridge per scheduled-thing class
SB13|*_policy|various↔SE57|policy-application|one bridge per entity type
SB14|security_zone_membership_*|SE62↔various|zone-membership|one bridge per entity type
SB15|compliance_scope_*|SE73↔various|regime-scoping|service+data_classification
SB16|*_ownership|various↔SE6|ownership|one bridge per entity type with ownership_role
SB17|service_stakeholder|SE25↔SE6|non-ownership|with stakeholder_role
SB18|service_runbook_reference|SE25↔SE81|docs|with runbook_purpose
SB19|service_dashboard_reference|SE25↔SE83|docs|with dashboard_purpose
SB20|runner_*_target|SE85↔various|runner-targeting|service|host_group|k8s_namespace|cloud_account
SB21|runner_job_target_*|SE93↔various|job-execution|with per_target_status+data
SB22|monitor_*_target|SE99↔various|monitor-application|machine|service|k8s_workload|cloud_resource
SB23|alert_dependency|SE107↔SE107|suppression|parent_alert+child_alert
SB24|evidence_record_*_target|SE125↔various|evidence-attribution|service|machine|credential|certificate|regime|manual_op
SB25|compliance_finding_target_service|SE132↔SE25|finding-scope|

# discriminators(id|entity|type_field|payload_field|values)
SD1|cloud_resource|cloud_resource_type|cloud_data_json|ec2_instance|gce_instance|azure_vm|s3_bucket|gcs_bucket|azure_blob_container|rds_database|cloud_sql_instance|azure_sql|lambda_function|cloud_run_service|azure_function|vpc|vnet|cloud_network|load_balancer|application_gateway|cloud_lb|cloudfront_distribution|cloud_cdn|azure_cdn|iam_role|service_account|azure_service_principal|route53_zone|cloud_dns_zone|azure_dns_zone|cloudwatch_log_group|cloud_logging_bucket|log_analytics_workspace
SD2|storage_resource|storage_resource_type|storage_data_json|ebs|s3|gcs|azure_blob|nfs_export|ceph_rbd|local_disk|iscsi
SD3|package_version|(per-package; no separate type field)|package_data_json|install/configure spec
SD4|k8s_workload_version|workload_type (on parent)|workload_data_json|deployment|statefulset|daemonset|job|cronjob|replicaset
SD5|k8s_helm_release_version|(Helm chart determines shape)|release_data_json|Helm values
SD6|authority|authority_type|authority_data_json|prometheus_server|log_aggregator|secret_vault|wiki|dashboard_platform|code_repository|identity_provider|runbook_store|ticketing_system|chat_platform|status_page|artifact_registry|container_registry
SD7|authority_pointer|pointer_type|pointer_data_json|metric|log_query|secret|dashboard|runbook|wiki_page|ticket|code_path|chat_thread|artifact|container_image
SD8|schedule|schedule_type|schedule_data_json|cron_expression|rate_based|event_triggered|calendar_anchored|deadline_driven|manual
SD9|policy|policy_type|policy_data_json|security_zone|data_classification|retention|approval_rule|escalation|change_management|schedule_governance|access_control|compliance_scope
SD10|runner_spec_version|runner_spec_type (on parent)|runner_data_json|see SD12
SD11|monitor|monitor_type|monitor_data_json|script_local|script_remote|prometheus_query|http_probe|tcp_probe|cloud_metric|k8s_event_watch
SD12|evidence_record|evidence_record_type|evidence_record_data_json|backup_verification|certificate_validity|compliance_scan|credential_rotation_verification|access_review|physical_inspection|tape_rotation_completed|keycard_revocation_completed|license_renewal_completed|vendor_contract_review_completed
SD13|manual_operation|manual_operation_type|manual_operation_data_json|tape_rotation|vendor_review|keycard_audit|license_renewal|contract_renewal|evidence_collection|physical_inspection
SD14|configuration_variable|variable_type|variable_data_json|string|int|float|bool|json|secret_reference

# enumerations(entity|field|values)
SE2|location_type|region|datacenter|cage|row|rack|cloud_region|cloud_zone|office|desk
SE8|hardware_component_type|chassis|motherboard|cpu|ram|disk|psu|nic|hba|fan|gpu
SE9|media_type|rj45|fiber|sfp|db9|c13|c19|usb|hdmi
SE9|resource_type|network|power_110|power_220|serial|video|kvm|storage|management
SE9|direction|provider|consumer|bidirectional
SE14|megavisor_type|bare_metal|kvm|vmware|xen|hyperv|docker|containerd|kubelet|firecracker|ec2|gce|azure_vm|lambda|cloudrun|fargate
SE20|os_family|linux|windows|freebsd|darwin
SE20|architecture|x86_64|arm64|riscv64
SE22|package_type|platform|service|sidecar|agent
SE23|interface_type|transaction|message|resource
SE23|protocol|tcp|udp|unix_socket|http|grpc
SE25|service_type|standard|database|k8s_cluster_member|cloud_managed
SE34|threshold_operator|gt|lt|gte|lte
SE35|k8s_distribution|vanilla|eks|gke|aks|openshift|rancher|k3s|talos
SE36|node_role|control_plane|worker|etcd|ingress
SE42|secret_type|opaque|tls|dockerconfigjson|service_account_token|basic_auth
SE43|k8s_service_type|cluster_ip|node_port|load_balancer|external_name|headless
SE45|relationship_role|primary_dashboard|runbook|log_query|metric_namespace|status_page|on_call_handoff
SE56|manual_operation_type|tape_rotation|vendor_review|keycard_audit|license_renewal|contract_renewal|evidence_collection|physical_inspection
SE62|name|production|corp|pci_cardholder|phi_processing|dmz
SE66|name|public|internal|confidential|restricted|regulated_pci|regulated_phi|regulated_pii
SE67|retention_type|time_bounded|count_bounded|hybrid|infinite
SE70|step_type|notify_role|notify_user|page_role|page_user|wait_seconds|branch_on_acknowledge
SE73|name|SOC2_TYPE2|ISO27001|PCI_DSS|HIPAA|FedRAMP_MODERATE|GDPR|SOX_ITGC
SE76|ownership_role|owner|technical_owner|business_owner|support_owner
SE80|stakeholder_role|consumer|dependency_owner|compliance_reviewer|security_reviewer
SE82|runbook_purpose|oncall_response|deployment|disaster_recovery|security_incident|capacity_response
SE84|dashboard_purpose|primary|capacity|error_budget|security|dependency
SE85|runner_spec_type|config_apply|template_generate|k8s_apply|cloud_provision|monitor_collect|alert_dispatch|drift_detect|verify_evidence|reconcile|scheduler_enforce|puller|compliance_scan|credential_rotator|certificate_renewer|manual_operation_tracker
SE86|capability_name|yum_install|k8s_apply|ec2_provision|template_render|secret_resolve|prometheus_query|tape_verify|keycard_revoke|license_check
SE93|job_status|pending|running|succeeded|failed|cancelled|timeout
SE99|monitor_type|script_local|script_remote|prometheus_query|http_probe|tcp_probe|cloud_metric|k8s_event_watch
SE106|action_type|set_state|set_trigger|set_alert
SE107|alert_severity|info|warning|critical|page
SE115|scope_type|helm_release_version|k8s_config_map_version|service_version|runner_spec_version|package_version|host_group|machine|service|k8s_namespace
SE116|change_set_status|draft|submitted|validating|pending_approval|approved|rejected|expired|applied|rolled_back|cancelled
SE117|field_change_type|create|update|delete
SE117|applied_status|pending|applied|failed
SE121|validation_type|schema|semantic|policy|lint
SE121|validation_status|passed|failed|warning
SE122|review_status|pending|approved_post_hoc|findings_filed|requires_corrective_change
SE124|action_type|read|create|update|delete|approve|reject|change_set_submit|schema_change
SE125|evidence_status|passed|failed|warning|partial
SE132|finding_severity|informational|low|medium|high|critical
SE132|finding_status|open|accepted|mitigating|resolved|accepted_risk
SE137|field_type|int|varchar|text|json|boolean|datetime
SE138|cardinality|one_to_one|one_to_many|many_to_many
SE138|on_delete_action|cascade|restrict|set_null

# versioning_classification(classification|entities|writer|gated)
SV1|change-managed|SE1|SE2|SE3|SE4|SE5|SE6|SE7|SE8|SE9|SE10|SE11|SE12|SE13|SE14|SE15|SE16|SE17|SE18|SE19|SE20|SE21|SE22|SE23|SE24|SE25|SE26|SE27|SE28|SE29|SE30|SE31|SE32|SE33|SE34|SE35|SE36|SE37|SE38|SE40|SE41|SE42|SE43|SE44|SE45|SE46|SE47|SE48|SE49|SE50|SE56|SE57|SE58|SE59|SE60|SE61|SE62|SE63|SE64|SE65|SE66|SE67|SE68|SE69|SE70|SE71|SE72|SE73|SE74|SE75|SE76|SE77|SE78|SE79|SE80|SE81|SE82|SE83|SE84|SE85|SE86|SE87|SE99|SE100|SE101|SE102|SE103|SE104|SE105|SE106|SE107|SE108|SE110|SE115|SE134|SE135|SE136|SE137|SE138|humans+runners via change_set|yes
SV2|observation-only|SE39|SE88|SE93|SE94|SE95|SE96|SE97|SE98|SE109|SE111|SE112|SE113|SE114|SE125|SE126|SE127|SE128|SE129|SE130|SE131|pullers/runners with scoped creds|no (audited)
SV3|append-only|SE124|API only; no UPDATE or DELETE|no
SV4|computed-by-tooling|SE134|SE135|SE136|SE137|SE138|API tooling on schema commit|via _schema_change_set

# scope_examples(domain|entities|scheduled_via|evidence_via)
SX1|tape rotations|manual_operation|manual_operation_schedule|evidence_record(tape_rotation_completed)
SX2|password/credential rotations|external credential entity|credential_rotation_schedule|evidence_record(credential_rotation_verification)
SX3|certificate renewals|external certificate entity|certificate_expiration_schedule|evidence_record(certificate_validity)
SX4|DNS registration expirations|external|certificate_expiration_schedule (analogous)|evidence_record(custom)
SX5|vendor contract renewals|manual_operation(vendor_review)|manual_operation_schedule|evidence_record(vendor_contract_review_completed)
SX6|software license renewals|manual_operation(license_renewal)|manual_operation_schedule|evidence_record(license_renewal_completed)
SX7|compliance audit submissions|compliance_regime|compliance_audit_schedule|evidence_record(compliance_scan)
SX8|patch windows|host_group|runner_schedule|runner_job
SX9|disaster recovery drills|manual_operation|manual_operation_schedule|evidence_record(physical_inspection or custom)
SX10|access reviews|manual_operation|manual_operation_schedule|evidence_record(access_review)
SX11|on-call rotation|on_call_schedule|schedule|on_call_assignment
SX12|backup verification|monitor or runner|runner_schedule|evidence_record(backup_verification)
SX13|keycard deactivation when employee leaves|manual_operation(keycard_audit)|manual_operation_schedule|evidence_record(keycard_revocation_completed)
SX14|laptop fleet patch status|host_group|runner_schedule|runner_job
SX15|internal CA root cert renewals|external certificate entity|certificate_expiration_schedule|evidence_record(certificate_validity)
SX16|capacity planning reviews|manual_operation|manual_operation_schedule|evidence_record(custom)
SX17|code dependency scans|runner|runner_schedule|evidence_record(compliance_scan)

# excluded_from_schema(domain|where_it_lives|opsdb_holds)
EX1|prose content (wikis|design docs|runbook bodies)|wiki+notion+equivalent|runbook_reference rows with last-reviewed
EX2|full-resolution time series|prometheus+datadog+cloudwatch|observation_cache_metric for summaries; prometheus_config+authority_pointer for live queries
EX3|code and binaries|repositories+container registries|runner_image_reference+package_data_json pointers
EX4|chat and discussion|slack+teams+irc|authority pointers to threads
EX5|tickets and incidents|jira+linear+servicenow|ticket_pointer_authority_pointer_id on entities like change_set
EX6|secret values|vault+aws-sm+gcp-sm|k8s_secret_reference+configuration_variable(secret_reference) pointers
EX7|email/document files/video|external systems|pointers if needed

# relationships(from|rel|to)
SP1|applies_to|all-entities
SP2|sibling_of|change-managed-entities
SP3|implements|heterogeneous-data
SP4|implements|polymorphic-relationships
SP5|prefixes|governance-fields
SP6|enables|hierarchy-traversal
SP7|covers|helm-values+configmap-data+service-params+runner-params+package-params
SP8|unifies|bare-metal+VM+container+pod+cloud-compute
SP9|covers|metric+state+config-observation
SP10|enables|schema-introspection-via-API
SE15|self_chains_to|SE15
SE15|terminates_at|SE12 (bare-metal) OR SE18 (cloud)
SE21|hosted_on|SE15
SE36|bridges_to|SE21
SE39|bridges_to|SE15
SE25|composed_of|SE26
SE26|references|SE22
SE25|topology_via|SE28
SE40|values_in|SE115
SE41|contents_in|SE115
SE42|points_to|external-secret-backend
SE45|owned_by|SE44
SE99|owned_by|SE22
SE107|scoped_to|SE25
SE108|enables|alert-suppression-graph
SE110|combines|SE6+SE50
SE111|resolved_at|query-time-against-current-time
SE112|written_by|SE93
SE113|written_by|SE93
SE114|written_by|SE93
SE115|scoped_via|SC scope_type+scope_id
SE116|bundles|SE117
SE116|requires|SE118
SE116|fulfilled_by|SE119
SE116|blocked_by|SE120
SE116|validated_by|SE121
SE116|reviewed_by|SE122 (when emergency)
SE116|structured_by|SE123 (when bulk)
SE124|append_only|true
SE124|written_only_by|API
SE125|target_via|SE126|SE127|SE128|SE129|SE130|SE131
SE132|resolved_by|SE116
SE134|chains_to|SE134
SE135|produces|SE134
SE136|registers|entity-types
SE137|registers|fields
SE138|registers|relationships
SE137|references|SE136 (foreign_key_target)
SE85|references_artifact|external-registry (image not in OpsDB)
SE93|writes|SE98
SE93|writes_to_targets|SE94|SE95|SE96|SE97
SE45|verified_by|verifier-runner-on-schedule
SE116|emergency_path_via|is_emergency=true
SE116|bulk_via|is_bulk=true
SE116|proposed_by|SE3 OR SE93
SE116|atomic|true (all field changes commit or none)
SE17|scoped_to|SE16
SE18|located_in|SE2 (cloud_region/cloud_zone)
SE12|located_in|SE2
SE2|hierarchical|self-FK
SE6|filled_by|SE3 (via SE7)
SE104|owned_by|SE44 (prometheus_server authority)
SE105|nested_in|SE104
SE73|scoped_via|SE74+SE75
SE62|members_via|SE63+SE64+SE65
SE57|targets_via|SE58+SE59+SE60+SE61
SE69|stepped_via|SE70 (with step_order)
SE71|attaches|SE69_to_SE25_with_severity
SE81|enriched_with|last_reviewed+last_tested+next_review_due
SE45|attached_to_entities_via|SE46+SE47+SE48+SE49 (and similar bridges)
SE50|targeted_via|SE51+SE52+SE53+SE54+SE55
SE85|targets_via|SE89+SE90+SE91+SE92
SE99|targets_via|SE100+SE101+SE102+SE103
SE125|targets_via|SE126+SE127+SE128+SE129+SE130+SE131

# section_index(section|title|entity_ids)
2|Conventions|SC1-SC16,SP1-SP10,SR1-SR10,SG1-SG9
3|Top-Level Cuts|ST1-ST17
4|Reserved Fields and Universal Patterns|SR1-SR10,SP1-SP10,SG1-SG9
5|Site Location Identity|SE1,SE2,SE3,SE4,SE5,SE6,SE7
6|Substrate Hierarchy|SE8,SE9,SE10,SE11,SE12,SE13,SE14,SE15,SE16,SE17,SE18,SE19,SE20,SE21
7|Service Abstraction|SE22,SE23,SE24,SE25,SE26,SE27,SE28,SE29,SE30,SE31,SE32,SE33,SE34
8|Kubernetes|SE35,SE36,SE37,SE38,SE39,SE40,SE41,SE42,SE43
9|Cloud Resources|SE18,SD1
10|Authority Directory|SE44,SE45,SE46,SE47,SE48,SE49
11|Schedules|SE50,SE51,SE52,SE53,SE54,SE55,SE56
12|Policy|SE57,SE58,SE59,SE60,SE61,SE62,SE63,SE64,SE65,SE66,SE67,SE68,SE69,SE70,SE71,SE72,SE73,SE74,SE75
13|Documentation Metadata|SE76,SE77,SE78,SE79,SE80,SE81,SE82,SE83,SE84
14|Runners|SE85,SE86,SE87,SE88,SE89,SE90,SE91,SE92,SE93,SE94,SE95,SE96,SE97,SE98
15|Monitoring and Alerting|SE99,SE100,SE101,SE102,SE103,SE104,SE105,SE106,SE107,SE108,SE109,SE110,SE111
16|Cached Observation|SE112,SE113,SE114
17|Configuration Variables|SE115
18|Change Management|SE116,SE117,SE118,SE119,SE120,SE121,SE122,SE123
19|Audit and Evidence|SE124,SE125,SE126,SE127,SE128,SE129,SE130,SE131,SE132,SE133
20|Schema Metadata|SE134,SE135,SE136,SE137,SE138
21|Excluded Domains|EX1-EX7

# decode_legend
field_types: INT|VARCHAR|TEXT|JSON|BOOL|DATETIME|FLOAT|BIGINT|FK|FK-self
nullable: y|n
versioned: yes|no|append-only
classifications: change-managed|observation-only|append-only|computed-by-tooling
+V suffix: entity has a versioning sibling table named *_version
+reserved: id|created_time|updated_time|is_active fields implicit on every entity
discriminator-payload: *_type column + *_data_json column; API validates JSON against schema registered for type value
bridge_notation: SE_X↔SE_Y means many-to-many bridge; one_to_many uses FK directly
external in fk column: refers to entity not detailed in this schema (credential|certificate as referenced types)
