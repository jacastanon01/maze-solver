import unittest

from src.maze import Maze, Cell


class MazeTest(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
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
