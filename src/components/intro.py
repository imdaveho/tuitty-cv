from ffi import Effect


def render(props):
    tty = props["dispatcher"]
    offset = props["offset_mid"]
    (w, h) = props["size"]
    # Intro
    from_top = h // 3
    # Print Title
    title = "Dave Ho CLI v0.beta"
    from_col = w // 2 - (len(title) // 2) - offset
    tty.goto(from_col, from_top)
    tty.prints(title)
    # Print Subtitle
    subtitle = "\\\'dæv • \'hoh\\  賀毅超  (he, him, his)"
    from_col = w // 2 - (len(subtitle) + 3) // 2 - offset
    tty.goto(from_col, from_top + 1)
    tty.prints(subtitle[:13])
    tty.set_fx(Effect.Dim)
    tty.prints(subtitle[13:20])
    tty.set_fx(Effect.Reset)
    tty.prints(subtitle[20:])