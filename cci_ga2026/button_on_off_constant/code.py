# CPX Buton On/Off Constant 
# Tested with CircuitPython 9.x
# Uses the 2 buttons on the CircuitPlayground Express to turn the LED on and off. 
# Button A turns it on, Button B turns it off. 
# This constantly updates the value on each loop run. 

import time
import board
import digitalio

led = digitalio.DigitalInOut(board.D13)
led.switch_to_output()

button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_a.switch_to_input(pull=digitalio.Pull.DOWN)
button_b.switch_to_input(pull=digitalio.Pull.DOWN)

while True:
    if button_a.value:
        led.value = True
    if button_b.value: 
        led.value = False

    time.sleep(0.1)
