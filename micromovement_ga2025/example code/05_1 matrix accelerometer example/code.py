import board
import adafruit_lis3dh
import time

from adafruit_ht16k33.matrix import Matrix8x8x2

i2c = board.STEMMA_I2C()
matrix = Matrix8x8x2(i2c)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G

while True:
    # Put your code here!
    x, y, z = (value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration)
    
    if (x > .9): 
        matrix.fill(matrix.LED_GREEN)
    else:
        matrix.fill(matrix.LED_OFF)

    
    time.sleep(0.1)
