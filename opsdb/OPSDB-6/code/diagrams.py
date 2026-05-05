#!/usr/bin/env python3
"""
OPSDB OPSDB-6 Diagrams — The OpsDB API Layer
8 figures covering the API gate, authorization, change_set lifecycle, versioning,
optimistic concurrency, runner report keys, and audit chain.
Output: PNG files to ../figures/
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge, Rectangle, Polygon
import numpy as np
import os

# ================================================================
# GLOBAL STYLE
# ================================================================

# Light mode
if True:
    # ── Global palette (Kindle / light mode) ──
    BG      = '#ffffff'
    PAN     = '#f0ede8'
    GOLD    = '#a07820'
    SILVER  = '#505860'
    CYAN    = '#1a8a80'
    MAG     = '#a03058'
    BLUE    = '#2855a0'
    GREEN   = '#2a7a3a'
    RED     = '#b82020'
    ORANGE  = '#c06a18'
    WHITE   = '#1a1a22'
    DIM     = '#908e88'
    PURPLE  = '#6040a0'
else:
    # ── Global palette (D7.2) ──
    BG      = '#0a0a12'
    PAN     = '#12121f'
    GOLD    = '#d4a843'
    SILVER  = '#a0a8b8'
    CYAN    = '#4ecdc4'
    MAG     = '#c74b7a'
    BLUE    = '#5b8def'
    GREEN   = '#6bcf7f'
    RED     = '#e05555'
    ORANGE  = '#e8944a'
    WHITE   = '#e8e8f0'
    DIM     = '#555570'
    PURPLE  = '#9b7bd4'
    

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
os.makedirs(outdir, exist_ok=True)


def style_axes(ax):
    ax.set_facecolor(PAN)
    for spine in ax.spines.values():
        spine.set_color(DIM)
        spine.set_linewidth(0.5)
    ax.tick_params(colors=DIM, labelsize=9)


def save(fig, filename):
    path = os.path.join(outdir, filename)
    fig.savefig(path, dpi=180, facecolor=BG, bbox_inches='tight', pad_inches=0.3)
    plt.close(fig)
    print("  Saved: %s" % filename)


# ================================================================
# FIG 1: 10-STEP GATE AS CONCENTRIC RINGS
# Type: 4 (Geometric Cross-Section)
# Shows: every operation passes through 10 enforcement steps in order;
#        substrate is the protected center; the gate is uniform across all ops.
# ================================================================

fig, ax = plt.subplots(figsize=(16, 14), facecolor=BG)
ax.set_facecolor(BG)

steps = [
    ('1. Authentication',   'IdP / secret backend'),
    ('2. Authorization',    'Five-layer model'),
    ('3. Schema validation','Shape vs registered schema'),
    ('4. Bound validation', 'Declarative constraints'),
    ('5. Policy evaluation','Active policy rows'),
    ('6. Versioning prep',  'Version row pending'),
    ('7. Change-mgmt route','Approval requirements'),
    ('8. Audit logging',    'audit_log_entry written'),
    ('9. Execution',        'Atomic apply'),
    ('10. Response',        'Result + metadata'),
]

ring_colors = [CYAN, BLUE, PURPLE, MAG, ORANGE, GOLD, GREEN, GREEN, GOLD, CYAN]

inner_r = 1.2
ring_w = 0.55
gap = 0.05

# Draw substrate at center
substrate = Circle((0, 0), inner_r, facecolor=PAN, edgecolor=GOLD,
                   linewidth=2.5, zorder=10)
ax.add_patch(substrate)
ax.text(0, 0.15, 'OpsDB', ha='center', va='center',
        fontsize=15, color=GOLD, fontweight='bold', zorder=11)
ax.text(0, -0.25, 'substrate', ha='center', va='center',
        fontsize=11, color=SILVER, zorder=11)
ax.text(0, -0.55, '(passive)', ha='center', va='center',
        fontsize=9, color=DIM, style='italic', zorder=11)

# Draw the ten rings
count = 0
for i, (label, sublabel) in enumerate(steps):
    r_in = inner_r + i * (ring_w + gap)
    r_out = r_in + ring_w
    color = ring_colors[i]

    ring = Wedge((0, 0), r_out, 0, 360, width=ring_w,
                 facecolor=color, edgecolor=BG, linewidth=2,
                 alpha=0.18, zorder=5)
    ax.add_patch(ring)

    # Ring outline for crispness
    outer = Circle((0, 0), r_out, fill=False, edgecolor=color,
                   linewidth=1.2, alpha=0.6, zorder=6)
    ax.add_patch(outer)

    offsetY = 0
    if count % 2 == 1:
        offsetY = 0.2 + (i * 0.3)
    else:
        offsetY = -0.2 + (i * -0.3)

    # Step label on the ring (right side)
    angle = 0  # right side of each ring
    r_mid = (r_in + r_out) / 2
    ax.text(r_mid + 0.7, 0.18 + offsetY, label, ha='center', va='center',
            fontsize=9.5, color=WHITE, fontweight='bold', zorder=7)
    ax.text(r_mid + 0.7, -0.18 + offsetY, sublabel, ha='center', va='center',
            fontsize=7.5, color=color, zorder=7)

    count += 1

# Operation arrow coming in from the left
arrow_y = 0
ax.annotate('', xy=(-inner_r - 0.05, arrow_y),
            xytext=(-(inner_r + 10 * (ring_w + gap)) - 1.5, arrow_y),
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=2.5),
            zorder=12)
ax.text(-(inner_r + 10 * (ring_w + gap)) - 1.7, 0.35, 'Operation',
        ha='left', va='bottom', fontsize=12, color=GOLD, fontweight='bold')
ax.text(-(inner_r + 10 * (ring_w + gap)) - 1.7, -0.45, '(human, runner,\nor auditor)',
        ha='left', va='top', fontsize=9, color=SILVER, style='italic')

# Bottom note
ax.text(0, -(inner_r + 10 * (ring_w + gap)) - 0.6,
        'Every operation flows through every ring, in order. First denial fails the operation.',
        ha='center', va='top', fontsize=10.5, color=SILVER, style='italic')

ax.set_xlim(-9.5, 8.5)
ax.set_ylim(-8.2, 8.2)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('The OpsDB API as a 10-Step Gate\nUniform enforcement across every operation',
             color=GOLD, fontsize=16, fontweight='bold', pad=15)

save(fig, 'infra5_01_ten_step_gate_rings.png')


# ================================================================
# FIG 2: FIVE-LAYER AUTHORIZATION STACK
# Type: 7 (Progression/Sequence)
# Shows: an operation flows through five layers; denial at any layer halts;
#        all five must pass for the operation to proceed.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 11), facecolor=BG)
ax.set_facecolor(BG)

layers = [
    ('Layer 1', 'Standard role + group',
     'ops_user_role_member,\nops_group_member',
     'Baseline operation class', BLUE),
    ('Layer 2', 'Per-entity governance',
     '_requires_group on row',
     'Sensitive row escalation', CYAN),
    ('Layer 3', 'Per-field classification',
     '_access_classification',
     'Clearance level vs sensitivity', PURPLE),
    ('Layer 4', 'Per-runner authority',
     'runner_capability,\nrunner_*_target bridges',
     'Declared scope check', ORANGE),
    ('Layer 5', 'Policy rules',
     "policy.policy_type =\n'access_control'",
     'Time-of-day, SoD, tenure', GOLD),
]

# Two example operations: one passes, one denied at layer 3
n = len(layers)
y_pass = 7.0
y_deny = 2.5
layer_w = 2.6
layer_h = 2.3
x0 = 1.5
gap = 0.7

# Draw layer boxes for each operation
for op_idx, (op_y, op_label, deny_at, op_color) in enumerate([
    (y_pass, 'Operation A: Service owner reads service config', None, GREEN),
    (y_deny, 'Operation B: Auditor reads confidential_finance field', 2, RED),
]):
    # Operation label
    ax.text(x0 - 0.7, op_y + layer_h/2, op_label,
            ha='right', va='center', fontsize=11, color=op_color, fontweight='bold')

    for i, (layer_n, layer_name, layer_data, layer_check, color) in enumerate(layers):
        x = x0 + i * (layer_w + gap)

        if deny_at is not None and i > deny_at:
            # Layer not reached
            box = FancyBboxPatch((x, op_y), layer_w, layer_h,
                                 boxstyle='round,pad=0.05',
                                 facecolor=PAN, edgecolor=DIM,
                                 linewidth=1, alpha=0.4)
            ax.add_patch(box)
            ax.text(x + layer_w/2, op_y + layer_h*0.7, layer_n,
                    ha='center', va='center', fontsize=9, color=DIM)
            ax.text(x + layer_w/2, op_y + layer_h*0.4, '(not reached)',
                    ha='center', va='center', fontsize=8, color=DIM, style='italic')
        elif deny_at is not None and i == deny_at:
            # Denying layer - red
            box = FancyBboxPatch((x, op_y), layer_w, layer_h,
                                 boxstyle='round,pad=0.05',
                                 facecolor=PAN, edgecolor=RED,
                                 linewidth=2.5)
            ax.add_patch(box)
            ax.text(x + layer_w/2, op_y + layer_h*0.78, layer_n,
                    ha='center', va='center', fontsize=9.5, color=RED, fontweight='bold')
            ax.text(x + layer_w/2, op_y + layer_h*0.55, layer_name,
                    ha='center', va='center', fontsize=9, color=WHITE, fontweight='bold')
            ax.text(x + layer_w/2, op_y + layer_h*0.30, layer_data,
                    ha='center', va='center', fontsize=7.5, color=SILVER)
            ax.text(x + layer_w/2, op_y + layer_h*0.08, 'DENIED',
                    ha='center', va='center', fontsize=10, color=RED, fontweight='bold')
        else:
            # Pass layer - green
            box = FancyBboxPatch((x, op_y), layer_w, layer_h,
                                 boxstyle='round,pad=0.05',
                                 facecolor=PAN, edgecolor=color,
                                 linewidth=2)
            ax.add_patch(box)
            ax.text(x + layer_w/2, op_y + layer_h*0.78, layer_n,
                    ha='center', va='center', fontsize=9.5, color=color, fontweight='bold')
            ax.text(x + layer_w/2, op_y + layer_h*0.55, layer_name,
                    ha='center', va='center', fontsize=9, color=WHITE, fontweight='bold')
            ax.text(x + layer_w/2, op_y + layer_h*0.30, layer_data,
                    ha='center', va='center', fontsize=7.5, color=SILVER)
            ax.text(x + layer_w/2, op_y + layer_h*0.08, 'PASS',
                    ha='center', va='center', fontsize=9.5, color=GREEN, fontweight='bold')

        # Arrow to next layer (or to outcome)
        if i < n - 1 and (deny_at is None or i < deny_at):
            ax.annotate('', xy=(x + layer_w + gap - 0.05, op_y + layer_h/2),
                        xytext=(x + layer_w + 0.05, op_y + layer_h/2),
                        arrowprops=dict(arrowstyle='->', color=op_color, lw=1.8))

    # Outcome
    out_x = x0 + n * (layer_w + gap)
    if deny_at is None:
        outcome_box = FancyBboxPatch((out_x, op_y + 0.3), 2.4, layer_h - 0.6,
                                     boxstyle='round,pad=0.05',
                                     facecolor=GREEN, edgecolor=GREEN,
                                     linewidth=2, alpha=0.25)
        ax.add_patch(outcome_box)
        ax.text(out_x + 1.2, op_y + layer_h/2 + 0.2, 'OPERATION',
                ha='center', va='center', fontsize=10, color=GREEN, fontweight='bold')
        ax.text(out_x + 1.2, op_y + layer_h/2 - 0.2, 'PROCEEDS',
                ha='center', va='center', fontsize=10, color=GREEN, fontweight='bold')
    else:
        outcome_box = FancyBboxPatch((out_x, op_y + 0.3), 2.4, layer_h - 0.6,
                                     boxstyle='round,pad=0.05',
                                     facecolor=RED, edgecolor=RED,
                                     linewidth=2, alpha=0.25)
        ax.add_patch(outcome_box)
        ax.text(out_x + 1.2, op_y + layer_h/2 + 0.3, 'OPERATION',
                ha='center', va='center', fontsize=10, color=RED, fontweight='bold')
        ax.text(out_x + 1.2, op_y + layer_h/2 - 0.05, 'REJECTED',
                ha='center', va='center', fontsize=10, color=RED, fontweight='bold')
        ax.text(out_x + 1.2, op_y + layer_h/2 - 0.45, '+ audit entry',
                ha='center', va='center', fontsize=8, color=SILVER, style='italic')

# Footer note
ax.text(10.0, 0.7,
        'AND-gate semantics: every layer must PASS. First denial halts the operation.\n'
        'All five layers are data; changing what a caller can do is changing rows, not code.',
        ha='center', va='center', fontsize=10.5, color=SILVER, style='italic')

ax.set_xlim(-3.5, 23.5)
ax.set_ylim(-0.3, 11.0)
ax.set_aspect('auto')
ax.axis('off')
ax.set_title('Five-Layer Authorization Model\nEvery operation evaluates all five; first denial fails',
             color=GOLD, fontsize=16, fontweight='bold', pad=12)

save(fig, 'infra5_02_five_layer_authorization.png')


# ================================================================
# FIG 3: STAKEHOLDER ROUTING FAN-OUT
# Type: 5 (Connection Map)
# Shows: a change_set's field changes fan out through entity ownership
#        bridges to required approver groups; multi-source approval composition.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 12), facecolor=BG)
ax.set_facecolor(BG)

# Three columns: change_set / field_changes / approver_groups
# Field changes hit different entity types, each producing different approval rules

# Column 1: change_set (left)
cs_box = FancyBboxPatch((0.5, 5.0), 3.0, 2.0,
                        boxstyle='round,pad=0.1',
                        facecolor=PAN, edgecolor=GOLD, linewidth=2.5)
ax.add_patch(cs_box)
ax.text(2.0, 6.5, 'change_set', ha='center', va='center',
        fontsize=12, color=GOLD, fontweight='bold')
ax.text(2.0, 6.05, '#42891', ha='center', va='center',
        fontsize=10, color=WHITE)
ax.text(2.0, 5.55, '"Q3 deployment +', ha='center', va='center',
        fontsize=9, color=SILVER)
ax.text(2.0, 5.25, 'security policy update"', ha='center', va='center',
        fontsize=9, color=SILVER)

# Column 2: field changes (4 rows)
field_changes = [
    ('change_set_field_change', 'service.config_json',     'service: user-api',          CYAN,   9.5),
    ('change_set_field_change', 'k8s_workload.replicas',   'workload: payments',         BLUE,   7.7),
    ('change_set_field_change', 'security_zone.zone_data', 'security_zone: pci',         MAG,    5.9),
    ('change_set_field_change', 'compliance_regime.scope', 'regime: PCI_DSS',            ORANGE, 4.1),
    ('change_set_field_change', '_schema_field.constraint','_schema_*: schema change',   PURPLE, 2.3),
]

fc_x = 6.0
fc_w = 3.6
fc_h = 1.3

for tbl, field, target, color, y in field_changes:
    fc_box = FancyBboxPatch((fc_x, y), fc_w, fc_h,
                            boxstyle='round,pad=0.05',
                            facecolor=PAN, edgecolor=color, linewidth=1.8)
    ax.add_patch(fc_box)
    ax.text(fc_x + fc_w/2, y + fc_h*0.72, tbl,
            ha='center', va='center', fontsize=8, color=color, style='italic')
    ax.text(fc_x + fc_w/2, y + fc_h*0.43, field,
            ha='center', va='center', fontsize=9.5, color=WHITE, fontweight='bold')
    ax.text(fc_x + fc_w/2, y + fc_h*0.15, target,
            ha='center', va='center', fontsize=8.5, color=SILVER)

    # Arrow from change_set to field_change
    ax.annotate('', xy=(fc_x - 0.05, y + fc_h/2),
                xytext=(2.0 + 1.5, 6.0),
                arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.2, alpha=0.6))

# Column 3: approver groups
# Each field_change routes to one or more groups via ownership/policy
approver_groups = [
    ('Service owner',          'user-api team',    CYAN,   10.0),
    ('Production ops',         'prod-ops group',   BLUE,    8.5),
    ('Security team',          'sec-review group', MAG,     6.5),
    ('Compliance team',        'compliance group', ORANGE,  4.5),
    ('Schema steward',         'schema-stewards',  PURPLE,  2.5),
]

ag_x = 13.5
ag_w = 3.5
ag_h = 1.05

for grp, members, color, y in approver_groups:
    ag_box = FancyBboxPatch((ag_x, y), ag_w, ag_h,
                            boxstyle='round,pad=0.05',
                            facecolor=PAN, edgecolor=color, linewidth=2)
    ax.add_patch(ag_box)
    ax.text(ag_x + ag_w/2, y + ag_h*0.65, grp,
            ha='center', va='center', fontsize=10, color=color, fontweight='bold')
    ax.text(ag_x + ag_w/2, y + ag_h*0.25, members,
            ha='center', va='center', fontsize=8.5, color=SILVER)

# Routing arrows: each field_change -> one or more groups
# Per the paper: a service config change routes to service owner + prod ops
# A security zone touch routes to security team
# A compliance change routes to compliance
# A schema change routes to schema steward
# Production-namespace changes always also route to prod ops
routes = [
    # (fc_index, ag_index)
    (0, 0),  # service.config -> service owner
    (0, 1),  # service.config -> production ops (prod ns)
    (1, 0),  # k8s replicas -> service owner (workload owner)
    (1, 1),  # k8s replicas -> production ops
    (2, 2),  # security_zone -> security team
    (2, 1),  # security_zone -> production ops
    (3, 3),  # compliance scope -> compliance team
    (3, 2),  # compliance scope -> security team
    (4, 4),  # schema -> schema steward
]

for fc_i, ag_i in routes:
    fc_y = field_changes[fc_i][4]
    ag_y = approver_groups[ag_i][3]
    color = approver_groups[ag_i][2]
    ax.annotate('',
                xy=(ag_x - 0.05, ag_y + ag_h/2),
                xytext=(fc_x + fc_w + 0.05, fc_y + fc_h/2),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.3, alpha=0.55,
                                connectionstyle='arc3,rad=0.05'))

# Right side: AND composition note
comp_y = 0.5
ax.text(15.25, comp_y + 0.6,
        'change_set_approval_required (AND)',
        ha='center', va='center', fontsize=10.5, color=GOLD, fontweight='bold')
ax.text(15.25, comp_y + 0.2,
        'All five rows must be fulfilled before status -> approved',
        ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# Column headers
ax.text(2.0, 8.5, 'change_set', ha='center', va='center',
        fontsize=12, color=GOLD, fontweight='bold')
ax.text(7.8, 11.3, 'Per-field changes\n(walk ownership/stakeholder bridges)',
        ha='center', va='center', fontsize=10.5, color=WHITE, fontweight='bold')
ax.text(15.25, 11.45, 'Approver groups\n(computed by approval_rule policies)',
        ha='center', va='center', fontsize=10.5, color=WHITE, fontweight='bold')

ax.set_xlim(-0.5, 18.0)
ax.set_ylim(-0.5, 12.5)
ax.set_aspect('auto')
ax.axis('off')
ax.set_title('Stakeholder Routing — Multi-Source Approval Composition\n'
             'One change_set, N field changes, M approver groups',
             color=GOLD, fontsize=15, fontweight='bold', pad=12)

save(fig, 'infra5_03_stakeholder_routing_fanout.png')


# ================================================================
# FIG 4: CHANGE_SET LIFECYCLE STATE MACHINE
# Type: 4 (Geometric)
# Shows: every change_set's possible states and transitions; the linear
#        approval path and the branching paths to terminal failure states.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 10), facecolor=BG)
ax.set_facecolor(BG)

# States laid out roughly linearly with terminal branches below
states = {
    'draft':            (1.5,  6.0, SILVER,  'Editing'),
    'submitted':        (4.0,  6.0, BLUE,    'API received'),
    'validating':       (6.5,  6.0, CYAN,    'Lint, schema, semantic, policy'),
    'pending_approval': (9.5,  6.0, ORANGE,  'Awaiting approvers'),
    'approved':         (12.7, 6.0, GOLD,    'In to-perform queue'),
    'applied':          (15.5, 6.0, GREEN,   'Field changes committed'),
    'rejected':         (9.5,  2.5, RED,     'Required approver rejected'),
    'expired':          (10.5, 2.5, RED,     'Deadline passed'),
    'cancelled':        (11.5, 2.5, RED,     'Submitter withdrew'),
    'failed':           (15.5, 2.5, RED,     'Apply chunk failed; rolled'),
}

# Draw state boxes
state_w = 2.0
state_h = 0.95

for name, (x, y, color, sub) in states.items():
    is_terminal = name in ('rejected', 'expired', 'cancelled', 'failed', 'applied')
    edge_w = 2.5 if is_terminal else 1.8

    box = FancyBboxPatch((x - state_w/2, y - state_h/2), state_w, state_h,
                         boxstyle='round,pad=0.05',
                         facecolor=PAN, edgecolor=color, linewidth=edge_w)
    ax.add_patch(box)
    ax.text(x, y + 0.16, name, ha='center', va='center',
            fontsize=10, color=color, fontweight='bold')
    ax.text(x, y - 0.22, sub, ha='center', va='center',
            fontsize=7.5, color=SILVER, style='italic')

    # Terminal indicator
    if is_terminal and name != 'applied':
        ax.text(x, y - state_h/2 - 0.25, 'terminal',
                ha='center', va='center', fontsize=7, color=DIM, style='italic')
    if name == 'applied':
        ax.text(x, y - state_h/2 - 0.25, 'success terminal',
                ha='center', va='center', fontsize=7.5, color=GREEN, style='italic',
                fontweight='bold')


def state_arrow(s_from, s_to, color, style='-', curve=0.0, lw=1.8):
    x1, y1, _, _ = states[s_from]
    x2, y2, _, _ = states[s_to]
    # Compute edge points on the boxes
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        # primarily horizontal
        if dx > 0:
            xs = x1 + state_w/2
            xe = x2 - state_w/2
        else:
            xs = x1 - state_w/2
            xe = x2 + state_w/2
        ys = y1
        ye = y2
    else:
        if dy > 0:
            ys = y1 + state_h/2
            ye = y2 - state_h/2
        else:
            ys = y1 - state_h/2
            ye = y2 + state_h/2
        xs = x1
        xe = x2

    arrow = FancyArrowPatch((xs, ys), (xe, ye),
                            arrowstyle='->', color=color,
                            linewidth=lw, alpha=0.85,
                            linestyle=style,
                            connectionstyle='arc3,rad=%f' % curve,
                            mutation_scale=15)
    ax.add_patch(arrow)


# Forward path
state_arrow('draft', 'submitted', GOLD)
state_arrow('submitted', 'validating', GOLD)
state_arrow('validating', 'pending_approval', GOLD)
state_arrow('pending_approval', 'approved', GOLD)
state_arrow('approved', 'applied', GREEN, lw=2.2)

# Validation failure back to draft
state_arrow('validating', 'draft', SILVER, style='--', curve=0.4)

# Branches to terminal failures
state_arrow('pending_approval', 'rejected', RED)
state_arrow('pending_approval', 'expired', RED, curve=-0.1)
state_arrow('pending_approval', 'cancelled', RED, curve=-0.2)
state_arrow('approved', 'failed', RED)

# Annotations on key transitions
ax.text(2.75, 6.4, 'submit', ha='center', fontsize=8, color=GOLD, style='italic')
ax.text(5.25, 6.4, 'auto', ha='center', fontsize=8, color=GOLD, style='italic')
ax.text(8.0, 6.4, 'validation pass', ha='center', fontsize=8, color=GOLD, style='italic')
ax.text(11.1, 6.4, 'all approvals', ha='center', fontsize=8, color=GOLD, style='italic')
ax.text(14.1, 6.4, 'executor applies', ha='center', fontsize=8, color=GREEN, style='italic')
ax.text(4.0, 4.6, 'validation fail\n(returns for edit)', ha='center',
        fontsize=8, color=SILVER, style='italic')

# Legend / key
legend_x = 0.5
legend_y = 0.4
ax.text(legend_x, legend_y + 0.5, 'Edge legend:', fontsize=9.5, color=GOLD, fontweight='bold')
ax.plot([legend_x + 1.5, legend_x + 2.2], [legend_y + 0.5, legend_y + 0.5],
        color=GOLD, lw=1.8)
ax.text(legend_x + 2.4, legend_y + 0.5, 'Forward progress',
        fontsize=9, color=WHITE, va='center')
ax.plot([legend_x + 4.8, legend_x + 5.5], [legend_y + 0.5, legend_y + 0.5],
        color=GREEN, lw=2.2)
ax.text(legend_x + 5.7, legend_y + 0.5, 'Apply (executor runner)',
        fontsize=9, color=WHITE, va='center')
ax.plot([legend_x + 9.0, legend_x + 9.7], [legend_y + 0.5, legend_y + 0.5],
        color=RED, lw=1.8)
ax.text(legend_x + 9.9, legend_y + 0.5, 'To terminal failure',
        fontsize=9, color=WHITE, va='center')
ax.plot([legend_x + 12.5, legend_x + 13.2], [legend_y + 0.5, legend_y + 0.5],
        color=SILVER, lw=1.5, linestyle='--')
ax.text(legend_x + 13.4, legend_y + 0.5, 'Validation rework',
        fontsize=9, color=WHITE, va='center')

ax.set_xlim(-0.3, 17.5)
ax.set_ylim(0.0, 8.0)
ax.set_aspect('auto')
ax.axis('off')
ax.set_title('change_set Lifecycle\nStates and transitions as OpsDB-row data',
             color=GOLD, fontsize=16, fontweight='bold', pad=12)

save(fig, 'infra5_04_change_set_lifecycle.png')


# ================================================================
# FIG 5: FULL-STATE VS CHAIN-OF-DELTAS VERSIONING
# Type: 4 (Geometric) + cost curve
# Shows: two-panel comparison; full-state stores N copies but reads in O(1);
#        delta chain stores deltas but reads in O(N).
# ================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9),
                                facecolor=BG, gridspec_kw={'wspace': 0.30})
ax1.set_facecolor(PAN)
ax2.set_facecolor(PAN)

# === LEFT PANEL: chain of deltas ===
ax1.set_title('Chain-of-deltas (rejected)\nReconstruction = fold over chain',
              color=RED, fontsize=13, fontweight='bold', pad=10)

# Draw a chain of delta nodes
n_versions = 6
chain_y = 6.5
node_x = np.linspace(0.8, 8.5, n_versions)

for i, x in enumerate(node_x):
    if i == 0:
        # base state
        rect = FancyBboxPatch((x - 0.45, chain_y - 0.45), 0.9, 0.9,
                              boxstyle='round,pad=0.05',
                              facecolor=PAN, edgecolor=BLUE, linewidth=2)
        ax1.add_patch(rect)
        ax1.text(x, chain_y + 0.05, 'V0', ha='center', va='center',
                 fontsize=10, color=BLUE, fontweight='bold')
        ax1.text(x, chain_y - 0.15, 'base', ha='center', va='center',
                 fontsize=7, color=SILVER, style='italic')
    else:
        rect = FancyBboxPatch((x - 0.40, chain_y - 0.40), 0.80, 0.80,
                              boxstyle='round,pad=0.05',
                              facecolor=PAN, edgecolor=ORANGE, linewidth=1.6)
        ax1.add_patch(rect)
        ax1.text(x, chain_y + 0.05, 'd%d' % i, ha='center', va='center',
                 fontsize=10, color=ORANGE, fontweight='bold')
        ax1.text(x, chain_y - 0.18, 'delta', ha='center', va='center',
                 fontsize=7, color=SILVER, style='italic')

    if i < n_versions - 1:
        ax1.annotate('', xy=(node_x[i+1] - 0.45, chain_y),
                     xytext=(x + 0.45, chain_y),
                     arrowprops=dict(arrowstyle='->', color=DIM, lw=1.2))

# Reconstruction at version 5 — must walk all
recon_x = node_x[-1]
ax1.annotate('', xy=(recon_x, chain_y - 1.0),
             xytext=(recon_x, chain_y - 0.55),
             arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))
ax1.text(recon_x, chain_y - 1.4, 'get_at(V5)?',
         ha='center', va='center', fontsize=9.5, color=RED, fontweight='bold')

# Show fold over chain
fold_y = chain_y - 2.5
ax1.text(node_x[0], fold_y + 0.5, 'fold:', ha='center',
         fontsize=10, color=WHITE, fontweight='bold')
ax1.plot(node_x, [fold_y]*n_versions, 'o-', color=RED,
         markersize=10, linewidth=1.8, alpha=0.7)
for i, x in enumerate(node_x):
    ax1.text(x, fold_y - 0.4, '+' if i > 0 else 'V0',
             ha='center', va='center', fontsize=9, color=RED)

# Cost annotation
ax1.text(4.5, 2.5, 'Read cost: O(N) per query',
         ha='center', va='center', fontsize=12, color=RED, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.4', facecolor=BG, edgecolor=RED))
ax1.text(4.5, 1.7, 'Storage: small (deltas only)',
         ha='center', va='center', fontsize=10, color=SILVER)
ax1.text(4.5, 1.0,
         'Diff between versions = fold both, compare results',
         ha='center', va='center', fontsize=9, color=SILVER, style='italic')

ax1.set_xlim(0, 9.2)
ax1.set_ylim(0.4, 8.0)
ax1.axis('off')

# === RIGHT PANEL: full-state per version (chosen) ===
ax2.set_title('Full-state per version (chosen)\nReconstruction = single row lookup',
              color=GREEN, fontsize=13, fontweight='bold', pad=10)

versions_y = 6.5
v_node_x = np.linspace(0.8, 8.5, n_versions)

for i, x in enumerate(v_node_x):
    rect = FancyBboxPatch((x - 0.50, versions_y - 0.55), 1.0, 1.1,
                          boxstyle='round,pad=0.05',
                          facecolor=PAN, edgecolor=GREEN, linewidth=2)
    ax2.add_patch(rect)
    ax2.text(x, versions_y + 0.25, 'V%d' % i, ha='center', va='center',
             fontsize=10, color=GREEN, fontweight='bold')
    ax2.text(x, versions_y - 0.05, 'full', ha='center', va='center',
             fontsize=8, color=WHITE)
    ax2.text(x, versions_y - 0.30, 'state', ha='center', va='center',
             fontsize=8, color=WHITE)

    if i < n_versions - 1:
        ax2.annotate('', xy=(v_node_x[i+1] - 0.55, versions_y),
                     xytext=(x + 0.55, versions_y),
                     arrowprops=dict(arrowstyle='->', color=DIM, lw=1.2))

# Reconstruction is direct
ax2.annotate('', xy=(v_node_x[-1], versions_y - 1.1),
             xytext=(v_node_x[-1], versions_y - 0.65),
             arrowprops=dict(arrowstyle='->', color=GREEN, lw=2.0))
ax2.text(v_node_x[-1], versions_y - 1.55, 'get_at(V5)',
         ha='center', va='center', fontsize=9.5, color=GREEN, fontweight='bold')

# Single lookup
lookup_y = versions_y - 2.5
ax2.text(v_node_x[-1], lookup_y + 0.5, 'O(1) lookup',
         ha='center', va='center', fontsize=10, color=GREEN, fontweight='bold')
ax2.plot([v_node_x[-1]], [lookup_y], 'o', color=GREEN, markersize=18,
         markeredgecolor=WHITE, markeredgewidth=2)
ax2.text(v_node_x[-1], lookup_y - 0.45, 'one row',
         ha='center', va='center', fontsize=8.5, color=WHITE)

# Cost annotation
ax2.text(4.5, 2.5, 'Read cost: O(1) per query',
         ha='center', va='center', fontsize=12, color=GREEN, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.4', facecolor=BG, edgecolor=GREEN))
ax2.text(4.5, 1.7, 'Storage: larger (N x rows)',
         ha='center', va='center', fontsize=10, color=SILVER)
ax2.text(4.5, 1.0,
         'Diff between versions = compare two rows',
         ha='center', va='center', fontsize=9, color=SILVER, style='italic')

ax2.set_xlim(0, 9.2)
ax2.set_ylim(0.4, 8.0)
ax2.axis('off')

fig.suptitle('Versioning Storage Trade-off\nThe API spends storage to make point-in-time reads cheap',
             color=GOLD, fontsize=15, fontweight='bold', y=0.98)

save(fig, 'infra5_05_versioning_tradeoff.png')


# ================================================================
# FIG 6: OPTIMISTIC CONCURRENCY TIMELINE
# Type: 7 (Progression)
# Shows: two change_sets drafted against same version, one commits, the
#        other gets stale_version on submit; loud failure at submit time.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 10), facecolor=BG)
ax.set_facecolor(PAN)

# Three swim lanes: Entity (versions), Alice's change_set, Bob's change_set
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)

# Time axis at the top
ax.axhline(y=8.5, xmin=0.04, xmax=0.96, color=DIM, linewidth=0.5)
times = ['t0', 't1', 't2', 't3', 't4', 't5', 't6']
time_x = np.linspace(1.5, 14.5, len(times))
for tx, t in zip(time_x, times):
    ax.plot([tx, tx], [8.4, 8.6], color=DIM, linewidth=0.8)
    ax.text(tx, 8.85, t, ha='center', va='center', fontsize=10, color=DIM)
ax.text(0.5, 8.5, 'time', ha='right', va='center', fontsize=10, color=DIM, style='italic')

# Entity lane (top)
entity_y = 7.0
ax.text(0.5, entity_y, 'Entity\n(service X)', ha='right', va='center',
        fontsize=10, color=GOLD, fontweight='bold')

# Entity version markers
entity_versions = [
    (time_x[0], 'V42', GOLD,  'current'),
    (time_x[3], 'V43', GREEN, 'after Alice'),
]
for ex, label, color, sub in entity_versions:
    circle = Circle((ex, entity_y), 0.32, facecolor=PAN,
                    edgecolor=color, linewidth=2.5)
    ax.add_patch(circle)
    ax.text(ex, entity_y, label, ha='center', va='center',
            fontsize=9, color=color, fontweight='bold')
    ax.text(ex, entity_y - 0.55, sub, ha='center', va='center',
            fontsize=8, color=SILVER, style='italic')

# Connecting line between versions
ax.plot([time_x[0], time_x[3]], [entity_y, entity_y],
        color=DIM, linewidth=1, linestyle=':', alpha=0.5)

# Alice's lane
alice_y = 5.0
ax.text(0.5, alice_y, 'Alice\nchange_set', ha='right', va='center',
        fontsize=10, color=CYAN, fontweight='bold')

# Alice draft -> submit -> commit
alice_events = [
    (time_x[0], 'read V42', CYAN, 'draft starts'),
    (time_x[1], 'edit', CYAN, 'modify field'),
    (time_x[2], 'submit\n(against V42)', CYAN, 'API checks: V42 == current ✓'),
    (time_x[3], 'apply', GREEN, 'commits as V43'),
]
for ax_x, label, color, sub in alice_events:
    box = FancyBboxPatch((ax_x - 0.55, alice_y - 0.35), 1.10, 0.70,
                         boxstyle='round,pad=0.05',
                         facecolor=PAN, edgecolor=color, linewidth=1.5)
    ax.add_patch(box)
    ax.text(ax_x, alice_y, label, ha='center', va='center',
            fontsize=8.5, color=color, fontweight='bold')
    ax.text(ax_x, alice_y - 0.75, sub, ha='center', va='center',
            fontsize=7.5, color=SILVER, style='italic')

# Connect Alice's events
for i in range(len(alice_events) - 1):
    ax.annotate('', xy=(alice_events[i+1][0] - 0.55, alice_y),
                xytext=(alice_events[i][0] + 0.55, alice_y),
                arrowprops=dict(arrowstyle='->', color=CYAN, lw=1.2, alpha=0.8))

# Alice's apply produces V43 - dotted up to entity
ax.annotate('', xy=(time_x[3], entity_y - 0.4),
            xytext=(time_x[3], alice_y + 0.4),
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5,
                            linestyle='--', alpha=0.7))

# Bob's lane
bob_y = 3.0
ax.text(0.5, bob_y, 'Bob\nchange_set', ha='right', va='center',
        fontsize=10, color=MAG, fontweight='bold')

bob_events = [
    (time_x[0], 'read V42', MAG, 'draft starts'),
    (time_x[2], 'edit', MAG, 'modify field'),
    (time_x[5], 'submit\n(against V42)', RED, 'API checks: V42 != current'),
]
for bx, label, color, sub in bob_events:
    box = FancyBboxPatch((bx - 0.55, bob_y - 0.35), 1.10, 0.70,
                         boxstyle='round,pad=0.05',
                         facecolor=PAN, edgecolor=color, linewidth=1.5)
    ax.add_patch(box)
    ax.text(bx, bob_y, label, ha='center', va='center',
            fontsize=8.5, color=color, fontweight='bold')
    ax.text(bx, bob_y - 0.75, sub, ha='center', va='center',
            fontsize=7.5, color=SILVER, style='italic')

# Connect Bob's events
for i in range(len(bob_events) - 1):
    color_seg = MAG if i < 1 else MAG
    ax.annotate('', xy=(bob_events[i+1][0] - 0.55, bob_y),
                xytext=(bob_events[i][0] + 0.55, bob_y),
                arrowprops=dict(arrowstyle='->', color=color_seg, lw=1.2, alpha=0.8))

# Stale version error at t5 - large red marker
err_x = time_x[5]
err_y = bob_y
err_box = FancyBboxPatch((err_x + 1.0, bob_y - 0.6), 3.5, 1.2,
                        boxstyle='round,pad=0.1',
                        facecolor=PAN, edgecolor=RED, linewidth=2.5)
ax.add_patch(err_box)
ax.text(err_x + 2.75, bob_y + 0.25, 'stale_version error',
        ha='center', va='center', fontsize=11, color=RED, fontweight='bold')
ax.text(err_x + 2.75, bob_y - 0.10, 'submit rejected',
        ha='center', va='center', fontsize=9.5, color=WHITE)
ax.text(err_x + 2.75, bob_y - 0.35, '"current is V43, your draft is V42"',
        ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')

ax.annotate('', xy=(err_x + 1.0, bob_y),
            xytext=(err_x + 0.55, bob_y),
            arrowprops=dict(arrowstyle='->', color=RED, lw=2))

# Show that Bob must reconcile
recon_y = 1.3
ax.text(err_x + 2.75, recon_y + 0.3,
        'Bob retrieves V43, reconciles, resubmits',
        ha='center', va='center', fontsize=9.5, color=ORANGE, fontweight='bold')
ax.text(err_x + 2.75, recon_y - 0.05,
        '(loud failure at SUBMIT, not at apply)',
        ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')

# Big takeaway banner
ax.text(8.0, 0.4,
        'Approvers never approve a change_set based on stale state. '
        'Conflict surfaces before approval starts.',
        ha='center', va='center', fontsize=10.5, color=GOLD, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor=BG, edgecolor=GOLD))

style_axes(ax)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_title('Optimistic Concurrency at Submit Time\nTwo change_sets drafted against V42; only one can win',
             color=GOLD, fontsize=15, fontweight='bold', pad=12)

save(fig, 'infra5_06_optimistic_concurrency_timeline.png')


# ================================================================
# FIG 7: RUNNER REPORT KEY VERIFICATION
# Type: 7 (Progression) — side-by-side write attempts
# Shows: declared key passes the additional gate; undeclared key rejected
#        with audit entry. Fail-closed surface.
# ================================================================

fig, (axL, axR) = plt.subplots(1, 2, figsize=(18, 10),
                                facecolor=BG, gridspec_kw={'wspace': 0.18})

for ax in (axL, axR):
    ax.set_facecolor(PAN)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)

# --- LEFT PANEL: declared key passes ---
axL.set_title('Declared key — write PASSES',
              color=GREEN, fontsize=13, fontweight='bold', pad=10)

# Runner box at top
runner_box_L = FancyBboxPatch((1.0, 10.0), 8.0, 1.5,
                              boxstyle='round,pad=0.1',
                              facecolor=PAN, edgecolor=BLUE, linewidth=2)
axL.add_patch(runner_box_L)
axL.text(5.0, 10.95, 'prometheus_host_metrics_puller',
         ha='center', va='center', fontsize=11, color=BLUE, fontweight='bold')
axL.text(5.0, 10.50, 'submits write to observation_cache_metric',
         ha='center', va='center', fontsize=9, color=SILVER)
axL.text(5.0, 10.20, 'metric_key = "host_cpu_seconds_total", value = 12345.67',
         ha='center', va='center', fontsize=9, color=WHITE, fontfamily='monospace')

# Arrow down
axL.annotate('', xy=(5.0, 9.4), xytext=(5.0, 10.0),
             arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.8))

# Standard auth layers (compressed)
auth_box_L = FancyBboxPatch((1.0, 8.0), 8.0, 1.3,
                            boxstyle='round,pad=0.1',
                            facecolor=PAN, edgecolor=DIM, linewidth=1.5)
axL.add_patch(auth_box_L)
axL.text(5.0, 8.85, 'Standard authorization (Layers 1-5)',
         ha='center', va='center', fontsize=10, color=SILVER, fontweight='bold')
axL.text(5.0, 8.40, 'role + governance + classification + runner authority + policy',
         ha='center', va='center', fontsize=8, color=DIM, style='italic')
axL.text(5.0, 8.10, 'PASS',
         ha='center', va='center', fontsize=10, color=GREEN, fontweight='bold')

axL.annotate('', xy=(5.0, 7.4), xytext=(5.0, 8.0),
             arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.8))

# Report key check (the ADDITIONAL gate)
rk_box_L = FancyBboxPatch((0.5, 5.4), 9.0, 1.9,
                          boxstyle='round,pad=0.1',
                          facecolor=PAN, edgecolor=GOLD, linewidth=2.5)
axL.add_patch(rk_box_L)
axL.text(5.0, 7.0, 'runner_report_key check',
         ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold')
axL.text(5.0, 6.65, 'Does this runner have a declaration for this key?',
         ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# Show declared keys
declared_y = 6.10
axL.text(5.0, declared_y + 0.10, 'Declared keys (active runner_report_key rows):',
         ha='center', va='center', fontsize=8, color=WHITE)
declared_keys = ['host_cpu_seconds_total', 'host_memory_bytes_total', 'host_disk_bytes_total']
key_xs = [2.5, 5.0, 7.5]
for kx, k in zip(key_xs, declared_keys):
    is_match = (k == 'host_cpu_seconds_total')
    color = GREEN if is_match else DIM
    edge_color = GREEN if is_match else DIM
    edge_w = 2 if is_match else 1
    axL.text(kx, declared_y - 0.20, k, ha='center', va='center',
             fontsize=7.5, color=color, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.2', facecolor=PAN,
                       edgecolor=edge_color, linewidth=edge_w))

axL.text(5.0, 5.55, 'submitted key MATCHES a declaration',
         ha='center', va='center', fontsize=9, color=GREEN, fontweight='bold')

axL.annotate('', xy=(5.0, 4.9), xytext=(5.0, 5.4),
             arrowprops=dict(arrowstyle='->', color=GREEN, lw=2))

# Value validation
val_box_L = FancyBboxPatch((1.0, 3.5), 8.0, 1.3,
                           boxstyle='round,pad=0.1',
                           facecolor=PAN, edgecolor=GREEN, linewidth=1.5)
axL.add_patch(val_box_L)
axL.text(5.0, 4.40, 'Value validation against report_key_data_json',
         ha='center', va='center', fontsize=10, color=GREEN, fontweight='bold')
axL.text(5.0, 4.05, 'type=float, min=0, max=1e12 — value 12345.67 in range',
         ha='center', va='center', fontsize=8.5, color=WHITE, fontfamily='monospace')
axL.text(5.0, 3.75, 'PASS',
         ha='center', va='center', fontsize=9.5, color=GREEN, fontweight='bold')

axL.annotate('', xy=(5.0, 2.9), xytext=(5.0, 3.5),
             arrowprops=dict(arrowstyle='->', color=GREEN, lw=2))

# Outcome
out_box_L = FancyBboxPatch((1.0, 1.0), 8.0, 1.8,
                           boxstyle='round,pad=0.1',
                           facecolor=GREEN, edgecolor=GREEN, linewidth=2, alpha=0.25)
axL.add_patch(out_box_L)
axL.text(5.0, 2.30, 'WRITE COMMITTED',
         ha='center', va='center', fontsize=13, color=GREEN, fontweight='bold')
axL.text(5.0, 1.85, 'observation_cache_metric row written',
         ha='center', va='center', fontsize=9.5, color=WHITE)
axL.text(5.0, 1.45, 'audit_log_entry: action=write, key=host_cpu_seconds_total,',
         ha='center', va='center', fontsize=8.5, color=SILVER, fontfamily='monospace')
axL.text(5.0, 1.20, 'authorized_by=runner_report_key #847',
         ha='center', va='center', fontsize=8.5, color=SILVER, fontfamily='monospace')

# --- RIGHT PANEL: undeclared key rejected ---
axR.set_title('Undeclared key — write REJECTED',
              color=RED, fontsize=13, fontweight='bold', pad=10)

# Runner box at top
runner_box_R = FancyBboxPatch((1.0, 10.0), 8.0, 1.5,
                              boxstyle='round,pad=0.1',
                              facecolor=PAN, edgecolor=ORANGE, linewidth=2)
axR.add_patch(runner_box_R)
axR.text(5.0, 10.95, 'prometheus_host_metrics_puller',
         ha='center', va='center', fontsize=11, color=ORANGE, fontweight='bold')
axR.text(5.0, 10.50, 'submits write to observation_cache_metric',
         ha='center', va='center', fontsize=9, color=SILVER)
axR.text(5.0, 10.20, 'metric_key = "database_credentials_active", value = 1',
         ha='center', va='center', fontsize=9, color=ORANGE, fontfamily='monospace')

axR.annotate('', xy=(5.0, 9.4), xytext=(5.0, 10.0),
             arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.8))

# Standard auth — passes (because the runner has table-level write authority)
auth_box_R = FancyBboxPatch((1.0, 8.0), 8.0, 1.3,
                            boxstyle='round,pad=0.1',
                            facecolor=PAN, edgecolor=DIM, linewidth=1.5)
axR.add_patch(auth_box_R)
axR.text(5.0, 8.85, 'Standard authorization (Layers 1-5)',
         ha='center', va='center', fontsize=10, color=SILVER, fontweight='bold')
axR.text(5.0, 8.40, 'runner has table-level write to observation_cache_metric',
         ha='center', va='center', fontsize=8, color=DIM, style='italic')
axR.text(5.0, 8.10, 'PASS — without report key check, this would commit',
         ha='center', va='center', fontsize=9, color=ORANGE, fontweight='bold')

axR.annotate('', xy=(5.0, 7.4), xytext=(5.0, 8.0),
             arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.8))

# Report key check — FAILS
rk_box_R = FancyBboxPatch((0.5, 5.4), 9.0, 1.9,
                          boxstyle='round,pad=0.1',
                          facecolor=PAN, edgecolor=RED, linewidth=2.5)
axR.add_patch(rk_box_R)
axR.text(5.0, 7.0, 'runner_report_key check',
         ha='center', va='center', fontsize=11, color=RED, fontweight='bold')
axR.text(5.0, 6.65, 'Does this runner have a declaration for this key?',
         ha='center', va='center', fontsize=9, color=SILVER, style='italic')

declared_y_r = 6.10
axR.text(5.0, declared_y_r + 0.10, 'Declared keys (active runner_report_key rows):',
         ha='center', va='center', fontsize=8, color=WHITE)
for kx, k in zip(key_xs, declared_keys):
    axR.text(kx, declared_y_r - 0.20, k, ha='center', va='center',
             fontsize=7.5, color=DIM, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.2', facecolor=PAN,
                       edgecolor=DIM, linewidth=1))

axR.text(5.0, 5.55, '"database_credentials_active" NOT in declared set',
         ha='center', va='center', fontsize=9, color=RED, fontweight='bold')

axR.annotate('', xy=(5.0, 4.9), xytext=(5.0, 5.4),
             arrowprops=dict(arrowstyle='->', color=RED, lw=2.5))

# Failure outcome
out_box_R = FancyBboxPatch((1.0, 1.0), 8.0, 3.7,
                           boxstyle='round,pad=0.1',
                           facecolor=RED, edgecolor=RED, linewidth=2.5, alpha=0.25)
axR.add_patch(out_box_R)
axR.text(5.0, 4.20, 'WRITE REJECTED',
         ha='center', va='center', fontsize=13, color=RED, fontweight='bold')
axR.text(5.0, 3.75, 'undeclared_report_key error',
         ha='center', va='center', fontsize=9.5, color=WHITE, fontfamily='monospace')
axR.text(5.0, 3.30, 'observation_cache_metric: NO ROW WRITTEN',
         ha='center', va='center', fontsize=9, color=WHITE, fontweight='bold')
axR.text(5.0, 2.75, 'audit_log_entry: action=write_rejected,',
         ha='center', va='center', fontsize=8.5, color=SILVER, fontfamily='monospace')
axR.text(5.0, 2.45, 'submitted_key=database_credentials_active,',
         ha='center', va='center', fontsize=8.5, color=SILVER, fontfamily='monospace')
axR.text(5.0, 2.15, 'reason=undeclared_report_key,',
         ha='center', va='center', fontsize=8.5, color=SILVER, fontfamily='monospace')
axR.text(5.0, 1.85, 'runner=prometheus_host_metrics_puller',
         ha='center', va='center', fontsize=8.5, color=SILVER, fontfamily='monospace')
axR.text(5.0, 1.30, 'fail closed — operator queries rejection, files finding',
         ha='center', va='center', fontsize=8.5, color=ORANGE, style='italic')

for ax in (axL, axR):
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.suptitle('Runner Report Key Verification — the additional gate on the writable surface\n'
             'Same standard authorization, different declared keys, different outcomes',
             color=GOLD, fontsize=15, fontweight='bold', y=0.98)

save(fig, 'infra5_07_runner_report_key_verification.png')


# ================================================================
# FIG 8: AUDIT LOG CRYPTOGRAPHIC CHAIN
# Type: 4 (Geometric)
# Shows: sequential audit entries linked via hash; tampering of one entry
#        breaks the chain at that point and propagates forward.
# ================================================================

fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(18, 11),
                                      facecolor=BG, gridspec_kw={'hspace': 0.35})

for ax in (ax_top, ax_bot):
    ax.set_facecolor(PAN)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 5)

# --- TOP PANEL: intact chain ---
ax_top.set_title('Intact chain — every entry verifies',
                 color=GREEN, fontsize=13, fontweight='bold', pad=10)

n_entries = 6
entry_w = 2.4
entry_h = 2.6
entry_gap = 0.30
x_start = 0.5

entries_top = []
for i in range(n_entries):
    x = x_start + i * (entry_w + entry_gap)
    entries_top.append(x)

    # Entry box
    box = FancyBboxPatch((x, 1.2), entry_w, entry_h,
                         boxstyle='round,pad=0.05',
                         facecolor=PAN, edgecolor=GREEN, linewidth=2)
    ax_top.add_patch(box)

    # Entry header
    ax_top.text(x + entry_w/2, 3.45, 'entry #%d' % (i + 100),
                ha='center', va='center', fontsize=10, color=GREEN, fontweight='bold')

    # Entry contents
    ax_top.text(x + entry_w/2, 3.05, 'caller, action,',
                ha='center', va='center', fontsize=7.5, color=WHITE)
    ax_top.text(x + entry_w/2, 2.80, 'target, time',
                ha='center', va='center', fontsize=7.5, color=WHITE)

    # Hash field
    ax_top.text(x + entry_w/2, 2.30, '_audit_chain_hash:',
                ha='center', va='center', fontsize=7, color=SILVER, style='italic')

    # Synthetic hash values
    hash_val = 'h%d=H(prev||entry)' % i if i > 0 else 'h0=H(genesis||entry)'
    ax_top.text(x + entry_w/2, 1.95, hash_val,
                ha='center', va='center', fontsize=7, color=GOLD, fontfamily='monospace')

    short_hash = ['9f3a..', '4b1c..', '7e29..', '2d8b..', '6a5f..', 'c041..'][i]
    ax_top.text(x + entry_w/2, 1.55, short_hash,
                ha='center', va='center', fontsize=8, color=GOLD,
                fontfamily='monospace', fontweight='bold')

# Chain links between entries
for i in range(n_entries - 1):
    x1 = entries_top[i] + entry_w
    x2 = entries_top[i + 1]
    y_mid = 1.95
    ax_top.annotate('', xy=(x2 - 0.05, y_mid), xytext=(x1 + 0.05, y_mid),
                    arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.8))
    # Mid-arrow label
    mid_x = (x1 + x2) / 2
    ax_top.text(mid_x, y_mid + 0.30, 'links', ha='center', va='center',
                fontsize=7, color=GREEN, style='italic')

# Verification sweep at bottom
verify_y = 0.5
ax_top.text(0.5, verify_y, 'verifier:', ha='left', va='center',
            fontsize=9, color=GOLD, fontweight='bold')
for i, x in enumerate(entries_top):
    ax_top.text(x + entry_w/2, verify_y, 'recompute h%d ✓' % i,
                ha='center', va='center', fontsize=8, color=GREEN)

# --- BOTTOM PANEL: tampered chain ---
ax_bot.set_title('Tampered entry — break detected and propagates forward',
                 color=RED, fontsize=13, fontweight='bold', pad=10)

# Same layout, but entry #102 is tampered
tampered_idx = 2
entries_bot = []
for i in range(n_entries):
    x = x_start + i * (entry_w + entry_gap)
    entries_bot.append(x)

    if i < tampered_idx:
        color = GREEN
        status = '✓'
    elif i == tampered_idx:
        color = RED
        status = 'TAMPERED'
    else:
        color = ORANGE
        status = 'BROKEN'

    edge_w = 2.5 if i >= tampered_idx else 2

    box = FancyBboxPatch((x, 1.2), entry_w, entry_h,
                         boxstyle='round,pad=0.05',
                         facecolor=PAN, edgecolor=color, linewidth=edge_w)
    ax_bot.add_patch(box)

    ax_bot.text(x + entry_w/2, 3.45, 'entry #%d' % (i + 100),
                ha='center', va='center', fontsize=10, color=color, fontweight='bold')

    if i == tampered_idx:
        ax_bot.text(x + entry_w/2, 3.05, 'caller, action,',
                    ha='center', va='center', fontsize=7.5, color=RED,
                    style='italic')
        ax_bot.text(x + entry_w/2, 2.80, 'target, time (modified)',
                    ha='center', va='center', fontsize=7.5, color=RED,
                    style='italic')
    else:
        ax_bot.text(x + entry_w/2, 3.05, 'caller, action,',
                    ha='center', va='center', fontsize=7.5, color=WHITE)
        ax_bot.text(x + entry_w/2, 2.80, 'target, time',
                    ha='center', va='center', fontsize=7.5, color=WHITE)

    ax_bot.text(x + entry_w/2, 2.30, '_audit_chain_hash:',
                ha='center', va='center', fontsize=7, color=SILVER, style='italic')

    if i < tampered_idx:
        hashes = ['9f3a..', '4b1c..']
        ax_bot.text(x + entry_w/2, 1.55, hashes[i],
                    ha='center', va='center', fontsize=8, color=GOLD,
                    fontfamily='monospace', fontweight='bold')
        ax_bot.text(x + entry_w/2, 1.95, 'h%d (matches)' % i,
                    ha='center', va='center', fontsize=7, color=GOLD,
                    fontfamily='monospace')
    elif i == tampered_idx:
        ax_bot.text(x + entry_w/2, 1.95, 'stored: 7e29..',
                    ha='center', va='center', fontsize=7.5, color=ORANGE,
                    fontfamily='monospace')
        ax_bot.text(x + entry_w/2, 1.55, 'recomputed: a4f1..',
                    ha='center', va='center', fontsize=8, color=RED,
                    fontfamily='monospace', fontweight='bold')
    else:
        ax_bot.text(x + entry_w/2, 1.95, 'h%d (cascading)' % i,
                    ha='center', va='center', fontsize=7, color=ORANGE,
                    fontfamily='monospace')
        ax_bot.text(x + entry_w/2, 1.55, '?',
                    ha='center', va='center', fontsize=10, color=ORANGE,
                    fontweight='bold')

# Chain arrows
for i in range(n_entries - 1):
    x1 = entries_bot[i] + entry_w
    x2 = entries_bot[i + 1]
    y_mid = 1.95
    if i < tampered_idx - 1:
        ax_bot.annotate('', xy=(x2 - 0.05, y_mid), xytext=(x1 + 0.05, y_mid),
                        arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.8))
    else:
        ax_bot.annotate('', xy=(x2 - 0.05, y_mid), xytext=(x1 + 0.05, y_mid),
                        arrowprops=dict(arrowstyle='->', color=RED, lw=2.0,
                                        linestyle='--'))

# Tampering indicator on entry #102
tx = entries_bot[tampered_idx] + entry_w/2
ax_bot.annotate('', xy=(tx, 3.95), xytext=(tx, 4.6),
                arrowprops=dict(arrowstyle='->', color=RED, lw=2))
ax_bot.text(tx, 4.75, 'TAMPER',
            ha='center', va='center', fontsize=10, color=RED, fontweight='bold')

# Verification sweep at bottom
verify_y_b = 0.5
ax_bot.text(0.5, verify_y_b, 'verifier:', ha='left', va='center',
            fontsize=9, color=GOLD, fontweight='bold')
for i, x in enumerate(entries_bot):
    if i < tampered_idx:
        ax_bot.text(x + entry_w/2, verify_y_b, 'recompute h%d ✓' % i,
                    ha='center', va='center', fontsize=8, color=GREEN)
    elif i == tampered_idx:
        ax_bot.text(x + entry_w/2, verify_y_b, 'h%d MISMATCH' % i,
                    ha='center', va='center', fontsize=8.5, color=RED,
                    fontweight='bold')
    else:
        ax_bot.text(x + entry_w/2, verify_y_b, 'h%d cascade fail' % i,
                    ha='center', va='center', fontsize=8, color=ORANGE)

for ax in (ax_top, ax_bot):
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.suptitle('Audit Log Cryptographic Chaining (optional, tamper-evidence regimes)\n'
             'Each entry hashes prev || entry; modification breaks chain at the point and forward',
             color=GOLD, fontsize=15, fontweight='bold', y=0.98)

save(fig, 'infra5_08_audit_chain_tamper_detection.png')


# ================================================================
# SUMMARY
# ================================================================

print("\n" + "=" * 60)
print("OPSDB-6 diagram script complete")
print("=" * 60)
print("Files written to: %s" % outdir)
print()
print("  infra5_01_ten_step_gate_rings.png")
print("  infra5_02_five_layer_authorization.png")
print("  infra5_03_stakeholder_routing_fanout.png")
print("  infra5_04_change_set_lifecycle.png")
print("  infra5_05_versioning_tradeoff.png")
print("  infra5_06_optimistic_concurrency_timeline.png")
print("  infra5_07_runner_report_key_verification.png")
print("  infra5_08_audit_chain_tamper_detection.png")
