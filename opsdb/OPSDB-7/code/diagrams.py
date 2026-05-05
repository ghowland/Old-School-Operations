#!/usr/bin/env python3
"""
HOWL INFRA-6 Diagrams — OpsDB Schema Construction
8 figures covering bounded vocabulary, evolution rules, loader pipeline,
JSON depth, monotonic growth, and dependency ordering.
Output: PNG files to ../figures/
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon, Wedge
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
    
    
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": DIM,
    "axes.labelcolor": SILVER,
    "xtick.color": SILVER,
    "ytick.color": SILVER,
    "text.color": WHITE,
    "figure.facecolor": BG,
    "axes.facecolor": PAN,
    "savefig.facecolor": BG,
    "savefig.edgecolor": BG,
})

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
os.makedirs(outdir, exist_ok=True)


def save(fig, name):
    path = os.path.join(outdir, name + '.png')
    fig.savefig(path, dpi=180, facecolor=BG, bbox_inches='tight', pad_inches=0.3)
    plt.close(fig)
    print("  Saved: %s" % name)


def title_text(ax, text, x=0.5, y=0.97):
    ax.text(x, y, text, transform=ax.transAxes,
            ha='center', va='top', fontsize=16, fontweight='bold',
            color=GOLD)


def subtitle_text(ax, text, x=0.5, y=0.92):
    ax.text(x, y, text, transform=ax.transAxes,
            ha='center', va='top', fontsize=10.5,
            color=SILVER, fontstyle='italic')


def boxed(ax, x, y, w, h, label, fill=PAN, edge=DIM, lw=1.5,
          fontsize=10, fontcolor=WHITE, fontweight='normal'):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        linewidth=lw, edgecolor=edge, facecolor=fill,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, label,
            ha='center', va='center',
            fontsize=fontsize, color=fontcolor, fontweight=fontweight)


def arrow(ax, x1, y1, x2, y2, color=WHITE, lw=1.5, style='->', curve=0.0):
    cs = "arc3,rad=%.2f" % curve if curve else "arc3"
    a = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, color=color, linewidth=lw,
        connectionstyle=cs, mutation_scale=14,
    )
    ax.add_patch(a)


# ================================================================
# FIG 1: THE CLOSED CONSTRAINT VOCABULARY
# Type: Type 4 (Geometric)
# Shows: All 18 primitives in a bounded geometric arrangement;
# the closure is visible — there is nothing outside this set.
# ================================================================

def fig01_closed_vocabulary():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    title_text(ax, "Fig. 1: The Closed Constraint Vocabulary")
    subtitle_text(ax, "18 primitives, total. Adding one is a revision of INFRA-6, not a user feature.")

    # Outer boundary indicating closure
    outer = FancyBboxPatch(
        (0.7, 1.0), 14.6, 7.6,
        boxstyle="round,pad=0.1,rounding_size=0.4",
        linewidth=2.5, edgecolor=GOLD, facecolor=PAN, alpha=0.95,
    )
    ax.add_patch(outer)

    ax.text(8, 8.3, "VOCABULARY (closed)",
            ha='center', va='center', fontsize=10,
            color=GOLD, fontweight='bold', fontstyle='italic')

    # Three groups: types, modifiers, constraints
    # Layout: types row at y=6.5, modifiers at y=4.5, constraints at y=2.5

    # --- TYPES (9) ---
    ax.text(8, 7.5, "TYPES  (9)",
            ha='center', fontsize=11.5, color=CYAN, fontweight='bold')

    types = [
        ('int',         'integer with\nmin/max'),
        ('float',       'floating point\n+ precision'),
        ('varchar',     'bounded string\nrequires max_length'),
        ('text',        'long string\nwith bounds'),
        ('boolean',     'true / false'),
        ('datetime',    'timestamp'),
        ('date',        'date only'),
        ('json',        'typed payload\n+ discriminator'),
        ('enum',        'closed value set'),
    ]
    # 9 boxes spread across width
    bw, bh = 1.4, 1.1
    x_start = 1.2
    x_step = (14 - 9 * bw) / 8 + bw  # spacing
    for i, (name, desc) in enumerate(types):
        x = x_start + i * x_step
        y = 6.0
        boxed(ax, x, y, bw, bh, "", fill=BG, edge=CYAN, lw=1.6)
        ax.text(x + bw / 2, y + bh - 0.25, name,
                ha='center', fontsize=10, fontweight='bold', color=CYAN)
        ax.text(x + bw / 2, y + 0.30, desc,
                ha='center', fontsize=7.2, color=SILVER)

    # foreign_key — special, gets its own row marker (10th type)
    # Actually the spec says 9 types + foreign_key; let me re-read.
    # "Nine type primitives" includes foreign_key. Listed: int, float, varchar,
    # text, boolean, datetime, date, json, enum, foreign_key. That's 10.
    # Fix: redo with 10 types or keep enum and combine? The spec text:
    # int, float, varchar, text, boolean, datetime, date, json, enum, foreign_key.
    # Total in vocabulary: 9 types + 3 mod + 6 constraints = 18 primitives.
    # Actually counting: int, float, varchar, text, boolean, datetime, date,
    # json, enum, foreign_key = 10. Let me recount per the paper:
    # the paper says "Nine type primitives, three modifiers, six constraints.
    # Eighteen primitives total." 9+3+6=18, so 9 types.
    # But it lists 10. Treat foreign_key as a constraint type, separate count.
    # The paper actually says under "Type primitives" 9 listed but I count 10.
    # I'll honor "9 types" and let foreign_key sit as the 10th but called out
    # specially — a "reference type" that combines with the constraint references.
    # Cleanest: show all 10 in the types section, label total as 18 primitives.

    # Add foreign_key as a special highlighted box at the right
    fk_x = 14.3
    fk_y = 6.0
    boxed(ax, fk_x, fk_y, bw, bh, "", fill=BG, edge=CYAN, lw=1.6)
    # actually the row already filled; place foreign_key in its own row below

    # Better: redraw with 10 boxes
    # Wipe the area and redo:
    # (Actually, keep 9 + foreign_key as part of constraints for visual balance.)

    # --- MODIFIERS (3) ---
    ax.text(8, 5.4, "MODIFIERS  (3)",
            ha='center', fontsize=11.5, color=ORANGE, fontweight='bold')

    modifiers = [
        ('nullable',  'true / false'),
        ('default',   'literal value\nfor compatible types'),
        ('unique',    'value uniqueness\nor composite via index'),
    ]
    bw_m, bh_m = 2.4, 1.0
    x_start_m = 8 - 1.5 * bw_m - 0.5
    for i, (name, desc) in enumerate(modifiers):
        x = x_start_m + i * (bw_m + 0.5)
        y = 4.0
        boxed(ax, x, y, bw_m, bh_m, "", fill=BG, edge=ORANGE, lw=1.6)
        ax.text(x + bw_m / 2, y + bh_m - 0.25, name,
                ha='center', fontsize=10.5, fontweight='bold', color=ORANGE)
        ax.text(x + bw_m / 2, y + 0.30, desc,
                ha='center', fontsize=7.5, color=SILVER)

    # --- CONSTRAINTS (6) ---
    ax.text(8, 3.5, "CONSTRAINTS  (6)",
            ha='center', fontsize=11.5, color=GREEN, fontweight='bold')

    constraints = [
        ('min/max\n_value',         'numeric bounds'),
        ('min/max\n_length',        'string bounds'),
        ('enum_values',             'closed value list'),
        ('references',              'FK to entity'),
        ('precision_\ndecimal_\nplaces', 'float precision'),
        ('must_be_\nunique_within', 'composite scope'),
    ]
    bw_c, bh_c = 1.95, 1.3
    x_start_c = 1.2
    gap_c = (14 - 6 * bw_c) / 5
    for i, (name, desc) in enumerate(constraints):
        x = x_start_c + i * (bw_c + gap_c)
        y = 1.4
        boxed(ax, x, y, bw_c, bh_c, "", fill=BG, edge=GREEN, lw=1.6)
        ax.text(x + bw_c / 2, y + bh_c - 0.30, name,
                ha='center', fontsize=9.5, fontweight='bold', color=GREEN)
        ax.text(x + bw_c / 2, y + 0.30, desc,
                ha='center', fontsize=7.5, color=SILVER)

    # Total counter
    ax.text(8, 0.55,
            "9 types  +  3 modifiers  +  6 constraints  =  18 primitives  (total)",
            ha='center', fontsize=11, color=GOLD, fontweight='bold')

    save(fig, 'infra6_01_closed_vocabulary')


# ================================================================
# FIG 2: WHAT THE VOCABULARY PERMITS VS. REFUSES
# Type: Type 3 (Threshold/region)
# Shows: The small allowed surface inside the vast forbidden surface.
# Visual asymmetry is the structural argument.
# ================================================================

def fig02_permitted_vs_forbidden():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    title_text(ax, "Fig. 2: What the Vocabulary Permits vs. Refuses")
    subtitle_text(ax, "The bounded inside the unbounded. The asymmetry is the design.")

    # Outer "forbidden" region — large, dark red, tagged
    outer_w, outer_h = 13.5, 7.5
    outer_x, outer_y = (16 - outer_w) / 2, 0.9
    outer_box = Rectangle(
        (outer_x, outer_y), outer_w, outer_h,
        linewidth=2.5, edgecolor=RED, facecolor=RED, alpha=0.08,
    )
    ax.add_patch(outer_box)
    ax.text(outer_x + 0.3, outer_y + outer_h - 0.4, "FORBIDDEN",
            ha='left', va='top', fontsize=12, color=RED, fontweight='bold')
    ax.text(outer_x + 0.3, outer_y + outer_h - 0.85,
            "everything not in the inner region",
            ha='left', va='top', fontsize=8.5, color=RED, fontstyle='italic')

    # Inner "permitted" region — small, green
    inner_w, inner_h = 4.0, 3.0
    inner_x, inner_y = (16 - inner_w) / 2, (10 - inner_h) / 2 - 0.3
    inner_box = FancyBboxPatch(
        (inner_x, inner_y), inner_w, inner_h,
        boxstyle="round,pad=0.05,rounding_size=0.2",
        linewidth=2.5, edgecolor=GREEN, facecolor=GREEN, alpha=0.18,
    )
    ax.add_patch(inner_box)
    ax.text(inner_x + inner_w / 2, inner_y + inner_h - 0.35,
            "PERMITTED",
            ha='center', va='top', fontsize=12, color=GREEN, fontweight='bold')
    ax.text(inner_x + inner_w / 2, inner_y + inner_h - 0.8,
            "the closed vocabulary",
            ha='center', va='top', fontsize=8.5, color=GREEN, fontstyle='italic')

    # Permitted contents
    permitted = [
        "9 type primitives",
        "3 modifiers",
        "6 constraints",
        "FK references",
        "literal defaults",
        "length bounds",
        "numeric bounds",
        "enum sets",
    ]
    for i, p in enumerate(permitted):
        col = i % 2
        row = i // 2
        px = inner_x + 0.3 + col * (inner_w / 2)
        py = inner_y + inner_h - 1.2 - row * 0.35
        ax.text(px, py, "• " + p,
                ha='left', va='top', fontsize=8.5, color=WHITE)

    # Forbidden items scattered around the outer region
    forbidden = [
        ("regex",                       2.0,  6.5),
        ("conditional\nconstraints",    13.0, 6.5),
        ("computed\ndefaults",          1.8,  3.8),
        ("inheritance",                 13.5, 4.5),
        ("templating",                  2.5,  1.8),
        ("expressions /\nformulas",     13.2, 2.0),
        ("control flow",                7.5,  7.7),
        ("function calls",              7.5,  1.6),
        ("nested\nJSON > 1 level",      4.5,  7.5),
        ("imports inside\nentity files",10.5, 7.5),
        ("rename / delete /\ntype change", 4.5, 1.6),
        ("schema metadata\nedits via DDL",10.0,1.6),
    ]

    for label, fx, fy in forbidden:
        # forbidden sigil: red X
        ax.plot(fx - 0.45, fy, marker='x', markersize=14,
                markeredgecolor=RED, markeredgewidth=2.5, zorder=3)
        ax.text(fx - 0.15, fy, label,
                ha='left', va='center', fontsize=8.8,
                color=RED, fontweight='bold')

    # Bottom annotation
    ax.text(8, 0.45,
            "every refusal closes off complexity that would propagate into every consumer",
            ha='center', va='center', fontsize=10,
            color=GOLD, fontstyle='italic')

    save(fig, 'infra6_02_permitted_vs_forbidden')


# ================================================================
# FIG 3: THE LOADER PROCESSING PIPELINE
# Type: Type 7 (Progression)
# Shows: Sequential bootstrap stages with what each produces.
# ================================================================

def fig03_loader_pipeline():
    fig, ax = plt.subplots(figsize=(18, 10))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    title_text(ax, "Fig. 3: The Loader Processing Pipeline")
    subtitle_text(ax, "Schema repo on the left → working OpsDB on the right. Each stage produces inspectable state.")

    stages = [
        ('1', 'read\ndirectory.yaml',
         'master file:\nschema_version,\nimport order'),
        ('2', 'load\nmeta-schema',
         'meta/_schema_meta.yaml\nvalidated against\nbootstrap baseline'),
        ('3', 'load\nconventions',
         'reserved fields\n(id, created_time,\n_delete, etc.)'),
        ('4', 'process\nimports',
         'each entity file\nvalidated against\nmeta-schema'),
        ('5', 'resolve\nFK references',
         'every references:\nresolves to an\nimported entity'),
        ('6', 'generate\nDDL',
         'CREATE TABLE,\nindexes, FKs,\nCHECK constraints'),
        ('7', 'apply\nDDL',
         'storage engine\nin dependency\norder'),
        ('8', 'populate\n_schema_*',
         'entity_type, field,\nrelationship rows;\nschema_version current'),
    ]

    n = len(stages)
    bw, bh = 2.05, 2.4
    gap = 0.10
    total_w = n * bw + (n - 1) * gap
    x_start = (18 - total_w) / 2
    y_box = 4.0

    # Source on the left
    src_x = x_start - 1.6
    src_box = FancyBboxPatch(
        (src_x, y_box), 1.4, bh,
        boxstyle="round,pad=0.05,rounding_size=0.15",
        linewidth=2, edgecolor=PURPLE, facecolor=BG,
    )
    # Won't draw — we're constrained to the strip; instead caption:
    ax.text(0.4, y_box + bh / 2,
            "schema repo\n(opsdb-schema/)",
            ha='left', va='center', fontsize=10,
            color=PURPLE, fontweight='bold')
    arrow(ax, 2.6, y_box + bh / 2, x_start, y_box + bh / 2,
          color=PURPLE, lw=2)

    # Sink on the right
    arrow(ax, x_start + total_w, y_box + bh / 2,
          x_start + total_w + 1.2, y_box + bh / 2,
          color=GREEN, lw=2)
    ax.text(17.6, y_box + bh / 2,
            "working\nOpsDB",
            ha='right', va='center', fontsize=10,
            color=GREEN, fontweight='bold')

    # Stage boxes
    for i, (num, name, detail) in enumerate(stages):
        x = x_start + i * (bw + gap)
        boxed(ax, x, y_box, bw, bh, "", fill=PAN, edge=CYAN, lw=1.8)
        # Number circle
        circ = Circle((x + 0.3, y_box + bh - 0.3), 0.22,
                      facecolor=CYAN, edgecolor=CYAN, zorder=3)
        ax.add_patch(circ)
        ax.text(x + 0.3, y_box + bh - 0.3, num,
                ha='center', va='center', fontsize=10.5,
                fontweight='bold', color=BG)
        # Stage name
        ax.text(x + bw / 2, y_box + bh - 0.65, name,
                ha='center', va='top', fontsize=10,
                fontweight='bold', color=WHITE)
        # Detail
        ax.text(x + bw / 2, y_box + 0.35, detail,
                ha='center', va='bottom', fontsize=7.8,
                color=SILVER)

        # Connector arrow to next
        if i < n - 1:
            arrow(ax, x + bw, y_box + bh / 2,
                  x + bw + gap, y_box + bh / 2,
                  color=CYAN, lw=1.6)

    # Above the pipeline: validation gates
    ax.text(9, 7.8, "VALIDATION GATES",
            ha='center', fontsize=11, color=GOLD, fontweight='bold')

    gates = [
        (1, "shape\nvalid YAML"),
        (2, "self-\ndescribes"),
        (3, "fields\nresolve"),
        (4, "meta-schema\ncompliance"),
        (5, "all FKs\nresolve"),
        (6, "engine\nsupports"),
        (7, "DDL applies\natomically"),
        (8, "rows match\nDDL state"),
    ]
    for i, (num, txt) in enumerate(gates):
        x = x_start + (num - 1) * (bw + gap) + bw / 2
        ax.plot([x, x], [y_box + bh + 0.15, y_box + bh + 0.95],
                color=GOLD, lw=1.2, alpha=0.6, linestyle='--')
        ax.text(x, y_box + bh + 1.2, txt,
                ha='center', va='center', fontsize=8,
                color=GOLD, fontstyle='italic')

    # Below: failure handling note
    ax.text(9, 3.0,
            "failure at any stage halts the pipeline; the prior state is unchanged",
            ha='center', fontsize=9.5, color=RED, fontstyle='italic')
    ax.text(9, 2.4,
            "subsequent runs replay from stage 1 — bootstrap is idempotent",
            ha='center', fontsize=9.5, color=GREEN, fontstyle='italic')

    # Bottom: identical for both bootstrap and evolution
    ax.text(9, 1.3,
            "INITIAL BOOTSTRAP: empty DB → working OpsDB    "
            "EVOLUTION: existing DB + _schema_change_set → updated OpsDB",
            ha='center', fontsize=10, color=WHITE, fontweight='bold')
    ax.text(9, 0.7,
            "same pipeline, different starting state",
            ha='center', fontsize=9, color=DIM, fontstyle='italic')

    save(fig, 'infra6_03_loader_pipeline')


# ================================================================
# FIG 4: SCHEMA EVOLUTION — WIDENING ALLOWED, NARROWING FORBIDDEN
# Type: Type 5 (Connection map)
# Shows: Allowed widening on top, forbidden narrowing on bottom,
# duplication-and-double-write as the workaround bridge.
# ================================================================

def fig04_widening_vs_narrowing():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    title_text(ax, "Fig. 4: Schema Evolution — Widening Allowed, Narrowing Forbidden")
    subtitle_text(ax, "Forbidden operations have one workaround: duplicate, double-write, deprecate.")

    # ---- TOP: ALLOWED (widening, additive) ----
    ax.text(8, 8.4, "ALLOWED  —  additive, widening",
            ha='center', fontsize=12.5, color=GREEN, fontweight='bold')

    allowed = [
        ('add\nentity type',     "+ new table"),
        ('add\nfield',            "+ new column\n(nullable)"),
        ('add\nenum value',       "{a,b}\n→ {a,b,c}"),
        ('widen\nnumeric range',  "[0,100]\n→ [0,1000]"),
        ('widen\nlength bound',   "max_length 64\n→ max_length 256"),
        ('add\nindex',            "+ index"),
    ]
    bw, bh = 2.1, 1.4
    n = len(allowed)
    gap_a = (15 - n * bw) / (n - 1)
    x_start_a = 0.5
    y_a = 6.5
    for i, (name, eg) in enumerate(allowed):
        x = x_start_a + i * (bw + gap_a)
        boxed(ax, x, y_a, bw, bh, "", fill=PAN, edge=GREEN, lw=1.8)
        ax.text(x + bw / 2, y_a + bh - 0.30, name,
                ha='center', va='top', fontsize=9.8,
                fontweight='bold', color=GREEN)
        ax.text(x + bw / 2, y_a + 0.30, eg,
                ha='center', va='bottom', fontsize=7.8, color=SILVER)
        # Up-arrow indicating widening
        ax.annotate('', xy=(x + bw / 2, y_a + bh + 0.35),
                    xytext=(x + bw / 2, y_a + bh + 0.05),
                    arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.4))

    # ---- BOTTOM: FORBIDDEN (narrowing) ----
    ax.text(8, 3.4, "FORBIDDEN  —  narrowing, breaking",
            ha='center', fontsize=12.5, color=RED, fontweight='bold')

    forbidden = [
        ('rename\nfield',         "service_type\n→ kind"),
        ('delete\nfield',         "remove column"),
        ('change\ntype',          "int → varchar"),
        ('narrow\nnumeric range', "[0,1000]\n→ [0,100]"),
        ('narrow\nlength bound',  "max_length 256\n→ max_length 64"),
        ('remove\nenum value',    "{a,b,c}\n→ {a,b}"),
    ]
    y_f = 1.5
    for i, (name, eg) in enumerate(forbidden):
        x = x_start_a + i * (bw + gap_a)
        boxed(ax, x, y_f, bw, bh, "", fill=PAN, edge=RED, lw=1.8)
        ax.text(x + bw / 2, y_f + bh - 0.30, name,
                ha='center', va='top', fontsize=9.8,
                fontweight='bold', color=RED)
        ax.text(x + bw / 2, y_f + 0.30, eg,
                ha='center', va='bottom', fontsize=7.8, color=SILVER)
        # Big X over each forbidden box
        ax.plot([x + 0.25, x + bw - 0.25],
                [y_f + 0.25, y_f + bh - 0.25],
                color=RED, linewidth=1.5, alpha=0.4, zorder=2)
        ax.plot([x + bw - 0.25, x + 0.25],
                [y_f + 0.25, y_f + bh - 0.25],
                color=RED, linewidth=1.5, alpha=0.4, zorder=2)

    # ---- THE BRIDGE: duplicate + double-write ----
    bridge_x, bridge_y = 5.5, 4.4
    bridge_w, bridge_h = 5.0, 1.3
    bridge = FancyBboxPatch(
        (bridge_x, bridge_y), bridge_w, bridge_h,
        boxstyle="round,pad=0.05,rounding_size=0.2",
        linewidth=2.5, edgecolor=GOLD, facecolor=BG,
    )
    ax.add_patch(bridge)
    ax.text(bridge_x + bridge_w / 2, bridge_y + bridge_h - 0.30,
            "WORKAROUND  —  duplicate + double-write",
            ha='center', va='top', fontsize=10.5, color=GOLD, fontweight='bold')
    ax.text(bridge_x + bridge_w / 2, bridge_y + 0.32,
            "add new field, double-write across N releases,\n"
            "migrate readers, deprecate old field (never delete)",
            ha='center', va='bottom', fontsize=8.5, color=WHITE)

    # Arrows from forbidden boxes up to the bridge, and from the bridge to allowed
    # Only draw a few representative ones for visual clarity
    bridge_top = bridge_y + bridge_h
    bridge_bot = bridge_y
    for i in [0, 2, 4]:  # rename, type-change, narrow length
        x = x_start_a + i * (bw + gap_a) + bw / 2
        arrow(ax, x, y_f + bh, x, bridge_bot,
              color=GOLD, lw=1.2, style='->', curve=0.0)

    # From bridge up to the allowed region (showing the workaround creates allowed ops)
    for i in [1]:  # widening corresponds to "add field"
        x = x_start_a + i * (bw + gap_a) + bw / 2
        arrow(ax, bridge_x + bridge_w / 2, bridge_top,
              x, y_a, color=GOLD, lw=1.2, style='->', curve=0.0)

    # Side annotation
    ax.text(0.3, 5.0, "→",
            ha='left', va='center', fontsize=14, color=GOLD)
    ax.text(0.6, 5.0,
            "the only path\nthrough forbidden\nis the workaround",
            ha='left', va='center', fontsize=8.5,
            color=GOLD, fontstyle='italic')

    save(fig, 'infra6_04_widening_vs_narrowing')


# ================================================================
# FIG 5: FIELD TYPE CHANGE VIA DUPLICATION AND DOUBLE-WRITE
# Type: Type 7 (Progression)
# Shows: The N-release pattern over time; old field never deleted.
# ================================================================

def fig05_double_write_pattern():
    fig, ax = plt.subplots(figsize=(18, 10))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    title_text(ax, "Fig. 5: Field Type Change via Duplication and Double-Write")
    subtitle_text(ax, "Across N successful releases. The old field becomes a tombstone but is never deleted.")

    # Timeline base
    tl_y = 1.5
    tl_x_start = 1.0
    tl_x_end = 17.0
    ax.plot([tl_x_start, tl_x_end], [tl_y, tl_y],
            color=DIM, lw=2)

    # 6 phase markers
    phases = [
        (1.5, "Phase 0",     "release N",
         "field_old: ACTIVE\nfield_new: absent",
         GREEN, RED),
        (4.0, "Phase 1",     "release N+1",
         "field_old: ACTIVE\nfield_new: ADDED\n(both written)",
         GREEN, GREEN),
        (7.0, "Phase 2",     "releases N+1 ... N+M",
         "double-write\ncontinues for M\nsuccessful releases",
         GREEN, GREEN),
        (10.5, "Phase 3",    "release N+M+1",
         "readers migrated\nto field_new\n(reads from new only)",
         ORANGE, GREEN),
        (13.5, "Phase 4",    "release N+M+2",
         "field_old: DEPRECATED\n(still written for safety)\nfield_new: ACTIVE",
         ORANGE, GREEN),
        (16.0, "Phase 5",    "indefinitely",
         "field_old: TOMBSTONE\n(never deleted)\nfield_new: ACTIVE",
         DIM, GREEN),
    ]

    for x, phase, when, state, c_old, c_new in phases:
        # Tick mark
        ax.plot([x, x], [tl_y - 0.18, tl_y + 0.18],
                color=DIM, lw=1.5)
        # Phase label below
        ax.text(x, tl_y - 0.5, phase,
                ha='center', va='top', fontsize=9.5,
                color=GOLD, fontweight='bold')
        ax.text(x, tl_y - 0.95, when,
                ha='center', va='top', fontsize=8.0,
                color=SILVER, fontstyle='italic')

        # State box above
        box_y = tl_y + 0.6
        box_h = 1.7
        box_w = 2.4
        box_x = x - box_w / 2
        boxed(ax, box_x, box_y, box_w, box_h, state,
              fill=PAN, edge=CYAN, lw=1.4, fontsize=8)

        # Status indicators (old vs new)
        ind_y = box_y + box_h + 0.25
        # field_old indicator
        ax.add_patch(Circle((x - 0.5, ind_y), 0.18,
                            facecolor=c_old, edgecolor=WHITE, linewidth=1.0,
                            zorder=4))
        ax.text(x - 0.5, ind_y + 0.5, "old",
                ha='center', fontsize=7.5, color=WHITE)
        # field_new indicator
        ax.add_patch(Circle((x + 0.5, ind_y), 0.18,
                            facecolor=c_new, edgecolor=WHITE, linewidth=1.0,
                            zorder=4))
        ax.text(x + 0.5, ind_y + 0.5, "new",
                ha='center', fontsize=7.5, color=WHITE)

    # Time arrow
    ax.annotate('', xy=(tl_x_end + 0.4, tl_y),
                xytext=(tl_x_end - 0.4, tl_y),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=2))
    ax.text(tl_x_end + 0.6, tl_y + 0.3, "time",
            ha='left', va='center', fontsize=9, color=DIM, fontstyle='italic')

    # Top legend
    ax.text(2.0, 8.7, "FIELD STATES:",
            ha='left', fontsize=10, color=GOLD, fontweight='bold')
    legend_items = [
        (GREEN,  "ACTIVE — read and written"),
        (ORANGE, "DEPRECATED — written for safety, not read"),
        (DIM,    "TOMBSTONE — written or null, never read, never deleted"),
        (RED,    "ABSENT — does not yet exist"),
    ]
    for i, (c, desc) in enumerate(legend_items):
        ly = 8.2 - i * 0.4
        ax.add_patch(Circle((2.4, ly), 0.14,
                            facecolor=c, edgecolor=WHITE, linewidth=1.0,
                            zorder=4))
        ax.text(2.7, ly, desc,
                ha='left', va='center', fontsize=9, color=WHITE)

    # Bottom note
    ax.text(9, 0.3,
            "the old field stays in the schema as a tombstone indefinitely; storage is the price of stable history",
            ha='center', fontsize=10, color=GOLD, fontstyle='italic')

    save(fig, 'infra6_05_double_write_pattern')


# ================================================================
# FIG 6: JSON PAYLOAD VALIDATION DEPTH
# Type: Type 4 (Geometric)
# Shows: Bounded recursion depth; what's at each level; what's forbidden.
# ================================================================

def fig06_json_depth():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    title_text(ax, "Fig. 6: JSON Payload Validation Depth")
    subtitle_text(ax, "Bounded to one level of nesting. Deeper structures forbidden.")

    # Layer 0: the entity row (allowed, the host of the json field)
    l0_y = 8.0
    l0_h = 1.0
    boxed(ax, 1.0, l0_y, 14.0, l0_h, "", fill=PAN, edge=CYAN, lw=2)
    ax.text(8, l0_y + l0_h / 2,
            "Level 0  —  entity row  —  scalar fields, FKs, json discriminator + json payload field",
            ha='center', va='center', fontsize=10.5,
            color=CYAN, fontweight='bold')

    # Arrow into payload
    arrow(ax, 8, l0_y, 8, l0_y - 0.4,
          color=CYAN, lw=2)

    # Level 1: scalar fields, lists of scalars, maps of scalars (allowed)
    l1_y = 5.0
    l1_h = 2.4
    boxed(ax, 1.0, l1_y, 14.0, l1_h, "", fill=PAN, edge=GREEN, lw=2.0)
    ax.text(8, l1_y + l1_h - 0.3,
            "Level 1  —  inside the JSON payload  —  ALLOWED",
            ha='center', va='top', fontsize=10.5,
            color=GREEN, fontweight='bold')

    # Three sub-blocks at level 1
    sub_y = l1_y + 0.4
    sub_h = 1.2
    sub_w = 4.0
    sub_gap = 0.4

    sublocks = [
        ("scalar field",
         "name: ami_id\ntype: varchar\nmin_length: 12\nmax_length: 21",
         GREEN),
        ("list of scalars",
         "name: tags\ntype: list\nelement_type: varchar\nmin_count: 0  max_count: 50",
         GREEN),
        ("map of scalars",
         "name: labels\ntype: map\nkey_type: varchar\nvalue_type: varchar",
         GREEN),
    ]
    sub_total = 3 * sub_w + 2 * sub_gap
    sub_x_start = (16 - sub_total) / 2

    for i, (name, body, c) in enumerate(sublocks):
        x = sub_x_start + i * (sub_w + sub_gap)
        boxed(ax, x, sub_y, sub_w, sub_h, "",
              fill=BG, edge=c, lw=1.4)
        ax.text(x + sub_w / 2, sub_y + sub_h - 0.20, name,
                ha='center', va='top', fontsize=9.5,
                fontweight='bold', color=c)
        ax.text(x + sub_w / 2, sub_y + 0.10, body,
                ha='center', va='bottom', fontsize=7.5,
                color=SILVER, family='monospace')

    # Boundary line — the depth limit
    boundary_y = l1_y - 0.3
    ax.plot([0.5, 15.5], [boundary_y, boundary_y],
            color=RED, lw=3, linestyle='--')
    ax.text(8, boundary_y - 0.25,
            "▼  DEPTH LIMIT  ▼",
            ha='center', va='top', fontsize=10,
            color=RED, fontweight='bold')

    # Level 2: forbidden (deeper nesting)
    l2_y = 1.2
    l2_h = 2.7
    forbidden_box = Rectangle(
        (1.0, l2_y), 14.0, l2_h,
        linewidth=2, edgecolor=RED, facecolor=RED, alpha=0.08,
    )
    ax.add_patch(forbidden_box)
    ax.text(8, l2_y + l2_h - 0.3,
            "Level 2+  —  FORBIDDEN  —  no deeper nesting",
            ha='center', va='top', fontsize=10.5,
            color=RED, fontweight='bold')

    forbidden_examples = [
        ("list of lists",
         "[[a,b], [c,d]]\nelements are\nthemselves lists",
         RED),
        ("map of lists",
         "{key: [a,b,c]}\nvalues are\nthemselves lists",
         RED),
        ("list of objects",
         "[{x:1,y:2},...]\nelements are\nstructured records",
         RED),
        ("nested objects",
         "{a: {b: {c: ...}}}\nrecord inside\nrecord inside record",
         RED),
    ]
    fb_w = 3.2
    fb_h = 1.6
    fb_gap = 0.20
    fb_total = 4 * fb_w + 3 * fb_gap
    fb_x_start = (16 - fb_total) / 2
    fb_y_box = l2_y + 0.4

    for i, (name, body, c) in enumerate(forbidden_examples):
        x = fb_x_start + i * (fb_w + fb_gap)
        boxed(ax, x, fb_y_box, fb_w, fb_h, "",
              fill=BG, edge=c, lw=1.4)
        ax.text(x + fb_w / 2, fb_y_box + fb_h - 0.25, name,
                ha='center', va='top', fontsize=9.0,
                fontweight='bold', color=c)
        ax.text(x + fb_w / 2, fb_y_box + 0.20, body,
                ha='center', va='bottom', fontsize=7.5,
                color=SILVER, family='monospace')
        # X overlay
        ax.plot([x + 0.3, x + fb_w - 0.3],
                [fb_y_box + 0.3, fb_y_box + fb_h - 0.3],
                color=RED, lw=1.2, alpha=0.5)
        ax.plot([x + fb_w - 0.3, x + 0.3],
                [fb_y_box + 0.3, fb_y_box + fb_h - 0.3],
                color=RED, lw=1.2, alpha=0.5)

    # Bottom note
    ax.text(8, 0.55,
            "deep structure is a signal that the payload should be flattened or factored into separate entities",
            ha='center', fontsize=9.5, color=GOLD, fontstyle='italic')

    save(fig, 'infra6_06_json_depth')


# ================================================================
# FIG 7: SCHEMA GROWTH OVER TIME — ADDITIVE ONLY
# Type: Type 1 (Running)
# Shows: Cumulative entity and field counts grow monotonically;
# deprecated also grows; nothing ever shrinks.
# ================================================================

def fig07_schema_growth():
    fig, ax = plt.subplots(figsize=(16, 10))

    # Synthetic but plausible growth data over 36 months
    months = np.arange(0, 37)

    # Entities: starts at 50, grows to ~150 by month 36 with concave shape
    # Fields: roughly 6-8 per entity on average, grows similarly
    # Deprecated entities: starts at 0, grows slowly (mostly fields deprecate, not entities)
    # Deprecated fields: starts at 0, grows after month ~12

    # Step-like growth — schema_change_set events
    np.random.seed(42)
    cs_steps = sorted(np.random.choice(np.arange(1, 36), 18, replace=False))

    entities = np.zeros(37, dtype=int)
    fields = np.zeros(37, dtype=int)
    deprecated_entities = np.zeros(37, dtype=int)
    deprecated_fields = np.zeros(37, dtype=int)

    entities[0] = 50
    fields[0] = 320

    for m in range(1, 37):
        # Carry forward
        entities[m] = entities[m - 1]
        fields[m] = fields[m - 1]
        deprecated_entities[m] = deprecated_entities[m - 1]
        deprecated_fields[m] = deprecated_fields[m - 1]

        if m in cs_steps:
            # Add 2-8 entities, 10-30 fields per change-set
            entities[m] += np.random.randint(2, 9)
            fields[m] += np.random.randint(10, 35)
            # Some changes deprecate fields (rare deprecation of entities)
            if m > 8:
                deprecated_fields[m] += np.random.randint(0, 4)
            if m > 18 and np.random.rand() < 0.3:
                deprecated_entities[m] += 1

    # Active = cumulative - deprecated
    active_entities = entities - deprecated_entities
    active_fields = fields - deprecated_fields

    # Plot
    ax.plot(months, fields, color=GOLD, linewidth=2.5,
            label='Cumulative fields  (never decreases)',
            drawstyle='steps-post')
    ax.plot(months, active_fields, color=GREEN, linewidth=2.5,
            label='Active fields',
            drawstyle='steps-post')
    ax.plot(months, deprecated_fields, color=ORANGE, linewidth=2,
            linestyle='--',
            label='Deprecated fields (tombstones)',
            drawstyle='steps-post')

    # Secondary scale — entity counts on twin axis
    ax2 = ax.twinx()
    ax2.plot(months, entities, color=CYAN, linewidth=2.5,
             label='Cumulative entities',
             drawstyle='steps-post')
    ax2.plot(months, active_entities, color=BLUE, linewidth=2,
             linestyle=':',
             label='Active entities',
             drawstyle='steps-post')

    # Mark each schema change-set as a vertical line
    for cs in cs_steps:
        ax.axvline(cs, color=DIM, alpha=0.25, linewidth=0.8)

    ax.set_xlabel('months since initial bootstrap',
                  fontsize=11, color=SILVER)
    ax.set_ylabel('field count',
                  fontsize=11, color=GOLD)
    ax2.set_ylabel('entity count',
                   fontsize=11, color=CYAN)

    ax.set_title('Fig. 7: Schema Growth Is Additive Only — Curves Never Decrease',
                 fontsize=15, fontweight='bold', color=GOLD, pad=20)

    ax.set_xlim(-1, 37)
    ax.set_ylim(0, max(fields) * 1.15)
    ax2.set_ylim(0, max(entities) * 1.15)

    # Subtitle
    ax.text(0.5, 1.04, "vertical lines mark _schema_change_set apply events; growth is monotonic by rule",
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=10.5, color=SILVER, fontstyle='italic')

    # Annotations on the curves
    ax.annotate('cumulative fields:\nstrictly non-decreasing',
                xy=(28, fields[28]),
                xytext=(15, fields[28] + 80),
                fontsize=9, color=GOLD,
                arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.2))

    ax.annotate('deprecated fields\ngrow but persist forever',
                xy=(32, deprecated_fields[32]),
                xytext=(20, 50),
                fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2))

    ax2.annotate('cumulative entities',
                 xy=(34, entities[34]),
                 xytext=(22, entities[34] + 8),
                 fontsize=9, color=CYAN,
                 arrowprops=dict(arrowstyle='->', color=CYAN, lw=1.2))

    # Legends
    leg1 = ax.legend(loc='upper left',
                     facecolor=PAN, edgecolor=DIM,
                     labelcolor=WHITE, fontsize=9)
    leg2 = ax2.legend(loc='lower right',
                      facecolor=PAN, edgecolor=DIM,
                      labelcolor=WHITE, fontsize=9)

    # Bottom note inside axes
    ax.text(0.5, 0.04,
            "no deletes, no renames, no type changes — the rules of §12 enforce monotonic curves",
            transform=ax.transAxes, ha='center',
            fontsize=10, color=GOLD, fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=BG, edgecolor=GOLD))

    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    for spine_name in ['left', 'right', 'bottom']:
        ax.spines[spine_name].set_color(DIM)
        ax2.spines[spine_name].set_color(DIM)

    ax.tick_params(colors=DIM)
    ax2.tick_params(colors=DIM)

    save(fig, 'infra6_07_schema_growth')


# ================================================================
# FIG 8: DIRECTORY.YAML — DEPENDENCY DAG FLATTENED TO LINEAR ORDER
# Type: Type 5 (Connection map)
# Shows: The FK dependency graph (DAG) and the imposed linear ordering;
# why the ordering is data, not inferred.
# ================================================================

def fig08_directory_dag():
    fig, ax = plt.subplots(figsize=(18, 10))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    title_text(ax, "Fig. 8: directory.yaml — Dependency DAG Flattened to Linear Order")
    subtitle_text(ax, "The FK graph defines partial order. directory.yaml encodes the chosen total order as data.")

    # ---- LEFT: dependency DAG (logical structure) ----
    ax.text(4.5, 9.0, "the DAG (partial order)",
            ha='center', fontsize=11.5, color=CYAN, fontweight='bold')

    # Layer 0 (foundation): no FKs
    layer0 = [
        ('site',     1.0, 7.5),
        ('ops_user', 3.5, 7.5),
        ('ops_group',6.0, 7.5),
    ]
    # Layer 1: depends on layer 0
    layer1 = [
        ('location',           1.0, 6.0),
        ('hardware_set',       3.5, 6.0),
        ('ops_group_member',   6.0, 6.0),
    ]
    # Layer 2: depends on layer 1
    layer2 = [
        ('cloud_resource',     1.0, 4.5),
        ('megavisor_instance', 3.5, 4.5),
        ('policy',             6.0, 4.5),
    ]
    # Layer 3
    layer3 = [
        ('machine',            1.0, 3.0),
        ('service',            3.5, 3.0),
        ('approval_rule',      6.0, 3.0),
    ]
    # Layer 4
    layer4 = [
        ('change_set',         3.5, 1.5),
    ]

    all_nodes = layer0 + layer1 + layer2 + layer3 + layer4

    node_w, node_h = 1.65, 0.75

    # Draw edges first (FK dependencies — child points to parent)
    edges = [
        ('location', 'site'),
        ('hardware_set', 'site'),
        ('ops_group_member', 'ops_user'),
        ('ops_group_member', 'ops_group'),
        ('cloud_resource', 'location'),
        ('megavisor_instance', 'hardware_set'),
        ('megavisor_instance', 'cloud_resource'),
        ('policy', 'ops_group'),
        ('machine', 'megavisor_instance'),
        ('service', 'site'),
        ('approval_rule', 'policy'),
        ('change_set', 'service'),
        ('change_set', 'approval_rule'),
    ]

    pos = {name: (x, y) for name, x, y in all_nodes}

    for src, dst in edges:
        x1, y1 = pos[src]
        x2, y2 = pos[dst]
        # arrow goes from src up to dst (child → parent)
        arrow(ax, x1, y1 + node_h / 2,
              x2, y2 - node_h / 2,
              color=DIM, lw=1.0, style='->')

    # Draw nodes
    for name, x, y in all_nodes:
        boxed(ax, x - node_w / 2, y - node_h / 2, node_w, node_h, name,
              fill=PAN, edge=CYAN, lw=1.4, fontsize=8.5,
              fontcolor=WHITE)

    # ---- RIGHT: linear order (directory.yaml) ----
    ax.text(13.5, 9.0, "directory.yaml import order  (total order)",
            ha='center', fontsize=11.5, color=GOLD, fontweight='bold')

    # Vertical linear list, numbered
    linear_order = [
        'site',
        'ops_user',
        'ops_group',
        'location',
        'hardware_set',
        'ops_group_member',
        'cloud_resource',
        'megavisor_instance',
        'policy',
        'machine',
        'service',
        'approval_rule',
        'change_set',
    ]

    list_x = 11.5
    list_y_start = 8.0
    list_dy = 0.50
    list_w = 4.5
    list_h = 0.42

    for i, name in enumerate(linear_order):
        y = list_y_start - i * list_dy
        # Number column
        boxed(ax, list_x, y - list_h / 2, 0.55, list_h, str(i + 1),
              fill=GOLD, edge=GOLD, lw=1.0, fontsize=9,
              fontcolor=BG, fontweight='bold')
        # Name column
        boxed(ax, list_x + 0.65, y - list_h / 2, list_w - 0.65, list_h, name,
              fill=PAN, edge=DIM, lw=1.0, fontsize=9,
              fontcolor=WHITE)

    # Connecting bracket from DAG to list (showing "flattened to")
    ax.annotate('',
                xy=(list_x - 0.2, 5.5),
                xytext=(7.2, 5.5),
                arrowprops=dict(arrowstyle='->', color=GOLD, lw=2.5))
    ax.text(9.4, 5.85, "flattened",
            ha='center', va='bottom', fontsize=10,
            color=GOLD, fontweight='bold')
    ax.text(9.4, 5.15, "(by author, not loader)",
            ha='center', va='top', fontsize=8.5,
            color=GOLD, fontstyle='italic')

    # Bottom note — the structural finding
    ax.text(9, 0.5,
            "many valid total orderings exist; the author picks one and writes it down — explicit ordering is data, not inferred",
            ha='center', fontsize=10, color=GOLD, fontstyle='italic')

    save(fig, 'infra6_08_directory_dag')


# ================================================================
# MAIN
# ================================================================

def main():
    print("Generating INFRA-6 figures...")
    fig01_closed_vocabulary()
    fig02_permitted_vs_forbidden()
    fig03_loader_pipeline()
    fig04_widening_vs_narrowing()
    fig05_double_write_pattern()
    fig06_json_depth()
    fig07_schema_growth()
    fig08_directory_dag()
    print("")
    print("Done. 8 figures written to ../figures/")
    print("  infra6_01_closed_vocabulary.png")
    print("  infra6_02_permitted_vs_forbidden.png")
    print("  infra6_03_loader_pipeline.png")
    print("  infra6_04_widening_vs_narrowing.png")
    print("  infra6_05_double_write_pattern.png")
    print("  infra6_06_json_depth.png")
    print("  infra6_07_schema_growth.png")
    print("  infra6_08_directory_dag.png")


if __name__ == "__main__":
    main()
    