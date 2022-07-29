import time
import curses


def draw(canvas):
    row, column = (5, 20)
    canvas.border()
    canvas.addstr(row, column, 'Hello, World!')
    canvas.refresh()
    canvas.refresh()

    time.sleep(3)


if __name__ == '__main__':
    curses.initscr()
    curses.curs_set(False)
    curses.update_lines_cols()

    curses.wrapper(draw)