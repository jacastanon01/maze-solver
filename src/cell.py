from dataclasses import dataclass

@dataclass
class Point:
    """Data Class that represents position on x,y grid"""
    x: int
    y: int

@dataclass
class Line:
    """
        Class that represents distance between two points

        Attributes
        -----
        - point1 : Point
        - point2 : Point
    """

    point1: Point
    point2: Point

    def get_points(self) -> tuple[Point, Point]:
        """Returns the two connecting points of a line"""
        return self.__point1, self.__point2

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
        - draw(x1 : int, y1 : int, x2 : int, y2 : int)
            Draws cell to screen

        - draw_move(to_cell : Cell, undo ?: bool)   
            Draws line thru cells

        - get_wall_directions -> dict[{str: tuple(int)}] : 
            Retrieves the coordinates for a given wall direction
    """

    # Dunder methods
    def __init__(self, window: "CanvasFrame"):
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

