"""Render concept-level blueprint drawings as SVG.

Each drawing is a left-to-right flow of columns with a governance band and an
engineering-style title block. Run: python3 tools/blueprint.py
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape

W = 1200
BG = "#0b3768"
GRID_MINOR = "#164a82"
GRID_MAJOR = "#1f5a99"
INK = "#e8f1ff"
INK_DIM = "#9fc3ef"
ACCENT = "#ffd36b"
FONT = "'JetBrains Mono','DejaVu Sans Mono',Consolas,monospace"


@dataclass
class Blueprint:
    number: str
    slug: str
    title: str
    period: str
    columns: list[tuple[str, list[str]]]
    band: str
    notes: list[str] = field(default_factory=list)


def _grid(H: int) -> str:
    parts = []
    for x in range(0, W + 1, 20):
        c = GRID_MAJOR if x % 100 == 0 else GRID_MINOR
        parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{c}" stroke-width="1"/>')
    for y in range(0, H + 1, 20):
        c = GRID_MAJOR if y % 100 == 0 else GRID_MINOR
        parts.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{c}" stroke-width="1"/>')
    return "\n".join(parts)


def _text(x, y, s, size=14, anchor="start", fill=INK, weight="normal", spacing=0):
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-weight="{weight}" letter-spacing="{spacing}">{escape(s)}</text>'
    )


def _wrap(label: str, width: int) -> list[str]:
    words, lines, cur = label.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def render(bp: Blueprint) -> str:
    n = len(bp.columns)
    left, right, top = 48, W - 48, 128
    gap = 34
    col_w = (right - left - gap * (n - 1)) / n
    box_h, box_gap = 58, 14
    max_rows = max(len(items) for _, items in bp.columns)
    col_bottom = top + 34 + max_rows * (box_h + box_gap)
    band_y = col_bottom + 22
    tb_w, tb_h = 470, 96
    H = band_y + 34 + 26 + tb_h + 24

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="{escape(bp.title)} blueprint">',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        _grid(H),
        f'<rect x="16" y="16" width="{W - 32}" height="{H - 32}" fill="none" stroke="{INK}" stroke-width="2"/>',
        f'<rect x="24" y="24" width="{W - 48}" height="{H - 48}" fill="none" stroke="{INK_DIM}" stroke-width="1"/>',
        _text(48, 66, bp.title.upper(), 24, weight="bold", spacing=1),
        _text(48, 92, bp.period, 14, fill=INK_DIM),
    ]
    centers: list[float] = []

    for i, (head, items) in enumerate(bp.columns):
        x = left + i * (col_w + gap)
        out.append(
            f'<rect x="{x:.1f}" y="{top}" width="{col_w:.1f}" height="{col_bottom - top + 6}" '
            f'fill="none" stroke="{INK_DIM}" stroke-width="1" stroke-dasharray="6 4"/>'
        )
        out.append(_text(x + col_w / 2, top + 22, head.upper(), 12, "middle", ACCENT, "bold", 1))
        y0 = top + 34
        rows = len(items)
        offset = (max_rows - rows) * (box_h + box_gap) / 2
        for j, item in enumerate(items):
            y = y0 + offset + j * (box_h + box_gap)
            out.append(
                f'<rect x="{x + 10:.1f}" y="{y:.1f}" width="{col_w - 20:.1f}" height="{box_h}" '
                f'fill="{BG}" stroke="{INK}" stroke-width="1.6"/>'
            )
            lines = _wrap(item, int((col_w - 30) / 8))
            ly = y + box_h / 2 - (len(lines) - 1) * 8 + 5
            for k, line in enumerate(lines):
                out.append(_text(x + col_w / 2, ly + k * 16, line, 13, "middle"))
        centers.append(x + col_w)

    mid_y = top + 34 + max_rows * (box_h + box_gap) / 2 - box_gap / 2
    for i in range(n - 1):
        x1, x2 = centers[i] + 2, centers[i] + gap - 2
        out.append(f'<line x1="{x1:.1f}" y1="{mid_y:.1f}" x2="{x2 - 8:.1f}" y2="{mid_y:.1f}" stroke="{ACCENT}" stroke-width="2.5"/>')
        out.append(
            f'<polygon points="{x2:.1f},{mid_y:.1f} {x2 - 10:.1f},{mid_y - 6:.1f} {x2 - 10:.1f},{mid_y + 6:.1f}" fill="{ACCENT}"/>'
        )

    out.append(
        f'<rect x="{left}" y="{band_y}" width="{right - left}" height="34" fill="none" stroke="{INK}" stroke-width="1.6"/>'
    )
    out.append(_text(W / 2, band_y + 22, bp.band, 13, "middle", INK, "bold", 1))

    # title block
    tbx, tby = W - 24 - tb_w, H - 24 - tb_h
    out.append(f'<rect x="{tbx}" y="{tby}" width="{tb_w}" height="{tb_h}" fill="{BG}" stroke="{INK}" stroke-width="1.6"/>')
    out.append(f'<line x1="{tbx}" y1="{tby + 32}" x2="{tbx + tb_w}" y2="{tby + 32}" stroke="{INK}" stroke-width="1"/>')
    out.append(f'<line x1="{tbx}" y1="{tby + 64}" x2="{tbx + tb_w}" y2="{tby + 64}" stroke="{INK}" stroke-width="1"/>')
    out.append(f'<line x1="{tbx + 150}" y1="{tby}" x2="{tbx + 150}" y2="{tby + 64}" stroke="{INK}" stroke-width="1"/>')
    out.append(_text(tbx + 10, tby + 21, f"DWG {bp.number}", 12, fill=INK_DIM))
    out.append(_text(tbx + 160, tby + 21, "CONCEPT LEVEL / SIMPLIFIED", 12, fill=INK_DIM))
    out.append(_text(tbx + 10, tby + 53, "DESIGN", 12, fill=INK_DIM))
    out.append(_text(tbx + 160, tby + 53, "P. GALLO", 12, fill=INK_DIM))
    out.append(_text(tbx + tb_w / 2, tby + 86, "CONFIDENTIAL / PROPRIETARY / NOT PUBLIC", 13, "middle", ACCENT, "bold", 1))

    ny = H - 24 - tb_h + 16
    for k, note in enumerate(bp.notes):
        out.append(_text(48, ny + k * 20, f"NOTE {k + 1}: {note}", 12, fill=INK_DIM))

    out.append("</svg>")
    return "\n".join(out)


@dataclass
class CycleBlueprint:
    """A continuous loop of stages around a central hub, fed by external inputs."""

    number: str
    slug: str
    title: str
    period: str
    stages: list[tuple[str, list[str]]]
    hub: list[str]
    inputs: list[str]
    band: str
    notes: list[str] = field(default_factory=list)


def _clip_to_box(cx, cy, tx, ty, hw, hh):
    """Point where the segment from box centre (cx, cy) towards (tx, ty) leaves the box."""
    dx, dy = tx - cx, ty - cy
    sx = hw / abs(dx) if dx else float("inf")
    sy = hh / abs(dy) if dy else float("inf")
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s


def _arrow(x1, y1, x2, y2, color=ACCENT, width=2.5, curve=0.0):
    import math

    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 11 * math.cos(ang), y2 - 11 * math.sin(ang)
    mx, my = (x1 + hx) / 2, (y1 + hy) / 2
    nx, ny = -(hy - y1), hx - x1
    cx, cy = mx + nx * curve, my + ny * curve
    left = (x2 - 11 * math.cos(ang - 0.45), y2 - 11 * math.sin(ang - 0.45))
    right = (x2 - 11 * math.cos(ang + 0.45), y2 - 11 * math.sin(ang + 0.45))
    return (
        f'<path d="M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {hx:.1f},{hy:.1f}" fill="none" '
        f'stroke="{color}" stroke-width="{width}"/>'
        f'<polygon points="{x2:.1f},{y2:.1f} {left[0]:.1f},{left[1]:.1f} {right[0]:.1f},{right[1]:.1f}" fill="{color}"/>'
    )


def render_cycle(bp: CycleBlueprint) -> str:
    import math

    H = 800
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="{escape(bp.title)} blueprint">',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        _grid(H),
        f'<rect x="16" y="16" width="{W - 32}" height="{H - 32}" fill="none" stroke="{INK}" stroke-width="2"/>',
        f'<rect x="24" y="24" width="{W - 48}" height="{H - 48}" fill="none" stroke="{INK_DIM}" stroke-width="1"/>',
        _text(48, 66, bp.title.upper(), 24, weight="bold", spacing=1),
        _text(48, 92, bp.period, 14, fill=INK_DIM),
    ]

    # inputs panel
    px, py, pw = 48, 150, 220
    ih, igap = 54, 14
    ph = 34 + len(bp.inputs) * (ih + igap)
    out.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="none" stroke="{INK_DIM}" stroke-dasharray="6 4"/>')
    out.append(_text(px + pw / 2, py + 22, "INTELLIGENCE INPUTS", 12, "middle", ACCENT, "bold", 1))
    for i, label in enumerate(bp.inputs):
        y = py + 34 + i * (ih + igap)
        out.append(f'<rect x="{px + 10}" y="{y}" width="{pw - 20}" height="{ih}" fill="{BG}" stroke="{INK}" stroke-width="1.6"/>')
        lines = _wrap(label, 22)
        ly = y + ih / 2 - (len(lines) - 1) * 8 + 5
        for k, line in enumerate(lines):
            out.append(_text(px + pw / 2, ly + k * 16, line, 13, "middle"))

    # cycle geometry
    cx, cy, rx, ry = 760, 400, 300, 205
    bw, bh = 236, 92
    n = len(bp.stages)
    pos = []
    for i in range(n):
        a = math.radians(-90 + i * 360 / n)
        pos.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))

    # dashed orbit
    out.append(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{INK_DIM}" '
        f'stroke-width="1" stroke-dasharray="3 6"/>'
    )

    # hub
    hub_r = 92
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{hub_r}" fill="{BG}" stroke="{ACCENT}" stroke-width="2"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{hub_r - 8}" fill="none" stroke="{INK_DIM}" stroke-width="1"/>')
    hy0 = cy - (len(bp.hub) - 1) * 9 + 5
    for k, line in enumerate(bp.hub):
        out.append(_text(cx, hy0 + k * 18, line, 13, "middle", INK, "bold" if k == 0 else "normal"))

    # inputs feed the cycle (short arrow into the gap below the leftmost stage)
    feed_y = py + ph - 30
    out.append(_arrow(px + pw + 4, feed_y, px + pw + 120, feed_y, ACCENT, 2.5, 0.0))
    out.append(_text(px + pw + 8, feed_y - 10, "FEEDS EVERY STAGE", 10, fill=INK_DIM, spacing=1))

    # hub spokes: every stage reads and writes the shared graph
    for x, y in pos:
        ang = math.atan2(y - cy, x - cx)
        sx, sy = cx + (hub_r + 4) * math.cos(ang), cy + (hub_r + 4) * math.sin(ang)
        ex, ey = _clip_to_box(x, y, cx, cy, bw / 2 + 4, bh / 2 + 4)
        out.append(
            f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{INK_DIM}" '
            f'stroke-width="1.2" stroke-dasharray="4 4"/>'
        )

    # arrows between stages (clockwise)
    for i in range(n):
        (x1, y1), (x2, y2) = pos[i], pos[(i + 1) % n]
        sx, sy = _clip_to_box(x1, y1, x2, y2, bw / 2 + 6, bh / 2 + 6)
        ex, ey = _clip_to_box(x2, y2, x1, y1, bw / 2 + 6, bh / 2 + 6)
        out.append(_arrow(sx, sy, ex, ey, ACCENT, 2.5, -0.18))

    # stage boxes
    for i, (name, items) in enumerate(bp.stages):
        x, y = pos[i]
        bx, by = x - bw / 2, y - bh / 2
        out.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw}" height="{bh}" fill="{BG}" stroke="{INK}" stroke-width="1.8"/>')
        out.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="34" height="{bh}" fill="{INK}" opacity="0.12"/>')
        out.append(_text(bx + 17, y + 7, str(i + 1), 20, "middle", ACCENT, "bold"))
        out.append(_text(bx + 46, by + 26, name.upper(), 14, "start", ACCENT, "bold", 1))
        for k, item in enumerate(items):
            out.append(_text(bx + 46, by + 50 + k * 19, item, 12, "start", INK))

    # band
    band_y = 640
    out.append(f'<rect x="48" y="{band_y}" width="{W - 96}" height="34" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    out.append(_text(W / 2, band_y + 22, bp.band, 13, "middle", INK, "bold", 1))

    out.append(_title_block(bp.number, H))
    for k, note in enumerate(bp.notes):
        out.append(_text(48, H - 24 - 96 + 16 + 34 + k * 20, f"NOTE {k + 1}: {note}", 12, fill=INK_DIM))
    out.append("</svg>")
    return "\n".join(out)


def _title_block(number: str, H: int) -> str:
    tb_w, tb_h = 470, 96
    tbx, tby = W - 24 - tb_w, H - 24 - tb_h
    return "\n".join([
        f'<rect x="{tbx}" y="{tby}" width="{tb_w}" height="{tb_h}" fill="{BG}" stroke="{INK}" stroke-width="1.6"/>',
        f'<line x1="{tbx}" y1="{tby + 32}" x2="{tbx + tb_w}" y2="{tby + 32}" stroke="{INK}" stroke-width="1"/>',
        f'<line x1="{tbx}" y1="{tby + 64}" x2="{tbx + tb_w}" y2="{tby + 64}" stroke="{INK}" stroke-width="1"/>',
        f'<line x1="{tbx + 150}" y1="{tby}" x2="{tbx + 150}" y2="{tby + 64}" stroke="{INK}" stroke-width="1"/>',
        _text(tbx + 10, tby + 21, f"DWG {number}", 12, fill=INK_DIM),
        _text(tbx + 160, tby + 21, "CONCEPT LEVEL / SIMPLIFIED", 12, fill=INK_DIM),
        _text(tbx + 10, tby + 53, "DESIGN", 12, fill=INK_DIM),
        _text(tbx + 160, tby + 53, "P. GALLO", 12, fill=INK_DIM),
        _text(tbx + tb_w / 2, tby + 86, "CONFIDENTIAL / PROPRIETARY / NOT PUBLIC", 13, "middle", ACCENT, "bold", 1),
    ])


BLUEPRINTS = [
    Blueprint(
        "BP-01", "decision-intelligence-platform",
        "Decision intelligence fusion platform", "2023 to present  |  product owner and architect  |  0 to 1",
        [
            ("Sources", ["Heterogeneous data sources", "Documents and reports", "Analyst input"]),
            ("Fusion", ["Entity extraction and linking", "Normalisation", "Knowledge graph"]),
            ("Reasoning", ["Multi-agent orchestration", "LLM pipelines", "GraphRAG retrieval"]),
            ("Human control", ["Confidence scoring", "Explainable results", "Human override"]),
            ("Decisions", ["Assessments and briefs", "Alerts"]),
        ],
        "AUDIT TRAIL ACROSS EVERY STAGE  |  HUMAN IN THE LOOP BY DESIGN",
        ["Production system. Code, data and deployments are not public."],
    ),
    CycleBlueprint(
        "BP-02", "threat-intelligence-ctem",
        "Cyber threat intelligence for CTEM",
        "2023 to present  |  product owner and architect  |  0 to 1",
        [
            ("Scoping", ["Business-critical assets", "Attack surface boundaries"]),
            ("Discovery", ["Assets and exposures", "Threat actors and TTPs"]),
            ("Prioritisation", ["Exploitability in context", "Business impact"]),
            ("Validation", ["Attack path analysis", "Control effectiveness"]),
            ("Mobilisation", ["Remediation workflows", "Reporting and metrics"]),
        ],
        ["THREAT AND", "EXPOSURE", "KNOWLEDGE GRAPH"],
        ["Threat intelligence feeds", "Open, deep and dark web sources", "Vulnerability and asset data", "Analyst input"],
        "CONTINUOUS THREAT EXPOSURE MANAGEMENT  |  THREAT INTELLIGENCE DRIVES EVERY STAGE",
        ["Production system. Code, data and deployments are not public."],
    ),
    Blueprint(
        "BP-03", "life-sciences-knowledge-platform",
        "Neuro-symbolic life sciences knowledge platform", "2019 to 2023  |  conceived and led  |  0 to 1, prototype to production",
        [
            ("Content", ["Scientific literature", "Clinical and regulatory documents"]),
            ("Knowledge", ["Biomedical meta-thesaurus (4M+ concepts)", "Concept linking"]),
            ("Understanding", ["Symbolic NLU", "Machine learning models"]),
            ("Graph", ["Biomedical knowledge graph", "Semantic search"]),
            ("Use", ["Drug discovery workflows", "Analyst interface"]),
        ],
        "NEURO-SYMBOLIC: SYMBOLIC PRECISION + NEURAL SCALE, GROUNDED IN STRUCTURED KNOWLEDGE",
        [
            "Production system used by large pharma organisations. Not public.",
            "Knowledge acquisition pipeline over a unified biomedical vocabulary (clinical, drug, lab terms).",
        ],
    ),
    Blueprint(
        "BP-04", "analyst-case-management",
        "Case management and semantic search for analysts", "2014 to 2018  |  product lead  |  0 to 1",
        [
            ("Inputs", ["Documents", "Case data"]),
            ("Semantics", ["Semantic analysis", "Entity extraction"]),
            ("Workspace", ["Case management", "Semantic search"]),
            ("Users", ["Analyst teams"]),
        ],
        "CASE-CENTRIC ANALYSIS WITH SEMANTIC RETRIEVAL",
        ["Production system. Not public."],
    ),
    Blueprint(
        "BP-05", "semantic-intelligence-suite",
        "Semantic intelligence suite", "2007 to 2014  |  product management  |  0 to 1",
        [
            ("Sources", ["Open and closed sources"]),
            ("Engine", ["Semantic NLU engine", "Categorisation", "Entity extraction"]),
            ("Applications", ["Semantic search", "Intelligence analysis"]),
            ("Deployment", ["Agencies and enterprises in several countries"]),
        ],
        "FLAGSHIP SEMANTIC INTELLIGENCE SUITE",
        ["Commercial product. Source and deployments are not public."],
    ),
    Blueprint(
        "BP-06", "icu-monitoring-system",
        "Intensive care monitoring system", "1996  |  independent developer  |  first product shipped to real users",
        [
            ("Bedside", ["Monitors", "Ventilators", "Infusion pumps"]),
            ("Connectivity", ["Device interfaces", "Protocol adapters"]),
            ("Real time", ["Telemonitoring", "Alarm management"]),
            ("Clinical", ["Central monitoring station"]),
        ],
        "CLINICAL MONITORING SOFTWARE FOR INTENSIVE CARE UNITS",
        ["Delivered system. Not public."],
    ),
    Blueprint(
        "BP-08", "sip-contact-center",
        "SIP voice and video contact center", "1999 to 2000 voice, 2001 video  |  design and development  |  0 to 1",
        [
            ("Callers", ["Voice callers", "Video callers", "SIP trunks"]),
            ("SIP layer", ["Registrar and proxy", "B2BUA and media relay", "SDP audio and video"]),
            ("Contact center", ["IVR with DTMF", "Skills-based ACD", "Queues and overflow"]),
            ("Agents", ["Agent states", "Desktop via CSTA", "Video-capable routing"]),
            ("Platforms", ["Open-source PBX manager interfaces", "Commercial PBX via CSTA", "CDRs and reporting"]),
        ],
        "SIP SIGNALLING  |  RTP/RTCP VOICE AND VIDEO  |  CSTA THIRD-PARTY CALL CONTROL",
        [
            "Delivered systems. Code and deployments are not public.",
            "2001: video added end to end (video IVR, video agents, audio fallback, lip sync).",
        ],
    ),
    Blueprint(
        "BP-07", "narrative-intelligence",
        "Narrative intelligence", "Architecture for tracking narratives across open sources",
        [
            ("Sources", ["News and media", "Social platforms and forums", "Messaging channels"]),
            ("Understanding", ["Multilingual NLP", "Claim and entity extraction", "Stance and sentiment"]),
            ("Narratives", ["Narrative clustering", "Narrative lineage over time", "LLM summaries"]),
            ("Propagation", ["Actors and amplifiers", "Coordinated behaviour", "Reach and velocity"]),
            ("Assessment", ["Risk scoring", "Analyst validation", "Early-warning briefs"]),
        ],
        "FROM SCATTERED CONTENT TO TRACKED NARRATIVES  |  ANALYSTS VALIDATE EVERY ASSESSMENT",
        ["Not public."],
    ),
]


def main() -> None:
    out_dir = Path(__file__).resolve().parent.parent / "blueprints"
    out_dir.mkdir(exist_ok=True)
    for old in out_dir.glob("*.svg"):
        old.unlink()
    for bp in BLUEPRINTS:
        svg = render_cycle(bp) if isinstance(bp, CycleBlueprint) else render(bp)
        (out_dir / f"{bp.number.lower()}-{bp.slug}.svg").write_text(svg, encoding="utf-8")
        print(f"wrote {bp.number} {bp.slug}")


if __name__ == "__main__":
    main()
