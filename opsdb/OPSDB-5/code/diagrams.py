#!/usr/bin/env python3
"""
OPSDB OPSDB-5 Diagrams - Runner Design
8 figures covering the runner pattern, runner kinds, coordination, gating,
GitOps cast, shared-library framework, idempotency convergence, and the
standard-practice vs OpsDB-coordinated contrast.
Output: PNG files to ../figures/
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Wedge, Ellipse
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
# FIG 1: THE RUNNER PATTERN - GET, ACT, SET
# Type: 7 (Progression/Sequence Diagram)
# Shows: Three phases with OpsDB on both sides
# ================================================================

print("Fig 1: The runner pattern - get, act, set")

fig, ax = plt.subplots(figsize=(18, 10))
hide_axis(ax)
ax.set_xlim(0, 20)
ax.set_ylim(0, 11)

ax.text(10, 10.3, 'The Runner Pattern - Get, Act, Set',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(10, 9.65,
        'OpsDB is the runner\'s only stable interface - reads in, writes out',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# OpsDB on the left (read source)
opsdb_left_x = 1.2
opsdb_y = 5.0
opsdb_w = 2.6
opsdb_h = 5.0

ax.add_patch(FancyBboxPatch((opsdb_left_x, opsdb_y - opsdb_h/2),
                            opsdb_w, opsdb_h,
                            boxstyle='round,pad=0.1',
                            facecolor=BG, edgecolor=GOLD,
                            linewidth=2.5, zorder=2))
ax.text(opsdb_left_x + opsdb_w/2, opsdb_y + opsdb_h/2 - 0.55,
        'OpsDB', ha='center', va='center',
        color=GOLD, fontsize=13, fontweight='bold')

# Tables read
read_tables = [
    'runner_spec_version',
    'entity rows',
    'observation_cache_*',
    'policy',
    'change_set',
]
for i, t in enumerate(read_tables):
    y = opsdb_y + 1.4 - i * 0.55
    ax.text(opsdb_left_x + opsdb_w/2, y, t,
            ha='center', va='center',
            color=WHITE, fontsize=8.5, family='monospace')

# OpsDB on the right (write target)
opsdb_right_x = 16.2

ax.add_patch(FancyBboxPatch((opsdb_right_x, opsdb_y - opsdb_h/2),
                            opsdb_w, opsdb_h,
                            boxstyle='round,pad=0.1',
                            facecolor=BG, edgecolor=GOLD,
                            linewidth=2.5, zorder=2))
ax.text(opsdb_right_x + opsdb_w/2, opsdb_y + opsdb_h/2 - 0.55,
        'OpsDB', ha='center', va='center',
        color=GOLD, fontsize=13, fontweight='bold')

# Tables written
write_tables = [
    'runner_job',
    'runner_job_output_var',
    'observation_cache_*',
    'evidence_record',
    'change_set (proposed)',
    'audit_log_entry',
]
for i, t in enumerate(write_tables):
    y = opsdb_y + 1.4 - i * 0.55
    ax.text(opsdb_right_x + opsdb_w/2, y, t,
            ha='center', va='center',
            color=WHITE, fontsize=8.5, family='monospace')

# Three phases in the middle
phases = [
    (5.5,  'GET',  BLUE,
     'read config\nread desired\nread observed\nread policy'),
    (9.5,  'ACT',  CYAN,
     'compute diff\ndecide actions\ncall world\n(via shared libs)'),
    (13.5, 'SET',  MAG,
     'write runner_job\nwrite output vars\nwrite evidence\npropose change_set'),
]

phase_w = 2.6
phase_h = 3.0

for x, label, color, content in phases:
    ax.add_patch(FancyBboxPatch((x - phase_w/2, opsdb_y - phase_h/2),
                                phase_w, phase_h,
                                boxstyle='round,pad=0.05',
                                facecolor=PAN, edgecolor=color,
                                linewidth=2, zorder=3))
    ax.text(x, opsdb_y + phase_h/2 - 0.4,
            label, ha='center', va='center',
            color=color, fontsize=14, fontweight='bold', zorder=4)
    ax.text(x, opsdb_y - 0.2, content,
            ha='center', va='center',
            color=WHITE, fontsize=9, zorder=4)

# OpsDB read arrow into GET
draw_arrow(ax, opsdb_left_x + opsdb_w + 0.1, opsdb_y,
           5.5 - phase_w/2 - 0.1, opsdb_y,
           color=BLUE, lw=2.0, alpha=0.9)

# GET to ACT
draw_arrow(ax, 5.5 + phase_w/2 + 0.1, opsdb_y,
           9.5 - phase_w/2 - 0.1, opsdb_y,
           color=SILVER, lw=2.0, alpha=0.9)

# ACT to SET
draw_arrow(ax, 9.5 + phase_w/2 + 0.1, opsdb_y,
           13.5 - phase_w/2 - 0.1, opsdb_y,
           color=SILVER, lw=2.0, alpha=0.9)

# SET to OpsDB write
draw_arrow(ax, 13.5 + phase_w/2 + 0.1, opsdb_y,
           opsdb_right_x - 0.1, opsdb_y,
           color=MAG, lw=2.0, alpha=0.9)

# World below ACT
world_y = 1.5
ax.add_patch(FancyBboxPatch((7.5, world_y - 0.5), 4.0, 1.0,
                            boxstyle='round,pad=0.05',
                            facecolor=BG, edgecolor=DIM,
                            linewidth=1.2, zorder=2))
ax.text(9.5, world_y, 'the world\n(K8s, cloud, hosts, vault, monitoring)',
        ha='center', va='center',
        color=SILVER, fontsize=9, style='italic', zorder=3)

# Bidirectional arrow ACT to world
draw_arrow(ax, 9.5, opsdb_y - phase_h/2 - 0.1,
           9.5, world_y + 0.5 + 0.1,
           color=CYAN, lw=1.5, alpha=0.8, style='<->')

ax.text(11.0, 2.7, 'side effects',
        ha='left', va='center',
        color=CYAN, fontsize=9, style='italic')

# Labels for read/write streams above arrows
ax.text(4.4, opsdb_y + 0.4, 'read',
        ha='center', va='center',
        color=BLUE, fontsize=10, fontweight='bold', style='italic')
ax.text(15.6, opsdb_y + 0.4, 'write',
        ha='center', va='center',
        color=MAG, fontsize=10, fontweight='bold', style='italic')

# Bottom note
ax.text(10, 0.4,
        'every read and write goes through the API.  every write produces an audit_log_entry.',
        ha='center', va='center',
        color=DIM, fontsize=9.5, style='italic')

save(fig, 'infra4_01_runner_pattern.png')


# ================================================================
# FIG 2: RUNNER KINDS MAPPED TO MECHANISM FAMILIES
# Type: 5 (Connection Map)
# Shows: Each runner kind instantiates one or more OPSDB-9 mechanism families
# ================================================================

print("Fig 2: Runner kinds to mechanism families")

fig, ax = plt.subplots(figsize=(18, 12))
hide_axis(ax)
ax.set_xlim(0, 20)
ax.set_ylim(0, 13)

ax.text(10, 12.3, 'Runner Kinds Mapped to Mechanism Families',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(10, 11.65,
        'Each runner kind instantiates one or more mechanism families from OPSDB-9',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# Left column: mechanism families (from OPSDB-9)
families = [
    ('Sensing',          BLUE,   2.0),
    ('Control loop',     CYAN,   3.7),
    ('Resilience',       MAG,    5.4),
    ('Coordination',     ORANGE, 7.1),
    ('Lifecycle',        GREEN,  8.8),
    ('Gating',           PURPLE, 10.5),
]

fam_x = 3.5
fam_w = 2.8
fam_h = 0.85

for name, color, y in families:
    ax.add_patch(FancyBboxPatch((fam_x - fam_w/2, y - fam_h/2),
                                fam_w, fam_h,
                                boxstyle='round,pad=0.05',
                                facecolor=PAN, edgecolor=color,
                                linewidth=1.8, zorder=3))
    ax.text(fam_x, y, name,
            ha='center', va='center',
            color=color, fontsize=11, fontweight='bold', zorder=4)

# Section label for mechanism families
ax.text(fam_x, 11.2, 'MECHANISM FAMILIES',
        ha='center', va='center',
        color=SILVER, fontsize=10, fontweight='bold')
ax.text(fam_x, 10.85, '(from OPSDB-9)',
        ha='center', va='center',
        color=DIM, fontsize=8.5, style='italic')

# Right column: runner kinds
runners = [
    ('Puller',                BLUE,   1.5),
    ('Reactor',               BLUE,   2.6),
    ('Reconciler',            CYAN,   3.7),
    ('Drift Detector',        CYAN,   4.8),
    ('Failover Handler',      MAG,    5.9),
    ('Change-Set Executor',   ORANGE, 7.0),
    ('Scheduler',             ORANGE, 8.1),
    ('Bootstrapper',          GREEN,  9.2),
    ('Reaper',                GREEN,  10.3),
    ('Verifier',              PURPLE, 11.0),
]

run_x = 16.5
run_w = 3.4
run_h = 0.75

for name, color, y in runners:
    ax.add_patch(FancyBboxPatch((run_x - run_w/2, y - run_h/2),
                                run_w, run_h,
                                boxstyle='round,pad=0.05',
                                facecolor=PAN, edgecolor=color,
                                linewidth=1.6, zorder=3))
    ax.text(run_x, y, name,
            ha='center', va='center',
            color=color, fontsize=10, fontweight='bold', zorder=4)

ax.text(run_x, 11.85, 'RUNNER KINDS',
        ha='center', va='center',
        color=SILVER, fontsize=10, fontweight='bold')
ax.text(run_x, 11.50, '(from OPSDB-5)',
        ha='center', va='center',
        color=DIM, fontsize=8.5, style='italic')

# Connections: runner -> family
# (runner_y, family_y, color)
connections = [
    (1.5,  2.0,  BLUE),    # Puller -> Sensing
    (2.6,  2.0,  BLUE),    # Reactor -> Sensing
    (2.6,  3.7,  CYAN),    # Reactor -> Control loop
    (3.7,  3.7,  CYAN),    # Reconciler -> Control loop
    (3.7,  2.0,  BLUE),    # Reconciler -> Sensing
    (4.8,  3.7,  CYAN),    # Drift Detector -> Control loop
    (4.8,  2.0,  BLUE),    # Drift Detector -> Sensing
    (5.9,  5.4,  MAG),     # Failover Handler -> Resilience
    (5.9,  7.1,  ORANGE),  # Failover Handler -> Coordination
    (7.0,  7.1,  ORANGE),  # Change-Set Executor -> Coordination
    (8.1,  7.1,  ORANGE),  # Scheduler -> Coordination
    (8.1,  3.7,  CYAN),    # Scheduler -> Control loop
    (9.2,  8.8,  GREEN),   # Bootstrapper -> Lifecycle
    (9.2,  3.7,  CYAN),    # Bootstrapper -> Control loop
    (10.3, 8.8,  GREEN),   # Reaper -> Lifecycle
    (11.0, 10.5, PURPLE),  # Verifier -> Gating
    (11.0, 2.0,  BLUE),    # Verifier -> Sensing
]

for ry, fy, color in connections:
    ax.plot([fam_x + fam_w/2, run_x - run_w/2],
            [fy, ry],
            color=color, linewidth=1.2, alpha=0.5, zorder=2)

# Bottom note
ax.add_patch(FancyBboxPatch((1.5, 0.3), 17, 0.85,
                            boxstyle='round,pad=0.08',
                            facecolor=BG, edgecolor=DIM,
                            linewidth=1.0, alpha=0.85))
ax.text(10, 0.7,
        'Some runners draw from multiple families.  '
        'New kinds register a new runner_spec_type and inherit the pattern.',
        ha='center', va='center',
        color=SILVER, fontsize=9.5, style='italic')

save(fig, 'infra4_02_runner_kinds_to_families.png')


# ================================================================
# FIG 3: COORDINATION THROUGH SHARED SUBSTRATE
# Type: 5 (Connection Map)
# Shows: Three runners around the OpsDB with no direct edges; coordination through data
# ================================================================

print("Fig 3: Coordination through shared substrate")

fig, ax = plt.subplots(figsize=(16, 13))
hide_axis(ax)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')

ax.text(0, 8.8, 'Coordination Through Shared Substrate',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(0, 8.0,
        'No direct edges between runners.  Coordination is reading what other runners wrote.',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# OpsDB at center
opsdb_radius = 2.4
center = Circle((0, 0), opsdb_radius,
                facecolor=GOLD, edgecolor=WHITE,
                linewidth=2.5, alpha=0.85, zorder=10)
ax.add_patch(center)
ax.text(0, 0.4, 'OpsDB',
        ha='center', va='center',
        color=BG, fontsize=14, fontweight='bold', zorder=11)
ax.text(0, -0.3, 'rendezvous',
        ha='center', va='center',
        color=BG, fontsize=10, fontweight='bold', zorder=11)
ax.text(0, -0.85, 'no orchestration',
        ha='center', va='center',
        color=BG, fontsize=8.5, style='italic', zorder=11)

# Three runners at 120 degree intervals
runner_radius = 5.5

runners = [
    (90,  'Drift Detector',
     ['reads:',
      ' service desired',
      ' observation_cache',
      'writes:',
      ' change_set (proposed)',
      ' runner_job'],
     CYAN, 1),
    (210, 'Change-Set\nExecutor',
     ['reads:',
      ' change_set (approved)',
      ' field_change rows',
      'writes:',
      ' entity rows updated',
      ' *_version rows',
      ' runner_job'],
     ORANGE, 2),
    (330, 'Helm Git\nExporter',
     ['reads:',
      ' helm_release_version',
      ' configuration_variable',
      'writes:',
      ' runner_job_output_var',
      ' (commit hash)'],
     MAG, 3),
]

runner_w = 4.0
runner_h = 3.4

for angle_deg, name, content, color, seq in runners:
    angle = np.radians(angle_deg)
    rx = runner_radius * np.cos(angle)
    ry = runner_radius * np.sin(angle)

    # Runner box
    ax.add_patch(FancyBboxPatch((rx - runner_w/2, ry - runner_h/2),
                                runner_w, runner_h,
                                boxstyle='round,pad=0.08',
                                facecolor=PAN, edgecolor=color,
                                linewidth=2, zorder=4))
    ax.text(rx, ry + runner_h/2 - 0.4, name,
            ha='center', va='center',
            color=color, fontsize=11, fontweight='bold', zorder=5)

    # Sequence number
    seq_offset_x = -runner_w/2 + 0.4
    seq_offset_y = runner_h/2 - 0.4
    ax.add_patch(Circle((rx + seq_offset_x, ry + seq_offset_y),
                        0.32,
                        facecolor=BG, edgecolor=color,
                        linewidth=1.5, zorder=6))
    ax.text(rx + seq_offset_x, ry + seq_offset_y, str(seq),
            ha='center', va='center',
            color=color, fontsize=10, fontweight='bold', zorder=7)

    # Content
    for i, line in enumerate(content):
        is_header = line.endswith(':')
        ax.text(rx, ry + 0.4 - i * 0.32, line,
                ha='center', va='center',
                color=GOLD if is_header else WHITE,
                fontsize=8.5,
                fontweight='bold' if is_header else 'normal',
                family='monospace', zorder=5)

    # Read arrow (OpsDB to runner)
    edge_x = rx - opsdb_radius * np.cos(angle) * 0.42
    edge_y = ry - opsdb_radius * np.sin(angle) * 0.42

    # From OpsDB edge to runner edge
    opsdb_edge_x = opsdb_radius * np.cos(angle)
    opsdb_edge_y = opsdb_radius * np.sin(angle)
    runner_edge_x = rx - (runner_w/2 - 0.1) * np.cos(angle)
    runner_edge_y = ry - (runner_h/2 - 0.1) * np.sin(angle)

    # Two-way arrow showing read+write
    draw_arrow(ax, opsdb_edge_x, opsdb_edge_y,
               runner_edge_x, runner_edge_y,
               color=color, lw=2.0, style='<->', alpha=0.9)

# Sequence flow annotations
ax.text(0, -7.5, 'Sequence (each runner runs on its own cycle):',
        ha='center', va='center',
        color=GOLD, fontsize=11, fontweight='bold')

seq_text = [
    ('1. Drift Detector cycle:  detects drift -> writes change_set (proposed)',
     CYAN),
    ('   ...time passes, change_set goes through approval...',
     DIM),
    ('2. Change-Set Executor cycle:  reads approved change_set -> applies fields',
     ORANGE),
    ('3. Helm Git Exporter cycle:  reads updated helm_release_version -> commits to git',
     MAG),
]
for i, (line, color) in enumerate(seq_text):
    ax.text(0, -8.1 - i * 0.36, line,
            ha='center', va='center',
            color=color, fontsize=9.5,
            family='monospace' if i != 1 else None,
            style='italic' if i == 1 else 'normal')

# Note about no direct edges
ax.add_patch(FancyBboxPatch((-9.5, -10.0), 6, 1.4,
                            boxstyle='round,pad=0.1',
                            facecolor=BG, edgecolor=GREEN,
                            linewidth=1.2, alpha=0.9))
ax.text(-6.5, -9.3, 'NO direct edges',
        ha='center', va='center',
        color=GREEN, fontsize=10, fontweight='bold')
ax.text(-6.5, -9.75, 'between runners',
        ha='center', va='center',
        color=WHITE, fontsize=9)

ax.add_patch(FancyBboxPatch((3.5, -10.0), 6, 1.4,
                            boxstyle='round,pad=0.1',
                            facecolor=BG, edgecolor=GREEN,
                            linewidth=1.2, alpha=0.9))
ax.text(6.5, -9.3, 'data IS the coordination',
        ha='center', va='center',
        color=GREEN, fontsize=10, fontweight='bold')
ax.text(6.5, -9.75, 'crash one - others continue',
        ha='center', va='center',
        color=WHITE, fontsize=9)

save(fig, 'infra4_03_coordination_through_substrate.png')


# ================================================================
# FIG 4: CHANGE-MANAGEMENT GATING - THREE RUNNER PATHS
# Type: 7 (Progression/Sequence Diagram)
# Shows: Three gating modes, three runner paths
# ================================================================

print("Fig 4: Change-management gating - three runner paths")

fig, ax = plt.subplots(figsize=(18, 12))
hide_axis(ax)
ax.set_xlim(0, 20)
ax.set_ylim(0, 13)

ax.text(10, 12.3, 'Change-Management Gating - Three Runner Paths',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(10, 11.65,
        'Same pipeline, three policies.  Per-runner, per-target, expressed as data.',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# Three rows
row_y = [9.0, 5.8, 2.6]
row_labels = ['DIRECT WRITE', 'AUTO-APPROVED', 'APPROVAL-REQUIRED']
row_colors = [BLUE, GREEN, MAG]
row_subtitles = [
    'observation only - no change management',
    'change_set submitted, policy auto-approves',
    'change_set submitted, routes to humans',
]
row_examples = [
    'pullers, verifiers, reapers',
    'drift correctors (low-stakes), cert renewers, scheduled rotations',
    'production database changes, security policy changes, schema changes',
]

# Row labels on left
for i, (y, label, color, subtitle, example) in enumerate(
        zip(row_y, row_labels, row_colors, row_subtitles, row_examples)):
    ax.text(0.5, y + 0.3, label,
            ha='left', va='center',
            color=color, fontsize=12, fontweight='bold')
    ax.text(0.5, y - 0.15, subtitle,
            ha='left', va='center',
            color=SILVER, fontsize=9, style='italic')
    ax.text(0.5, y - 0.6, 'examples:  ' + example,
            ha='left', va='center',
            color=DIM, fontsize=8.5)

# Pipeline stages for each row
def draw_path_stage(ax, x, y, w, h, label, fill, edge, text_color=WHITE,
                    fontsize=9, fontweight='bold', alpha=1.0):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                boxstyle='round,pad=0.05',
                                facecolor=fill, edgecolor=edge,
                                linewidth=1.5, alpha=alpha, zorder=3))
    ax.text(x, y, label,
            ha='center', va='center',
            color=text_color, fontsize=fontsize,
            fontweight=fontweight, zorder=4)


# Common: runner box on left
runner_x = 6.5
runner_w = 2.0
runner_h = 0.85
target_x = 17.5

# Row 1: Direct write
y = row_y[0]
draw_path_stage(ax, runner_x, y, runner_w, runner_h, 'Runner',
                fill=PAN, edge=BLUE)
draw_path_stage(ax, 11.0, y, 2.6, runner_h, 'API write',
                fill=PAN, edge=BLUE, fontsize=9)
draw_path_stage(ax, 14.5, y, 2.4, runner_h, 'audit_log_entry',
                fill=PAN, edge=BLUE, fontsize=9, text_color=BLUE)
draw_path_stage(ax, target_x, y, 2.4, runner_h, 'observation_\ncache_*',
                fill=PAN, edge=GOLD, text_color=GOLD, fontsize=9)
draw_arrow(ax, runner_x + runner_w/2, y, 11.0 - 1.3, y,
           color=BLUE, lw=1.5)
draw_arrow(ax, 11.0 + 1.3, y, 14.5 - 1.2, y,
           color=BLUE, lw=1.5)
draw_arrow(ax, 14.5 + 1.2, y, target_x - 1.2, y,
           color=BLUE, lw=1.5)

# Row 2: Auto-approved change set
y = row_y[1]
draw_path_stage(ax, runner_x, y, runner_w, runner_h, 'Runner',
                fill=PAN, edge=GREEN)
draw_path_stage(ax, 9.5, y, 2.0, runner_h, 'change_set\nproposed',
                fill=PAN, edge=GREEN, fontsize=9)
# Auto-gate (small)
draw_path_stage(ax, 12.0, y, 1.4, runner_h * 0.85, 'auto-\napprove',
                fill=BG, edge=GREEN, fontsize=8.5,
                text_color=GREEN, fontweight='bold')
draw_path_stage(ax, 14.5, y, 2.0, runner_h, 'executor\napplies',
                fill=PAN, edge=GREEN, fontsize=9)
draw_path_stage(ax, target_x, y, 2.4, runner_h, 'entity rows\n+ *_version',
                fill=PAN, edge=GOLD, text_color=GOLD, fontsize=9)
draw_arrow(ax, runner_x + runner_w/2, y, 9.5 - 1.0, y,
           color=GREEN, lw=1.5)
draw_arrow(ax, 9.5 + 1.0, y, 12.0 - 0.7, y,
           color=GREEN, lw=1.5)
draw_arrow(ax, 12.0 + 0.7, y, 14.5 - 1.0, y,
           color=GREEN, lw=1.5)
draw_arrow(ax, 14.5 + 1.0, y, target_x - 1.2, y,
           color=GREEN, lw=1.5)

# Policy annotation
ax.text(12.0, y + 0.85, 'policy data\nmatches rule',
        ha='center', va='center',
        color=GREEN, fontsize=8, style='italic',
        bbox=dict(boxstyle='round,pad=0.2',
                  facecolor=BG, edgecolor=GREEN, linewidth=0.6))

# Row 3: Approval-required change set
y = row_y[2]
draw_path_stage(ax, runner_x, y, runner_w, runner_h, 'Runner',
                fill=PAN, edge=MAG)
draw_path_stage(ax, 9.5, y, 2.0, runner_h, 'change_set\nproposed',
                fill=PAN, edge=MAG, fontsize=9)
# Human gate (large)
ax.add_patch(FancyBboxPatch((11.7, y - 0.6),
                            2.6, 1.2,
                            boxstyle='round,pad=0.05',
                            facecolor=BG, edgecolor=MAG,
                            linewidth=2, zorder=3))
ax.text(13.0, y + 0.20, 'human\napprovers',
        ha='center', va='center',
        color=MAG, fontsize=9, fontweight='bold', zorder=4)
# Approver dots
for j in range(3):
    ax.add_patch(Circle((12.4 + j * 0.6, y - 0.3), 0.15,
                        facecolor=MAG, edgecolor=WHITE,
                        linewidth=0.8, zorder=5))

draw_path_stage(ax, 15.6, y, 1.6, runner_h, 'executor\napplies',
                fill=PAN, edge=MAG, fontsize=9)
draw_path_stage(ax, target_x + 0.2, y, 2.0, runner_h, 'entity rows\n+ *_version',
                fill=PAN, edge=GOLD, text_color=GOLD, fontsize=9)

draw_arrow(ax, runner_x + runner_w/2, y, 9.5 - 1.0, y,
           color=MAG, lw=1.5)
draw_arrow(ax, 9.5 + 1.0, y, 11.7, y,
           color=MAG, lw=1.5)
draw_arrow(ax, 11.7 + 2.6, y, 15.6 - 0.8, y,
           color=MAG, lw=1.5)
draw_arrow(ax, 15.6 + 0.8, y, target_x + 0.2 - 1.0, y,
           color=MAG, lw=1.5)

ax.text(13.0, y + 1.0, 'rule routes\nfor approval',
        ha='center', va='center',
        color=MAG, fontsize=8, style='italic',
        bbox=dict(boxstyle='round,pad=0.2',
                  facecolor=BG, edgecolor=MAG, linewidth=0.6))

# Bottom note
ax.add_patch(FancyBboxPatch((1, 0.3), 18, 1.2,
                            boxstyle='round,pad=0.1',
                            facecolor=BG, edgecolor=GOLD,
                            linewidth=1.2, alpha=0.85))
ax.text(10, 1.08,
        'Same runner code, three different gating policies.',
        ha='center', va='center',
        color=GOLD, fontsize=10.5, fontweight='bold')
ax.text(10, 0.62,
        'A drift corrector might auto-approve in staging, route to humans in production, '
        'refuse to act on compliance-restricted entities.',
        ha='center', va='center',
        color=SILVER, fontsize=9, style='italic')

save(fig, 'infra4_04_gating_three_paths.png')


# ================================================================
# FIG 5: THE GITOPS DEPLOYMENT CAST
# Type: 7 (Progression/Sequence Diagram)
# Shows: Six runners coordinating one deployment through OpsDB rows
# ================================================================

print("Fig 5: The GitOps deployment cast")

fig, ax = plt.subplots(figsize=(18, 12))
hide_axis(ax)
ax.set_xlim(0, 20)
ax.set_ylim(0, 13)

ax.text(10, 12.3, 'The GitOps Deployment Cast - Six Runners, One Deployment',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(10, 11.65,
        'Each runner small, single-purpose, coordinating through OpsDB rows',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# OpsDB strip across the bottom
opsdb_y = 1.8
opsdb_h = 1.2
ax.add_patch(FancyBboxPatch((0.5, opsdb_y - opsdb_h/2),
                            19.0, opsdb_h,
                            boxstyle='round,pad=0.05',
                            facecolor=BG, edgecolor=GOLD,
                            linewidth=2.0, zorder=2))
ax.text(10, opsdb_y + 0.15, 'OpsDB',
        ha='center', va='center',
        color=GOLD, fontsize=13, fontweight='bold', zorder=3)
ax.text(10, opsdb_y - 0.30,
        'change_set | runner_job | runner_job_output_var | observation_cache_state | evidence_record | audit_log_entry',
        ha='center', va='center',
        color=WHITE, fontsize=8.5, family='monospace', zorder=3)

# Six runners across the top
runner_y = 7.8
runner_w = 2.6
runner_h = 1.8

cast = [
    (2.2,  'Helm\nChange-Set\nExecutor',  ORANGE, '1'),
    (5.4,  'Helm\nGit\nExporter',          MAG,    '2'),
    (8.6,  'Argo CD\n/ Flux\n(external)',  DIM,    '3'),
    (11.8, 'Deploy\nWatcher',              CYAN,   '4'),
    (15.0, 'Image\nDigest\nVerifier',      GREEN,  '5'),
    (18.0, 'Drift\nDetector',              BLUE,   '6'),
]

for i, (x, name, color, seq) in enumerate(cast):
    is_external = (i == 2)
    edge_style = '--' if is_external else '-'

    box = FancyBboxPatch((x - runner_w/2, runner_y - runner_h/2),
                         runner_w, runner_h,
                         boxstyle='round,pad=0.08',
                         facecolor=PAN if not is_external else BG,
                         edgecolor=color,
                         linewidth=1.8 if not is_external else 1.5,
                         linestyle=edge_style,
                         zorder=4)
    ax.add_patch(box)
    ax.text(x, runner_y + 0.1, name,
            ha='center', va='center',
            color=color, fontsize=10, fontweight='bold', zorder=5)

    # Sequence circle
    ax.add_patch(Circle((x - runner_w/2 + 0.35, runner_y + runner_h/2 - 0.3),
                        0.28,
                        facecolor=BG, edgecolor=color,
                        linewidth=1.5, zorder=6))
    ax.text(x - runner_w/2 + 0.35, runner_y + runner_h/2 - 0.3, seq,
            ha='center', va='center',
            color=color, fontsize=10, fontweight='bold', zorder=7)

    # Read/write annotations under each runner
    if i == 0:
        rw = 'reads:\n change_set\nwrites:\n entity rows updated\n output_var ready'
    elif i == 1:
        rw = 'reads:\n new helm_release_\n version\nwrites:\n output_var\n (commit hash)'
    elif i == 2:
        rw = 'NOT OpsDB-aware\nwatches git\napplies to cluster'
    elif i == 3:
        rw = 'reads:\n cluster watch\nwrites:\n observation_cache_state\n output_vars\n (rollout outcome)'
    elif i == 4:
        rw = 'reads:\n change_set intent\n deploy outcome\nwrites:\n evidence_record\n (or finding)'
    elif i == 5:
        rw = 'reads:\n OpsDB-known\n cluster-observed\nwrites:\n change_set\n (if drift)'

    color_rw = color if not is_external else DIM
    ax.text(x, runner_y - runner_h/2 - 1.1, rw,
            ha='center', va='center',
            color=color_rw, fontsize=7.5,
            family='monospace', zorder=4)

# Arrows from runners DOWN to OpsDB (write) and UP from OpsDB (read)
for i, (x, name, color, seq) in enumerate(cast):
    is_external = (i == 2)
    if is_external:
        # External tool: arrows show git-side flow
        # arrow from runner 2 (git exporter) to argo (this runner)
        continue

    # Simplified: a single bidirectional connection to OpsDB
    draw_arrow(ax, x, runner_y - runner_h/2 - 1.9,
               x, opsdb_y + opsdb_h/2 + 0.05,
               color=color, lw=1.4, alpha=0.8, style='<->')

# External tool gets dashed arrows showing git relationship
# Runner 2 -> external (git push)
ax.annotate('git push',
            xy=(8.6 - runner_w/2, runner_y),
            xytext=(5.4 + runner_w/2, runner_y),
            color=DIM, fontsize=8, style='italic',
            ha='center', va='center',
            arrowprops=dict(arrowstyle='->', color=DIM, lw=1.2,
                            linestyle='--', alpha=0.7))
# External tool -> cluster (kubectl apply)
ax.text(8.6, runner_y - runner_h/2 - 1.0,
        'applies to\nK8s cluster',
        ha='center', va='center',
        color=DIM, fontsize=7.5, style='italic',
        family='monospace')

# Cluster watch shown as arrow from cluster (implicit) to runner 4
ax.text(11.8 - 0.8, runner_y + runner_h/2 + 0.5,
        'cluster\nwatch',
        ha='right', va='center',
        color=CYAN, fontsize=8, style='italic',
        family='monospace')

# Sequence flow at top
seq_y = 11.0
seq_text = '1. CS approved & applied  ->  2. Render & commit  ->  3. Argo applies  ->  4. Watch & record  ->  5. Verify digest  ->  6. Drift check'
ax.text(10, seq_y, seq_text,
        ha='center', va='center',
        color=GOLD, fontsize=10, fontweight='bold',
        family='monospace')

# Bottom: the trail
ax.text(10, 0.5,
        'Each runner writes structured rows the next consumes.  '
        'The full deployment trail is one query joining the OpsDB tables.',
        ha='center', va='center',
        color=DIM, fontsize=9.5, style='italic')

save(fig, 'infra4_05_gitops_cast.png')


# ================================================================
# FIG 6: THE SHARED-LIBRARY SUITE AS FRAMEWORK LAYER
# Type: 4 (Geometric Cross-Section)
# Shows: Layered architecture - runners, libraries, OpsDB and world
# ================================================================

print("Fig 6: Shared-library suite as framework layer")

fig, ax = plt.subplots(figsize=(18, 12))
hide_axis(ax)
ax.set_xlim(0, 20)
ax.set_ylim(0, 13)

ax.text(10, 12.3, 'The Shared-Library Suite as Framework Layer',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(10, 11.65,
        'Runners stay small because the libraries do the heavy lifting',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# Top layer: many small runners
runner_layer_y = 9.6
runner_layer_h = 1.4
ax.text(0.5, runner_layer_y + runner_layer_h/2 + 0.45,
        'RUNNERS',
        ha='left', va='center',
        color=GOLD, fontsize=10, fontweight='bold')
ax.text(0.5, runner_layer_y + runner_layer_h/2 + 0.1,
        '~200-500 lines each',
        ha='left', va='center',
        color=SILVER, fontsize=8.5, style='italic')

# Draw 14 small runner boxes
n_runners = 14
runner_box_w = 1.1
runner_box_spacing = (19.0 - 0.5 - n_runners * runner_box_w) / (n_runners - 1)
runner_names = [
    'Puller', 'Reactor', 'Reconciler',
    'Drift\nDetector', 'Failover', 'CS\nExecutor',
    'Scheduler', 'Bootstrap', 'Reaper',
    'Verifier', 'Helm\nExporter', 'Deploy\nWatcher',
    'Cert\nRenewer', 'Compliance\nScanner',
]
runner_box_colors = [BLUE, BLUE, CYAN, CYAN, MAG, ORANGE,
                     ORANGE, GREEN, GREEN, PURPLE, MAG, CYAN,
                     CYAN, PURPLE]
for i in range(n_runners):
    x = 0.5 + i * (runner_box_w + runner_box_spacing)
    color = runner_box_colors[i]
    ax.add_patch(FancyBboxPatch((x, runner_layer_y),
                                runner_box_w, runner_layer_h,
                                boxstyle='round,pad=0.03',
                                facecolor=PAN, edgecolor=color,
                                linewidth=1.2, zorder=3))
    ax.text(x + runner_box_w/2, runner_layer_y + runner_layer_h/2,
            runner_names[i],
            ha='center', va='center',
            color=color, fontsize=7.5,
            fontweight='bold', zorder=4)

# Middle layer: shared libraries
lib_layer_y = 5.5
lib_layer_h = 2.8
lib_layer_x = 1.0
lib_layer_w = 18.0
ax.add_patch(FancyBboxPatch((lib_layer_x, lib_layer_y),
                            lib_layer_w, lib_layer_h,
                            boxstyle='round,pad=0.1',
                            facecolor=PAN, edgecolor=GOLD,
                            linewidth=2.5, zorder=3))
ax.text(0.5, lib_layer_y + lib_layer_h + 0.3,
        'SHARED LIBRARIES  (the framework)',
        ha='left', va='center',
        color=GOLD, fontsize=10, fontweight='bold')
ax.text(0.5, lib_layer_y - 0.25,
        'one way to do each thing  -  versioned, tested, released',
        ha='left', va='center',
        color=SILVER, fontsize=8.5, style='italic')

# Library categories inside the layer
lib_categories = [
    ('OpsDB API\nclient',  CYAN),
    ('Kubernetes\nops',    BLUE),
    ('Cloud ops\n(AWS/GCP/Azure)', MAG),
    ('Secret\naccess',     PURPLE),
    ('Logging &\nmetrics', GREEN),
    ('Retry &\nbackoff',   ORANGE),
    ('Notifications\n(email/chat/page)', CYAN),
    ('SSH /\nremote exec', DIM),
    ('Git\nops',           MAG),
]

n_libs = len(lib_categories)
lib_inner_padding = 0.3
lib_inner_x = lib_layer_x + lib_inner_padding
lib_inner_w = lib_layer_w - 2 * lib_inner_padding
lib_box_w = (lib_inner_w - (n_libs - 1) * 0.15) / n_libs
lib_box_h = lib_layer_h - 0.7
lib_box_y = lib_layer_y + 0.35

for i, (name, color) in enumerate(lib_categories):
    x = lib_inner_x + i * (lib_box_w + 0.15)
    ax.add_patch(FancyBboxPatch((x, lib_box_y),
                                lib_box_w, lib_box_h,
                                boxstyle='round,pad=0.05',
                                facecolor=BG, edgecolor=color,
                                linewidth=1.3, zorder=4))
    ax.text(x + lib_box_w/2, lib_box_y + lib_box_h/2,
            name,
            ha='center', va='center',
            color=color, fontsize=9, fontweight='bold', zorder=5)

# Bottom layer: OpsDB and world side-by-side
bottom_y = 1.8
bottom_h = 1.6

# OpsDB (left)
ax.add_patch(FancyBboxPatch((1.0, bottom_y),
                            8.5, bottom_h,
                            boxstyle='round,pad=0.1',
                            facecolor=BG, edgecolor=GOLD,
                            linewidth=2.5, zorder=3))
ax.text(5.25, bottom_y + bottom_h - 0.35,
        'OpsDB',
        ha='center', va='center',
        color=GOLD, fontsize=13, fontweight='bold', zorder=4)
ax.text(5.25, bottom_y + 0.4,
        'data substrate (passive)\nthe stable interface',
        ha='center', va='center',
        color=WHITE, fontsize=9, zorder=4)

# World (right)
ax.add_patch(FancyBboxPatch((10.5, bottom_y),
                            8.5, bottom_h,
                            boxstyle='round,pad=0.1',
                            facecolor=BG, edgecolor=DIM,
                            linewidth=1.5, zorder=3))
ax.text(14.75, bottom_y + bottom_h - 0.35,
        'the world',
        ha='center', va='center',
        color=SILVER, fontsize=13, fontweight='bold', zorder=4)
ax.text(14.75, bottom_y + 0.4,
        'K8s clusters | cloud APIs | hosts | vault\nmonitoring authorities | git registries',
        ha='center', va='center',
        color=WHITE, fontsize=9, zorder=4)

# Connections between layers (suggestive, not exhaustive)
# Runners -> Libraries
for i in [1, 4, 7, 10, 13]:
    x = 0.5 + i * (runner_box_w + runner_box_spacing) + runner_box_w/2
    ax.plot([x, x], [runner_layer_y, lib_layer_y + lib_layer_h],
            color=DIM, linewidth=0.6, alpha=0.5, zorder=2)

# Libraries -> OpsDB and World
ax.plot([5.25, 5.25], [lib_layer_y, bottom_y + bottom_h],
        color=GOLD, linewidth=1.5, alpha=0.6, zorder=2)
ax.plot([14.75, 14.75], [lib_layer_y, bottom_y + bottom_h],
        color=SILVER, linewidth=1.5, alpha=0.6, zorder=2)

# Side annotation
ax.text(19.5, lib_layer_y + lib_layer_h/2 + 0.4,
        'all\nrunners\nuse',
        ha='right', va='center',
        color=GOLD, fontsize=9, fontweight='bold', style='italic')

# Bottom note
ax.text(10, 0.7,
        'a runner without the suite is 1500 lines, mostly reinvented basics.  '
        'with the suite, 200 lines of runner-specific logic.',
        ha='center', va='center',
        color=DIM, fontsize=9.5, style='italic')

save(fig, 'infra4_06_shared_library_framework.png')


# ================================================================
# FIG 7: IDEMPOTENCY CONVERGENCE
# Type: 1 (Running/Convergence Chart)
# Shows: Multiple drift starting points converging to the same desired end state
# ================================================================

print("Fig 7: Idempotency convergence")

fig, ax = plt.subplots(figsize=(16, 10))
style_axis(ax)

ax.set_title('Idempotency Convergence - Same End State From Different Starts',
             color=GOLD, fontsize=15, fontweight='bold', pad=14)

# x = reconciler cycle number
# y = "drift magnitude" (1.0 = fully drifted, 0.0 = matches desired)
cycles = np.arange(0, 12)

# Multiple starting drift positions, all converging to 0
np.random.seed(7)

starts = [
    (0.95,  'severe drift\n(missing replica)',     RED),
    (0.75,  'major drift\n(stale config)',         ORANGE),
    (0.50,  'moderate drift\n(label mismatch)',    GOLD),
    (0.30,  'minor drift\n(small param off)',      CYAN),
    (0.10,  'near-converged\n(tiny offset)',       GREEN),
    (0.00,  'already converged\n(no action)',      BLUE),
]

# Each curve approaches 0 with a step-function shape
# (idempotent reconcilers correct in one or two cycles when possible)
for start, label, color in starts:
    if start == 0.0:
        # Already converged: stays at 0
        y = np.zeros_like(cycles, dtype=float)
    else:
        # Sharp convergence within ~2-3 cycles, then flat
        decay_rate = 0.7
        y = start * (decay_rate ** cycles.astype(float))
        # Add small noise except at end
        y = y + np.random.normal(0, 0.005, len(cycles))
        # Clip to non-negative
        y = np.clip(y, 0, 1)
        # After cycle 4, snap to ~0 (idempotency: nothing more to do)
        y[4:] = np.maximum(y[4:] * 0.05, 0)

    ax.plot(cycles, y,
            color=color, linewidth=2.5,
            marker='o', markersize=8,
            markeredgecolor=WHITE, markeredgewidth=1.0,
            label=label, zorder=4)

# Mark the desired-state line at y=0
ax.axhline(0, color=GOLD, linewidth=1.5, linestyle='--',
           alpha=0.8, zorder=3)
ax.text(11.3, 0.04, 'desired state',
        ha='right', va='bottom',
        color=GOLD, fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.25',
                  facecolor=BG, edgecolor=GOLD, linewidth=0.8))

# Shaded "converged" zone
ax.axhspan(-0.04, 0.04, color=GREEN, alpha=0.08, zorder=1)

# Annotations
ax.annotate('idempotent re-runs:\nsame state in,\nno additional changes',
            xy=(7, 0.0),
            xytext=(7, 0.45),
            color=GREEN, fontsize=10, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.4',
                      facecolor=BG, edgecolor=GREEN, linewidth=1.2),
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.4))

ax.annotate('reconcilers converge\nin 1-3 cycles',
            xy=(2, 0.30),
            xytext=(3.8, 0.65),
            color=GOLD, fontsize=10, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.4',
                      facecolor=BG, edgecolor=GOLD, linewidth=1.2),
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.4))

# Axes
ax.set_xlabel('reconciler cycle number',
              color=SILVER, fontsize=11, labelpad=8)
ax.set_ylabel('drift magnitude  (1.0 = fully drifted, 0 = matches desired)',
              color=SILVER, fontsize=11, labelpad=8)
ax.set_xlim(-0.5, 11.5)
ax.set_ylim(-0.05, 1.05)
ax.set_xticks(cycles)

# Legend
leg = ax.legend(loc='upper right',
                facecolor=PAN, edgecolor=DIM,
                labelcolor=WHITE, fontsize=9,
                framealpha=0.95)

save(fig, 'infra4_07_idempotency_convergence.png')


# ================================================================
# FIG 8: STANDARD vs OPSDB-COORDINATED ALERT RESPONSE
# Type: 6 (Comparison Bar Chart) - parallel structured columns
# Shows: Same incident response, two trails: scattered tools vs structured substrate
# ================================================================

print("Fig 8: Standard vs OpsDB-coordinated alert response")

fig, ax = plt.subplots(figsize=(18, 13))
hide_axis(ax)
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)

ax.text(10, 13.4, 'Standard Practice vs OpsDB-Coordinated  -  Alert Response',
        ha='center', va='center',
        color=GOLD, fontsize=16, fontweight='bold')
ax.text(10, 12.7,
        'Same engineer, same incident.  The difference is what gets recorded.',
        ha='center', va='center',
        color=SILVER, fontsize=11)

# Two columns
col_left_x = 1.0
col_right_x = 11.0
col_w = 8.0
col_top = 11.8
col_bottom = 1.8

# Column headers
ax.add_patch(FancyBboxPatch((col_left_x, col_top - 0.6),
                            col_w, 0.7,
                            boxstyle='round,pad=0.05',
                            facecolor=PAN, edgecolor=RED,
                            linewidth=2, zorder=3))
ax.text(col_left_x + col_w/2, col_top - 0.25,
        'STANDARD K8S SHOP', ha='center', va='center',
        color=RED, fontsize=12, fontweight='bold', zorder=4)

ax.add_patch(FancyBboxPatch((col_right_x, col_top - 0.6),
                            col_w, 0.7,
                            boxstyle='round,pad=0.05',
                            facecolor=PAN, edgecolor=GREEN,
                            linewidth=2, zorder=3))
ax.text(col_right_x + col_w/2, col_top - 0.25,
        'OPSDB-COORDINATED', ha='center', va='center',
        color=GREEN, fontsize=12, fontweight='bold', zorder=4)

# Steps left side
left_steps = [
    ('PagerDuty pages',           '(its own schedule data)'),
    ('Open Slack',                '(find incident channel)'),
    ('Open Grafana',              '(URL bookmarked or memory)'),
    ('SSH or kubectl',            '(get pods, logs)'),
    ('Find runbook',              '(guess wiki page)'),
    ('Follow runbook',            '(commands typed)'),
    ('Update Slack',              '(status thread)'),
    ('Post-incident write-up',    '(or never)'),
]

# Steps right side
right_steps = [
    ('alert_fire row',            '(in OpsDB)'),
    ('Escalation runner pages',   '(reads on_call_assignment)'),
    ('Page includes context',     '(runbook, dashboards, recent change_sets)'),
    ('Engineer follows runbook',  '(commands as runner_jobs, gated)'),
    ('runner_job rows record',    '(actions with attribution)'),
    ('Discussion in chat',        '(linked from alert_fire)'),
    ('Runbook updated as CS',     '(last_tested_time updated)'),
    ('Trail is queryable',        '(no extra effort)'),
]

step_h = 1.05
step_gap = 0.20
total_steps_h = len(left_steps) * (step_h + step_gap) - step_gap
start_y = col_top - 1.0

# Left column steps
for i, (action, detail) in enumerate(left_steps):
    y = start_y - i * (step_h + step_gap) - step_h
    color = RED if i in [4, 7] else SILVER

    ax.add_patch(FancyBboxPatch((col_left_x + 0.2, y),
                                col_w - 0.4, step_h,
                                boxstyle='round,pad=0.04',
                                facecolor=BG, edgecolor=color,
                                linewidth=1.2, alpha=0.85, zorder=3))
    ax.text(col_left_x + 0.4, y + step_h - 0.30,
            '%d. %s' % (i + 1, action),
            ha='left', va='center',
            color=color, fontsize=10.5, fontweight='bold', zorder=4)
    ax.text(col_left_x + 0.4, y + 0.30,
            detail,
            ha='left', va='center',
            color=DIM, fontsize=8.5, style='italic', zorder=4)

# Right column steps
for i, (action, detail) in enumerate(right_steps):
    y = start_y - i * (step_h + step_gap) - step_h
    color = GREEN

    ax.add_patch(FancyBboxPatch((col_right_x + 0.2, y),
                                col_w - 0.4, step_h,
                                boxstyle='round,pad=0.04',
                                facecolor=BG, edgecolor=color,
                                linewidth=1.2, alpha=0.85, zorder=3))
    ax.text(col_right_x + 0.4, y + step_h - 0.30,
            '%d. %s' % (i + 1, action),
            ha='left', va='center',
            color=color, fontsize=10.5, fontweight='bold', zorder=4)
    ax.text(col_right_x + 0.4, y + 0.30,
            detail,
            ha='left', va='center',
            color=WHITE, fontsize=8.5, style='italic', zorder=4)

# Bottom summary boxes
summary_y = 0.6
summary_h = 0.85

# Left summary
ax.add_patch(FancyBboxPatch((col_left_x, summary_y),
                            col_w, summary_h,
                            boxstyle='round,pad=0.05',
                            facecolor=BG, edgecolor=RED,
                            linewidth=1.5, alpha=0.9, zorder=3))
ax.text(col_left_x + col_w/2, summary_y + summary_h/2,
        'data scattered across PagerDuty, Slack, Grafana, kubectl output, wiki.\n'
        'no single substrate knows what happened.',
        ha='center', va='center',
        color=SILVER, fontsize=9, style='italic', zorder=4)

# Right summary
ax.add_patch(FancyBboxPatch((col_right_x, summary_y),
                            col_w, summary_h,
                            boxstyle='round,pad=0.05',
                            facecolor=BG, edgecolor=GREEN,
                            linewidth=1.5, alpha=0.9, zorder=3))
ax.text(col_right_x + col_w/2, summary_y + summary_h/2,
        'one substrate.  every action attributed.  full trail queryable.\n'
        'the trail IS the data the operations naturally produce.',
        ha='center', va='center',
        color=WHITE, fontsize=9, style='italic', zorder=4)

save(fig, 'infra4_08_standard_vs_opsdb.png')


# ================================================================
# SUMMARY
# ================================================================

print("")
print("All 8 figures generated:")
print("  infra4_01_runner_pattern.png")
print("  infra4_02_runner_kinds_to_families.png")
print("  infra4_03_coordination_through_substrate.png")
print("  infra4_04_gating_three_paths.png")
print("  infra4_05_gitops_cast.png")
print("  infra4_06_shared_library_framework.png")
print("  infra4_07_idempotency_convergence.png")
print("  infra4_08_standard_vs_opsdb.png")
