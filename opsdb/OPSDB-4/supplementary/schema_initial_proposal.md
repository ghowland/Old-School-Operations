# Modern Multi-DOS Controller Schema

A schema proposal in REM-style hierarchy, DSNC naming, modeling: physical hardware, K8s clusters, cloud providers, runners, and the full operational substrate that produces and applies configuration. Source of truth is opsdb. Runners are the executors. Code does not live in opsdb — runner specs do.

---

## Naming and structural conventions used throughout

- All field/table names singular, lower_case_with_underscores
- Hierarchical prefixes: `web_`, `web_site_`, `web_site_widget_` style
- FK fields = `referenced_table_name + _id`; role-prefix when multiple FKs to same table (`primary_machine_id`, `replica_machine_id`)
- Type suffixes mandatory: `_time` for DATETIME, `_date` for DATE, `_json` for JSON blobs, `_id` for FK
- Boolean prefixes: `is_` (present), `was_` (past)
- Reserved fields on every table: `id`, `created_time`, `updated_time`, `parent_id` where hierarchical
- `*_data_json` fields hold typed-but-flexible payloads (cloud-specific, K8s-specific) — typed by sibling `*_type` field
- Versioned tables suffix `_version` and carry `version_serial`, `parent_version_id`, `is_active`

---

## 1. Site, Location, Hierarchy roots

The REM `site` concept survives. A site is the top-level operational universe.

```
site
  id
  name
  description
  domain
  is_active
  created_time
  updated_time

location
  id
  parent_id              -- self-FK, hierarchical
  site_id
  name
  location_type          -- region, datacenter, cage, row, rack, desk, cloud_region, cloud_zone
  latitude
  longitude
  is_active
  created_time
  updated_time
```

Rationale: latitude/longitude only set where physically meaningful; hierarchical resolution walks up to nearest set values. Cloud regions and zones are locations too — `us-east-1` is a location with `location_type = cloud_region`, parent linking to the provider's location root.

---

## 2. Hardware (REM hardware lineage, expanded)

```
hardware_component
  id
  name
  manufacturer
  model
  rack_unit_height
  hardware_component_type    -- chassis, motherboard, cpu, ram, disk, psu, nic, etc.
  parent_hardware_component_id    -- hierarchical (chassis → motherboard → cpu)
  is_active
  created_time
  updated_time

hardware_port
  id
  hardware_component_id
  name
  media_type           -- rj45, fiber, sfp, db9, c13, c19
  resource_type        -- network, power_110, power_220, serial, video, kvm, storage
  direction            -- provider, consumer, bidirectional
  is_active
  created_time
  updated_time

hardware_set
  id
  name
  description
  -- A specification: e.g., "Dell R750 with 2x Xeon, 256GB, 8x NVMe"
  is_active
  created_time
  updated_time

hardware_set_component
  id
  hardware_set_id
  hardware_component_id
  position_label              -- "cpu_0", "ram_slot_3"
  created_time
  updated_time

hardware_set_instance
  id
  hardware_set_id
  location_id
  rack_unit_mount_height
  serial_number
  asset_tag
  is_active
  decommissioned_time
  created_time
  updated_time

hardware_set_instance_port_connection
  id
  source_hardware_set_instance_id
  source_hardware_port_id
  destination_hardware_set_instance_id
  destination_hardware_port_id
  cable_label
  created_time
  updated_time
```

This is REM's hardware tree, named per DSNC. Cables/connections are first-class so dependency graphs (power chains, network chains) are queryable for alert suppression.

---

## 3. Megavisor (extended to nest containers and pods)

REM's Megavisor wrapped hypervisors and bare metal. Modern stack adds container runtimes and pod runtimes. Key insight: same nesting concept, more layers.

```
megavisor
  id
  name
  megavisor_type        -- bare_metal, kvm, vmware, xen, hyperv, docker, containerd, kubelet, firecracker, ec2, gce
  version
  is_active
  created_time
  updated_time

megavisor_function
  id
  megavisor_id
  function_name         -- create, destroy, snapshot, start, stop, freeze, unfreeze
  runner_spec_id        -- which runner knows how to invoke this (runner_spec defined later)
  created_time
  updated_time

megavisor_instance
  id
  parent_megavisor_instance_id   -- self-FK; this is the nesting!
  megavisor_id
  hardware_set_instance_id       -- nullable; only set at the bare-metal root
  location_id                    -- inherited but cached for query speed
  external_id                    -- vm UUID, container ID, pod UID, ec2 instance ID
  hostname
  ip_primary
  is_active
  is_running
  provisioned_time
  decommissioned_time
  created_time
  updated_time
```

The crucial field is `parent_megavisor_instance_id`. Walk up the chain to get the full nesting:

```
pod_xyz (megavisor=kubelet)
  → node_n3 (megavisor=kvm guest)
    → vm_host_42 (megavisor=kvm)
      → bare_metal_server_007 (megavisor=bare_metal, hardware_set_instance_id=...)
        → rack 14 in DC-east (location)
```

A K8s pod, all the way down to a rack unit, in one self-joining table. Same query pattern works for a Lambda function in EC2 in an AWS region, or a container on a developer laptop.

---

## 4. Machine (REM concept, now polymorphic over megavisor types)

A machine is a megavisor_instance that's "the unit we configure as a host." Not every megavisor_instance is a machine (a hypervisor host is not itself a configured machine in the traditional sense, though it might be).

```
machine
  id
  megavisor_instance_id
  fqdn
  host_group_id              -- single host group, sysync-style
  platform_id
  is_active
  is_under_management
  bootstrapped_time
  last_converged_time
  created_time
  updated_time
```

`is_under_management` is the kill switch — if false, runners skip this machine. The book's "level-triggered, but bounded" — you can take a host out of automation without deleting its row.

`host_group_id` is single-valued. One host, one group. Per the sysync stance.

---

## 5. Platform (REM platform concept)

```
platform
  id
  name                    -- "rocky-9-base", "ubuntu-24-04-hardened"
  os_family               -- linux, windows, freebsd
  os_version
  architecture            -- x86_64, arm64
  is_active
  is_approved_for_production
  created_time
  updated_time

platform_package
  id
  platform_id
  package_id
  install_order
  created_time
  updated_time
```

---

## 6. Package, Interface, Connection (REM, refined)

```
package
  id
  name
  package_type            -- platform, service, sidecar, agent
  description
  is_active
  created_time
  updated_time

package_version
  id
  package_id
  version_serial
  parent_package_version_id
  package_data_json       -- the actual install/configure spec, runner-interpreted
  is_active
  approved_for_production_time
  created_time
  updated_time

package_interface
  id
  package_version_id
  name                    -- "http", "syslog_listener", "metrics_scrape"
  interface_type          -- transaction, message, resource
  protocol                -- tcp, udp, unix_socket, http
  default_port
  description
  created_time
  updated_time

package_connection
  id
  package_version_id
  name                    -- "syslog_upstream", "database_primary"
  target_interface_name   -- name of an interface on another package, resolved at service-level
  is_required
  description
  created_time
  updated_time
```

The package is the abstraction; package_version is the unit of change. Following the book's "data is king and outlives logic" — package definitions are versioned and change-managed; the runner interprets them.

---

## 7. Service (REM concept — the binding layer)

```
service
  id
  site_id
  name
  description
  service_type            -- standard, database, k8s_cluster_member, cloud_managed
  parent_service_id       -- nullable; allows service hierarchies
  is_active
  created_time
  updated_time

service_version
  id
  service_id
  version_serial
  parent_service_version_id
  is_active
  approved_for_production_time
  created_time
  updated_time

service_package
  id
  service_version_id
  package_version_id
  install_order
  created_time
  updated_time

service_interface_mount
  id
  service_version_id
  package_interface_id
  exposed_name            -- the public name of this interface for this service
  exposed_port            -- override the package default
  exposed_protocol
  is_external             -- accepts traffic from outside the service mesh
  created_time
  updated_time

service_connection
  id
  source_service_version_id
  destination_service_id
  destination_service_interface_mount_id
  source_package_connection_id
  is_required
  created_time
  updated_time
```

This graph drives:
- Config template generation (resolves to concrete addresses/ports)
- Firewall rules (only mounted interfaces are open)
- Alert dependency suppression
- Capacity planning

---

## 8. Service Level + Site Location ordering (REM 0/N at the role level)

```
site_location
  id
  site_id
  service_id
  location_id
  precedence_order        -- 0, 1, 2... reorder these for failover
  is_active
  created_time
  updated_time

service_level
  id
  service_version_id
  site_location_id
  hardware_set_id         -- nullable; constrains hw spec
  machine_count_minimum
  machine_count_maximum
  service_level_metric_id -- nullable; for SLO-driven scaling
  created_time
  updated_time

service_level_metric
  id
  name
  metric_query            -- prometheus query string, or runner-interpreted spec
  threshold_value
  threshold_operator      -- gt, lt, gte, lte
  rate_change_minimum_time -- seconds before scaling action allowed
  created_time
  updated_time
```

`precedence_order` is the renaming knob — DC fails, you re-order, the role moves. Roles are infinite-capable; physical locations are interchangeable.

---

## 9. K8s cluster modeling

K8s is a service-of-services with its own internal substrate. We model the *cluster as a service*, the *nodes as machines*, the *pods as megavisor_instances nested under nodes*, and the *K8s-specific configuration data* in dedicated tables.

```
k8s_cluster
  id
  service_id              -- the cluster IS a service
  site_id
  name
  k8s_distribution        -- vanilla, eks, gke, aks, openshift, rancher
  k8s_version
  api_endpoint_fqdn
  is_active
  created_time
  updated_time

k8s_cluster_node
  id
  k8s_cluster_id
  machine_id              -- the underlying machine
  node_role               -- control_plane, worker, etcd, ingress
  is_schedulable
  joined_time
  created_time
  updated_time

k8s_namespace
  id
  k8s_cluster_id
  name
  is_active
  created_time
  updated_time

k8s_workload
  id
  k8s_cluster_id
  k8s_namespace_id
  name
  workload_type           -- deployment, statefulset, daemonset, job, cronjob
  workload_data_json      -- the spec; runner-interpreted
  is_active
  created_time
  updated_time

k8s_workload_version
  id
  k8s_workload_id
  version_serial
  parent_k8s_workload_version_id
  workload_data_json
  is_active
  approved_for_production_time
  created_time
  updated_time

k8s_pod
  id
  megavisor_instance_id   -- this is how pods slot into the nesting hierarchy
  k8s_workload_id
  k8s_namespace_id
  k8s_cluster_node_id
  name
  pod_uid
  is_running
  scheduled_time
  created_time
  updated_time

k8s_helm_release
  id
  k8s_cluster_id
  k8s_namespace_id
  name
  chart_name
  chart_version
  release_data_json       -- values, overrides
  is_active
  installed_time
  created_time
  updated_time

k8s_helm_release_version
  id
  k8s_helm_release_id
  version_serial
  parent_k8s_helm_release_version_id
  release_data_json
  is_active
  approved_for_production_time
  created_time
  updated_time

k8s_config_map
  id
  k8s_cluster_id
  k8s_namespace_id
  name
  config_map_data_json    -- the key/value pairs
  is_active
  created_time
  updated_time

k8s_secret_reference
  id
  k8s_cluster_id
  k8s_namespace_id
  name
  secret_type             -- opaque, tls, dockerconfigjson, etc.
  secret_backend_id       -- FK to secret_backend (vault, sops, kms, etc.)
  secret_backend_path     -- where the actual secret lives
  is_active
  created_time
  updated_time
```

Note: `k8s_secret_reference` does NOT store the secret. It stores *where the secret lives* in an external secret backend. The opsdb is source of truth for *configuration*, not for credentials.

The pod-via-megavisor-instance bridge is what lets you query: "give me every pod running in rack 14 in DC-east." The query walks `k8s_pod → megavisor_instance → parent → parent → ... → hardware_set_instance → location`. One self-joining tree, all layers.

---

## 10. Cloud provider modeling (generic across AWS/Azure/GCP)

Same shape: model the abstract resource generically, store provider-specific payload as typed JSON, runner specs say which runner handles which provider+resource_type.

```
cloud_provider
  id
  name                    -- aws, azure, gcp, digital_ocean, hetzner
  is_active
  created_time
  updated_time

cloud_account
  id
  cloud_provider_id
  site_id
  name                    -- "production-aws-account", "billing-azure-tenant"
  account_external_id     -- the AWS account ID, Azure tenant ID, GCP project ID
  is_active
  created_time
  updated_time

cloud_resource
  id
  cloud_account_id
  location_id             -- maps to cloud_region/cloud_zone location
  cloud_resource_type     -- ec2_instance, s3_bucket, rds_database, lambda_function,
                          --   azure_vm, blob_container, gce_instance, gcs_bucket, etc.
  external_id             -- arn, resource id, self link
  name
  cloud_data_json         -- provider-specific payload (instance type, AMI, IAM, tags, etc.)
  megavisor_instance_id   -- nullable; set if this resource IS a compute unit (EC2, GCE)
  is_active
  provisioned_time
  decommissioned_time
  created_time
  updated_time

cloud_resource_version
  id
  cloud_resource_id
  version_serial
  parent_cloud_resource_version_id
  cloud_data_json
  is_active
  approved_for_production_time
  created_time
  updated_time

storage_resource
  id
  cloud_resource_id       -- nullable; storage may or may not be cloud-backed
  hardware_set_instance_id -- nullable; for physical storage
  storage_resource_type   -- ebs, s3, gcs, azure_blob, nfs_export, ceph_rbd, local_disk
  size_bytes
  storage_data_json       -- backend-specific config (iops, replication, etc.)
  is_active
  created_time
  updated_time
```

`cloud_data_json` is bounded by API validation against the `cloud_resource_type` — runners reject malformed JSON at ingest. The opsdb stays clean; the JSON stays interpretable.

The `megavisor_instance_id` link on `cloud_resource` is what makes EC2 instances participate in the nesting hierarchy alongside bare metal and containers. An EC2 instance is a megavisor_instance whose hardware_set_instance_id is null and whose cloud_resource_id is set. Same query patterns apply.

---

## 11. Runners — the executor model

Runners are the operational logic. opsdb stores their *specs* (what they are, where they run, what they handle), not their code.

```
runner_spec
  id
  name
  runner_spec_type        -- config_apply, template_generate, k8s_apply, cloud_provision,
                          --   monitor_collect, alert_dispatch, drift_detect, ...
  description
  runner_image_reference  -- container image, binary path, or repo locator (NOT code)
  runner_entrypoint
  is_active
  created_time
  updated_time

runner_spec_version
  id
  runner_spec_id
  version_serial
  parent_runner_spec_version_id
  runner_image_reference
  runner_data_json        -- runner-specific config schema
  is_active
  approved_for_production_time
  created_time
  updated_time

runner_capability
  id
  runner_spec_id
  capability_name         -- "yum_install", "k8s_apply", "ec2_provision",
                          --   "template_render", "secret_resolve"
  capability_data_json
  created_time
  updated_time

runner_machine                  -- which machines host runners (the runners are themselves managed!)
  id
  machine_id
  runner_spec_id
  is_active
  capacity_concurrent_jobs
  created_time
  updated_time

runner_schedule
  id
  runner_spec_id
  service_id              -- nullable; what service this schedule targets
  cron_expression
  is_active
  next_run_time
  last_run_time
  created_time
  updated_time

runner_job
  id
  runner_spec_id
  runner_machine_id       -- which runner machine actually executed it
  triggered_by_runner_job_id  -- nullable; for runner-triggers-runner chains
  target_machine_id       -- nullable; what host this job acted on
  target_service_id       -- nullable
  target_k8s_cluster_id   -- nullable
  target_cloud_resource_id -- nullable
  job_status              -- pending, running, succeeded, failed, cancelled
  job_input_data_json     -- the input the runner was given
  job_output_data_json    -- structured output, including discrete output vars
  job_log_text            -- stdout/stderr capture
  scheduled_time
  started_time
  finished_time
  created_time
  updated_time

runner_job_output_var
  id
  runner_job_id
  var_name
  var_value
  var_type                -- string, int, bool, json
  created_time
```

`runner_job_output_var` is the key automation primitive. Discrete output variables become rows; downstream automation reads those rows; chains form. This is how the loop closes.

The runner-triggering-runner pattern lives in `triggered_by_runner_job_id`. A "pull config" runner detects drift, kicks off a "render templates" runner, which kicks off a "sysync apply" runner — three rows linked, full audit trail in opsdb.

Runners themselves run on machines; those machines are managed via the same machine/host_group/package mechanism. The system bootstraps itself off the same data model. This is the book's "operational logic must minimize external dependencies, especially networked ones" — runners do their work locally on machines whose configs come from opsdb that they themselves help apply.

---

## 12. Templating data (the upstream layer sysync expects to see)

```
template_data
  id
  template_data_type      -- service, host_group, machine, k8s_cluster, etc.
  scope_id                -- polymorphic; the ID in the relevant scope table
  scope_type              -- service, host_group, machine, k8s_cluster, ...
  template_data_json      -- the variable bag
  is_active
  created_time
  updated_time

template_data_version
  id
  template_data_id
  version_serial
  parent_template_data_version_id
  template_data_json
  is_active
  approved_for_production_time
  created_time
  updated_time

template_generation_runner
  id
  template_data_id
  runner_spec_id
  generation_order        -- runners that produce template data run in order
  is_active
  created_time
  updated_time
```

This is the layer that sits *upstream* of sysync (or whatever leaf config tool you use). Per your point: complex resolution happens here, the output is concrete data, the data is versioned and audited, and the leaf tool gets handed something dumb to substitute.

---

## 13. Monitoring, alerts, Prometheus

```
monitor
  id
  package_version_id      -- monitors are owned by packages, REM-style
  name
  monitor_type            -- script_local, script_remote, prometheus_query, http_probe, tcp_probe
  monitor_data_json       -- spec for the runner that executes the monitor
  collection_interval_seconds
  is_active
  created_time
  updated_time

prometheus_config
  id
  service_id              -- nullable; cluster-wide if null
  scrape_target_data_json
  rule_data_json
  is_active
  created_time
  updated_time

monitor_level
  id
  monitor_id
  name                    -- the AND-grouping name from REM
  condition_expression    -- runner-interpreted; e.g., PromQL or simple comparator
  condition_data_json
  action_type             -- set_state, set_trigger, set_alert
  action_target_id        -- FK polymorphic by action_type
  is_active
  created_time
  updated_time

state_value
  id
  state_scope_type        -- machine, service, package_instance, k8s_cluster, cloud_resource
  state_scope_id
  state_name
  state_value_text
  state_value_numeric
  state_recorded_time
  created_time

alert
  id
  service_id
  name
  alert_severity          -- info, warning, critical, page
  description
  is_active
  created_time
  updated_time

alert_dependency
  id
  parent_alert_id         -- if parent is firing, this one is suppressed
  child_alert_id
  created_time

alert_fire
  id
  alert_id
  fired_time
  cleared_time
  is_acknowledged
  acknowledged_user_id
  acknowledged_time
  acknowledge_suppression_until_time
  created_time
  updated_time
```

Monitor level → state/trigger/alert mapping is REM's, named and structured for opsdb. Alert dependency graph is computable from `service_connection` plus explicit `alert_dependency` entries.

---

## 14. Users, roles, on-call

```
ops_user
  id
  site_id
  username
  fullname
  email
  is_active
  created_time
  updated_time

ops_user_role
  id
  site_id
  name
  description
  created_time
  updated_time

ops_user_role_member
  id
  ops_user_role_id
  ops_user_id
  rotation_order
  created_time
  updated_time

service_ownership
  id
  service_id
  ops_user_role_id
  notification_order
  created_time
  updated_time

on_call_schedule
  id
  ops_user_role_id
  ops_user_id
  on_call_start_time
  on_call_stop_time
  is_active
  created_time
  updated_time
```

(`ops_user` because `user` is a reserved word in many DBs and a heavily overloaded name; `ops_` prefix scopes it.)

---

## 15. Change management (cross-cutting)

```
change_request
  id
  site_id
  name
  description
  change_request_status   -- draft, submitted, approved, applied, rolled_back, cancelled
  submitted_user_id
  approved_user_id
  applied_user_id
  submitted_time
  approved_time
  applied_time
  rolled_back_time
  created_time
  updated_time

change_request_target
  id
  change_request_id
  target_type             -- service_version, package_version, k8s_workload_version,
                          --   cloud_resource_version, host_group, etc.
  target_id
  before_state_data_json  -- snapshot of the row before
  after_state_data_json   -- intended new state
  created_time
  updated_time
```

Every `*_version` table participates. Approvals gate `is_active = true` flips. Rollback is just re-activating a prior version row. Per the book: data is king, history is data, rollback is a data operation.

---

## How the pieces compose at runtime

A simple workflow, end to end:

1. Operator submits a `change_request` modifying a `service_version`.
2. On approval, `runner_schedule` (or an event-driven `runner_job`) fires a "template_generate" runner.
3. Template runner reads `template_data`, resolves variables (service_connection graph, location data, secret references), writes a new `template_data_version`.
4. A "config_apply" runner pulls the latest `template_data_version` for the target machine, compares to last applied version on that machine, finds drift.
5. If `machine.is_under_management` is true, runner pushes the rendered config to the target host.
6. A leaf tool (sysync, or any other) applies the config locally.
7. Local runner reports `runner_job_output_var` rows back via API.
8. Validation/bounding at the API ensures only typed, expected output is stored.
9. Monitor runners observe state; `monitor_level` evaluates; `state_value` rows accumulate; `alert_fire` rows appear when thresholds cross.
10. Alert dependency graph (computed from service_connection + alert_dependency) suppresses downstream noise.

Everything an operator sees in dashboards, every automation decision downstream — all reads from opsdb. opsdb is the single source of truth.

---

## What this schema buys you

- **One nesting hierarchy** spans rack → server → VM → container → pod (`megavisor_instance.parent_megavisor_instance_id`). Cloud instances slot in via their `cloud_resource → megavisor_instance` link. K8s pods slot in via `k8s_pod → megavisor_instance`.
- **Generic-then-specific** for cloud and K8s. `cloud_resource` plus `cloud_data_json` covers all providers; provider-specific runners interpret the JSON. Same pattern for K8s workloads, Helm releases, configmaps.
- **Configuration is data, code is referenced.** `runner_image_reference` points at code; opsdb does not store code. Runner specs say *what* to run; runners contain *how*.
- **Versioning everywhere that matters.** Every config-shaped table has a `_version` sibling with `parent_version_id` chains. Rollback is a row update.
- **Validated-bounded ingest.** `*_data_json` fields are typed by sibling `*_type` fields; API validation enforces shape per type. Invalid data does not enter the store.
- **Self-bootstrapping.** Runners run on machines whose configs come from opsdb. The system manages itself by the same rules it manages everything else.
- **Single source of truth for everything operational.** Runner schedules, alert routes, Prometheus configs, secret backends, machine bootstraps, K8s clusters, cloud resources — all live in this one schema.

---

## Where to draw lines for the next paper

This schema sketches the shape. The paper will need to defend choices like:

- Polymorphic FKs vs explicit join tables (I leaned on `scope_type + scope_id` in a few places — debatable).
- The `_data_json` escape hatch — necessary for provider/distro-specific payloads, but the line between "typed JSON" and "code-as-data" needs to be drawn carefully.
- Whether `megavisor_instance` self-nesting is too clever. It's elegant but it puts a lot of weight on one field; the queries that walk it need indexes and clear access patterns.
- Versioning policy: every table or only "config" tables? Cost of versioning vs benefit per table type.

Ready to refine any of this. Where do you want to take it?
