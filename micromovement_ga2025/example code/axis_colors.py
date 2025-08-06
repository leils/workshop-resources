import board
import busio
import neopixel
import adafruit_lis3dh
import time

from adafruit_ht16k33.matrix import Matrix8x8x2

i2c = board.STEMMA_I2C()
matrix = Matrix8x8x2(i2c)


pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

matrix[0,0] = matrix.LED_GREEN

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G

# Loop forever printing accelerometer values
while True:
    # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
    # z axis values.  Divide them by 9.806 to convert to Gs.
    x, y, z = (value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration)
    print(f"x = {x:.3f} G, y = {y:.3f} G, z = {z:.3f} G")
    
    absValues = [abs(x), abs(y), abs(z)]
    maxValue = max(absValues)
    maxIndex = absValues.index(maxValue)
    
    if (maxIndex == 0):
            matrix.fill(matrix.LED_GREEN)
    elif (maxIndex == 1):
            matrix.fill(matrix.LED_YELLOW)
    elif (maxIndex == 2):
            matrix.fill(matrix.LED_RED)
    



    time.sleep(0.1)
