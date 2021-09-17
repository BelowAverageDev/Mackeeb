# Mackeeb
2% macropad mechanical keyboard designed around macintosh keycaps  
![Finished project](https://imgur.com/a/Uj5SjoH)

## Usage
When you plug it in, the Mackeeb will run its main mode.

### Main mode
| Action                      | Result                        |
| ---                         | ---                           |
| Press Button 1              | Macro A                       |
| Press Button 2              | Macro B                       |
| Hold Button 1               | Macro C                       |
| Hold Button 2               | Macro D                       |
| Hold Button 1 & 2 together  | Switch to backlight set mode  |  

### Backlight set mode
| Action                      | Result                        |
| ---                         | ---                           |
| Press Button 1              | Increase Brightness           |
| Press Button 2              | Decrease Brightness           |
| Hold Button 1 & 2 together  | Switch to main mode           |

### Changing macros
To set Macro A-D, you need to put the device in config mode using the following steps:
1. Unplug the Mackeeb
2. Hold down Button 1 & 2 together
3. Plug in the Mackeeb
4. The underglow will begin flashing slowly. You may release Button 1 & 2
5. A new drive titled `CIRCUITPY` should appear on your computer
6. Open `CIRCUITPY/main.py` in any text editor
7. Modify `BUTTON_A_KEYS`, `BUTTON_B_KEYS`, `BUTTON_C_KEYS`, `BUTTON_D_KEYS` to your liking
8. Save `main.py`
9. Unplug and re-plug the Mackeeb

Note: These macros can be sequences of keystrokes, modifier keys, and combinations. For example, you can do a complex action like: `[[Keycode.COMMAND, Keycode.F], "search", Keycode.ENTER]` to search for a string, and then hit enter!

If your macros do not work as expected, you likely made an error. You can debug your macros by connecting to the trinket over a serial port, where any errors will be printed.

## Building your own

### Materials
- [Trinket m0](https://www.adafruit.com/product/3500?gclid=CjwKCAjwybyJBhBwEiwAvz4G77peeVcom4f-hD8dLuuwjS7zw9Dao5IvX-oa2v0OJsnX6UEL5DRNvxoCOocQAvD_BwE)
- [Macintosh keycaps](https://www.keebmonkey.com/products/keebmonkey-mac-modular-artisan-keycap?_pos=1&_sid=b556e45d8&_ss=r)
- 2x Mechanical keyswitches
- 3d printer (or access to one)
- 1x 3mm LED
- 1x Resistor (I used 200 ohm)
- Wire (recommend silicon coated for flexibility)
- Soldering iron
- Solder
- Flux
- MicroUSB cable

### Circuit
![Circuit Diagram](/diagram.svg)

Note that the switch connected on pin 3 will be the switch in the back, and the switch connected on pin 4 will be the switch in the front. Additionally, the LED should be put through the keyswitch before soldering.

### Assembly

#### Trinket setup
1. Install CircuitPy 7  
First, you want to load CircuitPy 7 onto the trinket. Be sure to download **CircuitPy 7**!  
[Upgrade Circuitpy](https://learn.adafruit.com/adafruit-trinket-m0-circuitpython-arduino/circuitpython)  

2. Install CircuitPy 7 Libraries  
Download the CircuitPy libraries required for this build, but **make sure you download the v7 library bundle**:
[Download](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries)
From this bundle we need:
    ```
    adafruit_hid
    adafruit_dotstar.mpy
    adafruit_pypixelbuf.mpy
    ```
Move these to `CIRCUITPY/lib`

3. Install Project Code  
Load the project code onto the trinket by moving `boot.py` and `main.py` to the `CIRCUITPY` drive that shows up when you plug in the trinket.


#### Soldering
Start by soldering all the wires you need to the trinket, making sure that the joints are flush with the bottom of the trinket.  
Next, place the trinket in the case with the wires sticking through the correct holes in the case.  
Then, solder the switches and led accoring to the diagram above.

TIP: Fitting the resistor can be a little tricky, so I soldered it between the LED ground lead and the rear switch ground lead in order to save space and prevent shorts.

Finally, test that the trinket is working with the switches

## Code
[About the code](code/README.md)
