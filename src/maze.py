import time

from screen import Window, Line, Point


class Cell:
    """
    A class to represent different cells in a maze

    Attributes
    -----
    window : Screen
        Represents Tkinter window to place cells
    has_{side}_wall: bool
        Flags to indicate which walls to draw on cell
    x1, y1 : int
        Represents bottom-left point of cell. To be used to draw walls
    x2, y2 : int
        Represents top-right point of cell. To be used to draw walls

    Methods
    -----
    draw(x1 : int, y1 : int, x2 : int, y2 : int) -> None
    draw_move(to_cell : Cell, undo ?: bool) -> None
    """

    def __init__(self, window: Window):
        self._window = window
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

    def draw(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Draws walls of cell depending on point positions and wall flags

        Parameters
        -----
        x1, y1 : int
            Represents bottom-left point of cell. To be used to draw walls
        x2, y2 : int
            Represents top-right point of cell. To be used to draw walls
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        if self.has_left_wall:
            self._window.draw_line(
                Line(Point(x1, y1), Point(x1, y2)),
            )
        if self.has_top_wall:
            self._window.draw_line(
                Line(Point(x1, y1), Point(x2, y1)),
            )
        if self.has_right_wall:
            self._window.draw_line(
                Line(Point(x2, y1), Point(x2, y2)),
            )
        if self.has_bottom_wall:
            self._window.draw_line(
                Line(Point(x1, y2), Point(x2, y2)),
            )

    def draw_move(self, to_cell: "Cell", undo=False) -> None:
        """
        Draws lines that navigates between cells

        Parameters
        -----
        to_cell : Cell
            Specifies next cell to draw line toward
        undo ?: bool
            Indicates whether line is backtracking
        """
        line_color = "gray"

        if undo:
            line_color = "red"

        x_source = (self.x1 + self.x2) // 2
        y_source = (self.y1 + self.y2) // 2

        x_destination = (to_cell.x1 + to_cell.x2) // 2
        y_destination = (to_cell.y1 + to_cell.y2) // 2

        line = Line(Point(x_source, y_source), Point(x_destination, y_destination))

        self._window.draw_line(line, fill_color=line_color)


class Maze:
    """
    Data class for Maze structure

    Attributes
    -----
    x : int : Represents how many pixels from the left the maze runner should start
    y : int : Represents how many pixels from the top the maze runner should start
    num_cols : int : Total cell columns
    num_rows : int : Total cell rows
    cell_size_x : int : Cell width
    cell_size_y : int : Cell height
    cells : list[Cell] : List of cells in the maze
    """

    def __init__(
        self,
        x: int,
        y: int,
        num_cols: int,
        num_rows: int,
        cell_size_x: int,
        cell_size_y: int,
    ):
        self._x = x
        self._y = y
        self._num_cols = num_cols
        self._num_rows = num_rows
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._cells = []

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    @property
    def num_cols(self) -> int:
        return self._num_cols

    @property
    def num_rows(self) -> int:
        return self._num_rows

    @property
    def cell_size_x(self) -> int:
        return self._cell_size_x

    @property
    def cell_size_y(self) -> int:
        return self._cell_size_y

    def init_cells(self, win: Window):
        """Initializes the matrix of a maze"""
        self._cells = [
            [Cell(win) for _ in range(self._num_cols)] for _ in range(self._num_rows)
        ]

    def get_cell(self, row: int, col: int):
        """Returns the cell at the specified row and column."""
        if 0 <= row < self._num_rows and 0 <= col < self._num_cols:
            return self._cells[row][col]
        else:
            return None


class MazeDrawer:
    """
    Handles maze logic to draw cells to screen and handles navigation to cells

    Attributes
    -----
    maze : Maze

    Methods:
    ----
    draw_cells(i : int, j : int) -> None
    animate -> None
    """

    def __init__(self, maze: Maze, window: Window):
        self._maze = maze
        self._window = window
        self._maze.init_cells(self._window)

    def _create_cells(self):
        """Creates matrix of cells to draw to screen"""
        for i in range(self._maze.num_rows):
            for j in range(self._maze.num_cols):
                self._draw_cells(i, j)

    def _draw_cells(self, i: int, j: int) -> None:
        """Calculates the x/y positions and draws the cell"""
        cell = self._maze.get_cell(i, j)

        cell_x1 = self._maze.x + i * self._maze.cell_size_x
        cell_y1 = self._maze.y + j * self._maze.cell_size_y
        cell_x2 = cell_x1 + self._maze.cell_size_x
        cell_y2 = cell_y1 + self._maze.cell_size_y

        cell.draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate()

    def _animate(self) -> None:
        """Animates maze by drawing cells one at a time and allows us to visulize our algorithm"""
        self._window.redraw()
        time.sleep(0.05)


# TODO: Decouple the drawing logic from maze class


# class MazeGenerator:
#     """
#     Generates a matrix of cells and handles behavior to re-render maze

#     Attributes
#     -----
#     maze : Maze

#     Methods
#     -----
#     create_cells -> None
#     """

#     def __init__(self, maze: Maze, window: Window):
#         self._window = window
#         self._maze = maze

#     def _create_cells(self):
#         """Creates matrix of cells to draw to screen"""
#         self._maze.init_cells()
#         drawer = MazeDrawer(self._maze, self._window)
#         for i in range(self._maze.num_rows + 1):
#             for j in range(self._maze.num_cols + 1):
#                 self._maze._cells[i][j] = Cell(self._window)
#                 drawer._draw_cells(i, j)
