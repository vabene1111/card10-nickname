import utime
import display
import leds
import ledfx
import buttons
import light_sensor
import ujson
import os
import personal_state

FILENAME = 'nickname.txt'
FILENAME_ADV = 'nickname.json'
ANIM_TYPES = ['none', 'led', 'fade', 'gay', 'rainbow', 'rnd_led']
LINE_POSYS = [[30], [18, 42], [4, 28, 52], [0, 20, 40, 60]]

PERSONAL_STATES = [
    personal_state.NO_STATE, personal_state.NO_CONTACT,
    personal_state.CHAOS, personal_state.COMMUNICATION,
    personal_state.CAMP
]


def cycle_personal_state():
    state, _ = personal_state.get()
    state_i = PERSONAL_STATES.index(state)
    state_i += 1
    if state_i >= len(PERSONAL_STATES):
        state_i = 0
    personal_state.set(PERSONAL_STATES[state_i], True)


def wheel(pos):
    """
    Taken from https://badge.team/projects/rainbow_name
    Input a value 0 to 255 to get a color value.
    The colours are a transition r - g - b - back to r.
    :param pos: input position
    :return: rgb value
    """
    if pos < 0:
        return 0, 0, 0
    if pos > 255:
        pos -= 255
    if pos < 85:
        return int(255 - pos * 3), int(pos * 3), 0
    if pos < 170:
        pos -= 85
        return 0, int(255 - pos * 3), int(pos * 3)
    pos -= 170
    return int(pos * 3), 0, int(255 - (pos * 3))


def random_rgb():
    """
    Generates a random RGB value
    :return: RGB array
    """
    rgb = []
    for i in range(0, 3):
        rand = int.from_bytes(os.urandom(1), 'little')
        if rand > 255:
            rand = 255
        rgb.append(rand)
    return rgb


def blink_led(led):
    """
    Turns off leds, blinks given led for 100ms
    can be used as an indicator
    :param led: led to blink
    """
    leds.clear()
    utime.sleep(0.1)
    leds.set(led, [255, 0, 0])
    utime.sleep(0.1)
    leds.clear()


def render_error(err1, err2):
    """
    Function to render two lines of text (each max 11 chars). Useful to display error messages
    :param err1: line one
    :param err2: line two
    """
    with display.open() as disp:
        disp.clear()
        disp.print(err1, posx=80 - round(len(err1) / 2 * 14), posy=18)
        disp.print(err2, posx=80 - round(len(err2) / 2 * 14), posy=42)
        disp.update()
        disp.close()


def get_bat_color(bat):
    """
    Function determines the color of the battery indicator. Colors can be set in config.
    Voltage threshold's are currently estimates as voltage isn't that great of an indicator for
    battery charge.
    :param bat: battery config tuple (boolean: indicator on/off, array: good rgb, array: ok rgb, array: bad rgb)
    :return: false if old firmware, RGB color array otherwise
    """
    try:
        v = os.read_battery()
        if v > 3.8:
            return bat[1]
        if v > 3.6:
            return bat[2]
        return bat[3]
    except AttributeError:
        return False


def render_battery(disp, bat):
    """
    Adds the battery indicator to the display. Does not call update or clear so it can be used in addition to
    other display code.
    :param disp: open display
    :param bat: battery config tuple (boolean: indicator on/off, array: good rgb, array: ok rgb, array: bad rgb)
    """
    c = get_bat_color(bat)
    if not c:
        return
    disp.rect(140, 2, 155, 9, filled=True, col=c)
    disp.rect(155, 4, 157, 7, filled=True, col=c)


def get_time():
    """
    Generates a nice timestamp in format hh:mm:ss from the devices localtime
    :return: timestamp
    """
    timestamp = ''
    if utime.localtime()[3] < 10:
        timestamp = timestamp + '0'
    timestamp = timestamp + str(utime.localtime()[3]) + ':'
    if utime.localtime()[4] < 10:
        timestamp = timestamp + '0'
    timestamp = timestamp + str(utime.localtime()[4]) + ':'
    if utime.localtime()[5] < 10:
        timestamp = timestamp + '0'
    timestamp = timestamp + str(utime.localtime()[5])
    return timestamp


def toggle_rockets(state):
    """
    Turns all rocked LEDs on or off.
    :param state: True=on, False=off
    """
    brightness = 15
    if not state:
        brightness = 0
    leds.set_rocket(0, brightness)
    leds.set_rocket(1, brightness)
    leds.set_rocket(2, brightness)


def render_nickname(title, sub, fg, bg, fg_sub, bg_sub, main_bg, mode, bat):
    """
    Main function to render the nickname on screen.
    Pretty ugly but not time for cleanup right now (and some APIs missing)
    :param title: first row of text
    :param sub: second row of text
    :param fg: tuple of (day, night) rgb for title text color
    :param bg: tuple of (day, night) rgb for title background color
    :param fg_sub: tuple of (day, night) rgb for subtitle text color
    :param bg_sub: tuple of (day, night) rgb for subtitle background color
    :param main_bg: tuple of (day, night) rgb for general background color
    :param mode: default animation to start in (index of ANIM_TYPES array)
    :param bat: battery config tuple (boolean: indicator on/off, array: good rgb, array: ok rgb, array: bad rgb)
    """
    anim = mode
    r = 255
    g = 0
    b = 0
    rainbow_led_pos = 0
    last_btn_poll = utime.time() - 2
    while True:
        sleep = 0.5
        r_sub = sub.copy()
        for i, line in enumerate(sub):
            if line == '#time':
                r_sub[i] = get_time()
        dark = 0
        if light_sensor.get_reading() < 30:
            dark = 1
        r_fg_color = fg[dark]
        r_bg_color = bg[dark]
        r_fg_sub_color = fg_sub[dark]
        r_bg_sub_color = bg_sub[dark]
        r_bg = main_bg[dark]
        # Button handling
        pressed = buttons.read(
            buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT | buttons.TOP_RIGHT
        )
        if utime.time() - last_btn_poll >= 1:
            last_btn_poll = utime.time()
            if pressed & buttons.BOTTOM_RIGHT != 0:
                anim = anim + 1
                if anim >= len(ANIM_TYPES):
                    anim = 0
                blink_led(0)
            if pressed & buttons.BOTTOM_LEFT != 0:
                anim = anim - 1
                if anim < 0:
                    anim = len(ANIM_TYPES) - 1
                blink_led(0)
            if pressed & buttons.TOP_RIGHT:
                cycle_personal_state()
        # Animations
        if ANIM_TYPES[anim] == 'fade':
            sleep = 0.1
            leds.clear()
            toggle_rockets(False)
            if r > 0 and b == 0:
                r -= 1
                g += 1
            if g > 0 and r == 0:
                g -= 1
                b += 1
            if b > 0 and g == 0:
                r += 1
                b -= 1
            r_bg = [r, g, b]
            r_bg_color = r_bg
            r_bg_sub_color = r_bg
        if ANIM_TYPES[anim] == 'led':
            if dark == 1:
                for i in range(0, 11):
                    leds.prep(i, r_bg)
                leds.update()
                leds.dim_top(4)
                toggle_rockets(True)
            else:
                leds.clear()
                toggle_rockets(False)
        if ANIM_TYPES[anim] == 'rnd_led':
            if dark == 1:
                for i in range(0, 11):
                    leds.prep(i, random_rgb())
                leds.update()
                leds.dim_top(4)
                toggle_rockets(True)
            else:
                leds.clear()
                toggle_rockets(False)
        if ANIM_TYPES[anim] == 'gay':
            toggle_rockets(False)
            leds.gay(0.4)
        if ANIM_TYPES[anim] == 'rainbow':
            for i in range(0, 11):
                lr, lg, lb = wheel(rainbow_led_pos + i * 3)
                leds.prep(i, [lr, lg, lb])
            rainbow_led_pos += 1
            if rainbow_led_pos > 255:
                rainbow_led_pos = 0
            leds.update()
            leds.dim_top(3)
            toggle_rockets(True)
        if ANIM_TYPES[anim] == 'none':
            leds.clear()
            toggle_rockets(False)
        with display.open() as disp:
            disp.rect(0, 0, 160, 80, col=r_bg, filled=True)
            if bat[0]:
                render_battery(disp, bat)
            num_lines = len(title) + len(r_sub)
            posys = LINE_POSYS[num_lines - 1]
            i = 0
            for line in title:
                disp.print(line, fg=r_fg_color, bg=r_bg_color, posx=80 -
                                                                    round(len(line) / 2 * 14), posy=posys[i])
                i += 1
            for line in r_sub:
                disp.print(line, fg=r_fg_sub_color, bg=r_bg_sub_color,
                           posx=80 - round(len(line) / 2 * 14), posy=posys[i])
                i += 1
            disp.update()
            disp.close()
        utime.sleep(sleep)


def get_key(json, key, default):
    """
    Gets a defined key from a json object or returns a default if the key cant be found
    :param json: json object to search key in
    :param key: key to search for
    :param default: default to return if no key is found
    :return:
    """
    try:
        return json[key]
    except KeyError:
        return default


def split_lines(line, maxlen):
    """
    Split a long line into multiple lines
    Splits at spaces only, the space where split is removed. Stripping off of
    further spaces at start and end is deliberately not done to allow
    creativity even without explicit multi-lines.
    :param line: line to split
    :param maxlen: maximum line length in result
    :return: A list of lines fitting within the maximum
    """
    lines = []
    left = line
    while len(left) > maxlen:
        found = False
        for i in range(maxlen, 0, -1):
            if left[i] == ' ':
                lines.append(left[0:i])
                left = left[i + 1:]
                found = True
                break
        if not found:
            lines.append(left[0:maxlen])
            left = left[maxlen:]
    if left:
        lines.append(left)
    return lines


leds.clear()
if FILENAME_ADV in os.listdir("."):
    f = open(FILENAME_ADV, 'r')
    try:
        c = ujson.loads(f.read())
        f.close()
        # parse config
        nick = get_key(c, 'nickname', 'no nick')
        if isinstance(nick, str):
            nick = split_lines(nick, 11)[0:4]
        sub = get_key(c, 'subtitle', [])
        if isinstance(sub, str):
            sub = split_lines(sub, 11)[0:4]
        mode = get_key(c, 'mode', 0)
        # battery
        battery_show = get_key(c, 'battery', True)
        battery_c_good = get_key(c, 'battery_color_good', [0, 230, 00])
        battery_c_ok = get_key(c, 'battery_color_ok', [255, 215, 0])
        battery_c_bad = get_key(c, 'battery_color_bad', [255, 0, 0])
        # daytime values
        background = get_key(c, 'background', [0, 0, 0])
        fg_color = get_key(c, 'fg_color', [255, 255, 255])
        bg_color = get_key(c, 'bg_color', background)
        fg_sub_color = get_key(c, 'fg_sub_color', [255, 255, 255])
        bg_sub_color = get_key(c, 'bg_sub_color', background)
        # nighttime values
        background_night = get_key(c, 'background_night', [0, 0, 0])
        fg_color_night = get_key(c, 'fg_color_night', [255, 255, 255])
        bg_color_night = get_key(c, 'bg_color_night', background_night)
        fg_sub_color_night = get_key(c, 'fg_sub_color_night', [255, 255, 255])
        bg_sub_color_night = get_key(c, 'bg_sub_color_night', background_night)
        # render nickname
        render_nickname(nick, sub, (fg_color, fg_color_night), (bg_color, bg_color_night),
                        (fg_sub_color, fg_sub_color_night), (bg_sub_color, bg_sub_color_night),
                        (background, background_night), mode,
                        (battery_show, battery_c_good, battery_c_ok, battery_c_bad))
    except ValueError:
        render_error('invalid', 'json')
elif FILENAME not in os.listdir("."):
    render_error('file not', 'found')
else:
    f = open(FILENAME, 'r')
    nick = f.read()
    f.close()
    nick = split_lines(nick, 11)
    if len(nick) > 4:
        render_error('name too', 'long')
    elif not nick:
        render_error('nick file', 'empty')
    else:
        render_nickname(nick, [], ([255, 255, 255], [255, 255, 255]), ([0, 0, 0], [0, 0, 0]),
                        ([255, 255, 255], [255, 255, 255]), ([0, 0, 0], [0, 0, 0]), ([0, 0, 0], [0, 0, 0]), 1,
                        (True, [0, 230, 00], [255, 215, 0], [255, 0, 0]))
