from unittest import TestCase, mock, main
from functools import wraps

from src.screen import Window
from src.maze import Maze, Cell, MazeDrawer


def mock_gui_with_setup(func):
    """
    Decorator to mock certain drawing functionality without opening a new window
    Instantiates Window, Maze and MazeDrawer mock objects for testing
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        with mock.patch(
            "src.screen.Window.__init__",
            lambda *args, **kwargs: None,
        ), mock.patch(
            "src.maze.MazeDrawer._animate", lambda *args, **kwargs: None
        ), mock.patch(
            "src.maze.Cell.draw_wall", lambda *args, **kwargs: None
        ):
            win = Window(800, 800)
            num_cols = 12
            num_rows = 10
            m = Maze(0, 0, num_cols, num_rows, 10, 10)
            MazeDrawer(m, win)
            kwargs.update({"m": m})

            return func(*args, **kwargs)

    return wrapper


class MazeTest(TestCase):
    def test_maze_create_cells(self):
        win = Window(800, 800)
        num_cols = 12
        num_rows = 10
        m = Maze(0, 0, num_cols, num_rows, 10, 10)
        m.init_cells(win)
        self.assertEqual(
            len(m._cells),
            num_cols,
        )
        self.assertEqual(
            len(m._cells[0]),
            num_rows,
        )

    def test_maze_invalid_input(self):
        # Test for invalid number of rows
        with self.assertRaises(ValueError):
            m = Maze(0, 0, 0, 10, 10, 10)
        # Test for invalid number of columns
        with self.assertRaises(ValueError):
            m = Maze(0, 0, 10, 0, 10, 10)
            # Test for invalud cell width or height:
        with self.assertRaises(ValueError):
            m = Maze(10, 10, 10, 10, 0, 10)
            m.cell_width
        # Test for invalud cell width or height:
        with self.assertRaises(ValueError):
            m = Maze(10, 10, 10, 10, 5, 0)
            m.cell_height

    def test_maze_format_str(self):
        num_cols = 12
        num_rows = 10
        cell_width = 10
        cell_height = 10
        m = Maze(0, 0, num_cols, num_rows, cell_width, cell_height)
        self.assertEqual(
            f"{m:long}",
            f"Maze with {num_rows} rows and {num_cols} columns, cell size: {cell_width}x{cell_height}",
        )

    @mock_gui_with_setup
    def test_maze_draw_entrance_and_exit(self, m: Maze):
        top = m.get_cell(0, 0)
        bottom = m.get_cell(
            m.num_cols - 1,
            m.num_rows - 1,
        )
        self.assertEqual(top.has_top_wall, False)
        self.assertEqual(bottom.has_bottom_wall, False)

    @mock_gui_with_setup
    def test_reset_visited_cells(self, m: Maze):
        for col in m._cells:
            for cell in col:
                self.assertEqual(cell.visited, False)


if __name__ == "__main__":
    main()
