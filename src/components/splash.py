import asyncio
from ffi import Color, Effect, InputEvent


def render(props):
    tty = props["dispatcher"]
    offset = props["offset_mid"]
    (w, h) = props["size"]
    sections = props["sections"]
    # Navigation instructions
    from_top = h // 3 + 3
    midpoint = w // 2
    instructions = "Navigate with ↑↓ Press <ENTER> to view"
    from_col = midpoint - len(instructions) // 2 - offset
    tty.goto(from_col, from_top)
    tty.prints(instructions[:23])
    tty.set_fg(Color.Cyan)
    tty.prints(instructions[23:30])
    tty.set_fg(Color.Reset)
    tty.prints(instructions[30:])
    # Section breakdown
    tty.set_fx(Effect.Dim)
    from_col = midpoint - 9
    from_top = from_top + 2
    for i, section in enumerate(sections):
        tty.goto(from_col, from_top + i)
        if i == 0:
            tty.set_fx(Effect.Reset)
            tty.set_fg(Color.Green)
            tty.prints(section)
            tty.set_fg(Color.Reset)
            tty.set_fx(Effect.Dim)
        else:
            tty.prints(section)
    tty.set_fx(Effect.Reset)
    # Tab instructions
    instructions = "Press <TAB> to toggle the navbar after this point"
    from_col = w // 2 - len(instructions) // 2 - offset
    from_top = from_top + 7
    tty.goto(from_col, from_top)
    tty.prints(instructions[:6])
    tty.set_fg(Color.Cyan)
    tty.prints(instructions[6:11])
    tty.set_fg(Color.Reset)
    tty.prints(instructions[11:])


async def handle(props):
    delay = props["delay"]
    tty = props["dispatcher"]
    with tty.spawn() as handle:
        while True:
            await asyncio.sleep(delay)
            if not props["is_running"]:
                break
            evt = handle.poll_latest_async()
            if evt is None:
                continue
            # setup region and local variables
            (w, h) = props["size"]
            from_col = w // 2 - 9
            from_top = h // 3 + 3 + 2
            index = props["menu_index"]
            sections = props["sections"]
            # handle events
            if evt.kind() == InputEvent.Up:
                handle.set_fx(Effect.Reset)
                if index == 0:
                    # At top, so wrap around
                    handle.goto(from_col, from_top)
                    handle.set_fx(Effect.Dim)
                    handle.prints(sections[0])
                    handle.goto(from_col, from_top + 4)
                    handle.set_fx(Effect.Reset)
                    handle.set_fg(Color.Green)
                    handle.printf(sections[4])
                    props["menu_index"] = 4
                    index = props["menu_index"]
                else:
                    # Move up one
                    handle.goto(from_col, from_top + index)
                    handle.set_fx(Effect.Dim)
                    handle.prints(sections[index])
                    props["menu_index"] = index - 1
                    index = props["menu_index"]
                    handle.goto(from_col, from_top + index)
                    handle.set_fx(Effect.Reset)
                    handle.set_fg(Color.Green)
                    handle.printf(sections[index])
            elif evt.kind() == InputEvent.Down:
                handle.set_fx(Effect.Reset)
                if index == 4:
                    # At bottom, so wrap around
                    handle.goto(from_col, from_top + 4)
                    handle.set_fx(Effect.Dim)
                    handle.prints(sections[4])
                    handle.goto(from_col, from_top)
                    handle.set_fx(Effect.Reset)
                    handle.set_fg(Color.Green)
                    handle.printf(sections[0])
                    props["menu_index"] = 0
                    index = props["menu_index"]
                else:
                    # Move down one
                    handle.goto(from_col, from_top + index)
                    handle.set_fx(Effect.Dim)
                    handle.prints(sections[index])
                    props["menu_index"] = index + 1
                    index = props["menu_index"]
                    handle.goto(from_col, from_top + index)
                    handle.set_fx(Effect.Reset)
                    handle.set_fg(Color.Green)
                    handle.printf(sections[index])
            elif evt.kind() == InputEvent.Enter:
                handle.set_fx(Effect.Reset)
                props["section_id"] = index
                break
            else:
                pass
        # <-- end loop
    # <-- close handle
