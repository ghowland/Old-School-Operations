#!/usr/bin/env python3
"""
HOWL OPSDB-8 Diagrams - The Shared Library Suite
8 figures covering two-sided policy enforcement, the library/runner boundary,
denial paths, library/mechanism mapping, evolution, cross-implementation,
runner anatomy, and the API client lifecycle.
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
# FIG 1: TWO-SIDED POLICY ENFORCEMENT
# Type: 4 (Geometric Cross-Section)
# Shows: runner declarations gate both OpsDB writes (API gate) and
#        world-side actions (library suite); same input, two surfaces,
#        comprehensive coverage.
# ================================================================

fig, ax = plt.subplots(figsize=(20, 13), facecolor=BG)
ax.set_facecolor(BG)

# Runner at top center
runner_x, runner_y = 10, 10.5
runner_box = FancyBboxPatch((runner_x - 2.5, runner_y - 0.9), 5.0, 1.8,
                            boxstyle='round,pad=0.1',
                            facecolor=PAN, edgecolor=ORANGE, linewidth=2.5)
ax.add_patch(runner_box)
ax.text(runner_x, runner_y + 0.45, 'runner_spec_v3.1',
        ha='center', va='center', fontsize=12, color=ORANGE, fontweight='bold')
ax.text(runner_x, runner_y + 0.05, 'k8s_pvc_repair',
        ha='center', va='center', fontsize=10, color=WHITE,
        fontfamily='monospace')
ax.text(runner_x, runner_y - 0.40, 'wants to perform an action',
        ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# Runner declarations - shown as a row of boxes below the runner
decl_y = 8.3
declarations = [
    ('runner_*_target',     'k8s_namespace=prod_a',     CYAN,    3.0),
    ('runner_capability',   'k8s_apply, secret_read',   PURPLE,  7.0),
    ('runner_report_key',   'metric=pvc_repair_count',  GOLD,   11.0),
    ('runner_*_target',     'cloud_account=prod_aws',   CYAN,   15.0),
    ('runner_capability',   'cloud_provision',          PURPLE, 19.0),
]

# Box around all declarations
decl_bg = FancyBboxPatch((1.5, decl_y - 0.65), 19.0, 1.30,
                        boxstyle='round,pad=0.05',
                        facecolor=PAN, edgecolor=GOLD, linewidth=1.5,
                        alpha=0.5)
ax.add_patch(decl_bg)
ax.text(10.5, decl_y + 0.85, 'Runner declarations (OpsDB rows)',
        ha='center', va='center', fontsize=10, color=GOLD, fontweight='bold')

decl_w = 3.4
for name, val, color, x in declarations:
    box = FancyBboxPatch((x - decl_w/2, decl_y - 0.45), decl_w, 0.90,
                        boxstyle='round,pad=0.04',
                        facecolor=PAN, edgecolor=color, linewidth=1.3)
    ax.add_patch(box)
    ax.text(x, decl_y + 0.18, name, ha='center', va='center',
            fontsize=8, color=color, fontweight='bold')
    ax.text(x, decl_y - 0.20, val, ha='center', va='center',
            fontsize=7.5, color=WHITE, fontfamily='monospace')

# Arrow from runner down through declarations
ax.annotate('', xy=(10.5, decl_y + 0.65), xytext=(10.0, runner_y - 0.9),
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.8))
ax.text(11.5, 9.3, 'declares', ha='left', va='center',
        fontsize=9, color=ORANGE, style='italic')

# Now the runner's actions split into two paths
# Left path: OpsDB writes
# Right path: world-side actions

# Action labels
ax.text(5.5, 6.9, 'OpsDB write', ha='center', va='center',
        fontsize=11, color=WHITE, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=GOLD,
                  linewidth=1.2))
ax.text(15.0, 6.9, 'World-side action', ha='center', va='center',
        fontsize=11, color=WHITE, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=GOLD,
                  linewidth=1.2))

# Arrows from declarations down to gate / library
ax.annotate('', xy=(5.5, 6.55), xytext=(7.0, decl_y - 0.65),
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.5, alpha=0.7))
ax.annotate('', xy=(15.0, 6.55), xytext=(15.0, decl_y - 0.65),
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.5, alpha=0.7))

# LEFT: API Gate
gate_box = FancyBboxPatch((1.5, 4.0), 8.0, 2.4,
                          boxstyle='round,pad=0.1',
                          facecolor=PAN, edgecolor=GOLD, linewidth=2.5)
ax.add_patch(gate_box)
ax.text(5.5, 5.95, 'OpsDB API Gate (OPSDB-6)',
        ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold')
ax.text(5.5, 5.55, '10-step gate sequence',
        ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# Gate steps as small dots
gate_steps = ['auth', 'authz', 'schema', 'bound', 'policy', 'version',
              'route', 'audit', 'execute', 'respond']
for i, step in enumerate(gate_steps):
    sx = 2.0 + i * 0.75
    dot = Circle((sx, 4.95), 0.10, facecolor=GOLD, edgecolor=GOLD)
    ax.add_patch(dot)
    ax.text(sx, 4.55, step, ha='center', va='center',
            fontsize=6.5, color=DIM, rotation=0)

# Inside-the-gate text on report keys
ax.text(5.5, 4.20, 'runner_report_key gates writable surface',
        ha='center', va='center', fontsize=8.5, color=GOLD,
        fontfamily='monospace')

# RIGHT: Library Suite
lib_box = FancyBboxPatch((10.5, 4.0), 8.0, 2.4,
                        boxstyle='round,pad=0.1',
                        facecolor=PAN, edgecolor=GOLD, linewidth=2.5)
ax.add_patch(lib_box)
ax.text(14.5, 5.95, 'Library Suite (OPSDB-8)',
        ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold')
ax.text(14.5, 5.55, 'each library validates declared scope',
        ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# Libraries as small dots
libraries_list = ['k8s', 'cloud', 'host', 'secret', 'identity',
                  'monitoring', 'notify', 'registry']
for i, lib in enumerate(libraries_list):
    sx = 11.0 + i * 0.95
    dot = Circle((sx, 4.95), 0.10, facecolor=GOLD, edgecolor=GOLD)
    ax.add_patch(dot)
    ax.text(sx, 4.55, lib, ha='center', va='center',
            fontsize=6.5, color=DIM)

ax.text(14.5, 4.20, 'runner_*_target gates world-side actions',
        ha='center', va='center', fontsize=8.5, color=GOLD,
        fontfamily='monospace')

# Outcomes - both fail closed, both audit-logged
outcomes_y = 2.4

# Left outcome
out_left = FancyBboxPatch((1.5, outcomes_y - 0.55), 8.0, 1.10,
                          boxstyle='round,pad=0.05',
                          facecolor=GREEN, edgecolor=GREEN, linewidth=2,
                          alpha=0.20)
ax.add_patch(out_left)
ax.text(5.5, outcomes_y + 0.20,
        'IF declared: write committed; audit_log_entry recorded',
        ha='center', va='center', fontsize=9, color=WHITE)
ax.text(5.5, outcomes_y - 0.20,
        'IF undeclared: undeclared_report_key rejection; audited',
        ha='center', va='center', fontsize=9, color=WHITE)

# Right outcome
out_right = FancyBboxPatch((10.5, outcomes_y - 0.55), 8.0, 1.10,
                          boxstyle='round,pad=0.05',
                          facecolor=GREEN, edgecolor=GREEN, linewidth=2,
                          alpha=0.20)
ax.add_patch(out_right)
ax.text(14.5, outcomes_y + 0.20,
        'IF declared: world-side call proceeds; observed and metered',
        ha='center', va='center', fontsize=9, color=WHITE)
ax.text(14.5, outcomes_y - 0.20,
        'IF undeclared: library_authorization_denied; logged',
        ha='center', va='center', fontsize=9, color=WHITE)

# Arrows from gate/library to outcomes
ax.annotate('', xy=(5.5, outcomes_y + 0.6), xytext=(5.5, 4.0),
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5, alpha=0.6))
ax.annotate('', xy=(14.5, outcomes_y + 0.6), xytext=(14.5, 4.0),
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5, alpha=0.6))

# Bottom synthesis - arrows converging to "trail"
trail_y = 0.55
trail_box = FancyBboxPatch((6.0, trail_y - 0.45), 9.0, 0.95,
                          boxstyle='round,pad=0.1',
                          facecolor=PAN, edgecolor=GOLD, linewidth=2.5)
ax.add_patch(trail_box)
ax.text(10.5, trail_y + 0.12,
        'One trail. Both surfaces. Same declarations.',
        ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold')
ax.text(10.5, trail_y - 0.22,
        'Runner cannot perform any action outside its declared scope.',
        ha='center', va='center', fontsize=9, color=SILVER, style='italic')

ax.annotate('', xy=(8.5, trail_y + 0.5), xytext=(5.5, outcomes_y - 0.55),
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.4, alpha=0.6))
ax.annotate('', xy=(12.5, trail_y + 0.5), xytext=(14.5, outcomes_y - 0.55),
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.4, alpha=0.6))

ax.set_xlim(0.5, 21.5)
ax.set_ylim(-0.1, 12.0)
ax.set_aspect('auto')
ax.axis('off')
ax.set_title('Two-Sided Policy Enforcement\n'
             'Same declarations gate both OpsDB writes (left) and world-side actions (right)',
             color=GOLD, fontsize=16, fontweight='bold', pad=14)

save(fig, 'infra8_01_two_sided_enforcement.png')


# ================================================================
# FIG 2: THE LIBRARY/RUNNER BOUNDARY
# Type: 4 (Geometric Cross-Section)
# Shows: where the line is drawn and why; runner-specific decision
#        logic above, library calls below.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 13), facecolor=BG)
ax.set_facecolor(BG)

# Two-zone background
runner_zone = Rectangle((1.0, 7.5), 16.0, 4.5, facecolor=ORANGE,
                       alpha=0.06, zorder=1)
ax.add_patch(runner_zone)
library_zone = Rectangle((1.0, 0.5), 16.0, 6.7, facecolor=BLUE,
                        alpha=0.06, zorder=1)
ax.add_patch(library_zone)

# Zone labels
ax.text(0.4, 9.7, 'RUNNER\nZONE', ha='center', va='center',
        fontsize=12, color=ORANGE, fontweight='bold', rotation=90)
ax.text(0.4, 3.85, 'LIBRARY\nZONE', ha='center', va='center',
        fontsize=12, color=BLUE, fontweight='bold', rotation=90)

# Boundary line with label
ax.axhline(y=7.35, xmin=0.06, xmax=0.96, color=GOLD, linewidth=2,
           linestyle='--', zorder=3)
ax.text(9.0, 7.35, 'the boundary',
        ha='center', va='center', fontsize=10, color=GOLD,
        fontweight='bold', style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                  edgecolor=GOLD, linewidth=1.5))

# Runner-zone content (top) - runner-specific decision logic
ax.text(9.0, 11.5, 'runner-specific decision logic',
        ha='center', va='center', fontsize=11, color=ORANGE,
        fontweight='bold', style='italic')

runner_logic = [
    (3.5, 10.5, 'select PVCs in\nattention-worthy state'),
    (9.0, 10.5, 'compute repair kind\n(rebind/resize/replace)'),
    (14.5, 10.5, 'construct repair manifest\nspecific to PVC'),
    (5.5, 8.7, 'decide auto-correct vs\nfile finding per policy'),
    (12.5, 8.7, 'record outcome\nwith per-target detail'),
]

logic_w = 3.6
logic_h = 1.3

for lx, ly, label in runner_logic:
    box = FancyBboxPatch((lx - logic_w/2, ly - logic_h/2), logic_w, logic_h,
                        boxstyle='round,pad=0.06',
                        facecolor=PAN, edgecolor=ORANGE, linewidth=1.4)
    ax.add_patch(box)
    lines = label.split('\n')
    if len(lines) == 2:
        ax.text(lx, ly + 0.18, lines[0], ha='center', va='center',
                fontsize=8.5, color=WHITE, fontweight='bold')
        ax.text(lx, ly - 0.20, lines[1], ha='center', va='center',
                fontsize=8, color=SILVER)
    else:
        ax.text(lx, ly, label, ha='center', va='center',
                fontsize=8.5, color=WHITE, fontweight='bold')

# Library-zone content (bottom) - libraries the runner uses
ax.text(9.0, 6.6, 'shared libraries (mechanical, uniform across runner population)',
        ha='center', va='center', fontsize=11, color=BLUE,
        fontweight='bold', style='italic')

libraries = [
    (2.5, 5.0, 'opsdb.api',      'OpsDB I/O',         CYAN),
    (5.5, 5.0, 'world.k8s',      'apply, query, watch', PURPLE),
    (8.5, 5.0, 'world.cloud',    'cloud operations',   GREEN),
    (11.5, 5.0,'world.secret',   'secret backend',     MAG),
    (14.5, 5.0,'world.monitoring','metric queries',    BLUE),

    (2.5, 3.2, 'coordination.retry', 'retry+backoff', GOLD),
    (5.5, 3.2, 'coordination.breaker','circuit',     RED),
    (8.5, 3.2, 'observation.logging', 'structured logs', SILVER),
    (11.5, 3.2,'observation.metrics', 'counters/gauges', SILVER),
    (14.5, 3.2,'notification',      'pages/chat',       ORANGE),

    (5.5, 1.4, 'templating.config', 'render configs',  GREEN),
    (11.5, 1.4,'git',                'commit/push',     CYAN),
]

lib_w = 2.5
lib_h = 1.0

for lx, ly, name, sub, color in libraries:
    box = FancyBboxPatch((lx - lib_w/2, ly - lib_h/2), lib_w, lib_h,
                        boxstyle='round,pad=0.05',
                        facecolor=PAN, edgecolor=color, linewidth=1.3)
    ax.add_patch(box)
    ax.text(lx, ly + 0.18, name, ha='center', va='center',
            fontsize=8.5, color=color, fontweight='bold',
            fontfamily='monospace')
    ax.text(lx, ly - 0.20, sub, ha='center', va='center',
            fontsize=7.5, color=SILVER, style='italic')

# Lines crossing the boundary - showing what the runner calls
# (kept faint and few to avoid clutter)
crossing_calls = [
    # (runner_logic_idx_x, library_idx_xy)
    ((3.5, 10.5 - logic_h/2), (2.5, 5.0 + lib_h/2),  CYAN),    # PVC select -> opsdb.api
    ((9.0, 10.5 - logic_h/2), (5.5, 5.0 + lib_h/2),  PURPLE),  # repair kind -> k8s
    ((14.5, 10.5 - logic_h/2), (5.5, 5.0 + lib_h/2), PURPLE),  # manifest -> k8s
    ((5.5, 8.7 - logic_h/2), (2.5, 5.0 + lib_h/2),   CYAN),    # decide -> opsdb.api
    ((12.5, 8.7 - logic_h/2), (2.5, 5.0 + lib_h/2),  CYAN),    # record -> opsdb.api
    ((12.5, 8.7 - logic_h/2), (8.5, 3.2 + lib_h/2),  SILVER),  # record -> logging
]

for (sx, sy), (ex, ey), color in crossing_calls:
    ax.plot([sx, ex], [sy, ey], color=color, linewidth=0.8,
            alpha=0.40, linestyle=':', zorder=2)

# Bottom caption
ax.text(9.0, 0.0,
        'The test: would the same code appear in two runners? -> library. Specific to one runner\'s job? -> runner.',
        ha='center', va='center', fontsize=10, color=GOLD, style='italic',
        fontweight='bold')

ax.set_xlim(0, 18)
ax.set_ylim(-0.3, 12.5)
ax.set_aspect('auto')
ax.axis('off')
ax.set_title('The Library/Runner Boundary\n'
             'Decision logic above; library calls below; the line is drawn by the "two runners" test',
             color=GOLD, fontsize=16, fontweight='bold', pad=14)

save(fig, 'infra8_02_library_runner_boundary.png')


# ================================================================
# FIG 3: SAME RUNNER, TWO DENIAL PATHS
# Type: 7 (Progression) x 2 panels
# Shows: concrete demonstration of two-sided enforcement; same runner,
#        two attempts, denial at different surfaces, both audited.
# ================================================================

fig, (axL, axR) = plt.subplots(1, 2, figsize=(20, 12),
                                facecolor=BG, gridspec_kw={'wspace': 0.10})

for ax in (axL, axR):
    ax.set_facecolor(PAN)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)

# --- LEFT PANEL: API Gate denial ---
axL.set_title('Attempt A: write observation_cache_metric',
              color=RED, fontsize=13, fontweight='bold', pad=10)

# Runner box
runner_box_L = FancyBboxPatch((1.0, 12.6), 8.0, 1.1,
                              boxstyle='round,pad=0.1',
                              facecolor=PAN, edgecolor=ORANGE, linewidth=2)
axL.add_patch(runner_box_L)
axL.text(5.0, 13.32, 'k8s_pvc_repair runner',
         ha='center', va='center', fontsize=10.5, color=ORANGE,
         fontweight='bold')
axL.text(5.0, 12.95,
         'attempts: write metric_key="db_credentials_active"',
         ha='center', va='center', fontsize=8.5, color=WHITE,
         fontfamily='monospace')

axL.annotate('', xy=(5.0, 12.0), xytext=(5.0, 12.6),
             arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.5))

# Library: OpsDB API client
client_box = FancyBboxPatch((1.0, 10.6), 8.0, 1.3,
                            boxstyle='round,pad=0.1',
                            facecolor=PAN, edgecolor=CYAN, linewidth=1.6)
axL.add_patch(client_box)
axL.text(5.0, 11.45, 'opsdb.api client',
         ha='center', va='center', fontsize=10, color=CYAN, fontweight='bold')
axL.text(5.0, 11.10,
         'serializes write_observation call, attaches credentials',
         ha='center', va='center', fontsize=8, color=SILVER, style='italic')
axL.text(5.0, 10.80, 'sends to API gate',
         ha='center', va='center', fontsize=8, color=WHITE)

axL.annotate('', xy=(5.0, 10.0), xytext=(5.0, 10.6),
             arrowprops=dict(arrowstyle='->', color=CYAN, lw=1.5))

# API Gate
gate_box_L = FancyBboxPatch((1.0, 7.3), 8.0, 2.6,
                            boxstyle='round,pad=0.1',
                            facecolor=PAN, edgecolor=GOLD, linewidth=2.5)
axL.add_patch(gate_box_L)
axL.text(5.0, 9.55, 'API Gate (OPSDB-6)',
         ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold')

# Within the gate, mark which step denies
axL.text(5.0, 9.20, 'auth: PASS', ha='center', va='center',
         fontsize=8, color=GREEN, fontfamily='monospace')
axL.text(5.0, 8.95, 'authz: PASS', ha='center', va='center',
         fontsize=8, color=GREEN, fontfamily='monospace')
axL.text(5.0, 8.70, 'schema: PASS', ha='center', va='center',
         fontsize=8, color=GREEN, fontfamily='monospace')
axL.text(5.0, 8.45, 'bound: PASS', ha='center', va='center',
         fontsize=8, color=GREEN, fontfamily='monospace')
axL.text(5.0, 8.13,
         'runner_report_key check:',
         ha='center', va='center', fontsize=9, color=RED, fontweight='bold')
axL.text(5.0, 7.85,
         '"db_credentials_active" NOT in declared keys',
         ha='center', va='center', fontsize=8.5, color=RED,
         fontfamily='monospace')
axL.text(5.0, 7.55,
         'declared: pvc_repair_count, pvc_skip_count',
         ha='center', va='center', fontsize=7.5, color=SILVER,
         fontfamily='monospace')

axL.annotate('', xy=(5.0, 6.7), xytext=(5.0, 7.3),
             arrowprops=dict(arrowstyle='->', color=RED, lw=2))

# Outcome
out_box_L = FancyBboxPatch((1.0, 3.5), 8.0, 3.0,
                          boxstyle='round,pad=0.1',
                          facecolor=RED, edgecolor=RED, linewidth=2.5,
                          alpha=0.20)
axL.add_patch(out_box_L)
axL.text(5.0, 6.10, 'WRITE REJECTED',
         ha='center', va='center', fontsize=12, color=RED, fontweight='bold')
axL.text(5.0, 5.65, 'undeclared_report_key',
         ha='center', va='center', fontsize=9.5, color=WHITE,
         fontfamily='monospace')
axL.text(5.0, 5.20, 'observation_cache_metric: NO ROW WRITTEN',
         ha='center', va='center', fontsize=8.5, color=WHITE,
         fontweight='bold')
axL.text(5.0, 4.65, 'audit_log_entry written:',
         ha='center', va='center', fontsize=8.5, color=GOLD, fontweight='bold')
axL.text(5.0, 4.30,
         'action=write_rejected,',
         ha='center', va='center', fontsize=7.5, color=SILVER,
         fontfamily='monospace')
axL.text(5.0, 4.05,
         'submitted_key=db_credentials_active,',
         ha='center', va='center', fontsize=7.5, color=SILVER,
         fontfamily='monospace')
axL.text(5.0, 3.80,
         'reason=undeclared_report_key,',
         ha='center', va='center', fontsize=7.5, color=SILVER,
         fontfamily='monospace')

axL.text(5.0, 2.7, 'Surface: API gate (OPSDB-6 §8)',
         ha='center', va='center', fontsize=9.5, color=GOLD,
         fontweight='bold')
axL.text(5.0, 2.35, 'Caught at OpsDB write time',
         ha='center', va='center', fontsize=8.5, color=SILVER,
         style='italic')

# Bottom row - the audit query
audit_y = 1.1
audit_box = FancyBboxPatch((0.5, audit_y - 0.6), 9.0, 1.2,
                          boxstyle='round,pad=0.06',
                          facecolor=PAN, edgecolor=GOLD, linewidth=1.5)
axL.add_patch(audit_box)
axL.text(5.0, audit_y + 0.30,
         'queryable: SELECT * FROM audit_log_entry',
         ha='center', va='center', fontsize=9, color=GOLD,
         fontfamily='monospace')
axL.text(5.0, audit_y - 0.05,
         'WHERE acting_runner = pvc_repair AND result = "rejected"',
         ha='center', va='center', fontsize=8, color=SILVER,
         fontfamily='monospace')
axL.text(5.0, audit_y - 0.40,
         '   ORDER BY acted_time DESC LIMIT 100',
         ha='center', va='center', fontsize=8, color=SILVER,
         fontfamily='monospace')

# --- RIGHT PANEL: Library denial ---
axR.set_title('Attempt B: apply K8s manifest in undeclared namespace',
              color=RED, fontsize=13, fontweight='bold', pad=10)

# Runner box
runner_box_R = FancyBboxPatch((1.0, 12.6), 8.0, 1.1,
                              boxstyle='round,pad=0.1',
                              facecolor=PAN, edgecolor=ORANGE, linewidth=2)
axR.add_patch(runner_box_R)
axR.text(5.0, 13.32, 'k8s_pvc_repair runner',
         ha='center', va='center', fontsize=10.5, color=ORANGE,
         fontweight='bold')
axR.text(5.0, 12.95,
         'attempts: world.k8s.apply_manifest(cluster_a, ns_finance)',
         ha='center', va='center', fontsize=8.5, color=WHITE,
         fontfamily='monospace')

axR.annotate('', xy=(5.0, 12.0), xytext=(5.0, 12.6),
             arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.5))

# Library: K8s
k8s_box = FancyBboxPatch((1.0, 7.3), 8.0, 4.6,
                        boxstyle='round,pad=0.1',
                        facecolor=PAN, edgecolor=PURPLE, linewidth=2.5)
axR.add_patch(k8s_box)
axR.text(5.0, 11.55, 'opsdb.world.kubernetes',
         ha='center', va='center', fontsize=11, color=PURPLE, fontweight='bold')
axR.text(5.0, 11.20, 'before reaching the cluster, the library checks scope:',
         ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')

# Show the scope check
axR.text(5.0, 10.65, 'load runner declarations from cache',
         ha='center', va='center', fontsize=8.5, color=WHITE)
axR.text(5.0, 10.35,
         'check (cluster_a, ns_finance) against declarations:',
         ha='center', va='center', fontsize=8.5, color=WHITE)

# Declarations shown as a list
decl_y_start = 9.85
decl_items = [
    ('runner_k8s_namespace_target #1', '(cluster_a, prod_a)',  GREEN, False),
    ('runner_k8s_namespace_target #2', '(cluster_a, prod_b)',  GREEN, False),
    ('runner_k8s_namespace_target #3', '(cluster_b, staging)', GREEN, False),
]
for i, (name, val, c, _) in enumerate(decl_items):
    y = decl_y_start - i * 0.32
    axR.text(2.7, y, '-', ha='center', va='center',
             fontsize=10, color=DIM)
    axR.text(2.95, y, name, ha='left', va='center',
             fontsize=7.5, color=DIM, fontfamily='monospace')
    axR.text(6.0, y, val, ha='left', va='center',
             fontsize=7.5, color=SILVER, fontfamily='monospace')

axR.text(5.0, 8.65,
         'no declaration covers (cluster_a, ns_finance)',
         ha='center', va='center', fontsize=9, color=RED, fontweight='bold')
axR.text(5.0, 8.30,
         'library refuses BEFORE reaching the cluster',
         ha='center', va='center', fontsize=8, color=RED, style='italic')

# Show that the kube API never sees the call
axR.text(5.0, 7.85, '[ kube API not contacted ]',
         ha='center', va='center', fontsize=8, color=DIM,
         fontfamily='monospace', style='italic')
axR.text(5.0, 7.55,
         'world-side action prevented at library layer',
         ha='center', va='center', fontsize=8, color=DIM, style='italic')

axR.annotate('', xy=(5.0, 6.7), xytext=(5.0, 7.3),
             arrowprops=dict(arrowstyle='->', color=RED, lw=2))

# Outcome
out_box_R = FancyBboxPatch((1.0, 3.5), 8.0, 3.0,
                          boxstyle='round,pad=0.1',
                          facecolor=RED, edgecolor=RED, linewidth=2.5,
                          alpha=0.20)
axR.add_patch(out_box_R)
axR.text(5.0, 6.10, 'CALL REJECTED',
         ha='center', va='center', fontsize=12, color=RED, fontweight='bold')
axR.text(5.0, 5.65, 'library_authorization_denied',
         ha='center', va='center', fontsize=9.5, color=WHITE,
         fontfamily='monospace')
axR.text(5.0, 5.20, 'cluster: NO MANIFEST APPLIED',
         ha='center', va='center', fontsize=8.5, color=WHITE,
         fontweight='bold')
axR.text(5.0, 4.65, 'observation log emitted:',
         ha='center', va='center', fontsize=8.5, color=GOLD, fontweight='bold')
axR.text(5.0, 4.30,
         'event=library_denial,',
         ha='center', va='center', fontsize=7.5, color=SILVER,
         fontfamily='monospace')
axR.text(5.0, 4.05,
         'library=opsdb.world.kubernetes,',
         ha='center', va='center', fontsize=7.5, color=SILVER,
         fontfamily='monospace')
axR.text(5.0, 3.80,
         'attempted_target=(cluster_a, ns_finance)',
         ha='center', va='center', fontsize=7.5, color=SILVER,
         fontfamily='monospace')

axR.text(5.0, 2.7, 'Surface: library suite (OPSDB-8 §13)',
         ha='center', va='center', fontsize=9.5, color=GOLD,
         fontweight='bold')
axR.text(5.0, 2.35, 'Caught at world-side action time',
         ha='center', va='center', fontsize=8.5, color=SILVER,
         style='italic')

# Bottom audit query - same query catches both
audit_box_R = FancyBboxPatch((0.5, audit_y - 0.6), 9.0, 1.2,
                            boxstyle='round,pad=0.06',
                            facecolor=PAN, edgecolor=GOLD, linewidth=1.5)
axR.add_patch(audit_box_R)
axR.text(5.0, audit_y + 0.30,
         'same audit pattern: library denials emit observation logs',
         ha='center', va='center', fontsize=9, color=GOLD,
         fontfamily='monospace')
axR.text(5.0, audit_y - 0.05,
         'queryable through monitoring authority pointer + filter',
         ha='center', va='center', fontsize=8, color=SILVER,
         fontfamily='monospace')
axR.text(5.0, audit_y - 0.40,
         'investigation joins both surfaces by runner identity',
         ha='center', va='center', fontsize=8, color=SILVER,
         fontfamily='monospace')

for ax in (axL, axR):
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.suptitle('Same Runner, Two Denial Paths\n'
             'Both surfaces refuse the action; both produce structured records',
             color=GOLD, fontsize=15, fontweight='bold', y=0.99)

save(fig, 'infra8_03_two_denial_paths.png')


# ================================================================
# FIG 4: LIBRARY CATEGORIES -> MECHANISM FAMILIES
# Type: 5 (Connection Map)
# Shows: each library category mapped to one or more OPSDB-9 mechanism
#        families. Library taxonomy follows mechanism taxonomy.
# ================================================================

fig, ax = plt.subplots(figsize=(20, 13), facecolor=BG)
ax.set_facecolor(BG)

# Left column: library categories
# Right column: OPSDB-9 mechanism families

libraries_col = [
    ('opsdb.api',            'OpsDB API client',          0,  CYAN),
    ('world.kubernetes',     'K8s operations',            1,  PURPLE),
    ('world.cloud',          'cloud operations',          2,  GREEN),
    ('world.secret',         'secret backend',            3,  MAG),
    ('world.identity',       'IdP queries',               4,  MAG),
    ('world.monitoring',     'metric/log queries',        5,  BLUE),
    ('coordination.retry',   'retry / backoff',           6,  GOLD),
    ('coordination.breaker', 'circuit breaker',           7,  RED),
    ('coordination.hedger',  'hedged requests',           8,  ORANGE),
    ('coordination.bulkhead','isolation pools',           9,  ORANGE),
    ('observation.logging',  'structured logs',          10,  SILVER),
    ('observation.metrics',  'counters/gauges',          11,  SILVER),
    ('notification',         'pages, chat, tickets',     12,  CYAN),
    ('templating',           'value substitution',       13,  GREEN),
    ('git',                  'commit, push, PR',         14,  GOLD),
]

mechanisms_col = [
    ('Authenticator',           'Gating',         0,   GOLD),
    ('Authorizer',              'Gating',         1,   GOLD),
    ('Validator',               'Gating',         2,   GOLD),
    ('Wrap/unwrap',             'Representation', 3,   PURPLE),
    ('Channel',                 'Info movement',  4,   CYAN),
    ('Replicator',              'Info movement',  5,   CYAN),
    ('Retrier',                 'Resilience',     6,   GREEN),
    ('Circuit breaker',         'Resilience',     7,   RED),
    ('Hedger',                  'Resilience',     8,   ORANGE),
    ('Bulkhead',                'Resilience',     9,   ORANGE),
    ('Counter / Gauge',         'Sensing',        10,  BLUE),
    ('Renderer / Transformer',  'Transformation', 11,  GREEN),
    ('Filter',                  'Gating',         12,  GOLD),
    ('Version stamp / History', 'Versioning',     13,  PURPLE),
]

# Layout
left_x = 4.0
right_x = 16.0
y_top = 12.5
y_bottom = 0.5

n_libs = len(libraries_col)
n_mechs = len(mechanisms_col)

lib_w = 4.5
lib_h = 0.65
mech_w = 4.5
mech_h = 0.70

lib_ys = np.linspace(y_top, y_bottom, n_libs)
mech_ys = np.linspace(y_top, y_bottom, n_mechs)

# Column headers
ax.text(left_x, y_top + 0.85, 'Library categories (OPSDB-8)',
        ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=GOLD,
                  linewidth=1.5))
ax.text(right_x, y_top + 0.85, 'Mechanism families (OPSDB-9)',
        ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=GOLD,
                  linewidth=1.5))

# Draw library boxes
for name, sub, idx, color in libraries_col:
    y = lib_ys[idx]
    box = FancyBboxPatch((left_x - lib_w/2, y - lib_h/2), lib_w, lib_h,
                        boxstyle='round,pad=0.04',
                        facecolor=PAN, edgecolor=color, linewidth=1.3)
    ax.add_patch(box)
    ax.text(left_x - 1.95, y, name, ha='left', va='center',
            fontsize=8.5, color=color, fontweight='bold',
            fontfamily='monospace')
    ax.text(left_x + 2.0, y, sub, ha='right', va='center',
            fontsize=7.5, color=SILVER, style='italic')

# Draw mechanism boxes
for name, family, idx, color in mechanisms_col:
    y = mech_ys[idx]
    box = FancyBboxPatch((right_x - mech_w/2, y - mech_h/2), mech_w, mech_h,
                        boxstyle='round,pad=0.04',
                        facecolor=PAN, edgecolor=color, linewidth=1.3)
    ax.add_patch(box)
    ax.text(right_x - 2.0, y + 0.10, name, ha='left', va='center',
            fontsize=9, color=color, fontweight='bold')
    ax.text(right_x - 2.0, y - 0.16, '(' + family + ')', ha='left', va='center',
            fontsize=7.5, color=SILVER, style='italic')

# Mappings: (library_idx, mechanism_idx)
# Each library category maps to one or more mechanisms
mappings = [
    # opsdb.api -> Authenticator, Wrap/unwrap, Channel
    (0, 0), (0, 3), (0, 4),
    # world.kubernetes -> Authenticator, Channel, Wrap/unwrap
    (1, 0), (1, 3), (1, 4),
    # world.cloud -> Authenticator, Channel, Wrap/unwrap
    (2, 0), (2, 3),
    # world.secret -> Authenticator, Channel
    (3, 0), (3, 4),
    # world.identity -> Channel, Validator
    (4, 4), (4, 2),
    # world.monitoring -> Channel
    (5, 4),
    # coordination.retry -> Retrier
    (6, 6),
    # coordination.breaker -> Circuit breaker
    (7, 7),
    # coordination.hedger -> Hedger
    (8, 8),
    # coordination.bulkhead -> Bulkhead
    (9, 9),
    # observation.logging -> Counter/Gauge (a kind of structured emission)
    (10, 10),
    # observation.metrics -> Counter/Gauge
    (11, 10),
    # notification -> Channel, Filter
    (12, 4), (12, 12),
    # templating -> Renderer/Transformer
    (13, 11),
    # git -> Channel, Version stamp
    (14, 4), (14, 13),
]

for lib_idx, mech_idx in mappings:
    ly = lib_ys[lib_idx]
    my = mech_ys[mech_idx]
    color = libraries_col[lib_idx][3]
    ax.plot([left_x + lib_w/2 + 0.05, right_x - mech_w/2 - 0.05],
            [ly, my],
            color=color, linewidth=0.9, alpha=0.45, zorder=2)

# Bottom caption
ax.text(10.0, -0.4,
        'The library taxonomy is not arbitrary - it follows the mechanism taxonomy from OPSDB-9.',
        ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold')
ax.text(10.0, -0.85,
        'Each library is the operational realization of one or more mechanism families.',
        ha='center', va='center', fontsize=10, color=SILVER, style='italic')

ax.set_xlim(-0.5, 20.5)
ax.set_ylim(-1.3, 14.0)
ax.set_aspect('auto')
ax.axis('off')
ax.set_title('Library Categories Mapped to Mechanism Families\n'
             'OPSDB-8 libraries are the operational realization of OPSDB-9 mechanisms',
             color=GOLD, fontsize=15, fontweight='bold', pad=12)

save(fig, 'infra8_04_libraries_to_mechanisms.png')


# ================================================================
# FIG 5: LIBRARY EVOLUTION TIMELINE
# Type: 1 (Running chart)
# Shows: semantic versioning in practice; major versions, deprecation
#        cycles, multiple versions coexisting, runners pinned to versions.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 11), facecolor=BG)
style_axes(ax)

# X-axis: time in months over a 5-year span
total_months = 60
months = np.arange(0, total_months + 1)

# Track 1: opsdb.world.kubernetes major versions
# v1.x: months 0-22, supported until 30 (overlap with v2)
# v2.x: months 18-46, supported until 54 (overlap with v3)
# v3.x: months 42-60+

# Track 2: opsdb.coordination.retry major versions
# v1.x: months 0-36, supported until 48
# v2.x: months 30-60+

# Vertical layout: each version on its own row band
# Y values represent which version is "current" or "supported"

# Library 1: opsdb.world.kubernetes
y_kube_1 = 8.0
y_kube_2 = 7.0
y_kube_3 = 6.0

# Library 2: opsdb.coordination.retry
y_retry_1 = 4.0
y_retry_2 = 3.0

# Draw version bars
def version_bar(ax_in, y, start, current_end, deprec_end, label, color,
                short_label):
    # Active period (solid)
    ax_in.barh(y, current_end - start, left=start, height=0.55,
               color=color, alpha=0.5, edgecolor=color, linewidth=1.5)
    # Deprecated period (lighter, dashed border)
    if deprec_end > current_end:
        ax_in.barh(y, deprec_end - current_end, left=current_end, height=0.55,
                   color=color, alpha=0.15, edgecolor=color, linewidth=1,
                   hatch='///')
    # Label at start
    ax_in.text(start + 0.5, y, short_label, ha='left', va='center',
               fontsize=10, color=color, fontweight='bold')


# opsdb.world.kubernetes versions
version_bar(ax, y_kube_1, 0,  22, 30, 'kube v1', PURPLE, 'v1.x')
version_bar(ax, y_kube_2, 18, 46, 54, 'kube v2', BLUE,   'v2.x')
version_bar(ax, y_kube_3, 42, 60, 60, 'kube v3', GREEN,  'v3.x')

# opsdb.coordination.retry versions
version_bar(ax, y_retry_1, 0,  36, 48, 'retry v1', GOLD, 'v1.x')
version_bar(ax, y_retry_2, 30, 60, 60, 'retry v2', CYAN, 'v2.x')

# Library labels on the left
ax.text(-2.5, 7.0, 'opsdb.world\n.kubernetes', ha='center', va='center',
        fontsize=10, color=WHITE, fontweight='bold')
ax.text(-2.5, 3.5, 'opsdb.coordination\n.retry', ha='center', va='center',
        fontsize=10, color=WHITE, fontweight='bold')

# Version annotations
# kube v2 release event
ax.annotate('v2.0 released\n(adds watch streams)',
            xy=(18, y_kube_2 + 0.3), xytext=(14, 9.4),
            fontsize=8.5, color=BLUE, ha='center',
            arrowprops=dict(arrowstyle='->', color=BLUE, lw=1, alpha=0.6),
            bbox=dict(boxstyle='round,pad=0.2', facecolor=BG,
                      edgecolor=BLUE, linewidth=1))

ax.annotate('v1 deprecated\n(8-cycle window)',
            xy=(22, y_kube_1 + 0.3), xytext=(26, 9.4),
            fontsize=8.5, color=PURPLE, ha='center',
            arrowprops=dict(arrowstyle='->', color=PURPLE, lw=1, alpha=0.6),
            bbox=dict(boxstyle='round,pad=0.2', facecolor=BG,
                      edgecolor=PURPLE, linewidth=1))

ax.annotate('v1 removed\n(after dep cycle)',
            xy=(30, y_kube_1), xytext=(34, 9.4),
            fontsize=8.5, color=DIM, ha='center',
            arrowprops=dict(arrowstyle='->', color=DIM, lw=1, alpha=0.6),
            bbox=dict(boxstyle='round,pad=0.2', facecolor=BG,
                      edgecolor=DIM, linewidth=1))

ax.annotate('v3.0 released\n(typed payloads)',
            xy=(42, y_kube_3 + 0.3), xytext=(48, 9.4),
            fontsize=8.5, color=GREEN, ha='center',
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1, alpha=0.6),
            bbox=dict(boxstyle='round,pad=0.2', facecolor=BG,
                      edgecolor=GREEN, linewidth=1))

ax.annotate('retry v2\n(idempotency keys)',
            xy=(30, y_retry_2 + 0.3), xytext=(28, 1.6),
            fontsize=8.5, color=CYAN, ha='center',
            arrowprops=dict(arrowstyle='->', color=CYAN, lw=1, alpha=0.6),
            bbox=dict(boxstyle='round,pad=0.2', facecolor=BG,
                      edgecolor=CYAN, linewidth=1))

# Show some runner pins
ax.text(60.5, y_kube_1, 'no runners',
        ha='left', va='center', fontsize=7.5, color=DIM, style='italic')
ax.text(60.5, y_kube_2, '12 runners pinned',
        ha='left', va='center', fontsize=8, color=BLUE, style='italic')
ax.text(60.5, y_kube_3, '47 runners pinned',
        ha='left', va='center', fontsize=8, color=GREEN, style='italic')
ax.text(60.5, y_retry_1, '3 legacy runners',
        ha='left', va='center', fontsize=7.5, color=GOLD, style='italic')
ax.text(60.5, y_retry_2, '180 runners pinned',
        ha='left', va='center', fontsize=8, color=CYAN, style='italic')

# Legend for hatching pattern
legend_y = 0.5
ax.text(2, legend_y, 'solid:', ha='left', va='center',
        fontsize=9, color=GOLD, fontweight='bold')
ax.barh(legend_y, 5, left=4, height=0.30, color=BLUE, alpha=0.5)
ax.text(10, legend_y, 'current/active version',
        ha='left', va='center', fontsize=9, color=WHITE)

ax.text(22, legend_y, 'hatched:', ha='left', va='center',
        fontsize=9, color=GOLD, fontweight='bold')
ax.barh(legend_y, 5, left=25, height=0.30, color=BLUE, alpha=0.15,
        hatch='///', edgecolor=BLUE, linewidth=0.8)
ax.text(31, legend_y, 'deprecated, still supported',
        ha='left', va='center', fontsize=9, color=WHITE)

ax.text(43, legend_y, 'gap:', ha='left', va='center',
        fontsize=9, color=GOLD, fontweight='bold')
ax.text(46, legend_y, 'version removed (tombstone in docs)',
        ha='left', va='center', fontsize=9, color=DIM, style='italic')

# X-axis: months
ax.set_xlim(-5, 64)
ax.set_ylim(-0.5, 10.3)
ax.set_xticks([0, 12, 24, 36, 48, 60])
ax.set_xticklabels(['month 0', 'month 12', 'month 24',
                    'month 36', 'month 48', 'month 60'],
                   fontsize=10, color=SILVER)
ax.set_yticks([])
ax.set_xlabel('time (5-year span)', color=SILVER, fontsize=11)

# Year markers
for y_marker in [12, 24, 36, 48]:
    ax.axvline(x=y_marker, color=DIM, linewidth=0.5, linestyle=':', alpha=0.4)

ax.set_title('Library Evolution Timeline\n'
             'Semantic versioning, deprecation cycles, runners pin and migrate at their own pace',
             color=GOLD, fontsize=15, fontweight='bold', pad=12)

save(fig, 'infra8_05_library_evolution.png')


# ================================================================
# FIG 6: THE CROSS-IMPLEMENTATION CONTRACT
# Type: 5 (Connection Map)
# Shows: one contract, multiple language implementations gated by
#        contract test suite, runners pin to versions.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 13), facecolor=BG)
ax.set_facecolor(BG)

# Center: the contract
contract_x, contract_y = 9, 7.5
contract_box = FancyBboxPatch((contract_x - 3.0, contract_y - 1.6),
                              6.0, 3.2,
                              boxstyle='round,pad=0.15',
                              facecolor=PAN, edgecolor=GOLD, linewidth=3)
ax.add_patch(contract_box)
ax.text(contract_x, contract_y + 1.20,
        'opsdb.world.kubernetes',
        ha='center', va='center', fontsize=12, color=GOLD,
        fontweight='bold', fontfamily='monospace')
ax.text(contract_x, contract_y + 0.85,
        'CONTRACT v2.5',
        ha='center', va='center', fontsize=11, color=WHITE,
        fontweight='bold')
ax.text(contract_x, contract_y + 0.40,
        'apply_manifest(cluster, ns, manifest)',
        ha='center', va='center', fontsize=8, color=SILVER,
        fontfamily='monospace')
ax.text(contract_x, contract_y + 0.10,
        'query_resource(cluster, ns, kind, name)',
        ha='center', va='center', fontsize=8, color=SILVER,
        fontfamily='monospace')
ax.text(contract_x, contract_y - 0.20,
        'watch_resources(cluster, ns, kind, callback)',
        ha='center', va='center', fontsize=8, color=SILVER,
        fontfamily='monospace')
ax.text(contract_x, contract_y - 0.50,
        'helm_render(chart_ref, values)',
        ha='center', va='center', fontsize=8, color=SILVER,
        fontfamily='monospace')
ax.text(contract_x, contract_y - 0.80,
        'helm_install(...)',
        ha='center', va='center', fontsize=8, color=SILVER,
        fontfamily='monospace')
ax.text(contract_x, contract_y - 1.20,
        '+ failure modes, guarantees, bounds',
        ha='center', va='center', fontsize=7.5, color=DIM,
        style='italic')

# Test suite below the contract
test_box = FancyBboxPatch((contract_x - 3.0, 4.4), 6.0, 1.6,
                          boxstyle='round,pad=0.1',
                          facecolor=PAN, edgecolor=ORANGE, linewidth=2.5)
ax.add_patch(test_box)
ax.text(contract_x, 5.65, 'CONTRACT TEST SUITE',
        ha='center', va='center', fontsize=11, color=ORANGE,
        fontweight='bold')
ax.text(contract_x, 5.30, 'every operation, every failure mode,',
        ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')
ax.text(contract_x, 5.00, 'every policy enforcement check',
        ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')
ax.text(contract_x, 4.65,
        'any implementation must pass to claim contract conformance',
        ha='center', va='center', fontsize=8, color=ORANGE)

# Arrow from contract to tests
ax.annotate('', xy=(contract_x, 6.0), xytext=(contract_x, 5.9),
            arrowprops=dict(arrowstyle='-', color=GOLD, lw=1.5))

# Three implementations below the test suite
impl_y = 2.5
implementations = [
    ('Python impl',  'opsdb-k8s-python',     2.5, BLUE,    '2.5.3'),
    ('Go impl',      'opsdb-k8s-go',         9.0, GREEN,   '2.5.1'),
    ('Rust impl',    'opsdb-k8s-rust',      15.5, PURPLE,  '2.5.0'),
]

impl_w = 3.6
impl_h = 1.4

for label, pkg_name, x, color, version in implementations:
    box = FancyBboxPatch((x - impl_w/2, impl_y - impl_h/2), impl_w, impl_h,
                        boxstyle='round,pad=0.1',
                        facecolor=PAN, edgecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(x, impl_y + 0.40, label, ha='center', va='center',
            fontsize=11, color=color, fontweight='bold')
    ax.text(x, impl_y + 0.05, pkg_name, ha='center', va='center',
            fontsize=8.5, color=WHITE, fontfamily='monospace')
    ax.text(x, impl_y - 0.30, 'v' + version, ha='center', va='center',
            fontsize=8.5, color=SILVER, fontfamily='monospace')

    # PASS marker
    ax.text(x, impl_y - 0.55, 'contract tests PASS',
            ha='center', va='center', fontsize=7.5, color=GREEN,
            fontweight='bold')

    # Arrow from test suite to implementation
    ax.annotate('', xy=(x, impl_y + impl_h/2 + 0.05),
                xytext=(contract_x, 4.4),
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2,
                                alpha=0.6))

# Runners below, each pinned to one implementation
runner_y = 0.5
runners_pinned = [
    ('reconciler-A',  2.5,  BLUE),
    ('reconciler-B',  4.0,  BLUE),
    ('drift-det-C',   5.5,  BLUE),
    ('verifier-D',    7.5,  GREEN),
    ('reconciler-E',  9.0,  GREEN),
    ('verifier-F',   10.5,  GREEN),
    ('puller-G',     13.5,  PURPLE),
    ('reconciler-H', 15.0,  PURPLE),
    ('drift-det-I',  16.5,  PURPLE),
]

r_w = 1.3
r_h = 0.55

for name, x, color in runners_pinned:
    box = FancyBboxPatch((x - r_w/2, runner_y - r_h/2), r_w, r_h,
                        boxstyle='round,pad=0.04',
                        facecolor=PAN, edgecolor=color, linewidth=1)
    ax.add_patch(box)
    ax.text(x, runner_y, name, ha='center', va='center',
            fontsize=7.5, color=WHITE, fontweight='bold')

# Arrows from implementations to their runners
runner_implementation_pairs = [
    (2.5,  2.5),  (2.5, 4.0),  (2.5, 5.5),    # Python implementation runners
    (9.0,  7.5),  (9.0, 9.0),  (9.0, 10.5),   # Go implementation runners
    (15.5, 13.5), (15.5, 15.0),(15.5, 16.5),  # Rust implementation runners
]

for impl_x, runner_x in runner_implementation_pairs:
    color_idx = 0
    if impl_x == 2.5:
        color = BLUE
    elif impl_x == 9.0:
        color = GREEN
    else:
        color = PURPLE
    ax.annotate('', xy=(runner_x, runner_y + r_h/2),
                xytext=(impl_x, impl_y - impl_h/2),
                arrowprops=dict(arrowstyle='->', color=color, lw=0.8,
                                alpha=0.5))

# Top caption
ax.text(contract_x, 11.5,
        'one contract',
        ha='center', va='center', fontsize=14, color=GOLD,
        fontweight='bold')
ax.text(contract_x, 11.05,
        'language-neutral specification of operations, inputs, outputs,',
        ha='center', va='center', fontsize=9.5, color=SILVER,
        style='italic')
ax.text(contract_x, 10.75,
        'guarantees, and failure modes',
        ha='center', va='center', fontsize=9.5, color=SILVER,
        style='italic')

# Layer labels on the left
ax.text(0.2, 7.5, 'CONTRACT', ha='center', va='center',
        fontsize=10, color=GOLD, fontweight='bold', rotation=90)
ax.text(0.2, 5.2, 'TEST GATE', ha='center', va='center',
        fontsize=10, color=ORANGE, fontweight='bold', rotation=90)
ax.text(0.2, 2.5, 'IMPLEMENTATIONS', ha='center', va='center',
        fontsize=10, color=BLUE, fontweight='bold', rotation=90)
ax.text(0.2, 0.5, 'RUNNERS', ha='center', va='center',
        fontsize=10, color=SILVER, fontweight='bold', rotation=90)

# Bottom caption
ax.text(contract_x, -0.4,
        'Multiple implementations coexist; runners pin to versions; the contract is the stable surface.',
        ha='center', va='center', fontsize=10, color=GOLD, fontweight='bold')

ax.set_xlim(-0.5, 19.0)
ax.set_ylim(-0.9, 12.0)
ax.set_aspect('auto')
ax.axis('off')
ax.set_title('The Cross-Implementation Contract\n'
             'One contract, multiple language implementations, contract tests as the gate',
             color=GOLD, fontsize=16, fontweight='bold', pad=12)

save(fig, 'infra8_06_cross_implementation_contract.png')


# ================================================================
# FIG 7: PVC-REPAIR RUNNER ANATOMY
# Type: 8 (Identity Card) - one per paper, used here
# Shows: the 200-line runner exploded view; library glue vs runner logic.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 12), facecolor=BG)
ax.set_facecolor(BG)

# Header: runner identity card
header_box = FancyBboxPatch((1.0, 10.5), 16.0, 1.4,
                            boxstyle='round,pad=0.15',
                            facecolor=PAN, edgecolor=GOLD, linewidth=2.5)
ax.add_patch(header_box)
ax.text(9.0, 11.50, 'k8s_pvc_repair runner',
        ha='center', va='center', fontsize=14, color=GOLD,
        fontweight='bold', fontfamily='monospace')
ax.text(9.0, 11.10, 'a typical small runner: ~200 lines, single purpose, data-defined',
        ha='center', va='center', fontsize=10, color=SILVER, style='italic')
ax.text(9.0, 10.75,
        'reads OpsDB -> decides -> acts via libraries -> records outcome',
        ha='center', va='center', fontsize=9, color=WHITE)

# Two columns: Library glue (~50 lines) and Runner-specific logic (~150 lines)

# Left column: library glue
glue_x = 4.5
glue_y = 5.0
glue_box = FancyBboxPatch((1.0, 1.2), 7.0, 8.7,
                          boxstyle='round,pad=0.1',
                          facecolor=BLUE, edgecolor=BLUE, linewidth=2,
                          alpha=0.10)
ax.add_patch(glue_box)
ax.text(4.5, 9.55 + 0.6, 'LIBRARY GLUE (~50 lines)',
        ha='center', va='center', fontsize=12, color=BLUE,
        fontweight='bold')
ax.text(4.5, 9.20 + 0.6, 'mechanical, uniform across all runners',
        ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')

# Code-like list of library calls
glue_calls = [
    ('client = opsdb.api.connect()',                      9.55, CYAN),
    ('# (handles credentials, retries, audit)',           9.55, DIM),

    ('candidates = client.search(',                       8.85, CYAN),
    ('  entity_type="k8s_pvc",',                          8.85, CYAN),
    ('  filter=spec.runner_data_json.selector,',          8.85, CYAN),
    ('  freshness_max_seconds=300)',                      8.85, CYAN),

    ('logger = opsdb.observation.logging.get()',          7.75, SILVER),
    ('metrics = opsdb.observation.metrics.get()',         7.45, SILVER),

    ('with metrics.timer("pvc_repair_cycle"):',           6.65, GOLD),
    ('  for pvc in candidates:',                          6.40, GOLD),

    ('    # ... runner-specific decision in right panel ...', 5.65, DIM),

    ('    if action == "apply":',                         4.85, GOLD),
    ('      result = opsdb.coordination.retry.with_retry(', 4.55, GOLD),
    ('        lambda: opsdb.world.kubernetes.apply_manifest(', 4.55, PURPLE),
    ('          cluster_id=pvc.cluster_id,',              4.55, PURPLE),
    ('          namespace=pvc.namespace,',                4.55, PURPLE),
    ('          manifest=repair_manifest))',              4.55, PURPLE),

    ('    client.write_observation(',                     3.05, CYAN),
    ('      table="runner_job_target_k8s_workload",',     3.05, CYAN),
    ('      payload={',                                   3.05, CYAN),
    ('        "k8s_workload_id": pvc.parent_workload_id,', 3.05, CYAN),
    ('        "per_target_status": result.status})',      3.05, CYAN),

    ('logger.log("info", "cycle_complete", ...)',         1.65, SILVER),
    ('metrics.counter_increment("pvc_repair_count", ...)', 1.40, SILVER),
]

# Render glue calls as code-style text lines, one below another
y_cursor = 9.55
prev_y = None
line_height = 0.30
for code, _, color in glue_calls:
    if prev_y is None:
        prev_y = y_cursor
    else:
        y_cursor -= line_height
        prev_y = y_cursor

    if code.startswith('#'):
        ax.text(1.4, y_cursor, code, ha='left', va='center',
                fontsize=7.5, color=color, fontfamily='monospace',
                style='italic')
    else:
        ax.text(1.4, y_cursor, code, ha='left', va='center',
                fontsize=7.5, color=color, fontfamily='monospace')

# Right column: runner-specific decision logic
logic_box = FancyBboxPatch((9.0, 1.2), 7.5, 8.7,
                          boxstyle='round,pad=0.1',
                          facecolor=ORANGE, edgecolor=ORANGE, linewidth=2,
                          alpha=0.10)
ax.add_patch(logic_box)
ax.text(12.75, 9.55 + 0.6, 'RUNNER-SPECIFIC LOGIC (~150 lines)',
        ha='center', va='center', fontsize=12, color=ORANGE,
        fontweight='bold')
ax.text(12.75, 9.20 + 0.6, 'PVC repair decisions; not in any other runner',
        ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')

# Logic blocks
logic_blocks = [
    (8.65, 'def is_repairable(pvc):',                        ORANGE,  False),
    (8.40, '  """attention-worthy state classification"""',  DIM,     True),
    (8.15, '  if pvc.status_phase == "Lost":',               WHITE,   False),
    (7.90, '    return False  # unrecoverable',              DIM,     True),
    (7.65, '  if pvc.status_phase == "Pending"',             WHITE,   False),
    (7.45, '     and pvc.age_seconds > 300:',                WHITE,   False),
    (7.20, '    return True',                                WHITE,   False),
    (6.95, '  if pvc.has_orphaned_pod():',                   WHITE,   False),
    (6.75, '    return True',                                WHITE,   False),
    (6.50, '  return False',                                 WHITE,   False),

    (6.05, '',                                                WHITE,   False),
    (5.85, 'def choose_repair(pvc):',                         ORANGE,  False),
    (5.60, '  """rebind / resize / replace"""',               DIM,     True),
    (5.35, '  if pvc.usage_pct > 95:',                        WHITE,   False),
    (5.10, '    return RESIZE',                               WHITE,   False),
    (4.85, '  if pvc.binding_lost():',                        WHITE,   False),
    (4.60, '    return REBIND',                               WHITE,   False),
    (4.35, '  return REPLACE',                                WHITE,   False),

    (3.95, '',                                                WHITE,   False),
    (3.75, 'def build_repair_manifest(pvc, repair):',         ORANGE,  False),
    (3.50, '  """construct K8s manifest for repair"""',       DIM,     True),
    (3.25, '  base = load_template("pvc_repair.yaml")',       WHITE,   False),
    (3.00, '  return apply_repair_overrides(base, ...)',      WHITE,   False),

    (2.55, '',                                                WHITE,   False),
    (2.40, 'def auto_or_propose(pvc, repair):',               ORANGE,  False),
    (2.15, '  """policy: auto-correct vs file finding"""',    DIM,     True),
    (1.90, '  if pvc.namespace.startswith("staging_"):',      WHITE,   False),
    (1.65, '    return ACTION_APPLY',                         WHITE,   False),
    (1.40, '  return ACTION_FILE_FINDING',                    WHITE,   False),
]

for y, code, color, is_comment in logic_blocks:
    if is_comment:
        ax.text(9.4, y, code, ha='left', va='center',
                fontsize=7.5, color=color, fontfamily='monospace',
                style='italic')
    else:
        ax.text(9.4, y, code, ha='left', va='center',
                fontsize=7.5, color=color, fontfamily='monospace')

# Bottom: line counts
ax.text(4.5, 0.6, 'lines: ~50',
        ha='center', va='center', fontsize=10, color=BLUE,
        fontweight='bold')
ax.text(4.5, 0.3, '(if this code appears in another runner, it stays here)',
        ha='center', va='center', fontsize=8, color=DIM, style='italic')

ax.text(12.75, 0.6, 'lines: ~150',
        ha='center', va='center', fontsize=10, color=ORANGE,
        fontweight='bold')
ax.text(12.75, 0.3, '(specific to PVC repair; lives only in this runner)',
        ha='center', va='center', fontsize=8, color=DIM, style='italic')

ax.set_xlim(0, 18)
ax.set_ylim(-0.1, 12.5)
ax.set_aspect('auto')
ax.axis('off')
ax.set_title('PVC-Repair Runner Anatomy\n'
             'A typical small runner: 50 lines library glue + 150 lines runner-specific decision logic',
             color=GOLD, fontsize=15, fontweight='bold', pad=12)

save(fig, 'infra8_07_pvc_repair_anatomy.png')


# ================================================================
# FIG 8: THE OPSDB API CLIENT LIFECYCLE
# Type: 7 (Progression)
# Shows: what a single API client call actually does behind the scenes;
#        credential acquisition, request construction, audit, retry.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 12), facecolor=BG)
ax.set_facecolor(BG)

# Vertical sequence diagram showing one API client call from runner's POV
# Each phase is a horizontal band with explanation

phases = [
    ('runner code',
     'client.submit_change_set(field_changes, reason="rotate creds")',
     ORANGE,
     'a single line in the runner',
     11.0),

    ('phase 1: credential check',
     'is current credential still valid? if expiring, refresh from secret backend',
     MAG,
     'opsdb.world.secret library auto-refreshes',
     9.5),

    ('phase 2: correlation',
     'attach runner_job_id, propagate trace context, generate request_id',
     CYAN,
     'audit correlation IDs flow through the call chain',
     8.0),

    ('phase 3: optimistic version stamp',
     'attach drafted-against version stamps for each affected entity',
     PURPLE,
     'OPSDB-6 §5.6 stale-version protection',
     6.5),

    ('phase 4: serialize and send',
     'POST /change_set with structured payload over TLS',
     BLUE,
     'opsdb.api transport handles the wire format',
     5.0),

    ('phase 5: API gate processing',
     '10-step gate sequence runs (auth/authz/validate/route/audit/execute)',
     GOLD,
     'this is OPSDB-6 territory',
     3.5),

    ('phase 6: response parsing',
     'parse structured response, surface errors as typed exceptions',
     GREEN,
     'runner sees a clean structured result or a structured error',
     2.0),
]

# Layout
phase_x_start = 1.0
phase_x_end = 17.0
phase_w = phase_x_end - phase_x_start
phase_h = 1.1

for label, detail, color, sub, y in phases:
    box = FancyBboxPatch((phase_x_start, y - phase_h/2), phase_w, phase_h,
                        boxstyle='round,pad=0.06',
                        facecolor=PAN, edgecolor=color, linewidth=1.8)
    ax.add_patch(box)
    ax.text(phase_x_start + 0.2, y + 0.30, label, ha='left', va='center',
            fontsize=11, color=color, fontweight='bold')
    ax.text(phase_x_start + 0.2, y - 0.05, detail, ha='left', va='center',
            fontsize=9, color=WHITE, fontfamily='monospace')
    ax.text(phase_x_start + 0.2, y - 0.35, sub, ha='left', va='center',
            fontsize=8.5, color=SILVER, style='italic')

# Connecting arrows between phases
for i in range(len(phases) - 1):
    y_top = phases[i][4] - phase_h/2
    y_bot = phases[i+1][4] + phase_h/2
    ax.annotate('', xy=(2.5, y_bot - 0.05), xytext=(2.5, y_top + 0.05),
                arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.5,
                                alpha=0.7))

# Special path: stale version retry loop (between phase 5 and phase 6)
# Show as a curved arrow back from response to phase 3
loop_start_y = phases[5][4]  # API gate
loop_target_y = phases[2][4]  # correlation (we re-do version stamps then resend)

ax.annotate('',
            xy=(15.5, loop_target_y),
            xytext=(15.5, loop_start_y - 0.1),
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.5,
                            connectionstyle='arc3,rad=-0.4', alpha=0.8))
ax.text(16.7, (loop_start_y + loop_target_y) / 2,
        'on stale_version:\nrefetch, reconcile,\nretry submit',
        ha='center', va='center', fontsize=8.5, color=ORANGE,
        style='italic',
        bbox=dict(boxstyle='round,pad=0.25', facecolor=BG,
                  edgecolor=ORANGE, linewidth=1))

# Bottom: the runner sees only this
result_y = 0.35
result_box = FancyBboxPatch((1.0, result_y - 0.4), 16.0, 0.8,
                           boxstyle='round,pad=0.08',
                           facecolor=PAN, edgecolor=GREEN, linewidth=2)
ax.add_patch(result_box)
ax.text(9.0, result_y + 0.10,
        'runner sees: change_set_id (success) or typed exception (failure)',
        ha='center', va='center', fontsize=10, color=GREEN, fontweight='bold')
ax.text(9.0, result_y - 0.25,
        'all six phases above are handled by the library; the runner code is one line',
        ha='center', va='center', fontsize=8.5, color=SILVER, style='italic')

# Side annotations explaining what's at stake at each layer
ax.text(0.4, 9.5, 'transport', ha='center', va='center',
        fontsize=8, color=DIM, rotation=90)
ax.text(0.4, 6.5, 'protocol', ha='center', va='center',
        fontsize=8, color=DIM, rotation=90)
ax.text(0.4, 3.5, 'remote', ha='center', va='center',
        fontsize=8, color=DIM, rotation=90)

ax.set_xlim(-0.5, 19.0)
ax.set_ylim(-0.4, 12.0)
ax.set_aspect('auto')
ax.axis('off')
ax.set_title('The OpsDB API Client Lifecycle\n'
             'What a single client.submit_change_set() call actually does',
             color=GOLD, fontsize=16, fontweight='bold', pad=12)

save(fig, 'infra8_08_api_client_lifecycle.png')


# ================================================================
# SUMMARY
# ================================================================

print("\n" + "=" * 60)
print("OPSDB-8 diagram script complete")
print("=" * 60)
print("Files written to: %s" % outdir)
print()
print("  infra8_01_two_sided_enforcement.png")
print("  infra8_02_library_runner_boundary.png")
print("  infra8_03_two_denial_paths.png")
print("  infra8_04_libraries_to_mechanisms.png")
print("  infra8_05_library_evolution.png")
print("  infra8_06_cross_implementation_contract.png")
print("  infra8_07_pvc_repair_anatomy.png")
print("  infra8_08_api_client_lifecycle.png")
