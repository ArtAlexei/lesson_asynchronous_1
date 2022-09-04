from curses_tools import draw_frame, get_frame_size
from sleep import sleep


def get_game_over(file_path):
    with open(file_path, "r") as file:
        game_over = file.read()
    return game_over


async def show_game_over(canvas, text):
    while True:
        rows_number, columns_number = canvas.getmaxyx()
        text_row, text_column = get_frame_size(text)
        draw_frame(
            canvas,
            rows_number // 2 - text_row // 2,
            columns_number // 2 - text_column // 2,
            text,
        )
        await sleep()
