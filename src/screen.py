from tkinter import Tk, BOTH, Canvas


class Point:
    """Class that represents position on x,y grid"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    """
    Class that represents distance between two points

    Attributes
    -----
    point1, point2 : Point

    Methods
    -----
    draw(canvas : Tk.Canvas, fill_color : str) -> None
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
    width, height : int
    root : Tk

    Methods
    -----
    wait_for_close -> None
    close -> None
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title("Maze Solver")
        self.is_window_running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def wait_for_close(self) -> None:
        """Function that checks if window is still open before drawing to it"""
        self.is_window_running = True
        while self.is_window_running:
            self.redraw()

    def close(self) -> None:
        """Function to terminate window"""
        self.is_window_running = False

    def redraw(self) -> None:
        """Function that updates Tkinter root"""
        self.root.update_idletasks()
        self.root.update()


class CanvasManager:
    """
    Class that represents the Tkinter canvas manager

    Attributes
    -----
    canvas : Tk.Canvas
    window : Window

    Methods
    -----
    draw_line(line : Line, fill_color : str) -> None
    """

    def __init__(self, window: Window):
        self.window = window
        self.canvas = Canvas(
            self.window.root,
            bg="white",
            height=self.window.height,
            width=self.window.width,
        )
        self.canvas.pack(fill=BOTH, expand=True)

    def draw_line(self, line: Line, fill_color: str = "black") -> None:
        """Function that calls draw method from Line instance with color"""
        line.draw(self.canvas, fill_color)

    """
    Class that represents Tkinter canvas

    Attributes
    -----
    width, height : int
    root : Tk
    canvas : Tk.Canvas

    Methods
    -----
    draw_line(line : Line, fill_color : str) -> None
    redraw -> None
    wait_for_close -> None
    close -> None
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self._canvas = Canvas(
            self.__root, bg="white", height=self.height, width=self.width
        )
        self._canvas.pack(fill=BOTH, expand=True)
        self._is_window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line: Line, fill_color: str = "black") -> None:
        """Function that calls draw method from Line instance with color"""
        line.draw(self._canvas, fill_color)

    def redraw(self) -> None:
        """Function that updates Tkinter root"""
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        """Function that checks if window is still open before drawing to it"""
        self._is_window_running = True
        while self._is_window_running:
            self.redraw()

    def close(self) -> None:
        """Function to terminate window"""
        self._is_window_running = False
