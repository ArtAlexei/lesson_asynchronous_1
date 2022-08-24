
import asyncio
from itertools import cycle

from config import SPACESHIP_HEIGHT, SPACESHIP_ROUTE, SPACESHIP_WEIGHT

from curses_tools import draw_frame, read_controls


def get_spaceships(*spaceships_names):
    spaceships = []
    for spaceship_name in spaceships_names:
        file_path = SPACESHIP_ROUTE + spaceship_name + '.txt'
        with open(file_path, "r") as file:
            spaceships.append(file.read())
    return spaceships


def calculate_spaceship_location(canvas, row, column):
    max_row, max_column = canvas.getmaxyx()
    rows_direction, columns_direction, space_pressed = read_controls(canvas)

    future_column = column + columns_direction
    if (future_column < max_column - SPACESHIP_WEIGHT) \
            and (future_column >= SPACESHIP_WEIGHT):
        column += columns_direction

    future_row = row + rows_direction
    if (future_row < max_row - SPACESHIP_HEIGHT) and (future_row > 0):
        row += rows_direction

    return row, column


async def animate_spaceship(canvas, row, column, spaceships):
    for spaceship in cycle(spaceships):
        for _ in range(2):
            row, column = calculate_spaceship_location(canvas, row, column)
            drawing_raw, drawing_column = row, column
            draw_frame(canvas, drawing_raw, drawing_column-2, spaceship)
            await asyncio.sleep(0)
            draw_frame(canvas, drawing_raw, drawing_column-2, spaceship, negative=True)
