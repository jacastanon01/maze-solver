import time
import random
from typing import Dict, Tuple, List

from src.cell import Cell


class Maze:
    """
    Data class for Maze structure

    Attributes
    -----
    - x_start : int
        Represents how many pixels from the left the maze runner should start

    - y_start : int
        Represents how many pixels from the top the maze runner should start

    - num_cols : int
        Total cell columns

    - num_rows : int
        Total cell rows

    - cell_width : int
        Cell width

    - cell_height : int
        Cell height

    - cells : list[list[Cell]]
        List of cells in the maze

    - seed : int : Random seed


    Methods
    -----
    - get_neighbor_coords(col: int, row: int, direction: str) -> Tuple[Tuple[int, int], str]
        Returns the coordinates of the neighbor cell and the direction of the wall that connects them

    - get_cell(col: int, row: int) -> Cell
        Returns the cell at the specified column and row

    - get_neighbor_coords(col: int, row: int, direction: str) -> Tuple[Tuple[int, int], str]:
        Returns all the neboring cells from a cell in a given position

    - reset_visited_cells -> None
        Resets all cell's visited attribute to False
    """

    def __init__(
        self,
        x_start: int,
        y_start: int,
        num_cols: int,
        num_rows: int,
        cell_width: int,
        cell_height: int,
        seed=None,
    ):
        self._x_start = x_start
        self._y_start = y_start
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_width = cell_width
        self._cell_height = cell_height
        self._cells = []
        if seed:
            self._seed = random.seed(cell_width)

    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case "short":
                return f"{self.num_cols}x{self.num_rows}"
            case "long":
                return f"Maze with {self.num_rows} rows and {self.num_cols} columns, cell size: {self.cell_width}x{self.cell_height}"
            case _:
                return self.__repr__()

    def __repr__(self) -> str:
        return f"Maze({self.x_start}, {self.x_start}, {self.num_rows}, {self.num_cols}, {self.cell_width}, {self.cell_height})"

    @property
    def x_start(self) -> int:
        return self._x_start

    @x_start.setter
    def x_start(self, new_x) -> None:
        self._x_start = new_x

    @property
    def y_start(self) -> int:
        return self._y_start

    @y_start.setter
    def y_start(self, new_y: int) -> None:
        self._y_start = new_y

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

    @property
    def start_cell(self) -> Cell | None:
        if not self._cells:
            return None
        return self._cells[0][0]

    @property
    def end_cell(self) -> Cell | None:
        if not self._cells:
            return None
        return self._cells[self.num_cols - 1][self.num_rows - 1]

    @property
    def cells(self) -> List[List[Cell]]:
        return self._cells

    @cells.setter
    def cells(self, new_cells: List[List[Cell]]) -> None:
        if len(new_cells) == self.num_cols:
            self._cells = new_cells

    def get_cell(self, col: int, row: int) -> Cell | None:
        """
        Returns the cell at the specified row and column.
        Returns None if the cell is out of bounds.
        """
        if 0 <= row < self._num_rows and 0 <= col < self._num_cols:
            return self._cells[col][row]
        else:
            return None

    def get_neighbor_coords(
        self, col: int, row: int, direction: str
    ) -> Tuple[Tuple[int, int], str]:
        """
        Dictionary to map direction to neighbor coordinates and opposite wall
        -----
        adjacent_cells = {
            "top": ((col, row - 1, ), "bottom"),
            "right": ((col + 1, row), "left"),
            "bottom": ((col, row + 1), "top"),
            "left": ((col - 1, row), "right"),
        }
        return adjacent_cells[direction]
        """
        adjacent_cells = {
            "top": (
                (
                    col,
                    row - 1,
                ),
                "bottom",
            ),
            "right": ((col + 1, row), "left"),
            "bottom": ((col, row + 1), "top"),
            "left": ((col - 1, row), "right"),
        }
        return adjacent_cells[direction]

    def reset_visited_cells(self):
        """Sets all cells in matrix to unvisited"""
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._cells[col][row].visited = False


class MazeDrawer:
    """
    Handles maze logic to draw cells to screen and handles navigation to cells

    Attributes
    -----
    - _maze : Maze

    - _canvas : CanvasFrame

    Methods:
    ----
    - init_cells
        Initializes the matrix with Cell objects

    - create_cells
        Initializes the matrix of cells and draws them to screen

    - draw_cell(i: int, j: int)
        Draws a cell to screen at specified row/column position

    - animate
        Animates maze by drawing cells one at a time and allows us to visulize our algorithm

    - draw_entrance_and_exit
        Draws entrance and exit to maze by removing the top wall of the first cell and
        the bottom wall of the last cell

    - break_walls_r(col : int, row : int)
        Recursive backtracking algorithm to create maze
    """

    def __init__(self, maze: Maze, frame: "CanvasFrame"):
        self._maze = maze
        self._canvas = frame

        self._init_cells()
        self._create_cells()
        self._create_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._maze.reset_visited_cells()

    def _init_cells(self) -> None:
        """Initializes the matrix of a maze"""
        new_cells = [
            [Cell(self._canvas) for _ in range(self._maze.num_rows)]
            for _ in range(self._maze.num_cols)
        ]
        self._maze.cells = new_cells

    def _create_cells(self) -> None:
        """Draws matrix of cells to draw to screen"""

        if self._maze.num_cols <= 0 or self._maze.num_rows <= 0:
            raise ValueError("Maze must have a positive number of rows and columns")
        for i in range(self._maze.num_cols):
            for j in range(self._maze.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, x: int, y: int) -> None:
        """Calculates the x/y positions and draws the cell"""
        cell = self._maze.get_cell(x, y)

        cell_x1 = self._maze.x_start + x * self._maze.cell_width
        cell_y1 = self._maze.y_start + y * self._maze.cell_height
        cell_x2 = cell_x1 + self._maze.cell_width
        cell_y2 = cell_y1 + self._maze.cell_height

        cell.draw_wall(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate()

    def _animate(self, path=False) -> None:
        """
        Animates maze by drawing cells one at a time and allows us to visulize our algorithm

        Parameters
        -----
        - path ?: bool : Flag to indicate if method was called to draw cells or path.
            Defaults to False
            Used to determine time to sleep while redrawing
        """
        self._canvas.window.redraw()
        if path:
            time.sleep(0.1)
        else:
            pass

    def _create_entrance_and_exit(self) -> None:
        """Creates entrance and exit to maze by removing the top wall of the first cell and
        the bottom wall of the last cell"""
        top_cell = self._maze.get_cell(0, 0)
        bottom_cell = self._maze.get_cell(
            self._maze.num_cols - 1,
            self._maze.num_rows - 1,
        )
        top_cell.has_top_wall = False
        bottom_cell.has_bottom_wall = False
        top_cell.visited = True

        self._draw_cell(0, 0)
        self._draw_cell(self._maze.num_cols - 1, self._maze.num_rows - 1)

    def _break_walls_r(self, col: int, row: int) -> None:
        """
        Uses a depth-first approach to setting the walls of the maze.
        This method is used to break the walls of the maze in a random order and set every cell to visited.
        """
        current_cell: Cell = self._maze.get_cell(col, row)
        current_cell.visited = True

        directions = ["top", "right", "bottom", "left"]
        random.shuffle(directions)

        for direction in directions:
            neighbor_coords, opposite_direction = self._maze.get_neighbor_coords(
                col, row, direction
            )
            neighbor_col, neighbor_row = neighbor_coords

            if (
                0 <= neighbor_row < self._maze.num_rows
                and 0 <= neighbor_col < self._maze.num_cols
            ):
                neighbor = self._maze.get_cell(neighbor_col, neighbor_row)

                if neighbor and not neighbor.visited:
                    # Break the wall between current cell and neighbor
                    setattr(current_cell, f"has_{direction}_wall", False)
                    setattr(neighbor, f"has_{opposite_direction}_wall", False)

                    # Recursively call the function for the neighbor cell
                    self._break_walls_r(neighbor_col, neighbor_row)
            self._draw_cell(col, row)


class MazeSolver:
    """
    Contains solvers for mazes.

    Attributes
    ----------
    - maze : Maze
        The maze object.

    - drawer : MazeDrawer
        The maze drawer object.

    Methods
    -------
    - solve() -> bool:
        Solves the maze using depth-first traversal to find the exit path.

    - _dfs_r(col: int, row: int) -> bool:
        Performs depth-first solution to find the end of the maze.
    """

    def __init__(self, maze: Maze, md: MazeDrawer):
        self._maze = maze
        self._drawer = md

    def solve(self) -> bool:
        """
        Solves maze using depth-first traversal to find exit path
        Calls self._dfs_r from the first cell
        return self._dfs_r(0, 0)
        """
        return self._dfs_r(0, 0)

    def _dfs_r(self, col: int, row: int) -> bool:
        """
        The _solve_r method returns True if the current cell is an end cell,
        OR if it leads to the end cell. It returns False if the current cell is a loser cell.
        Performs depth-first solution to find end of maze
        """

        current_cell = self._maze.get_cell(col, row)
        current_cell.visited = True

        if current_cell is self._maze.end_cell:
            return True

        directions = ["top", "right", "bottom", "left"]
        random.shuffle(directions)

        for direction in directions:
            neighbor_coords, opposite_direction = self._maze.get_neighbor_coords(
                col, row, direction
            )
            neighbor = self._maze.get_cell(*neighbor_coords)

            neighbor_col, neighbor_row = neighbor_coords

            # Boundary check
            if (
                0 <= neighbor_row < self._maze.num_rows
                and 0 <= neighbor_col < self._maze.num_cols
            ):

                # If the neighbor hasn't been visited, recurse on it
                if (
                    neighbor
                    and not neighbor.visited
                    and not getattr(neighbor, f"has_{opposite_direction}_wall")
                ):
                    # draw move to neighbor
                    current_cell.draw_move(neighbor)
                    self._drawer._animate(path=True)
                    if self._dfs_r(neighbor_col, neighbor_row):
                        return True
                    else:
                        neighbor.draw_move(current_cell, undo=True)
                        self._drawer._animate(path=True)

                    self._dfs_r(neighbor_col, neighbor_row)

        return False
