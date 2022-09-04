import curses

import global_variable
from game_scenario import PHRASES
from sleep import sleep


async def years(canvas, game_time_speed):
    max_width = 49
    year_window = canvas.derwin(3, max_width, 0, 0)
    description = ""
    while True:
        if global_variable.year in PHRASES:
            description = PHRASES[global_variable.year]
        text = f"{str(global_variable.year)}:{description}"
        for _ in range(game_time_speed):
            year_window.addstr(1, 1, text, curses.A_BOLD)
            year_window.border()
            year_window.refresh()
            await sleep()
        global_variable.year += 1
