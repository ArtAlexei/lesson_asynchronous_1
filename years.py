import curses
from global_variable import year
from sleep import sleep
from game_scenario import PHRASES


async def years(canvas, game_time_speed):
    max_width = 49
    year_window = canvas.derwin(3, max_width, 0, 0)
    description = ''
    global year
    while True:
        if year in PHRASES:
            description = PHRASES[year]
        text = f'{str(year)}:{description}'
        for _ in range(game_time_speed):
            year_window.addstr(1, 1, text, curses.A_BOLD)
            year_window.border()
            year_window.refresh()
            await sleep()
        year += 1
