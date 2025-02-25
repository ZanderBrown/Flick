import flicklib
import time
import curses
from curses import wrapper

some_value = 5000

@flicklib.move()
def move(x, y, z):
    global xyztxt
    xyztxt = '{:5.3f} {:5.3f} {:5.3f}'.format(x,y,z)

@flicklib.flick()
def flick(start,finish):
    global flicktxt
    flicktxt = start + ' - ' + finish

@flicklib.airwheel()
def spinny(delta):
    global some_value
    global airwheeltxt
    some_value += delta
    if some_value < 0:
        some_value = 0
    if some_value > 10000:
        some_value = 10000
    airwheeltxt = str(some_value/100)

@flicklib.double_tap()
def doubletap(position):
    global doubletaptxt
    doubletaptxt = position

@flicklib.tap()
def tap(position):
    global taptxt
    taptxt = position

@flicklib.touch()
def touch(position):
    global touchtxt
    touchtxt = position


#
# Main display using curses
#


def real_main(stdscr):
    global xyztxt
    global flicktxt
    global airwheeltxt
    global touchtxt
    global taptxt
    global doubletaptxt

    xyztxt = ''
    flicktxt = ''
    flickcount = 0
    airwheeltxt = ''
    airwheelcount = 0
    touchtxt = ''
    touchcount = 0
    taptxt = ''
    tapcount = 0
    doubletaptxt = ''
    doubletapcount = 0

    # Clear screen and hide cursor
    stdscr.clear()
    curses.curs_set(0)

    # Add title and footer
    exittxt = 'Control-C to exit'
    title = '**** Flick Demo ****'
    stdscr.addstr( 0, (curses.COLS - len(title)) // 2, title)
    stdscr.addstr(22, (curses.COLS - len(exittxt)) // 2, exittxt)
    stdscr.refresh()

    fw_info = flicklib.getfwinfo()

    datawin = curses.newwin( 8, curses.COLS - 6,  2, 3)
    fwwin   = curses.newwin(10, curses.COLS - 6, 11, 3)

    # Fill firmware info window.
    fwwin.erase()
    fwwin.border()
    fwwin.addstr(1, 2, 'Firmware valid: ' + 'Yes' if fw_info['FwValid'] == 0xaa else 'No')
    fwwin.addstr(2, 2, 'Hardware Revison: ' + str(fw_info['HwRev'][0]) + '.' + str(fw_info['HwRev'][1]))
    fwwin.addstr(3, 2, 'Params Start Addr: ' + '0x{:04x}'.format(fw_info['ParamStartAddr']))
    fwwin.addstr(4, 2, 'Library Loader Version: ' + str(fw_info['LibLoaderVer'][0]) + '.' + str(fw_info['LibLoaderVer'][1]))
    fwwin.addstr(5, 2, 'Library Loader Platform: ' + 'Hillstar' if fw_info['LibLoaderPlatform'] == 21 else 'Woodstar')
    fwwin.addstr(6, 2, 'Firmware Start Addr: 0x' + '{:04x}'.format(fw_info['FwStartAddr']))
    fwver_part1, fwver_part2 = fw_info['FwVersion'].split(';DSP:')
    fwwin.addstr(7, 2, 'Firmware Version: ' + fwver_part1)
    fwwin.addstr(8, 2, 'DSP: ' + fwver_part2)
    fwwin.refresh()

    # Update data window continuously until Control-C
    while True:
        datawin.erase()
        datawin.border()
        datawin.addstr(1, 2, 'X Y Z     : ' + xyztxt)
        datawin.addstr(2, 2, 'Flick     : ' + flicktxt)
        datawin.addstr(3, 2, 'Airwheel  : ' + airwheeltxt)
        datawin.addstr(4, 2, 'Touch     : ' + touchtxt)
        datawin.addstr(5, 2, 'Tap       : ' + taptxt)
        datawin.addstr(6, 2, 'Doubletap : ' + doubletaptxt)
        datawin.refresh()

        xyztxt = ''

        if len(flicktxt) > 0 and flickcount < 5:
            flickcount += 1
        else:
            flicktxt = ''
            flickcount = 0

        if len(airwheeltxt) > 0 and airwheelcount < 5:
            airwheelcount += 1
        else:
            airwheeltxt = ''
            airwheelcount = 0

        if len(touchtxt) > 0 and touchcount < 5:
            touchcount += 1
        else:
            touchtxt = ''
            touchcount = 0

        if len(taptxt) > 0 and tapcount < 5:
            tapcount += 1
        else:
            taptxt = ''
            tapcount = 0

        if len(doubletaptxt) > 0 and doubletapcount < 5:
            doubletapcount += 1
        else:
            doubletaptxt = ''
            doubletapcount = 0

        time.sleep(0.1)


def main() -> None:
    wrapper(real_main)


if __name__ == "__main__":
    main()
