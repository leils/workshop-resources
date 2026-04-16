import time 
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

button = digitalio.DigitalInOut(board.BUTTON_A)
button.switch_to_input(pull=digitalio.Pull.DOWN)

last_hello = time.time()
seconds_between_hellos = 5

while True:
    now = time.time()
    if (now - last_hello > seconds_between_hellos):
        print("hello")
        last_hello = now
    
    if (button.value):
        led.value = True
    else: 
        led.value = False