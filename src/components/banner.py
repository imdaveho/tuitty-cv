from ffi import Color, Effect

# NOTE: Issues with reseting styles on Windows
# Specifically with git-bash / winpty (and possibly
# legacy mode)


def render(props):
    tty = props["dispatcher"]
    w = props["size"][0]
    # Top Bar
    tty.goto(0, 0)
    tty.set_fg(Color.Green)
    tty.prints(" ≡ ")
    tty.set_fg(Color.Reset)
    tty.prints("MENU")
    tty.goto(w - 4, 0)
    tty.set_fg(Color.Red)
    tty.prints("[x]")
    tty.set_fg(Color.Reset)
    # Horiz Rule
    tty.goto(0, 1)
    tty.set_fx(Effect.Dim)
    tty.prints("─" * w)
    tty.set_fx(Effect.Reset)
