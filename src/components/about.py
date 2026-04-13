import asyncio
from os import path
from random import shuffle
from webbrowser import open_new_tab
from ffi import Clear, InputEvent, Color


async def render(props):
    tty = props["dispatcher"]
    w = props["size"][0]
    # Setup messages
    quotes = [
        ("Find the good", "and believe it"),
        ("Perfect is the", "enemy of great"),
        ("Thru discipline", "comes freedom"),
        ("if knocked_down:", "  get_up += 1"),
        ("Non nobis solum", "nati sumus"),
        ("Ad astra", "per aspera")]
    errors = [
        ("404 Not Found:", "file `good.py`"),
        ("ERR04 Recursion", "depth exceeded"),
        ("[error]: cannot", "assign to field"),
        ("[!] `undefined`", "is not an object"),
        ("RefErr: event", "is undefined"),
        ("#: Cannot find", "vcvarsall.bat")]
    relaxes = [
        ("Ok, keep calm", "and carry on"),
        ("Hmm...oh! Just", "a typo : vs ;"),
        ("www.reddit.com/", "r/funnycats"),
        ("It works again!", "...no idea why"),
        ("Not a bug! Call", "it a feature!"),
        ("Maybe it's time", "to recaffinate!")]
    indices = [0, 1, 2, 3, 4, 5]
    shuffle(indices)
    scene_delay = 0.1
    # Read animation file
    scenes_path = path.join(path.abspath(
        path.dirname(path.abspath(__file__))), "scenes.txt")
    scene_len = 0
    scene_queue = asyncio.Queue(maxsize=263)
    with open(scenes_path, encoding="utf-8", mode="r") as f:
        scenes = f.read().split('1.')
        scene_len = len(scenes)
        for scene in scenes:
            try:
                scene_queue.put_nowait(scene)
            except asyncio.QueueFull:
                raise("Incorrect scene length")
    # <-- close file
    # Setup screen
    tty.clear(Clear.CursorDown)

    render_blurb(props)

    (start_col, start_row) = (0, 14)
    (iterations, full_loops) = (0, 0)
    (inita, initb) = (170, 243)
    tty.goto(start_col, start_row)
    msg_id = indices.pop()
    while True:
        tty.goto(start_col, start_row)
        if props["section_id"] != 0 or not props["is_running"]:
            break
        scene = await scene_queue.get()
        # put scene back to make circular buffer
        await scene_queue.put(scene)
        if (iterations % scene_len) in range(46, 73):
            (qav, qbv) = quotes[msg_id]
            (enda, endb) = (inita + len(qav), initb + len(qbv))
            updated = scene[:inita] + qav + \
                scene[enda:initb] + qbv + scene[endb:]
        elif (iterations % scene_len) in range(74, 99):
            (eav, ebv) = errors[msg_id]
            (enda, endb) = (inita + len(eav), initb + len(ebv))
            updated = scene[:inita] + eav + \
                scene[enda:initb] + ebv + scene[endb:]
        elif (iterations % scene_len) in range(120, 132):
            (rav, rbv) = relaxes[msg_id]
            (enda, endb) = (inita + len(rav), initb + len(rbv))
            updated = scene[:inita] + rav + \
                scene[enda:initb] + rbv + scene[endb:]
        elif iterations == scene_len:
            iterations = 1
            full_loops += scene_len
            try:
                msg_id = indices.pop()
            except IndexError:
                indices.extend([0, 1, 2, 3, 4, 5])
                shuffle(indices)
                msg_id = indices.pop()
            await asyncio.sleep(scene_delay)
            continue
        else:
            updated = scene
        # center animation w padding
        padded = ""
        for i, line in enumerate(updated.split("\n")):
            if i % 14 == 0:
                continue
            padded += line.center(w)
        iterations += 1
        tty.printf(padded)
        await asyncio.sleep(scene_delay)
    # <-- end loop


async def handle(props):
    delay = props["delay"]
    tty = props["dispatcher"]
    with tty.spawn() as handle:
        while True:
            await asyncio.sleep(delay)
            if not props["is_running"] or props["section_id"] != 0:
                break
            evt = handle.poll_latest_async()
            if evt is None:
                continue
            # TODO: example case, replace with click events
            if evt.kind() == InputEvent.Char and not props["is_menu_open"]:
                if evt.data() == 'g':
                    open_new_tab("https://github.com/imdaveho")
                    break
            else:
                pass
        # <-- end loop
    # <-- close handle


def render_blurb(props):
    tty = props["dispatcher"]
    w = props["size"][0]

    blurb1 = "I am a product leader obsessed with driving "
    blurb1 += "results and creating value"
    blurb2 = "for users. In my spare time, I code, write, "
    blurb2 += "and pursue new venture ideas."
    blurb4 = "Made with ♥ in NYC.".center(w)

    tty.goto(0, 5)
    tty.prints(blurb1.center(w))
    tty.goto(0, 6)
    tty.prints(blurb2.center(w))
    tty.goto(0, 7)
    tty.prints(blurb4[:blurb4.find('♥')])
    tty.set_fg(Color.Red)
    tty.prints('♥')
    tty.set_fg(Color.Reset)
    tty.prints(blurb4[blurb4.find('♥') + 1:])

    links = "GITHUB  |  LINKEDIN  |  WEBSITE  |  EMAIL"
    link_col = w // 2 - len(links) // 2
    tty.goto(link_col, 10)
    tty.set_fg(Color.DarkCyan)
    tty.prints("GITHUB")
    tty.set_fg(Color.Reset)
    tty.prints("  |  ")
    tty.set_fg(Color.DarkCyan)
    tty.prints("LINKEDIN")
    tty.set_fg(Color.Reset)
    tty.prints("  |  ")
    tty.set_fg(Color.DarkCyan)
    tty.prints("WEBSITE")
    tty.set_fg(Color.Reset)
    tty.prints("  |  ")
    tty.set_fg(Color.DarkCyan)
    tty.prints("EMAIL")
    tty.set_fg(Color.Reset)
