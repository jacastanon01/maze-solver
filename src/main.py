from random import randint, choice
import argparse


from src.maze import Maze, MazeDrawer
from src.screen import Window


def main() -> None:
    print(
        "Welcome to the Maze Solver where you can visualize the path you take to solve a maze.",
        end=f"\n{'=' * 10}\n",
    )

    width, height, padding_x, padding_y, cols, rows = calculate_window_sizes()
    while True:
        try:
            draw_maze(width, height, padding_x, padding_y, cols, rows)
            choice = int(input("Enter 1 to solve the maze or 2 to exit: "))
            if choice == 1:
                print("\nSolving maze...")
                solve_maze()
                break
            elif choice == 2:
                print("Exiting program.")
                break
            else:
                print("Invalid input. Try again.")
        except ValueError as e:
            print("\nPlease enter a valid integer.")


def calculate_window_sizes():
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

            else:
                print(f"Generating a {cols} by {rows} maze...")
                cell_size = 50
                width = cols * cell_size
                height = rows * cell_size

                padding_x = 50 % width if width // 5 <= 1000 else 1000
                padding_y = 50 % height if height // 5 <= height else height

                return (width, height, padding_x, padding_y, cols, rows)

        except ValueError as e:
            print("Please enter a valid integer.")


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


def is_valid_input(value: int) -> bool:
    """Helper function to validate input for maze"""
    if 2 > value or value > 50:
        print("Input must be between 2 and 50. Please enter values again.")
        return False
    return True


if __name__ == "__main__":
    main()
