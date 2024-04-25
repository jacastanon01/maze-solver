from random import randint, choice
import argparse
from typing import Tuple


from src.maze import Maze, MazeDrawer, MazeSolver
from src.screen import Window


def main() -> None:
    print(
        "Welcome to the Maze Solver where you can visualize the path you take to solve a maze.",
        end=f"\n{'=' * 10}\n",
    )

    width, height, padding_x, padding_y, cols, rows = calculate_window_sizes()
    cell_cols = 20 if cols < 25 else 10
    cell_rows = 20 if rows < 25 else 10
    my_maze = Maze(padding_x, padding_y, cols, rows, cell_cols, cell_rows)
    window = Window(width, height)
    render_maze(my_maze, window)


def calculate_window_sizes() -> Tuple[int, int, int, int, int, int]:
    """
    Takes user input of columns and rows to calculate the size of a window based on those values.
    Calls draw_maze with input values to draw the maze
    """
    while True:
        try:
            cols = int(input("Enter number of columns: "))
            if not is_valid_input(cols):
                continue
            rows = int(input("Enter number of rows: "))
            if not is_valid_input(rows):
                continue

            print(f"Generating a {cols} by {rows} maze...")
            desired_padding = 50
            cell_cols = 20 if cols < 25 else 10
            cell_rows = 20 if rows < 25 else 10
            window_size = 800

            maze_width = cols * cell_cols
            maze_height = rows * cell_rows

            window_width = maze_width + (
                desired_padding * 2
            )  # Maze size plus padding for left and right
            window_height = maze_height + (
                desired_padding * 2
            )  # Maze size plus padding for top and bottom

            padding_x = (window_size - maze_width) // 2
            padding_y = (window_size - maze_height) // 2

            return (
                window_size,
                window_size,
                padding_x,
                padding_y,
                cols,
                rows,
            )

        except ValueError as e:
            print("Please enter a valid integer.")


def render_maze(maze: Maze, window: Window) -> None:
    """
    Draws a maze with the given parameters

    Parameters
    -----
    - padding_x (int): _description_
    - padding_y (int): _description_
    - cols (int): _description_
    - rows (int): _description_
    """
    drawer = MazeDrawer(maze, window)
    solve_maze(maze, drawer)
    window.start()
    window.wait_for_close()


def solve_maze(maze: Maze, drawer: MazeDrawer) -> None:
    """Creates MazeSolver instance to call solve method on maze"""
    solution = MazeSolver(maze, drawer)
    solution.solve()


def is_valid_input(value: int) -> bool:
    """Helper function to validate input for maze"""
    if 2 > value or value > 50:
        print("Input must be between 2 and 50. Please enter values again.")
        return False
    return True


if __name__ == "__main__":
    main()
