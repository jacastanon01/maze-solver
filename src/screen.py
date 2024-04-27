from tkinter import (
    Tk,
    BOTH,
    Canvas,
    TclError,
    Frame,
    Button,
    Entry,
    X,
    Y,
    NE,
    NS,
    BOTTOM,
    LEFT,
    RIGHT,
    TOP,
    Label,
    StringVar,
)
from tkinter.messagebox import showerror


from src.utils import initialize_maze, solve_maze


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
    - point1 : Point
    - point2 : Point
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
    Class that containig data of Tkinter window

    Attributes
    -----
    - width : int
    - height : int

    Methods
    -----
    - wait_for_close -> None : calls self.redraw() if window still is valid
    - start() -> None : starts mainloop for window to stay open
    - close -> None : terminates window
    - redraw() -> None : Updates window
    - is_valid_window -> bool : checks if window still exists
    """

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self.__root = Tk()
        self.__root.geometry(f"{self._width}x{self._height}")

        # Define frames
        control_frame = Frame(self.__root)
        control_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=10)

        canvas_frame = Frame(self.__root)
        canvas_frame.grid(row=1, column=0, sticky="nsew")

        # make canvas frame expandable
        self.__root.grid_rowconfigure(1, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # initialize widgets with frames
        self.__widgets = ButtonWidgets(control_frame)
        self.__canvas = CanvasFrame(canvas_frame, self)

        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas.pack(fill=BOTH, expand=True)

    @property
    def root(self) -> Tk:
        return self.__root

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def canvas(self) -> "CanvasFrame":
        return self.__canvas

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
        """
        Method that updates Tkinter root to draw to it
        """
        if self.is_valid_window():
            self.__root.update_idletasks()
            self.__root.update()

    def is_valid_window(self) -> bool:
        """Method that checks if window is still open before drawing to it"""
        try:
            return self.__root.winfo_exists()
        except TclError:
            pass


class CanvasFrame(Frame):
    """
    Behvaior class that handles interactions between maze and canvas

    Methods
    -----
    - draw_line(line : Line, fille_color ?: str) -> None : Draws line to canvas
    """

    def __init__(self, parent: Frame, window: Window):
        super().__init__(parent)
        self.__window = window
        self.__canvas = Canvas(
            self,
            bg="white",
        )
        self.__canvas.pack(fill=BOTH, expand=True)

    def draw_line(self, line: Line, fill_color: str = "black") -> None:
        """
        Responsible for drawing a line on the canvas
        """
        point1, point2 = line.get_points()
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        self.__canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)

    def redraw(self) -> None:
        """
        Method that updates Tkinter root to draw to it
        """
        if self.__window.is_valid_window():
            self.__window.root.update_idletasks()
            self.__window.root.update()


class ButtonWidgets:
    """Class that contains all buttons in the maze solver"""

    def __init__(self, parent: Frame):
        self._container = None
        self._parent = parent
        # Grid placement for buttons
        self.reset_button = Button(
            parent, text="Reset", command=self.reset, cursor="exchange"
        )
        self.reset_button.grid(row=1, column=0, padx=5, sticky="nsew")

        self.solve_button = Button(
            parent, text="Solve", command=self.solve, cursor="arrow"
        )
        self.solve_button.grid(row=2, column=0, padx=5, sticky="nsew")

        # User input
        self.draw_button = Button(
            parent, text="Draw", command=self.draw, cursor="arrow"
        )
        self.draw_button.grid(
            row=2, column=1, columnspan=2, ipadx=5, ipady=5, sticky="ew"
        )

        # Add entries
        self.row_input = StringVar()
        row_label = Label(parent, text="Rows", font=("Helvetica", 14))
        row_label.grid(row=0, column=1, sticky="ew")
        self.rows_entry = Entry(
            parent,
            textvariable=self.row_input,
            width=5,
            bg="white",
            fg="black",
            takefocus=True,
            font=("Helvetica", 14),
            justify="center",
        )
        self.rows_entry.grid(row=1, column=1, ipadx=5, ipady=5, sticky="ew")

        self.col_input = StringVar()
        col_label = Label(parent, text="Columns", font=("Helvetica", 14))
        col_label.grid(row=0, column=2, sticky="ew")
        self.columns_entry = Entry(
            parent,
            textvariable=self.col_input,
            width=5,
            bg="white",
            fg="black",
            font=("Helvetica", 14),
            justify="center",
        )
        self.columns_entry.grid(row=1, column=2, ipadx=5, ipady=5, sticky="ew")

        for i in range(3):
            parent.grid_columnconfigure(i, weight=1)
        parent.grid_rowconfigure(1, weight=2)

    def draw(self):
        """Method that draws the maze"""
        try:
            cols = int(self.col_input.get())
            rows = int(self.row_input.get())
            container = initialize_maze(cols, rows)
            print(container)
            self._container = container
        except ValueError as e:
            showerror(title="Error", message=e)

    def solve(self):
        """Method that solves the maze"""
        print(self._container)

    def reset(self):
        """Method that resets the maze"""
        print("Resetting...")


if __name__ == "__main__":
    window = Window(1000, 600)
    window.start()
