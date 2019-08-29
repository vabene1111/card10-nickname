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
ANIM_TYPES = ['none', 'led', 'fade', 'gay', 'rainbow', 'rnd_led']


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


def render_nickname(title):
    with display.open() as disp:
        disp.print(title)
        disp.update()
        disp.close()


leds.clear()
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
        render_nickname(nick)
