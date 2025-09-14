# Particle code by Dave Elfving 
# Generated using Github Copilot

import board
import adafruit_lis3dh
import time
import math

from adafruit_ht16k33.matrix import Matrix8x8x2

# Initialize I2C and devices
i2c = board.STEMMA_I2C()
matrix = Matrix8x8x2(i2c)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# Set accelerometer range
lis3dh.range = adafruit_lis3dh.RANGE_2_G

# Water droplet positions and velocities
# Each droplet: [x, y, velocity_x, velocity_y]
droplets = [
    [1.0, 1.0, 0.0, 0.0],  # droplet 1
    [3.0, 2.0, 0.0, 0.0],  # droplet 2
    [5.0, 1.0, 0.0, 0.0],  # droplet 3
    [2.0, 4.0, 0.0, 0.0],  # droplet 4
    [6.0, 3.0, 0.0, 0.0],  # droplet 5
    [4.0, 5.0, 0.0, 0.0],  # droplet 6
    [1.0, 6.0, 0.0, 0.0],  # droplet 7
]

# Physics constants
FRICTION = 0.92
MAX_VELOCITY = 0.8
ACCEL_FACTOR = 0.25
BOUNCE_DAMPING = 0.7
COLLISION_DISTANCE = 1.2
REPULSION_FORCE = 0.3

# Warm yellow color (red + green LEDs)
WARM_YELLOW = 3  # matrix.LED_RED (1) + matrix.LED_GREEN (2)

# Accelerometer smoothing
smooth_x = 0.0
smooth_y = 0.0
SMOOTH_FACTOR = 0.8

# Track occupied pixels to prevent flickering
occupied_pixels = {}
previous_positions = []
MOVEMENT_THRESHOLD = 0.05  # Minimum movement to trigger display update
last_matrix_state = [[0 for _ in range(8)] for _ in range(8)]  # Track LED states

def distance(x1, y1, x2, y2):
    """Calculate distance between two points"""
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)

def has_significant_movement():
    """Check if any droplet has moved significantly"""
    global previous_positions
    
    # Initialize previous positions if empty
    if len(previous_positions) != len(droplets):
        previous_positions = [[d[0], d[1]] for d in droplets]
        return True
    
    # Check if any droplet moved beyond threshold
    for i, droplet in enumerate(droplets):
        prev_x, prev_y = previous_positions[i]
        curr_x, curr_y = droplet[0], droplet[1]
        
        if distance(prev_x, prev_y, curr_x, curr_y) > MOVEMENT_THRESHOLD:
            return True
        
        # Also check velocity - if droplet is moving, keep updating
        vel_x, vel_y = droplet[2], droplet[3]
        velocity_mag = math.sqrt(vel_x * vel_x + vel_y * vel_y)
        if velocity_mag > 0.02:  # Very small threshold for velocity
            return True
    
    return False

def update_previous_positions():
    """Update the stored previous positions"""
    global previous_positions
    previous_positions = [[d[0], d[1]] for d in droplets]

def render_to_matrix():
    """Render droplets to matrix with stable positioning"""
    global last_matrix_state
    
    # Create new matrix state
    new_matrix_state = [[0 for _ in range(8)] for _ in range(8)]
    occupied_pixels.clear()
    
    # Render droplets to new state
    for droplet in droplets:
        x_pos, y_pos, vel_x, vel_y = droplet
        
        # Convert to pixel coordinates
        pixel_x = int(x_pos + 0.5)  # Round to nearest integer
        pixel_y = int(y_pos + 0.5)
        
        # Ensure pixel is within bounds
        if 0 <= pixel_x <= 7 and 0 <= pixel_y <= 7:
            pixel_key = (pixel_x, pixel_y)
            
            # If pixel is already occupied, try adjacent pixels
            if pixel_key in occupied_pixels:
                # Try nearby pixels in a small radius
                found_spot = False
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        new_x = pixel_x + dx
                        new_y = pixel_y + dy
                        new_key = (new_x, new_y)
                        
                        if (0 <= new_x <= 7 and 0 <= new_y <= 7 and 
                            new_key not in occupied_pixels):
                            new_matrix_state[new_x][new_y] = WARM_YELLOW
                            occupied_pixels[new_key] = True
                            found_spot = True
                            break
                    if found_spot:
                        break
                
                # If no nearby spot found, still light the original pixel
                if not found_spot:
                    new_matrix_state[pixel_x][pixel_y] = WARM_YELLOW
            else:
                # Pixel is free, use it
                new_matrix_state[pixel_x][pixel_y] = WARM_YELLOW
                occupied_pixels[pixel_key] = True
    
    # Only update matrix if the state has changed
    if new_matrix_state != last_matrix_state:
        matrix.fill(0)  # Clear matrix
        for x in range(8):
            for y in range(8):
                if new_matrix_state[x][y] != 0:
                    matrix[x, y] = new_matrix_state[x][y]
        
        last_matrix_state = [row[:] for row in new_matrix_state]  # Deep copy

def handle_collisions():
    """Handle droplet-to-droplet collisions"""
    for i in range(len(droplets)):
        for j in range(i + 1, len(droplets)):
            x1, y1, vx1, vy1 = droplets[i]
            x2, y2, vx2, vy2 = droplets[j]
            
            dist = distance(x1, y1, x2, y2)
            
            if dist < COLLISION_DISTANCE and dist > 0:
                # Calculate repulsion direction
                dx = x2 - x1
                dy = y2 - y1
                
                # Normalize direction
                dx_norm = dx / dist
                dy_norm = dy / dist
                
                # Apply repulsion force
                force = REPULSION_FORCE * (COLLISION_DISTANCE - dist)
                
                # Update velocities (repel from each other)
                droplets[i][2] -= dx_norm * force
                droplets[i][3] -= dy_norm * force
                droplets[j][2] += dx_norm * force
                droplets[j][3] += dy_norm * force
                
                # Separate overlapping droplets
                overlap = COLLISION_DISTANCE - dist
                separate_dist = overlap * 0.5
                
                droplets[i][0] -= dx_norm * separate_dist
                droplets[i][1] -= dy_norm * separate_dist
                droplets[j][0] += dx_norm * separate_dist
                droplets[j][1] += dy_norm * separate_dist

print("Water droplet simulation starting...")

while True:
    # Read accelerometer values
    x, y, z = lis3dh.acceleration
    # Convert to G and apply smoothing
    accel_x = (y / adafruit_lis3dh.STANDARD_GRAVITY)  # swapped: X now from -Y
    accel_y = (x / adafruit_lis3dh.STANDARD_GRAVITY)   # swapped: Y now from X
    
    # Apply smoothing filter
    smooth_x = smooth_x * SMOOTH_FACTOR + accel_x * (1 - SMOOTH_FACTOR)
    smooth_y = smooth_y * SMOOTH_FACTOR + accel_y * (1 - SMOOTH_FACTOR)

    
    # Update each droplet
    for droplet in droplets:
        x_pos, y_pos, vel_x, vel_y = droplet
        
        # Apply acceleration
        vel_x += smooth_x * ACCEL_FACTOR
        vel_y += smooth_y * ACCEL_FACTOR
        
        # Apply friction
        vel_x *= FRICTION
        vel_y *= FRICTION
        
        # Limit maximum velocity
        velocity_mag = math.sqrt(vel_x * vel_x + vel_y * vel_y)
        if velocity_mag > MAX_VELOCITY:
            vel_x = (vel_x / velocity_mag) * MAX_VELOCITY
            vel_y = (vel_y / velocity_mag) * MAX_VELOCITY
        
        # Update position
        x_pos += vel_x
        y_pos += vel_y
        
        # Handle wall collisions with bouncing
        if x_pos < 0:
            x_pos = 0
            vel_x = -vel_x * BOUNCE_DAMPING
        elif x_pos > 7:
            x_pos = 7
            vel_x = -vel_x * BOUNCE_DAMPING
            
        if y_pos < 0:
            y_pos = 0
            vel_y = -vel_y * BOUNCE_DAMPING
        elif y_pos > 7:
            y_pos = 7
            vel_y = -vel_y * BOUNCE_DAMPING
        
        # Update droplet data
        droplet[0] = x_pos
        droplet[1] = y_pos
        droplet[2] = vel_x
        droplet[3] = vel_y
    
    # Handle droplet-to-droplet collisions
    handle_collisions()
    
    # Only update display if there's significant movement
    if has_significant_movement():
        render_to_matrix()
        update_previous_positions()
    
    # Update at ~30 FPS for stable motion
    time.sleep(0.033)
