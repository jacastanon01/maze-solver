from random import randint, choice

from maze import Maze, MazeDrawer
from screen import Window


def main() -> None:
    window = Window(800, 800)
    my_maze = Maze(10, 10, 6, 4, 10, 10)
    maze = MazeDrawer(my_maze, window)
    maze._create_cells()
    window.start()
    window.wait_for_close()


if __name__ == "__main__":
    main()
