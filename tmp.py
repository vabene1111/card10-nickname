import display

with display.open() as disp:
    disp.clear()
    disp.rect(0, 0, 160, 80, col=[255,255,255], filled=True)
    disp.rect(140, 1, 155, 8, filled=True, col=[255, 0, 0])
    disp.rect(155, 3, 157, 6, filled=True, col=[255, 0, 0])
    disp.update()
