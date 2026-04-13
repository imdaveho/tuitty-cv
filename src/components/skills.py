import asyncio
from ffi import Effect, Color, InputEvent, Clear


def render_categories(props):
    tty = props["dispatcher"]
    categories = ["Technical", "Product", "Leadership", "Analytics"]
    width = 65
    w = props["size"][0]
    from_left = (w - width) // 2
    # print skill list
    choice = props["skill_index"]
    is_detail_open = props["skill_detail_open"]
    for i, cat in enumerate(categories):
        if i == choice:
            tty.goto(from_left, 6 + i * 2)
            tty.set_fg(Color.Green)
            tty.prints(" › ")
            tty.set_fg(Color.Reset)
            tty.prints(cat.ljust(11))
        else:
            tty.goto(from_left, 6 + i * 2)
            tty.prints(f"   {cat}".ljust(11))
    if is_detail_open:
        from_left = (w - width) // 2
        tty.goto(from_left, 6 + (choice * 2))
        tty.set_fx(Effect.Reverse)
        category = categories[choice]
        tty.prints(f" › {category}".ljust(14))
        tty.set_fx(Effect.Reset)
    tty.flush()


def render_category(choice, tty, w, **kwargs):
    categories = ["Technical", "Product", "Leadership", "Analytics"]
    width = 65
    from_left = (w - width) // 2
    tty.goto(from_left, 6 + (choice * 2))
    tty.set_fx(Effect.Reverse)
    category = categories[choice]
    tty.prints(f" › {category}".ljust(14))
    tty.set_fx(Effect.Reset)
    from_left = (w - width) // 2 + 14
    for i in range(7):
        tty.goto(from_left, 6 + i)
        tty.prints("│")

    if choice == 0:
        for i in range(7):
            tty.goto(from_left + 18, 6 + i)
            tty.prints("│")
        selected = kwargs["technical_index"]
        render_tech_list(tty, from_left, selected)
    elif choice == 1:
        selected = kwargs["product_index"]
        render_prod_list(tty, from_left, selected)
    elif choice == 2:
        selected = kwargs["leader_index"]
        render_lead_list(tty, from_left, selected)
    elif choice == 3:
        selected = kwargs["analysis_index"]
        render_data_list(tty, from_left, selected)
    else:
        pass


proficiency = {
    1: "› Capable",
    2: "› Skilled",
    3: "› Proficient"
}


technical_list = {
    "after fx": {
        "rating": 2,
        "domain": [("video editing", 1), ("motion graphics", 1),
                   ("special effects", 0)]
    },
    "blender/3d": {
        "rating": 1,
        "domain": [("printing", 0), ("modeling", 0), ("animation", 0)]
    },
    "2d graphics": {
        "rating": 2,
        "domain": [("logos", 1), ("vector graphics", 1), ("illustration", 0)]
    },
    "clojure": {
        "rating": 3,
        "domain": [("web apps", 1), ("analytics", 1),
                   ("scripting", 1), ("data/ML", 0)]
    },
    "dart": {
        "rating": 2,
        "domain": [("mobile apps", 1), ("desktop apps", 1), ("web apps", 0)]
    },
    "golang": {
        "rating": 2,
        "domain": [("dev tools", 1), ("devops", 0), ("system libs", 0)]
    },
    "javascript": {
        "rating": 3,
        "domain": [("web apps", 1), ("scripting", 1),
                   ("desktop apps", 1), ("mobile apps", 0)]
    },
    "java/kotlin": {
        "rating": 1,
        "domain": [("mobile apps", 0),  ("game dev", 0)]
    },
    "nim/c": {
        "rating": 2,
        "domain": [("ffi", 1), ("dev tools", 1),
                   ("game dev", 1), ("system libs", 0)]
    },
    "python": {
        "rating": 3,
        "domain": [("scripting", 1), ("analytics", 1),
                   ("web apps", 1), ("dev tools", 1)]
    },
    "ruby": {
        "rating": 1,
        "domain": [("web apps", 1), ("scripting", 1)]
    },
    "rust": {
        "rating": 2,
        "domain": [("system libs", 1), ("binaries", 1),
                   ("networking", 0), ("desktop apps", 0)]
    },
    "swift/obj-C": {
        "rating": 1,
        "domain": [("mobile apps", 0)]
    },
    "sql": {
        "rating": 2,
        "domain": [("analytics", 1), ("web apps", 1), ("data/ML", 0)]
    }
}


def render_tech_list(tty, from_left, selected):
    # print technical list
    show_count = 7
    tech_list = list(technical_list.keys())
    selected_key = tech_list[selected]
    if selected <= 3:
        start = 0
        index = selected
    elif selected >= len(tech_list) - 4:
        start = len(tech_list) - show_count
        index = show_count - (len(tech_list) - selected)
    else:
        start = selected - 3
        index = 3
    for i, item in enumerate(tech_list[start:start + show_count]):
        tty.goto(from_left + 1, 6 + i)
        if i == index:
            # print active selection
            tty.set_fg(Color.Green)
            tty.prints(f" ● {item.upper()}".ljust(14))
            tty.set_fg(Color.Reset)
            # print selection details
            tty.goto(from_left + 20, 6)
            rating = technical_list[selected_key]["rating"]
            score = ("★" * rating).strip()
            score_details = proficiency[rating]
            tty.prints(f" Rating: ({score}) {score_details}".ljust(27))
            for j in range(5):
                tty.goto(from_left + 22, 8 + j)
                tty.clear(Clear.NewLine)
            for j, jtem in enumerate(technical_list[selected_key]["domain"]):
                tty.goto(from_left + 22, 8 + j)
                symbol = "● " if jtem[1] == 1 else "◐ "
                tty.prints((symbol + jtem[0]).ljust(18))
        else:
            tty.set_fx(Effect.Dim)
            tty.prints(f"   {item.upper()}".ljust(14))
            tty.set_fx(Effect.Reset)
    tty.flush()


def render_prod_list(tty, from_left, selected):
    tty.goto(from_left + 2, 6)
    tty.prints("Case Studies")
    cases = [
        "#1 - Theory of Contraints",
        "#2 - Silver Bites the Bullet",
        "#3 - Platform Before the Horse",
        "#4 - Emperor's New Clothes",
        "#5 - Crouching Turtles, Hidden Data"
    ]
    for i, t in enumerate(cases):
        if i == selected:
            tty.set_fg(Color.Cyan)
            tty.goto(from_left + 4, 8 + i)
            tty.prints(t)
            tty.set_fg(Color.Reset)
            # TODO: print description
        else:
            tty.goto(from_left + 4, 8 + i)
            tty.prints(t)
    synopsis = [
        "Revenue has been trending sideways for the last 8 quarters. "
        + "Site metrics have averaged out so that any gains from new "
        + "\"features\"  (UI updates) have declined after a few weeks. "
        + "Senior leadership  understandably is reacting by changing tactics "
        + "every few weeks.  The Theory of Contraints informs us to find the "
        + "bottleneck, but  when opinions are heated and uncertainty is high, "
        + "how do you     present an case of doing something seemingly out of "
        + "left field?",

        "When the entire organization believes that X team building new "
        + "  \"product\" Y will solve everyone's problems, as the lead PM, "
        + "you  know your primary job is to dispell the myth of the panacea "
        + "     product. The approach must first identify all the parties "
        + "       involved, discover the root problems each team is facing, "
        + "and    define criteria to gauge positive outcomes. The goal at this"
        + "     point for the PM is to shift the narrative from producing an"
        + " all-cure, towards an iteration cycle of gradually improving "
        + "results.",

        "The engineering team has been pressured in the last 3 months to "
        + " create a \"platform\". You have been pushing back and attempting "
        + "toadd definition and structure to what was asked. You have just "
        + "   stablized a portion of the API design (the MVP if you must), "
        + "but in order to be successful, we must observe if the rest of the "
        + "   organization adopts our solution, learn from usage, and iterate."
        + " Leadership claims that they can simply \"mandate\" usage, and the "
        + " tech team releases the rest into production. Things break and "
        + "   crash often. The product's reputation suffers and trust in the"
        + "   platform erodes. What happens next?",

        "Often times, the most difficult part of a product manager's job  is "
        + "not in the planning, analysis, or development of the product "
        + " itself. Rather, it is managing strong opinions from within the "
        + "  organization. This is due to the fact that the product role is "
        + "  not defined by any single skillset, but draws from many domains:"
        # "Most of the time, this comes from senior executives "
        # + "with zero to little real world knowledge of product practices. "
        + " marketing, analytics, design, programming, etc. So when everyone "
        + "and anyone believes they can do the product work, we need to "
        + "    differentiate product vs. the rest while simultaneously not "
        + "     suppressing innovation from the rest of the organization?",
        # "This is to say that product "
        # + "management has a very gradual learning curve and competence is "
        # + "quite easily mistaken and errors obfuscated long after the "
        # + "original work is shipped.

        "PMs are not immune to cognitive biases like projection "
        + "bias. Exp-erience can mitigate "
        + "this, but experience can also perpetuate thesame bias. Because we "
        + "have a sense of familiarity of a problem   domain, we assume the "
        + "proverbial \"two weeks\" stance for how long a known enitity may "
        + "take. However, we should take caution and    recall that there are "
        + "always unknowns and incomplete data/info.  Care should be "
        + "exercised to not underestimate and reduce a new   endeavor to an "
        + "\"it's just a simple\" statement."
    ]
    tty.goto(from_left - 14, 15)
    tty.prints("Summary:")
    tty.goto(from_left + 39, 15)
    tty.set_fg(Color.Cyan)
    tty.prints("(view post)")
    tty.set_fg(Color.Reset)
    tty.clear(Clear.CursorDown)
    content = synopsis[selected]
    wraps = len(content) // 65
    for i in range(wraps + 1):
        start = i * 65
        stop = start + 65
        tty.goto(from_left - 14, 17 + i)
        tty.prints(content[start:stop])
    tty.flush()


def render_lead_list(tty, from_left, selected):
    tty.goto(from_left + 2, 6)
    tty.prints("Thought Leadership")
    titles = [
            "It isn't about speed, but predictable consistency.",
            "What organizations get wrong about iteration.",
            "Why \"stay in your lane\" hurts innovation.",
            "Hiring is broken because people aren't a priority.",
            "CAPM: Capital Asset [Product] Model."
    ]
    for i, t in enumerate(titles):
        if i == selected:
            tty.set_fg(Color.Cyan)
            tty.goto(from_left + 4, 8 + i)
            tty.prints(t)
            tty.set_fg(Color.Reset)
        else:
            tty.goto(from_left + 4, 8 + i)
            tty.prints(t)
    synopsis = [
        "In the development world, there is a mutual understanding that "
        + "  predictability and determinism is preferred over performance "
        + "and speed. Because it is known that if the program is incorrect "
        + "and  hard to debug, then a speedy program just makes the errors "
        + "      propagate that much more frequently, further exacerbating "
        + "the    problem. Does this work even when the commonly accepted "
        + "belief isthat faster time to market brings success?",

        "Organizations love to echo catchy phrases like \"fail fast\" and "
        + "  \"iterate or die\". We need to acknowledge that software also "
        + "obeysthe law of entropy like anything else in this world. Which "
        + "means that it's either going to suck at the beginning, or it's "
        + "going tosuck eventually. Iteration is more about preservation "
        + "and a      recognition to fix up mistakes that were made at the "
        + "start and   throughout the process. Iteration should not get "
        + "mixed up with   innovation.",

        "Role clarity and a firm understanding of how one contributes to  an "
        + "organization is incredibly important. What falls short after "
        + " creating these verticals and roles, is an emphasis on the "
        + "       interactions between them. The outcome of this deficiency "
        + "is the expression to \"stay in your lane\". That expression is a "
        + "bane to  innovation.",

        "When hiring, we always look for qualifications, skills, and "
        + "     criteria and end up regreting hiring decisions when the "
        + "\"fit\"    doesn't manifest after a few weeks or months. But "
        + "why should we  expect anything different when we have made our "
        + "focus strictly oncredentials instead of the person?",

        "In finance, the Capital Asset Pricing Model (CAPM) describes the "
        + "relationship between systematic risk and expected returns for "
        + "   assets (eg. stocks, bonds). One key concept of this model is "
        + "    something called the \"efficient frontier\". This describes "
        + "the    optimal portfolio relative to risk that an investor can "
        + "make.    When we consider software trade-offs like build vs. "
        + "buy, React   vs. Angular, native vs. hybrid, and when to incur "
        + "vs. pay off    tech debt, could we also model it using a similar "
        + "construct?"
    ]
    tty.goto(from_left - 14, 15)
    tty.prints("Summary:")
    tty.goto(from_left + 39, 15)
    tty.set_fg(Color.Cyan)
    tty.prints("(view post)")
    tty.set_fg(Color.Reset)
    tty.clear(Clear.CursorDown)
    content = synopsis[selected]
    wraps = len(content) // 65
    for i in range(wraps + 1):
        start = i * 65
        stop = start + 65
        tty.goto(from_left - 14, 17 + i)
        tty.prints(content[start:stop])
    tty.flush()


def render_data_list(tty, from_left, selected):
    tty.goto(from_left + 2, 6)
    tty.prints("Working Analyses")
    tty.goto(from_left + 4, 8)
    tty.set_fg(Color.Cyan)
    tty.prints("TBA")
    tty.set_fg(Color.Reset)
    # tty.goto(from_left - 14, 15)
    tty.goto(from_left + 4, 9)
    tty.prints("Summary:")
    # tty.goto(from_left - 14, 17)
    tty.goto(from_left + 4, 11)
    tty.prints("To be added later.")
    tty.flush()


async def handle(props):
    delay = props["delay"]
    tty = props["dispatcher"]
    is_detail_open = props["skill_detail_open"]
    choice = props["skill_index"]
    w = props["size"][0]
    width = 65
    from_left = (w - width) // 2 + 14
    render_categories(props)
    with tty.spawn() as handle:
        while True:
            await asyncio.sleep(delay)
            if not props["is_running"] or props["section_id"] != 2:
                props["skill_index"] = 0
                break
            evt = handle.poll_latest_async()
            if evt is None:
                continue

            if evt.kind() == InputEvent.Up and not props["is_menu_open"]:
                # depending on if detail is open or which skill section
                # this will either update the detail or the skill list
                if not is_detail_open:
                    if props["skill_index"] - 1 < 0:
                        props["skill_index"] = 0
                    else:
                        props["skill_index"] -= 1
                    choice = props["skill_index"]
                    render_categories(props)
                elif is_detail_open and choice == 0:
                    # handle tech list
                    if props["technical_index"] - 1 < 0:
                        props["technical_index"] = 0
                    else:
                        props["technical_index"] -= 1
                    selected = props["technical_index"]
                    render_tech_list(tty, from_left, selected)
                elif is_detail_open and choice == 1:
                    # handle product list
                    if props["product_index"] - 1 < 0:
                        props["product_index"] = 0
                    else:
                        props["product_index"] -= 1
                    selected = props["product_index"]
                    render_prod_list(tty, from_left, selected)
                elif is_detail_open and choice == 2:
                    # handle leader list
                    if props["leader_index"] - 1 < 0:
                        props["leader_index"] = 0
                    else:
                        props["leader_index"] -= 1
                    selected = props["leader_index"]
                    render_lead_list(tty, from_left, selected)
                else:
                    pass

            elif evt.kind() == InputEvent.Down and not props["is_menu_open"]:
                # depending on if detail is open or which skill section
                # this will either update the detail or the skill list
                if not is_detail_open:
                    if props["skill_index"] + 1 > 3:
                        props["skill_index"] = 3
                    else:
                        props["skill_index"] += 1
                    choice = props["skill_index"]
                    render_categories(props)
                elif is_detail_open and choice == 0:
                    # handle tech list
                    maxlen = len(technical_list)
                    if props["technical_index"] + 1 > maxlen - 1:
                        props["technical_index"] = maxlen - 1
                    else:
                        props["technical_index"] += 1
                    selected = props["technical_index"]
                    render_tech_list(tty, from_left, selected)
                elif is_detail_open and choice == 1:
                    # handle product list
                    if props["product_index"] + 1 > 4:
                        props["product_index"] = 4
                    else:
                        props["product_index"] += 1
                    selected = props["product_index"]
                    render_prod_list(tty, from_left, selected)
                elif is_detail_open and choice == 2:
                    # handle leader list
                    if props["leader_index"] + 1 > 4:
                        props["leader_index"] = 4
                    else:
                        props["leader_index"] += 1
                    selected = props["leader_index"]
                    render_lead_list(tty, from_left, selected)
                else:
                    pass

            elif ((evt.kind() == InputEvent.Left or
                  evt.kind() == InputEvent.Backspace) and
                  not props["is_menu_open"]):
                if is_detail_open:
                    props["skill_detail_open"] = False
                    is_detail_open = props["skill_detail_open"]
                    # clear detail section
                    for i in range(8):
                        tty.goto(from_left, 6 + i)
                        tty.clear(Clear.NewLine)
                    tty.clear(Clear.CursorDown)
                    render_categories(props)

            elif ((evt.kind() == InputEvent.Right or
                  evt.kind() == InputEvent.Enter) and
                  not props["is_menu_open"]):
                if not is_detail_open:
                    props["skill_detail_open"] = True
                    is_detail_open = props["skill_detail_open"]
                    # load appropriate detail section
                    data = {
                        "technical_index": props["technical_index"],
                        "product_index": props["product_index"],
                        "leader_index": props["leader_index"],
                        "analysis_index": props["analysis_index"],
                    }
                    render_category(props["skill_index"], tty, w, **data)
                elif is_detail_open and choice == 1:
                    # TODO: open link
                    pass
                elif is_detail_open and choice == 2:
                    # TODO: open link
                    pass
            elif evt.kind() == InputEvent.MousePressLeft:
                # TODO: handle click events
                pass
            else:
                pass
