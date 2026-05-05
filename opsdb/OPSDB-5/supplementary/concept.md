# Considering OPSDB-5 — Runner Design Across the Stack

Sitting with what we have. The papers and artifacts in the conversation give a layered foundation that OPSDB-5 inherits:

- **The book** establishes "data is king, logic is shell," operational vs application logic, the 0/1/∞ rule, comprehensive vs aggregate, idempotency as primary algorithmic property, and the DOS framing.
- **REM** demonstrated the comprehensive substrate with its package/service/connection model, megavisor wrapping, storage handler stacks, and runner-like script management — pre-K8s but architecturally mature.
- **sysync** showed what a tightly-scoped operational tool looks like when the principles are applied at one job: data-defined, idempotent, deterministic, planned, run locally, refusing to do anything beyond config.
- **DSNC** is the namespace discipline that prevents collision at scale.
- **OPSDB-9** named mechanisms, properties, and principles. Reconciler, Reactor, Puller, Verifier are mechanism families. Idempotency, Convergence, Liveness are property claims. Level-triggered-over-edge-triggered, idempotent retry, bound everything are principles.
- **OPSDB-2** specified the OpsDB design — the passive substrate the runners coordinate through.
- **OPSDB-4** specified the schema — the entity types runners read and write.

OPSDB-5 sits on all of this. It describes how runners are designed, what kinds of runners exist, how they coordinate, how they handle real operational scenarios, and how they relate to current standard practice in K8s shops.

Walking through what OPSDB-5 needs to cover.

## What OPSDB-5 is fundamentally about

OPSDB-5 is the runner design paper — the operational logic layer that sits above the OpsDB and acts in the world. The OpsDB has all the data; runners have all the logic. OPSDB-5 specifies how those runners are built, how they coordinate through the OpsDB, and how they handle the operational scenarios real organizations face.

It is not a catalog of every possible runner. It is a design specification: the runner pattern, its decomposition into kinds, its interaction model with the OpsDB and with authorities, and the disciplines that keep runners small, knowable, and reliable.

The structural claim mirrors OPSDB-2's: **runners are the operational logic shell around the OpsDB data; each runner is small enough to be fully knowable; runners coordinate through shared data, never directly with each other; the framework (shared libraries) is consistent across runners while each runner remains specific.**

## The runner kinds that need treatment

From OPSDB-9's mechanism families, certain mechanisms appear directly as runner kinds:

**Pullers** — Watch/Probe/Counter/Gauge/Histogram authorities and write cached observation. Read from authorities (Prometheus, Kubernetes API, cloud control planes, vault for non-secret metadata, identity providers, ticketing systems). Write to `observation_cache_*` tables in the OpsDB. Pure read on one side, scoped write on the other. The simplest runner shape, and the most common — there will be dozens of pullers in a mature OpsDB.

**Reconcilers** — Read desired state and observed state from the OpsDB, compute the diff, decide actions, execute through shared libraries. Level-triggered. Reconcilers are the workhorse runners; they include K8s controllers in spirit if not in implementation, configuration drift correctors, certificate renewers, capacity adjusters.

**Verifiers** — Check that scheduled work happened or scheduled state is correct. Produce `evidence_record` rows. The compliance-evidence backbone. A backup verifier confirms backup B happened today; a certificate scanner confirms certificates are valid; a compliance scanner confirms a policy is in effect.

**Schedulers (enforcement)** — Read `runner_schedule` rows and enforce them on target substrates. Either trigger another runner directly (within the OpsDB-aware infrastructure) or template a schedule onto a target host (cron, systemd timer, K8s CronJob) which then runs locally. The OpsDB stores the schedule data; this runner kind enforces it.

**Reactors** — Edge-triggered runners that respond to specific events. Less common than reconcilers (because edge-triggered loses missed events) but useful for low-latency operations: webhook receivers, K8s event watchers, alert handlers.

**Drift detectors** — A specialization of reconciler. Read desired vs observed; do not act, only propose. Submit `change_set` rows for a human or another runner to act on. Useful where automatic correction is too risky.

**Change set executors** — Read approved `change_set` rows and apply the field changes. The runner that closes the loop on change management.

**Compaction / reaper runners** — Apply retention policies. Trim `observation_cache_*` tables, expire `audit_log_entry` rows past their horizon (where allowed), reap `runner_job` rows with finished_time past retention.

**Bootstrap runners** — Set up new machines from minimal state. Read `host_group` and `package` data from the OpsDB, use templated configs, register the new machine in the OpsDB.

**Failover / failover-verifier runners** — Detect that a primary is failing, perform the failover, verify the failover succeeded, update the OpsDB to reflect the new primary.

These are not fixed; the runner kinds are an open set. OPSDB-5 enumerates the common ones, shows the pattern they share, and provides guidance for new kinds.

## The shared-library suite

Runners are small because the shared libs are good. OPSDB-5 needs to specify the shared library layer at the structural level (what categories of capability, what the contract looks like) without specifying the implementation:

- **OpsDB API client** — auth, retry, validation handling, change-set submission, structured output writes
- **Kubernetes operations** — apply manifests, query state, watch streams, helm operations
- **Cloud operations** — generic abstraction over AWS / GCP / Azure with provider-specific implementations behind one interface
- **Secret access** — pull from vault, sops, KMS at runtime; never persist
- **Logging and metrics emission** — uniform format the org consumes
- **Retry, backoff, idempotency markers** — patterns wrapped in helpers
- **Notifications** — email, chat, page; through configured channels
- **SSH / remote command execution** — for legacy substrate
- **Git operations** — clone, commit, push, tag, pull-request creation; for GitOps integration

Each library is versioned, tested, released. Runners pin to library versions and upgrade through change sets like any other config.

## GitOps as a first-class integration pattern

The user's framing pulls this directly: "helm config into git repos to make changes via gitops to k8s updates with normal pod deploys getting logged into opsdb by a gitops trigger." This is a concrete operational pattern that OPSDB-5 should model carefully because it represents how most modern K8s shops actually work.

The GitOps loop in OpsDB-aware form:

1. A change set in the OpsDB updates `k8s_helm_release_version` (the release spec) and the configuration variables scoped to it.
2. A **GitOps export runner** reads the new version, renders the helm values file, commits it to the appropriate git repo with a structured commit message linking back to the change set ID.
3. Argo CD / Flux / equivalent picks up the git change and applies it to the cluster.
4. A **K8s deploy watcher runner** observes the actual deployment in the cluster (via watch on the K8s API) and writes the rollout status, pod transitions, and final state to `observation_cache_state` and to a `runner_job` record.
5. Discrete output variables on the runner_job (rollout_succeeded, pod_count, image_digest_deployed) become queryable. Other runners consume them: a verifier confirms the deployed image matches the change set's intended image; a tag-tracker records "this version is now deployed in production at this time"; a compliance evidence runner records that the deployment followed the change-management discipline.

This shape preserves several disciplines:
- **The OpsDB is source of truth for intent** — the change set and helm release version describe what was wanted.
- **Git is source of truth for what's checked in** — Argo CD reconciles git-to-cluster.
- **The cluster is source of truth for live state** — pulled into the OpsDB cache.
- **The OpsDB is source of truth for the trail** — change set, commit reference, runner job, rollout outcome all tied together by IDs.

The user said: "fixed version artifact deployment, or tagged, etc." — these become trivial automations once the deploy outcomes are in the OpsDB. A "deploy this fixed version to staging" runner submits a change set with the version pinned; a "deploy whatever's tagged latest-stable" runner queries the artifact registry for the current tag, then submits a change set; a "promote staging deploy to production" runner reads the staging deploy's recorded image digest and submits a change set for production with that digest. All read structured data, write structured data, never special-case logic.

## Change-management gating per runner

The user said: "runners could be gated on change management approvals behind a queue of requests that has CM around it, or free to automate on their own." This is a per-runner-kind, per-target policy decision, expressible as data.

OPSDB-5 needs to make this explicit. For each runner, the schema records:

- Whether the runner submits change sets that require approval (gated)
- Whether the runner submits change sets that auto-approve under specific policies (queued behind CM but auto-pass for routine cases)
- Whether the runner acts directly without going through change management (only valid for observation-only writes — pullers, verifiers writing evidence, reaper runners trimming cache)

The gating is policy data. A drift-correction runner for low-stakes config might auto-approve its proposals. The same runner targeting a production database submits proposals that route to humans. Same runner code, different policies, different behavior.

This pattern matches OPSDB-2's stance that change-management rules are themselves data and that runners use the same change-set infrastructure as humans.

## Idempotency, level-triggering, and bound everything

From OPSDB-9 and the book, three principles dominate runner design:

**Idempotency** — every runner action must be safely retryable. The runner that ensures a configmap exists with specific values produces the same end state on every run. The runner that rotates a credential uses uniqueness keys so that a partial failure followed by a retry doesn't produce two rotations. OPSDB-5 specifies idempotency as a contract of every runner; runners that cannot be made idempotent are flagged in their `runner_spec` so operators know they require special care.

**Level-triggered over edge-triggered** — runners read current state and act on it, rather than reacting to event streams. A drift detector that compares OpsDB desired state against K8s observed state on every cycle catches drift regardless of what events were missed. A reactor that fires on K8s events misses anything that happened during a network partition. Both have their place; the default is level-triggered.

**Bound everything** — every runner has bounded resources. Bounded retry budget. Bounded execution time. Bounded queue depth for runners that queue work. Bounded memory. The runner_spec records the bounds; the runner enforces them at runtime; the runner_job records what bound was hit if execution stopped early.

OPSDB-5 needs a section on each, with the OpsDB schema fields that express the bounds and the runtime expectations that runners commit to.

## Stack walking and dependency awareness

The user mentioned "the stack walking concept" — this connects to the substrate hierarchy from §6 of OPSDB-4. A pod's full ancestry walks from `k8s_pod` → `megavisor_instance` (kubelet) → parent (the underlying VM, bare metal, or cloud resource) → up to the rack location or cloud region.

Runners benefit from this walking when they need to make decisions based on dependency. Examples:

- A reconciler that won't touch a service whose underlying VM is being decommissioned. The runner walks the stack from service → host_group → machine → megavisor_instance → checks whether the megavisor_instance has `decommissioned_time` set in any pending change set.
- A failover runner that needs to know what infrastructure is shared between primary and replica before deciding whether the failover is safe (if both replicas live in the same rack, the failover is dangerous).
- A capacity reconciler that walks K8s nodes to underlying machines to underlying hardware sets to compute available headroom.

The schema makes these queries possible because of the unified hierarchy. OPSDB-5 should include a section on **dependency-aware runners** showing how walking the substrate informs runner decisions that simpler tools cannot make.

## Standard K8s runbooks vs OpsDB-coordinated runbooks

The user said: "consider this... against standard k8s runbooks today." This contrast is worth doing explicitly in OPSDB-5. Walking through what changes:

**Standard K8s runbook today, "service is alerting":**

1. PagerDuty pages the on-call engineer (PagerDuty has its own schedule data).
2. Engineer opens Slack to find the incident channel.
3. Engineer opens Grafana to see the dashboard (URL bookmarked or remembered).
4. Engineer SSHes to a bastion or kubectl into the cluster.
5. Engineer runs `kubectl get pods -n production` to find the service.
6. Engineer runs `kubectl logs <pod>` to see what's happening.
7. Engineer guesses or recalls which runbook applies; opens the wiki, finds the runbook.
8. Engineer follows the runbook steps, maybe runs commands, maybe restarts something.
9. Engineer updates the incident channel with status.
10. Post-incident, engineer writes the runbook update somewhere (or doesn't).

The data is scattered: PagerDuty has the schedule, Grafana has the dashboard, kubectl output is ephemeral, the wiki has the runbook (maybe), Slack has the discussion. No single substrate knows what happened.

**OpsDB-coordinated runbook for the same alert:**

1. Alert fires; `alert_fire` row appears in the OpsDB. The escalation runner reads `service_escalation_path` for the affected service, queries `on_call_assignment` for the current on-call user, sends the page through the configured channel (PagerDuty, Opsgenie, or direct).
2. The page includes a link to a service incident view that resolves: the service's `runbook_reference` (with last-tested time), the relevant `dashboard_reference` URLs, the recent `change_set` history (was anything deployed recently?), the recent `evidence_record` history (did backup verification fail?), the dependent services from `service_connection`, the on-call schedule for upstream services if escalation is needed.
3. The engineer sees one page with the resolved context. They follow the runbook. If the runbook has documented commands, those commands are runner invocations submitted as runner_job requests, which the change-management policy may auto-approve for low-stakes operations or route for approval for higher-stakes.
4. As the engineer takes actions, runner_job rows record what was done, with attribution.
5. The incident channel is a `chat_authority_pointer` linked from the alert_fire; discussion happens there but the structured trail is in the OpsDB.
6. Post-incident, the runbook is updated through a change set; the runbook_reference's last_tested_time is updated; the new version is in version history.

The contrast isn't that the second is shorter — it's that the second produces a complete, queryable, auditable trail without extra effort, because the trail IS the data the system runs on.

OPSDB-5 should walk through this contrast for several common scenarios: alert response, deployment, certificate renewal, compliance evidence collection, drift correction. Each scenario shows the standard practice and the OpsDB-coordinated practice side by side. The benefit is not eliminating the work — it's making the work tracked, automated, and auditable.

## The runner as small unit of knowable logic

The user's framing — "runners designed like sysync" — pulls from sysync's discipline directly. Sysync is small (~3000 lines of Python), data-defined, idempotent, deterministic, run locally, refuses to do anything beyond config. Each runner in OPSDB-5's design follows the same discipline:

- **Small** — typically 200-500 lines of runner-specific logic, with shared libraries doing the heavy lifting
- **Data-defined** — reads its config from the OpsDB (its `runner_spec_version.runner_data_json`), produces structured outputs
- **Idempotent** — same inputs produce same end state
- **Deterministic** — the action sequence given a state is computable and inspectable; dry-run mode shows what would happen
- **Single-purpose** — one runner, one job; if a runner's job description has "and" in it, split it
- **Bounded** — explicit bounds on retry, time, memory, queue depth

This shape is replicable across runner kinds. A puller is 200 lines: query the authority, transform the response, write to the OpsDB. A verifier is 300 lines: check the condition, write the evidence. A simple reconciler is 500 lines: read desired and observed, compute diff, apply through shared libs.

OPSDB-5 should include skeletal pseudocode (not full implementations) showing the shape of each runner kind. Real implementations are organization-specific; the shape is the contract.

## Helm-into-git-into-cluster as the worked example

The user pointed at this specific flow as a worked example. OPSDB-5 should treat it as the central illustrated pattern — the running example threaded through the paper to show how runners coordinate.

The cast of runners involved in one helm-via-gitops deployment:

1. **Helm spec change-set runner** — reads a submitted change set targeting `k8s_helm_release_version` and its configuration variables. Validates per the API. Routes for approval per policy.
2. **Helm git exporter** — on approved change set, renders the helm values file with the resolved configuration variables, commits to the appropriate git repo, tags with the change set ID, opens a pull request or pushes to the watched branch.
3. **Argo CD / Flux** — not an OpsDB runner; an external tool watching git. Reads the new commit, applies to the cluster.
4. **K8s deploy watcher** — watches the cluster's deployment status (via watch on the K8s API), writes pod state transitions to `observation_cache_state`, writes the final rollout outcome to `runner_job_output_var` rows.
5. **Image digest verifier** — once rollout completes, queries the cluster for actual deployed image digests, compares against the change set's intended digests, writes an evidence record. If mismatch, files a compliance finding.
6. **Deploy event publisher** — writes a structured "deploy occurred" record that other runners can react to: tag-trackers, capacity-adjusters, rolling-deploy-coordinators.
7. **Drift detector** — on a schedule, compares OpsDB-known helm release version against cluster-observed helm release version. If drift, files a finding or auto-corrects (per policy).

Each runner is small, knowable, single-purpose. They coordinate through OpsDB rows. No runner directs another. The full deployment trail — from change set submission to verified production rollout — is queryable as a join across `change_set`, `runner_job`, `evidence_record`, `observation_cache_state`, and `audit_log_entry`.

This running example demonstrates the design at every level: the OpsDB has the data, runners are the logic, the framework is the shared libraries, the discipline is in the small single-purpose units, and standard K8s practice is enriched (not replaced) by being OpsDB-aware.

## Document structure for OPSDB-5

A working outline:

**§1 Introduction** — Purpose, relationship to OPSDB-9/2/3, reader assumptions.

**§2 The runner pattern** — What every runner is and does. Reads from OpsDB, acts in the world, writes to OpsDB. Small, single-purpose, data-defined, idempotent, level-triggered, bounded.

**§3 Runner kinds** — Pullers, reconcilers, verifiers, schedulers, reactors, drift detectors, change-set executors, reapers, bootstrappers, failover handlers. Each with its purpose, inputs, outputs, and skeletal shape.

**§4 The shared library suite** — Categories of capability: OpsDB client, K8s ops, cloud ops, secret access, logging/metrics, retry/backoff/idempotency, notifications, git ops. The contract for each.

**§5 Coordination through shared substrate** — How runners coordinate without orchestration. Reading each other's outputs. Submitting change sets. Reactors triggered by other runners' writes. Decentralization through shared data.

**§6 Idempotency, level-triggering, and bound everything** — The three load-bearing disciplines. How each is enforced in runner design. Schema fields that record bounds and contracts.

**§7 Change management gating** — Per-runner policy. Direct write (observation only). Auto-approved change sets. Approval-required change sets. The discipline of choosing which gating each runner gets.

**§8 Stack-walking and dependency-aware runners** — Using the substrate hierarchy from OPSDB-4 to make decisions that simpler tools cannot. Dependency analysis. Failure-domain-aware operations.

**§9 GitOps integration** — The helm-into-git-into-cluster pattern as a worked example. What runners participate. What data flows through the OpsDB at each step. How the trail composes.

**§10 Standard practice vs OpsDB-coordinated practice** — Side-by-side walkthroughs of common operational scenarios: alert response, deployment, certificate renewal, compliance evidence, drift correction. The contrast made concrete.

**§11 Designing new runners** — Guidance for organizations adding runner kinds the paper doesn't enumerate. The discipline transfers; the specifics adapt.

**§12 Anti-patterns** — What runners should not do. Orchestrating other runners directly. Storing state outside the OpsDB. Reinventing what shared libraries provide. Acting on stale cache without freshness checks. Embedding logic in template variables.

**§13 Closing** — Restatement of the structural claim. The runner layer as the operational logic shell around the OpsDB data substrate.

## Open questions before drafting

1. **How concrete should the runner pseudocode be?** Skeletal shape (input → action → output) is helpful; full implementations would lock to specific stacks (Python, Go, etc.). Probably skeletal, with a note that the runner itself is in any language.

2. **How deep into K8s specifics should §9 go?** The helm-via-gitops example needs enough detail to be illustrative but not so much it becomes a K8s tutorial. Probably one running example carried through, with details on the OpsDB-side mechanics.

3. **Should §10's contrast be its own appendix?** The side-by-side scenarios are powerful but lengthy. Possibly an appendix with the structured comparison.

4. **How much of the shared library suite gets specified?** Categories yes; specific APIs no. OPSDB-5 specifies the contract surface (what each library category does); the implementation is per-org.

5. **Whether to include "runner of runners" patterns.** Some runners spawn child runners (a fleet-wide deploy runner that issues per-host runner_jobs). This is fine architecturally but worth being explicit about — the parent doesn't direct the children, it submits work; the children pick up work; coordination through the OpsDB.

6. **The relationship to existing tools.** Argo CD, Flux, Crossplane, Pulumi, Terraform, Salt, Ansible, Puppet — all do some of what OPSDB-5 describes. Should the paper map them onto the runner-kind taxonomy explicitly? Probably yes, briefly, in a single section: "these tools fill these runner-kind slots; the OpsDB-aware version of each adds the writes-back-to-OpsDB discipline."

7. **Bootstrapping — where it sits.** Bootstrap runners are a special case because they need to operate in a state where the OpsDB is reachable but the host being bootstrapped isn't yet in it. Templated configs, locally cached OpsDB slices (per OPSDB-2 §4.8 and §12.8), and explicit registration steps. Probably gets its own subsection or appendix.

## What this paper avoids

- Specifying the implementation language (any language can build runners)
- Specifying the deployment platform for runners (K8s pods, systemd services, lambdas, serverless — all valid)
- Reproducing the OpsDB schema (refer to OPSDB-4)
- Reproducing the design rationale (refer to OPSDB-2)
- Building a runner library or framework as artifact (separate concern)
- Becoming a K8s tutorial or GitOps tutorial (the patterns are illustrated; the tutorials live elsewhere)

---

Ready to refine the plan or proceed to a full OPSDB-5 plan in the tightened style we used for OPSDB-4.
