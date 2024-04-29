from typing import Tuple


def initialize_maze(cols_entry: int, rows_entry: int) -> Tuple["Maze", "Window"]:
    """
    Validates column and row entries and constructs a Maze instance with the given parameters
    Calculates size of window from given parameters
    Calls render_maze to draw maze to canvas

    Parameters
    -----
    - cols_entry : int
    - rows_entry : int
    """

    from src.maze import Maze, Window

    print(
        "Welcome to the Maze Solver where you can visualize the path you take to solve a maze.",
        end=f"\n{'=' * 10}\n",
    )

    width, height, padding_x, padding_y, cols, rows = calculate_window_sizes(
        cols_entry, rows_entry
    )
    cell_cols = 20 if cols < 25 else 10
    cell_rows = 20 if rows < 25 else 10
    my_maze = Maze(padding_x, padding_y, cols, rows, cell_cols, cell_rows)
    # window = Window(width, height)
    # render_maze(my_maze, window)
    return my_maze


def calculate_window_sizes(cols: int, rows: int) -> Tuple[int, int, int, int, int, int]:
    """
    Takes user input of columns and rows to calculate the size of a window based on those values.
    Calls draw_maze with input values to draw the maze
    """
    if not is_valid_input(cols):
        raise ValueError("Maze must have between 2 and 50 columns")
    if not is_valid_input(rows):
        raise ValueError("Maze must have between 2 and 50 rows")

    print(f"Generating a {cols} by {rows} maze...")
    desired_padding = 10
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

    padding_x = (window_size - maze_width) / 2
    padding_y = (window_size - maze_height) / 2

    return (
        window_size,
        window_size,
        padding_x,
        padding_y,
        cols,
        rows,
    )


def render_maze(maze: "Maze", window: "Window") -> None:
    """
    Draws a maze with the given parameters

    Parameters
    -----
    - maze : Maze
    - window : Window
    """

    from src.maze import MazeDrawer

    drawer = MazeDrawer(maze, window.canvas)
    window.start()
    window.redraw()


def solve_maze(maze: "Maze", drawer: "MazeDrawer") -> None:
    """Creates MazeSolver instance to call solve method on maze"""

    from src.maze import MazeSolver

    solution = MazeSolver(maze, drawer)
    solution.solve()


def is_valid_input(value: int) -> bool:
    """Helper function to validate input for maze"""
    if 2 > value or value > 50:
        print("Input must be between 2 and 50. Please enter values again.")
        return False
    return True
