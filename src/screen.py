from tkinter import (
    Tk,
    Frame,
    Button,
    BOTH,
    Entry,
    Label,
    Canvas,
    DISABLED,
    NORMAL,
    TclError,
)
from tkinter.messagebox import showerror
from enum import Enum
from typing import Tuple, Callable


from src.maze import Maze, MazeDrawer, MazeSolver
from src.cell import Line

WINDOW_SIZE = 800


class CanvasState(Enum):
    IDLE = 1
    DRAWING = 2
    SOLVING = 3


class App(Frame):
    """
    Class containing data of Tkinter window

    Attributes
    ----------
    - root : Tk
        The Tkinter root instance.

    - control_frame : Frame


    Methods
    -------
    - set_state(state: State) -> None:
        Sets the state of the window.

    - toggle_button_state(value: str, state: Optional[bool] = None) -> None:
        Toggles the state of a button based on the current state of the canvas.
        If `state` is provided, sets the button state accordingly.

    - _create_widgets() -> None:
        Defines the frame for widget components.

    - _create_buttons() -> None:
        Creates buttons for drawing, solving, and resetting the maze.

    - start() -> None:
        Starts the Tkinter window main loop.

    - close() -> None:
        Terminates the window.

    - is_valid_window() -> bool:
        Checks if the window is still open.

    - wait_for_close() -> None:
        Waits for the window to close before redrawing.
    """

    def __init__(self, master: Tk):
        # instantiaing the Tkinter window and setting size
        super().__init__(master)
        self.__root = master
        self.__root.geometry("800x800")
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        # setting state
        self.canvas_state = CanvasState.IDLE
        self.buttons = {}

        # adding widgets to GUI and creating a frame for the maze
        self._create_widgets()
        self.canvas_frame = CanvasFrame(self)
        self._create_buttons()
        self.canvas_frame.pack(fill=BOTH, expand=True)

        # validates the input box contains an int or backspace or enter
        validate_int = self.register(lambda x: x.isdigit() or x == "")
        self.row_input.config(validate="key", validatecommand=(validate_int, "%P"))
        self.col_input.config(validate="key", validatecommand=(validate_int, "%P"))

    def _enable_draw_button(self, event):
        """
        Validates that both entries have values before enabling draw button
        """
        if self.row_input.get() and self.col_input.get():
            self.toggle_button_state("draw", True)
        else:
            self.toggle_button_state("draw", False)

    @property
    def root(self):
        return self.__root

    def _create_widgets(self):
        """
        Defines new Frame for widget components
        """
        self.control_frame = Frame(self.__root)
        self.control_frame.pack()

        row_label = Label(self.control_frame, text="Rows")
        row_label.grid(row=0, column=0)
        self.row_input = Entry(self.control_frame)
        self.row_input.grid(row=0, column=1)
        self.row_input.focus()

        col_label = Label(self.control_frame, text="Columns")
        col_label.grid(row=1, column=0)
        self.col_input = Entry(self.control_frame)
        self.col_input.grid(row=1, column=1)

        self.row_input.bind("<KeyRelease>", self._enable_draw_button)
        self.col_input.bind("<KeyRelease>", self._enable_draw_button)

    def _create_buttons(self):
        actions = ["draw", "solve", "reset"]
        for i, action in enumerate(actions):
            self.buttons[action] = Button(
                self.control_frame,
                text=f"{action.capitalize()} Maze",
                command=getattr(self.canvas_frame, f"{action}_maze"),
                pady=5,
            )

            self.buttons[action].grid(row=2, column=i)

        self.toggle_button_state("draw", False)
        self.toggle_button_state("solve", False)

    def start(self) -> None:
        self.__root.mainloop()

    def close(self) -> None:
        self.__root.destroy()

    def is_valid_window(self) -> bool:
        """Method that checks if window is still open before drawing to it"""
        try:
            return self.__root.winfo_exists()
        except TclError:
            pass

    def wait_for_close(self) -> None:
        """Method that checks if window is still open before drawing to it"""
        try:
            while self.is_valid_window():
                self.redraw()
        except TclError:
            pass

    def redraw(self) -> None:
        if self.canvas_state != CanvasState.IDLE:
            self.__root.update_idletasks()
            self.__root.update()

    def toggle_button_state(self, value: str, state: bool = None):
        btn = self.buttons.get(value)
        if btn is None:
            raise ValueError("Invalid button")
        # if state is explicitly defined, set button to it
        if state is not None:
            btn["state"] = NORMAL if state else DISABLED
        else:
            # Only togglable when canvas is idle
            if self.canvas_state == CanvasState.IDLE:
                btn["state"] = NORMAL if btn["state"] == DISABLED else DISABLED


class CanvasFrame(Frame):
    """
    Behavior class that handles interactions between maze and canvas

    Attributes
    ----------
    - window : App
        The parent window instance.

    - buttons : Dict[str, Button]
        Dictionary of buttons associated with the canvas.

    - canvas : Canvas
        The Tkinter canvas instance.

    - is_drawing : bool
        Flag indicating whether drawing is in progress.

    - maze : Maze
        The maze object associated with the canvas.

    Methods
    -------
    - draw_line(line, fill_color="black") -> None:
        Draws a line on the canvas.

    - _clear_canvas() -> None:
        Clears the canvas.

    - _calculate_padding() -> Tuple[int, int, int, int, int, int]:
        Calculates window sizes based on user input.

    - draw_maze(event=None) -> None:
        Draws the maze based on user input.

    - solve_maze(event=None) -> None:
        Solves the maze.

    - reset_maze() -> None:
        Resets the maze.

    - redraw() -> None:
        Updates the Tkinter root to draw to it.

    - _bind_return(func: Callable) -> None:
        Binds the return key to a function.
    """

    def __init__(self, window: App):
        super().__init__(window.root)
        self.__window = window

        self.maze = None
        self.canvas = None

        self.create_canvas()
        self._bind_return(self.draw_maze)

    @property
    def window(self):
        return self.__window

    def set_state(self, state: CanvasState):
        self.__window.canvas_state = state

    def toggle_button_state(self, value: str, state: bool = None):
        self.__window.toggle_button_state(value, state)

    def create_canvas(self):
        self.canvas = Canvas(self, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)

    def draw_line(self, line: Line, fill_color="black"):
        """Draws line to canvas"""
        if self.__window.canvas_state in [CanvasState.DRAWING, CanvasState.SOLVING]:
            point1, point2 = line.get_points()
            x1, y1 = point1.x, point1.y
            x2, y2 = point2.x, point2.y
            self.canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)

    def _clear_canvas(self):
        self.canvas.delete("all")

    def _validate_input(self) -> Tuple[int, int]:
        """
        Returns (cols, rows) if entry is within range and int
        Otherwise, an exception is raised
        """
        try:
            cols_entry = int(self.__window.col_input.get())
            rows_entry = int(self.__window.row_input.get())
            if cols_entry < 2 or cols_entry > 50 or rows_entry < 2 or rows_entry > 50:
                raise ValueError("Maze must have between 2 and 50 columns")
            return cols_entry, rows_entry
        except ValueError:
            raise ValueError("Please enter valid numeric values for rows and columns.")

    def _calculate_padding(self, num_cols: int, num_rows: int) -> Tuple[int, int]:
        """
        Takes user input of columns and rows to calculate how much padding to put around the maze

        Parameters
        ----------
        - num_cols: int
            Number of columns in the maze
        - num_rows: int
            Number of rows in the maze
        """
        cell_cols = 20 if num_rows < 25 else 10
        cell_rows = 20 if num_cols < 25 else 10

        maze_width = num_rows * cell_cols
        maze_height = num_cols * cell_rows

        padding_x = (WINDOW_SIZE - maze_width) / 2
        padding_y = (WINDOW_SIZE - maze_height) / 2

        return (padding_x, padding_y)

    def draw_maze(self, event=None):
        try:
            num_cols, num_rows = self._validate_input()
            padding_x, padding_y = self._calculate_padding(num_cols, num_rows)
            self.reset_maze()

            self.toggle_button_state("draw", False)
            self.toggle_button_state("solve", False)
            self.set_state(CanvasState.DRAWING)

            cell_cols = 20 if num_cols < 25 else 10
            cell_rows = 20 if num_rows < 25 else 10

            self.maze = Maze(
                padding_x,
                padding_y,
                num_cols=num_cols,
                num_rows=num_rows,
                cell_width=cell_cols,
                cell_height=cell_rows,
                cells=[],
            )
            self.drawer = MazeDrawer(self.maze, self)

            if self.maze and self.drawer:
                self.toggle_button_state("solve", True)
                self.set_state(CanvasState.IDLE)
                self._bind_return(self.solve_maze)

        except ValueError as e:
            showerror("Error", message=e)

    def solve_maze(self, event=None):
        if self.window.canvas_state != CanvasState.IDLE:
            self._clear_canvas()
        self.set_state(CanvasState.SOLVING)
        if self.drawer and self.maze:
            self.toggle_button_state("draw", False)
            self.toggle_button_state("solve", False)
            solver = MazeSolver(self.maze, self.drawer)
            solver.solve()
            self._bind_return(self.draw_maze)
        else:
            showerror(title="Error", message="Must draw maze before solving it")
        self.set_state(CanvasState.IDLE)
        self.toggle_button_state("draw", True)

    def reset_maze(self):
        self._clear_canvas()
        # self.maze = None
        self.drawer = None
        self.set_state(CanvasState.IDLE)
        self.toggle_button_state("solve", False)
        self.toggle_button_state("draw", True)

    def _bind_return(self, func: Callable):
        """
        Method that binds return key to a function
        """
        self.__window.root.bind("<Return>", func)
