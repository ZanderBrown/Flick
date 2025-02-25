import flicklib
import time
import curses
from curses import wrapper

# Requires sudo apt-get install python-alsaaudio
try:
    import alsaaudio 
except ImportError:
    exit("This library requires the alsaaudio module")

some_value = 5000

@flicklib.airwheel()
def spinny(delta):
    global some_value
    global airwheelint
    some_value += delta
    if some_value < 0:
        some_value = 0
    if some_value > 10000:
        some_value = 10000
    airwheelint = int(some_value/100)

#
# Main display using curses
#


def real_main(stdscr):
    global airwheelint

    airwheelint = 0

    # Clear screen and hide cursor
    stdscr.clear()
    curses.curs_set(0)

    # Add title and footer
    exittxt = 'Control-C to exit'
    errortxt = ''
    title = '**** Volume control ****'
    stdscr.addstr( 0, (curses.COLS - len(title)) // 2, title)
    stdscr.addstr(10, (curses.COLS - len(exittxt)) // 2, exittxt)
    stdscr.addstr(22, (0 - len(errortxt)) // 2, errortxt)
    stdscr.refresh()

    # Setup the mixer
    cardId = -1
    for i in range(len(alsaaudio.cards())):      # Find the JustBoom card
        if (alsaaudio.cards()[i] == 'sndrpiboomberry' or alsaaudio.cards()[i] == 'sndrpijustboomd'):
            card = 'JustBoom DAC'
            control = 'Digital'
            cardId = i
            break
    if cardId == -1:                             # JustBoom card not found
        for i in range(len(alsaaudio.cards())):  # Find the default onboard 'ALSA' card
            if (alsaaudio.cards()[i] == 'ALSA'):
                card = 'bcm2835 ALSA'
                control = 'PCM'
                cardId = i
                break
    if cardId == -1:
        exit("Compatible audio card not found")
    try:
        mixer = alsaaudio.Mixer(control=control, cardindex=cardId)
    except:
        exit("Compatible audio card not found")

    fwwin = curses.newwin(3, curses.COLS - 6, 1, 3)
    datawin = curses.newwin(4, curses.COLS - 6, 4, 3)

    # Fill firmware info window.
    fwwin.erase()
    fwwin.border()
    fwwin.addstr(1, 2, 'Selected Audio Card: ' + str(card))
    fwwin.refresh()
    # Update data window continuously until Control-C

    while True:
        datawin.erase()
        datawin.border()
        datawin.addstr(1, 2, 'Airwheel  : ' + str(airwheelint))
        datawin.addstr(2, 2, 'Volume  : ' + str(mixer.getvolume()))
        datawin.refresh()
        mixer.setvolume(airwheelint)

        time.sleep(0.1)


def main() -> None:
    wrapper(real_main)


if __name__ == "__main__":
    main()
