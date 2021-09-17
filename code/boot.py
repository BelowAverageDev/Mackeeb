"""
boot.py

Executed when device boots

NOTE: Hold both switches to enter config mode
where you can view/edit this code!
"""

import board
from digitalio import DigitalInOut, Direction, Pull
import storage
import usb_cdc

# init switch_a
switch_a = DigitalInOut(board.D4)
switch_a.direction = Direction.INPUT
switch_a.pull = Pull.UP

# init switch_b
switch_b = DigitalInOut(board.D3)
switch_b.direction = Direction.INPUT
switch_b.pull = Pull.UP

# config mode if both switches are pressed on boot
config_mode = (not switch_a.value) and (not switch_b.value)

print("config_mode", config_mode)

# set writable in config mode
storage.remount("/", config_mode)

# If both switches are pressed
if config_mode:
    # config mode

    # enable usb drive
    storage.enable_usb_drive()
    # enable uart
    usb_cdc.enable()
else:
    # usage mode

    # disable usb drive
    storage.disable_usb_drive()
    # disable uart
    # usb_cdc.disable()

del config_mode
