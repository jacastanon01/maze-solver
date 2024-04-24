from tkinter import Tk, BOTH, Canvas, TclError


class Point:
    """Data Class that represents position on x,y grid"""

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def __repr__(self):
        return f"Point({self._x}, {self._y})"

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y


class Line:
    """
    Class that represents distance between two points

    Attributes
    -----
    point1 : Point
    point2 : Point
    """

    def __init__(self, point1: Point, point2: Point):
        self.__point1 = point1
        self.__point2 = point2

    def __repr__(self):
        return f"Line(\n\t{repr(self.__point1)},\n\t{repr(self.__point2)}\n\t)"

    def get_points(self) -> tuple[Point, Point]:
        """Returns the two connecting points of a line"""
        return self.__point1, self.__point2


class Window:
    """
    Class that represents the Tkinter window

    Attributes
    -----
    width : int
    height : int

    Methods
    -----
    wait_for_close -> None : calls self.redraw() if window still is valid
    draw_line(line : Line, fille_color ?: str) -> None : Draws line to canvas
    start() -> None : starts mainloop for window to stay open
    close -> None : terminates window
    redraw() -> None : Updates window
    is_valid_window -> bool : checks if window still exists
    """

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self.__root = Tk()
        self._canvas = Canvas(
            self.__root,
            bg="white",
            height=self._height,
            width=self._width,
        )

        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self._canvas.pack(fill=BOTH, expand=True)

    @property
    def root(self) -> Tk:
        return self.__root

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def draw_line(self, line: Line, fill_color: str = "black") -> None:
        """
        Responsible for drawing a line on the canvas
        """
        point1, point2 = line.get_points()
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        self._canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)

    def wait_for_close(self) -> None:
        """Method that checks if window is still open before drawing to it"""
        try:
            while self.is_valid_window():
                self.redraw()
        except TclError:
            pass

    def start(self) -> None:
        """Starts the Tkinter window"""
        self.__root.mainloop()

    def close(self) -> None:
        """Method to terminate window"""
        if self.is_valid_window():
            self.__root.destroy()

    def redraw(self) -> None:
        """Method that updates Tkinter root"""
        if self.is_valid_window():
            self.__root.update_idletasks()
            self.__root.update()

    def is_valid_window(self) -> bool:
        """Method that checks if window is still open before drawing to it"""
        try:
            return self.__root.winfo_exists()
        except TclError:
            return False
