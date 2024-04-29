from tkinter import (
    Tk,
    Frame,
    Button,
    BOTH,
    Entry,
    Label,
    IntVar,
    Canvas,
    DISABLED,
    NORMAL,
    TclError,
)
from tkinter.messagebox import showerror
from enum import Enum
from typing import Tuple, Callable


from src.maze import Maze, MazeDrawer, MazeSolver


class State(Enum):
    IDLE = 1
    DRAWING = 2
    SOLVING = 3


class Window(Frame):
    """
    Class that containig data of Tkinter window

    Attributes
    ----------
    - root : Tk
        The Tkinter root instance.

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
        super().__init__(master)
        self.__root = master
        self.__root.geometry("800x800")
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.buttons = {}
        self.state = State.IDLE

        self._create_widgets()
        self._create_buttons()

    @property
    def root(self):
        return self.__root

    def set_state(self, state: State):
        self.state = state

    def toggle_button_state(self, value: str, state: bool = None):
        """
        Checks if canvas is idle before toggling active state of buttons
        """
        btn = self.buttons.get(value)
        if btn is None:
            raise ValueError("Invalid button")
        # if state is explicitly defined, set button to it
        if state is not None:
            btn["state"] = NORMAL if state else DISABLED
        else:
            # Only togglable when canvas is idle
            if self.state == State.IDLE:
                btn["state"] = NORMAL if btn["state"] == DISABLED else DISABLED

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

        self.canvas_frame = CanvasFrame(self)
        self.canvas_frame.pack(fill=BOTH, expand=True)

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

        if self.buttons.get("solve"):
            self.buttons["solve"]["state"] = DISABLED

    def start(self) -> None:
        """Starts the Tkinter window"""
        self.__root.mainloop()

    def close(self) -> None:
        """Method to terminate window"""
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


class CanvasFrame(Frame):
    """
    Behavior class that handles interactions between maze and canvas

    Attributes
    ----------
    - window : Window
        The parent window instance.

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
    - clear_canvas() -> None:
        Clears the canvas.
    - calculate_window_sizes() -> Tuple[int, int, int, int, int, int]:
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

    def __init__(self, window: Window):
        super().__init__(window.root)
        self.__window = window
        self.__root = self.__window.root

        self.maze = None
        self.canvas = None
        self.create_canvas()
        self._bind_return(self.draw_maze)

    def create_canvas(self):
        self.canvas = Canvas(self, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)

    def draw_line(self, line, fill_color="black"):
        """Draws line to canvas"""
        if self.__window.state in [State.DRAWING, State.SOLVING]:
            point1, point2 = line.get_points()
            x1, y1 = point1.x, point1.y
            x2, y2 = point2.x, point2.y
            self.canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)

    def clear_canvas(self):
        self.__window.set_state(State.IDLE)
        self.canvas.delete("all")

    def _calculate_window_sizes(self) -> Tuple[int, int, int, int, int, int]:
        """
        Takes user input of columns and rows to calculate the size of a window based on those values.
        Calls draw_maze with input values to draw the maze
        """
        self.rows_entry = int(self.__window.row_input.get())
        self.cols_entry = int(self.__window.col_input.get())
        if (
            self.cols_entry < 0
            or self.cols_entry > 50
            or self.rows_entry < 0
            or self.rows_entry > 50
        ):
            raise ValueError("Maze must have between 2 and 50 columns")
        print(f"Generating a {self.cols_entry} by {self.rows_entry} maze...")
        desired_padding = 10
        cell_cols = 20 if self.cols_entry < 25 else 10
        cell_rows = 20 if self.rows_entry < 25 else 10
        window_size = 800

        maze_width = self.cols_entry * cell_cols
        maze_height = self.rows_entry * cell_rows

        window_width = maze_width + (
            desired_padding * 2
        )  # Maze size plus padding for left and right
        window_height = maze_height + (
            desired_padding * 2
        )  # Maze size plus padding for top and bottom

        padding_x = (window_size - maze_width) / 2
        padding_y = (window_size - maze_height) / 2

        return (
            window_size,
            window_size,
            padding_x,
            padding_y,
            self.cols_entry,
            self.rows_entry,
        )

    def draw_maze(self, event=None):
        try:
            width, height, padding_x, padding_y, num_cols, num_rows = (
                self._calculate_window_sizes()
            )
            self.reset_maze()
            if self.__window.buttons["solve"]["state"] == NORMAL:
                self.__window.toggle_button_state("solve")
            self.__window.set_state(State.DRAWING)

            cell_cols = 20 if num_cols < 25 else 10
            cell_rows = 20 if num_rows < 25 else 10

            self.maze = Maze(
                padding_x,
                padding_y,
                num_cols=num_cols,
                num_rows=num_rows,
                cell_width=cell_cols,
                cell_height=cell_rows,
            )
            self.drawer = MazeDrawer(self.maze, self)
            # enable solve button
            self.__window.set_state(State.IDLE)
            self.__window.toggle_button_state("solve")
            self._bind_return(self.solve_maze)

        except ValueError as e:
            showerror("Error", message=e)

    def solve_maze(self, event=None):
        if self.__window.state == State.IDLE:
            self.__window.set_state(State.SOLVING)
            if self.drawer and self.maze:
                self.__window.toggle_button_state("draw")
                solver = MazeSolver(self.maze, self.drawer)
                solver.solve()
                self._bind_return(self.draw_maze)
            else:
                showerror(title="Error", message="Must draw maze before solving it")
            self.__window.set_state(State.IDLE)
            self.__window.toggle_button_state("draw")

    def reset_maze(self):
        self.clear_canvas()
        self.__window.set_state(State.IDLE)
        self.__window.toggle_button_state("solve", False)
        self.__window.toggle_button_state("draw", True)

    def redraw(self) -> None:
        """
        Method that updates Tkinter root to draw to it
        """
        if self.__window.is_valid_window():
            self.__root.update_idletasks()
            self.__root.update()

    def _bind_return(self, func: Callable):
        """
        Method that binds return key to a function
        """
        self.__root.bind("<Return>", func)
