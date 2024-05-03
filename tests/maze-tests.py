from unittest import TestCase, mock, main
from functools import wraps
from tkinter import Tk, Frame, Entry

from src.screen import App, CanvasFrame
from src.maze import Maze, Cell, MazeDrawer


def mock_gui_with_setup(func):
    """
    Decorator to mock certain drawing functionality without opening a new window
    Instantiates Window, Maze and MazeDrawer mock objects for testing
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        with mock.patch("src.maze.MazeDrawer._animate", lambda *args, **kwargs: None):
            tk = Tk()
            app = App(tk)
            num_cols = 12
            num_rows = 10
            m = Maze(
                x_start=0,
                y_start=0,
                num_cols=num_cols,
                num_rows=num_rows,
                cell_width=10,
                cell_height=10,
                cells=[],
            )
            MazeDrawer(m, app.canvas_frame)
            kwargs.update({"m": m})

            return func(*args, **kwargs)

    return wrapper


class MazeTest(TestCase):
    @mock_gui_with_setup
    def test_maze_create_cells(self, m):
        num_cols = 12
        num_rows = 10
        self.assertEqual(
            len(m.cells),
            num_cols,
        )
        self.assertEqual(
            len(m.cells[0]),
            num_rows,
        )

    def test_maze_format_str(self):
        num_cols = 12
        num_rows = 10
        cell_width = 10
        cell_height = 10
        m = Maze(
            x_start=0,
            y_start=0,
            num_cols=num_cols,
            num_rows=num_rows,
            cell_width=cell_width,
            cell_height=cell_height,
            cells=[],
        )
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
        for col in m.cells:
            for cell in col:
                self.assertEqual(cell.visited, False)

    def test_canvas_invalid_inputs(self):
        # Creating an App instance
        tk = Tk()
        app = App(tk)
        app._create_widgets()

        # Mocking the Entry widget
        entry_mock = mock.Mock(spec=Entry)
        entry_mock.get.side_effect = ["1", "51", "in"]

        # Patching the Entry widget on the Window instance
        with mock.patch.object(app, "row_input", entry_mock), mock.patch.object(
            app, "col_input", entry_mock
        ):
            with self.assertRaises(ValueError):
                app.canvas_frame._validate_input()


if __name__ == "__main__":
    main()
