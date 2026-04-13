import asyncio
import webbrowser
from ffi import Color, InputEvent


projects = [
    {
        "url": "https://github.com/imdaveho/tuitty",
        "title": "tuitty: cross-platform, interoperable, terminal library"
    },
    {
        "url": "https://github.com/imdaveho/impromptu",
        "title": "impromptu: interactive forms in the command line"
    },
    {
        "url": "https://github.com/imdaveho/daveho-cli",
        "title": "daveho-cli: this application :)"
    }
]


def render(props):
    (w, h) = props["size"]
    tty = props["dispatcher"]
    choice = props["opensrc_index"]
    from_left = (w - 65) // 2 + 4
    from_top = h // 2 - 4
    for i, item in enumerate(projects):
        tty.goto(from_left, from_top + i)
        if i == choice:
            tty.set_fg(Color.Cyan)
        tty.prints(item["title"])
        if i == choice:
            tty.set_fg(Color.Reset)
    tty.flush()


async def handle(props):
    delay = props["delay"]
    (w, h) = props["size"]
    tty = props["dispatcher"]
    tty.goto(w // 2 - 16, h // 2 + 2)
    tty.prints("Press ")
    tty.set_fg(Color.Cyan)
    tty.prints("<ENTER>")
    tty.set_fg(Color.Reset)
    tty.prints(" to visit the link")
    render(props)
    with tty.spawn() as handle:
        while True:
            await asyncio.sleep(delay)
            if not props["is_running"] or props["section_id"] != 4:
                props["opensrc_index"] = 0
                break
            evt = handle.poll_latest_async()
            if evt is None:
                continue

            if evt.kind() == InputEvent.Up and not props["is_menu_open"]:
                if props["opensrc_index"] - 1 < 0:
                    props["opensrc_index"] = 0
                else:
                    props["opensrc_index"] -= 1
                render(props)

            elif evt.kind() == InputEvent.Down and not props["is_menu_open"]:
                if props["opensrc_index"] + 1 > 3 - 1:
                    props["opensrc_index"] = 3 - 1
                else:
                    props["opensrc_index"] += 1
                render(props)

            elif evt.kind() == InputEvent.Enter and not props["is_menu_open"]:
                choice = props["opensrc_index"]
                link = projects[choice]["url"]
                webbrowser.open_new_tab(link)
            else:
                pass
