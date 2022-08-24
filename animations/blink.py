import asyncio
import curses

from sleep import sleep


async def blink(canvas, row, column, offset_tics=0, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(20)
        for _ in range(offset_tics):
            await sleep()
        canvas.addstr(row, column, symbol)
        await sleep(3)
        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(5)
        canvas.addstr(row, column, symbol)
        await sleep(3)
