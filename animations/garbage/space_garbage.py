import random
from curses_tools import draw_frame
import asyncio

from global_variable import coroutines


async def fill_orbit_with_garbage(canvas):
    with open('animations/garbage/duck.txt', "r") as garbage_file:
        frame = garbage_file.read()
    rows_number, columns_number = canvas.getmaxyx()
    while True:
        for _ in range(20):
            await asyncio.sleep(0)
        column = random.randint(0, columns_number)
        coroutines.append(fly_garbage(canvas, column, frame))


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
