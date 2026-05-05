#!/usr/bin/env python3
"""
HOWL INFRA-2 Diagrams — OpsDB Design
8 figures covering the three-population model, cardinality, API-as-perimeter,
change-set lifecycle, architectural layering, freshness, investigation flow,
and the local-replica pattern.
Output: PNG files to ../figures/
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle, Wedge, Polygon
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

# ================================================================
# FIG 1: THREE POPULATIONS ON ONE SUBSTRATE
# Type: 5 (Connection Map)
# Shows: Humans, automation, auditors converging on the OpsDB
# ================================================================
fig, ax = plt.subplots(figsize=(16, 11))
ax.set_facecolor(BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 11)
ax.axis('off')

# OpsDB at center
opsdb_x, opsdb_y = 8.0, 5.5
opsdb_box = FancyBboxPatch((opsdb_x - 2.0, opsdb_y - 1.0), 4.0, 2.0,
                            boxstyle='round,pad=0.1', facecolor=PAN,
                            edgecolor=GOLD, linewidth=3)
ax.add_patch(opsdb_box)
ax.text(opsdb_x, opsdb_y + 0.45, 'OpsDB', ha='center', va='center',
        fontsize=18, fontweight='bold', color=GOLD)
ax.text(opsdb_x, opsdb_y - 0.05, 'one substrate', ha='center', va='center',
        fontsize=10, color=WHITE, style='italic')
ax.text(opsdb_x, opsdb_y - 0.55, 'config + cached state +', ha='center', va='center',
        fontsize=8, color=SILVER)
ax.text(opsdb_x, opsdb_y - 0.85, 'pointers + history + audit', ha='center', va='center',
        fontsize=8, color=SILVER)

# API ring around OpsDB
api_ring = Circle((opsdb_x, opsdb_y), 1.55, facecolor='none',
                   edgecolor=ORANGE, linewidth=2, linestyle='--', alpha=0.7)
ax.add_patch(api_ring)
ax.text(opsdb_x + 1.45, opsdb_y - 1.65, 'API gate',
        ha='center', va='center', fontsize=9, color=ORANGE, style='italic')

# Three populations as nodes
def population_node(x, y, name, sublabel, color, examples):
    box = FancyBboxPatch((x - 1.7, y - 0.7), 3.4, 1.4,
                          boxstyle='round,pad=0.08', facecolor=PAN,
                          edgecolor=color, linewidth=2.2)
    ax.add_patch(box)
    ax.text(x, y + 0.30, name, ha='center', va='center',
            fontsize=13, fontweight='bold', color=color)
    ax.text(x, y - 0.05, sublabel, ha='center', va='center',
            fontsize=9, color=WHITE, style='italic')
    ax.text(x, y - 0.45, examples, ha='center', va='center',
            fontsize=7, color=SILVER)

humans_xy    = (3.0, 9.0)
runners_xy   = (13.0, 9.0)
auditors_xy  = (8.0, 1.5)

population_node(*humans_xy, 'HUMANS', 'investigate, plan, propose', CYAN,
                'operators, planners, owners')
population_node(*runners_xy, 'AUTOMATION', 'read, act, write back', GREEN,
                'pullers, reconcilers, verifiers')
population_node(*auditors_xy, 'AUDITORS', 'verify, evidence, attest', MAG,
                'compliance, internal audit')

# Arrows from each population to OpsDB API ring
def pop_arrow(start, end, color, label_pos, label):
    arr = FancyArrowPatch(start, end,
                           arrowstyle='->,head_width=7,head_length=9',
                           color=color, linewidth=1.8, alpha=0.75,
                           connectionstyle="arc3,rad=0.0")
    ax.add_patch(arr)
    ax.text(label_pos[0], label_pos[1], label, ha='center', va='center',
            fontsize=8, color=color,
            bbox=dict(boxstyle='round,pad=0.25', facecolor=BG,
                      edgecolor=color, linewidth=0.8))

# Humans → API
pop_arrow((humans_xy[0] + 1.0, humans_xy[1] - 0.6),
          (opsdb_x - 1.4, opsdb_y + 1.1),
          CYAN, (5.4, 7.6), 'query, propose changes')
# Automation → API
pop_arrow((runners_xy[0] - 1.0, runners_xy[1] - 0.6),
          (opsdb_x + 1.4, opsdb_y + 1.1),
          GREEN, (10.7, 7.6), 'poll, write results')
# Auditors → API
pop_arrow((auditors_xy[0] - 1.0, auditors_xy[1] + 0.5),
          (opsdb_x - 0.5, opsdb_y - 1.4),
          MAG, (5.4, 3.0), 'read evidence, history')

# "Same data" annotation at center
ax.text(opsdb_x, 0.5,
        'Same data, same gate, same trail. Three audiences served from one substrate.',
        ha='center', va='center', fontsize=10, color=GOLD, style='italic',
        bbox=dict(boxstyle='round,pad=0.4', facecolor=PAN, edgecolor=GOLD, linewidth=1))

ax.text(8.0, 10.4, 'Three Populations on One Substrate',
        ha='center', va='center', fontsize=16, fontweight='bold', color=GOLD)

save(fig, 'infra2_01_three_populations.png')

# ================================================================
# FIG 2: THE 0/1/N CARDINALITY LANDSCAPE
# Type: 2 + 3 (Scale/Landscape + Threshold/Region)
# Shows: Three valid regions; "2" explicitly forbidden
# ================================================================
fig, ax = plt.subplots(figsize=(18, 10))
ax.set_facecolor(BG)
ax.set_xlim(0, 18)
ax.set_ylim(0, 10)
ax.axis('off')

# Region backgrounds
ax.add_patch(Rectangle((0.5, 1.5), 4.0, 7.0, facecolor=DIM, alpha=0.10,
                        edgecolor=DIM, linewidth=1))
ax.add_patch(Rectangle((4.5, 1.5), 4.0, 7.0, facecolor=GOLD, alpha=0.10,
                        edgecolor=GOLD, linewidth=1.5))
ax.add_patch(Rectangle((8.5, 1.5), 1.5, 7.0, facecolor=RED, alpha=0.18,
                        edgecolor=RED, linewidth=1.5))
ax.add_patch(Rectangle((10.0, 1.5), 7.5, 7.0, facecolor=CYAN, alpha=0.10,
                        edgecolor=CYAN, linewidth=1.5))

# Region headers
ax.text(2.5, 8.0, '0', ha='center', fontsize=32, color=DIM, fontweight='bold')
ax.text(6.5, 8.0, '1', ha='center', fontsize=32, color=GOLD, fontweight='bold')
ax.text(9.25, 8.0, '2', ha='center', fontsize=32, color=RED, fontweight='bold')
ax.text(13.75, 8.0, 'N', ha='center', fontsize=32, color=CYAN, fontweight='bold')

# Subtitles
ax.text(2.5, 7.3, 'where most orgs are',
        ha='center', fontsize=10, color=SILVER, style='italic')
ax.text(6.5, 7.3, 'one substrate, defended',
        ha='center', fontsize=10, color=SILVER, style='italic')
ax.text(9.25, 7.3, 'failure state',
        ha='center', fontsize=10, color=RED, style='italic', fontweight='bold')
ax.text(13.75, 7.3, 'planned multi-substrate',
        ha='center', fontsize=10, color=SILVER, style='italic')

# 0 region content
zero_text = [
    '• Operations is human-driven',
    '• Configuration scattered',
    '  across N tools',
    '• No coordination substrate',
    '• Most organizations today',
]
for i, t in enumerate(zero_text):
    ax.text(2.5, 6.5 - i * 0.4, t, ha='center', va='center',
            fontsize=8, color=SILVER)

# 1 region content
one_text = [
    '• One substrate',
    '• API enforces SSO + RBAC',
    '• Single security umbrella',
    '• Most non-mega-corps',
    '• Defended forever, or N',
]
for i, t in enumerate(one_text):
    ax.text(6.5, 6.5 - i * 0.4, t, ha='center', va='center',
            fontsize=8, color=WHITE)

# 2 region — forbidden
ax.text(9.25, 6.5, '✗', ha='center', va='center',
        fontsize=42, color=RED, fontweight='bold')
ax.text(9.25, 5.4, 'NO', ha='center', va='center',
        fontsize=14, color=RED, fontweight='bold')
ax.text(9.25, 4.9, 'SUCH', ha='center', va='center',
        fontsize=11, color=RED, fontweight='bold')
ax.text(9.25, 4.5, 'STATE', ha='center', va='center',
        fontsize=11, color=RED, fontweight='bold')
ax.text(9.25, 3.6,
        'split-brain ops',
        ha='center', va='center', fontsize=8, color=RED, style='italic')
ax.text(9.25, 3.2,
        'two schemas',
        ha='center', va='center', fontsize=8, color=RED, style='italic')
ax.text(9.25, 2.8,
        'drifting apart',
        ha='center', va='center', fontsize=8, color=RED, style='italic')

# N region content (split into reasons-yes and reasons-no)
ax.text(11.7, 6.7, 'JUSTIFIES N', ha='center', fontsize=10,
        color=GREEN, fontweight='bold')
yes_reasons = [
    'org boundaries',
    'security perimeter',
    'legal/regulatory zones',
    'human comm boundaries',
    'air-gap requirements',
]
for i, r in enumerate(yes_reasons):
    ax.text(11.7, 6.2 - i * 0.35, '✓ ' + r, ha='center', va='center',
            fontsize=8, color=GREEN)

ax.text(15.7, 6.7, 'DOES NOT', ha='center', fontsize=10,
        color=RED, fontweight='bold')
no_reasons = [
    'technical fragility',
    'convenience',
    'premature optimization',
    'performance scaling',
    '(fix ops practice instead)',
]
for i, r in enumerate(no_reasons):
    color = RED if i < 4 else SILVER
    style = 'normal' if i < 4 else 'italic'
    ax.text(15.7, 6.2 - i * 0.35, '✗ ' + r, ha='center', va='center',
            fontsize=8, color=color, style=style)

# Barrier between 1 and 2
ax.plot([8.5, 8.5], [1.5, 8.5], color=RED, linewidth=2.5, linestyle='-')
# Barrier between 2 and N
ax.plot([10.0, 10.0], [1.5, 8.5], color=RED, linewidth=2.5, linestyle='-')

# Bottom callout
ax.text(9.0, 0.7,
        'There is no 2.  Either commit to 1 and defend it, or architect for N.',
        ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor=PAN, edgecolor=GOLD, linewidth=1))

ax.text(9.0, 9.4, 'OpsDB Cardinality — The 0/1/N Rule',
        ha='center', va='center', fontsize=16, fontweight='bold', color=GOLD)

save(fig, 'infra2_02_cardinality_landscape.png')

# ================================================================
# FIG 3: API AS GOVERNANCE PERIMETER
# Type: 4 (Geometric Cross-Section)
# Shows: Substrate at center, API ring with seven enforcement layers,
# three populations approaching from outside
# ================================================================
fig, ax = plt.subplots(figsize=(15, 13))
ax.set_facecolor(BG)
ax.set_xlim(-7.5, 7.5)
ax.set_ylim(-7.5, 7.5)
ax.set_aspect('equal')
ax.axis('off')

# Outer ring zone (population approach area)
# Substrate (innermost)
ax.add_patch(Circle((0, 0), 1.6, facecolor=PAN,
                     edgecolor=GOLD, linewidth=2.5))
ax.text(0, 0.25, 'SUBSTRATE', ha='center', va='center',
        fontsize=12, fontweight='bold', color=GOLD)
ax.text(0, -0.25, 'data only', ha='center', va='center',
        fontsize=9, color=WHITE, style='italic')
ax.text(0, -0.65, '(simple)', ha='center', va='center',
        fontsize=8, color=SILVER)

# API ring (single ring, sectioned into 7 enforcement layers as wedges)
api_inner_r = 1.7
api_outer_r = 4.5

# Seven enforcement layers as colored wedges
layers = [
    ('Auth\n(SSO, identity)',         BLUE,    0,    51.4),
    ('Authorization\n(RBAC, scopes)', PURPLE,  51.4, 102.8),
    ('Validation\n(schema, rules)',   CYAN,    102.8, 154.2),
    ('Change Mgmt\n(propose+approve)', GOLD,   154.2, 205.6),
    ('Versioning\n(history)',          GREEN,  205.6, 257.0),
    ('Audit\n(append-only log)',       MAG,    257.0, 308.4),
    ('Rate Limit\n(abuse defense)',    ORANGE, 308.4, 360.0),
]

for name, color, t0, t1 in layers:
    wedge = Wedge((0, 0), api_outer_r, t0, t1,
                   width=api_outer_r - api_inner_r,
                   facecolor=color, alpha=0.30, edgecolor=color, linewidth=1.5)
    ax.add_patch(wedge)
    # Label inside the wedge
    mid_angle = np.deg2rad((t0 + t1) / 2)
    label_r = (api_inner_r + api_outer_r) / 2
    lx = label_r * np.cos(mid_angle)
    ly = label_r * np.sin(mid_angle)
    ax.text(lx, ly, name, ha='center', va='center',
            fontsize=8, color=WHITE, fontweight='bold')

# Outer ring label
ax.text(0, api_outer_r + 0.4, 'API GATE — sophisticated',
        ha='center', va='center', fontsize=11, color=ORANGE,
        fontweight='bold', style='italic')
ax.text(0, -api_outer_r - 0.4,
        '(the only path to the substrate)',
        ha='center', va='center', fontsize=9, color=ORANGE, style='italic')

# Three populations arriving from outside
def approaching_population(x, y, name, color):
    box = FancyBboxPatch((x - 1.3, y - 0.45), 2.6, 0.9,
                         boxstyle='round,pad=0.05', facecolor=PAN,
                         edgecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center',
            fontsize=10, fontweight='bold', color=color)

# Position three populations radially around the API
hum_x, hum_y = -5.5, 4.5
auto_x, auto_y = 5.5, 4.5
aud_x, aud_y = 0, -6.0

approaching_population(hum_x, hum_y, 'humans', CYAN)
approaching_population(auto_x, auto_y, 'automation', GREEN)
approaching_population(aud_x, aud_y, 'auditors', MAG)

# Arrows from each population through the API ring
def gate_arrow(sx, sy, ex_dir_x, ex_dir_y, color):
    # Draw arrow from population to outer edge of API ring
    norm = np.sqrt(ex_dir_x**2 + ex_dir_y**2)
    target_x = api_outer_r * ex_dir_x / norm
    target_y = api_outer_r * ex_dir_y / norm
    arr = FancyArrowPatch((sx, sy), (target_x, target_y),
                           arrowstyle='->,head_width=6,head_length=9',
                           color=color, linewidth=1.8, alpha=0.7)
    ax.add_patch(arr)

gate_arrow(hum_x + 0.7, hum_y - 0.4, -1, 1, CYAN)
gate_arrow(auto_x - 0.7, auto_y - 0.4, 1, 1, GREEN)
gate_arrow(aud_x, aud_y + 0.5, 0, -1, MAG)

# Title
ax.text(0, 6.7, 'API as Governance Perimeter',
        ha='center', va='center', fontsize=15, fontweight='bold', color=GOLD)
ax.text(0, 6.1,
        'Sophisticated API surrounds simple substrate.  Every interaction passes through the gate.',
        ha='center', va='center', fontsize=9, color=SILVER, style='italic')

save(fig, 'infra2_03_api_perimeter.png')

# ================================================================
# FIG 4: CHANGE-SET LIFECYCLE
# Type: 7 (Progression / Sequence)
# Shows: propose → validate → route → approve → commit → version
# with the emergency path branching off
# ================================================================
fig, ax = plt.subplots(figsize=(18, 9))
ax.set_facecolor(PAN)
ax.set_xlim(0, 18)
ax.set_ylim(0, 9)
ax.axis('off')

# Main flow stages
stages = [
    (1.2,  'Propose',     'change set\nbundle + reason',  CYAN),
    (4.0,  'Validate',    'schema, policy,\nintegrity',   BLUE),
    (6.8,  'Route',       'compute approvers\nnotify',    PURPLE),
    (9.6,  'Collect',     'approve / reject\ncomment',    GOLD),
    (12.4, 'Commit',      'atomic across\nbundle',        GREEN),
    (15.2, 'Version',     'history entry\naudit log',     MAG),
]

main_y = 5.2

# Draw stage boxes
for x, name, sublabel, color in stages:
    box = FancyBboxPatch((x - 1.0, main_y - 0.7), 2.0, 1.4,
                         boxstyle='round,pad=0.05', facecolor=BG,
                         edgecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(x, main_y + 0.30, name, ha='center', va='center',
            fontsize=11, fontweight='bold', color=color)
    ax.text(x, main_y - 0.20, sublabel, ha='center', va='center',
            fontsize=8, color=WHITE)

# Connecting arrows on the main flow
for i in range(len(stages) - 1):
    x0 = stages[i][0] + 1.0
    x1 = stages[i+1][0] - 1.0
    arr = FancyArrowPatch((x0, main_y), (x1, main_y),
                           arrowstyle='->,head_width=7,head_length=9',
                           color=GOLD, linewidth=1.5, alpha=0.7)
    ax.add_patch(arr)

# Emergency branch — split between Validate and Route
emerg_y = 7.5
# Branch up from Validate
branch_x_up = stages[1][0]
arr_up = FancyArrowPatch((branch_x_up, main_y + 0.7),
                          (branch_x_up + 1.0, emerg_y - 0.5),
                          arrowstyle='->,head_width=6,head_length=8',
                          color=RED, linewidth=1.5, alpha=0.7,
                          connectionstyle="arc3,rad=0.15")
ax.add_patch(arr_up)
# Emergency stage box
emerg_box = FancyBboxPatch((branch_x_up + 1.0 - 1.4, emerg_y - 0.5), 2.8, 1.0,
                            boxstyle='round,pad=0.05', facecolor=BG,
                            edgecolor=RED, linewidth=2, linestyle='--')
ax.add_patch(emerg_box)
ax.text(branch_x_up + 1.0, emerg_y + 0.1, 'EMERGENCY PATH',
        ha='center', va='center', fontsize=10, fontweight='bold', color=RED)
ax.text(branch_x_up + 1.0, emerg_y - 0.25,
        'reduced approval • flagged in audit', ha='center', va='center',
        fontsize=8, color=WHITE)
# Emergency flows back to Commit
arr_down = FancyArrowPatch((branch_x_up + 1.0 + 1.4, emerg_y - 0.5),
                            (stages[4][0] - 0.5, main_y + 0.7),
                            arrowstyle='->,head_width=6,head_length=8',
                            color=RED, linewidth=1.5, alpha=0.7,
                            connectionstyle="arc3,rad=-0.15")
ax.add_patch(arr_down)

# Rejection / expiry path — drops down from Collect
reject_y = 2.5
arr_rej = FancyArrowPatch((stages[3][0], main_y - 0.7),
                           (stages[3][0], reject_y + 0.5),
                           arrowstyle='->,head_width=6,head_length=8',
                           color=DIM, linewidth=1.2, alpha=0.7)
ax.add_patch(arr_rej)
rej_box = FancyBboxPatch((stages[3][0] - 1.5, reject_y - 0.5), 3.0, 1.0,
                          boxstyle='round,pad=0.05', facecolor=BG,
                          edgecolor=DIM, linewidth=1.5, linestyle=':')
ax.add_patch(rej_box)
ax.text(stages[3][0], reject_y + 0.1, 'REJECTED  /  EXPIRED',
        ha='center', va='center', fontsize=10, fontweight='bold', color=DIM)
ax.text(stages[3][0], reject_y - 0.25,
        'recorded in history; does not commit', ha='center', va='center',
        fontsize=8, color=SILVER)

# Bottom annotation
ax.text(9.0, 0.6,
        'Every change is proposed, reviewed, and committed atomically.  Discipline applies uniformly to all centrally-managed data.',
        ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# Title
ax.text(9.0, 8.4, 'Change-Set Lifecycle',
        ha='center', va='center', fontsize=16, fontweight='bold', color=GOLD)

save(fig, 'infra2_04_change_set_lifecycle.png')

# ================================================================
# FIG 5: ARCHITECTURAL LAYERING — DATA PRIMACY IN TIME
# Type: 4 (Geometric Cross-Section, with a time axis)
# Shows: Three layers with churn rates over time; schema as long-lived center
# ================================================================
fig, ax = plt.subplots(figsize=(18, 10))
ax.set_facecolor(PAN)
ax.set_xlim(0, 18)
ax.set_ylim(0, 10)

# X axis: time (years)
years = np.arange(0, 11, 1)

# Three layers shown as horizontal bands
# Bottom: schema (very stable)
# Middle: runners + libs (medium churn)
# Top: integrations + adapters (high churn)

# Bottom layer — schema
schema_y0, schema_y1 = 0.8, 2.5
ax.add_patch(Rectangle((0.5, schema_y0), 17.0, schema_y1 - schema_y0,
                        facecolor=GOLD, alpha=0.20,
                        edgecolor=GOLD, linewidth=1.5))
ax.text(0.8, (schema_y0 + schema_y1) / 2 + 0.30, 'SCHEMA',
        fontsize=13, fontweight='bold', color=GOLD, va='center')
ax.text(0.8, (schema_y0 + schema_y1) / 2 - 0.20,
        'stable across decades', fontsize=9, color=WHITE, style='italic',
        va='center')

# Schema additions over time (small marks showing additive evolution)
schema_additions = [1.5, 2.8, 4.0, 5.2, 6.8, 8.5]
for x in schema_additions:
    ax.plot([x, x], [schema_y0, schema_y1], color=GOLD,
            linewidth=2, alpha=0.7)
    ax.plot([x], [schema_y1 + 0.1], marker='+', markersize=8,
            color=GOLD, alpha=0.8)

ax.text(11, schema_y0 + 0.3, '+ = additive change set (new entity type, field)',
        fontsize=8, color=GOLD, style='italic', va='center', alpha=0.8)

# Middle layer — runners + libraries
mid_y0, mid_y1 = 3.2, 5.4
ax.add_patch(Rectangle((0.5, mid_y0), 17.0, mid_y1 - mid_y0,
                        facecolor=GREEN, alpha=0.18,
                        edgecolor=GREEN, linewidth=1.5))
ax.text(0.8, (mid_y0 + mid_y1) / 2 + 0.35, 'RUNNERS + SHARED LIBS',
        fontsize=13, fontweight='bold', color=GREEN, va='center')
ax.text(0.8, (mid_y0 + mid_y1) / 2 - 0.20,
        'medium churn — rewritten as goals shift', fontsize=9, color=WHITE,
        style='italic', va='center')

# Generate jagged churn pattern for runners
np.random.seed(42)
runner_churn_x = np.linspace(1.0, 17.0, 80)
runner_churn_y = (mid_y0 + mid_y1) / 2 + 0.3 * np.sin(runner_churn_x * 1.2) + \
                 0.15 * np.random.randn(80)
ax.plot(runner_churn_x, runner_churn_y, color=GREEN, linewidth=1.8, alpha=0.7)

# Top layer — integrations and adapters
top_y0, top_y1 = 6.1, 8.3
ax.add_patch(Rectangle((0.5, top_y0), 17.0, top_y1 - top_y0,
                        facecolor=CYAN, alpha=0.18,
                        edgecolor=CYAN, linewidth=1.5))
ax.text(0.8, (top_y0 + top_y1) / 2 + 0.35, 'INTEGRATIONS + ADAPTERS',
        fontsize=13, fontweight='bold', color=CYAN, va='center')
ax.text(0.8, (top_y0 + top_y1) / 2 - 0.20,
        'high churn — auth/cloud/k8s APIs evolve constantly',
        fontsize=9, color=WHITE, style='italic', va='center')

# Generate higher-frequency churn for integrations
integ_churn_x = np.linspace(1.0, 17.0, 200)
integ_churn_y = (top_y0 + top_y1) / 2 + 0.4 * np.sin(integ_churn_x * 3.0) + \
                0.25 * np.random.randn(200)
ax.plot(integ_churn_x, integ_churn_y, color=CYAN, linewidth=1.5, alpha=0.7)

# Time axis at bottom
ax.axhline(0.5, color=DIM, linewidth=1)
ax.set_xticks([0.5, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 17.5])
ax.set_xticklabels(['', '1y', '2y', '3y', '4y', '5y', '6y', '7y', '8y', '10y'],
                    color=DIM, fontsize=9)
ax.set_yticks([])
ax.set_xlabel('time', fontsize=10, color=SILVER)

for spine in ax.spines.values():
    spine.set_color(DIM)
    spine.set_linewidth(0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Legend at right
legend_x = 14.5
ax.text(legend_x, 9.4, 'CHURN RATE',
        ha='center', fontsize=10, color=WHITE, fontweight='bold')

# Title
ax.text(9.0, 9.5, 'Data Primacy as Architectural Layering',
        ha='center', va='center', fontsize=16, fontweight='bold', color=GOLD)

# Bottom annotation
ax.text(9.0, 0.15,
        'Schema persists. Runners and libs are rewritten as goals shift. Integrations adapt to constantly-evolving external APIs.',
        ha='center', va='center', fontsize=9, color=SILVER, style='italic')

save(fig, 'infra2_05_layering_in_time.png')

# ================================================================
# FIG 6: CACHED STATE FRESHNESS VS. POPULATION METHOD
# Type: 1 (Running / Convergence Chart)
# Shows: Curves showing how staleness varies by populator type
# ================================================================
fig, ax = plt.subplots(figsize=(18, 10))
ax.set_facecolor(PAN)

# X axis: time since last write (seconds, log scale)
# Y axis: fraction of cached entities at that staleness or fresher

t = np.logspace(-1, 4, 200)  # 0.1 sec to 10000 sec (~3 hours)

# Each population method has a different freshness distribution
# Watch stream: very fresh, sharp drop after seconds
# 30s poller: most fresh within 30s, plateau, full coverage by 60s
# 5min poller: fresher items still recent, full coverage by 300-600s
# Hourly batch: most data within ~1 hour, full coverage by then
# Manual import: very stale, only recent at import times

def freshness_curve(t, scale, sharpness):
    """Returns fraction of cached entries fresher than time t."""
    return 1.0 / (1.0 + (t / scale) ** sharpness)

watch_curve = freshness_curve(t, scale=1.5, sharpness=4.0)
poll_30s = freshness_curve(t, scale=20, sharpness=3.5)
poll_5min = freshness_curve(t, scale=200, sharpness=3.0)
hourly = freshness_curve(t, scale=2400, sharpness=2.5)
manual = freshness_curve(t, scale=8000, sharpness=2.0)

ax.plot(t, watch_curve, color=GREEN, linewidth=2.5,
        label='watch stream (event-driven)')
ax.plot(t, poll_30s, color=CYAN, linewidth=2.5,
        label='30s poller')
ax.plot(t, poll_5min, color=BLUE, linewidth=2.5,
        label='5min poller')
ax.plot(t, hourly, color=ORANGE, linewidth=2.5,
        label='hourly batch')
ax.plot(t, manual, color=MAG, linewidth=2.5, linestyle='--',
        label='manual import')

# Threshold bands
ax.axvspan(0.1, 10, facecolor=GREEN, alpha=0.06)
ax.axvspan(10, 300, facecolor=CYAN, alpha=0.06)
ax.axvspan(300, 3600, facecolor=ORANGE, alpha=0.06)
ax.axvspan(3600, 36000, facecolor=MAG, alpha=0.06)

# Threshold labels at top
ax.text(1.0, 1.05, 'sub-10s', ha='center', fontsize=8,
        color=GREEN, style='italic')
ax.text(55, 1.05, '10s–5min', ha='center', fontsize=8,
        color=CYAN, style='italic')
ax.text(1100, 1.05, '5min–1h', ha='center', fontsize=8,
        color=ORANGE, style='italic')
ax.text(11000, 1.05, '1h+', ha='center', fontsize=8,
        color=MAG, style='italic')

# Reference line at 50%
ax.axhline(0.5, color=DIM, linewidth=1, linestyle=':', alpha=0.6)
ax.text(0.12, 0.52, '50% fresh-or-fresher line',
        fontsize=8, color=DIM, style='italic')

ax.set_xscale('log')
ax.set_xlim(0.1, 18000)
ax.set_ylim(0, 1.08)
ax.set_xlabel('time since last write (seconds, log scale)',
              fontsize=11, color=SILVER)
ax.set_ylabel('fraction of cached entities at that staleness or fresher',
              fontsize=11, color=SILVER)
ax.tick_params(colors=DIM, labelsize=9)

for spine in ax.spines.values():
    spine.set_color(DIM)
    spine.set_linewidth(0.5)

leg = ax.legend(loc='lower left', facecolor=PAN, edgecolor=DIM,
                labelcolor=WHITE, fontsize=9, framealpha=0.95)
for text in leg.get_texts():
    text.set_color(WHITE)

# Annotation box
ann_text = (
    'The OpsDB does not impose freshness contracts.\n'
    'Whatever the population method produces is the cache.\n'
    'Consumers read timestamps and decide if it is fresh enough.'
)
ax.text(0.15, 0.18, ann_text, fontsize=10, color=GOLD,
        bbox=dict(boxstyle='round,pad=0.4', facecolor=BG,
                  edgecolor=GOLD, linewidth=1),
        va='top', transform=ax.transAxes)

ax.set_title('Cached State Freshness vs. Population Method',
             fontsize=15, fontweight='bold', color=GOLD, pad=18)

save(fig, 'infra2_06_freshness_curves.png')

# ================================================================
# FIG 7: INVESTIGATION FLOW — WITHOUT vs. WITH OPSDB
# Type: 5 (Connection Map)
# Shows: Operator switching N tools (left) vs. one OpsDB query plus
# directed pointers (right)
# ================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10),
                                 gridspec_kw={'wspace': 0.20})
fig.patch.set_facecolor(BG)

for ax in (ax1, ax2):
    ax.set_facecolor(PAN)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

# --- LEFT PANEL: Without OpsDB ---
ax1.text(5.0, 9.5, 'Without OpsDB',
         ha='center', va='center', fontsize=14, fontweight='bold', color=RED)
ax1.text(5.0, 9.0,
         'operator assembles the picture by switching tools',
         ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# Operator at center
op_x, op_y = 5.0, 5.0
op_circle = Circle((op_x, op_y), 0.7, facecolor=PAN,
                    edgecolor=CYAN, linewidth=2.5)
ax1.add_patch(op_circle)
ax1.text(op_x, op_y, 'OP', ha='center', va='center',
         fontsize=11, fontweight='bold', color=CYAN)

# Six scattered tools around operator — each disconnected from others
tools_left = [
    (1.5, 7.5, 'k8s\nconsole',  BLUE),
    (8.5, 7.5, 'cloud\nconsole', PURPLE),
    (1.5, 5.0, 'wiki',           ORANGE),
    (8.5, 5.0, 'monitoring',     MAG),
    (1.5, 2.5, 'logs',           GREEN),
    (8.5, 2.5, 'CMDB',           CYAN),
]

for tx, ty, name, color in tools_left:
    box = FancyBboxPatch((tx - 0.7, ty - 0.5), 1.4, 1.0,
                         boxstyle='round,pad=0.05', facecolor=BG,
                         edgecolor=color, linewidth=1.5)
    ax1.add_patch(box)
    ax1.text(tx, ty, name, ha='center', va='center',
             fontsize=8, color=color, fontweight='bold')

# Lots of bidirectional arrows operator <-> each tool
for tx, ty, name, color in tools_left:
    arr1 = FancyArrowPatch((op_x, op_y), (tx, ty),
                            arrowstyle='->', color=color,
                            linewidth=1.0, alpha=0.55,
                            connectionstyle="arc3,rad=0.08")
    ax1.add_patch(arr1)
    arr2 = FancyArrowPatch((tx, ty), (op_x, op_y),
                            arrowstyle='->', color=color,
                            linewidth=1.0, alpha=0.55,
                            connectionstyle="arc3,rad=0.08")
    ax1.add_patch(arr2)

# Cost annotation
ax1.text(5.0, 0.6,
         '6+ tool switches per investigation\nMental join in operator\'s head',
         ha='center', va='center', fontsize=9, color=RED, style='italic',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                   edgecolor=RED, linewidth=1))

# --- RIGHT PANEL: With OpsDB ---
ax2.text(5.0, 9.5, 'With OpsDB',
         ha='center', va='center', fontsize=14, fontweight='bold', color=GREEN)
ax2.text(5.0, 9.0,
         'operator queries one substrate; pointers direct to authorities',
         ha='center', va='center', fontsize=9, color=SILVER, style='italic')

# Operator at left
op_x2, op_y2 = 1.5, 5.0
op_circle2 = Circle((op_x2, op_y2), 0.7, facecolor=PAN,
                     edgecolor=CYAN, linewidth=2.5)
ax2.add_patch(op_circle2)
ax2.text(op_x2, op_y2, 'OP', ha='center', va='center',
         fontsize=11, fontweight='bold', color=CYAN)

# OpsDB in the middle
opsdb_x2, opsdb_y2 = 5.0, 5.0
opsdb_box = FancyBboxPatch((opsdb_x2 - 1.0, opsdb_y2 - 0.7), 2.0, 1.4,
                            boxstyle='round,pad=0.05', facecolor=PAN,
                            edgecolor=GOLD, linewidth=2.5)
ax2.add_patch(opsdb_box)
ax2.text(opsdb_x2, opsdb_y2 + 0.30, 'OpsDB', ha='center', va='center',
         fontsize=12, fontweight='bold', color=GOLD)
ax2.text(opsdb_x2, opsdb_y2 - 0.10, 'config + state', ha='center', va='center',
         fontsize=8, color=WHITE)
ax2.text(opsdb_x2, opsdb_y2 - 0.40, '+ pointers', ha='center', va='center',
         fontsize=8, color=WHITE)

# Operator → OpsDB (single arrow, prominent)
arr_main = FancyArrowPatch((op_x2 + 0.7, op_y2), (opsdb_x2 - 1.0, opsdb_y2),
                            arrowstyle='->,head_width=8,head_length=10',
                            color=CYAN, linewidth=2.5, alpha=0.9)
ax2.add_patch(arr_main)
ax2.text((op_x2 + opsdb_x2) / 2, op_y2 + 0.5, 'one query',
         ha='center', va='center', fontsize=9, color=CYAN, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.25', facecolor=BG,
                   edgecolor=CYAN, linewidth=0.8))

# Authorities to the right of OpsDB — reached via pointers
authorities = [
    (8.5, 8.0, 'k8s API',     BLUE),
    (8.5, 6.5, 'cloud API',   PURPLE),
    (8.5, 5.0, 'wiki',        ORANGE),
    (8.5, 3.5, 'Prom server', MAG),
    (8.5, 2.0, 'log index',   GREEN),
]

for ax_x, ax_y, name, color in authorities:
    box = FancyBboxPatch((ax_x - 0.7, ax_y - 0.4), 1.4, 0.8,
                         boxstyle='round,pad=0.05', facecolor=BG,
                         edgecolor=color, linewidth=1.5)
    ax2.add_patch(box)
    ax2.text(ax_x, ax_y, name, ha='center', va='center',
             fontsize=8, color=color, fontweight='bold')
    # Pointer arrow from OpsDB to authority (dashed = "pointer")
    arr = FancyArrowPatch((opsdb_x2 + 1.0, opsdb_y2),
                           (ax_x - 0.7, ax_y),
                           arrowstyle='->', color=color,
                           linewidth=1.0, alpha=0.55, linestyle='--')
    ax2.add_patch(arr)

# Pointer label
ax2.text(7.2, 4.7, 'pointers', ha='center', va='center',
         fontsize=8, color=DIM, style='italic')

# Cost annotation
ax2.text(5.0, 0.6,
         'One query gets the picture\nFollow pointers when live data needed',
         ha='center', va='center', fontsize=9, color=GREEN, style='italic',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                   edgecolor=GREEN, linewidth=1))

# Title
fig.suptitle('Investigation Flow:  N tools  →  one substrate',
             fontsize=16, fontweight='bold', color=GOLD, y=0.98)

save(fig, 'infra2_07_investigation_flow.png')

# ================================================================
# FIG 8: LOCAL REPLICA + GLOBAL TRUTH PATTERN
# Type: 4 (Geometric Cross-Section)
# Shows: OpsDB at center with hosts holding local cached slices,
# including disconnected hosts continuing to serve local automation
# ================================================================
fig, ax = plt.subplots(figsize=(16, 12))
ax.set_facecolor(BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# OpsDB in the middle
opsdb_x, opsdb_y = 8.0, 6.5
opsdb_box = FancyBboxPatch((opsdb_x - 1.5, opsdb_y - 0.9), 3.0, 1.8,
                            boxstyle='round,pad=0.1', facecolor=PAN,
                            edgecolor=GOLD, linewidth=3)
ax.add_patch(opsdb_box)
ax.text(opsdb_x, opsdb_y + 0.35, 'OpsDB', ha='center', va='center',
        fontsize=15, fontweight='bold', color=GOLD)
ax.text(opsdb_x, opsdb_y - 0.05, 'global truth', ha='center', va='center',
        fontsize=10, color=WHITE, style='italic')
ax.text(opsdb_x, opsdb_y - 0.45, 'authoritative', ha='center', va='center',
        fontsize=8, color=SILVER)

# Hosts arranged around the OpsDB
# Connected hosts (read recent data, periodically refresh)
connected_hosts = [
    (3.0, 9.5,  'host A', 'fresh'),
    (13.0, 9.5, 'host B', 'fresh'),
    (3.0, 6.5,  'host C', 'fresh'),
    (13.0, 6.5, 'host D', 'fresh'),
    (4.5, 3.0,  'host E', 'fresh'),
]

# Disconnected hosts (network partition; serving local replica)
disconnected_hosts = [
    (11.5, 3.0, 'host F', 'partition: 7m'),
    (8.0, 1.5,  'host G', 'partition: 23m'),
]

def host_node(x, y, name, status, is_connected):
    """Draw a host with a small local-replica box attached."""
    color = GREEN if is_connected else ORANGE
    # Host box
    box = FancyBboxPatch((x - 0.7, y - 0.4), 1.4, 0.8,
                         boxstyle='round,pad=0.05', facecolor=PAN,
                         edgecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center',
            fontsize=10, fontweight='bold', color=color)
    # Small local-replica indicator (small box)
    rep_size = 0.35
    rep_box = FancyBboxPatch((x + 0.5, y - 0.55), rep_size, rep_size,
                              boxstyle='round,pad=0.02', facecolor=color,
                              alpha=0.5, edgecolor=color, linewidth=1)
    ax.add_patch(rep_box)
    # Status label below
    status_color = GREEN if is_connected else ORANGE
    ax.text(x, y - 0.85, status, ha='center', va='center',
            fontsize=7, color=status_color, style='italic')

# Connection arrows (active sync)
def connect_arrow(host_x, host_y, color, alpha=0.7, dashed=False):
    style = '--' if dashed else '-'
    arr = FancyArrowPatch((host_x, host_y),
                           (opsdb_x, opsdb_y + 0.9 if host_y > opsdb_y else opsdb_y - 0.9),
                           arrowstyle='-', color=color,
                           linewidth=1.5, alpha=alpha, linestyle=style)
    ax.add_patch(arr)

# Draw connected hosts and their sync lines
for hx, hy, name, status in connected_hosts:
    host_node(hx, hy, name, status, is_connected=True)
    # Closer endpoint to OpsDB box edge
    if hx < opsdb_x:
        end_x = opsdb_x - 1.5
    elif hx > opsdb_x:
        end_x = opsdb_x + 1.5
    else:
        end_x = opsdb_x
    if hy > opsdb_y:
        end_y = opsdb_y + 0.9
    elif hy < opsdb_y:
        end_y = opsdb_y - 0.9
    else:
        end_y = opsdb_y
    arr = FancyArrowPatch((hx, hy), (end_x, end_y),
                           arrowstyle='-', color=GREEN,
                           linewidth=1.5, alpha=0.6)
    ax.add_patch(arr)

# Draw disconnected hosts with broken connection indication
for hx, hy, name, status in disconnected_hosts:
    host_node(hx, hy, name, status, is_connected=False)
    # Broken/dashed line attempting to reach OpsDB
    if hx < opsdb_x:
        end_x = opsdb_x - 1.5
    elif hx > opsdb_x:
        end_x = opsdb_x + 1.5
    else:
        end_x = opsdb_x
    if hy > opsdb_y:
        end_y = opsdb_y + 0.9
    elif hy < opsdb_y:
        end_y = opsdb_y - 0.9
    else:
        end_y = opsdb_y
    # Partial line — only draws part of the way, simulating broken
    mid_x = (hx + end_x) / 2
    mid_y = (hy + end_y) / 2
    arr1 = FancyArrowPatch((hx, hy), (mid_x - 0.3, mid_y - 0.3),
                            arrowstyle='-', color=ORANGE,
                            linewidth=1.5, alpha=0.6, linestyle=':')
    ax.add_patch(arr1)
    # X mark indicating broken link
    ax.plot([mid_x - 0.5, mid_x + 0.1], [mid_y - 0.5, mid_y + 0.1],
            color=RED, linewidth=2, alpha=0.8)
    ax.plot([mid_x - 0.5, mid_x + 0.1], [mid_y + 0.1, mid_y - 0.5],
            color=RED, linewidth=2, alpha=0.8)

# "still serving local automation" callout for disconnected hosts
ax.text(11.5, 2.0, 'still serving\nlocal automation',
        ha='center', va='center', fontsize=8, color=ORANGE, style='italic')
ax.text(8.0, 0.5, 'still serving local automation',
        ha='center', va='center', fontsize=8, color=ORANGE, style='italic')

# Legend
leg_x = 1.0
leg_y_top = 11.0
ax.add_patch(Rectangle((leg_x, leg_y_top - 0.3), 0.4, 0.4, facecolor=GREEN, alpha=0.5))
ax.text(leg_x + 0.6, leg_y_top - 0.1, 'local replica  (cached slice)',
        fontsize=9, color=WHITE, va='center')

ax.plot([leg_x, leg_x + 0.4], [leg_y_top - 0.7, leg_y_top - 0.7],
        color=GREEN, linewidth=2)
ax.text(leg_x + 0.6, leg_y_top - 0.7, 'connected — periodic sync',
        fontsize=9, color=WHITE, va='center')

ax.plot([leg_x, leg_x + 0.4], [leg_y_top - 1.1, leg_y_top - 1.1],
        color=ORANGE, linewidth=2, linestyle=':')
ax.text(leg_x + 0.6, leg_y_top - 1.1, 'partition — replica still local',
        fontsize=9, color=WHITE, va='center')

# Title
ax.text(8.0, 11.4, 'Local Replica + Global Truth',
        ha='center', va='center', fontsize=16, fontweight='bold', color=GOLD)

# Bottom note
ax.text(8.0, 10.5,
        'OpsDB is the global authority. Every host can hold a dumped slice locally; partition does not stop work.',
        ha='center', va='center', fontsize=9, color=SILVER, style='italic')

save(fig, 'infra2_08_local_replica.png')

# ================================================================
# SUMMARY
# ================================================================
print("\nAll 8 figures saved to: %s" % outdir)
print("  infra2_01_three_populations.png")
print("  infra2_02_cardinality_landscape.png")
print("  infra2_03_api_perimeter.png")
print("  infra2_04_change_set_lifecycle.png")
print("  infra2_05_layering_in_time.png")
print("  infra2_06_freshness_curves.png")
print("  infra2_07_investigation_flow.png")
print("  infra2_08_local_replica.png")
