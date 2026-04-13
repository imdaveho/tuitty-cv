import asyncio
from ffi import Color, Effect, InputEvent
from . import about, stats, skills, reads, opensrc


def render(props):
    tty = props["dispatcher"]
    index = props["menu_index"]
    sections = props["sections"]

    tty.goto(0, 1)
    tty.set_fx(Effect.Dim)
    tty.prints("┌" + "─" * 14 + "┬")
    for i, section in enumerate(sections):
        tty.goto(0, 2 + i)
        if i == index:
            tty.prints("│")
            tty.set_fx(Effect.Reset)
            tty.set_fg(Color.Green)
            tty.prints("▎")
            tty.set_fg(Color.Reset)
            tty.set_fx(Effect.Reverse)
            tty.prints(section.ljust(13))
            tty.reset_styles()
            tty.set_fx(Effect.Dim)
            tty.prints("│")
        else:
            tty.prints("│")
            tty.set_fx(Effect.Reset)
            tty.set_fg(Color.Green)
            tty.prints("▎")
            tty.set_fg(Color.Reset)
            tty.prints(section.ljust(13))
            tty.set_fx(Effect.Dim)
            tty.prints("│")
    tty.goto(0, 7)
    tty.prints("└" + "─" * 14 + "┘")
    tty.set_fx(Effect.Reset)
    tty.flush()


async def handle(props):
    delay = props["delay"]
    tty = props["dispatcher"]
    with tty.spawn() as handle:
        while True:
            await asyncio.sleep(delay)
            if not props["is_running"]:
                break
            evt = handle.poll_latest_async()
            if evt is None or props["section_id"] == -1:
                continue
            # handle menu open/close
            sections = props["sections"]
            index = props["menu_index"]
            if evt.kind() == InputEvent.Tab:
                if not props["is_menu_open"]:
                    render(props)
                    props["is_menu_open"] = True
                else:
                    props["is_menu_open"] = False
                    reset_menu(handle)
                    reset_section(props)
                    handle.flush()

            elif evt.kind() == InputEvent.MousePressLeft:
                (col, row) = evt.data()
                if row == 0 and 0 <= col <= 5 and not props["is_menu_open"]:
                    render(props)
                    props["is_menu_open"] = True
                elif row == 0 and 0 <= col <= 5 and props["is_menu_open"]:
                    props["is_menu_open"] = False
                    reset_menu(handle)
                    reset_section(props)
                    handle.flush()

            elif evt.kind() == InputEvent.Esc and props["is_menu_open"]:
                props["is_menu_open"] = False
                reset_menu(handle)
                reset_section(props)
                handle.flush()

            elif evt.kind() == InputEvent.Up and props["is_menu_open"]:
                handle.set_fx(Effect.Dim)
                if index == 0:
                    handle.goto(0, 2)
                    handle.prints("│")
                    handle.set_fx(Effect.Reset)
                    handle.set_fg(Color.Green)
                    handle.prints("▎")
                    handle.set_fg(Color.Reset)
                    handle.prints(sections[index].ljust(13))
                    handle.set_fx(Effect.Dim)
                    handle.prints("│")
                    props["menu_index"] = 4
                    index = props["menu_index"]
                    handle.goto(0, 2 + 4)
                    handle.prints("│")
                    handle.set_fx(Effect.Reset)
                    handle.set_fg(Color.Green)
                    handle.prints("▎")
                    handle.set_fg(Color.Reset)
                    handle.set_fx(Effect.Reverse)
                    handle.prints(sections[index].ljust(13))
                    handle.reset_styles()
                    handle.set_fx(Effect.Dim)
                    handle.prints("│")
                    handle.flush()
                else:
                    handle.goto(0, 2 + index)
                    handle.prints("│")
                    handle.set_fx(Effect.Reset)
                    handle.set_fg(Color.Green)
                    handle.prints("▎")
                    handle.set_fg(Color.Reset)
                    handle.prints(sections[index].ljust(13))
                    handle.set_fx(Effect.Dim)
                    handle.prints("│")
                    props["menu_index"] = index - 1
                    index = props["menu_index"]
                    handle.goto(0, 2 + index)
                    handle.prints("│")
                    handle.set_fx(Effect.Reset)
                    handle.set_fg(Color.Green)
                    handle.prints("▎")
                    handle.set_fg(Color.Reset)
                    handle.set_fx(Effect.Reverse)
                    handle.prints(sections[index].ljust(13))
                    handle.reset_styles()
                    handle.set_fx(Effect.Dim)
                    handle.prints("│")
                    handle.flush()

            elif evt.kind() == InputEvent.Down and props["is_menu_open"]:
                handle.set_fx(Effect.Dim)
                if index == 4:
                    handle.goto(0, 2 + 4)
                    handle.prints("│")
                    handle.set_fx(Effect.Reset)
                    handle.set_fg(Color.Green)
                    handle.prints("▎")
                    handle.set_fg(Color.Reset)
                    handle.prints(sections[index].ljust(13))
                    handle.set_fx(Effect.Dim)
                    handle.prints("│")
                    props["menu_index"] = 0
                    index = props["menu_index"]
                    handle.goto(0, 2)
                    handle.prints("│")
                    handle.set_fx(Effect.Reset)
                    handle.set_fg(Color.Green)
                    handle.prints("▎")
                    handle.set_fg(Color.Reset)
                    handle.set_fx(Effect.Reverse)
                    handle.prints(sections[index].ljust(13))
                    handle.reset_styles()
                    handle.set_fx(Effect.Dim)
                    handle.prints("│")
                    handle.flush()
                else:
                    handle.goto(0, 2 + index)
                    handle.prints("│")
                    handle.set_fx(Effect.Reset)
                    handle.set_fg(Color.Green)
                    handle.prints("▎")
                    handle.set_fg(Color.Reset)
                    handle.prints(sections[index].ljust(13))
                    handle.set_fx(Effect.Dim)
                    handle.prints("│")
                    props["menu_index"] = index + 1
                    index = props["menu_index"]
                    handle.goto(0, 2 + index)
                    handle.prints("│")
                    handle.set_fx(Effect.Reset)
                    handle.set_fg(Color.Green)
                    handle.prints("▎")
                    handle.set_fg(Color.Reset)
                    handle.set_fx(Effect.Reverse)
                    handle.prints(sections[index].ljust(13))
                    handle.reset_styles()
                    handle.set_fx(Effect.Dim)
                    handle.prints("│")
                    handle.flush()

            elif evt.kind() == InputEvent.Enter and props["is_menu_open"]:
                props["is_menu_open"] = False
                reset_menu(handle)
                reset_section(props)
                handle.flush()
                props["section_id"] = index
            else:
                pass


def reset_menu(handle):
    handle.reset_styles()
    # restore top bar
    handle.goto(0, 1)
    handle.set_fx(Effect.Dim)
    handle.prints("─" * 16)
    handle.set_fx(Effect.Reset)
    # clear out menu
    for i in range(5):
        handle.goto(0, 2 + i)
        handle.prints(" " * 16)
    handle.goto(0, 7)
    handle.prints(" " * 16)


def reset_section(props):
    section = props["section_id"]
    section_fx = {
        0: about.render_blurb,
        1: stats.render_statline,
        2: skills.render_categories,
        3: reads.render_reads,
        4: opensrc.render
    }.get(section, lambda props: None)
    section_fx(props)
