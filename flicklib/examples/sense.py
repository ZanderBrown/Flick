import sys
import time

import flicklib

try:
    from sense_hat import SenseHat
except ImportError:
    exit("This library requires the SenseHAT module")

some_value = 5000

sense = SenseHat()
# This function is used to show the gesture pictures on the Sense HAT
def show_image(gesture, value):
    cangles = [0, 90, 180, 270]     # Clockwise angles
    ccangles = [270, 180, 90, 0]    # Counterclockwise angles
    b = (0, 0, 255)     # Blue
    c = (0, 255, 255)   # Cyan
    g = (0, 255, 0)     # Green
    n = (0, 0, 0)       # Black

    # Wheel picture
    wheel = [
        n, n, n, b, g, n, n, n,
        n, b, n, n, n, n, g, n,
        n, n, n, n, n, n, n, n,
        b, n, n, n, n, n, n, g,
        g, n, n, n, n, n, n, g,
        n, n, n, n, n, n, n, n,
        n, g, n, n, n, n, g, n,
        n, n, n, g, g, n, n, n
    ]

    # Arrow picture
    flick = [
        n, n, n, n, b, n, n, n,
        n, n, n, n, n, b, n, n,
        n, n, n, n, n, n, b, n,
        b, b, b, b, b, b, b, b,
        n, n, n, n, n, n, b, n,
        n, n, n, n, n, b, n, n,
        n, n, n, n, b, n, n, n,
        n, n, n, n, n, n, n, n
    ]

    # Thick bar picture
    touch = [
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        c, c, c, c, c, c, c, c,
        b, b, b, b, b, b, b, b
    ]

    # Thick spot picture
    touchc = [
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, c, c, n, n, n,
        n, n, c, b, b, c, n, n,
        n, n, c, b, b, c, n, n,
        n, n, n, c, c, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n
    ]

    # Thin bar picture
    tap = [
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        g, g, g, g, g, g, g, g
    ]

    # Spot picture
    tapc = [
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, g, g, n, n, n,
        n, n, n, g, g, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n
    ]

    # Decide which picure to show based on gesture and value received
    # Track a finger adapting Flick coordinates to match the Sense HAT grid
    # The Z dimension changes the brightness of the LEDs
    if gesture == 'xyz':
        sx = int(round((value[0]*10)*7/10))
        sy = 7- int(round((value[1]*10)*7/10))
        sc = int(round((value[2]*100)*255/100))
        sense.set_pixel(sx, sy, (255 - sc, 255 - sc, 255 - sc))

    # Shows an arrow
    elif gesture == 'flick':
        sense.set_pixels(flick)
        if value == 'west - east':
            sense.set_rotation(0)
        elif value == 'east - west':
            sense.set_rotation(180)
        elif value == 'south - north':
            sense.set_rotation(270)
        elif value == 'north - south':
            sense.set_rotation(90)

    # Shows a rotating circle
    elif gesture == 'airwheel':
        delay = 0.3
        sense.set_pixels(wheel)
        if value == 'clock':            # Clockwise
            for r in cangles:
                sense.set_rotation(r)
                time.sleep(delay)
        else:                           # Counterclockwise
            for r in ccangles:
                sense.set_rotation(r)
                time.sleep(delay)

    # Shows a blinking bar. Uses only one picture for the cardinal directions and simply rotate accordingly
    elif gesture == 'doubletap':
        rep = 3                         # Number of times the bar blinks
        delay = 0.2                     # Delay in seconds between blinks
        if value == 'east':
            for i in range(rep):
                time.sleep(delay)
                sense.clear()
                time.sleep(delay)
                sense.set_pixels(tap)
                sense.set_rotation(270)
        elif value == 'west':
            for i in range(rep):
                time.sleep(delay)
                sense.clear()
                time.sleep(delay)
                sense.set_pixels(tap)
                sense.set_rotation(90)
        elif value == 'south':
            for i in range(rep):
                time.sleep(delay)
                sense.clear()
                time.sleep(delay)
                sense.set_pixels(tap)
                sense.set_rotation(0)
        elif value == 'north':
            for i in range(rep):
                time.sleep(delay)
                sense.clear()
                time.sleep(delay)
                sense.set_pixels(tap)
                sense.set_rotation(180)
        elif value == 'center':
            for i in range(rep):
                time.sleep(delay)
                sense.clear()
                time.sleep(delay)
                sense.set_pixels(tapc)

    # Shows a thin bar. Uses only one picture for the cardinal directions and simply rotate accordingly
    elif gesture == 'tap':
        sense.set_pixels(tap)
        if value == 'east':
            sense.set_rotation(270)
        elif value == 'west':
            sense.set_rotation(90)
        elif value == 'south':
            sense.set_rotation(0)
        elif value == 'north':
            sense.set_rotation(180)
        elif value == 'center':
            sense.set_pixels(tapc)

    # Shows a thick bar. Uses only one picture for the cardinal directions and simply rotate accordingly
    elif gesture == 'touch':
        sense.set_pixels(touch)
        if value == 'east':
            sense.set_rotation(270)
        elif value == 'west':
            sense.set_rotation(90)
        elif value == 'south':
            sense.set_rotation(0)
        elif value == 'north':
            sense.set_rotation(180)
        elif value == 'center':
            sense.set_pixels(touchc)

@flicklib.move()
def move(x, y, z):
    global xyztxt
    global xyz
    xyztxt = '{:5.3f} {:5.3f} {:5.3f}'.format(x,y,z)
    xyz = (x, y, z)

@flicklib.flick()
def flick(start,finish):
    global flicktxt
    flicktxt = start + ' - ' + finish

@flicklib.airwheel()
def spinny(delta):
    global some_value
    global airwheeltxt
    global airwheel
    some_value += delta
    if some_value < 0:
        some_value = 0
    if some_value > 10000:
        some_value = 10000
    airwheeltxt = str(some_value/100)
    airwheel = delta

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


def real_main(argv: list[str]) -> None:

    global xyztxt
    global flicktxt
    global airwheeltxt
    global touchtxt
    global taptxt
    global doubletaptxt
    global xyz
    global airwheel

    xyztxt = ''
    flicktxt = ''
    airwheeltxt = ''
    touchtxt = ''
    taptxt = ''
    doubletaptxt = ''
    xyz = (0, 0, 0)
    airwheel  = 0

    message = "Flick demo"
    print(message)
    black = (0, 0, 0)
    orange = (255, 140, 0)
    speed = 0.05
    sense.show_message(message, speed, text_colour=orange, back_colour=black)

    # This loop prints on the screen the values coming from the events and keeps the program running until CTRL^C
    while True:
        if len(xyztxt) > 0:
            print('xyz: ' + xyztxt)
            show_image('xyz', xyz)
            xyztxt = ''
        if len(flicktxt) > 0:
            print('Flick: ' + flicktxt)
            show_image('flick', flicktxt)
            flicktxt = ''
        if len(airwheeltxt) > 0:
            print('Airwheel: ' + airwheeltxt)
            if airwheel >= 0:
                show_image('airwheel', 'clock')
            else:
                show_image('airwheel', 'cclock')
            airwheeltxt = ''
        if len(touchtxt) > 0:
            print('Touch: ' + touchtxt)
            show_image('touch', touchtxt)
            touchtxt = ''
        if len(taptxt) > 0:
            print('Tap: ' + taptxt)
            show_image('tap', taptxt)
            taptxt = ''
        if len(doubletaptxt) > 0:
            print('Double Tap: ' + doubletaptxt)
            show_image('doubletap', doubletaptxt)
            doubletaptxt = ''
        time.sleep(0.1)


# main
def main() -> None:
    if len(sys.argv) < 1:
        sys.exit("usage: {p:s}".format(p=sys.argv[0]))

    try:
        real_main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit("interrupted")


if "__main__" == __name__:
    main()
