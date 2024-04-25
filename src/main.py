from random import randint, choice
import argparse


from src.maze import Maze, MazeDrawer
from src.screen import Window


def main() -> None:
    print(
        "Welcome to the Maze Solver where you can visualize the path you take to solve a maze.",
        end=f"\n{'=' * 10}\n",
    )
    render_maze()


def render_maze():
    """
    Takes user input of columns and rows to calculate the size of a window based on those values.
    Calls draw_maze with input values to draw the maze
    """
    while True:
        cols = int(input("Enter number of columns: "))
        rows = int(input("Enter number of rows: "))
        print(f"Generating a {cols} by {rows} maze...")

        if 2 < cols > 100 or 2 < rows > 100:
            print("Columns and rows must be between 2 and 100.")
            continue
        else:
            cell_size = 50
            width = cols * cell_size
            height = rows * cell_size

            padding_x = 50 % width if width // 5 <= 1000 else 1000
            padding_y = 50 % height if height // 5 <= height else height

            draw_maze(width, height, padding_x, padding_y, cols, rows)
            break


def draw_maze(
    width: int, height: int, padding_x: int, padding_y: int, cols: int, rows: int
) -> None:
    """
    Draws a maze with the given parameters

    Parameters
    -----
    - padding_x (int): _description_
    - padding_y (int): _description_
    - cols (int): _description_
    - rows (int): _description_
    """
    my_maze = Maze(padding_x, padding_y, cols, rows, 10, 10)
    window = Window(width, height)
    maze = MazeDrawer(my_maze, window)
    window.start()
    window.wait_for_close()


if __name__ == "__main__":
    main()
