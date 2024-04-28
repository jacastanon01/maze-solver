import time
import random
from typing import Dict, Tuple, List

from src.screen import Window, Line, Point, CanvasFrame


class Cell:
    """
    A class to represent different cells in a maze

    Attributes
    -----
    - window : CanvasFrame
        Interface for drawing onto canvas
    - x1, y1 : int
        Represents bottom-left point of cell. To be used to draw walls
    - x2, y2 : int
        Represents top-right point of cell. To be used to draw walls
    - has_{side}_wall: bool
        Flags to indicate which walls to draw on cell
    - visited : list : Keeps track of which cell has already been added to path in DFS

    Methods
    -----
    - draw(x1 : int, y1 : int, x2 : int, y2 : int)  : Draws cell to screen
    - draw_move(to_cell : Cell, undo ?: bool)  : Draws line thru cells
    - get_wall_directions -> dict[{str: tuple(int)}] : Retrieves the coordinates for a given wall direction
    """

    # Dunder methods
    def __init__(self, window: CanvasFrame):
        self._canvas = window
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.visited = False

    def __repr__(self):
        return "\n------\n".join((
            f"Cell(x1: {self.x1}, y1: {self.y1}, x2: {self.x2}, y2: {self.y2})",
            f"\nwalls: {"top" if self.has_top_wall else "no top"} {"left" if self.has_left_wall else "no left"}, {"right" if self.has_right_wall else "no right"}, {"bottom" if self.has_bottom_wall else "no bottom"}",
        ))

    def __format__(self, format_spec: str):
        """
        Parameters
        ------
        format_spec : str : takes the following key mappings
            "w": number of walls belonging to this cell
            "v": indicates if instance has been visited during path generation
            "c": returns cell's coordinates
        """
        format_spec = set(format_spec)
        if "w" in format_spec:        
            num_walls = [
                1 if i else 0
                for i in [
                    self.has_left_wall,
                    self.has_top_wall,
                    self.has_right_wall,
                    self.has_bottom_wall,
                ]
            ]
            format_str = f"Cell has {num_walls.count(1)} walls: "
            for wall in ["top", "right", "bottom", "left"]:
                if getattr(self, f"has_{wall}_wall"):
                    format_str += f"{wall} "
            return format_str
        if "v" in format_spec:
            return f"Cell is {self.visited and 'visited' or 'not visited'}"
        if "c" in format_spec:
            if self.x1 and self.y1 and self.x2 and self.y2:
                center_x_source = (self.x1 + self.x2) // 2
                center_y_source = (self.y1 + self.y2) // 2
                return f" with the following coordinates:\nX: {center_x_source}\nY: {center_y_source}"
        return self.__repr__()

    def draw_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Creates a line from coordinates to draw on screen
        

        Parameters
        -----
            x1, y1 : int : Represents top-left point of cell. To be used to draw walls
            x2, y2 : int : Represents bottom-right point of cell. To be used to draw walls
        """

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        # wall_directions = self.get_wall_directions()
        wall_directions = {
            "top": (self.x1, self.y1, self.x2, self.y1),
            "right": (self.x2, self.y2, self.x2, self.y1),
            "bottom": (self.x2, self.y2, self.x1, self.y2),
            "left": (self.x1, self.y1, self.x1, self.y2),
        }

        for direction in wall_directions:
            fill_color = (
                "white" if not getattr(self, f"has_{direction}_wall") else "black"
            )

            point1 = wall_directions[direction][:2]
            point2 = wall_directions[direction][2:]
            wall_line = Line(Point(*point1), Point(*point2))
            self._canvas.draw_line(wall_line, fill_color)

    def draw_move(self, to_cell: "Cell", undo=False) -> None:
        """
        Draws lines that navigates between cells

        Parameters
        -----
        to_cell : Cell : Specifies next cell to draw line toward
        undo ?: bool : Indicates whether line is backtracking
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
        self._canvas.draw_line(line, fill_color=line_color)


class Maze:
    """
    Data class for Maze structure

    Attributes
    -----
    - x_start : int : Represents how many pixels from the left the maze runner should start
    - y_start : int : Represents how many pixels from the top the maze runner should start
    - num_cols : int : Total cell columns
    - num_rows : int : Total cell rows
    - cell_width : int : Cell width
    - cell_height : int : Cell height
    - cells : list[list[Cell]] : List of cells in the maze
    - seed : int : Random seed

    Methods
    -----
    - get_neighbor_coords(col: int, row: int, direction: str) -> Tuple[Tuple[int, int], str]
        Returns the coordinates of the neighbor cell and the direction of the wall that connects them  
    - get_cell(col: int, row: int) -> Cell : Returns the cell at the specified column and row
    - get_neighbor_coords(col: int, row: int, direction: str) -> Tuple[Tuple[int, int], str]:
        Returns all the neboring cells from a cell in a given position
    - reset_visited_cells -> None : Resets all cell's visited attribute to False
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

    
    def get_neighbor_coords(self, col: int, row: int, direction: str) -> Tuple[Tuple[int, int], str]:
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
            "top": ((col, row - 1, ), "bottom"),
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
    - maze : Maze
    - window : Window

    Methods:
    ----
    - init_cells  : Initializes the matrix with Cell objects
    - create_cells  : Initializes the matrix of cells and draws them to screen
    - draw_cell(i: int, j: int) : Draws a cell to screen at specified row/column position
    - animate : Animates maze by drawing cells one at a time and allows us to visulize our algorithm
    - draw_entrance_and_exit  : Draws entrance and exit to maze by removing the top wall of the first cell and
    the bottom wall of the last cell
    - break_walls_r(col : int, row : int)  : Recursive backtracking algorithm to create maze   
    """

    def __init__(self, maze: Maze, window: CanvasFrame):
        self._maze = maze
        self._canvas = window
        # self.center_maze()
        self._init_cells()
        # self._window.root.after(10, self.center_maze)

        self._create_cells()
        self._create_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._maze.reset_visited_cells()


    # def center_maze(self) -> None:
    #     """Calculates necessary space to render maze at the center of its canvas"""
    #     canvas_width = self._window.canvas.winfo_width()
    #     canvas_height = self._window.canvas.winfo_height()

    #     print(canvas_height, canvas_width, end="\n!!!!!!!!!!")
    #     maze_width = self._maze.num_cols * 10
    #     maze_height = self._maze.num_rows * 10

    #     x_start = (canvas_width - maze_width) / 2
    #     y_start = (canvas_height - maze_height) / 2

    #     self._maze.x_start = x_start
    #     self._maze.y_start = y_start


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
        # if < 0 or x >= self._maze.num_rows or y < 0 or y >= self._maze.num_cols:
        #     raise ValueError("Invalid cell position")
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
        self._canvas.redraw()
        if path:
            time.sleep(0.1)
        else:
            pass

    def _create_entrance_and_exit(self) -> None:
        """Creates entrance and exit to maze by removing the top wall of the first cell and
        the bottom wall of the last cell"""
        top_cell = self._maze.get_cell(0, 0)
        bottom_cell = self._maze.get_cell(
            self._maze.num_cols - 1, self._maze.num_rows - 1, 
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

        # Directions to move in the maze
        directions = ["top", "right", "bottom", "left"]
        random.shuffle(directions)  # Shuffle directions to create a random maze

        for direction in directions:
            # Get the neighbor cell based on the direction
            neighbor_coords, opposite_direction = self._maze.get_neighbor_coords(col, row, direction)
            neighbor_col, neighbor_row = neighbor_coords
           
            # Boundary check
            if 0 <= neighbor_row < self._maze.num_rows and 0 <= neighbor_col < self._maze.num_cols:
                neighbor = self._maze.get_cell(neighbor_col, neighbor_row)

                # If the neighbor hasn't been visited, break the walls and recurse
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
        
        # if self._maze.num_cols - 1 == col and self._maze.num_rows - 1 == row:
        #     return True
        current_cell = self._maze.get_cell(col, row)
        current_cell.visited = True
        
        if current_cell is self._maze.end_cell:
            return True      
        
        directions = ["top", "right", "bottom", "left"]
        random.shuffle(directions)

        for direction in directions:
            neighbor_coords, opposite_direction = self._maze.get_neighbor_coords(col, row, direction)
            neighbor = self._maze.get_cell(*neighbor_coords)

            neighbor_col, neighbor_row = neighbor_coords
            
            # Boundary check
            if 0 <= neighbor_row < self._maze.num_rows and 0 <= neighbor_col < self._maze.num_cols:

                # If the neighbor hasn't been visited, recurse on it
                if neighbor and not neighbor.visited and not getattr(neighbor, f"has_{opposite_direction}_wall"):
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


        
        
