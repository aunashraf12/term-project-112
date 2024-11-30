from cmu_graphics import *
import math

# Parameters
num_pivots = 3  # Number of pivots
pivot_spacing = 50  # Distance between pivots
initial_pivot_x, pivot_y = 200, 100  # Initial pivot position
length = 150  # Length of the rope
angle = -math.pi / 6  # Initial angle (leftmost position)
angular_velocity = 0  # Angular velocity
angular_acceleration = 0  # Angular acceleration
gravity = 0.0005  # Gravitational constant for swinging

# Swing range
swing_range_left = -math.pi / 6  # Leftmost swing limit
swing_range_right = math.pi / 6  # Rightmost swing limit

# Square properties
square_size = 20
square_x_velocity = 1  # Constant rightward movement speed
max_distance = 300  # Swinging stops if the square moves beyond this distance

# State tracking
pivots = []  # List of pivot points
squares = []  # List of square objects
ropes = []  # List of ropes
swinging_states = [False] * num_pivots  # Swinging states for each square
angles = [angle] * num_pivots  # Angles for each pivot
angular_velocities = [0] * num_pivots  # Angular velocities for each pivot

# Create pivot, square, and rope objects
for i in range(num_pivots):
    pivot_x = initial_pivot_x + i * pivot_spacing
    pivots.append(Circle(pivot_x, pivot_y, 5, fill="red"))
    square_x = pivot_x + length * math.sin(angle)
    square_y = pivot_y + length * math.cos(angle)
    squares.append(Rect(square_x, square_y, square_size, square_size, fill="blue"))
    ropes.append(Line(pivot_x, pivot_y, square_x, square_y, lineWidth=2, fill="black", visible=False))

# Function to calculate the square's position for a given pivot
def calculate_square_position(index):
    pivot_x = pivots[index].centerX
    square_x = pivot_x + length * math.sin(angles[index])
    square_y = pivot_y + length * math.cos(angles[index])
    return square_x, square_y

def onStep():
    global angular_velocities, angles, swinging_states

    # Update positions of all pivots and squares
    for i in range(num_pivots):
        # Move pivot and square to the right
        pivots[i].centerX += square_x_velocity
        pivot_x = pivots[i].centerX

        # Update square position
        square_x, square_y = calculate_square_position(i)

        # Check if the square is within the allowed swinging distance
        distance_from_pivot = abs(square_x - pivot_x)
        if distance_from_pivot > max_distance:
            swinging_states[i] = False
            ropes[i].visible = False  # Hide the rope when not swinging

        # Swing logic if the space bar is held and within range
        if swinging_states[i]:
            angular_acceleration = -gravity * math.sin(angles[i])
            angular_velocities[i] += angular_acceleration
            angles[i] += angular_velocities[i]

            # Clamp angle within the range
            if angles[i] > swing_range_right:
                angles[i] = swing_range_right
                angular_velocities[i] *= -1  # Reverse direction
            elif angles[i] < swing_range_left:
                angles[i] = swing_range_left
                angular_velocities[i] *= -1  # Reverse direction

            # Update rope visibility and position
            ropes[i].visible = True
            ropes[i].x1, ropes[i].y1 = pivot_x, pivot_y
            ropes[i].x2, ropes[i].y2 = square_x, square_y

        # Update graphical positions of squares
        squares[i].centerX = square_x
        squares[i].centerY = square_y

# Event handler for key press to control swinging
def onKeyHold(keys):
    global swinging_states
    if 'space' in keys:
        swinging_states = [True] * num_pivots
    else:
        swinging_states = [False] * num_pivots
        for rope in ropes:
            rope.visible = False  # Hide ropes when not swinging

# Add graphical elements to canvas
app.stepsPerSecond = 100
cmu_graphics.run()
