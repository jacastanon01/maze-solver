import time

from src.screen import Window, Line, Point


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
    draw(x1 : int, y1 : int, x2 : int, y2 : int) -> None : Draws cell to screen
    draw_move(to_cell : Cell, undo ?: bool) -> None : Draws line thru cells
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

    def __repr__(self):
        num_walls = [
            1 if i else 0
            for i in [
                self.has_left_wall,
                self.has_top_wall,
                self.has_right_wall,
                self.has_bottom_wall,
            ]
        ]
        return f"Cell has {num_walls.count(1)} walls"

    def draw(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Draws walls of cell depending on point positions and wall flags

        Parameters
        -----
        x1, y1 : int
            Represents top-left point of cell. To be used to draw walls
        x2, y2 : int
            Represents bottom-right point of cell. To be used to draw walls
        """

        wall_directions = {
            "top": (x1, y1, x2, y1),
            "right": (x2, y2, x2, y1),
            "bottom": (x2, y2, x1, y2),
            "left": (x1, y1, x1, y2),
        }

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        for direction in wall_directions:
            fill_color = (
                "white" if not getattr(self, f"has_{direction}_wall") else "black"
            )
            point1 = wall_directions[direction][:2]
            point2 = wall_directions[direction][2:]
            self._window.draw_line(Line(Point(*point1), Point(*point2)), fill_color)

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
        if not isinstance(to_cell, Cell):
            raise ValueError("Invalid cell instance")

        line_color = "gray"
        if undo:
            line_color = "red"

        center_x_source = (self.x1 + self.x2) // 2
        center_y_source = (self.y1 + self.y2) // 2

        center_x_destination = (to_cell.x1 + to_cell.x2) // 2
        center_y_destination = (to_cell.y1 + to_cell.y2) // 2

        line = Line(
            Point(center_x_source, center_y_source),
            Point(center_x_destination, center_y_destination),
        )

        self._window.draw_line(line, fill_color=line_color)


class Maze:
    """
    Data class for Maze structure

    Attributes
    -----
    x_start : int : Represents how many pixels from the left the maze runner should start
    x_start : int : Represents how many pixels from the top the maze runner should start
    num_cols : int : Total cell columns
    num_rows : int : Total cell rows
    cell_width : int : Cell width
    cell_height : int : Cell height
    cells : list[list[Cell]] : List of cells in the maze

    Methods
    -----
    init_cells -> None : Initializes the matrix of a maze
    get_cell(i: int, j: int) -> Cell : Returns the cell at the specified row and column
    """

    def __init__(
        self,
        x_start: int,
        y_start: int,
        num_cols: int,
        num_rows: int,
        cell_width: int,
        cell_height: int,
    ):
        if num_cols <= 0:
            raise ValueError("Maze must have a positive number of columns")
        if num_rows <= 0:
            raise ValueError("Maze must have a positive number of rows")
        if cell_width <= 0:
            raise ValueError("Cell width must be greater than zero")
        if cell_height <= 0:
            raise ValueError("Cell height must be greater than zero")
        self._x_start = x_start
        self._y_start = y_start
        self._num_cols = num_cols
        self._num_rows = num_rows
        self._cell_width = cell_width
        self._cell_height = cell_height
        self._cells = []

    def __format__(self, format_spec):
        match format_spec:
            case "short":
                return f"{self.num_cols}x{self.num_rows}"
            case "long":
                return f"Maze with {self.num_rows} rows and {self.num_cols} columns, cell size: {self.cell_width}x{self.cell_height}"
            case _:
                return self.__repr__()

    def __repr__(self):
        return f"Maze({self.x_start}, {self.x_start}, {self.num_rows}, {self.num_cols}, {self.cell_width}, {self.cell_height})"

    @property
    def x_start(self) -> int:
        return self._x_start

    @property
    def y_start(self) -> int:
        return self._y_start

    @property
    def num_cols(self) -> int:
        return self._num_cols

    @property
    def num_rows(self) -> int:
        return self._num_rows

    @property
    def cell_width(self) -> int:
        return self._cell_width

    @property
    def cell_height(self) -> int:
        return self._cell_height

    def init_cells(self, win: Window) -> None:
        """Initializes the matrix of a maze"""
        self._cells = [
            [Cell(win) for _ in range(self._num_cols)] for _ in range(self._num_rows)
        ]

    def get_cell(self, row: int, col: int) -> Cell | None:
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
    create_cells -> None : Initializes the matrix of cells and draws them to screen
    draw_cell(i: int, j: int) -> None : Draws a cell to screen at specified row/column position
    animate -> None : Animates maze by drawing cells one at a time and allows us to visulize our algorithm
    draw_entrance_and_exit -> None : Draws entrance and exit to maze by removing the top wall of the first cell and
    the bottom wall of the last cell
    """

    def __init__(self, maze: Maze, window: Window):
        self._maze = maze
        self._window = window

        self._maze.init_cells(self._window)
        self._create_entrance_and_exit()
        self._create_cells()

    def _create_cells(self) -> None:
        """Draws matrix of cells to draw to screen"""
        if self._maze.num_cols <= 0 or self._maze.num_rows <= 0:
            raise ValueError("Maze must have a positive number of rows and columns")
        for i in range(self._maze.num_rows):
            for j in range(self._maze.num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, x: int, y: int) -> None:
        """Calculates the x/y positions and draws the cell"""
        cell = self._maze.get_cell(x, y)

        cell_x1 = self._maze.x_start + x * self._maze.cell_width
        cell_y1 = self._maze.y_start + y * self._maze.cell_height
        cell_x2 = cell_x1 + self._maze.cell_width
        cell_y2 = cell_y1 + self._maze.cell_height

        cell.draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate()

    def _animate(self) -> None:
        """Animates maze by drawing cells one at a time and allows us to visulize our algorithm"""
        self._window.redraw()
        time.sleep(0.05)

    def _create_entrance_and_exit(self) -> None:
        """Creates entrance and exit to maze by removing the top wall of the first cell and
        the bottom wall of the last cell"""
        top_cell = self._maze.get_cell(0, 0)
        bottom_cell = self._maze.get_cell(
            self._maze.num_rows - 1, self._maze.num_cols - 1
        )
        top_cell.has_top_wall = False
        bottom_cell.has_bottom_wall = False
