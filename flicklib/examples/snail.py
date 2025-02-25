# Author: Russel Davis @ukscone

import flicklib
import time
import curses
from curses import wrapper


@flicklib.flick()
def flick(start,finish):
    global flicktxt
    global Xaxis
    global Yaxis
    flicktxt = start + ' - ' + finish
    if finish == "north":
        Yaxis -= 3
        if Yaxis < 0:
            Yaxis = 1
    elif finish == "south":
        Yaxis += 3
        if Yaxis > 19:
            Yaxis = 19
    elif finish == "east":
        Xaxis += 3
        if Xaxis > 39:
            Xaxis = 39
    elif finish == "west":
        Xaxis -= 3
        if Xaxis < 0:
            Xaxis = 1
    else:
        pass


#
# Main display using curses
#


def real_main(stdscr):
    global flicktxt
    global Xaxis
    global Yaxis
    flicktxt = ''

    # Clear screen and hide cursor
    stdscr.clear()
    curses.curs_set(0)

    # Add title and footer
    exittxt = 'Control-C to exit'
    title = '**** Flick Demo ****'
    stdscr.addstr( 0, (curses.COLS - len(title)) // 2, title)
    stdscr.addstr(22, (curses.COLS - len(exittxt)) // 2, exittxt)
    stdscr.refresh()

    datawin = curses.newwin( 8, curses.COLS - 6,  2, 3)
    fwwin   = curses.newwin(20, 41, 11, 3)

    # Fill firmware info window.
    fwwin.erase()
    fwwin.border()
    fwwin.refresh()

    Xaxis=20
    Yaxis=10

    # Update data window continuously until Control-C
    while True:
        datawin.erase()
        datawin.border()
        datawin.addstr(2, 2, 'Flick     : ' + flicktxt)
        datawin.refresh()
        fwwin.erase()
        fwwin.border()
        fwwin.addch(Yaxis,Xaxis,'@')
        fwwin.refresh()

        time.sleep(0.1)


def main() -> None:
    wrapper(real_main)


if __name__ == "__main__":
    main()
