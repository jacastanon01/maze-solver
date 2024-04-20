from random import randint, choice

from maze import Maze, MazeDrawer
from screen import Window


def main() -> None:
    window = Window(800, 800)
    my_maze = Maze(10, 10, 6, 4, 10, 10)
    maze = MazeDrawer(my_maze, window)
    maze._create_cells()
    window.start()
    # render_maze(window)
    # render_grid(window)
    # c1 = Cell(window)
    # c1.has_right_wall = False
    # c1.draw(50, 50, 100, 100)

    # c2 = Cell(window)
    # c2.has_left_wall = False
    # c2.has_bottom_wall = False
    # c2.draw(100, 50, 150, 100)

    # c1.draw_move(c2)

    # c3 = Cell(window)
    # c3.has_top_wall = False
    # c3.has_right_wall = False
    # c3.draw(100, 100, 150, 150)

    # c2.draw_move(c3)

    # c4 = Cell(window)
    # c4.has_left_wall = False
    # c4.draw(150, 100, 200, 150)

    # c3.draw_move(c4, True)

    window.wait_for_close()


if __name__ == "__main__":
    main()
