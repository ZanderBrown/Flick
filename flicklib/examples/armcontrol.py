import flicklib
import time
import curses
from curses import wrapper
import RobotArm

arm = RobotArm.RobotArm()

some_value = 5000

@flicklib.flick()
def flick(start,finish):
    global flicktxt
    flicktxt = start + ' - ' + finish
    if flicktxt == "south - north":
        arm.moveShoulder(1)
        time.sleep(1)
        arm.reset()

    if flicktxt == "north - south":
        arm.moveShoulder(2)
        time.sleep(1)
        arm.reset()

    if flicktxt == "west - east":
        arm.moveElbow(1)
        time.sleep(1)
        arm.reset()

    if flicktxt == "east - west":
        arm.moveElbow(2)
        time.sleep(1)
        arm.reset()


@flicklib.airwheel()
def spinny(delta):
    global some_value
    global airwheeltxt
    some_value += delta

    if delta < 0:
        arm.moveBase(2)
        time.sleep(0.5)
    arm.reset()
    if delta > 0:
	    arm.moveBase(1)
	    time.sleep(0.5)
    arm.reset()
    if some_value < 0:
        some_value = 0
    if some_value > 10000:
        some_value = 10000
    airwheeltxt = str(some_value/100)

@flicklib.double_tap()
def doubletap(position):
    global doubletaptxt
    doubletaptxt = position
    arm.toggleLight()   
    time.sleep(1)

@flicklib.touch()
def touch(position):
    global touchtxt
    touchtxt = position
    while touchtxt == "north":
        arm.moveWrist(2)
    arm.reset()
    while touchtxt == "south":
        arm.moveWrist(1)
    arm.reset()
    while touchtxt == "west":
        arm.moveGrip(1)
    arm.reset()
    while touchtxt == "east":
        arm.moveGrip(2)
    arm.reset()


#
# Main display using curses
#


def real_main(stdscr) -> None:
    global flicktxt
    global airwheeltxt
    global touchtxt
    global doubletaptxt

    flicktxt = ''
    flickcount = 0
    airwheeltxt = ''
    airwheelcount = 0
    touchtxt = ''
    touchcount = 0
    doubletaptxt = ''
    doubletapcount = 0

    # Clear screen and hide cursor
    stdscr.clear()
    curses.curs_set(0)

    # Add title and footer
    exittxt = 'Control-C to exit'
    title = '**** Maplin Robotic Arm Control  ****'
    Instr = '**** Instructions ****'
    stdscr.addstr( 0, (curses.COLS - len(title)) // 2, title)
    stdscr.addstr( 9, (curses.COLS - len(exittxt)) // 2, exittxt)
    stdscr.addstr( 11, (curses.COLS - len(Instr)) // 2, Instr)
    stdscr.refresh()

    datawin = curses.newwin( 6, curses.COLS - 6,  2, 3)
    fwwin   = curses.newwin(14, curses.COLS - 6, 13, 3)

    # Fill firmware info window.
    fwwin.erase()
    fwwin.border()
    fwwin.addstr(1, 2, 'South - North Flick = Shoulder Back')
    fwwin.addstr(2, 2, 'North - South Flick = Shoudler Forward')
    fwwin.addstr(3, 2, '  West - East Flick = Elbow Back')
    fwwin.addstr(4, 2, '  East - West Flick = Elbow Forward')
    fwwin.addstr(5, 2, '        CW Airwheel = Base Rotate CW')
    fwwin.addstr(6, 2, '       CCW Airwheel = Base Rotate CCW')
    fwwin.addstr(7, 2, '         Double Tap = Light On')
    fwwin.addstr(8, 2, '                Tap = Light Off')
    fwwin.addstr(9, 2, '          South Tap = Wrist Back')
    fwwin.addstr(10, 2, '          North Tap = Wrist Forward')
    fwwin.addstr(11, 2, '           West Tap = Grip Close')
    fwwin.addstr(12, 2, '           East Tap = Grip Open')
    fwwin.refresh()

    # Update data window continuously until Control-C
    while True:
        datawin.erase()
        datawin.border()
        datawin.addstr(1, 2, 'Flick     : ' + flicktxt)
        datawin.addstr(2, 2, 'Airwheel  : ' + airwheeltxt)
        datawin.addstr(3, 2, 'Touch     : ' + touchtxt)
        datawin.addstr(4, 2, 'Doubletap : ' + doubletaptxt)
        datawin.refresh()


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
