#!/usr/bin/env python3
"""
HOWL OPSDB-4 Diagrams — An Example OpsDB Schema
8 figures covering top-level taxonomy, substrate nesting, change-set lifecycle,
DSNC namespace scaling, service connection graph, versioning siblings,
polymorphic bridges, and the audit/evidence/version stream distinction.
Output: PNG files to ../figures/
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Wedge
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


def style_axis(ax):
    ax.set_facecolor(PAN)
    for spine in ax.spines.values():
        spine.set_color(DIM)
        spine.set_linewidth(0.5)
    ax.tick_params(colors=DIM, labelsize=9)


def hide_axis(ax):
    ax.set_facecolor(PAN)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def save(fig, filename):
    path = os.path.join(outdir, filename)
    fig.savefig(path, dpi=180, facecolor=BG, bbox_inches='tight', pad_inches=0.3)
    plt.close(fig)
    print("  Saved: %s" % filename)


def draw_box(ax, x, y, w, h, text, fill=PAN, edge=GOLD, text_color=WHITE,
             fontsize=10, fontweight='normal', alpha=1.0, zorder=2):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.02",
                         facecolor=fill, edgecolor=edge,
                         linewidth=1.5, alpha=alpha, zorder=zorder)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text,
            ha='center', va='center',
            color=text_color, fontsize=fontsize,
            fontweight=fontweight, zorder=zorder+1)


def draw_arrow(ax, x1, y1, x2, y2, color=SILVER, lw=1.5, style='->', alpha=0.8):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle=style,
                            color=color, linewidth=lw,
                            alpha=alpha,
                            mutation_scale=15)
    ax.add_patch(arrow)


# ================================================================
# FIG 1: TOP-LEVEL TAXONOMY RADIAL MAP
# Type: 4 (Geometric Cross-Section)
# Shows: The 18 cuts as a comprehensive carving around the substrate
# ================================================================

print("Fig 1: Top-level taxonomy radial map")

fig, ax = plt.subplots(figsize=(16, 16))
hide_axis(ax)
ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)
ax.set_aspect('equal')

# Central OpsDB node
center = Circle((0, 0), 1.6, facecolor=GOLD, edgecolor=WHITE,
                linewidth=2.5, alpha=0.85, zorder=10)
ax.add_patch(center)
ax.text(0, 0.18, 'OpsDB', ha='center', va='center',
        color=BG, fontsize=15, fontweight='bold', zorder=11)
ax.text(0, -0.45, 'Schema', ha='center', va='center',
        color=BG, fontsize=10, fontweight='bold', zorder=11)

# Inner ring: API gate
api_ring = Circle((0, 0), 2.6, facecolor='none', edgecolor=ORANGE,
                  linewidth=1.5, linestyle='--', alpha=0.7, zorder=5)
ax.add_patch(api_ring)
ax.text(0, 2.35, 'API gate', ha='center', va='center',
        color=ORANGE, fontsize=9, alpha=0.8, zorder=6)

# 18 cuts grouped into 5 bands by color
cuts = [
    # Substrate band (BLUE)
    ('Site & Location',     BLUE),
    ('Identity',            BLUE),
    ('Substrate',           BLUE),
    ('Service Abstraction', BLUE),
    ('Kubernetes',          BLUE),
    ('Cloud Resources',     BLUE),
    # Directory & schedules (CYAN)
    ('Authority Directory', CYAN),
    ('Schedules',           CYAN),
    # Governance (MAG)
    ('Policy',              MAG),
    ('Documentation Meta',  MAG),
    # Operational (GREEN)
    ('Runners',             GREEN),
    ('Monitoring',          GREEN),
    ('Cached Observation',  GREEN),
    ('Config Variables',    GREEN),
    # Audit & integrity (PURPLE)
    ('Change Management',   PURPLE),
    ('Audit & Evidence',    PURPLE),
    ('Schema Metadata',     PURPLE),
    # And one more for spacing - Boundaries note
    ('What is NOT here',    DIM),
]

n = len(cuts)
radius_inner = 4.5
radius_outer = 7.2

for i, (label, color) in enumerate(cuts):
    angle = (i / n) * 2 * np.pi - np.pi / 2
    x_mid = (radius_inner + radius_outer) / 2 * np.cos(angle)
    y_mid = (radius_inner + radius_outer) / 2 * np.sin(angle)

    # Wedge for each cut
    angle_deg_start = np.degrees(angle) - (180.0 / n)
    angle_deg_end   = np.degrees(angle) + (180.0 / n)
    wedge = Wedge((0, 0), radius_outer, angle_deg_start, angle_deg_end,
                  width=radius_outer - radius_inner,
                  facecolor=color, edgecolor=BG,
                  linewidth=2, alpha=0.18, zorder=2)
    ax.add_patch(wedge)

    # Label oriented along radius
    angle_deg = np.degrees(angle)
    rotation = angle_deg
    if angle_deg > 90 and angle_deg < 270:
        rotation = angle_deg + 180
    ax.text(x_mid, y_mid, label,
            ha='center', va='center',
            color=color if color != DIM else SILVER,
            fontsize=10, fontweight='bold',
            rotation=rotation, zorder=4)

# Outer ring: comprehensive scope label
outer_ring = Circle((0, 0), 7.2, facecolor='none', edgecolor=DIM,
                    linewidth=0.8, alpha=0.6, zorder=1)
ax.add_patch(outer_ring)

# Band legend lower-left, inside the figure
legend_x = -11.2
legend_y_start = -8.8
band_legend = [
    ('Substrate',           BLUE),
    ('Directory & schedules', CYAN),
    ('Governance',          MAG),
    ('Operational',         GREEN),
    ('Audit & integrity',   PURPLE),
    ('Boundary',            DIM),
]
for i, (name, color) in enumerate(band_legend):
    swatch = Rectangle((legend_x, legend_y_start - i * 0.55),
                       0.5, 0.3,
                       facecolor=color, edgecolor=color,
                       alpha=0.5, linewidth=0)
    ax.add_patch(swatch)
    ax.text(legend_x + 0.7, legend_y_start - i * 0.55 + 0.15,
            name, ha='left', va='center',
            color=SILVER, fontsize=10)

# Title
ax.text(0, 10.5, 'OpsDB Schema — Top-Level Taxonomy',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(0, 9.6, 'Eighteen comprehensive cuts arranged around the substrate',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# Note at bottom
ax.text(0, -10.5,
        'The schema is one whole sliced into named segments.  '
        'Each cut owns its prefix namespace per DSNC.',
        ha='center', va='center',
        color=DIM, fontsize=9, style='italic')

save(fig, 'infra3_01_top_level_taxonomy.png')


# ================================================================
# FIG 2: SUBSTRATE NESTING HIERARCHY FROM RACK TO POD
# Type: 4 (Geometric Cross-Section)
# Shows: One self-FK chain unifies bare-metal and cloud substrate paths
# ================================================================

print("Fig 2: Substrate nesting hierarchy")

fig, ax = plt.subplots(figsize=(18, 13))
hide_axis(ax)
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)

# Title
ax.text(10, 13.2, 'Unified Substrate Hierarchy — Rack to Pod',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(10, 12.5,
        'Both bare-metal and cloud paths thread through megavisor_instance.parent_megavisor_instance_id',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# Two columns: bare metal (left) and cloud (right)
col_left = 5.0
col_right = 15.0
box_w = 4.4
box_h = 0.85
gap = 1.10

# Bare-metal column from bottom up
bm_levels = [
    ('location\n"Rack 14, DC-East"',                     BLUE),
    ('hardware_set_instance\nDell R750 #007',            BLUE),
    ('megavisor_instance\nmegavisor_type=bare_metal',    CYAN),
    ('megavisor_instance\nmegavisor_type=kvm  (host)',   CYAN),
    ('megavisor_instance\nmegavisor_type=kvm  (guest)',  CYAN),
    ('megavisor_instance\nmegavisor_type=kubelet',       CYAN),
    ('k8s_pod\nname="user-api-7d4b"',                    GOLD),
]

# Cloud column from bottom up
cl_levels = [
    ('location\n"us-east-1a"',                           BLUE),
    ('cloud_resource\ntype=ec2_instance',                MAG),
    ('megavisor_instance\nmegavisor_type=ec2',           CYAN),
    ('megavisor_instance\nmegavisor_type=kubelet',       CYAN),
    ('k8s_pod\nname="user-api-9c2f"',                    GOLD),
]

# Equalize heights by anchoring tops
y_bottom = 1.1
n_bm = len(bm_levels)
n_cl = len(cl_levels)

# Compute y positions
bm_y = [y_bottom + i * gap for i in range(n_bm)]
# Cloud top should match bare-metal top
cl_top = bm_y[-1]
cl_gap = (cl_top - y_bottom) / (n_cl - 1)
cl_y = [y_bottom + i * cl_gap for i in range(n_cl)]

# Draw bare-metal column
for i, (label, color) in enumerate(bm_levels):
    draw_box(ax, col_left - box_w/2, bm_y[i], box_w, box_h,
             label, fill=PAN, edge=color, text_color=WHITE,
             fontsize=9, fontweight='bold')
    if i < n_bm - 1:
        draw_arrow(ax, col_left, bm_y[i] + box_h,
                   col_left, bm_y[i+1],
                   color=color, lw=1.5)

# Draw cloud column
for i, (label, color) in enumerate(cl_levels):
    draw_box(ax, col_right - box_w/2, cl_y[i], box_w, box_h,
             label, fill=PAN, edge=color, text_color=WHITE,
             fontsize=9, fontweight='bold')
    if i < n_cl - 1:
        draw_arrow(ax, col_right, cl_y[i] + box_h,
                   col_right, cl_y[i+1],
                   color=color, lw=1.5)

# Column headers
ax.text(col_left, bm_y[-1] + box_h + 0.6,
        'BARE-METAL PATH',
        ha='center', va='center',
        color=BLUE, fontsize=12, fontweight='bold')
ax.text(col_right, cl_y[-1] + box_h + 0.6,
        'CLOUD PATH',
        ha='center', va='center',
        color=MAG, fontsize=12, fontweight='bold')

# Annotation arrows for "parent_megavisor_instance_id"
ax.annotate('parent_megavisor_instance_id\nself-FK chain',
            xy=(col_left + box_w/2 + 0.1, bm_y[3] + box_h/2),
            xytext=(col_left + box_w/2 + 2.2, bm_y[3] + box_h/2),
            color=GOLD, fontsize=9, fontweight='bold',
            ha='left', va='center',
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.4))

ax.annotate('parent_megavisor_instance_id\nself-FK chain',
            xy=(col_right - box_w/2 - 0.1, cl_y[2] + box_h/2),
            xytext=(col_right - box_w/2 - 2.2, cl_y[2] + box_h/2),
            color=GOLD, fontsize=9, fontweight='bold',
            ha='right', va='center',
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.4))

# Bottom note: scale annotations
ax.text(col_left, 0.5,
        'physical scale: ~10^0 m chassis  /  ~10^1 m rack',
        ha='center', va='center',
        color=DIM, fontsize=9, style='italic')
ax.text(col_right, 0.5,
        'cloud scale: ~10^7 m region  /  ~10^4 m zone',
        ha='center', va='center',
        color=DIM, fontsize=9, style='italic')

# Center insight
ax.text(10, 7.0,
        'ONE\nself-join\nchain',
        ha='center', va='center',
        color=GOLD, fontsize=14, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.6',
                  facecolor=BG, edgecolor=GOLD, linewidth=1.5))

save(fig, 'infra3_02_substrate_nesting.png')


# ================================================================
# FIG 3: DSNC NAMESPACE TREE AT SCALE
# Type: 4 (Geometric Cross-Section)
# Shows: Prefix discipline distributes ~150 entity types across non-colliding namespaces
# ================================================================

print("Fig 3: DSNC namespace tree")

fig, ax = plt.subplots(figsize=(18, 11))
hide_axis(ax)
ax.set_xlim(0, 20)
ax.set_ylim(0, 12)

ax.text(10, 11.3, 'DSNC Namespace Tree at Scale',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(10, 10.6,
        'Prefix discipline distributes ~150 entity types across non-colliding namespaces',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# Root
root_x, root_y = 10, 9.4
ax.add_patch(FancyBboxPatch((root_x - 1.2, root_y - 0.35), 2.4, 0.7,
                            boxstyle='round,pad=0.05',
                            facecolor=GOLD, edgecolor=WHITE,
                            linewidth=2, alpha=0.85))
ax.text(root_x, root_y, 'OpsDB schema',
        ha='center', va='center',
        color=BG, fontsize=11, fontweight='bold')

# Top-level namespaces with their leaf counts
namespaces = [
    ('hardware_*',      6, BLUE,   'hardware_component, hardware_port,\nhardware_set, hardware_set_*'),
    ('megavisor_*',     2, CYAN,   'megavisor, megavisor_instance'),
    ('cloud_*',         3, MAG,    'cloud_provider, cloud_account, cloud_resource'),
    ('k8s_*',          11, BLUE,   'k8s_cluster, k8s_namespace, k8s_workload,\nk8s_pod, k8s_helm_release, ...'),
    ('service_*',      11, GREEN,  'service, service_version, service_package,\nservice_connection, service_*_target, ...'),
    ('ops_*',           5, CYAN,   'ops_user, ops_group, ops_user_role, ...'),
    ('host_group_*',    3, GREEN,  'host_group, host_group_machine,\nhost_group_package'),
    ('runner_*',       10, ORANGE, 'runner_spec, runner_capability,\nrunner_machine, runner_*_target, runner_job, ...'),
    ('schedule_*',      6, ORANGE, 'schedule, runner_schedule,\ncredential_rotation_schedule, ...'),
    ('policy_*',        4, MAG,    'policy, security_zone, retention_policy,\napproval_rule'),
    ('change_set_*',    8, PURPLE, 'change_set, change_set_field_change,\nchange_set_approval, ...'),
    ('evidence_*',      8, PURPLE, 'evidence_record, evidence_record_*_target'),
    ('audit_*',         1, PURPLE, 'audit_log_entry'),
    ('observation_*',   3, GREEN,  'observation_cache_metric,\nobservation_cache_state, ...'),
    ('configuration_*', 2, GREEN,  'configuration_variable,\nconfiguration_variable_version'),
    ('authority_*',     2, CYAN,   'authority, authority_pointer'),
    ('compliance_*',    4, MAG,    'compliance_regime, compliance_finding, ...'),
    ('_schema_*',       5, GOLD,   '_schema_version, _schema_entity_type,\n_schema_field, _schema_relationship'),
]

# Distribute around root in two arcs (upper and lower)
n = len(namespaces)
y_levels_upper = [7.4, 5.6, 3.8]
x_positions_upper = np.linspace(1.8, 18.2, 6)

# Place namespaces in a 3-row grid below root
positions = []
cols = 6
rows = 3
for i in range(n):
    row = i // cols
    col = i % cols
    x = 1.6 + col * (16.8 / (cols - 1))
    y = 7.6 - row * 2.5
    positions.append((x, y))

box_ns_w = 2.6
box_ns_h = 0.65

for i, ((label, count, color, examples), (x, y)) in enumerate(zip(namespaces, positions)):
    # Connection from root
    ax.plot([root_x, x], [root_y - 0.35, y + box_ns_h/2],
            color=DIM, linewidth=0.5, alpha=0.4, zorder=1)

    # Namespace box
    ax.add_patch(FancyBboxPatch((x - box_ns_w/2, y - box_ns_h/2),
                                box_ns_w, box_ns_h,
                                boxstyle='round,pad=0.04',
                                facecolor=PAN, edgecolor=color,
                                linewidth=1.8, zorder=3))
    ax.text(x, y + 0.05, label,
            ha='center', va='center',
            color=color, fontsize=10, fontweight='bold', zorder=4)
    ax.text(x, y - 0.18, '%d entity types' % count,
            ha='center', va='center',
            color=SILVER, fontsize=8, zorder=4)

# Bottom annotation: the discipline insight
ax.add_patch(FancyBboxPatch((1.5, 0.3), 17, 1.5,
                            boxstyle='round,pad=0.1',
                            facecolor=BG, edgecolor=GOLD,
                            linewidth=1.2, alpha=0.85))
ax.text(10, 1.4,
        'No prefix collides.  Each prefix owns a hierarchical namespace.',
        ha='center', va='center',
        color=GOLD, fontsize=11, fontweight='bold')
ax.text(10, 0.75,
        'Adding a new domain creates a new prefix tree, never a renaming or collision.  '
        'The convention is structural, not memorized.',
        ha='center', va='center',
        color=SILVER, fontsize=9, style='italic')

save(fig, 'infra3_03_dsnc_namespace_tree.png')


# ================================================================
# FIG 4: SERVICE CONNECTION GRAPH AS MULTI-USE DATA
# Type: 5 (Connection Map)
# Shows: One graph drives templating, alerting, and capacity planning
# ================================================================

print("Fig 4: Service connection graph as multi-use data")

fig, ax = plt.subplots(figsize=(18, 11))
hide_axis(ax)
ax.set_xlim(0, 20)
ax.set_ylim(0, 12)

ax.text(10, 11.3, 'Service Connection Graph — One Structure, Many Uses',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(10, 10.6,
        'service_connection edges drive config templating, alert suppression, capacity planning',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# Three services laid out as a triangle
svc_a = (5,  6.8)
svc_b = (15, 6.8)
svc_c = (10, 3.5)

svc_w, svc_h = 3.0, 1.3

services = [
    (svc_a, 'user-api',           BLUE,
     ['http     :443',  'metrics  :9090']),
    (svc_b, 'billing-database',   GREEN,
     ['pg-wire  :5432', 'metrics  :9090']),
    (svc_c, 'audit-collector',    PURPLE,
     ['syslog   :514',  'metrics  :9090']),
]

for (x, y), name, color, ports in services:
    # Service box
    ax.add_patch(FancyBboxPatch((x - svc_w/2, y - svc_h/2),
                                svc_w, svc_h,
                                boxstyle='round,pad=0.05',
                                facecolor=PAN, edgecolor=color,
                                linewidth=2, zorder=4))
    ax.text(x, y + 0.42, name,
            ha='center', va='center',
            color=color, fontsize=11, fontweight='bold', zorder=5)
    for j, port in enumerate(ports):
        ax.text(x, y + 0.05 - j * 0.25, port,
                ha='center', va='center',
                color=WHITE, fontsize=8.5,
                family='monospace', zorder=5)

# Connections between services
def edge(p1, p2, label, color=CYAN, offset=(0, 0)):
    draw_arrow(ax, p1[0], p1[1], p2[0], p2[1],
               color=color, lw=1.8, alpha=0.85)
    mx = (p1[0] + p2[0]) / 2 + offset[0]
    my = (p1[1] + p2[1]) / 2 + offset[1]
    ax.text(mx, my, label,
            ha='center', va='center',
            color=color, fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25',
                      facecolor=BG, edgecolor=color, linewidth=0.8),
            zorder=6)

# user-api -> billing-database (data dependency)
edge((svc_a[0] + svc_w/2, svc_a[1]),
     (svc_b[0] - svc_w/2, svc_b[1]),
     'pg-wire',
     color=GREEN)

# user-api -> audit-collector (logs)
edge((svc_a[0] + svc_w/4, svc_a[1] - svc_h/2),
     (svc_c[0] - svc_w/2, svc_c[1] + svc_h/2),
     'syslog',
     color=PURPLE)

# billing-database -> audit-collector (logs)
edge((svc_b[0] - svc_w/4, svc_b[1] - svc_h/2),
     (svc_c[0] + svc_w/2, svc_c[1] + svc_h/2),
     'syslog',
     color=PURPLE)

# Three usage labels around the triangle
usages = [
    (1.5, 8.8, 'CONFIG TEMPLATING\n\nresolves endpoint addresses\nfor each service\'s rendered config',
     CYAN),
    (18.5, 8.8, 'ALERT SUPPRESSION\n\nif billing-database fires,\nuser-api dependent alerts suppress',
     ORANGE),
    (10, 1.3, 'CAPACITY PLANNING\n\ndependency fan-in / fan-out drives\nscaling and bulkhead decisions',
     GOLD),
]

for x, y, text, color in usages:
    ax.add_patch(FancyBboxPatch((x - 2.6, y - 0.85), 5.2, 1.7,
                                boxstyle='round,pad=0.1',
                                facecolor=BG, edgecolor=color,
                                linewidth=1.5, alpha=0.95))
    ax.text(x, y, text,
            ha='center', va='center',
            color=color, fontsize=9.5,
            fontweight='bold')

# Center caption
ax.text(10, 5.2,
        'one graph,\nmany uses',
        ha='center', va='center',
        color=GOLD, fontsize=12, fontweight='bold', style='italic',
        alpha=0.8)

save(fig, 'infra3_04_service_connection_graph.png')


# ================================================================
# FIG 5: POLYMORPHIC TARGETING VIA BRIDGE TABLES
# Type: 5 (Connection Map)
# Shows: Bridges preserve FK integrity where polymorphic FKs would break it
# ================================================================

print("Fig 5: Polymorphic targeting via bridge tables")

fig, ax = plt.subplots(figsize=(18, 11))
hide_axis(ax)
ax.set_xlim(0, 20)
ax.set_ylim(0, 12)

ax.text(10, 11.3, 'Polymorphic Targeting via Bridge Tables',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(10, 10.6,
        'One change_set targets many entity types — each through a typed bridge with clean FK integrity',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# Center: change_set
cs_x, cs_y = 10, 7.5
ax.add_patch(FancyBboxPatch((cs_x - 1.6, cs_y - 0.5), 3.2, 1.0,
                            boxstyle='round,pad=0.08',
                            facecolor=GOLD, edgecolor=WHITE,
                            linewidth=2, alpha=0.85))
ax.text(cs_x, cs_y, 'change_set',
        ha='center', va='center',
        color=BG, fontsize=12, fontweight='bold')

# Bridge tables (middle row)
bridges = [
    (3,  4.5, 'change_set_\nservice_target',         BLUE),
    (7,  4.5, 'change_set_\nmachine_target',         CYAN),
    (10, 4.5, 'change_set_\nk8s_workload_target',    GREEN),
    (13, 4.5, 'change_set_\ncloud_resource_target',  MAG),
    (17, 4.5, 'change_set_\npolicy_target',          PURPLE),
]

# Target entity tables (bottom row)
targets = [
    (3,  1.5, 'service',         BLUE),
    (7,  1.5, 'machine',         CYAN),
    (10, 1.5, 'k8s_workload',    GREEN),
    (13, 1.5, 'cloud_resource',  MAG),
    (17, 1.5, 'policy',          PURPLE),
]

bridge_w, bridge_h = 2.4, 1.0
target_w, target_h = 2.0, 0.8

# Draw bridges and targets and connections
for (bx, by, blabel, color), (tx, ty, tlabel, tcolor) in zip(bridges, targets):
    # Bridge box
    ax.add_patch(FancyBboxPatch((bx - bridge_w/2, by - bridge_h/2),
                                bridge_w, bridge_h,
                                boxstyle='round,pad=0.05',
                                facecolor=PAN, edgecolor=color,
                                linewidth=1.5))
    ax.text(bx, by, blabel,
            ha='center', va='center',
            color=color, fontsize=8.5, fontweight='bold')

    # Target box
    ax.add_patch(FancyBboxPatch((tx - target_w/2, ty - target_h/2),
                                target_w, target_h,
                                boxstyle='round,pad=0.05',
                                facecolor=BG, edgecolor=tcolor,
                                linewidth=1.5))
    ax.text(tx, ty, tlabel,
            ha='center', va='center',
            color=tcolor, fontsize=10, fontweight='bold',
            family='monospace')

    # change_set -> bridge arrow
    draw_arrow(ax, cs_x + (bx - cs_x) * 0.18, cs_y - 0.5,
               bx, by + bridge_h/2,
               color=color, lw=1.3, alpha=0.7)

    # bridge -> target arrow (FK)
    draw_arrow(ax, bx, by - bridge_h/2,
               tx, ty + target_h/2,
               color=color, lw=1.5, alpha=0.9)

    # FK label on bridge-target arrow
    ax.text(bx + 0.55, (by + ty) / 2 - 0.2, 'FK',
            ha='left', va='center',
            color=color, fontsize=7.5, alpha=0.8,
            style='italic')

# Annotation: clean FK integrity
ax.add_patch(FancyBboxPatch((0.5, 8.5), 5.5, 1.7,
                            boxstyle='round,pad=0.1',
                            facecolor=BG, edgecolor=GREEN,
                            linewidth=1.5, alpha=0.9))
ax.text(3.25, 9.6, 'WHAT THIS GIVES',
        ha='center', va='center',
        color=GREEN, fontsize=10, fontweight='bold')
ax.text(3.25, 9.0,
        'every FK targets a real table\nintegrity enforced by the engine\nper-bridge columns possible',
        ha='center', va='center',
        color=WHITE, fontsize=8.5)

ax.add_patch(FancyBboxPatch((14, 8.5), 5.5, 1.7,
                            boxstyle='round,pad=0.1',
                            facecolor=BG, edgecolor=RED,
                            linewidth=1.5, alpha=0.9))
ax.text(16.75, 9.6, 'WHAT POLYMORPHIC FKS LOSE',
        ha='center', va='center',
        color=RED, fontsize=10, fontweight='bold')
ax.text(16.75, 9.0,
        'target_id integrity not enforceable\norphans accumulate silently\ntype field can drift from id',
        ha='center', va='center',
        color=WHITE, fontsize=8.5)

# Bottom note
ax.text(10, 0.4,
        'Same pattern applies to schedule_target, evidence_record_target, runner_target, '
        'monitor_target, policy_target, ownership, stakeholder.',
        ha='center', va='center',
        color=DIM, fontsize=9, style='italic')

save(fig, 'infra3_05_polymorphic_bridge_tables.png')


# ================================================================
# FIG 6: CHANGE SET LIFECYCLE STATE MACHINE
# Type: 7 (Progression/Sequence Diagram)
# Shows: States, transitions, and bridge tables consulted at each
# ================================================================

print("Fig 6: Change set lifecycle state machine")

fig, ax = plt.subplots(figsize=(18, 11))
hide_axis(ax)
ax.set_xlim(0, 20)
ax.set_ylim(0, 12)

ax.text(10, 11.3, 'Change Set Lifecycle — State Machine in Data',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(10, 10.6,
        'change_set.change_set_status walks through these states; each transition consults bridge tables',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# Main path states (left to right along middle)
main_path = [
    (1.8,  6.8, 'draft',           DIM),
    (4.2,  6.8, 'submitted',       BLUE),
    (6.8,  6.8, 'validating',      CYAN),
    (9.4,  6.8, 'pending_\napproval', ORANGE),
    (12.2, 6.8, 'approved',        GREEN),
    (14.8, 6.8, 'applied',         GOLD),
    (17.6, 6.8, 'rolled_back',     PURPLE),
]

state_w, state_h = 1.7, 0.95

for x, y, label, color in main_path:
    ax.add_patch(FancyBboxPatch((x - state_w/2, y - state_h/2),
                                state_w, state_h,
                                boxstyle='round,pad=0.05',
                                facecolor=PAN, edgecolor=color,
                                linewidth=2, zorder=3))
    ax.text(x, y, label,
            ha='center', va='center',
            color=color, fontsize=9.5, fontweight='bold', zorder=4)

# Forward arrows
for i in range(len(main_path) - 1):
    x1 = main_path[i][0] + state_w/2
    x2 = main_path[i+1][0] - state_w/2
    y  = main_path[i][1]
    draw_arrow(ax, x1, y, x2, y, color=SILVER, lw=1.5)

# Bridge-table consultations at each transition
consultations = [
    (3.0, 7.9,   'change_set_\nfield_change'),
    (5.5, 7.9,   'change_set_\nvalidation'),
    (8.1, 7.9,   'change_set_\napproval_required'),
    (10.8, 7.9,  'change_set_\napproval'),
    (13.5, 7.9,  'apply field changes\n+ version siblings'),
    (16.2, 7.9,  'audit_log_entry\non every step'),
]

for x, y, label in consultations:
    ax.text(x, y, label,
            ha='center', va='center',
            color=GOLD, fontsize=8, fontweight='bold',
            style='italic',
            bbox=dict(boxstyle='round,pad=0.2',
                      facecolor=BG, edgecolor=GOLD, linewidth=0.6, alpha=0.9))

# Branch states (below main path)
branches = [
    (4.2,  4.5, 'cancelled',      DIM,      'submitted',      'draft -> cancelled'),
    (6.8,  4.5, 'rejected',       RED,      'validating',     'on validation fail'),
    (9.4,  4.5, 'rejected',       RED,      'pending_\napproval', 'on rejection'),
    (9.4,  3.0, 'expired',        ORANGE,   'pending_\napproval', 'after deadline'),
]

# Emergency branch (above main path)
ax.add_patch(FancyBboxPatch((6.8 - state_w/2, 9.0 - state_h/2),
                            state_w, state_h,
                            boxstyle='round,pad=0.05',
                            facecolor=PAN, edgecolor=RED,
                            linewidth=2, zorder=3))
ax.text(6.8, 9.0, 'EMERGENCY\napplied',
        ha='center', va='center',
        color=RED, fontsize=9, fontweight='bold', zorder=4)
draw_arrow(ax, 6.8, 6.8 + state_h/2, 6.8, 9.0 - state_h/2,
           color=RED, lw=1.4, style='->', alpha=0.85)
ax.text(7.8, 8.0, 'is_emergency=true\nbreak-glass path',
        ha='left', va='center',
        color=RED, fontsize=8, style='italic')

# Emergency leads to applied AND requires post-hoc review
draw_arrow(ax, 6.8 + state_w/2, 9.0,
           14.8 - state_w/2, 6.8 + state_h/2 + 0.2,
           color=RED, lw=1.2, alpha=0.6, style='->')
ax.text(11.5, 9.4, 'requires change_set_emergency_review',
        ha='center', va='center',
        color=RED, fontsize=8, style='italic')

# Branch states
for x, y, label, color, parent_label, note in branches:
    ax.add_patch(FancyBboxPatch((x - state_w/2 + 0.2, y - state_h/2 + 0.1),
                                state_w - 0.4, state_h - 0.2,
                                boxstyle='round,pad=0.05',
                                facecolor=PAN, edgecolor=color,
                                linewidth=1.5, zorder=3))
    ax.text(x, y, label,
            ha='center', va='center',
            color=color, fontsize=9, fontweight='bold', zorder=4)
    # Arrow from main path
    draw_arrow(ax, x, 6.8 - state_h/2, x, y + state_h/2 - 0.1,
               color=color, lw=1.2, alpha=0.7)

# Rolled_back back-arrow from applied
ax.annotate('',
            xy=(17.6, 6.8 - 0.5),
            xytext=(14.8, 6.8 - 0.5),
            arrowprops=dict(arrowstyle='->', color=PURPLE,
                            lw=1.3, alpha=0.7,
                            connectionstyle='arc3,rad=-0.3'))
ax.text(16.2, 5.6, 'via new change_set\nrestoring prior values',
        ha='center', va='center',
        color=PURPLE, fontsize=8, style='italic')

# Bottom note
ax.add_patch(FancyBboxPatch((1, 0.6), 18, 1.3,
                            boxstyle='round,pad=0.1',
                            facecolor=BG, edgecolor=GOLD,
                            linewidth=1.2, alpha=0.85))
ax.text(10, 1.55,
        'every transition is recorded in audit_log_entry',
        ha='center', va='center',
        color=GOLD, fontsize=10, fontweight='bold')
ax.text(10, 1.0,
        'every approved change writes new rows in *_version siblings.  rollback is itself a change_set, never a side-channel.',
        ha='center', va='center',
        color=SILVER, fontsize=9, style='italic')

save(fig, 'infra3_06_change_set_lifecycle.png')


# ================================================================
# FIG 7: AUDIT LOG vs EVIDENCE RECORD vs VERSION HISTORY TIMELINES
# Type: 7 (Progression/Sequence Diagram)
# Shows: Three distinct streams over the same entity, distinct cadences and purposes
# ================================================================

print("Fig 7: Three streams — audit, evidence, version history")

fig, ax = plt.subplots(figsize=(18, 11))
style_axis(ax)
ax.set_xlim(0, 30)
ax.set_ylim(-0.5, 10)

ax.set_title('Audit Log, Evidence Record, Version History — Three Streams Over One Service',
             color=GOLD, fontsize=15, fontweight='bold', pad=14)
ax.text(15, 10.4,
        'Same entity (service "user-api"), three distinct streams with distinct cadences and purposes',
        ha='center', va='center',
        color=SILVER, fontsize=11, transform=ax.transData)

# Three lanes
lane_y_audit    = 7.5
lane_y_evidence = 4.8
lane_y_version  = 2.0

# Lane labels and frames
lanes = [
    (lane_y_audit,    'audit_log_entry',          MAG,
     'every API action  -  append-only  -  attribution + timestamp'),
    (lane_y_evidence, 'evidence_record',          GREEN,
     'verification outcomes  -  written by runners and humans'),
    (lane_y_version,  'service_version  (history)', BLUE,
     'every committed change to centrally-managed config  -  per-field versioning'),
]

for ly, name, color, sub in lanes:
    # Lane background band
    ax.axhspan(ly - 0.7, ly + 0.7, color=color, alpha=0.06, zorder=1)
    # Lane label on left
    ax.text(0.4, ly + 0.35, name,
            ha='left', va='center',
            color=color, fontsize=11, fontweight='bold')
    ax.text(0.4, ly - 0.2, sub,
            ha='left', va='center',
            color=SILVER, fontsize=8.5, style='italic')
    # Lane spine
    ax.axhline(ly, xmin=0.30, xmax=0.99,
               color=color, linewidth=0.8, alpha=0.4)

# Audit log events (high frequency)
np.random.seed(42)
audit_times = sorted(np.random.uniform(9, 28, 28))
for t in audit_times:
    ax.scatter(t, lane_y_audit, s=80,
               color=MAG, edgecolor=WHITE, linewidth=1.0, zorder=4)

# Evidence records (medium frequency, scheduled)
evidence_times = [10.5, 15.0, 19.5, 24.0]
evidence_status = [GREEN, GREEN, RED, GREEN]
evidence_labels = ['backup\nverified', 'cert\nvalidated', 'compliance\nFAIL', 'access\nreview ok']
for t, c, label in zip(evidence_times, evidence_status, evidence_labels):
    ax.scatter(t, lane_y_evidence, s=200,
               color=c, edgecolor=WHITE, linewidth=2, marker='D', zorder=4)
    ax.text(t, lane_y_evidence + 0.65, label,
            ha='center', va='bottom',
            color=c, fontsize=8, fontweight='bold')

# Version history (lower frequency, change-driven)
version_times = [11.0, 16.0, 20.5]
version_serials = ['v=4', 'v=5', 'v=6']
for t, vs in zip(version_times, version_serials):
    ax.scatter(t, lane_y_version, s=200,
               color=BLUE, edgecolor=WHITE, linewidth=2, zorder=4)
    ax.text(t, lane_y_version + 0.55, vs,
            ha='center', va='bottom',
            color=BLUE, fontsize=9, fontweight='bold')

# Vertical dashed lines connecting related events
# When a version commits, an audit_log entry is written
for vt in version_times:
    ax.plot([vt, vt], [lane_y_version, lane_y_audit],
            color=GOLD, linewidth=0.8, linestyle=':', alpha=0.5, zorder=2)

# Legend
ax.text(29.5, lane_y_audit, '~28 events',
        ha='right', va='center',
        color=MAG, fontsize=9, alpha=0.85)
ax.text(29.5, lane_y_evidence, '4 records',
        ha='right', va='center',
        color=GREEN, fontsize=9, alpha=0.85)
ax.text(29.5, lane_y_version, '3 versions',
        ha='right', va='center',
        color=BLUE, fontsize=9, alpha=0.85)

# Annotation showing relationship
ax.annotate('every committed change\nwrites BOTH a version\nAND audit entries',
            xy=(11.0, lane_y_audit - 0.2),
            xytext=(7.5, 9.4),
            color=GOLD, fontsize=8, style='italic',
            ha='center', va='center',
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.0, alpha=0.7))

# X axis: time
ax.set_xlabel('time  -->', color=SILVER, fontsize=11, labelpad=8)
ax.set_xticks([5, 10, 15, 20, 25])
ax.set_xticklabels(['day 1', 'day 4', 'day 7', 'day 10', 'day 13'])
ax.set_yticks([])

# Bottom note
ax.text(15, 0.4,
        'distinct cadences  /  distinct purposes  /  same entity  -  '
        'auditors query all three for full picture',
        ha='center', va='center',
        color=DIM, fontsize=9.5, style='italic')

save(fig, 'infra3_07_three_streams.png')


# ================================================================
# FIG 8: CACHED OBSERVATION FLOW WITH RETENTION HORIZON
# Type: 1 (Running/Convergence Chart)
# Shows: Pullers populate continuously, retention bounds growth, freshness annotated
# ================================================================

print("Fig 8: Cached observation flow with retention horizon")

fig, ax = plt.subplots(figsize=(18, 10))
style_axis(ax)

ax.set_title('observation_cache_metric — Continuous Population with Bounded Retention',
             color=GOLD, fontsize=15, fontweight='bold', pad=14)

# X axis: time in minutes
t_max = 60.0  # last 60 minutes
n_pullers = 3
puller_interval = [1.0, 2.0, 5.0]  # minutes between pulls per puller
puller_colors = [BLUE, GREEN, MAG]
puller_names = ['puller-A  (60s cadence)',
                'puller-B  (120s cadence)',
                'puller-C  (300s cadence)']
retention_horizon = 30.0  # minutes; rows older than this are reaped

# Generate pulls
all_pulls = []
for p_idx, (interval, color, name) in enumerate(zip(puller_interval,
                                                    puller_colors,
                                                    puller_names)):
    times = np.arange(0.5, t_max + 0.01, interval)
    for tm in times:
        all_pulls.append((tm, p_idx, color))

# Sort by time
all_pulls.sort(key=lambda r: r[0])

# Plot row count over time
times_grid = np.linspace(0, t_max, 600)
counts_grid = np.zeros_like(times_grid)
for i, t in enumerate(times_grid):
    # rows still alive: pulls with time > (t - retention_horizon) and time <= t
    alive = sum(1 for (pt, _, _) in all_pulls
                if (pt <= t) and (pt > t - retention_horizon))
    counts_grid[i] = alive

ax.plot(times_grid, counts_grid,
        color=GOLD, linewidth=2.5, label='cache row count', zorder=5)
ax.fill_between(times_grid, 0, counts_grid,
                color=GOLD, alpha=0.08, zorder=2)

# Mark individual pulls as dots near bottom
for i, (pt, p_idx, color) in enumerate(all_pulls):
    y = 1.5 + p_idx * 1.2
    ax.scatter(pt, y, s=35, color=color, edgecolor=WHITE,
               linewidth=0.8, zorder=4)

# Puller lane labels at right
for p_idx, (color, name) in enumerate(zip(puller_colors, puller_names)):
    y = 1.5 + p_idx * 1.2
    ax.text(t_max - 0.5, y + 0.05, name,
            ha='right', va='center',
            color=color, fontsize=9, fontweight='bold')

# Retention horizon shaded region
ax.axvspan(0, retention_horizon, color=RED, alpha=0.07, zorder=1)
ax.axvline(retention_horizon, color=RED, linewidth=1.6,
           linestyle='--', alpha=0.7, zorder=3)
ax.text(retention_horizon - 0.5, ax.get_ylim()[1] * 0.95
        if False else 38,
        'retention horizon',
        ha='right', va='top',
        color=RED, fontsize=10, fontweight='bold',
        rotation=90)

# Annotation for "rows reaped beyond horizon"
ax.annotate('older rows\nreaped',
            xy=(8, 14),
            xytext=(8, 28),
            color=RED, fontsize=9.5, fontweight='bold',
            ha='center', va='center',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.3))

# Annotation for the row count plateau
ax.annotate('count plateaus once\nretention horizon reached',
            xy=(45, counts_grid[-150]),
            xytext=(45, 50),
            color=GOLD, fontsize=9.5, fontweight='bold',
            ha='center', va='center',
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.3))

# Sample row schematic in upper right
schematic_x, schematic_y = 5, 47
ax.text(schematic_x, schematic_y + 4,
        'each row carries:',
        ha='left', va='center',
        color=SILVER, fontsize=9, fontweight='bold')
schematic_lines = [
    'metric_key',
    'hostname',
    'metric_value',
    '_observed_time',
    '_authority_id',
    '_puller_runner_job_id',
]
for i, line in enumerate(schematic_lines):
    color = GOLD if line.startswith('_') else WHITE
    ax.text(schematic_x, schematic_y + 2.5 - i * 1.2,
            line,
            ha='left', va='center',
            color=color, fontsize=8.5,
            family='monospace')

# Axes
ax.set_xlabel('time  (minutes ago, 0 = now)',
              color=SILVER, fontsize=11, labelpad=8)
ax.set_ylabel('rows in observation_cache_metric',
              color=SILVER, fontsize=11, labelpad=8)
ax.set_xlim(0, t_max)
ax.set_ylim(0, 60)

# Invert x-axis so "now" is on the right
ax.invert_xaxis()

# Bottom note inside axis bounds
ax.text(t_max / 2, 4.8,
        'cached observation does NOT go through change management.  '
        'pullers write with scoped credentials; reaper enforces retention.',
        ha='center', va='center',
        color=DIM, fontsize=9, style='italic')

save(fig, 'infra3_08_cached_observation_flow.png')


# ================================================================
# SUMMARY
# ================================================================

print("")
print("All 8 figures generated:")
print("  infra3_01_top_level_taxonomy.png")
print("  infra3_02_substrate_nesting.png")
print("  infra3_03_dsnc_namespace_tree.png")
print("  infra3_04_service_connection_graph.png")
print("  infra3_05_polymorphic_bridge_tables.png")
print("  infra3_06_change_set_lifecycle.png")
print("  infra3_07_three_streams.png")
print("  infra3_08_cached_observation_flow.png")
