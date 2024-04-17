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

    def draw_line(self, line: Line, fill_color: str = "black") -> None:
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
    def __init__(self, screen: Screen):
        self._window = screen
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None

    def draw(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        if self.has_left_wall:
            self._window.draw_line(
                Line(Point(x1, y1), Point(x1, y2)),
            )
        if self.has_top_wall:
            self._window.draw_line(
                Line(Point(x1, y1), Point(x2, y1)),
            )
        if self.has_right_wall:
            self._window.draw_line(
                Line(Point(x2, y1), Point(x2, y2)),
            )
        if self.has_bottom_wall:
            self._window.draw_line(
                Line(Point(x1, y2), Point(x2, y2)),
            )

    def draw_move(self, to_cell: "Cell", undo=False) -> None:
        line_color = "gray"

        if undo:
            line_color = "red"

        x_source = (self._x1 + self._x2) // 2
        y_source = (self._y1 + self._y2) // 2

        x_destination = (to_cell._x1 + to_cell._x2) // 2
        y_destination = (to_cell._y1 + to_cell._y2) // 2

        line = Line(Point(x_source, y_source), Point(x_destination, y_destination))

        self._window.draw_line(line, fill_color=line_color)
