import board
import time

from adafruit_ht16k33.matrix import Matrix8x8x2

i2c = board.STEMMA_I2C()
matrix = Matrix8x8x2(i2c)

matrix[0,0] = matrix.LED_GREEN
matrix[7,7] = matrix.LED_RED
# matrix.fill(matrix.LED_GREEN)
