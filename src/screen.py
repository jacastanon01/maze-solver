from tkinter import Tk, BOTH, Canvas


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, fill_color: str = "black") -> None:
        x1 = self.point1.x
        y1 = self.point1.y
        x2 = self.point2.x
        y2 = self.point2.y
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)
        canvas.pack(fill=BOTH, expand=1)


class Screen:
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

    def draw_line(self, line: Line, fill_color: str) -> None:
        line.draw(self._canvas, fill_color)

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self._is_window_running = True
        while self._is_window_running:
            self.redraw()

    def close(self) -> None:
        self._is_window_running = False


class Cell:
    def __init__(self, screen: Screen, x1: int, y1: int, x2: int, y2: int):
        self._window = screen
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    def draw(self) -> None:
        if self.has_left_wall:
            self._window.draw_line(
                Line(Point(self._x1, self._y1), Point(self._x1, self._y2)),
                "black",
            )
        if self.has_top_wall:
            self._window.draw_line(
                Line(Point(self._x1, self._y1), Point(self._x2, self._y1)),
                "black",
            )
        if self.has_right_wall:
            self._window.draw_line(
                Line(Point(self._x2, self._y1), Point(self._x2, self._y2)),
                "black",
            )
        if self.has_bottom_wall:
            self._window.draw_line(
                Line(Point(self._x2, self._y2), Point(self._x1, self._y2)),
                "black",
            )
