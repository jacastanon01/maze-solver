import time

from screen import Window, CanvasManager


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

        if self._has_left_wall:
            self._window.draw_line(
                Line(Point(x1, y1), Point(x1, y2)),
            )
        if self._has_top_wall:
            self._window.draw_line(
                Line(Point(x1, y1), Point(x2, y1)),
            )
        if self._has_right_wall:
            self._window.draw_line(
                Line(Point(x2, y1), Point(x2, y2)),
            )
        if self._has_bottom_wall:
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


class MazeRenderer:
    """
    Generates a a matrix of cells and handles behavior to re-render maze

    Attributes
    -----
    num_cols : int : Total cell columns
    num_rows : int : Total cell rows
    cell_size_x : int : Cell width
    cell_size_y : int : Cell height
    window : Window

    Methods
    -----
    create_cells -> None
    draw_cells(i : int, j : int) -> None
    animate -> None
    """

    def __init__(
        self,
        num_cols: int,
        num_rows: int,
        cell_size_x: int,
        cell_size_y: int,
        window: Window,
    ):
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._window = window

    def _create_cells(self):
        """Creates matrix of cells and draws to screen"""
        self._cells = [
            [Cell(self._window) for _ in range(self.num_cols + 1)]
            for _ in range(self.num_rows + 1)
        ]

        for i in range(len(self._cells)):
            for j in len(self._cells):
                self._draw_cells(i, j)

    def _draw_cells(self, i: int, j: int) -> None:
        """Calculates the x/y position and draws the cell"""
        self.x = i * (self.cell_size_x + 1) + self.cell_size_x
        self.y = j * (self.cell_size_y + 1) + self.cell_size_y

        self._cells[i][j].draw(
            self.x, self.y, self.x + self.cell_size_x, self.y + self.cell_size_y
        )
        self._animate()

    def _animate(self) -> None:
        """Animates maze by drawing cells one at a time and allows us to visulize our algorithm."""
        self._window.redraw()
        time.sleep(0.05)


# TODO: Decouple the drawing logic from maze class
class Maze:
    """
    Class that contains a matrix of cell objects

    Attributes
    -----
    x : int : Represents how many pixels from the left the maze runner should start
    y : int : Represents how many pixels from the top the maze runner should start
    """

    def __init__(
        self,
        x: int,
        y: int,
    ):
        self.x = x
        self.y = y

    def _create_cells(self):
        """Creates matrix of cells and draws to screen"""
        self._cells = [
            [Cell(self._window) for _ in range(self.num_cols + 1)]
            for _ in range(self.num_rows + 1)
        ]

        for i in range(len(self._cells)):
            for j in len(self._cells):
                self._draw_cells(i, j)

    def _draw_cells(self, i: int, j: int) -> None:
        """Calculates the x/y position and draws the cell"""
        self.x = i * (self.cell_size_x + 1) + self.cell_size_x
        self.y = j * (self.cell_size_y + 1) + self.cell_size_y

        self._cells[i][j].draw(
            self.x, self.y, self.x + self.cell_size_x, self.y + self.cell_size_y
        )
        self._animate()

    def _animate(self) -> None:
        """Animates maze by drawing cells one at a time and allows us to visulize our algorithm."""
        self._window.redraw()
        time.sleep(0.05)
