import time
import random
from typing import Dict, Tuple, List
from dataclasses import dataclass

from src.cell import Cell, Line, Point


@dataclass
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


    Methods
    -----
    - get_neighbor_coords(col: int, row: int, direction: str) -> Tuple[Tuple[int, int], str]
        Returns the coordinates of the neighbor cell and the direction of the wall that connects them

    - get_cell(col: int, row: int) -> Cell
        Returns the cell at the specified column and row

    - reset_visited_cells -> None
        Resets all cell's visited attribute to False
    """

    x_start: int
    y_start: int
    num_cols: int
    num_rows: int
    cell_width: int
    cell_height: int
    cells: List[List[Cell]]

    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case "short":
                return f"{self.num_cols}x{self.num_rows}"
            case "long":
                return f"Maze with {self.num_rows} rows and {self.num_cols} columns, cell size: {self.cell_width}x{self.cell_height}"
            case _:
                return self.__repr__()

    @property
    def start_cell(self) -> Cell | None:
        if not self.cells:
            return None
        return self.cells[0][0]

    @property
    def end_cell(self) -> Cell | None:
        if not self.cells:
            return None
        return self.cells[self.num_cols - 1][self.num_rows - 1]

    def get_cell(self, col: int, row: int) -> Cell | None:
        """
        Returns the cell at the specified row and column.
        Returns None if the cell is out of bounds.
        """
        if 0 <= row < self.num_rows and 0 <= col < self.num_cols:
            return self.cells[col][row]
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
            "top": ((col, row - 1), "bottom"),
            "right": ((col + 1, row), "left"),
            "bottom": ((col, row + 1), "top"),
            "left": ((col - 1, row), "right"),
        }
        return adjacent_cells[direction]

    def reset_visited_cells(self):
        """Sets all cells in matrix to unvisited"""
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self.cells[col][row].visited = False


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

    # def draw_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
    #     """
    #     Creates a line from coordinates to draw on screen

    #     Parameters
    #     -----
    #         x1, y1 : int : Represents top-left point of cell. To be used to draw walls

    #         x2, y2 : int : Represents bottom-right point of cell. To be used to draw walls
    #     """

    #     self.x1 = x1
    #     self.y1 = y1
    #     self.x2 = x2
    #     self.y2 = y2

    #     # wall_directions = self.get_wall_directions()
    #     wall_directions = {
    #         "top": (self.x1, self.y1, self.x2, self.y1),
    #         "right": (self.x2, self.y2, self.x2, self.y1),
    #         "bottom": (self.x2, self.y2, self.x1, self.y2),
    #         "left": (self.x1, self.y1, self.x1, self.y2),
    #     }

    #     for direction in wall_directions:
    #         fill_color = (
    #             "white" if not getattr(self, f"has_{direction}_wall") else "black"
    #         )

    #         point1 = wall_directions[direction][:2]
    #         point2 = wall_directions[direction][2:]
    #         wall_line = Line(Point(*point1), Point(*point2))
    #         self._canvas.draw_line(wall_line, fill_color)

    # def draw_move(self, to_cell: "Cell", undo=False) -> None:
    #     """
    #     Draws lines that navigates between cells

    #     Parameters
    #     -----
    #     to_cell : Cell : Specifies next cell to draw line toward

    #     undo ?: bool : Indicates whether line is backtracking
    #     """
    #     if not isinstance(to_cell, Cell):
    #         raise ValueError("Invalid cell instance")

    #     line_color = "gray"
    #     if undo:
    #         line_color = "red"

    #     center_x_source = (self.x1 + self.x2) // 2
    #     center_y_source = (self.y1 + self.y2) // 2

    #     center_x_destination = (to_cell.x1 + to_cell.x2) // 2
    #     center_y_destination = (to_cell.y1 + to_cell.y2) // 2

    #     line = Line(
    #         Point(center_x_source, center_y_source),
    #         Point(center_x_destination, center_y_destination),
    #     )
    #     self._canvas.draw_line(line, fill_color=line_color)


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
