import asyncio
from ffi import Effect, Color, InputEvent, Clear


# TODO: tuitty needs to implement some kind of string parser to make styling
# text much easier as marked up strings, and output seomthing like this:

document = {
    0: [{
            "start": 0,
            "text": "Career Summary",
            "styles": (None, None, Effect.Bold)
        }, {
            "start": 57,
            "text": "(view full PDF)",
            "styles": (Color.Cyan, None, None)
        }, ],
    1: [{
            "start": 0,
            "text": "─" * 72,
            "styles": (None, None, None)
        }, ],
    2: [{
            "start": 0,
            "text": "Director of Product at MealPal, Inc",
            "styles": (None, None, Effect.Bold)
        }, {
            "start": 42,
            "text": "New York, NY | (03/19 - 07/19)",
            "styles": (None, None, Effect.Dim)
        }, ],
    3: [{
            "start": 1,
            "text": ' * Launched a new flexible "Marketplace" product.',
            "styles": (None, None, None)
        }, ],
    4: [{
            "start": 1,
            "text": " * Revamped PM team with clear OKRs and fixed data gaps.",
            "styles": (None, None, None)
        }, ],
    5: [{
            "start": 0,
            "text": "",
            "styles": (None, None, None)
        }, ],
    6: [{
            "start": 0,
            "text": "Lead Product Manager at Jet.com",
            "styles": (None, None, Effect.Bold)
        }, {
            "start": 43,
            "text": "Hoboken, NJ | (08/17 - 03/19)",
            "styles": (None, None, Effect.Dim)
        }, ],
    7: [{
            "start": 1,
            "text": " * Managed the creation of a cross-functional " +
                    "workflow engine.",
            "styles": (None, None, None)
        }, ],
    8: [{
            "start": 1,
            "text": " * Unified multi-tenant, distributed systems of " +
                    "18 separate teams.",
            "styles": (None, None, None)
        }, ],
    9: [{
            "start": 1,
            "text": " * Led team of 4 PMs, 24 developers, and 3 designers.",
            "styles": (None, None, None)
        }, ],
    10: [{
            "start": 0,
            "text": "",
            "styles": (None, None, None)
        }, ],
    11: [{
            "start": 0,
            "text": "Senior Product Manager at Shapeways, Inc",
            "styles": (None, None, Effect.Bold)
        }, {
            "start": 42,
            "text": "New York, NY | (04/16 - 08/17)",
            "styles": (None, None, Effect.Dim)
        }, ],
    12: [{
            "start": 1,
            "text": " * Drove API initiatives for 3rd-party apps " +
                    "that incr. revenue +48%.",
            "styles": (None, None, None)
        }, ],
    13: [{
            "start": 1,
            "text": " * Optimized shopping UX to incr. retention and " +
                    "conversion +30%.",
            "styles": (None, None, None)
        }, ],
    14: [{
            "start": 0,
            "text": "",
            "styles": (None, None, None)
        }, ],
    15: [{
            "start": 0,
            "text": "Product Manager at Anvil Advisors, LLC",
            "styles": (None, None, Effect.Bold)
        }, {
            "start": 42,
            "text": "New York, NY | (12/13 - 11/15)",
            "styles": (None, None, Effect.Dim)
        }, ],
    16: [{
            "start": 1,
            "text": " * Launched AnvilIQ product that managed client " +
                    "equity grants.",
            "styles": (None, None, None)
        }, ],
    17: [{
            "start": 0,
            "text": "",
            "styles": (None, None, None)
        }, ],
    18: [{
            "start": 0,
            "text": "Co-Founder at Miss Nev, Inc",
            "styles": (None, None, Effect.Bold)
        }, {
            "start": 42,
            "text": "New York, NY | (10/12 - 09/14)",
            "styles": (None, None, Effect.Dim)
        }, ],
    19: [{
            "start": 1,
            "text": " * Launched beta with 50+ SMB partners and 300+ " +
                    "registered users.",
            "styles": (None, None, None)
        }, ],
    20: [{
            "start": 0,
            "text": "",
            "styles": (None, None, None)
        }, ],
    21: [{
            "start": 0,
            "text": "Stategy Analyst at NYSE Euronext, Inc",
            "styles": (None, None, Effect.Bold)
        }, {
            "start": 42,
            "text": "New York, NY | (07/10 - 08/12)",
            "styles": (None, None, Effect.Dim)
        }, ],
    22: [{
            "start": 1,
            "text": " * Advised web division build of listed company " +
                    "networking service.",
            "styles": (None, None, None)
        }, ],
    23: [{
            "start": 0,
            "text": "",
            "styles": (None, None, None)
        }, ],
    24: [{
            "start": 0,
            "text": "Education",
            "styles": (None, None, Effect.Bold)
        }, ],
    25: [{
            "start": 0,
            "text": "─" * 72,
            "styles": (None, None, None)
        }, ],
    26: [{
            "start": 0,
            "text": "NYU, Leonard N. Stern School of Business",
            "styles": (None, None, Effect.Bold)
        }, {
            "start": 42,
            "text": "New York, NY | (09/06 - 05/10)",
            "styles": (None, None, Effect.Dim)
        }, ],
    27: [{
            "start": 1,
            "text": " * Bachelor of Science in Finance and Economics.",
            "styles": (None, None, None)
        }, ],
    28: [{
            "start": 1,
            "text": " * Vice President of MCG and creator of PwC student " +
                    "mentorship program.",
            "styles": (None, None, None)
        }, ],
    29: [{
            "start": 0,
            "text": "",
            "styles": (None, None, None)
        }, ],
}


def render(tty, w, top_row, bot_row, doc_len, viewport, statline):
    doc_w = 72
    left_pad = (w - doc_w) // 2 - 1
    if doc_len > viewport:
        for i in range(viewport):
            val = document[statline + i]
            print_statline(val, left_pad, top_row + i, tty)
        tty.goto(0, top_row + viewport + 1)
        if statline == doc_len - viewport:
            # document end
            tty.prints("end of document".center(w))
            tty.goto(0, top_row + viewport + 2)
            tty.prints("scroll up with ↑ arrow".center(w))
        elif statline == 0:
            # document top
            tty.prints("scroll down with ↓ arrow".center(w))
        else:
            # document middle
            tty.prints("scroll by using ↑↓ arrows".center(w))
    else:
        # this means we can print the entire thing
        for i, val in enumerate(document.values()):
            print_statline(val, left_pad, top_row + i, tty)
    tty.flush()


def print_statline(val, pad, row, tty):
    for region in val:
        text = region["text"]
        if text:
            col = pad + region["start"]
            tty.goto(col, row)
            (fg, bg, fx) = region["styles"]
            if fg is not None:
                tty.set_fg(fg)
            if bg is not None:
                tty.set_bg(bg)
            if fx is not None:
                tty.set_fx(fx)
            tty.prints(text)
            tty.reset_styles()


async def handle(props):
    delay = props["delay"]
    tty = props["dispatcher"]
    (w, h) = props["size"]
    statline = props["statline"]
    top_row = 5
    bot_row = h - top_row
    viewport = bot_row - top_row
    doc_len = len(document)  # 30 as of 11/19
    render(tty, w, top_row, bot_row, doc_len, viewport, statline)
    with tty.spawn() as handle:
        while True:
            await asyncio.sleep(delay)
            if not props["is_running"] or props["section_id"] != 1:
                props["statline"] = 0
                break
            evt = handle.poll_latest_async()
            if evt is None:
                continue
            statline = props["statline"]
            if evt.kind() == InputEvent.Down and not props["is_menu_open"]:
                # update statline if document has not reached bottom
                if not statline + viewport >= doc_len:
                    if statline + 5 >= doc_len:
                        props["statline"] = doc_len - viewport
                    else:
                        props["statline"] += 5
                    statline = props["statline"]
                    tty.goto(0, top_row)
                    tty.clear(Clear.CursorDown)
                    render(tty, w, top_row, bot_row, doc_len,
                           viewport, statline)
            elif evt.kind() == InputEvent.Up and not props["is_menu_open"]:
                if statline > 0:
                    if statline - 5 > 0:
                        props["statline"] -= 5
                    else:
                        props["statline"] = 0
                    statline = props["statline"]
                    tty.goto(0, top_row)
                    tty.clear(Clear.CursorDown)
                    render(tty, w, top_row, bot_row, doc_len,
                           viewport, statline)
            else:
                pass
        # <-- end loop
    # <-- close handle


def render_statline(props):
    tty = props["dispatcher"]
    (w, h) = props["size"]
    statline = props["statline"]
    top_row = 5
    doc_w = 72
    left_pad = (w - doc_w) // 2 - 1
    for i in range(3):
        val = document[statline + i]
        print_statline(val, left_pad, top_row + i, tty)
    tty.flush()
