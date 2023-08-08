import numpy as np
import matplotlib.pyplot as plt
import copy

# Directions
RIGHT = np.array([0, 1])
DOWN = np.array([1, 0])
UP = np.array([-1, 0])
LEFT = np.array([0, -1])
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
# Starting condition
DIR = 1  # Initial direction is right
DIRECTION = DIRECTIONS[DIR]

# Global variables for any maze to begin
POSITION = np.array([0, 0])
MAZE = None
IM = None

# =======================================================
# Mazes
# =======================================================
MAZE0 = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1],
        [2, 0, 0, 0, 0, 0, 3],
        [1, 1, 1, 1, 1, 1, 1],
    ]
)

MAZE1 = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 3],
        [1, 1, 0, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 1],
        [2, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ]
)


MAZE2 = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 3],
        [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
        [2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
)
# -------------------------------------------------------
# =======================================================


def update(func):
    """Wrapper function to make all
    position/direction changes to
    update the plot
    """

    def wrapper(*args, **kwargs):
        global MAZE, POSITION, DIRECTION, IM
        func(*args, **kwargs)
        IM.set_data(MAZE)
        plt.arrow(
            x=POSITION[1],
            y=POSITION[0],
            dx=DIRECTION[1] / 3,
            dy=DIRECTION[0] / 3,
            width=0.12,
        )
        plt.pause(0.1)

    return wrapper


def get_start_position():
    global MAZE
    pos = np.where(MAZE == 2)
    return (pos[0][0], pos[1][0])


def reset_start(maze):
    global POSITION, MAZE, IM
    MAZE = copy.deepcopy(maze)
    POSITION = get_start_position()
    fig = plt.figure()
    plt.xticks([])
    plt.yticks([])
    plt.ion()
    IM = plt.imshow(MAZE, vmin=0, vmax=4)
    return fig


def is_position_clear(position):
    global MAZE
    return MAZE[position[0], position[1]] != 1


def left_dir_idx():
    global DIRECTION, DIR
    return DIR - 1 if DIR > 0 else len(DIRECTIONS) - 1


def right_dir_idx():
    global DIRECTION, DIR
    return DIR + 1 if DIR < len(DIRECTIONS) - 1 else 0


def left_of(d):
    global DIRECTIONS
    return DIRECTIONS[left_dir_idx()]


def right_of(d):
    global DIRECTIONS
    return DIRECTIONS[right_dir_idx()]


def is_front_clear():
    global POSITION, DIRECTION
    return is_position_clear(POSITION + DIRECTION)


def is_left_clear():
    global POSITION, DIRECTION
    return is_position_clear(POSITION + left_of(DIRECTION))


def is_right_clear():
    global POSITION, DIRECTION
    return is_position_clear(POSITION + right_of(DIRECTION))


@update
def turn_right():
    global DIRECTION, DIR
    DIR = right_dir_idx()
    DIRECTION = DIRECTIONS[DIR]


@update
def turn_left():
    global DIRECTION, DIR
    DIR = left_dir_idx()
    DIRECTION = DIRECTIONS[DIR]


@update
def move_forward():
    global POSITION, DIRECTION, MAZE
    current_val = MAZE[POSITION[0], POSITION[1]]

    MAZE[POSITION[0], POSITION[1]] = 0 if current_val == 4 else 1
    new_position = POSITION + DIRECTION
    # If the wall is hit - raise an error
    if MAZE[new_position[0], new_position[1]] == 1:
        raise ValueError("You hit the wall, try again")
    elif MAZE[new_position[0], new_position[1]] == 3:
        raise KeyError("Yay you completed the maze!")
    # Set new position
    POSITION = new_position
    # Update maze value
    MAZE[POSITION[0], POSITION[1]] = 4


### IGNORE BEGIN ###


def run(use_right=True):
    while True:
        if use_right:
            if is_right_clear():
                turn_right()
                move_forward()
            elif is_front_clear():
                move_forward()
            else:
                turn_left()
        else:
            if is_left_clear():
                turn_left()
                move_forward()
            elif is_front_clear():
                move_forward()
            else:
                turn_right()


if __name__ == "__main__":
    fig = reset_start(MAZE1)
    run()

### IGNORE END ###