from tkinter import Tk, BOTH, Canvas


class Point:
    """Data Class that represents position on x,y grid"""

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class Line:
    """
    Class that represents distance between two points

    Attributes
    -----
    point1, point2 : Point

    Methods
    -----
    draw(canvas : Tk.Canvas, fill_color ?: str) -> None
    """

    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, fill_color: str = "black") -> None:
        """Takes x and y positions of both points and draws a line between them"""
        x1 = self.point1.x
        y1 = self.point1.y
        x2 = self.point2.x
        y2 = self.point2.y
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)
        canvas.pack(fill=BOTH, expand=1)


class Window:
    """
    Class that represents the Tkinter window

    Attributes
    -----
    width : int
    height : int

    wait_for_close -> None
    start() -> None
    close -> None
    redraw() ->
    is_valid_window -> bool
    """

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self.__root = Tk()
        self._canvas = Canvas(
            self.__root,
            bg="white",
            height=self._window.height,
            width=self._window.width,
        )

        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self._canvas.pack(fill=BOTH, expand=True)

    @property
    def root(self):
        return self.__root

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def draw_line(self, line: Line, fill_color: str = "black") -> None:
        """
        Responsible for drawing a line on the canvas
        """
        line.draw(self._canvas, fill_color)

    def wait_for_close(self) -> None:
        """Method that checks if window is still open before drawing to it"""
        # self.__is_window_running = True
        while self.is_valid_window():
            self.redraw()

    def start(self) -> None:
        """Starts the Tkinter window"""
        self.__root.mainloop()

    def close(self) -> None:
        """Method to terminate window"""
        # self.__is_window_running = False
        self.__root.destroy()

    def redraw(self) -> None:
        """Method that updates Tkinter root"""
        if self.is_valid_window():
            self.__root.update_idletasks()
            self.__root.update()

    def is_valid_window(self) -> bool:
        """Method that checks if window is still open before drawing to it"""
        return self.__root.winfo_exists()


