def lcd(ser, txt):
    ser.write(txt)

def xlcd(ser, cmd):
    lcd(ser, cmd.decode("hex"))

def lcd_wrap_on(ser):
    xlcd(ser, "fe43")

def lcd_wrap_off(ser):
    xlcd(ser, "fe44")

def lcd_gohome(ser):
    xlcd(ser, "fe48")

def lcd_cls(ser):
    xlcd(ser, "fe58")

def lcd_clr(ser):
    lcd_cls(ser)
    lcd_gohome(ser)

def lcd_bgcolor(ser, c):
    xlcd(ser, "fed0")
    xlcd(ser, c)

def lcd_red(ser):
    lcd_bgcolor(ser, "ff0000")

def lcd_green(ser):
    lcd_bgcolor(ser, "00ff00")

def lcd_blue(ser):
    lcd_bgcolor(ser, "8080ff")

def lcd_dark_green(ser):
    lcd_bgcolor(ser, "008000")

def lcd_dark_blue(ser):
    lcd_bgcolor(ser, "000080")

def lcd_green_red(ser):
    lcd_bgcolor(ser, "ffff00")

def lcd_blue_red(ser):
    lcd_bgcolor(ser, "ff80ff")
