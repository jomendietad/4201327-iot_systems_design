#!/usr/bin/env python3
"""Figures for the session-8 deck (08_business.md).

    python3 biz_figs.py       # writes biz_*.svg here

biz_bill.svg is computed from assumed costs (US$50 per site visit, US$4 per ESP32-C6
module, a 500-node farm), not measured. The others are diagrams; biz_watchdog.svg follows
firmware/lab8_golden/src/watchdog.c.
"""
from pathlib import Path

from figlib import C, GRID, INK, MUTED, PAL, T, box, line, rect, save, text
from fleet_figs import arr, circle, fig, parr

HERE = Path(__file__).resolve().parent
PED, SCD, ASD, TH, RAID, UD, OMD, TW = (PAL[k] for k in
                                        ("PED", "SCD", "ASD", "Thread", "RAID", "UD", "OMD", "Trustworthiness"))


def lenses():
    """The six viewpoints in the standard's order, and the sessions where each led."""
    rows = [("Foundational", "gray", {0: "full"}),
            ("Business", "gray", {0: "hollow", 8: "full"}),
            ("Usage", "gray", {7: "full"}),
            ("Functional", "gray", {1: "full", 2: "full", 3: "full", 5: "full"}),
            ("Trustworthiness", TW, {4: "full", 6: "full"}),
            ("Construction", "gray", {8: "full"})]
    x0, dx, y0, dy = 250, 92, 64, 50
    body = [text(20, 30, "viewpoint, in the standard's order", 17, 700, MUTED),
            text(x0 + 4 * dx, 30, "session", 17, 700, MUTED, "middle")]
    for s in range(9):
        body.append(text(x0 + s * dx, 56, str(s), 19, 700, INK if s == 8 else MUTED, "middle"))
    body.append(rect(x0 + 8 * dx - 34, 36, 68, y0 + 6 * dy - 20, T["gray"], "none", 0, 10))
    body.append(text(x0 + 8 * dx, 56, "8", 19, 800, INK, "middle"))
    for i, (name, col, marks) in enumerate(rows):
        y = y0 + 22 + i * dy
        strong = name == "Business"
        body.append(text(20, y + 7, name, 21, 800 if strong else 600,
                         C[col] if col != "gray" else (INK if strong else MUTED)))
        body.append(line(x0 - 20, y, x0 + 8 * dx + 20, y, GRID, 1))
        mark_col = C[col] if col != "gray" else INK
        for s, kind in marks.items():
            if kind == "full":
                body.append(circle(x0 + s * dx, y, 13, mark_col))
            else:
                body.append(circle(x0 + s * dx, y, 12, "#fff", MUTED, 3))
    yb = y0 + 22 + 6 * dy + 6
    body.append(circle(30, yb, 10, INK))
    body.append(text(48, yb + 6, "the session's lens", 17, 400, INK))
    body.append(circle(250, yb, 9, "#fff", MUTED, 3))
    body.append(text(268, yb + 6, "week 1: answered before any firmware existed", 17, 400, INK))
    return fig(1040, yb + 24, body)


def chain():
    """The value path through the components the class built."""
    hops = [("reading", PED, "Lab 4"), ("CoAP", ASD, "Lab 3"), ("mesh", TH, "Lab 2"),
            ("OTBR", SCD, "Lab 5"), ("bridge", RAID, "Lab 7"), ("dashboard", UD, "Lab 7"),
            ("decision", "gray", ""), ("valve", PED, "Lab 3")]
    w, gap, y = 122, 18, 70
    body, x = [], 20
    xs = []
    for i, (name, col, lab) in enumerate(hops):
        xs.append(x)
        if name == "decision":
            body.append(rect(x, y, w, 70, "#fff", INK, 4, 10))
            body.append(text(x + w / 2, y + 41, name, 18, 800, INK, "middle"))
        elif name == "CoAP":
            body.append(box(x, y, w, 70, name, col, 18, "+ CBOR"))
        else:
            body.append(box(x, y, w, 70, name, col, 18))
        if lab:
            body.append(text(x + w / 2, y + 98, lab, 18, 400, MUTED, "middle"))
        if i < len(hops) - 1:
            body.append(arr(x + w + 1, y + 35, x + w + gap - 1, y + 35, INK, 2.5))
        x += w + gap
    dx = xs[6]
    body.append(text(dx + w / 2, 40, "value is captured here", 20, 800, INK, "middle"))
    yb = 210
    body.append(line(xs[0], yb, dx - 8, yb, MUTED, 3))
    body.append(line(xs[0], yb - 10, xs[0], yb + 10, MUTED, 3))
    body.append(line(dx - 8, yb - 10, dx - 8, yb + 10, MUTED, 3))
    body.append(text((xs[0] + dx) / 2, yb + 32, "cost: every link Gustavo pays for", 20, 700, MUTED, "middle"))
    end = xs[7] + w
    body.append(line(dx, yb, end, yb, INK, 3))
    body.append(line(dx, yb - 10, dx, yb + 10, INK, 3))
    body.append(line(end, yb - 10, end, yb + 10, INK, 3))
    body.append(text((dx + end) / 2, yb + 32, "the product", 20, 700, INK, "middle"))
    body.append(text(20, 296, "a reading nobody acts on is storage; a valve opened at the right time is water saved",
                     20, 400, MUTED))
    return fig(end + 20, 312, body)


def service():
    """What irrigation-as-a-service promises, and what was built for each promise."""
    rows = [("uptime the contract can state", "self-healing mesh, OTBR autostart, watchdog", "Labs 2, 8", SCD, False),
            ("see every node from the office", "health telemetry, bridge, dashboard", "Lab 7", OMD, False),
            ("nobody else opens the valves", "DTLS on every request", "Lab 6", TW, False),
            ("cut off means safe", "the valve fails closed", "Lab 8", PED, False),
            ("no lock-in for the farmer", "Thread and CoAP: open standards", "all labs", TH, False),
            ("fix a bug without a visit", "signed firmware update", "not built: a gap", "gray", True)]
    body = [text(20, 28, "the service promises", 18, 700, MUTED),
            text(470, 28, "what you built for it", 18, 700, MUTED),
            text(1060, 28, "where", 18, 700, MUTED, "end")]
    y = 44
    for promise, built, where, col, gap in rows:
        dash = "8 6" if gap else ""
        body.append(rect(20, y, 400, 46, "#fff" if gap else T[col], C[col], 2, 10, dash))
        body.append(text(36, y + 30, promise, 19, 700, C[col]))
        body.append(arr(424, y + 23, 462, y + 23, MUTED if gap else INK, 2.5, "6 5" if gap else ""))
        body.append(text(470, y + 30, built, 19, 400, MUTED if gap else INK, style="italic" if gap else ""))
        body.append(text(1060, y + 30, where, 17, 700 if gap else 400, INK if gap else MUTED, "end"))
        y += 58
    return fig(1080, y + 4, body)


def bill():
    """Yearly service cost against the hardware, from assumed costs."""
    nodes, visit, module = 500, 50, 4
    hw = nodes * module
    rates = [("1 node in 1,000", 0.001), ("1 node in 100", 0.01), ("1 node in 20", 0.05)]
    x0, scale, top = 240, 560 / 15000, 76
    body = [text(20, 28, f"a {nodes}-node farm · assumed: US${visit} per site visit, US${module} per module",
                 19, 700, MUTED),
            text(20, top - 14, "needs a hand each month", 19, 700, MUTED)]
    for i, (name, p) in enumerate(rates):
        y = top + i * 74
        cost = nodes * 12 * visit * p
        body.append(text(20, y + 31, name, 21, 700, INK))
        col = INK if cost > hw else MUTED
        body.append(rect(x0, y + 6, max(cost * scale, 3), 38, col, "none", 0, 4))
        lx = max(x0 + cost * scale, x0 + hw * scale) + 14
        body.append(text(lx, y + 33, f"US${cost:,.0f} a year", 21, 700, col))
    xh = x0 + hw * scale
    yb = top + 3 * 74
    body.append(line(xh, top - 2, xh, yb, INK, 2.5, "7 5"))
    body.append(text(xh + 8, yb + 24, f"all {nodes} modules: US${hw:,} once", 20, 700, INK))
    body.append(line(x0, top - 2, x0, yb, MUTED, 1.5))
    return fig(1040, yb + 40, body)


def watchdog():
    """Two monitored loops, the task watchdog, the hardware fallback, and the way back."""
    body = [box(20, 24, 270, 76, "sampler thread", SCD, 21, "reads the sensor"),
            box(20, 124, 270, 76, "system workqueue", SCD, 21, "Observe, health, fail-safe"),
            arr(292, 62, 366, 98, INK, 2.5), arr(292, 162, 366, 126, INK, 2.5),
            text(330, 66, "feed", 18, 700, MUTED, "middle"),
            box(370, 74, 240, 76, "task watchdog", TW, 21, "10 s per channel"),
            arr(612, 112, 690, 112, C[TW], 3),
            text(651, 94, "starved", 18, 700, C[TW], "middle"),
            box(694, 80, 130, 64, "reset", TW, 22),
            box(370, 232, 240, 60, "hardware watchdog", "gray", 20),
            parr([(490, 232), (490, 154)], MUTED, 2.5),
            text(502, 200, "if the task watchdog itself stops", 17, 400, MUTED),
            arr(826, 112, 868, 112, INK, 2.5),
            box(872, 74, 230, 76, "boot, rejoin", TH, 21, "stored network"),
            arr(987, 152, 987, 228, INK, 2.5),
            box(872, 232, 230, 60, "green again", OMD, 21)]
    body.append(text(20, 334, "a hang becomes a reboot, and a reboot is something the system already survives",
                     20, 400, MUTED))
    return fig(1122, 350, body)

if __name__ == "__main__":
    figs = [("biz_lenses.svg", lenses), ("biz_chain.svg", chain), ("biz_service.svg", service),
            ("biz_bill.svg", bill), ("biz_watchdog.svg", watchdog)]
    for name, f in figs:
        print(save(HERE, name, f()))
