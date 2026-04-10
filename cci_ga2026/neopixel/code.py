# Circuit Playground NeoPixel
# tested with CircuitPython 9.x 

# Neopixel Introduction
import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=False)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
OFF = (0, 0, 0)

while True:
    # Filling all the pixels with one color
    pixels.fill(CYAN)
    pixels.show()
    time.sleep(1)
    pixels.fill(OFF)
    pixels.show()
    time.sleep(1)


    # Addressing specific pixels
#     pixels[0] = CYAN
#     pixels[1] = RED
#     pixels.show()
#     time.sleep(1)
    
    
  