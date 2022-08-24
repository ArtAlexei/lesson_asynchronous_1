import random
from config import GARBAGE_ROUTE
from curses_tools import draw_frame
import asyncio


from global_variable import coroutines
from sleep import sleep


def get_garbage(*garbage_names):
    garbage = []
    for name in garbage_names:
        file_path = GARBAGE_ROUTE + name + '.txt'
        with open(file_path, "r") as file:
            garbage.append(file.read())
    return garbage


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. 
    Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas):
    garbage = get_garbage('duck', 'hubble', 'lamp',
                          'trash_large', 'trash_small', 'trash_xl')
    _, columns_number = canvas.getmaxyx()

    while True:
        await sleep(random.randint(30, 60))
        column = random.randint(0, columns_number)
        coroutines.append(fly_garbage(canvas,
                                      column,
                                      random.choice(garbage),
                                      random.uniform(0.05, 0.1)
                                      ))
