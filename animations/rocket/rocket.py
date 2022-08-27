
import asyncio
from itertools import cycle
from animations.fire import fire
from animations.game_over.geme_over import get_gemeover, show_gameover

from config import BORDER_THICKNESS, GAMEOVER_ROUTE, GUN_YEAR, SPACESHIP_HEIGHT, SPACESHIP_ROUTE, SPACESHIP_WIDTH

from curses_tools import draw_frame, read_controls
from physics import update_speed
import global_variable


def get_spaceships(*spaceships_names):
    spaceships = []
    for spaceship_name in spaceships_names:
        file_path = SPACESHIP_ROUTE + spaceship_name + '.txt'
        with open(file_path, "r") as file:
            spaceships.append(file.read())
    return spaceships


def calculate_spaceship_location(canvas, row, column, row_speed, column_speed):

    rows_direction, columns_direction, space_pressed = read_controls(canvas)

    if space_pressed and global_variable.year > GUN_YEAR:
        global_variable.coroutines.append(fire(canvas, row, column))

    max_row, max_column = canvas.getmaxyx()

    row_speed, column_speed = update_speed(row_speed, column_speed,
                                           rows_direction, columns_direction)

    future_column = column + column_speed
    if (future_column < max_column - SPACESHIP_WIDTH-BORDER_THICKNESS) \
            and (future_column > SPACESHIP_WIDTH):
        column = future_column

    future_row = row + row_speed
    if (future_row < max_row - SPACESHIP_HEIGHT-BORDER_THICKNESS) and (future_row > BORDER_THICKNESS):
        row = future_row

    return row, column, row_speed, column_speed


async def animate_spaceship(canvas, row, column, spaceships):
    row_speed = column_speed = 0
    for spaceship in cycle(spaceships):
        for _ in range(2):
            row, column, row_speed, column_speed = calculate_spaceship_location(
                canvas, row, column, row_speed, column_speed)

            for obstacle in global_variable.obstacles:
                if obstacle.has_collision(row,
                                          column,
                                          SPACESHIP_WIDTH,
                                          SPACESHIP_HEIGHT,):
                    gameover = get_gemeover(GAMEOVER_ROUTE)
                    global_variable.coroutines.append(show_gameover(canvas, gameover))
                    return

            draw_frame(canvas, row, column-2, spaceship)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column-2, spaceship, negative=True)
