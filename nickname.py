"""
Improvement ideas
- animations
    - dvd
    - rainbow
    - led control
    - fade effekt
- led nick writing
CA:4D:10
CA:4D:10:8f:40:fc
"""
import utime
import display
import leds
import ledfx
import buttons
import light_sensor
import ujson
import os

FILENAME = 'nickname.txt'
FILENAME_ADV = 'nickname.json'
ANIM_TYPES = ['none', 'led', 'fade', 'gay']


def render_error(err1, err2):
    with display.open() as disp:
        disp.clear()
        disp.print(err1, posx=80 - round(len(err1) / 2 * 14), posy=18)
        disp.print(err2, posx=80 - round(len(err2) / 2 * 14), posy=42)
        disp.update()
        disp.close()


def get_bat_color(bat):
    v = os.read_battery()
    if v > 3.9:
        return bat[1]
    if v > 3.6:
        return bat[2]
    return bat[3]


def render_battery(disp, bat):
    c = get_bat_color(bat)
    disp.rect(140, 2, 155, 9, filled=True, col=c)
    disp.rect(155, 4, 157, 7, filled=True, col=c)


def get_time():
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
    brightness = 15
    if not state:
        brightness = 0
    leds.set_rocket(0, brightness)
    leds.set_rocket(1, brightness)
    leds.set_rocket(2, brightness)


def render_nickname(title, sub, fg, bg, fg_sub, bg_sub, main_bg, mode, bat):
    anim = mode
    posy = 30
    if sub != '':
        posy = 18
    r = 255
    g = 0
    b = 0
    r_sub = sub
    last_btn_poll = utime.time() - 2
    while True:
        sleep = 0.5
        if sub == '#time':
            r_sub = get_time()
        dark = 0
        if light_sensor.get_reading() < 40:
            dark = 1
        r_fg_color = fg[dark]
        r_bg_color = bg[dark]
        r_fg_sub_color = fg_sub[dark]
        r_bg_sub_color = bg_sub[dark]
        r_bg = main_bg[dark]
        # Button handling
        pressed = buttons.read(
            buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT
        )
        if utime.time() - last_btn_poll >= 1:
            last_btn_poll = utime.time()
            if pressed & buttons.BOTTOM_RIGHT != 0:
                anim = anim + 1
                if anim >= len(ANIM_TYPES):
                    anim = 0
            if pressed & buttons.BOTTOM_LEFT != 0:
                anim = anim - 1
                if anim < 0:
                    anim = len(ANIM_TYPES) - 1
        # Animations
        if ANIM_TYPES[anim] == 'fade':
            sleep = 0.1
            leds.clear()
            toggle_rockets(False)
            if r > 0 and b == 0:
                r = r - 1
                g = g + 1
            if g > 0 and r == 0:
                g = g - 1
                b = b + 1
            if b > 0 and g == 0:
                r = r + 1
                b = b - 1
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
        if ANIM_TYPES[anim] == 'gay':
            toggle_rockets(False)
            leds.gay(0.4)
        if ANIM_TYPES[anim] == 'none':
            leds.clear()
            toggle_rockets(False)
        with display.open() as disp:
            disp.rect(0, 0, 160, 80, col=r_bg, filled=True)
            if bat[0]:
                render_battery(disp, bat)
            disp.print(title, fg=r_fg_color, bg=r_bg_color, posx=80 - round(len(title) / 2 * 14), posy=posy)
            if r_sub != '':
                disp.print(r_sub, fg=r_fg_sub_color, bg=r_bg_sub_color, posx=80 - round(len(r_sub) / 2 * 14), posy=42)
            disp.update()
            disp.close()
        utime.sleep(sleep)


def get_key(json, key, default):
    try:
        return json[key]
    except KeyError:
        return default


leds.clear()
with display.open() as disp:
    disp.clear().update()
    disp.close()
if FILENAME_ADV in os.listdir("."):
    f = open(FILENAME_ADV, 'r')
    try:
        c = ujson.loads(f.read())
        f.close()
        # parse config
        nick = get_key(c, 'nickname', 'no nick')
        sub = get_key(c, 'subtitle', '')
        mode = get_key(c, 'mode', 0)
        # battery
        battery_show = get_key(c, 'battery', True)
        battery_c_good = get_key(c, 'battery_color_good', [0, 230, 00])
        battery_c_ok = get_key(c, 'battery_color_ok', [255, 215, 0])
        battery_c_bad = get_key(c, 'battery_color_bad', [255,0,0])
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
else:
    if FILENAME not in os.listdir("."):
        render_error('file not', 'found')
    else:
        f = open(FILENAME, 'r')
        nick = f.read()
        f.close()
        if len(nick) > 11:
            render_error('name too', 'long')
        if len(nick) < 1:
            render_error('nick file', 'empty')
        else:
            render_nickname(nick, '', ([255, 255, 255], [255, 255, 255]), ([0, 0, 0], [0, 0, 0]),
                            ([255, 255, 255], [255, 255, 255]), ([0, 0, 0], [0, 0, 0]), ([0, 0, 0], [0, 0, 0]))
