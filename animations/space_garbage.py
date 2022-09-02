from sleep import sleep
from obstacles import Obstacle
import random
from config import START_YEAR
from curses_tools import draw_frame, get_frame_size
import asyncio
from animations.explosion import explode


import global_variable


async def fly_garbage(canvas, column, garbage_frame, speed, garbage_uid):
    """Animate garbage, flying from top to bottom. 
    Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    frame_rows, frame_columns = get_frame_size(garbage_frame)
    obstacle = Obstacle(
        row,
        column,
        frame_rows,
        frame_columns,
        garbage_uid
    )
    global_variable.obstacles.append(obstacle)

    while row < rows_number:
        obstacle.row = row
        obstacle.column = column
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed

        if obstacle in global_variable.obstacles_in_last_collisions:
            global_variable.obstacles_in_last_collisions.remove(obstacle)
            global_variable.obstacles.remove(obstacle)
            await explode(
                canvas,
                row+frame_rows//2,
                column+frame_columns//2
            )
            return
    global_variable.obstacles.remove(obstacle)


async def fill_orbit_with_garbage(canvas, garbage):

    _, columns_number = canvas.getmaxyx()
    garbage_uid = 0
    start_delay = 100
    while True:
        game_difficulty = global_variable.year - START_YEAR
        garbage_delay = max(start_delay - game_difficulty, 10)
        await sleep(garbage_delay)
        column = random.randint(0, columns_number)
        global_variable.coroutines.append(
            fly_garbage(
                canvas,
                column,
                random.choice(garbage),
                random.uniform(0.05, 0.1),
                garbage_uid
            )
        )
        garbage_uid += 1
