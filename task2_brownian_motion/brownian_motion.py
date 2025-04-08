import numpy as np
import matplotlib.pyplot as plt

arena_size = 10
robot_radius = 1  # robot's radius
robot_position = np.array([arena_size / 2, arena_size / 2])
robot_direction = np.random.uniform(0, 2 * np.pi)

def move_robot(position, direction):
    move_distance = 0.1
    new_position = position + move_distance * np.array([np.cos(direction), np.sin(direction)])
    if np.abs(new_position[0]) > arena_size-1 or np.abs(new_position[1]) > arena_size-1:
        direction += np.random.uniform(-np.pi , np.pi )
        new_position = position
    return new_position, direction

plt.ion()
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-arena_size, arena_size)
ax.set_ylim(-arena_size, arena_size)
positions = [robot_position]

while True:
    robot_position, robot_direction = move_robot(robot_position, robot_direction)
    positions.append(robot_position)

    x_positions = [pos[0] for pos in positions]
    y_positions = [pos[1] for pos in positions]

    ax.clear()
    ax.set_xlim(-arena_size, arena_size)
    ax.set_ylim(-arena_size, arena_size)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.plot(x_positions, y_positions, linestyle='-', color='blue')

    # Draw robot body
    robot_circle = plt.Circle(robot_position, robot_radius, color='red', fill=True)
    ax.add_patch(robot_circle)

    # Draw heading direction
    heading_x = robot_position[0] + robot_radius * 2 * np.cos(robot_direction)
    heading_y = robot_position[1] + robot_radius * 2 * np.sin(robot_direction)
    ax.plot([robot_position[0], heading_x], [robot_position[1], heading_y], color='green', linewidth=2)

    plt.title('Real-time Robot Motion with Heading')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.pause(0.01)

    if plt.get_fignums() == []:
        break
