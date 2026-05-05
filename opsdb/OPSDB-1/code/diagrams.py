#!/usr/bin/env python3
"""
OPSDB OPSDB-1 Diagrams - The OpsDB: A Substrate for Coherent Operations
8 figures covering fragmentation, architecture, scope, before/after workflows,
continuous compliance, compounding benefits, and drift lifecycle.
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
# FIG 1: FRAGMENTED OPERATIONS TODAY
# Type: 4 (Geometric Cross-Section)
# Shows: the picture-in-head burden; visual chaos of fragmentation;
#        operator at center surrounded by disconnected tools.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 13), facecolor=BG)
ax.set_facecolor(BG)

# Operator at center
op_x, op_y = 0, 0
op_circle = Circle((op_x, op_y), 1.4, facecolor=PAN, edgecolor=ORANGE,
                   linewidth=2.5, zorder=10)
ax.add_patch(op_circle)
ax.text(op_x, op_y + 0.30, 'Operator', ha='center', va='center',
        fontsize=13, color=ORANGE, fontweight='bold', zorder=11)
ax.text(op_x, op_y - 0.05, 'holds the picture', ha='center', va='center',
        fontsize=9, color=SILVER, zorder=11)
ax.text(op_x, op_y - 0.30, 'in their head', ha='center', va='center',
        fontsize=9, color=SILVER, zorder=11)
ax.text(op_x, op_y - 0.65, '(03:00)', ha='center', va='center',
        fontsize=8, color=DIM, style='italic', zorder=11)

# Tools scattered around the operator. Each tool holds one slice of operational reality.
tools = [
    # (angle_degrees, distance, tool_name, holds_what, color)
    ( 90, 6.5, 'PagerDuty',     'on-call',           CYAN),
    ( 50, 6.8, 'Grafana',       'dashboards',        BLUE),
    ( 18, 6.5, 'kubectl',       'cluster state',     PURPLE),
    (-18, 6.8, 'cloud console', 'cloud resources',   GREEN),
    (-50, 6.5, 'Datadog',       'metrics',           BLUE),
    (-85, 6.8, 'vault',         'secrets',           MAG),
    (-115, 6.5,'Jira',          'tickets',           ORANGE),
    (-150, 6.8,'wiki',          'runbooks',          GOLD),
    ( 180, 6.5,'Slack',         'discussion',        PURPLE),
    ( 150, 6.8,'git/CI',        'deployments',       CYAN),
    ( 120, 6.5,'IdP console',   'identities',        MAG),
    (  75, 6.8,'Salt/Ansible',  'host config',       GREEN),
]

tool_w = 2.4
tool_h = 1.4

for angle_deg, dist, name, holds, color in tools:
    angle = np.radians(angle_deg)
    tx = dist * np.cos(angle)
    ty = dist * np.sin(angle)

    # Tool box
    box = FancyBboxPatch((tx - tool_w/2, ty - tool_h/2), tool_w, tool_h,
                         boxstyle='round,pad=0.05',
                         facecolor=PAN, edgecolor=color, linewidth=1.8)
    ax.add_patch(box)
    ax.text(tx, ty + 0.22, name, ha='center', va='center',
            fontsize=10, color=color, fontweight='bold')
    ax.text(tx, ty - 0.20, 'holds:', ha='center', va='center',
            fontsize=7.5, color=DIM, style='italic')
    ax.text(tx, ty - 0.45, holds, ha='center', va='center',
            fontsize=8.5, color=SILVER)

    # Operator must visit this tool: dashed line from operator to tool
    # Pull the line endpoints back from the box edges
    inner_dist = 1.5  # operator radius
    outer_dist = dist - tool_w/2 * 0.6
    sx = inner_dist * np.cos(angle)
    sy = inner_dist * np.sin(angle)
    ex = outer_dist * np.cos(angle)
    ey = outer_dist * np.sin(angle)
    ax.plot([sx, ex], [sy, ey], color=DIM, linewidth=1.0, linestyle='--',
            alpha=0.5, zorder=2)

# Tangle indicator: cross-tool dashed lines suggesting operator must mentally join
tangle_pairs = [
    (0, 4),   # PagerDuty <-> Datadog
    (1, 7),   # Grafana <-> wiki
    (2, 8),   # kubectl <-> Slack
    (3, 9),   # cloud <-> git/CI
    (5, 10),  # vault <-> IdP
    (6, 11),  # Jira <-> Salt/Ansible
]
for i, j in tangle_pairs:
    a1 = np.radians(tools[i][0])
    a2 = np.radians(tools[j][0])
    d1 = tools[i][1] - tool_w/2 * 0.6
    d2 = tools[j][1] - tool_w/2 * 0.6
    x1, y1 = d1 * np.cos(a1), d1 * np.sin(a1)
    x2, y2 = d2 * np.cos(a2), d2 * np.sin(a2)
    ax.plot([x1, x2], [y1, y2], color=RED, linewidth=0.8, linestyle=':',
            alpha=0.35, zorder=1)

# Annotations along the bottom describing the cost
cost_y = -9.2
ax.text(0, cost_y + 0.4,
        'No tool owns the whole picture.',
        ha='center', va='center', fontsize=12, color=GOLD, fontweight='bold')
ax.text(0, cost_y - 0.05,
        'Investigation, change, and audit each require touring N tools and joining mentally.',
        ha='center', va='center', fontsize=10.5, color=SILVER, style='italic')
ax.text(0, cost_y - 0.50,
        'The cost is paid daily. It feels like the natural cost of operating.',
        ha='center', va='center', fontsize=10, color=DIM, style='italic')

ax.set_xlim(-10.5, 10.5)
ax.set_ylim(-10.0, 9.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Fragmented Operations Today\nThe starting state most organizations live in',
             color=GOLD, fontsize=16, fontweight='bold', pad=15)

save(fig, 'infra7_01_fragmented_operations.png')


# ================================================================
# FIG 2: THE OPSDB ARCHITECTURE IN ONE IMAGE
# Type: 4 (Geometric Cross-Section)
# Shows: passive substrate at center, runner ring, authority ring;
#        the whole architectural pattern in one view.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 14), facecolor=BG)
ax.set_facecolor(BG)

# --- Center: OpsDB substrate ---
opsdb_r = 1.8
opsdb = Circle((0, 0), opsdb_r, facecolor=PAN, edgecolor=GOLD,
               linewidth=3, zorder=10)
ax.add_patch(opsdb)
ax.text(0, 0.40, 'OpsDB', ha='center', va='center',
        fontsize=18, color=GOLD, fontweight='bold', zorder=11)
ax.text(0, 0.05, 'substrate', ha='center', va='center',
        fontsize=11, color=WHITE, zorder=11)
ax.text(0, -0.30, '(passive)', ha='center', va='center',
        fontsize=9, color=SILVER, style='italic', zorder=11)
ax.text(0, -0.60, 'config + cached state +', ha='center', va='center',
        fontsize=7.5, color=DIM, zorder=11)
ax.text(0, -0.85, 'pointers + history', ha='center', va='center',
        fontsize=7.5, color=DIM, zorder=11)

# --- API gate ring (thin) ---
gate_r_in = opsdb_r + 0.15
gate_r_out = gate_r_in + 0.5
gate = Wedge((0, 0), gate_r_out, 0, 360, width=gate_r_out - gate_r_in,
             facecolor=GOLD, edgecolor=GOLD, linewidth=1.5, alpha=0.20, zorder=8)
ax.add_patch(gate)
gate_outline_in = Circle((0, 0), gate_r_in, fill=False, edgecolor=GOLD,
                         linewidth=1.2, alpha=0.7, zorder=9)
gate_outline_out = Circle((0, 0), gate_r_out, fill=False, edgecolor=GOLD,
                          linewidth=1.5, alpha=0.9, zorder=9)
ax.add_patch(gate_outline_in)
ax.add_patch(gate_outline_out)
# Label "API gate" at the top of the ring
ax.text(0, gate_r_in + 0.25, 'API gate', ha='center', va='center',
        fontsize=10, color=GOLD, fontweight='bold', zorder=11,
        bbox=dict(boxstyle='round,pad=0.2', facecolor=BG, edgecolor=GOLD,
                  linewidth=1))

# --- Runner ring ---
runner_dist = 4.5
runners = [
    ( 90, 'puller',           CYAN),
    ( 50, 'reconciler',       BLUE),
    ( 18, 'verifier',         GREEN),
    (-18, 'drift detector',   PURPLE),
    (-50, 'change executor',  ORANGE),
    (-90, 'reaper',           MAG),
    (-130,'scheduler',        CYAN),
    (-160,'failover',         BLUE),
    ( 160,'bootstrapper',     GREEN),
    ( 130,'reactor',          PURPLE),
]

# Runner ring outline
ring_r_in = 3.8
ring_r_out = 5.2
ring = Wedge((0, 0), ring_r_out, 0, 360, width=ring_r_out - ring_r_in,
             facecolor=BLUE, edgecolor=DIM, linewidth=0.8, alpha=0.05, zorder=3)
ax.add_patch(ring)

runner_w = 1.7
runner_h = 0.75

for angle_deg, name, color in runners:
    angle = np.radians(angle_deg)
    rx = runner_dist * np.cos(angle)
    ry = runner_dist * np.sin(angle)

    box = FancyBboxPatch((rx - runner_w/2, ry - runner_h/2), runner_w, runner_h,
                         boxstyle='round,pad=0.04',
                         facecolor=PAN, edgecolor=color, linewidth=1.5, zorder=5)
    ax.add_patch(box)
    ax.text(rx, ry, name, ha='center', va='center',
            fontsize=9, color=color, fontweight='bold', zorder=6)

    # Bidirectional read/write through the gate
    inner_x = (gate_r_out + 0.05) * np.cos(angle)
    inner_y = (gate_r_out + 0.05) * np.sin(angle)
    outer_x = (runner_dist - runner_w/2 * 0.7) * np.cos(angle)
    outer_y = (runner_dist - runner_h/2 * 0.7) * np.sin(angle)
    ax.annotate('', xy=(outer_x, outer_y), xytext=(inner_x, inner_y),
                arrowprops=dict(arrowstyle='<->', color=color, lw=1.2, alpha=0.6),
                zorder=4)

# Runner ring label
ax.text(0, runner_dist + 1.0, 'runner population',
        ha='center', va='center', fontsize=11, color=WHITE, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.25', facecolor=BG, edgecolor=DIM,
                  linewidth=1))
ax.text(0, runner_dist + 0.6, '(small, single-purpose, decentralized)',
        ha='center', va='center', fontsize=8, color=SILVER, style='italic')

# --- Authority ring (outermost) ---
auth_dist = 7.8
authorities = [
    ( 75, 'Prometheus',       'metrics',         BLUE),
    ( 35, 'Kubernetes API',   'cluster state',   PURPLE),
    (  0, 'cloud control',    'cloud resources', GREEN),
    (-35, 'IdP',              'identities',      MAG),
    (-75, 'vault',            'secrets',         MAG),
    (-110,'monitoring',       'time series',     BLUE),
    (-150,'CI / registry',    'images',          ORANGE),
    ( 150,'wiki',             'runbooks',        GOLD),
    ( 110,'ticketing',        'tickets',         ORANGE),
]

auth_w = 2.2
auth_h = 1.2

for angle_deg, name, holds, color in authorities:
    angle = np.radians(angle_deg)
    ax_x = auth_dist * np.cos(angle)
    ax_y = auth_dist * np.sin(angle)

    box = FancyBboxPatch((ax_x - auth_w/2, ax_y - auth_h/2), auth_w, auth_h,
                         boxstyle='round,pad=0.05',
                         facecolor=PAN, edgecolor=color, linewidth=1.5,
                         alpha=0.85, zorder=5)
    ax.add_patch(box)
    ax.text(ax_x, ax_y + 0.18, name, ha='center', va='center',
            fontsize=9, color=color, fontweight='bold', zorder=6)
    ax.text(ax_x, ax_y - 0.20, holds, ha='center', va='center',
            fontsize=7.5, color=SILVER, style='italic', zorder=6)

    # Pointer from OpsDB (via gate) into authority - shows that OpsDB
    # holds the directory of where this lives
    inner_x = (gate_r_out + 0.05) * np.cos(angle)
    inner_y = (gate_r_out + 0.05) * np.sin(angle)
    outer_x = (auth_dist - auth_w/2 * 0.7) * np.cos(angle)
    outer_y = (auth_dist - auth_h/2 * 0.7) * np.sin(angle)
    ax.annotate('', xy=(outer_x, outer_y), xytext=(inner_x, inner_y),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.0,
                                alpha=0.35, linestyle=':'),
                zorder=3)

# Authority ring label - top
ax.text(0, auth_dist + 1.05, 'external authorities',
        ha='center', va='center', fontsize=11, color=WHITE, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.25', facecolor=BG, edgecolor=DIM,
                  linewidth=1))
ax.text(0, auth_dist + 0.65,
        '(OpsDB holds typed pointers to each)',
        ha='center', va='center', fontsize=8, color=SILVER, style='italic')

# Three populations entering from the bottom-left at the gate
populations = [
    (-9.5,  -2.0, 'humans',     CYAN,   'investigate, propose'),
    (-9.5,  -3.0, 'automation', BLUE,   '(the runners above)'),
    (-9.5,  -4.0, 'auditors',   PURPLE, 'verify controls'),
]
for px, py, label, color, sub in populations:
    box = FancyBboxPatch((px - 1.0, py - 0.30), 2.0, 0.60,
                         boxstyle='round,pad=0.05',
                         facecolor=PAN, edgecolor=color, linewidth=1.5)
    ax.add_patch(box)
    ax.text(px, py + 0.05, label, ha='center', va='center',
            fontsize=9.5, color=color, fontweight='bold')
    ax.text(px, py - 0.18, sub, ha='center', va='center',
            fontsize=7.5, color=SILVER, style='italic')

# Bottom caption
ax.text(0, -9.2,
        'One substrate. One gate. Many runners around it. Pointers to authorities for everything else.',
        ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold')
ax.text(0, -9.65,
        'The substrate is passive; the runners are the active layer; the authorities continue serving live data directly.',
        ha='center', va='center', fontsize=9.5, color=SILVER, style='italic')

ax.set_xlim(-11.5, 11.5)
ax.set_ylim(-10.5, 10.0)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('The OpsDB Architecture in One Image\nSubstrate at center, gate around it, runners and authorities outside',
             color=GOLD, fontsize=16, fontweight='bold', pad=15)

save(fig, 'infra7_02_opsdb_architecture.png')


# ================================================================
# FIG 3: THE COMPREHENSIVE SCOPE SWEEP
# Type: 4 (Geometric)
# Shows: that "all of ops" is a sweep across many domains, not a slogan.
# ================================================================

fig, ax = plt.subplots(figsize=(16, 14), facecolor=BG)
ax.set_facecolor(BG)

# All operational domains the OpsDB covers
domains = [
    ('substrate',         'hardware, VMs, hypervisors', GREEN),
    ('Kubernetes',        'clusters, pods, workloads',  BLUE),
    ('cloud',             'AWS, GCP, Azure resources',  PURPLE),
    ('services',          'packages, deployments',      CYAN),
    ('networking',        'DNS, load balancers, VPCs',  BLUE),
    ('identity',          'users, groups, roles',       MAG),
    ('certificates',      'TLS, SSH, signing keys',     ORANGE),
    ('credentials',       'rotation schedules',         MAG),
    ('vendors',           'contracts, renewals',        GOLD),
    ('manual ops',        'tape rotation, audits',      ORANGE),
    ('compliance',        'regimes, scopes, evidence',  GREEN),
    ('runners',           'enumeration, jobs, output',  PURPLE),
    ('schedules',         'when work happens',          BLUE),
    ('policies',          'security zones, retention',  RED),
    ('monitoring',        'monitors, alerts, on-call',  CYAN),
    ('observation',       'cached state from authorities', GREEN),
    ('documentation',     'runbooks, dashboards',       GOLD),
    ('change mgmt',       'change_sets, approvals',     ORANGE),
    ('audit',             'every action recorded',      MAG),
    ('schema metadata',   'OpsDB describes itself',     SILVER),
]

n = len(domains)
center_x, center_y = 0, 0
domain_dist = 5.6
domain_w = 2.6
domain_h = 1.05

# Center label
center_circle = Circle((0, 0), 1.5, facecolor=PAN, edgecolor=GOLD,
                       linewidth=2.5, zorder=10)
ax.add_patch(center_circle)
ax.text(0, 0.35, 'OpsDB', ha='center', va='center',
        fontsize=14, color=GOLD, fontweight='bold', zorder=11)
ax.text(0, 0.0, 'all of ops', ha='center', va='center',
        fontsize=10, color=WHITE, zorder=11)
ax.text(0, -0.35, '(comprehensive)', ha='center', va='center',
        fontsize=8, color=SILVER, style='italic', zorder=11)

# Place the 20 domains around the center.
# Use a careful angular spacing with a rotational offset so labels don't collide.
for i, (name, holds, color) in enumerate(domains):
    angle = np.radians(90 - i * (360.0 / n))  # start at top, go clockwise
    dx = domain_dist * np.cos(angle)
    dy = domain_dist * np.sin(angle)

    box = FancyBboxPatch((dx - domain_w/2, dy - domain_h/2),
                         domain_w, domain_h,
                         boxstyle='round,pad=0.05',
                         facecolor=PAN, edgecolor=color, linewidth=1.6,
                         zorder=5)
    ax.add_patch(box)
    ax.text(dx, dy + 0.20, name, ha='center', va='center',
            fontsize=9.5, color=color, fontweight='bold', zorder=6)
    ax.text(dx, dy - 0.22, holds, ha='center', va='center',
            fontsize=7.5, color=SILVER, zorder=6)

    # Spoke from center to domain
    inner_x = 1.6 * np.cos(angle)
    inner_y = 1.6 * np.sin(angle)
    outer_x = (domain_dist - domain_w/2 * 0.7) * np.cos(angle)
    outer_y = (domain_dist - domain_h/2 * 0.7) * np.sin(angle)
    ax.plot([inner_x, outer_x], [inner_y, outer_y],
            color=color, linewidth=1.0, alpha=0.4, zorder=3)

# Bottom caption
ax.text(0, -7.5,
        '20 operational domains, one substrate.',
        ha='center', va='center', fontsize=12, color=GOLD, fontweight='bold')
ax.text(0, -7.95,
        'Tape rotations and certificate inventories belong here as much as Kubernetes workloads.',
        ha='center', va='center', fontsize=10, color=SILVER, style='italic')
ax.text(0, -8.35,
        'If the organization performs the activity as part of operating itself, the OpsDB can hold its data.',
        ha='center', va='center', fontsize=9.5, color=DIM, style='italic')

ax.set_xlim(-9.5, 9.5)
ax.set_ylim(-9.0, 8.0)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('The Comprehensive Scope Sweep\n"All of ops" cashed out as 20 domains',
             color=GOLD, fontsize=16, fontweight='bold', pad=15)

save(fig, 'infra7_03_comprehensive_scope.png')


# ================================================================
# FIG 4: INVESTIGATION BEFORE VS AFTER
# Type: 7 (Progression) x 2 panels
# Shows: operator tour of 8 tools vs one query + resolved view.
# ================================================================

fig, (axL, axR) = plt.subplots(1, 2, figsize=(20, 11),
                                facecolor=BG, gridspec_kw={'wspace': 0.10})

for ax in (axL, axR):
    ax.set_facecolor(PAN)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)

# --- LEFT PANEL: Before ---
axL.set_title('BEFORE: tour of N tools',
              color=RED, fontsize=14, fontweight='bold', pad=12)

# Operator at top
op_box_L = FancyBboxPatch((3.5, 10.4), 3.0, 1.2,
                          boxstyle='round,pad=0.1',
                          facecolor=PAN, edgecolor=ORANGE, linewidth=2.5)
axL.add_patch(op_box_L)
axL.text(5.0, 11.20, 'Operator', ha='center', va='center',
         fontsize=11, color=ORANGE, fontweight='bold')
axL.text(5.0, 10.80, '03:00 page', ha='center', va='center',
         fontsize=9, color=SILVER, style='italic')
axL.text(5.0, 10.55, '"What is happening?"',
         ha='center', va='center', fontsize=8.5, color=WHITE)

# Sequence of tools the operator tours
tour_steps = [
    (1, 'PagerDuty',          'who is on-call?',         CYAN),
    (2, 'Slack',              'incident channel?',       PURPLE),
    (3, 'Grafana',            'find the dashboard',      BLUE),
    (4, 'kubectl',            'kubectl get pods',        GREEN),
    (5, 'kubectl logs',       'why is it failing?',      GREEN),
    (6, 'wiki',               'find a runbook',          GOLD),
    (7, 'git/CI',             'recent deploys?',         ORANGE),
    (8, 'cloud console',      'cloud-side check',        MAG),
]

step_y_top = 9.5
step_h = 0.85
step_gap = 0.20

for i, (n, tool, query, color) in enumerate(tour_steps):
    y = step_y_top - i * (step_h + step_gap)
    # Step number circle
    num_circle = Circle((1.2, y), 0.30, facecolor=PAN, edgecolor=color,
                        linewidth=1.5)
    axL.add_patch(num_circle)
    axL.text(1.2, y, str(n), ha='center', va='center',
             fontsize=9, color=color, fontweight='bold')

    # Tool box
    box = FancyBboxPatch((1.85, y - step_h/2), 7.6, step_h,
                         boxstyle='round,pad=0.05',
                         facecolor=PAN, edgecolor=color, linewidth=1.3)
    axL.add_patch(box)
    axL.text(2.5, y, tool, ha='left', va='center',
             fontsize=10, color=color, fontweight='bold')
    axL.text(5.5, y, query, ha='left', va='center',
             fontsize=8.5, color=SILVER, style='italic')

    # Connecting line down (except last)
    if i < len(tour_steps) - 1:
        axL.plot([1.2, 1.2], [y - step_h/2 - 0.05, y - step_h - step_gap + step_h/2 + 0.05],
                 color=DIM, linewidth=0.8, linestyle=':')

# Outcome at bottom
out_y = 0.85
out_box_L = FancyBboxPatch((1.0, 0.30), 8.0, 1.2,
                           boxstyle='round,pad=0.1',
                           facecolor=RED, edgecolor=RED, linewidth=2, alpha=0.20)
axL.add_patch(out_box_L)
axL.text(5.0, out_y + 0.30, 'Picture assembled in operator\'s head',
         ha='center', va='center', fontsize=10.5, color=RED, fontweight='bold')
axL.text(5.0, out_y - 0.10, 'No structured trail. Next operator next quarter starts over.',
         ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# --- RIGHT PANEL: After ---
axR.set_title('AFTER: one query, resolved view',
              color=GREEN, fontsize=14, fontweight='bold', pad=12)

# Operator at top
op_box_R = FancyBboxPatch((3.5, 10.4), 3.0, 1.2,
                          boxstyle='round,pad=0.1',
                          facecolor=PAN, edgecolor=ORANGE, linewidth=2.5)
axR.add_patch(op_box_R)
axR.text(5.0, 11.20, 'Operator', ha='center', va='center',
         fontsize=11, color=ORANGE, fontweight='bold')
axR.text(5.0, 10.80, '03:00 page', ha='center', va='center',
         fontsize=9, color=SILVER, style='italic')
axR.text(5.0, 10.55, '(page links to incident view)',
         ha='center', va='center', fontsize=8.5, color=WHITE)

# Single arrow down to the resolved view
axR.annotate('', xy=(5.0, 9.4), xytext=(5.0, 10.4),
             arrowprops=dict(arrowstyle='->', color=GOLD, lw=2.5))
axR.text(5.4, 9.85, 'one query', ha='left', va='center',
         fontsize=9, color=GOLD, fontweight='bold')

# OpsDB query box
query_box = FancyBboxPatch((1.0, 8.0), 8.0, 1.4,
                           boxstyle='round,pad=0.1',
                           facecolor=PAN, edgecolor=GOLD, linewidth=2.5)
axR.add_patch(query_box)
axR.text(5.0, 8.95, 'GET service incident view',
         ha='center', va='center', fontsize=11, color=GOLD,
         fontweight='bold', fontfamily='monospace')
axR.text(5.0, 8.55, 'one OpsDB query, all relevant context resolved',
         ha='center', va='center', fontsize=9, color=SILVER, style='italic')
axR.text(5.0, 8.25, 'service_id = affected_service',
         ha='center', va='center', fontsize=8, color=WHITE,
         fontfamily='monospace')

# Arrow down
axR.annotate('', xy=(5.0, 7.4), xytext=(5.0, 8.0),
             arrowprops=dict(arrowstyle='->', color=GOLD, lw=2))

# Resolved view: structured panels showing what comes back
resolved_items = [
    ('runbook reference',     'last_tested 18d ago',     GOLD,    7.0, 1.4),
    ('dashboards (3)',        'primary, capacity, errors', BLUE,  7.0, 5.4),
    ('recent change_sets',    '2 in last hour',          ORANGE,  6.0, 1.4),
    ('on-call schedule',      'current: alice@team',     CYAN,    6.0, 5.4),
    ('dependent services (5)','via service_connection',  PURPLE,  5.0, 1.4),
    ('recent evidence',       'backup ok, scan failed',  MAG,     5.0, 5.4),
    ('runner_job (recent)',   '12 jobs, all OK',         GREEN,   4.0, 1.4),
    ('cached state',          '_observed_time 23s ago',  CYAN,    4.0, 5.4),
]

r_w = 3.4
r_h = 0.80

for label, detail, color, y, x in resolved_items:
    box = FancyBboxPatch((x, y - r_h/2), r_w, r_h,
                         boxstyle='round,pad=0.04',
                         facecolor=PAN, edgecolor=color, linewidth=1.3)
    axR.add_patch(box)
    axR.text(x + 0.15, y + 0.13, label, ha='left', va='center',
             fontsize=9, color=color, fontweight='bold')
    axR.text(x + 0.15, y - 0.18, detail, ha='left', va='center',
             fontsize=7.5, color=SILVER, style='italic')

# Outcome at bottom
out_box_R = FancyBboxPatch((1.0, 0.30), 8.0, 2.6,
                           boxstyle='round,pad=0.1',
                           facecolor=GREEN, edgecolor=GREEN, linewidth=2, alpha=0.20)
axR.add_patch(out_box_R)
axR.text(5.0, 2.45, 'Picture assembled by the gate',
         ha='center', va='center', fontsize=10.5, color=GREEN, fontweight='bold')
axR.text(5.0, 2.05,
         'Operator follows runbook. Each action is a runner_job',
         ha='center', va='center', fontsize=9, color=WHITE)
axR.text(5.0, 1.75,
         'with full attribution. Trail composes itself.',
         ha='center', va='center', fontsize=9, color=WHITE)
axR.text(5.0, 1.20,
         'Post-incident: runbook update is a change_set;',
         ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')
axR.text(5.0, 0.90,
         'last_tested_time updates; new version in history.',
         ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')

for ax in (axL, axR):
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.suptitle('Investigation During an Incident: Before vs After\n'
             'Same operator, same incident; the difference is what gets recorded',
             color=GOLD, fontsize=15, fontweight='bold', y=0.99)

save(fig, 'infra7_04_investigation_before_after.png')


# ================================================================
# FIG 5: AUDIT BEFORE VS AFTER
# Type: 7 (Progression) x 2 panels
# Shows: scramble-and-binder vs auditor querying directly.
# ================================================================

fig, (axL, axR) = plt.subplots(1, 2, figsize=(20, 11),
                                facecolor=BG, gridspec_kw={'wspace': 0.10})

for ax in (axL, axR):
    ax.set_facecolor(PAN)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)

# --- LEFT PANEL: Before ---
axL.set_title('BEFORE: scramble and binder',
              color=RED, fontsize=14, fontweight='bold', pad=12)

# Auditor at top
aud_box_L = FancyBboxPatch((3.5, 10.4), 3.0, 1.2,
                           boxstyle='round,pad=0.1',
                           facecolor=PAN, edgecolor=PURPLE, linewidth=2.5)
axL.add_patch(aud_box_L)
axL.text(5.0, 11.20, 'Auditor', ha='center', va='center',
         fontsize=11, color=PURPLE, fontweight='bold')
axL.text(5.0, 10.80, 'requests evidence for Q3', ha='center', va='center',
         fontsize=9, color=SILVER, style='italic')
axL.text(5.0, 10.55, '"show me your access reviews"',
         ha='center', va='center', fontsize=8.5, color=WHITE)

# Arrow down to team
axL.annotate('', xy=(5.0, 9.7), xytext=(5.0, 10.4),
             arrowprops=dict(arrowstyle='->', color=PURPLE, lw=1.5))

# Team scrambling
scramble_box = FancyBboxPatch((1.0, 7.5), 8.0, 2.0,
                              boxstyle='round,pad=0.1',
                              facecolor=PAN, edgecolor=ORANGE, linewidth=2)
axL.add_patch(scramble_box)
axL.text(5.0, 9.10, 'Team scrambles',
         ha='center', va='center', fontsize=11, color=ORANGE, fontweight='bold')
axL.text(5.0, 8.75, 'searches Jira tickets, Slack threads, email archives,',
         ha='center', va='center', fontsize=9, color=SILVER)
axL.text(5.0, 8.45, 'screenshots, calendar invites, vault audit logs,',
         ha='center', va='center', fontsize=9, color=SILVER)
axL.text(5.0, 8.15, 'cron logs, manual spreadsheets...',
         ha='center', va='center', fontsize=9, color=SILVER)
axL.text(5.0, 7.80, 'over multiple weeks',
         ha='center', va='center', fontsize=9, color=RED, fontweight='bold')

# Scattered evidence sources
sources_y = 6.5
sources = [
    ('Jira',     1.3, BLUE),
    ('Slack',    2.7, PURPLE),
    ('email',    4.1, CYAN),
    ('screenshots', 5.5, ORANGE),
    ('cron logs', 7.0, GOLD),
    ('vault logs', 8.5, MAG),
]
for s, x, color in sources:
    box = FancyBboxPatch((x - 0.55, sources_y - 0.30), 1.1, 0.60,
                         boxstyle='round,pad=0.04',
                         facecolor=PAN, edgecolor=color, linewidth=1.2)
    axL.add_patch(box)
    axL.text(x, sources_y, s, ha='center', va='center',
             fontsize=8.5, color=color, fontweight='bold')

# Arrow down to binder
axL.annotate('', xy=(5.0, 5.3), xytext=(5.0, 6.0),
             arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.5))

# Binder
binder_box = FancyBboxPatch((2.0, 3.0), 6.0, 2.1,
                            boxstyle='round,pad=0.1',
                            facecolor=PAN, edgecolor=GOLD, linewidth=2)
axL.add_patch(binder_box)
axL.text(5.0, 4.65, 'Binder assembled',
         ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold')
axL.text(5.0, 4.30, 'evidence is screenshots,',
         ha='center', va='center', fontsize=9, color=SILVER)
axL.text(5.0, 4.05, 'pasted ticket links,',
         ha='center', va='center', fontsize=9, color=SILVER)
axL.text(5.0, 3.80, 'narrative descriptions',
         ha='center', va='center', fontsize=9, color=SILVER)
axL.text(5.0, 3.40, 'auditor accepts on faith,',
         ha='center', va='center', fontsize=8.5, color=DIM, style='italic')
axL.text(5.0, 3.15, 'samples a few items',
         ha='center', va='center', fontsize=8.5, color=DIM, style='italic')

# Outcome
out_box_L = FancyBboxPatch((1.0, 0.30), 8.0, 2.2,
                           boxstyle='round,pad=0.1',
                           facecolor=RED, edgecolor=RED, linewidth=2, alpha=0.20)
axL.add_patch(out_box_L)
axL.text(5.0, 2.05, 'Audit is a quarterly project',
         ha='center', va='center', fontsize=10.5, color=RED, fontweight='bold')
axL.text(5.0, 1.65,
         '"we promise we have controls" backed by',
         ha='center', va='center', fontsize=9, color=WHITE)
axL.text(5.0, 1.35,
         'documentation about the controls',
         ha='center', va='center', fontsize=9, color=WHITE)
axL.text(5.0, 0.85,
         'cost grows with org size; trust never fully verifiable',
         ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')

# --- RIGHT PANEL: After ---
axR.set_title('AFTER: auditor queries directly',
              color=GREEN, fontsize=14, fontweight='bold', pad=12)

# Auditor at top
aud_box_R = FancyBboxPatch((3.5, 10.4), 3.0, 1.2,
                           boxstyle='round,pad=0.1',
                           facecolor=PAN, edgecolor=PURPLE, linewidth=2.5)
axR.add_patch(aud_box_R)
axR.text(5.0, 11.20, 'Auditor', ha='center', va='center',
         fontsize=11, color=PURPLE, fontweight='bold')
axR.text(5.0, 10.80, 'read-only OpsDB access', ha='center', va='center',
         fontsize=9, color=SILVER, style='italic')
axR.text(5.0, 10.55, '(scoped role)',
         ha='center', va='center', fontsize=8.5, color=WHITE)

# Arrow to query
axR.annotate('', xy=(5.0, 9.4), xytext=(5.0, 10.4),
             arrowprops=dict(arrowstyle='->', color=GOLD, lw=2))

# Query box
query_box_R = FancyBboxPatch((1.0, 7.8), 8.0, 1.6,
                             boxstyle='round,pad=0.1',
                             facecolor=PAN, edgecolor=GOLD, linewidth=2.5)
axR.add_patch(query_box_R)
axR.text(5.0, 9.05, 'SEARCH evidence_record',
         ha='center', va='center', fontsize=11, color=GOLD,
         fontweight='bold', fontfamily='monospace')
axR.text(5.0, 8.65, 'WHERE evidence_record_type = \'access_review\'',
         ha='center', va='center', fontsize=9, color=WHITE,
         fontfamily='monospace')
axR.text(5.0, 8.35, 'AND observed_time BETWEEN Q3_start AND Q3_end',
         ha='center', va='center', fontsize=9, color=WHITE,
         fontfamily='monospace')
axR.text(5.0, 8.00, 'view_mode = with_history',
         ha='center', va='center', fontsize=9, color=WHITE,
         fontfamily='monospace')

# Arrow to structured result
axR.annotate('', xy=(5.0, 7.2), xytext=(5.0, 7.8),
             arrowprops=dict(arrowstyle='->', color=GOLD, lw=2))

# Structured result
results_box = FancyBboxPatch((1.0, 3.5), 8.0, 3.6,
                             boxstyle='round,pad=0.1',
                             facecolor=PAN, edgecolor=GREEN, linewidth=2)
axR.add_patch(results_box)
axR.text(5.0, 6.80, 'Structured result',
         ha='center', va='center', fontsize=11, color=GREEN, fontweight='bold')

# Result rows
result_rows_y = 6.30
result_rows = [
    'evidence_record #4471 - access_review_q3_eng - PASS - alice@team',
    'evidence_record #4472 - access_review_q3_finance - PASS - bob@team',
    'evidence_record #4473 - access_review_q3_security - PASS - carol@team',
    'evidence_record #4474 - access_review_q3_admin - PASS - dave@team',
    'evidence_record #4475 - access_review_q3_data - WARN - 2 stale users',
]
for i, row in enumerate(result_rows):
    y = result_rows_y - i * 0.45
    axR.text(5.0, y, row, ha='center', va='center',
             fontsize=8.5, color=WHITE, fontfamily='monospace')

axR.text(5.0, 3.85,
         '+ change_set joins, audit_log joins, version history',
         ha='center', va='center', fontsize=8, color=SILVER, style='italic')

# Outcome
out_box_R = FancyBboxPatch((1.0, 0.30), 8.0, 2.7,
                           boxstyle='round,pad=0.1',
                           facecolor=GREEN, edgecolor=GREEN, linewidth=2, alpha=0.20)
axR.add_patch(out_box_R)
axR.text(5.0, 2.55, 'Audit is verification of mechanism',
         ha='center', va='center', fontsize=10.5, color=GREEN, fontweight='bold')
axR.text(5.0, 2.15,
         'Auditor sees what the team sees.',
         ha='center', va='center', fontsize=9, color=WHITE)
axR.text(5.0, 1.85,
         'Same data, same vocabulary.',
         ha='center', va='center', fontsize=9, color=WHITE)
axR.text(5.0, 1.40,
         'No translation between operational language and audit language.',
         ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')
axR.text(5.0, 1.00,
         'Cost is constant regardless of org size; trust is mechanical.',
         ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')
axR.text(5.0, 0.55,
         'Findings file change_sets through the same pipeline.',
         ha='center', va='center', fontsize=8, color=DIM, style='italic')

for ax in (axL, axR):
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.suptitle('Compliance Evidence Collection: Before vs After\n'
             'The largest workflow change in many organizations',
             color=GOLD, fontsize=15, fontweight='bold', y=0.99)

save(fig, 'infra7_05_audit_before_after.png')


# ================================================================
# FIG 6: CONTINUOUS COMPLIANCE VS PERIODIC AUDIT
# Type: 1 (Running chart)
# Shows: shape difference - flat continuous evidence accumulation
#        vs spiky periodic audit projects.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 10), facecolor=BG)
style_axes(ax)

# X-axis: 12 months
months = np.arange(0, 12.01, 0.05)
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# --- BEFORE: spiky quarterly audit projects ---
# Most of the year very low activity, big spikes near quarter-end audit deadlines
before = np.zeros_like(months)
# Background level
before += 5 + 2 * np.sin(months * 0.5)
# Quarterly spikes - audit prep before quarter end
audit_centers = [3.0, 6.0, 9.0, 12.0]
for c in audit_centers:
    spike = 80 * np.exp(-((months - c + 0.4) / 0.35) ** 2)
    before += spike

# --- AFTER: continuous evidence accumulation ---
# Flat baseline of evidence_record writes throughout the year
# Rising slowly as more domains and runners come online
after = 25 + 1.5 * months + 3 * np.sin(months * 2) + 1 * np.cos(months * 4)

# Plot the lines
ax.plot(months, before, color=RED, linewidth=2.8, alpha=0.9,
        label='BEFORE: periodic audit projects')
ax.fill_between(months, 0, before, color=RED, alpha=0.10)

ax.plot(months, after, color=GREEN, linewidth=2.8, alpha=0.9,
        label='AFTER: continuous evidence accumulation')
ax.fill_between(months, 0, after, color=GREEN, alpha=0.10)

# Annotate spikes
for i, c in enumerate(audit_centers):
    label_y = 88
    ax.annotate('audit Q%d' % (i + 1),
                xy=(c - 0.4, 75),
                xytext=(c - 0.4, label_y),
                fontsize=9, color=RED, fontweight='bold',
                ha='center',
                arrowprops=dict(arrowstyle='->', color=RED, lw=1, alpha=0.6))

# Annotate the continuous line
ax.annotate('every cycle of every verifier runner',
            xy=(7.0, 41), xytext=(7.0, 60),
            fontsize=10, color=GREEN, fontweight='bold',
            ha='center',
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                      edgecolor=GREEN, linewidth=1))

ax.annotate('binder assembly\n(weeks of work)',
            xy=(3.0, 75), xytext=(1.5, 60),
            fontsize=9, color=RED, fontweight='bold',
            ha='center',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1, alpha=0.7),
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                      edgecolor=RED, linewidth=1))

# Axes
ax.set_xticks(np.arange(0.5, 12.5, 1))
ax.set_xticklabels(month_labels, fontsize=10, color=SILVER)
ax.set_xlim(-0.2, 12.2)
ax.set_ylim(0, 105)

ax.set_xlabel('time (one year)', color=SILVER, fontsize=11)
ax.set_ylabel('evidence-related work volume (relative units)',
              color=SILVER, fontsize=11)

# Vertical lines at quarter ends
for c in audit_centers:
    ax.axvline(x=c, color=DIM, linewidth=0.7, linestyle=':', alpha=0.4)

# Legend
legend = ax.legend(loc='upper left', facecolor=PAN, edgecolor=DIM,
                   labelcolor=WHITE, fontsize=10.5, framealpha=0.9)

# Bottom annotation
ax.text(6.0, -12, 'Same total compliance work; very different shape.',
        ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold',
        clip_on=False)
ax.text(6.0, -16,
        'Continuous evidence is a property of the system, not a project the team executes four times a year.',
        ha='center', va='center', fontsize=9.5, color=SILVER, style='italic',
        clip_on=False)

ax.set_title('Continuous Compliance vs Periodic Audit\n'
             'The shape difference is the finding',
             color=GOLD, fontsize=16, fontweight='bold', pad=15)

save(fig, 'infra7_06_continuous_vs_periodic.png')


# ================================================================
# FIG 7: THE COMPOUNDING BENEFITS GRAPH
# Type: 5 (Connection Map)
# Shows: how each capability strengthens the others; none stand alone.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 13), facecolor=BG)
ax.set_facecolor(BG)

# Capabilities and commitments arranged so that arrows show which enables/requires which.
# Layout: cause-on-left, effect-on-right roughly, but with cross-connections to show
# the compounding nature.

capabilities = {
    'closed_vocab':    (1.5, 11.5, 'Closed schema\nvocabulary',         GOLD,   2.6, 1.2),
    'no_outofband':    (1.5, 8.5,  'No out-of-band\npaths',             ORANGE, 2.6, 1.2),
    'one_gate':        (1.5, 5.5,  'Single API gate',                   GOLD,   2.6, 1.0),
    'one_substrate':   (1.5, 2.5,  'Single substrate',                  GOLD,   2.6, 1.0),

    'schema_stable':   (6.5, 11.5, 'Schema stable\nacross decades',     CYAN,   2.6, 1.2),
    'gate_uniform':    (6.5, 8.5,  'Gate enforcement\nis uniform',      CYAN,   2.6, 1.2),
    'every_action':    (6.5, 5.5,  'Every action\nattributable',        CYAN,   2.6, 1.2),
    'data_one_place':  (6.5, 2.5,  'Operational data\nin one place',    CYAN,   2.6, 1.2),

    'simple_consumers':(11.5, 11.0,'Consumers stay\nsimple',            GREEN,  2.6, 1.2),
    'mechanical_govern':(11.5,8.0, 'Mechanical\nchange governance',     GREEN,  2.8, 1.2),
    'continuous_audit':(11.5, 5.0, 'Continuous\nqueryable audit',       GREEN,  2.6, 1.2),
    'one_directory':   (11.5, 2.0, 'One directory\nfor every fact',     GREEN,  2.6, 1.2),

    'comprehensive':   (16.0, 8.0, 'Comprehensive\noperational coverage', GOLD, 3.0, 1.5),
    'replaceable_logic':(16.0,4.0, 'Replaceable logic\nover stable data', GOLD, 3.0, 1.5),
}

# Draw boxes
node_positions = {}
for key, (x, y, label, color, w, h) in capabilities.items():
    node_positions[key] = (x, y, w, h)
    is_anchor = key in ('comprehensive', 'replaceable_logic')
    edge_w = 2.5 if is_anchor else 1.6

    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle='round,pad=0.07',
                         facecolor=PAN, edgecolor=color, linewidth=edge_w,
                         zorder=5)
    ax.add_patch(box)
    ax.text(x, y, label, ha='center', va='center',
            fontsize=9.5 if is_anchor else 9, color=color, fontweight='bold',
            zorder=6)

# Compounding edges (cause -> effect)
edges = [
    # Closed vocabulary -> schema stable
    ('closed_vocab', 'schema_stable', GOLD, 'enables'),
    # Schema stable -> simple consumers
    ('schema_stable', 'simple_consumers', CYAN, 'enables'),
    # Simple consumers -> comprehensive coverage
    ('simple_consumers', 'comprehensive', GREEN, 'enables'),

    # No out-of-band -> gate uniform
    ('no_outofband', 'gate_uniform', ORANGE, 'enforces'),
    # Gate uniform -> mechanical govern
    ('gate_uniform', 'mechanical_govern', CYAN, 'enables'),
    # Mechanical govern -> continuous audit
    ('mechanical_govern', 'continuous_audit', GREEN, 'enables'),
    # Continuous audit -> comprehensive coverage
    ('continuous_audit', 'comprehensive', GREEN, 'reinforces'),

    # One gate -> every action attributable
    ('one_gate', 'every_action', GOLD, 'produces'),
    # Every action -> continuous audit
    ('every_action', 'continuous_audit', CYAN, 'feeds'),
    # Every action -> mechanical govern
    ('every_action', 'mechanical_govern', CYAN, 'feeds'),

    # One substrate -> data in one place
    ('one_substrate', 'data_one_place', GOLD, 'requires'),
    # Data in one place -> one directory
    ('data_one_place', 'one_directory', CYAN, 'enables'),
    # One directory -> replaceable logic
    ('one_directory', 'replaceable_logic', GREEN, 'supports'),
    # Schema stable -> replaceable logic
    ('schema_stable', 'replaceable_logic', CYAN, 'enables'),

    # Closed vocab -> gate uniform (vocab makes gate validation deterministic)
    ('closed_vocab', 'gate_uniform', GOLD, 'bounds'),
    # Simple consumers -> mechanical govern
    ('simple_consumers', 'mechanical_govern', GREEN, 'serves'),
    # Comprehensive coverage -> back-arrow to one substrate (closes loop)
]


def draw_edge(src, dst, color, label='', curve=0.0, lw=1.4, alpha=0.55):
    sx, sy, sw, sh = node_positions[src]
    dx, dy, dw, dh = node_positions[dst]

    # Compute edge endpoints on the boxes
    # Pick the side closest to the destination
    px = dx - sx
    py = dy - sy
    if abs(px) > abs(py):
        if px > 0:
            x1 = sx + sw / 2
            x2 = dx - dw / 2
        else:
            x1 = sx - sw / 2
            x2 = dx + dw / 2
        y1 = sy
        y2 = dy
    else:
        if py > 0:
            y1 = sy + sh / 2
            y2 = dy - dh / 2
        else:
            y1 = sy - sh / 2
            y2 = dy + dh / 2
        x1 = sx
        x2 = dx

    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle='->', color=color,
                            linewidth=lw, alpha=alpha,
                            connectionstyle='arc3,rad=%f' % curve,
                            mutation_scale=14, zorder=3)
    ax.add_patch(arrow)


for src, dst, color, label in edges:
    draw_edge(src, dst, color, label)

# Annotation at the top
ax.text(9.5, 13.3,
        'Each commitment supports the next.',
        ha='center', va='center', fontsize=13, color=GOLD, fontweight='bold')
ax.text(9.5, 12.85,
        'None of the benefits stand alone.',
        ha='center', va='center', fontsize=11, color=SILVER, style='italic')

# Bottom annotation
ax.text(9.5, 0.4,
        'Three columns: structural commitments -> intermediate properties -> operational consequences.',
        ha='center', va='center', fontsize=10, color=DIM, style='italic')
ax.text(9.5, 0.0,
        'Every commitment is what makes the next one mechanically possible.',
        ha='center', va='center', fontsize=10, color=SILVER, style='italic')

# Column labels
ax.text(1.5, 13.0, 'commitments', ha='center', va='center',
        fontsize=10, color=GOLD, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor=BG, edgecolor=GOLD,
                  linewidth=1))
ax.text(6.5, 13.0, 'enabled by', ha='center', va='center',
        fontsize=10, color=CYAN, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor=BG, edgecolor=CYAN,
                  linewidth=1))
ax.text(11.5, 13.0, 'consequences', ha='center', va='center',
        fontsize=10, color=GREEN, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor=BG, edgecolor=GREEN,
                  linewidth=1))
ax.text(16.0, 13.0, 'compound result', ha='center', va='center',
        fontsize=10, color=GOLD, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor=BG, edgecolor=GOLD,
                  linewidth=1))

ax.set_xlim(-0.5, 18.0)
ax.set_ylim(-0.5, 14.0)
ax.set_aspect('auto')
ax.axis('off')
ax.set_title('The Compounding Benefits Graph\n'
             'Architectural commitments -> mechanical consequences -> compound result',
             color=GOLD, fontsize=16, fontweight='bold', pad=12)

save(fig, 'infra7_07_compounding_benefits.png')


# ================================================================
# FIG 8: DRIFT LIFECYCLE: WITHOUT AND WITH OPSDB
# Type: 1 (Running chart) x 2
# Shows: time-to-detection collapse - without: months silent; with:
#        within one detector cycle.
# ================================================================

fig, (axT, axB) = plt.subplots(2, 1, figsize=(18, 11),
                                facecolor=BG, gridspec_kw={'hspace': 0.45})

style_axes(axT)
style_axes(axB)

# Common time axis: 0 to 180 days
days = np.linspace(0, 180, 1000)

# --- TOP PANEL: WITHOUT OpsDB ---
# Drift introduced at day 5; nobody notices; finally discovered at day 142
# (during an incident). State of "drift present and undetected" rises sharply
# at introduction and stays high until incident reveals it.

without = np.zeros_like(days)
# Drift introduced day 5
intro_day = 5
without += 1.0 * (days >= intro_day)
# Drift remains undetected
# At incident_day, drift is suddenly noticed
incident_day = 142
remediation_day = 148

# We'll plot "drift severity present in production":
# 0 before introduction, 1.0 from introduction onward, drops at remediation_day
without_severity = np.zeros_like(days)
without_severity[(days >= intro_day) & (days < remediation_day)] = 1.0
without_severity[(days >= remediation_day) & (days < remediation_day + 5)] = \
    1.0 - (days[(days >= remediation_day) & (days < remediation_day + 5)] - remediation_day) / 5.0

axT.fill_between(days, 0, without_severity, color=RED, alpha=0.25, zorder=2)
axT.plot(days, without_severity, color=RED, linewidth=2.5, zorder=3)

# Annotate introduction
axT.annotate('drift introduced',
             xy=(intro_day, 1.0), xytext=(intro_day + 8, 1.20),
             fontsize=10, color=ORANGE, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                       edgecolor=ORANGE, linewidth=1))

# Annotate the silent period
axT.annotate('drift undetected for 137 days',
             xy=(75, 1.0), xytext=(75, 0.55),
             fontsize=10.5, color=RED, fontweight='bold',
             ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                       edgecolor=RED, linewidth=1.5))
axT.text(75, 0.30,
         'no detector. no audit catches it. nobody knows.',
         ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# Annotate incident discovery
axT.annotate('discovered\nduring an incident',
             xy=(incident_day, 1.0), xytext=(incident_day - 10, 1.30),
             fontsize=10, color=RED, fontweight='bold',
             ha='center',
             arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                       edgecolor=RED, linewidth=1.2))

# Annotate remediation
axT.annotate('remediated',
             xy=(remediation_day, 0.5), xytext=(remediation_day + 12, 0.85),
             fontsize=9, color=GREEN, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.2))

axT.set_xlim(-3, 183)
axT.set_ylim(-0.05, 1.55)
axT.set_xticks([0, 30, 60, 90, 120, 150, 180])
axT.set_xticklabels(['day 0', 'day 30', 'day 60', 'day 90',
                     'day 120', 'day 150', 'day 180'],
                    fontsize=10, color=SILVER)
axT.set_yticks([0, 0.5, 1.0])
axT.set_yticklabels(['none', 'partial', 'full'], color=SILVER)
axT.set_ylabel('drift in production', color=SILVER, fontsize=10)

axT.set_title('WITHOUT OpsDB - drift accumulates silently for months',
              color=RED, fontsize=13, fontweight='bold', pad=10)

# --- BOTTOM PANEL: WITH OpsDB ---
# Drift introduced at day 5; detector runs every cycle (e.g., every 4 hours).
# Detected within one cycle. Either auto-corrected or finding filed within hours.

with_severity = np.zeros_like(days)
intro_day_b = 5
detector_cycle_hours = 4
detection_day = intro_day_b + detector_cycle_hours / 24.0
remediation_day_b = detection_day + 8 / 24.0  # 8 hours later, change_set applied

with_severity[(days >= intro_day_b) & (days < detection_day)] = 1.0
# Brief detected-but-not-yet-corrected window
mask_detected = (days >= detection_day) & (days < remediation_day_b)
with_severity[mask_detected] = 1.0 - (days[mask_detected] - detection_day) / \
    (remediation_day_b - detection_day)
# After remediation: zero
with_severity[days >= remediation_day_b] = 0.0

axB.fill_between(days, 0, with_severity, color=GREEN, alpha=0.25, zorder=2)
axB.plot(days, with_severity, color=GREEN, linewidth=2.5, zorder=3)

# Detector cycle markers (every 4 hours = every 1/6 day, but we show
# them only as conceptual ticks at the start to avoid clutter)
detector_ticks = np.arange(intro_day_b, intro_day_b + 3, detector_cycle_hours / 24.0)
for t in detector_ticks:
    axB.axvline(x=t, color=CYAN, linewidth=0.5, linestyle=':', alpha=0.4)

# Annotate introduction
axB.annotate('drift introduced',
             xy=(intro_day_b, 1.0), xytext=(intro_day_b + 5, 1.30),
             fontsize=10, color=ORANGE, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                       edgecolor=ORANGE, linewidth=1))

# Annotate detection
axB.annotate('detected within\none detector cycle',
             xy=(detection_day, 1.0), xytext=(detection_day + 18, 1.30),
             fontsize=10, color=CYAN, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=CYAN, lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                       edgecolor=CYAN, linewidth=1))

# Annotate remediation
axB.annotate('change_set applied,\ndrift corrected',
             xy=(remediation_day_b, 0.3), xytext=(remediation_day_b + 12, 0.75),
             fontsize=10, color=GREEN, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                       edgecolor=GREEN, linewidth=1))

# Annotate the long flat zero region: continuous drift detection
axB.text(100, 0.55,
         'drift detector runs continuously',
         ha='center', va='center', fontsize=11, color=GREEN, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                   edgecolor=GREEN, linewidth=1.5))
axB.text(100, 0.30,
         'every cycle: read desired, read observed, diff, propose change_set',
         ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# Show detector cycles continuing throughout the period
later_ticks = np.arange(20, 180, 30)  # symbolic, not literal cycle interval
for t in later_ticks:
    axB.axvline(x=t, color=CYAN, linewidth=0.4, linestyle=':', alpha=0.3)

axB.set_xlim(-3, 183)
axB.set_ylim(-0.05, 1.55)
axB.set_xticks([0, 30, 60, 90, 120, 150, 180])
axB.set_xticklabels(['day 0', 'day 30', 'day 60', 'day 90',
                     'day 120', 'day 150', 'day 180'],
                    fontsize=10, color=SILVER)
axB.set_yticks([0, 0.5, 1.0])
axB.set_yticklabels(['none', 'partial', 'full'], color=SILVER)
axB.set_ylabel('drift in production', color=SILVER, fontsize=10)
axB.set_xlabel('time since drift introduction', color=SILVER, fontsize=10)

axB.set_title('WITH OpsDB - drift detected within one cycle and corrected within hours',
              color=GREEN, fontsize=13, fontweight='bold', pad=10)

fig.suptitle('Drift Lifecycle: Without and With OpsDB\n'
             'Same drift event; very different time-to-detection',
             color=GOLD, fontsize=15, fontweight='bold', y=0.99)

save(fig, 'infra7_08_drift_lifecycle.png')


# ================================================================
# SUMMARY
# ================================================================

print("\n" + "=" * 60)
print("OPSDB-1 diagram script complete")
print("=" * 60)
print("Files written to: %s" % outdir)
print()
print("  infra7_01_fragmented_operations.png")
print("  infra7_02_opsdb_architecture.png")
print("  infra7_03_comprehensive_scope.png")
print("  infra7_04_investigation_before_after.png")
print("  infra7_05_audit_before_after.png")
print("  infra7_06_continuous_vs_periodic.png")
print("  infra7_07_compounding_benefits.png")
print("  infra7_08_drift_lifecycle.png")
