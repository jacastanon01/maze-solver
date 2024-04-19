from screen import Screen


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

    def __init__(self, screen: Screen):
        self._window = screen
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None

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
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

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

        x_source = (self._x1 + self._x2) // 2
        y_source = (self._y1 + self._y2) // 2

        x_destination = (to_cell._x1 + to_cell._x2) // 2
        y_destination = (to_cell._y1 + to_cell._y2) // 2

        line = Line(Point(x_source, y_source), Point(x_destination, y_destination))

        self._window.draw_line(line, fill_color=line_color)


# TODO: Decouple the drawing logic from maze class
class Maze:
    """
    Class that contains a matrix of cell objects

    Attributes
    -----
    x : int : Represents how many pixels from the left maze should start
    y : int : Represents how many pixels from the top maze should start
    num_cols : int : Total cell columns
    num_rows : int : Total cell rows
    cell_size_x : int : Cell width
    cell_size_y : int : Cell height
    window : Screen

    Methods
    -----
    create_cells -> None
    draw_cell(i : int, j : int) -> None
    animate -> None
    """

    def __init__(
        self,
        x: int,
        y: int,
        num_cols: int,
        num_rows: int,
        cell_size_x: int,
        cell_size_y: int,
        screen: Screen,
    ):
        self.x = x
        self.y = y
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._window = screen
        self._create_cells()

    def _create_cells(self):
        """Creates matrix of cells and draws to screen"""
        self._cells = [
            [Cell(self._window) for _ in range(self.num_cols + 1)]
            for _i in range(self.num_rows + 1)
        ]

        for i in range(len(self._cells)):
            for j in len(i):
                self._draw_cells(i, j)

    def _draw_cells(self, i: int, j: int):
        """Calculates the x/y position and draws the cell"""
