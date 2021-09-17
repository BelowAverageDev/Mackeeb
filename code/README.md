# Code

### main.py
Contains the code controlling the keyswitch polling and handlers for keyswitch presses/depresses. Fully capitalized variable names are considered configuration variables and can be modified in config mode to your liking.

The following variables define user-modifyable configurations:  
| Variable               | Importance                                          |
| ---                    | ---                                                 |
| BUTTON_A_KEYS          | Macro executed on Button 1 press                    |
| BUTTON_B_KEYS          | Macro executed on Button 2 press                    |
| BUTTON_C_KEYS          | Macro executed on Button 1 hold                     |
| BUTTON_D_KEYS          | Macro executed on Button 2 hold                     |
| UNDERGLOW_BRIGHTNESS   | Brightness of case lighting                         |
| UNDERGLOW_COLOR        | Color of case lighting (rgb code or function)       |
| DELAY                  | Polling rate of device                              |
| MODE_CHANGE_HOLD_DELAY | Time for both buttons hold before mode change       |
| HOLD_DELAY             | Time for single button hold to execute Macro C or D |

This code can only be modified in config mode which you can enter by holding down both switches while the device is booting.

For example, setting `UNDERGLOW_BRIGHTNESS` to `1.0` will make the underglow very bright.

Note: You may notice this code is incredibly messy; this is out of necessity. The trinket only as 32kb of available memory and after all necessary libraries are imported, we are left with around 10kb. This would be fine for our uses, however this 10kb is very fragmented. Because CircuitPython offers no way to defragment the heap, we are stuck in this state.

[Learn more about CircuitPython](https://circuitpython.org/)

### boot.py
Defines custom boot behavior for CircuitPython which is required for access to the `storage` module. This project uses `storage` to allow CircuitPython to write data to a file (`led_val`) so that backlight level can be saved.

Additionally, this file disables the `CIRCUITPY` drive from showing up unless it is booting into comfig mode.

It is not recommended to modify this code because if something goes wrong, your trinket may not boot. You would then need to completely reset the trinket.

[Learn more about why we need `boot.py` and the `storage` module](https://learn.adafruit.com/circuitpython-essentials/circuitpython-storage)