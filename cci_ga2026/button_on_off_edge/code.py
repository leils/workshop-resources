# CPX Button On/Off Edge Detection 
# Uses the 2 buttons on the CircuitPlayground Express to turn the LED on and off. 
# Button A turns it on, Button B turns it off. 
# This uses edge detection to update the value on press. 

# tested with CircuitPython 9.x

import time
import board
import digitalio

led = digitalio.DigitalInOut(board.D13)
led.switch_to_output()

button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_a.switch_to_input(pull=digitalio.Pull.DOWN)
button_b.switch_to_input(pull=digitalio.Pull.DOWN)

a_lastvalue = False
b_lastvalue = False

while True:
    if button_a.value and not a_lastvalue:
        led.value = True
    if button_b.value and not b_lastvalue: 
        led.value = False

    a_lastvalue = button_a.value
    b_lastvalue = button_b.value

    time.sleep(0.1)
