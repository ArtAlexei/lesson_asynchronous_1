import asyncio
import curses
import time

TIC_TIMEOUT = 0.01


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


def draw(canvas):
    canvas.border()
    canvas.refresh()
    coroutines = [blink(canvas, num_rows, num_columns),
                  blink(canvas, 3, 2),
                  blink(canvas, 3, 3),
                  blink(canvas, 3, 4),
                  blink(canvas, 3, 5), ]
    while True:
        try:
            for coroutine in coroutines:
                coroutine.send(None)  # В четвёртый раз здесь вылетит StopIteration
                time.sleep(TIC_TIMEOUT)
            canvas.refresh()
        except StopIteration:
            break


if __name__ == '__main__':
    curses.initscr()
    curses.curs_set(False)

    curses.update_lines_cols()
    num_rows, num_columns = curses.LINES, curses.COLS
    curses.wrapper(draw)
