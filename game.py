import curses
import random
import time
from animations.blink import blink
from animations.fire import fire
from animations.rocket.rocket import animate_spaceship, get_spaceships
from config import SPACESHIP_1_ROUTE, SPACESHIP_2_ROUTE, TIC_TIMEOUT


def draw(canvas,  page_rows, page_columns):
    canvas.nodelay(True)

    spaceship_row = page_rows // 2
    spaceship_column = page_columns // 2
    coroutines = [fire(canvas, spaceship_row, spaceship_column)]
    spaceships = get_spaceships(SPACESHIP_1_ROUTE, SPACESHIP_2_ROUTE)
    coroutines.append(
        animate_spaceship(canvas, spaceship_row, spaceship_column, spaceships)
    )

    for _ in range(100):
        row = random.randint(1, page_rows - 2)
        column = random.randint(1, page_columns - 2)
        offset_tics = random.randint(1, 30)
        symbol = random.choice('+*.:')
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


if __name__ == '__main__':
    window = curses.initscr()
    curses.curs_set(False)
    curses.update_lines_cols()
    page_rows, page_columns = window.getmaxyx()
    curses.wrapper(draw, page_rows, page_columns)
