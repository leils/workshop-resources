# CPX Sound Responsive Pinwheel 
# tested with CircuitPython 10.x
import array
import math
import audiobusio
import board
import neopixel
import time

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

COLORS = [RED, YELLOW, GREEN, BLUE, PURPLE, WHITE]
COLOR_INDEX = 0
NUM_COLORS = 6

# Color of the peak pixel.
PEAK_COLOR = (100, 0, 255)
# Number of total pixels - 10 build into Circuit Playground
NUM_PIXELS = 10

PIXEL_INDEX = 0
PIXEL_ADJUSTED_WAIT = 0.1
PIXEL_WAIT_MAX = 0.07
PIXEL_WAIT_MIN = 0.005
MAG_MAX = 8000
LAST_PIXEL_TIME = -1

min_threshold = 300

# Exponential scaling factor.
# Should probably be in range -10 .. 10 to be reasonable.
CURVE = 2
SCALE_EXPONENT = math.pow(10, CURVE * -0.1)

# Number of samples to read at once.
NUM_SAMPLES = 160


# Restrict value to be between floor and ceiling.
def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))


# Scale input_value between output_min and output_max, exponentially.
def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / \
                             (input_max - input_min)
    return output_min + \
        math.pow(normalized_input_value, SCALE_EXPONENT) \
        * (output_max - output_min)


# Remove DC bias before computing RMS.
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(samples_sum / len(values))


def mean(values):
    return sum(values) / len(values)

# This maps the magnitude of the sound experienced to the wait time between animation frames.
def range_map_magnitudes(mag):
    global PIXEL_ADJUSTED_WAIT
    if mag > MAG_MAX: 
        mag = MAG_MAX
    percent = 1 - (mag / MAG_MAX) #needs to be flipped in order to go faster when blowing harder
    PIXEL_ADJUSTED_WAIT = (percent * PIXEL_WAIT_MAX) 

# Main program

# Set up NeoPixels and turn them all off.
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.1, auto_write=False)
pixels.fill(0)
pixels.show()

mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                       sample_rate=16000, bit_depth=16)

# Record an initial sample to calibrate. Assume it's quiet when we start.
samples = array.array('H', [0] * NUM_SAMPLES)
mic.record(samples, len(samples))
# Set lowest level to expect, plus a little.
input_floor = normalized_rms(samples) + 10
input_ceiling = input_floor + 1000

peak = 0
while True:
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)

    # print magnitude for debugging
    # print(magnitude) 

    if magnitude > min_threshold: 
        now = time.monotonic()
        if (now >= LAST_PIXEL_TIME + PIXEL_ADJUSTED_WAIT):
            pixels.fill(OFF)
            pixels[PIXEL_INDEX] = YELLOW

            PIXEL_INDEX = (PIXEL_INDEX + 1) % NUM_PIXELS
            LAST_PIXEL_TIME = now
            COLOR_INDEX = (COLOR_INDEX + 1) % NUM_COLORS
            range_map_magnitudes(magnitude)
    else: 
        pixels.fill(OFF);
    pixels.show()