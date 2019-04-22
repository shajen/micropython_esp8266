import math

def hsvToRgb(hsv):
    (hue, sat, val) = hsv
    if val == 0:
        return (0, 0, 0)
    else:
        hue = hue / 60
        i = math.floor(hue)
        f = hue - i;
        p = val * (1 - sat)
        q = val * (1 - (sat * f))
        t = val * (1 - (sat * (1 - f)))
        val = round(val * 255)
        t = round(t * 255)
        p = round(p * 255)
        q = round(q * 255)
        if i == 0:
            return (val, t, p)
        elif i == 1:
            return (q, val, p)
        elif i == 2:
            return (p, val, t)
        elif i == 3:
            return (p, q, val)
        elif i == 4:
            return (t, p, val)
        elif i == 5:
            return (val, p, q)
    return (255, 255, 255)
