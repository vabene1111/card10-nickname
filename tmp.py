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
import light_sensor
import ujson
import os

while True:
    r = 255
    g = 0
    b = 0
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
    print(r_bg)
    with display.open() as disp:
        disp.clear()
        disp.rect(0, 0, 160, 80, col=r_bg, filled=True)
        disp.update()
        disp.close()
    utime.sleep(1)
