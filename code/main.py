import gc
from adafruit_hid.keyboard import Keyboard, Keycode
def main_loop(led_mode):
    a_ign_release = False
    b_ign_release = False
    a_hold_revs = 0
    b_hold_revs = 0

    switch_a_pressed = False
    switch_b_pressed = False

    # if static color, just set here
    if not callable(UNDERGLOW_COLOR):
        dot[0] = UNDERGLOW_COLOR

    # regular mode, switch to led set mode if possible
    set_led_mode = False

    i = 0
    while True:
        if callable(UNDERGLOW_COLOR):
            # set dot to non-static color
            dot[0] = UNDERGLOW_COLOR(i & 255)

        switch_a_pressed = not switch_a.value
        switch_b_pressed = not switch_b.value

        if switch_a_pressed:
            a_hold_revs += 1
            if a_hold_revs == HOLD_DELAY_REVS and not switch_b_pressed and not set_led_mode:
                print("C pressed")
                send_keys(BUTTON_C_KEYS)
                gc.collect()
                a_ign_release = True
        elif a_hold_revs:
            if a_ign_release:
                # ignore this press (recover from changing mode)
                a_ign_release = False
            else:
                if set_led_mode:
                    # change led by 1
                    if led_mode < len(LED_MODES) - 1:
                        led_mode += 1
                    print("LED_MODE:", led_mode)
                    led.value = LED_MODES[led_mode]
                else:
                    # button released, send keystroke
                    if a_hold_revs < HOLD_DELAY_REVS:
                        print("A pressed")
                        send_keys(BUTTON_A_KEYS)
                        gc.collect()
            a_hold_revs = 0

        if switch_b_pressed:
            b_hold_revs += 1
            if b_hold_revs == HOLD_DELAY_REVS  and not switch_a_pressed and not set_led_mode:
                print("D pressed")
                send_keys(BUTTON_D_KEYS)
                gc.collect()
                b_ign_release = True
        elif b_hold_revs:
            if b_ign_release:
                # ignore this press (recover from changing mode)
                b_ign_release = False
            else:
                if set_led_mode:
                    # change led by 1
                    if led_mode != 0:
                        led_mode -= 1
                    print("LED_MODE:", led_mode)
                    led.value = LED_MODES[led_mode]
                else:
                    # button released, send keystroke
                    if b_hold_revs < HOLD_DELAY_REVS:
                        print("B pressed")
                        send_keys(BUTTON_B_KEYS)
                        gc.collect()
            b_hold_revs = 0

        # check if we need to switch to light set mode
        if (switch_a_pressed and switch_b_pressed) and (
            min(a_hold_revs, b_hold_revs) == MODE_CHANGE_HOLD_DELAY_REVS
        ):
            print("LED_SET_MODE:", not set_led_mode)
            blink_val = max(LED_MODES[led_mode], LED_MODES[1])
            for _ in range(3):
                led.value = LED_MODES[0]
                sleep(0.1)
                led.value = blink_val
                sleep(0.1)
            
            led.value = LED_MODES[led_mode]

            if set_led_mode:
                # save value if in led_mode
                with open(LED_FILE, "w") as f:
                    f.write(str(led_mode))
                    f.flush()

            # swap between led and keyboard mode
            set_led_mode = not set_led_mode
            # ignore next keyup
            a_ign_release = b_ign_release = True


        i = (i + 1) % 256  # run from 0 to 255
        sleep(DELAY)

gc.collect()
print(gc.mem_free())

import adafruit_dotstar as dotstar
print(gc.mem_free())
import board
import usb_hid
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogOut
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from time import sleep

gc.collect()
print(gc.mem_free())

# NOTE: Try not to go crazy here, the memory is very fragmeneted
# and large strings may not work here
BUTTON_A_KEYS = ["Hello world!", Keycode.ENTER]
BUTTON_C_KEYS = [[Keycode.COMMAND, Keycode.F], "search", Keycode.ENTER]
BUTTON_B_KEYS = ["Hello I am a mackeeb! :) Please view my documentation to configure me!"]
BUTTON_D_KEYS = [[Keycode.ALT, Keycode.SHIFT, Keycode.H]]

# underglow brightness (0.0-1.0)
UNDERGLOW_BRIGHTNESS = 0.0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# underglow color (0,0,0)-(255,255,255)
# can be static or function depending on i
# 0 <= i <= 255
UNDERGLOW_COLOR = WHITE
# def UNDERGLOW_COLOR(i):
#     if i < 0:
#         return (0, 0, 0)
#     if i > 255:
#         return (0, 0, 0)
#     if i < 85:
#         return (int(i * 3), int(255 - (i * 3)), 0)
#     elif i < 170:
#         i -= 85
#         return (int(255 - i * 3), 0, int(i * 3))
#     else:
#         i -= 170
#         return (0, int(i * 3), int(255 - i * 3))

LED_FILE = "/led_val"
LED_MIN, LED_MAX = 65535 // 4 * 3, 65535
# set led modes list (modes 0-4) to a out values
LED_MODES = [i for i in range(LED_MIN, LED_MAX, (LED_MAX - LED_MIN) // 5)]
# set last mode to full voltage
LED_MODES[-1] = LED_MAX
# set first mode to 0 voltage
LED_MODES[0] = 0

# polling rates
DELAY = 0.001
MODE_CHANGE_HOLD_DELAY = 3
HOLD_DELAY = 1
MODE_CHANGE_HOLD_DELAY_REVS = round(MODE_CHANGE_HOLD_DELAY / DELAY / 10)
HOLD_DELAY_REVS = round(HOLD_DELAY / DELAY / 10)

# init kbd
kbd = Keyboard(usb_hid.devices)
kbd_layout = KeyboardLayoutUS(kbd)

# init dotstar (underglow RGB led)
dot = dotstar.DotStar(
    board.APA102_SCK, board.APA102_MOSI, 1, brightness=UNDERGLOW_BRIGHTNESS
)

# init led (backlight)
led = AnalogOut(board.D1)

# init switch_a
switch_a = DigitalInOut(board.D3)
switch_a.direction = Direction.INPUT
switch_a.pull = Pull.UP

# init switch_b
switch_b = DigitalInOut(board.D4)
switch_b.direction = Direction.INPUT
switch_b.pull = Pull.UP

led_mode = 0
try:
    with open(LED_FILE, "r") as f:
        led_mode = int(f.read()) % len(LED_MODES)
except Exception:
    pass

def send_keys(keys_list):
    for key in keys_list:
        if isinstance(key, str):
            kbd_layout.write(key)
        elif type(key) == list:
            kbd.send(*key)
        else:
            kbd.send(key)

led.value = LED_MODES[led_mode]


config_mode = 0
try:
    open(LED_FILE, "r+").close()

except OSError as e:
    config_mode = 1

print("config_mode:", config_mode)

if config_mode:
    # config mode
    dot.brightness = 0.5

    # blink white light
    while True:
        dot[0] = WHITE
        sleep(0.5)
        dot[0] = BLACK
        sleep(0.5)
else:
    main_loop(led_mode)
