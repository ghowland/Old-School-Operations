#!/usr/bin/env python3
"""
OPSDB OPSDB-9 Diagrams — A Taxonomy of Infrastructure Mechanisms, Properties, and Principles
8 figures covering the three-axis taxonomy, family relationships, and principle-driven structure.
Output: PNG files to ../figures/
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle, Wedge
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

def save(fig, filename):
    path = os.path.join(outdir, filename)
    fig.savefig(path, dpi=180, facecolor=BG, bbox_inches='tight', pad_inches=0.3)
    plt.close(fig)
    print("  Saved: %s" % filename)

def style_ax(ax, xlim=None, ylim=None):
    ax.set_facecolor(PAN)
    for spine in ax.spines.values():
        spine.set_color(DIM)
        spine.set_linewidth(0.5)
    ax.tick_params(colors=DIM, labelsize=9)
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

# ================================================================
# FIG 1: THREE-AXIS STRUCTURE
# Type: 5 (Connection / Integer Map)
# Shows: The load-bearing claim of the paper as a triangle of relationships
# ================================================================
fig, ax = plt.subplots(figsize=(16, 11))
ax.set_facecolor(BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 11)
ax.axis('off')

# Triangle vertices
mech_xy  = (8.0, 9.2)
prop_xy  = (3.0, 2.5)
princ_xy = (13.0, 2.5)

def axis_node(xy, label, sublabel, color, examples):
    x, y = xy
    box = FancyBboxPatch((x - 2.2, y - 1.0), 4.4, 2.0,
                         boxstyle='round,pad=0.1', facecolor=PAN,
                         edgecolor=color, linewidth=2.5)
    ax.add_patch(box)
    ax.text(x, y + 0.55, label, ha='center', va='center',
            fontsize=15, fontweight='bold', color=color)
    ax.text(x, y + 0.05, sublabel, ha='center', va='center',
            fontsize=10, color=WHITE, style='italic')
    ax.text(x, y - 0.55, examples, ha='center', va='center',
            fontsize=8, color=SILVER)

axis_node(mech_xy, 'MECHANISMS', 'what does work', GOLD,
          'Channel, Store, Reconciler, Quorum, Hasher...')#, GOLD)
axis_node(prop_xy, 'PROPERTIES', 'what holds', CYAN,
          'Idempotency, Durability, Convergence,\nOrdering, Availability...')#, CYAN)
axis_node(princ_xy, 'PRINCIPLES', 'rules for assembly', MAG,
          'Data primacy, 0/1/∞, Bound everything,\nFail closed/open...')#, MAG)

def labeled_arrow(start, end, label, color, offset=(0, 0), curve=0.0):
    arr = FancyArrowPatch(start, end, arrowstyle='->,head_width=8,head_length=10',
                           color=color, linewidth=2.0, alpha=0.8,
                           connectionstyle="arc3,rad=%f" % curve)
    ax.add_patch(arr)
    mx = (start[0] + end[0]) / 2 + offset[0]
    my = (start[1] + end[1]) / 2 + offset[1]
    ax.text(mx, my, label, ha='center', va='center',
            fontsize=10, color=color, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=color, linewidth=1))

# Mechanisms -> Properties (provides)
labeled_arrow((mech_xy[0] - 1.5, mech_xy[1] - 1.0),
              (prop_xy[0] + 1.0, prop_xy[1] + 1.0),
              'provides', GREEN, offset=(-0.3, 0.4), curve=0.15)

# Principles -> Mechanisms (governs)
labeled_arrow((princ_xy[0] - 1.0, princ_xy[1] + 1.0),
              (mech_xy[0] + 1.5, mech_xy[1] - 1.0),
              'governs', ORANGE, offset=(0.3, 0.4), curve=0.15)

# Principles -> Properties (constrains)
labeled_arrow((princ_xy[0] - 2.2, princ_xy[1] + 0.0),
              (prop_xy[0] + 2.2, prop_xy[1] + 0.0),
              'constrains', PURPLE, offset=(0, 0.4), curve=-0.2)

# Worked example footnote inside axes
ax.text(8.0, 0.6,
        'Example:  A Journal (mechanism) provides Durability and Auditability (properties)\n'
        'when configured under "bound everything" and "single source of truth" (principles).',
        ha='center', va='center', fontsize=10, color=SILVER, style='italic',
        bbox=dict(boxstyle='round,pad=0.5', facecolor=PAN, edgecolor=DIM, linewidth=1))

ax.text(8.0, 10.5, 'The Three-Axis Structure of Infrastructure Engineering',
        ha='center', va='center', fontsize=16, fontweight='bold', color=GOLD)

save(fig, 'infra1_01_three_axis_triangle.png')

# ================================================================
# FIG 2: MECHANISM × PROPERTY COVERAGE MATRIX
# Type: 6 (Comparison Bar Chart variant — coverage heatmap)
# Shows: Which mechanism families address which property bands
# ================================================================
families = [
    'Information movement',
    'Selection',
    'Representation',
    'Storage',
    'Versioning',
    'Lifecycle',
    'Sensing',
    'Control loop',
    'Gating',
    'Allocation',
    'Coordination',
    'Transformation',
    'Resilience'
]

properties = [
    'Idempotency', 'Atomicity', 'Durability', 'Consistency-data', 'Integrity',
    'Authenticity', 'Confidentiality', 'Determinism', 'Convergence', 'Liveness',
    'Availability', 'Boundedness', 'Isolation', 'Reversibility', 'Consistency-replica',
    'Ordering', 'Locality', 'Stability', 'Failure transp.', 'Observability', 'Auditability'
]

# Coverage matrix: 2 = primary, 1 = secondary, 0 = none
# Rows: families (13), Cols: properties (21)
coverage = np.zeros((len(families), len(properties)), dtype=int)
def setp(fam, prop, val):
    fi = families.index(fam)
    pj = properties.index(prop)
    coverage[fi, pj] = val

# Information movement
setp('Information movement', 'Locality', 1)
setp('Information movement', 'Failure transp.', 1)
setp('Information movement', 'Ordering', 1)
setp('Information movement', 'Durability', 2)
setp('Information movement', 'Consistency-replica', 2)
setp('Information movement', 'Availability', 2)

# Selection
setp('Selection', 'Determinism', 2)
setp('Selection', 'Locality', 2)
setp('Selection', 'Stability', 2)
setp('Selection', 'Ordering', 1)
setp('Selection', 'Idempotency', 1)

# Representation
setp('Representation', 'Integrity', 2)
setp('Representation', 'Authenticity', 2)
setp('Representation', 'Confidentiality', 2)
setp('Representation', 'Consistency-data', 2)
setp('Representation', 'Determinism', 2)
setp('Representation', 'Observability', 1)

# Storage
setp('Storage', 'Durability', 2)
setp('Storage', 'Consistency-data', 2)
setp('Storage', 'Auditability', 2)
setp('Storage', 'Boundedness', 2)
setp('Storage', 'Locality', 2)
setp('Storage', 'Reversibility', 2)
setp('Storage', 'Ordering', 1)
setp('Storage', 'Availability', 1)
setp('Storage', 'Observability', 1)

# Versioning
setp('Versioning', 'Reversibility', 2)
setp('Versioning', 'Auditability', 2)
setp('Versioning', 'Ordering', 2)
setp('Versioning', 'Stability', 1)
setp('Versioning', 'Convergence', 2)
setp('Versioning', 'Consistency-replica', 1)

# Lifecycle
setp('Lifecycle', 'Boundedness', 2)
setp('Lifecycle', 'Liveness', 2)
setp('Lifecycle', 'Availability', 1)
setp('Lifecycle', 'Failure transp.', 1)

# Sensing
setp('Sensing', 'Observability', 2)
setp('Sensing', 'Auditability', 1)
setp('Sensing', 'Failure transp.', 1)

# Control loop
setp('Control loop', 'Convergence', 2)
setp('Control loop', 'Liveness', 2)
setp('Control loop', 'Failure transp.', 2)
setp('Control loop', 'Boundedness', 1)

# Gating
setp('Gating', 'Confidentiality', 2)
setp('Gating', 'Integrity', 2)
setp('Gating', 'Authenticity', 2)
setp('Gating', 'Boundedness', 2)
setp('Gating', 'Consistency-data', 1)

# Allocation
setp('Allocation', 'Boundedness', 2)
setp('Allocation', 'Locality', 2)
setp('Allocation', 'Stability', 2)

# Coordination
setp('Coordination', 'Atomicity', 2)
setp('Coordination', 'Isolation', 2)
setp('Coordination', 'Ordering', 2)
setp('Coordination', 'Consistency-replica', 2)
setp('Coordination', 'Durability', 1)
setp('Coordination', 'Liveness', 1)

# Transformation
setp('Transformation', 'Determinism', 2)
setp('Transformation', 'Boundedness', 1)

# Resilience
setp('Resilience', 'Availability', 2)
setp('Resilience', 'Liveness', 2)
setp('Resilience', 'Failure transp.', 2)
setp('Resilience', 'Convergence', 1)
setp('Resilience', 'Boundedness', 1)
setp('Resilience', 'Stability', 1)

fig, ax = plt.subplots(figsize=(18, 10))
ax.set_facecolor(BG)

# Custom 3-color colormap: 0 = panel, 1 = cyan dim, 2 = gold bright
for i in range(len(families)):
    for j in range(len(properties)):
        v = coverage[i, j]
        if v == 0:
            color = PAN
            alpha = 1.0
        elif v == 1:
            color = CYAN
            alpha = 0.45
        else:
            color = GOLD
            alpha = 0.95
        rect = Rectangle((j, len(families) - 1 - i), 1, 1,
                         facecolor=color, alpha=alpha,
                         edgecolor=DIM, linewidth=0.5)
        ax.add_patch(rect)
        if v == 2:
            ax.text(j + 0.5, len(families) - 1 - i + 0.5, '★',
                    ha='center', va='center', fontsize=12, color=BG, fontweight='bold')
        elif v == 1:
            ax.text(j + 0.5, len(families) - 1 - i + 0.5, '○',
                    ha='center', va='center', fontsize=10, color=WHITE)

ax.set_xlim(0, len(properties))
ax.set_ylim(0, len(families))
ax.set_xticks(np.arange(len(properties)) + 0.5)
ax.set_xticklabels(properties, rotation=55, ha='right', fontsize=9, color=WHITE)
ax.set_yticks(np.arange(len(families)) + 0.5)
ax.set_yticklabels(list(reversed(families)), fontsize=10, color=WHITE)
ax.tick_params(length=0)

for spine in ax.spines.values():
    spine.set_color(DIM)
    spine.set_linewidth(0.5)

# Legend
legend_y = -1.5
ax.add_patch(Rectangle((0.5, legend_y), 0.7, 0.7, facecolor=GOLD, alpha=0.95,
                        edgecolor=DIM, linewidth=0.5))
ax.text(0.85, legend_y + 0.35, '★', ha='center', va='center', fontsize=12, color=BG, fontweight='bold')
ax.text(1.5, legend_y + 0.35, 'primary property the family is built to provide',
        fontsize=10, color=WHITE, va='center')

ax.add_patch(Rectangle((10.0, legend_y), 0.7, 0.7, facecolor=CYAN, alpha=0.45,
                        edgecolor=DIM, linewidth=0.5))
ax.text(10.35, legend_y + 0.35, '○', ha='center', va='center', fontsize=10, color=WHITE)
ax.text(11.0, legend_y + 0.35, 'secondary contribution', fontsize=10, color=WHITE, va='center')

ax.set_title('Mechanism Families × Properties — Coverage Matrix',
             fontsize=15, fontweight='bold', color=GOLD, pad=18)

ax.text(len(properties) / 2, len(families) + 0.6,
        'Clusters reveal which families dominate which property bands. Empty rows/columns mark intentional separations of concern.',
        ha='center', va='center', fontsize=9, color=SILVER, style='italic')

save(fig, 'infra1_02_mechanism_property_matrix.png')

# ================================================================
# FIG 3: PROPERTY COMPOSITION GRAPH
# Type: 5 (Connection Map)
# Shows: Which properties are atomic vs composed from others
# ================================================================
fig, ax = plt.subplots(figsize=(17, 11))
ax.set_facecolor(BG)
ax.set_xlim(0, 17)
ax.set_ylim(0, 11)
ax.axis('off')

# Atomic properties (primitives) — bottom row
atomic_props = [
    ('Persistence',     2.0, 1.5),
    ('Replication',     5.0, 1.5),
    ('Ordering',        8.0, 1.5),
    ('Idempotency',    11.0, 1.5),
    ('Boundedness',    14.0, 1.5),
]

# Composed properties — middle row
composed_props = [
    ('Durability',      3.5, 5.0),
    ('Atomicity',       6.5, 5.0),
    ('Convergence',     9.5, 5.0),
    ('Isolation',      12.5, 5.0),
]

# Higher-order properties — top row
higher_props = [
    ('Availability',    4.0, 8.5),
    ('Consistency\n(replica)', 8.5, 8.5),
    ('Failure\ntransparency', 13.0, 8.5),
]

def draw_node(x, y, label, color, w=2.0, h=0.9):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle='round,pad=0.05', facecolor=PAN,
                         edgecolor=color, linewidth=2.0)
    ax.add_patch(box)
    ax.text(x, y, label, ha='center', va='center',
            fontsize=10, color=color, fontweight='bold')

for name, x, y in atomic_props:
    draw_node(x, y, name, CYAN, w=2.2, h=0.85)
for name, x, y in composed_props:
    draw_node(x, y, name, GOLD, w=2.2, h=0.9)
for name, x, y in higher_props:
    draw_node(x, y, name, MAG, w=2.4, h=1.0)

def comp_arrow(src, dst, color, alpha=0.55):
    arr = FancyArrowPatch(src, dst, arrowstyle='->,head_width=5,head_length=7',
                          color=color, linewidth=1.4, alpha=alpha,
                          connectionstyle="arc3,rad=0.05")
    ax.add_patch(arr)

# Atomic -> Composed
# Durability requires Persistence + Replication
comp_arrow((2.0, 1.95), (3.2, 4.55), GREEN)
comp_arrow((5.0, 1.95), (3.8, 4.55), GREEN)
# Atomicity requires Ordering + (coordination — abstracted) + Idempotency
comp_arrow((8.0, 1.95), (6.5, 4.55), GREEN)
comp_arrow((11.0, 1.95), (6.8, 4.55), GREEN)
# Convergence requires Idempotency + Replication
comp_arrow((11.0, 1.95), (9.5, 4.55), GREEN)
comp_arrow((5.0, 1.95), (9.2, 4.55), GREEN)
# Isolation requires Ordering + Boundedness
comp_arrow((8.0, 1.95), (12.5, 4.55), GREEN)
comp_arrow((14.0, 1.95), (12.8, 4.55), GREEN)

# Composed -> Higher
# Availability uses Durability + Replication
comp_arrow((3.5, 5.45), (4.0, 8.0), ORANGE)
comp_arrow((5.0, 1.95), (4.0, 8.0), ORANGE, alpha=0.35)
# Consistency-replica uses Atomicity + Convergence + Ordering
comp_arrow((6.5, 5.45), (8.5, 8.0), ORANGE)
comp_arrow((9.5, 5.45), (8.5, 8.0), ORANGE)
# Failure transparency uses Convergence + Isolation
comp_arrow((9.5, 5.45), (13.0, 8.0), ORANGE)
comp_arrow((12.5, 5.45), (13.0, 8.0), ORANGE)

# Tier labels
ax.text(0.4, 1.5, 'Atomic\nproperties', fontsize=10, color=CYAN, fontweight='bold',
        ha='left', va='center', style='italic')
ax.text(0.4, 5.0, 'Composed\nproperties', fontsize=10, color=GOLD, fontweight='bold',
        ha='left', va='center', style='italic')
ax.text(0.4, 8.5, 'Higher-order\nproperties', fontsize=10, color=MAG, fontweight='bold',
        ha='left', va='center', style='italic')

# Legend strips
ax.plot([15.5, 16.5], [1.5, 1.5], color=CYAN, linewidth=3)
ax.plot([15.5, 16.5], [5.0, 5.0], color=GOLD, linewidth=3)
ax.plot([15.5, 16.5], [8.5, 8.5], color=MAG, linewidth=3)

ax.text(8.5, 10.4, 'Property Composition — What Stands Alone, What Is Built',
        ha='center', va='center', fontsize=15, fontweight='bold', color=GOLD)
ax.text(8.5, 9.8, 'Green arrows = composition dependency. Higher-order properties are not primitive; they require multiple atomic properties to hold simultaneously.',
        ha='center', va='center', fontsize=9, color=SILVER, style='italic')

save(fig, 'infra1_03_property_composition.png')

# ================================================================
# FIG 4: EDGE-TRIGGERED VS LEVEL-TRIGGERED CONTROL LOOPS
# Type: 4 (Geometric Cross-Section / Comparison)
# Shows: Why level-triggered is robust to missed events
# ================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9),
                                 gridspec_kw={'wspace': 0.30})
fig.patch.set_facecolor(BG)

for ax in (ax1, ax2):
    ax.set_facecolor(PAN)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    for spine in ax.spines.values():
        spine.set_visible(False)

# --- LEFT PANEL: Edge-triggered ---
ax1.text(5.0, 9.5, 'Edge-triggered  (Reactor)',
         ha='center', va='center', fontsize=14, fontweight='bold', color=ORANGE)
ax1.text(5.0, 9.0, 'reacts to events; missed events become missed work',
         ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# Source: state changes over time
ax1.add_patch(FancyBboxPatch((0.5, 6.5), 9.0, 1.2,
                              boxstyle='round,pad=0.05', facecolor=BG,
                              edgecolor=DIM, linewidth=1))
ax1.text(0.7, 7.95, 'state changes (events)', fontsize=9, color=SILVER, style='italic')

# Plot a series of edge events
event_times = [1.5, 2.8, 4.0, 5.3, 6.6, 8.0]
delivered = [True, True, False, True, False, True]
for t, d in zip(event_times, delivered):
    color = GREEN if d else RED
    ax1.plot([t, t], [6.6, 7.6], color=color, linewidth=2.5, alpha=0.9)
    if not d:
        ax1.text(t, 6.4, 'dropped', fontsize=7, color=RED, ha='center', style='italic')

# Handler row
ax1.add_patch(FancyBboxPatch((0.5, 4.2), 9.0, 1.0,
                              boxstyle='round,pad=0.05', facecolor=BG,
                              edgecolor=ORANGE, linewidth=1.5))
ax1.text(0.7, 5.45, 'handler invocations', fontsize=9, color=ORANGE, style='italic')
for t, d in zip(event_times, delivered):
    if d:
        ax1.add_patch(Circle((t, 4.7), 0.18, facecolor=ORANGE,
                              edgecolor=WHITE, linewidth=1.5))

# Arrows from events to handlers
for t, d in zip(event_times, delivered):
    if d:
        arr = FancyArrowPatch((t, 6.5), (t, 4.92),
                              arrowstyle='->', color=ORANGE,
                              linewidth=1, alpha=0.6)
        ax1.add_patch(arr)

# Resulting state — diverged
ax1.add_patch(FancyBboxPatch((0.5, 1.5), 9.0, 1.6,
                              boxstyle='round,pad=0.05', facecolor=BG,
                              edgecolor=RED, linewidth=1.5))
ax1.text(0.7, 2.85, 'final state vs. desired', fontsize=9, color=RED, style='italic')
ax1.text(5.0, 2.3, 'Δ',
         ha='center', va='center', fontsize=20, color=RED, fontweight='bold')
ax1.text(5.0, 1.85, 'state diverges — missed events leave gap',
         ha='center', va='center', fontsize=9, color=RED)

# Failure indicator legend
ax1.add_patch(Rectangle((0.5, 0.4), 0.4, 0.25, facecolor=GREEN, alpha=0.9))
ax1.text(1.05, 0.52, 'event delivered', fontsize=8, color=WHITE, va='center')
ax1.add_patch(Rectangle((4.5, 0.4), 0.4, 0.25, facecolor=RED, alpha=0.9))
ax1.text(5.05, 0.52, 'event dropped (network, restart, race)', fontsize=8, color=WHITE, va='center')

# --- RIGHT PANEL: Level-triggered ---
ax2.text(5.0, 9.5, 'Level-triggered  (Reconciler)',
         ha='center', va='center', fontsize=14, fontweight='bold', color=GREEN)
ax2.text(5.0, 9.0, 'reacts to current state; missed events tolerated',
         ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# Source: state changes over time
ax2.add_patch(FancyBboxPatch((0.5, 6.5), 9.0, 1.2,
                              boxstyle='round,pad=0.05', facecolor=BG,
                              edgecolor=DIM, linewidth=1))
ax2.text(0.7, 7.95, 'state changes (events also fire here)', fontsize=9, color=SILVER, style='italic')

for t, d in zip(event_times, delivered):
    color = GREEN if d else RED
    ax2.plot([t, t], [6.6, 7.6], color=color, linewidth=2.5, alpha=0.9)

# Periodic comparison ticks (the loop)
loop_times = [1.0, 2.5, 4.0, 5.5, 7.0, 8.5]
ax2.add_patch(FancyBboxPatch((0.5, 4.2), 9.0, 1.0,
                              boxstyle='round,pad=0.05', facecolor=BG,
                              edgecolor=GREEN, linewidth=1.5))
ax2.text(0.7, 5.45, 'reconcile cycles  (compare desired vs actual)',
         fontsize=9, color=GREEN, style='italic')
for t in loop_times:
    ax2.add_patch(Circle((t, 4.7), 0.18, facecolor=GREEN,
                          edgecolor=WHITE, linewidth=1.5))
    arr = FancyArrowPatch((t, 4.92), (t, 4.2),
                          arrowstyle='->', color=GREEN,
                          linewidth=0.8, alpha=0.0)
    ax2.add_patch(arr)

# Loop arrow showing it cycles forever
arr = FancyArrowPatch((9.5, 4.7), (0.5, 4.7),
                      arrowstyle='->', color=GREEN,
                      linewidth=1, alpha=0.4,
                      connectionstyle="arc3,rad=-0.4")
ax2.add_patch(arr)
ax2.text(5.0, 3.85, 'loop forever', fontsize=8, color=GREEN, ha='center', style='italic')

# Resulting state — converged
ax2.add_patch(FancyBboxPatch((0.5, 1.5), 9.0, 1.6,
                              boxstyle='round,pad=0.05', facecolor=BG,
                              edgecolor=GREEN, linewidth=1.5))
ax2.text(0.7, 2.85, 'final state vs. desired', fontsize=9, color=GREEN, style='italic')
ax2.text(5.0, 2.3, '=',
         ha='center', va='center', fontsize=20, color=GREEN, fontweight='bold')
ax2.text(5.0, 1.85, 'state converges — next cycle catches missed events',
         ha='center', va='center', fontsize=9, color=GREEN)

# Footnote bar
ax2.text(5.0, 0.5,
         'Principle  §5.3:  "level-triggered over edge-triggered"',
         ha='center', va='center', fontsize=9, color=GOLD, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.4', facecolor=BG, edgecolor=GOLD, linewidth=1))

fig.suptitle('Edge-triggered vs. Level-triggered Control Loops',
             fontsize=16, fontweight='bold', color=GOLD, y=0.98)

save(fig, 'infra1_04_edge_vs_level_triggered.png')

# ================================================================
# FIG 5: MECHANISM CARDINALITY LANDSCAPE (0/1/∞)
# Type: 2 (Scale / Landscape)
# Shows: Where each native mechanism sits on the 0/1/∞ axis
# ================================================================
fig, ax = plt.subplots(figsize=(18, 10))
ax.set_facecolor(BG)
ax.set_xlim(0, 18)
ax.set_ylim(0, 10)
ax.axis('off')

# Three regions
ax.add_patch(Rectangle((0.5, 1.0), 4.5, 7.5, facecolor=DIM, alpha=0.10,
                        edgecolor=DIM, linewidth=1))
ax.add_patch(Rectangle((5.0, 1.0), 5.5, 7.5, facecolor=GOLD, alpha=0.08,
                        edgecolor=GOLD, linewidth=1))
ax.add_patch(Rectangle((10.5, 1.0), 7.0, 7.5, facecolor=CYAN, alpha=0.08,
                        edgecolor=CYAN, linewidth=1))

# Region headers
ax.text(2.75, 8.2, '0', ha='center', fontsize=26, color=DIM, fontweight='bold')
ax.text(7.75, 8.2, '1  (or few)', ha='center', fontsize=20, color=GOLD, fontweight='bold')
ax.text(14.0, 8.2, '∞', ha='center', fontsize=26, color=CYAN, fontweight='bold')

ax.text(2.75, 7.6, 'absent / removed by automation',
        ha='center', fontsize=9, color=SILVER, style='italic')
ax.text(7.75, 7.6, 'centralized authority, single primary',
        ha='center', fontsize=9, color=SILVER, style='italic')
ax.text(14.0, 7.6, 'horizontally scalable, no built-in cap',
        ha='center', fontsize=9, color=SILVER, style='italic')

# Mechanisms placed in regions
zero_region = [
    ('removed work',  2.75, 6.6),
    ('eliminated',    2.75, 6.0),
    ('class', 2.75, 5.4),
]

one_region = [
    ('Lock',           6.5, 6.8),
    ('Election leader', 6.5, 6.2),
    ('Sequencer',      6.5, 5.6),
    ('Quorum',         8.8, 6.8),
    ('Authoritative\nStore', 8.8, 6.0),
    ('Schema',         8.8, 5.2),
    ('Naming\nconvention', 6.5, 4.6),
    ('Snapshot\n(point-in-time)', 8.8, 4.4),
    ('Reference\n(canonical)', 6.5, 3.6),
    ('Reconciler\n(active leader)', 8.8, 3.2),
    ('Election',       6.5, 2.6),
    ('Barrier',        8.8, 2.2),
]

inf_region = [
    ('Channel',         11.5, 6.8),
    ('Cache replica',   13.5, 6.8),
    ('CDN edge',        15.5, 6.8),
    ('Replicator\ntargets', 11.5, 5.8),
    ('Read replica',    13.5, 5.8),
    ('Anycast PoP',     15.5, 5.8),
    ('Pool member',     11.5, 4.8),
    ('Sharder bucket',  13.5, 4.8),
    ('Watch\nsubscriber', 15.5, 4.8),
    ('Heartbeat\nsource', 11.5, 3.8),
    ('Probe target',    13.5, 3.8),
    ('Workqueue\nworker', 15.5, 3.8),
    ('Counter',         11.5, 2.8),
    ('Filter\ninstance', 13.5, 2.8),
    ('Gauge',           15.5, 2.8),
]

def place_mech(items, color):
    for name, x, y in items:
        ax.add_patch(FancyBboxPatch((x - 0.85, y - 0.32), 1.7, 0.55,
                                     boxstyle='round,pad=0.05', facecolor=PAN,
                                     edgecolor=color, linewidth=1.2))
        ax.text(x, y, name, ha='center', va='center', fontsize=8, color=WHITE)

place_mech(zero_region, DIM)
place_mech(one_region, GOLD)
place_mech(inf_region, CYAN)

# "There is no 2" arrow between 1 and ∞
ax.add_patch(FancyArrowPatch((10.5, 1.4), (10.5, 1.4),
                              arrowstyle='-', color=RED, linewidth=2))
ax.plot([10.5, 10.5], [1.0, 8.5], color=RED, linewidth=1.5, linestyle='--', alpha=0.6)
ax.text(10.5, 0.55, 'There is no 2.', ha='center', va='center',
        fontsize=11, color=RED, fontweight='bold', style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=RED, linewidth=1))

ax.text(9.0, 9.4, 'Mechanism Cardinality Landscape  —  the 0 / 1 / ∞ Principle',
        ha='center', va='center', fontsize=15, fontweight='bold', color=GOLD)

save(fig, 'infra1_05_cardinality_landscape.png')

# ================================================================
# FIG 6: WRAP/UNWRAP CONCENTRIC LAYER STACK
# Type: 4 (Geometric Cross-Section)
# Shows: Encoding as one ring among many in a stack of wrapping
# ================================================================
fig, ax = plt.subplots(figsize=(15, 13))
ax.set_facecolor(BG)
ax.set_xlim(-7.5, 7.5)
ax.set_ylim(-7.5, 7.5)
ax.set_aspect('equal')
ax.axis('off')

# Concentric layers from outside in
layers = [
    (7.0, 'Routing wrap',     'VPN / VXLAN / GRE — adds delivery context',     PURPLE),
    (6.0, 'Transport framing', 'TCP / chunked HTTP — adds boundaries',         BLUE),
    (5.0, 'Secure wrap',      'TLS / IPSEC — confidentiality + integrity + authenticity', RED),
    (4.0, 'Compression',      'gzip / zstd — reduces size',                    ORANGE),
    (3.0, 'Encoding',         'JSON / protobuf / MessagePack — representation', GOLD),
    (2.0, 'Schema',           'declared structure',                            CYAN),
    (1.0, 'Payload',          'logical content',                               GREEN),
]

# Draw rings outermost first, with decreasing alpha for depth
for i, (r, name, desc, color) in enumerate(layers):
    alpha = 0.30 - i * 0.025
    if alpha < 0.10:
        alpha = 0.10
    ring = Circle((0, 0), r, facecolor=color, alpha=alpha,
                   edgecolor=color, linewidth=1.5)
    ax.add_patch(ring)

# Innermost solid payload
ax.add_patch(Circle((0, 0), 1.0, facecolor=GREEN, alpha=0.85,
                     edgecolor=WHITE, linewidth=1.5))
ax.text(0, 0, 'PAYLOAD', ha='center', va='center', fontsize=11,
        color=BG, fontweight='bold')

# External labels with leader lines (right side)
label_x = 7.8
for r, name, desc, color in layers:
    if r == 1.0:
        continue  # payload labelled inside
    # Leader line from ring at 30 degrees up-right
    angle = np.pi / 6
    px = r * np.cos(angle)
    py = r * np.sin(angle)
    # Stagger label y for legibility
    label_y = py + (r - 3.0) * 0.15
    ax.plot([px, label_x - 0.1], [py, label_y], color=color,
            linewidth=0.8, alpha=0.6)
    ax.add_patch(Circle((px, py), 0.06, facecolor=color, edgecolor=WHITE, linewidth=0.6))
    ax.text(label_x, label_y, name, ha='left', va='center', fontsize=10,
            color=color, fontweight='bold')
    ax.text(label_x, label_y - 0.32, desc, ha='left', va='center',
            fontsize=8, color=SILVER, style='italic')

# Wrap arrow (down) and unwrap arrow (up) on the left
arr_down = FancyArrowPatch((-7.0, 6.5), (-7.0, -6.5),
                            arrowstyle='->,head_width=8,head_length=10',
                            color=GOLD, linewidth=2, alpha=0.7)
ax.add_patch(arr_down)
ax.text(-7.3, 0, 'WRAP', rotation=90, ha='center', va='center',
        fontsize=11, color=GOLD, fontweight='bold')

arr_up = FancyArrowPatch((-6.3, -6.5), (-6.3, 6.5),
                          arrowstyle='->,head_width=8,head_length=10',
                          color=CYAN, linewidth=2, alpha=0.7)
ax.add_patch(arr_up)
ax.text(-6.0, 0, 'UNWRAP', rotation=90, ha='center', va='center',
        fontsize=11, color=CYAN, fontweight='bold')

ax.text(0, 7.4, 'Wrap / Unwrap — Encoding is One Layer Among Many',
        ha='center', va='center', fontsize=15, fontweight='bold', color=GOLD)
ax.text(0, -7.0,
        'Each ring adds context: structure, framing, security, routing, compression. Encoding/decoding (gold) is the case where wrapping is purely representational.',
        ha='center', va='center', fontsize=9, color=SILVER, style='italic')

save(fig, 'infra1_06_wrap_unwrap_layers.png')

# ================================================================
# FIG 7: STORAGE FAMILY TIMESCALE AXIS
# Type: 2 (Scale / Landscape)
# Shows: Log-scale retention from ns to permanent
# ================================================================
fig, ax = plt.subplots(figsize=(18, 9))
ax.set_facecolor(PAN)
ax.set_xlim(-9.5, 12)
ax.set_ylim(-3.5, 4.5)

# Log-time landmarks (powers of 10 seconds)
landmarks = [
    (-9, '1 ns',   'CPU\nregister'),
    (-7, '100 ns', 'L1 cache'),
    (-5, '10 µs',  'RAM read'),
    (-3, '1 ms',   'SSD'),
    ( 0, '1 sec',  ''),
    ( 2, '100 sec', ''),
    ( 4, '3 hr',   ''),
    ( 6, '12 days', ''),
    ( 8, '3 yrs',  ''),
    (10, '300 yrs', ''),
    (11, '∞',      'permanent'),
]

# Baseline axis
ax.axhline(0, color=DIM, linewidth=1.5)

for x, label, sublabel in landmarks:
    ax.plot([x, x], [-0.2, 0.2], color=DIM, linewidth=1)
    ax.text(x, -0.55, label, ha='center', fontsize=9, color=SILVER)
    if sublabel:
        ax.text(x, -1.05, sublabel, ha='center', fontsize=8, color=DIM, style='italic')

# Storage mechanisms placed as horizontal spans
# (x_start, x_end, y, name, color)
mechanisms = [
    (-9.5, -7,   3.6, 'Buffer (CPU register / L1)',         CYAN),
    (-7,   -3,   3.0, 'Buffer (RAM, ring buffer)',          CYAN),
    (-5,    2,   2.4, 'Cache  (in-memory)',                 BLUE),
    (-3,    6,   1.8, 'Cache  (disk, CDN edge)',            BLUE),
    (-3,   11.5, 1.2, 'Store  (durable, source of truth)',  GOLD),
    (-3,   11.5, 0.6, 'Journal  (append-only, replay)',     ORANGE),
    ( 0,   11.5, -1.6, 'Snapshot  (point-in-time)',         GREEN),
    (-3,    8,   -2.2, 'Log  (retention-bounded)',          PURPLE),
    ( 0,    7,   -2.8, 'Tombstone  (until GC)',             MAG),
]

for x0, x1, y, name, color in mechanisms:
    ax.add_patch(FancyBboxPatch((x0, y - 0.18), x1 - x0, 0.36,
                                 boxstyle='round,pad=0.02',
                                 facecolor=color, alpha=0.35,
                                 edgecolor=color, linewidth=1.5))
    ax.text(x0 + 0.15, y, name, ha='left', va='center',
            fontsize=10, color=WHITE, fontweight='bold')

# Volatile vs durable boundary
ax.axvline(-3, color=RED, linewidth=1.2, linestyle='--', alpha=0.5)
ax.text(-3, 4.2, 'volatility threshold\n(power-loss boundary)',
        ha='center', va='top', fontsize=8, color=RED, style='italic')

ax.set_xlabel('log₁₀(retention or access timescale, seconds)',
              fontsize=11, color=SILVER)
ax.set_xticks([x for x, _, _ in landmarks])
ax.set_xticklabels([x for x, _, _ in landmarks])
ax.tick_params(colors=DIM, labelsize=9)
ax.set_yticks([])

for spine in ax.spines.values():
    spine.set_color(DIM)
    spine.set_linewidth(0.5)

ax.set_title('Storage Family — Retention Timescale Spectrum',
             fontsize=15, fontweight='bold', color=GOLD, pad=15)

save(fig, 'infra1_07_storage_timescale.png')

# ================================================================
# FIG 8: DURABILITY PROVISION SPECTRUM
# Type: 3 (Threshold / Region)
# Shows: Configuration levels with crash/node/DC/region survival thresholds
# ================================================================
fig, ax = plt.subplots(figsize=(18, 10))
ax.set_facecolor(PAN)

# X axis: durability strength (configuration level)
# Y axis: latency cost (relative)
levels = [
    (1, 'in-memory only',          'no persistence',                         0.05, RED),
    (2, 'disk write, no fsync',    'OS may buffer, lost on crash',          0.3,  RED),
    (3, 'fsync per commit',        'survives process and machine crash',     1.5,  ORANGE),
    (4, 'fsync + replication\n(async, 1 replica)', 'survives node loss\n(small loss window)', 2.0, GOLD),
    (5, 'fsync + sync replication\n(quorum)', 'survives node loss',          5.0, GOLD),
    (6, 'multi-DC sync',           'survives DC loss',                       18.0, GREEN),
    (7, 'multi-region sync',       'survives region loss',                   80.0, GREEN),
]

# Draw threshold regions (horizontal bands by durability tier)
threshold_regions = [
    (0.5, 2.5, RED,    0.10, 'volatile region — power loss = data loss'),
    (2.5, 3.5, ORANGE, 0.10, 'crash-survivable — single node only'),
    (3.5, 5.5, GOLD,   0.10, 'node-survivable — replicated'),
    (5.5, 6.5, GREEN,  0.10, 'DC-survivable'),
    (6.5, 7.5, PURPLE, 0.10, 'region-survivable'),
]

for x0, x1, color, alpha, label in threshold_regions:
    ax.axvspan(x0, x1, facecolor=color, alpha=alpha)
    ax.text((x0 + x1) / 2, 200, label, ha='center', va='top',
            fontsize=8, color=color, style='italic', rotation=0)

# Plot the curve: latency cost rising with durability
xs = [lv[0] for lv in levels]
ys = [lv[3] for lv in levels]
ax.plot(xs, ys, color=GOLD, linewidth=2.5, alpha=0.85,
        marker='o', markersize=11, markeredgecolor=WHITE, markeredgewidth=1.5)

# Annotate each point
for level_n, name, surv, lat, color in levels:
    ax.annotate(name, xy=(level_n, lat),
                xytext=(level_n, lat * 3.5 if lat > 0.5 else lat + 1.0),
                ha='center', fontsize=9, color=WHITE, fontweight='bold',
                arrowprops=dict(arrowstyle='-', color=DIM, lw=0.7, alpha=0.7))
    ax.text(level_n, lat / 2.5 if lat > 0.5 else lat * 0.4, surv,
            ha='center', fontsize=7, color=SILVER, style='italic')

# Horizontal threshold lines for survival classes
crash_y = 1.5
node_y = 2.0
dc_y = 18.0
region_y = 80.0

ax.axhline(crash_y, color=ORANGE, linewidth=1, linestyle='--', alpha=0.4)
ax.axhline(dc_y, color=GREEN, linewidth=1, linestyle='--', alpha=0.4)

ax.set_xlim(0.3, 7.7)
ax.set_ylim(0.02, 300)
ax.set_yscale('log')
ax.set_xticks(xs)
ax.set_xticklabels(['L%d' % n for n in xs], fontsize=10, color=WHITE)
ax.set_xlabel('Durability provision level', fontsize=11, color=SILVER)
ax.set_ylabel('Relative commit latency  (log scale, ms)', fontsize=11, color=SILVER)
ax.tick_params(colors=DIM, labelsize=9)

for spine in ax.spines.values():
    spine.set_color(DIM)
    spine.set_linewidth(0.5)

# Legend / key callout
key_text = (
    'Each level claims survival through a strictly larger failure set\n'
    'than the previous, at strictly higher commit latency.\n'
    'There is no free durability; the property is bought.'
)
ax.text(0.55, 130, key_text, fontsize=9, color=GOLD,
        bbox=dict(boxstyle='round,pad=0.4', facecolor=BG, edgecolor=GOLD, linewidth=1),
        va='top')

ax.set_title('Durability Provision Spectrum — From In-Memory to Multi-Region',
             fontsize=15, fontweight='bold', color=GOLD, pad=15)

save(fig, 'infra1_08_durability_spectrum.png')

# ================================================================
# SUMMARY
# ================================================================
print("\nAll 8 figures saved to: %s" % outdir)
print("  infra1_01_three_axis_triangle.png")
print("  infra1_02_mechanism_property_matrix.png")
print("  infra1_03_property_composition.png")
print("  infra1_04_edge_vs_level_triggered.png")
print("  infra1_05_cardinality_landscape.png")
print("  infra1_06_wrap_unwrap_layers.png")
print("  infra1_07_storage_timescale.png")
print("  infra1_08_durability_spectrum.png")
