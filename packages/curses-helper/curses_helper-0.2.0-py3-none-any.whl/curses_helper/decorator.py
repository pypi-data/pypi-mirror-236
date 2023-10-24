import curses


def curses_app(echo=False, cbreak=True, keypad=False, color=True):
    def wrapper(func: callable):
        def wrapper(*args, **kwargs):
            try:
                stdscr = curses.initscr()

                if not echo:
                    curses.noecho()

                if cbreak:
                    curses.cbreak()

                stdscr.keypad(keypad)

                if curses.has_colors() and color:
                    curses.start_color()

                func(stdscr, *args, **kwargs)
            finally:
                curses.nocbreak()
                curses.echo()
                stdscr.keypad(False)
                curses.endwin()

        return wrapper

    return wrapper
