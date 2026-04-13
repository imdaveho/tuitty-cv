import json
import asyncio
import webbrowser
import urllib.request
from ffi import Color, InputEvent


async def render_loading(props):
    frames = ["▌", "▀", "▐", "▄"]
    (w, h) = props["size"]
    from_left = w // 2 - 12
    from_top = h // 2 - 4
    tty = props["dispatcher"]
    tty.goto(from_left + 2, from_top)
    tty.prints("loading reading list")
    queue = asyncio.Queue(maxsize=4)
    for frame in frames:
        try:
            queue.put_nowait(frame)
        except asyncio.QueueFull:
            raise("Incorrect loading length")
    count = 0
    tty.set_fg(Color.Yellow)
    while count < 24:
        tty.goto(from_left, from_top)
        frame = await queue.get()
        await queue.put(frame)
        tty.prints(frame)
        await asyncio.sleep(0.15)
        count += 1
        tty.flush()
    tty.set_fg(Color.Reset)


async def fetch_list(props):
    link = "https://us-central1-proud-matter-167404." + \
          "cloudfunctions.net/pocket_retrieve"
    with urllib.request.urlopen(url=link) as f:
        data = f.read()
        props["recent_cache"] = json.loads(data)


def render_reads(props):
    (w, h) = props["size"]
    tty = props["dispatcher"]
    recent = props["recent_cache"][0:8]
    choice = props["recent_index"]
    from_top = h // 2 - 4
    for i, item in enumerate(recent):
        tty.goto(0, from_top + i)
        if i == choice:
            tty.set_fg(Color.Cyan)
        tty.prints(item["title"].center(w))
        if i == choice:
            tty.set_fg(Color.Reset)
    tty.flush()


async def handle(props):
    delay = props["delay"]
    (w, h) = props["size"]
    tty = props["dispatcher"]
    tty.goto(w // 2 - 16, h // 2 + 6)
    tty.prints("Press ")
    tty.set_fg(Color.Cyan)
    tty.prints("<ENTER>")
    tty.set_fg(Color.Reset)
    tty.prints(" to visit the link")
    render_reads(props)
    recent = props["recent_cache"][0:8]
    with tty.spawn() as handle:
        while True:
            await asyncio.sleep(delay)
            if not props["is_running"] or props["section_id"] != 3:
                props["recent_index"] = 0
                break
            evt = handle.poll_latest_async()
            if evt is None:
                continue

            if evt.kind() == InputEvent.Up and not props["is_menu_open"]:
                if props["recent_index"] - 1 < 0:
                    props["recent_index"] = 0
                else:
                    props["recent_index"] -= 1
                render_reads(props)

            elif evt.kind() == InputEvent.Down and not props["is_menu_open"]:
                if props["recent_index"] + 1 > 8 - 1:
                    props["recent_index"] = 8 - 1
                else:
                    props["recent_index"] += 1
                render_reads(props)

            elif evt.kind() == InputEvent.Enter and not props["is_menu_open"]:
                choice = props["recent_index"]
                link = recent[choice]["url"]
                webbrowser.open_new_tab(link)
            else:
                pass
