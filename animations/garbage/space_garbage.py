import random
from config import GARBAGE_ROUTE
from curses_tools import draw_frame, get_frame_size
import asyncio
from explosion import explode


from global_variable import coroutines, obstacles, obstacles_in_last_collisions
from obstacles import Obstacle
from sleep import sleep


def get_garbage(*garbage_names):
    garbage = []
    for name in garbage_names:
        file_path = GARBAGE_ROUTE + name + '.txt'
        with open(file_path, "r") as file:
            garbage.append(file.read())
    return garbage


async def fly_garbage(canvas, column, garbage_frame, speed, garbage_uid):
    """Animate garbage, flying from top to bottom. 
    Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    frame_rows, frame_columns = get_frame_size(garbage_frame)
    obstacle = Obstacle(row,
                        column,
                        frame_rows,
                        frame_columns,
                        garbage_uid)
    obstacles.append(obstacle)

    while row < rows_number:
        obstacle.row = row
        obstacle.column = column
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed

        if obstacle in obstacles_in_last_collisions:
            obstacles_in_last_collisions.remove(obstacle)
            obstacles.remove(obstacle)
            await explode(canvas,
                          row+frame_rows//2,
                          column+frame_columns//2)
            return
    obstacles.remove(obstacle)


async def fill_orbit_with_garbage(canvas):
    garbage = get_garbage('duck', 'hubble', 'lamp',
                          'trash_large', 'trash_small', 'trash_xl')
    _, columns_number = canvas.getmaxyx()
    garbage_uid = 0
    while True:
        await sleep(random.randint(30, 60))
        column = random.randint(0, columns_number)
        coroutines.append(fly_garbage(canvas,
                                      column,
                                      random.choice(garbage),
                                      random.uniform(0.05, 0.1),
                                      garbage_uid
                                      ))
        garbage_uid += 1
