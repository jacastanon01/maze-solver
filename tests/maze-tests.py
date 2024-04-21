import unittest

from src.screen import Window
from src.maze import Maze, Cell


class MazeTest(unittest.TestCase):
    def test_maze_create_cells(self):
        win = Window(800, 800)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1.init_cells(win)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
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

    def test_maze_format(self):
        num_cols = 12
        num_rows = 10
        cell_width = 10
        cell_height = 10
        maze = Maze(0, 0, num_cols, num_rows, cell_width, cell_height)
        self.assertEqual(
            f"{maze:long}",
            f"Maze with {num_rows} rows and {num_cols} columns, cell size: {cell_width}x{cell_height}",
        )
        print(f"{maze:long}")


if __name__ == "__main__":
    unittest.main()
