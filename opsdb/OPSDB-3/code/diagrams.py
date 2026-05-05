#!/usr/bin/env python3
"""
OPSDB OPSDB-3 Diagrams - OpsDB Implementation Path
8 figures covering cardinality, phase progression, schema discipline,
library structure, governance transition, and operational growth.
Output: PNG files to ../figures/
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle
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

def save(fig, name):
    path = os.path.join(outdir, name)
    fig.savefig(path, dpi=180, facecolor=BG, bbox_inches='tight', pad_inches=0.3)
    plt.close(fig)
    print("  Saved: %s" % name)

# ================================================================
# FIG 1: RUNNER POPULATION GROWTH OVER PHASES
# Type: 1 (Curve)
# Shows: operational benefits arrive in phase 6, not before. Flat
# through phases 1-5 then sharp accumulation. Text cannot show the
# shape of the delay.
# ================================================================

fig, ax = plt.subplots(figsize=(16, 9))
fig.patch.set_facecolor(BG)
style_axes(ax)

# Phase boundaries on x-axis (cumulative time units, conceptual)
phase_starts = [0, 1, 2, 3.5, 4.5, 6, 7.5]
phase_labels = ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4', 'Phase 5', 'Phase 6', '']

# Runner counts: phases 1-5 produce zero "real-work" runners
# Phase 3-4 has scrappy ingestion scripts (not registered runners)
# Phase 5 registers them but they are still OpsDB-maintenance only
# Phase 6 starts adding operational-benefit runners
x = np.linspace(0, 9, 400)
y = np.zeros_like(x)
for i, xi in enumerate(x):
    if xi < 4.5:
        y[i] = 0
    elif xi < 6:
        # Phase 5: registers existing scripts as runners (OpsDB-maintenance)
        y[i] = 3 * (xi - 4.5) / 1.5
    else:
        # Phase 6: operational runners accumulate
        t = xi - 6
        y[i] = 3 + 18 * (1 - np.exp(-t * 0.6))

ax.plot(x, y, color=GOLD, linewidth=2.5, label='Operational runner count')

# Shade phase regions
phase_colors = [BLUE, BLUE, CYAN, CYAN, ORANGE, GREEN]
for i in range(6):
    ax.axvspan(phase_starts[i], phase_starts[i+1], alpha=0.05, color=phase_colors[i])

# Phase boundary lines and labels at top
for i in range(6):
    ax.axvline(phase_starts[i+1], color=DIM, linestyle=':', linewidth=0.8, alpha=0.6)
    mid = (phase_starts[i] + phase_starts[i+1]) / 2
    ax.text(mid, 24.5, phase_labels[i], color=SILVER, fontsize=10,
            ha='center', va='top', fontweight='bold')

# Annotation: "operational benefit arrives here"
ax.annotate('Operational benefits\nbegin arriving',
            xy=(6.3, 4.5), xytext=(7.6, 11),
            color=GOLD, fontsize=11, ha='center', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.5))

# Annotation: phases 1-5 produce zero real-work runners
ax.annotate('Phases 1-5: zero runners\ndoing operational work\nbeyond OpsDB maintenance',
            xy=(2.5, 0.3), xytext=(2.5, 8),
            color=SILVER, fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color=SILVER, lw=1.0, alpha=0.7))

# Annotation: phase 5 transition
ax.annotate('Phase 5: scripts become\nregistered runners',
            xy=(5.2, 2.1), xytext=(4.0, 16),
            color=ORANGE, fontsize=9, ha='center',
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.0, alpha=0.7))

# Phase 6 doesn't end note
ax.text(8.6, 20.5, 'Phase 6 does\nnot end',
        color=GREEN, fontsize=9, ha='center', style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=GREEN, linewidth=1))

ax.set_xlim(-0.3, 9.3)
ax.set_ylim(-1, 26)
ax.set_xlabel('Implementation timeline (conceptual)', color=SILVER, fontsize=12)
ax.set_ylabel('Runners performing operational work', color=SILVER, fontsize=12)
ax.set_title('Runner Population Growth Across Implementation Phases',
             color=GOLD, fontsize=15, fontweight='bold', pad=18)
ax.set_xticks([])

leg = ax.legend(loc='upper left', facecolor=PAN, edgecolor=DIM,
                labelcolor=WHITE, fontsize=10)

save(fig, 'infra09_01_runner_growth.png')

# ================================================================
# FIG 2: N-OPSDB SYNC ARCHITECTURE
# Type: 4 (Geometric Cross-Section)
# Shows: shared infrastructure (one schema, one library suite, one
# API codebase) deploys to N substrates with diverging data. Text
# cannot convey the "same shape, different contents" geometry.
# ================================================================

fig, ax = plt.subplots(figsize=(16, 10))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

# Top: shared infrastructure (one source of truth)
shared_y = 8.0
shared_box_w = 3.2
shared_box_h = 1.1
shared_items = [
    ('Schema repo', 2.5, BLUE),
    ('Library suite', 8.0, CYAN),
    ('API codebase', 13.5, ORANGE),
]
for label, cx, color in shared_items:
    box = FancyBboxPatch((cx - shared_box_w/2, shared_y - shared_box_h/2),
                          shared_box_w, shared_box_h,
                          boxstyle='round,pad=0.05', facecolor=PAN,
                          edgecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(cx, shared_y, label, color=WHITE, fontsize=11,
            ha='center', va='center', fontweight='bold')

# Header for shared row
ax.text(8, 9.45, 'ONE source of truth (shared across all substrates)',
        color=GOLD, fontsize=12, ha='center', fontweight='bold')

# Bottom: N substrates (showing 3 to make N visual)
substrate_y = 3.0
substrate_w = 4.2
substrate_h = 3.2
substrate_centers = [3.0, 8.0, 13.0]
substrate_labels = ['Substrate 1\n(production)', 'Substrate 2\n(corp)', 'Substrate N\n(...)']
substrate_data = [
    ['Production data', 'Prod users', 'Prod audit log', 'Prod runners'],
    ['Corp data', 'Corp users', 'Corp audit log', 'Corp runners'],
    ['Other data', 'Other users', 'Other audit log', 'Other runners'],
]

for cx, lbl, data in zip(substrate_centers, substrate_labels, substrate_data):
    # Outer substrate box
    box = FancyBboxPatch((cx - substrate_w/2, substrate_y - substrate_h/2),
                          substrate_w, substrate_h,
                          boxstyle='round,pad=0.05', facecolor=PAN,
                          edgecolor=GOLD, linewidth=1.5, alpha=0.9)
    ax.add_patch(box)
    # Substrate title
    ax.text(cx, substrate_y + substrate_h/2 - 0.35, lbl, color=GOLD,
            fontsize=10, ha='center', va='center', fontweight='bold')
    # Diverging contents
    for j, item in enumerate(data):
        ax.text(cx, substrate_y + 0.7 - j*0.45, item, color=SILVER,
                fontsize=9, ha='center', va='center')

# Header for substrate row
ax.text(8, 4.95, 'N substrates (data, users, audit log all diverge)',
        color=SILVER, fontsize=12, ha='center', fontweight='bold', style='italic')

# Arrows from shared to each substrate
for cx_top in [item[1] for item in shared_items]:
    for cx_bot in substrate_centers:
        arrow = FancyArrowPatch((cx_top, shared_y - shared_box_h/2 - 0.05),
                                 (cx_bot, substrate_y + substrate_h/2 + 0.05),
                                 arrowstyle='->', color=DIM,
                                 linewidth=0.7, alpha=0.5,
                                 mutation_scale=10)
        ax.add_patch(arrow)

# Bootstrap-at-N=2 note
ax.text(8, 1.1, 'Bootstrap at N=2 from day one. Adding N=3 later is cheap; '
                'retrofitting sync onto a system started at N=1 is expensive.',
        color=CYAN, fontsize=10, ha='center', style='italic',
        bbox=dict(boxstyle='round,pad=0.4', facecolor=BG,
                  edgecolor=CYAN, linewidth=1))

ax.text(8, 0.3,
        'No cross-substrate writes. Each substrate is its own write authority.',
        color=DIM, fontsize=9, ha='center', style='italic')

ax.set_title('N-OpsDB Sync Pipeline: Shared Infrastructure, Diverging Data',
             color=GOLD, fontsize=14, fontweight='bold', y=0.97)

save(fig, 'infra09_02_n_opsdb_sync.png')

# ================================================================
# FIG 3: DSNC LIST-OF-N RIGHT VS WRONG
# Type: 6 (Comparison)
# Shows: naive positional flattening vs proper sub-table. The
# visual contrast makes the structural difference immediate.
# ================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9),
                                gridspec_kw={'wspace': 0.30})
fig.patch.set_facecolor(BG)

for ax in (ax1, ax2):
    ax.set_facecolor(PAN)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

# === LEFT: WRONG ===
ax1.text(5, 11.3, 'WRONG: Positional Flattening',
         color=RED, fontsize=14, ha='center', fontweight='bold')
ax1.text(5, 10.6, 'Naive flatten of a list-of-N into indexed fields',
         color=SILVER, fontsize=10, ha='center', style='italic')

# Single bloated row
wrong_box = FancyBboxPatch((0.5, 4.5), 9.0, 5.5,
                            boxstyle='round,pad=0.1', facecolor=BG,
                            edgecolor=RED, linewidth=2)
ax1.add_patch(wrong_box)
ax1.text(5, 9.6, 'cloud_resource (one row)',
         color=RED, fontsize=11, ha='center', fontweight='bold')

wrong_fields = [
    'id: ec2-abc123',
    'cloud_data_volumes_0_id: vol-1',
    'cloud_data_volumes_0_size: 100',
    'cloud_data_volumes_1_id: vol-2',
    'cloud_data_volumes_1_size: 200',
    'cloud_data_volumes_2_id: vol-3',
    'cloud_data_volumes_2_size: 50',
    '... how many do we support?',
]
for i, f in enumerate(wrong_fields):
    color = WHITE if i == 0 else (RED if 'how many' in f else SILVER)
    ax1.text(0.9, 9.0 - i*0.55, f, color=color, fontsize=9,
             ha='left', va='center', family='monospace')

# Failure callouts
ax1.text(5, 3.7, 'Failures:', color=RED, fontsize=11,
         ha='center', fontweight='bold')
failures = [
    'Indices are positional, not meaningful',
    'Schema must change every time N grows',
    'Queries treat items non-uniformly',
    'Provenance of list-ness is lost',
]
for i, f in enumerate(failures):
    ax1.text(5, 3.0 - i*0.5, '- ' + f, color=RED, fontsize=9, ha='center')

# === RIGHT: CORRECT ===
ax2.text(5, 11.3, 'CORRECT: Sub-Table with FK',
         color=GREEN, fontsize=14, ha='center', fontweight='bold')
ax2.text(5, 10.6, 'List-of-N becomes N rows in a related table',
         color=SILVER, fontsize=10, ha='center', style='italic')

# Parent table
parent_box = FancyBboxPatch((1.5, 7.8), 7.0, 1.7,
                             boxstyle='round,pad=0.1', facecolor=BG,
                             edgecolor=GREEN, linewidth=2)
ax2.add_patch(parent_box)
ax2.text(5, 9.1, 'cloud_resource (one row)',
         color=GREEN, fontsize=11, ha='center', fontweight='bold')
ax2.text(5, 8.5, 'id: ec2-abc123', color=WHITE, fontsize=9,
         ha='center', family='monospace')
ax2.text(5, 8.05, 'cloud_resource_type: ec2_instance', color=SILVER,
         fontsize=9, ha='center', family='monospace')

# Child table with N rows
child_box = FancyBboxPatch((0.7, 4.0), 8.6, 3.0,
                            boxstyle='round,pad=0.1', facecolor=BG,
                            edgecolor=GREEN, linewidth=2)
ax2.add_patch(child_box)
ax2.text(5, 6.6, 'cloud_resource_attached_volume (N rows)',
         color=GREEN, fontsize=11, ha='center', fontweight='bold')

child_rows = [
    'id=v-1  parent=ec2-abc123  volume_id=vol-1  size=100',
    'id=v-2  parent=ec2-abc123  volume_id=vol-2  size=200',
    'id=v-3  parent=ec2-abc123  volume_id=vol-3  size=50',
]
for i, r in enumerate(child_rows):
    ax2.text(5, 6.05 - i*0.45, r, color=SILVER, fontsize=8.5,
             ha='center', family='monospace')

# FK arrow from child to parent
arrow = FancyArrowPatch((5, 7.05), (5, 7.75),
                         arrowstyle='->', color=GREEN,
                         linewidth=1.5, mutation_scale=15)
ax2.add_patch(arrow)
ax2.text(5.4, 7.4, 'FK', color=GREEN, fontsize=9, fontweight='bold')

# Success callouts
ax2.text(5, 3.4, 'Properties:', color=GREEN, fontsize=11,
         ha='center', fontweight='bold')
successes = [
    'Each item has its own identity',
    'N is unbounded without schema change',
    'Queries treat items uniformly',
    'Provenance preserved through FK',
]
for i, s in enumerate(successes):
    ax2.text(5, 2.7 - i*0.5, '+ ' + s, color=GREEN, fontsize=9, ha='center')

fig.suptitle('The DSNC List-of-N Test: How to Flatten JSON Without Losing Provenance',
             color=GOLD, fontsize=15, fontweight='bold', y=0.995)

save(fig, 'infra09_03_dsnc_list_of_n.png')

# ================================================================
# FIG 4: MINIMAL LIBRARY STARTING SET
# Type: 4 (Geometric Cross-Section)
# Shows: nested rings - foundational libraries at center, world-side
# libraries radiating outward, runners in the outer band. Text cannot
# convey what is load-bearing vs what comes later.
# ================================================================

fig, ax = plt.subplots(figsize=(14, 14))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(-7, 7)
ax.set_ylim(-7, 7)
ax.set_aspect('equal')
ax.axis('off')

# Outermost ring: runner population
outer = Circle((0, 0), 6.2, facecolor=PAN, edgecolor=GOLD,
               linewidth=2, alpha=0.4)
ax.add_patch(outer)

# Middle ring: world-side libraries (phase 6)
middle = Circle((0, 0), 4.5, facecolor=PAN, edgecolor=CYAN,
                linewidth=2, alpha=0.5)
ax.add_patch(middle)

# Inner ring: resilience/coordination libraries (phase 6 as patterns emerge)
inner_mid = Circle((0, 0), 3.0, facecolor=PAN, edgecolor=BLUE,
                   linewidth=2, alpha=0.6)
ax.add_patch(inner_mid)

# Innermost: foundational libraries (phase 4 minimum)
core = Circle((0, 0), 1.5, facecolor=BG, edgecolor=GOLD,
              linewidth=2.5)
ax.add_patch(core)

# Core labels (phase 4 minimum)
ax.text(0, 0.3, 'API client', color=GOLD, fontsize=11,
        ha='center', va='center', fontweight='bold')
ax.text(0, -0.3, 'Logging', color=GOLD, fontsize=11,
        ha='center', va='center', fontweight='bold')

# Inner-mid: coordination (placed at angles, with offsets to prevent overlap)
inner_items = [
    ('Retry/backoff',     90),
    ('Circuit breaker',  150),
    ('Bulkhead',         210),
    ('Hedger',           330),
]
for label, angle in inner_items:
    rad = np.radians(angle)
    rx = 2.25 * np.cos(rad)
    ry = 2.25 * np.sin(rad)
    ax.text(rx, ry, label, color=BLUE, fontsize=10,
            ha='center', va='center', fontweight='bold')

# Middle: world-side libraries
middle_items = [
    ('K8s ops',          45),
    ('Cloud ops',         0),
    ('Host ops',        315),
    ('Secret access',   270),
    ('Identity provider',225),
    ('Monitoring',      180),
    ('Notification',    135),
    ('Git ops',          90),
]
for label, angle in middle_items:
    rad = np.radians(angle)
    rx = 3.75 * np.cos(rad)
    ry = 3.75 * np.sin(rad)
    ax.text(rx, ry, label, color=CYAN, fontsize=9.5,
            ha='center', va='center')

# Outer: runner kinds
outer_items = [
    ('Pullers',          90),
    ('Reconcilers',      45),
    ('Verifiers',         0),
    ('Drift detectors', 315),
    ('Reactors',        270),
    ('Schedulers',      225),
    ('Reapers',         180),
    ('Executors',       135),
]
for label, angle in outer_items:
    rad = np.radians(angle)
    rx = 5.35 * np.cos(rad)
    ry = 5.35 * np.sin(rad)
    ax.text(rx, ry, label, color=GOLD, fontsize=10,
            ha='center', va='center', fontweight='bold')

# Ring labels (placed outside the rings to avoid overlap)
ring_labels = [
    (0,    1.5 + 0.32, 'Phase 4 minimum',  GOLD),
    (-2.85, 0,        'Phase 6 (patterns)', BLUE),
    (-4.55, -0.20,    'Phase 6 (world-side)', CYAN),
    (-6.45, -0.20,    'Phase 6 (runners)',   GOLD),
]
# Better: place ring labels along the bottom-left as offset annotations
for i, (label, color) in enumerate([
    ('Phase 4: foundational',   GOLD),
    ('Phase 6: resilience',     BLUE),
    ('Phase 6: world-side',     CYAN),
    ('Phase 6: runner kinds',   GOLD),
]):
    y = -6.6 + i * 0.3 if False else 0  # placeholder
# Use a proper legend instead

legend_handles = [
    mpatches.Patch(color=GOLD,  label='Phase 4 minimum: API client + logging'),
    mpatches.Patch(color=BLUE,  label='Phase 6: resilience patterns (extract once seen 3x)'),
    mpatches.Patch(color=CYAN,  label='Phase 6: world-side libraries (built when needed)'),
    mpatches.Patch(color=GOLD,  label='Phase 6: runners consuming the suite'),
]
leg = ax.legend(handles=legend_handles, loc='lower center',
                bbox_to_anchor=(0.5, -0.02),
                facecolor=PAN, edgecolor=DIM,
                labelcolor=WHITE, fontsize=10, ncol=2,
                frameon=True)

ax.set_title('Minimal Library Starting Set: What is Load-Bearing at Phase 4',
             color=GOLD, fontsize=15, fontweight='bold', pad=18)

save(fig, 'infra09_04_library_rings.png')

# ================================================================
# FIG 5: DEV-TO-OPERATIONAL CUTOVER
# Type: 7 (Progression)
# Shows: before/after states of the one-time transition at phase 5.
# Text cannot show the discrete cutover boundary visually.
# ================================================================

fig, ax = plt.subplots(figsize=(18, 10))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 18)
ax.set_ylim(0, 11)
ax.axis('off')

# Cutover line in the middle
ax.axvline(9, color=ORANGE, linewidth=3, linestyle='-', alpha=0.9)
ax.text(9, 10.5, 'CUTOVER', color=ORANGE, fontsize=13,
        ha='center', va='center', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                  edgecolor=ORANGE, linewidth=2))
ax.text(9, 0.4, 'One-time event at Phase 5',
        color=ORANGE, fontsize=10, ha='center', style='italic')

# === LEFT: BEFORE (development) ===
ax.text(4.5, 9.7, 'BEFORE: Development substrate',
        color=BLUE, fontsize=13, ha='center', fontweight='bold')
ax.text(4.5, 9.2, '(Phase 3-4 state)',
        color=SILVER, fontsize=10, ha='center', style='italic')

before_items = [
    ('Minimal API', 'authenticated read/write only', BLUE),
    ('No change management', 'direct writes accepted', BLUE),
    ('Rough authorization', 'role-based read/write', BLUE),
    ('No runner report keys', 'unrestricted write surface', BLUE),
    ('Simple request logging', 'no audit log infrastructure', BLUE),
    ('Ad-hoc ingestion scripts', 'not registered runners', BLUE),
    ('Schema iterations are cheap', 'no governance pipeline', BLUE),
]
for i, (title, sub, color) in enumerate(before_items):
    y = 8.4 - i * 1.05
    box = FancyBboxPatch((0.5, y - 0.4), 8.0, 0.8,
                          boxstyle='round,pad=0.05', facecolor=PAN,
                          edgecolor=color, linewidth=1, alpha=0.85)
    ax.add_patch(box)
    ax.text(0.9, y + 0.12, title, color=WHITE, fontsize=10,
            ha='left', va='center', fontweight='bold')
    ax.text(0.9, y - 0.22, sub, color=SILVER, fontsize=8.5,
            ha='left', va='center', style='italic')

# === RIGHT: AFTER (operational) ===
ax.text(13.5, 9.7, 'AFTER: Operational substrate',
        color=GREEN, fontsize=13, ha='center', fontweight='bold')
ax.text(13.5, 9.2, '(Phase 5 onward)',
        color=SILVER, fontsize=10, ha='center', style='italic')

after_items = [
    ('Full OPSDB-6 API', '10-step gate on every operation', GREEN),
    ('Change management active', 'change_managed entities gated', GREEN),
    ('Five-layer authorization', 'role/entity/field/runner/policy', GREEN),
    ('Runner report keys enforced', 'declared writable surface only', GREEN),
    ('Append-only audit log', 'full attribution every write', GREEN),
    ('Registered runners with scopes', 'runner_spec rows in OpsDB', GREEN),
    ('Schema changes are change_sets', 'governed evolution', GREEN),
]
for i, (title, sub, color) in enumerate(after_items):
    y = 8.4 - i * 1.05
    box = FancyBboxPatch((9.5, y - 0.4), 8.0, 0.8,
                          boxstyle='round,pad=0.05', facecolor=PAN,
                          edgecolor=color, linewidth=1, alpha=0.85)
    ax.add_patch(box)
    ax.text(9.9, y + 0.12, title, color=WHITE, fontsize=10,
            ha='left', va='center', fontweight='bold')
    ax.text(9.9, y - 0.22, sub, color=SILVER, fontsize=8.5,
            ha='left', va='center', style='italic')

# Bottom annotation about historical data
ax.text(9, 1.2,
        'Historical data loaded under dev API is preserved. '
        'Governance applies to changes after the cutover, not retroactively.',
        color=CYAN, fontsize=10, ha='center', style='italic',
        bbox=dict(boxstyle='round,pad=0.4', facecolor=BG,
                  edgecolor=CYAN, linewidth=1))

ax.set_title('The Development-to-Operational Cutover: A One-Time Transition',
             color=GOLD, fontsize=15, fontweight='bold', y=0.98)

save(fig, 'infra09_05_cutover.png')

# ================================================================
# FIG 6: SCHEMA QUALITY COST OVER LIFETIME
# Type: 1 (Curve)
# Shows: two divergent curves over years. Schema-right stays flat;
# schema-wrong diverges as every consumer pays the cost forever.
# Text cannot show the scale of compounding.
# ================================================================

fig, ax = plt.subplots(figsize=(16, 9))
fig.patch.set_facecolor(BG)
style_axes(ax)

t = np.linspace(0, 10, 400)

# Schema-right cost: small ongoing maintenance, grows linearly with scope
right_cost = 1.0 + 0.15 * t

# Schema-wrong cost: each consumer pays a fix-up tax; consumers grow
# over time, so cost grows superlinearly
# Approximate: linear consumer growth + per-consumer fixed tax + occasional
# major re-work events
wrong_cost = 1.0 + 0.4 * t + 0.18 * t**2 + 0.4 * np.sin(t * 0.8) * (t > 2)

ax.plot(t, right_cost, color=GREEN, linewidth=2.5,
        label='Schema right at Phase 3')
ax.plot(t, wrong_cost, color=RED, linewidth=2.5,
        label='Schema wrong at Phase 3')

# Fill the gap to emphasize the divergence
ax.fill_between(t, right_cost, wrong_cost,
                where=(wrong_cost > right_cost),
                color=RED, alpha=0.10)

# Phase 3 marker
ax.axvline(0.3, color=ORANGE, linestyle='--', linewidth=1.2, alpha=0.7)
ax.text(0.4, 19, 'Phase 3:\nschema baseline\nset here', color=ORANGE,
        fontsize=9, ha='left', va='top')

# Annotation: every consumer pays
ax.annotate('Every consumer pays\nthe schema-shape cost\non every cycle',
            xy=(7.5, wrong_cost[300]), xytext=(5.5, 9),
            color=RED, fontsize=10, ha='center', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.3))

# Annotation: stays flat
ax.annotate('Linear maintenance\nscaling with scope',
            xy=(7.5, right_cost[300]), xytext=(8.0, 4.5),
            color=GREEN, fontsize=10, ha='center', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.3))

# Key callouts inline
ax.text(2.0, 1.3, 'Both start near equal',
        color=SILVER, fontsize=9, ha='center', style='italic')

ax.set_xlim(-0.3, 10.3)
ax.set_ylim(0, 22)
ax.set_xlabel('Years of OpsDB operation', color=SILVER, fontsize=12)
ax.set_ylabel('Cumulative cost paid by consumers (relative units)',
              color=SILVER, fontsize=12)
ax.set_title('Schema Quality Cost Over OpsDB Lifetime',
             color=GOLD, fontsize=15, fontweight='bold', pad=18)

leg = ax.legend(loc='upper left', facecolor=PAN, edgecolor=DIM,
                labelcolor=WHITE, fontsize=11)

ax.text(5, -2.2,
        'Schema is cheap to fix at Phase 3 (no governance, no consumers). '
        'After Phase 5, every fix is paid by every consumer of the data.',
        color=DIM, fontsize=9, ha='center', style='italic',
        transform=ax.transData)
# Move that note inside the axes range
ax.text(5, 0.6,
        '(Schema is cheap to fix at Phase 3. After Phase 5, every fix is paid by every consumer.)',
        color=DIM, fontsize=9, ha='center', style='italic')

save(fig, 'infra09_06_schema_quality_cost.png')

# ================================================================
# FIG 7: CARDINALITY LANDSCAPE WITH N=2 FORBIDDEN
# Type: 3 (Threshold/Region)
# Shows: three valid regions (0, 1, N) with N=2 as explicit failure
# state. Text cannot make the "no 2" rule visually immediate.
# ================================================================

fig, ax = plt.subplots(figsize=(16, 9))
fig.patch.set_facecolor(BG)
ax.set_facecolor(PAN)
for spine in ax.spines.values():
    spine.set_color(DIM)
    spine.set_linewidth(0.5)
ax.tick_params(colors=DIM, labelsize=9)

# X-axis: cardinality value (0, 1, 2, 3, 4, 5+)
# Y-axis: validity (1.0 = valid, 0 = forbidden), but use it for visual placement

# Region shading
ax.axvspan(-0.5, 0.5, alpha=0.10, color=DIM)        # 0 region
ax.axvspan(0.5, 1.5,  alpha=0.15, color=GREEN)      # 1 region
ax.axvspan(1.5, 2.5,  alpha=0.20, color=RED)        # 2 forbidden
ax.axvspan(2.5, 5.5,  alpha=0.15, color=BLUE)       # N region

# Region labels at top
ax.text(0,   2.65, '0 OpsDBs',     color=DIM,   fontsize=12, ha='center', fontweight='bold')
ax.text(1,   2.65, '1 OpsDB',      color=GREEN, fontsize=12, ha='center', fontweight='bold')
ax.text(2,   2.65, '2 OpsDBs',     color=RED,   fontsize=12, ha='center', fontweight='bold')
ax.text(4,   2.65, 'N OpsDBs',     color=BLUE,  fontsize=12, ha='center', fontweight='bold')

# Status labels just below region labels
ax.text(0,   2.30, '(failure state - no coordination)',
        color=DIM,   fontsize=9, ha='center', style='italic')
ax.text(1,   2.30, 'VALID',
        color=GREEN, fontsize=10, ha='center', fontweight='bold')
ax.text(2,   2.30, 'FORBIDDEN',
        color=RED,   fontsize=10, ha='center', fontweight='bold')
ax.text(4,   2.30, 'VALID (N >= 3)',
        color=BLUE,  fontsize=10, ha='center', fontweight='bold')

# Markers at each cardinality
ax.scatter([0], [1.5], s=400, c=DIM,   edgecolors=WHITE, linewidth=1.5, zorder=5)
ax.scatter([1], [1.5], s=400, c=GREEN, edgecolors=WHITE, linewidth=1.5, zorder=5)
ax.scatter([2], [1.5], s=400, c=RED,   edgecolors=WHITE, linewidth=1.5,
           marker='X', zorder=5)
ax.scatter([3, 4, 5], [1.5, 1.5, 1.5], s=400, c=BLUE,
           edgecolors=WHITE, linewidth=1.5, zorder=5)

# Reasons that justify each (offset boxes below)
reasons_zero = ['Default failure state', 'before any OpsDB exists']
reasons_one  = ['Most orgs land here', 'under structural-unity threshold']
reasons_two  = ['NEVER. There is no', 'stable "almost 1" state']
reasons_n    = ['Security perimeters', 'Regulatory residency',
                'Air-gap requirements', 'Independent org units']

reason_groups = [
    (0, reasons_zero, DIM),
    (1, reasons_one,  GREEN),
    (2, reasons_two,  RED),
    (4, reasons_n,    BLUE),
]
for cx, reasons, color in reason_groups:
    box_h = 0.15 * len(reasons) + 0.5
    box = FancyBboxPatch((cx - 0.85, 0.15), 1.7, box_h,
                          boxstyle='round,pad=0.05', facecolor=BG,
                          edgecolor=color, linewidth=1.2)
    ax.add_patch(box)
    for i, r in enumerate(reasons):
        ax.text(cx, 0.15 + box_h - 0.25 - i * 0.18, r,
                color=color, fontsize=8.5, ha='center', va='center')

# What does NOT justify N callout (top right)
ax.text(4, -0.55, 'N is NOT justified by:',
        color=ORANGE, fontsize=10, ha='center', fontweight='bold')
not_reasons = [
    'Convenience',
    'Premature optimization',
    'Performance scaling (engine choice)',
    'Technical fragility (= bad ops practice)',
]
for i, nr in enumerate(not_reasons):
    ax.text(4, -0.80 - i * 0.18, '- ' + nr, color=ORANGE,
            fontsize=8.5, ha='center')

# Big "X" emphasis on the 2 region
ax.text(2, 1.5, 'X', color=RED, fontsize=48, ha='center', va='center',
        fontweight='bold', alpha=0.0)  # already drawn via scatter

ax.set_xlim(-0.7, 5.7)
ax.set_ylim(-1.7, 3.0)
ax.set_yticks([])
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xticklabels(['0', '1', '2', '3', '4', '5+'])
ax.set_xlabel('OpsDB cardinality', color=SILVER, fontsize=12)
ax.set_title('Cardinality Landscape: Valid Regions and the Forbidden N=2',
             color=GOLD, fontsize=15, fontweight='bold', pad=18)

save(fig, 'infra09_07_cardinality.png')

# ================================================================
# FIG 8: AUTO-APPROVAL POLICY SPECTRUM
# Type: 3 (Threshold/Region)
# Shows: change risk on x-axis, approval mode bands, with example
# patterns placed on the spectrum. Text cannot show calibration as
# a continuous design space.
# ================================================================

fig, ax = plt.subplots(figsize=(16, 9))
fig.patch.set_facecolor(BG)
ax.set_facecolor(PAN)
for spine in ax.spines.values():
    spine.set_color(DIM)
    spine.set_linewidth(0.5)
ax.tick_params(colors=DIM, labelsize=9)

# X-axis: change risk (0 to 10 conceptual)
# Y-axis: 4 horizontal bands for approval modes

# Bands
bands = [
    (3.0, 4.0, GREEN,  'Auto-approve',
     'Routine, low-risk, declared-scope'),
    (2.0, 3.0, CYAN,   'Single approver',
     'Service owner or domain owner'),
    (1.0, 2.0, BLUE,   'Multi-approver',
     'Service + security + compliance'),
    (0.0, 1.0, ORANGE, 'Emergency only',
     'High-risk, post-hoc review required'),
]
for ymin, ymax, color, label, sub in bands:
    ax.axhspan(ymin, ymax, alpha=0.12, color=color)
    ax.text(-0.2, (ymin + ymax) / 2 + 0.10, label, color=color,
            fontsize=11, ha='right', va='center', fontweight='bold')
    ax.text(-0.2, (ymin + ymax) / 2 - 0.18, sub, color=SILVER,
            fontsize=8.5, ha='right', va='center', style='italic')

# Example patterns placed on the spectrum
# (risk_x, band_y_center, label, color)
examples = [
    (0.8, 3.5,  'Drift correction\n(non-prod, low-risk fields)',         GREEN),
    (2.2, 3.5,  'Scheduled credential\nrotation',                         GREEN),
    (3.8, 3.5,  'Routine reconciler\nconfig adjust',                      GREEN),
    (1.5, 2.5,  'Service config update\n(non-prod)',                      CYAN),
    (4.0, 2.5,  'New runner registration',                                CYAN),
    (5.5, 2.5,  'Production service\nconfig update',                      CYAN),
    (5.0, 1.5,  'Security policy change',                                 BLUE),
    (6.5, 1.5,  'Production database\nschema change',                     BLUE),
    (8.0, 1.5,  'Compliance scope change',                                BLUE),
    (8.5, 0.5,  'Schema steward\noverride',                               ORANGE),
    (9.5, 0.5,  'Production failover\n(time-pressured)',                  ORANGE),
]

for rx, ry, label, color in examples:
    ax.scatter([rx], [ry], s=140, c=color, edgecolors=WHITE,
               linewidth=1.5, zorder=5)
    # Offset label to avoid overlapping the marker; alternate above/below
    # by using a slight y offset
    offset_y = 0.18 if (rx * 10) % 2 == 0 else -0.20
    va = 'bottom' if offset_y > 0 else 'top'
    ax.text(rx, ry + offset_y, label, color=color, fontsize=8.5,
            ha='center', va=va)

# Risk axis labels at bottom
ax.text(0.5, -0.45, 'Low risk', color=GREEN, fontsize=10,
        ha='center', fontweight='bold')
ax.text(5.0, -0.45, 'Medium risk', color=CYAN, fontsize=10,
        ha='center', fontweight='bold')
ax.text(9.5, -0.45, 'High risk', color=ORANGE, fontsize=10,
        ha='center', fontweight='bold')

# Bottom note
ax.text(5.0, -0.95,
        'Each org calibrates the bands at Phase 5. Bias is narrow auto-approval initially, '
        'broader as confidence builds. The bands themselves are change-managed policy data.',
        color=DIM, fontsize=9, ha='center', style='italic')

ax.set_xlim(-2.6, 10.5)
ax.set_ylim(-1.2, 4.3)
ax.set_yticks([])
ax.set_xticks([])
ax.set_xlabel('Change risk (low to high)', color=SILVER, fontsize=12, labelpad=20)
ax.set_title('Auto-Approval Policy Spectrum: Calibrating Approval Mode by Change Risk',
             color=GOLD, fontsize=15, fontweight='bold', pad=18)

save(fig, 'infra09_08_approval_spectrum.png')

# ================================================================
# SUMMARY
# ================================================================

print("\nOPSDB-3 diagram script complete. 8 figures generated:")
print("  1. infra09_01_runner_growth.png       - Runner population growth across phases")
print("  2. infra09_02_n_opsdb_sync.png        - N-OpsDB sync architecture")
print("  3. infra09_03_dsnc_list_of_n.png      - DSNC list-of-N right vs wrong")
print("  4. infra09_04_library_rings.png       - Minimal library starting set")
print("  5. infra09_05_cutover.png             - Dev-to-operational cutover")
print("  6. infra09_06_schema_quality_cost.png - Schema quality cost over lifetime")
print("  7. infra09_07_cardinality.png         - Cardinality landscape (0/1/N, no 2)")
print("  8. infra09_08_approval_spectrum.png   - Auto-approval policy spectrum")
