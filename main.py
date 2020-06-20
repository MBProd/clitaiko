import curses
from PyTaiko import engine

# TODO: Proper interface
data = list()
data.append((4000, 1, 1))
data.append((4200, 1, 2))
data.append((4400, 1, 1))
data.append((6000, 1, 2))
data.append((6200, 1, 1))
data.append((6400, 1, 2))

engine = engine.Engine(data)
try:
    engine.start()
except Exception as e:
    curses.endwin()
    print(e)
