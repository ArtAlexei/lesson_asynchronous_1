import curses
import random
import time

from animations.blink import blink
from animations.rocket import animate_spaceship
from animations.space_garbage import fill_orbit_with_garbage
from config import (BORDER_THICKNESS, GARBAGE_ROUTE, NUMBER_OR_STARS,
                    SPACESHIP_ROUTE, TIC_TIMEOUT)
from get_sprite import get_sprite
from global_variable import coroutines
from years import years


def draw(canvas, page_rows, page_columns):
    canvas.nodelay(True)

    spaceship_row = page_rows // 2
    spaceship_column = page_columns // 2

    spaceships = get_sprite(
        SPACESHIP_ROUTE, "rocket_frame_1", "rocket_frame_2")

    coroutines.append(
        animate_spaceship(canvas, spaceship_row, spaceship_column, spaceships)
    )
    garbage = get_sprite(
        GARBAGE_ROUTE,
        "duck",
        "hubble",
        "lamp",
        "trash_large",
        "trash_small",
        "trash_xl",
    )
    coroutines.append(fill_orbit_with_garbage(canvas, garbage))

    coroutines.append(years(canvas, 100))

    for _ in range(NUMBER_OR_STARS):
        row = random.randint(
            BORDER_THICKNESS, page_rows - 2 * BORDER_THICKNESS)
        column = random.randint(
            BORDER_THICKNESS, page_columns - 2 * BORDER_THICKNESS)
        offset_tics = random.randint(1, 30)
        symbol = random.choice("+*.:")
        coroutines.append(blink(canvas, row, column, offset_tics, symbol))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.border()

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == "__main__":
    window = curses.initscr()
    curses.curs_set(False)
    curses.update_lines_cols()
    page_rows, page_columns = window.getmaxyx()
    curses.wrapper(draw, page_rows, page_columns)
