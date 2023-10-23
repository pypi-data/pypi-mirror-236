import curses


def curses_app(echo=False, cbreak=True, keypad=False):
    def wrapper(func: callable):
        def wrapper(*args, **kwargs):
            try:
                stdscr = curses.initscr()
                if not echo:
                    curses.noecho()
                if cbreak:
                    curses.cbreak()
                stdscr.keypad(keypad)

                func(stdscr, *args, **kwargs)
            finally:
                curses.nocbreak()
                curses.echo()
                stdscr.keypad(False)
                curses.endwin()

        return wrapper

    return wrapper
