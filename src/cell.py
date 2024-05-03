from dataclasses import dataclass, field


@dataclass
class Point:
    """Dataclass that represents position on x,y grid"""

    x: int
    y: int


@dataclass
class Line:
    """
    Dataclass that represents a line on a grid

    Attributes
    -----
    - point1 : Point
    - point2 : Point
    """

    point1: Point
    point2: Point

    def get_points(self) -> tuple[Point, Point]:
        """Returns the two connecting points of a line"""
        return self.point1, self.point2


@dataclass
class Cell:
    """
    A dataclass to represent different cells in a maze

    Attributes
    -----
    - x1, y1 : int
        Represents bottom-left point of cell. To be used to draw walls

    - x2, y2 : int
        Represents top-right point of cell. To be used to draw walls

    - has_{side}_wall: bool
        Flags to indicate which walls to draw on cell

    - visited : list : Keeps track of which cell has already been added to path in DFS

    """

    x1: int = field(init=False)
    y1: int = field(init=False)
    x2: int = field(init=False)
    y2: int = field(init=False)
    has_left_wall: bool = True
    has_top_wall: bool = True
    has_right_wall: bool = True
    has_bottom_wall: bool = True
    visited: bool = False

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
