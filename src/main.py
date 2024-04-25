from random import randint, choice

from src.maze import Maze, MazeDrawer
from src.screen import Window


def main() -> None:
    print("Welcome to the maze solver!", end="\n==================\n\n")
    print("Please enter the dimensions of your maze:")
    cols = int(input("Columns: "))
    rows = int(input("Rows: "))
    width = cols * 50
    height = rows * 50
    print(f"\nYour maze is {cols} columns by {rows} rows.")
    window = Window(width, height)
    padding_x = width // 2
    padding_y = height // 2
    my_maze = Maze(padding_x, padding_y, cols, rows, 10, 10)
    maze = MazeDrawer(my_maze, window)
    window.start()
    window.wait_for_close()


if __name__ == "__main__":
    main()
