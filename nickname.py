"""
Improvement ideas
- animations
    - dvd
    - rainbow
    - led control
    - fade effekt
- led nick writing
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
ANIM_TYPES = ['none', 'led', 'fade']


def render_error(err1, err2):
    with display.open() as disp:
        disp.clear()
        disp.print(err1, posx=80 - round(len(err1) / 2 * 14), posy=18)
        disp.print(err2, posx=80 - round(len(err2) / 2 * 14), posy=42)
        disp.update()
        disp.close()


def render_nickname(title, sub, fg, bg, fg_sub, bg_sub, main_bg):
    anim = 'led'
    posy = 30
    if sub != '':
        posy = 18
    r = 255
    g = 0
    b = 0
    while True:
        dark = 0
        if light_sensor.get_reading() < 30:
            dark = 1
        r_fg_color = fg[dark]
        r_bg_color = bg[dark]
        r_fg_sub_color = fg_sub[dark]
        r_bg_sub_color = bg_sub[dark]
        r_bg = main_bg[dark]
        if anim == 'fade':
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
        if anim == 'led':
            for i in range(0, 11):
                leds.prep(i, r_bg)
            leds.update()
            leds.dim_top(3)
            leds.set_rocket(0, 15)
            leds.set_rocket(1, 15)
            leds.set_rocket(2, 15)
        if anim == 'none':
            leds.clear()
            leds.set_rocket(0, 0)
            leds.set_rocket(1, 0)
            leds.set_rocket(2, 0)
        with display.open() as disp:
            disp.rect(0, 0, 160, 80, col=r_bg, filled=True)
            disp.print(title, fg=r_fg_color, bg=r_bg_color, posx=80 - round(len(title) / 2 * 14), posy=posy)
            if sub != '':
                disp.print(sub, fg=r_fg_sub_color, bg=r_bg_sub_color, posx=80 - round(len(sub) / 2 * 14), posy=42)
            disp.update()
            disp.close()
        pressed = buttons.read(
            buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT
        )
        if pressed & buttons.BOTTOM_LEFT != 0:
            anim = ANIM_TYPES[1]
        if pressed & buttons.BOTTOM_RIGHT != 0:
            anim = ANIM_TYPES[0]
        utime.sleep(0.3)


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
                        (background, background_night))
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
