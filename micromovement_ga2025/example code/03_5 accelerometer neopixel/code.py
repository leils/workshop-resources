import board
import adafruit_lis3dh
import time
import neopixel

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G

# Loop forever printing accelerometer values
while True:
    # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
    # z axis values.  We divide them by 9.806 (STANDARD_GRAVITY) to convert to Gs.
    x, y, z = (value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration)
    print(f"x = {x:.3f} G, y = {y:.3f} G, z = {z:.3f} G")

    red = max(0, int(255*(x/2)))
    green = max(0, int(255*(y/2)))
    blue = max(0, int(255*(z/2)))
    pixels.fill((red, green, blue))

    time.sleep(0.1)