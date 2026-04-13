import asyncio
# from random import shuffle
# from itertools import cycle
# from webbrowser import open_new_tab
# import tuitty library
from ffi import Dispatcher, InputEvent
# import application components
from components import banner, intro, splash, sections, menu


async def handle_quit(props):
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
            w = props["size"][0]
            if evt.kind() == InputEvent.Ctrl:
                if evt.data() == 'q':
                    props["is_running"] = False
                    break
            elif evt.kind() == InputEvent.MousePressLeft:
                (col, row) = evt.data()
                if row == 0 and (w - 4) <= col <= (w - 2):
                    props["is_running"] = False
                    break
            else:
                pass
        # <-- end loop
    # <-- close handle


async def main():
    with Dispatcher() as tty:
        # set up screen
        tty.switch()
        tty.raw()
        tty.enable_mouse()
        tty.hide_cursor()
        shared_props = {
            "size": (0, 0),
            "delay": 0.1,
            "offset_mid": 3,
            "dispatcher": tty,
            "is_running": True,
            "sections": [
                "ABOUT", "EXPERIENCE", "SKILLS",
                "RECENT READS", "OPEN SOURCE"
            ],
            "section_id": -1,
            "menu_index": 0,
            "is_menu_open": False,
            "statline": 0,
            "skill_index": 0,
            "skill_detail_open": False,
            "technical_index": 0,
            "product_index": 0,
            "leader_index": 0,
            "analysis_index": 0,
            "recent_index": 0,
            "recent_cache": [],
            "opensrc_index": 0
        }
        # update props with screen dimensions
        with tty.listen() as handle:
            shared_props["size"] = handle.size()
        # Render top banner
        banner.render(shared_props)
        intro.render(shared_props)
        splash.render(shared_props)
        tty.flush()

        await asyncio.gather(
            asyncio.create_task(handle_quit(shared_props)),
            asyncio.create_task(sections.toggle(shared_props)),
            asyncio.create_task(menu.handle(shared_props))
        )

        # TODO: update so that if is_running == False to close the
        # event loop all together

        # await asyncio.sleep(2)

        # restore screen
        tty.disable_mouse()
        tty.show_cursor()
        await asyncio.sleep(0.1)
        tty.cook()
        tty.switch_to(0)
    # <-- dispatcher closes
# <-- end


if __name__ == '__main__':
    asyncio.run(main())
