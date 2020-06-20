import curses
import time

# Map Data (list) -> [time, velocity, pair]  (1 = red, 2 = blue)


class Engine:

    def __init__(self, map_data, framerate=60, audio=None):  # TODO: Map metadata (Accuracy thresholds, BPM, etc),
        # engine settings such as keybindings, etc
        self.map_data = map_data
        self.framerate = framerate
        self.audio = audio  # TODO: Play audio

    def start(self):
        start_time = time.time()
        stdscr = curses.initscr()
        stdscr.nodelay(1)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.curs_set(0)
        curses.cbreak()
        curses.echo(0)
        y, x = stdscr.getmaxyx()
        oldy = y
        oldx = x
        score = 0
        current = 0
        while True:
            y, x = stdscr.getmaxyx()
            if y != oldy or x != oldx:
                stdscr.clear()
                oldy = y
                oldx = x
            ctime = int((time.time() - start_time) * 1000)
            ch = stdscr.getch()
            stdscr.addstr(0, 0, f'Score: {score}')
            stdscr.addstr(5, 0, ' ' * x, curses.color_pair(1))
            stdscr.addstr(5, 1, '  ', curses.color_pair(5))
            i = 0
            for t, velocity, pair in self.map_data:
                curr = i == current
                i += 1
                diff = t - ctime
                location = int((diff/x)/velocity) + 1
                if location < 1:
                    if curr:
                        current += 1
                    continue
                if location > x-1:
                    continue
                stdscr.addstr(5, location, '*', curses.color_pair(pair))
            if current >= len(self.map_data):
                curses.endwin()
                return
            if ch != -1:
                red = ch == 97 or ch == 115  # A S
                blue = ch == 107 or ch == 108  # K L
                t, velocity, pair = self.map_data[current]
                diff = t - ctime
                if pair == 1 and red or pair == 2 and blue:
                    if diff > 350:  # Proper values + OD
                        continue
                    score += 300
                    current += 1
            stdscr.refresh()
            time.sleep(1000/self.framerate/1000)  # A disgusting way to limit framerate
