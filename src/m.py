from tkinter import Tk, Frame, Button, BOTH, Entry, Label, IntVar, Canvas
from tkinter.messagebox import showerror


from src.maze import Maze, MazeDrawer, MazeSolver
from src.utils import calculate_window_sizes


class Window(Frame):
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

    def __init__(self, master=None):
        super().__init__(master)
        self.__root = master
        self.__root.geometry("800x800")
        self.__root.title("Maze Solver")

        self._create_widgets()
        self._create_buttons()

    def _create_widgets(self):

        self.control_frame = Frame(self.__root)
        self.control_frame.pack()

        self.canvas_frame = CanvasFrame(self.__root)
        self.canvas_frame.pack(fill=BOTH, expand=True)

        row_label = Label(self.control_frame, text="Rows")
        row_label.grid(row=0, column=0)
        self.row_input = Entry(self.control_frame)
        self.row_input.grid(row=0, column=1)

        col_label = Label(self.control_frame, text="Columns")
        col_label.grid(row=1, column=0)
        self.col_input = Entry(self.control_frame)
        self.col_input.grid(row=1, column=1)

    def _create_buttons(self):
        actions = ["draw", "solve", "reset"]
        self.buttons = {}
        for i, action in enumerate(actions):
            self.buttons[action] = Button(
                self.control_frame,
                text=f"{action.capitalize()} Maze",
                command=getattr(self, f"{action}_maze"),
                pady=5,
            )
            self.buttons[action].grid(row=2, column=i)

    def draw_maze(self):
        self.reset_maze()
        rows_entry = int(self.row_input.get())
        cols_entry = int(self.col_input.get())
        width, height, padding_x, padding_y, num_cols, num_rows = (
            calculate_window_sizes(cols_entry, rows_entry)
        )
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
        # self.maze = initialize_maze(cols_entry, rows_entry)
        self.drawer = MazeDrawer(self.maze, self.canvas_frame)
        # drawer.draw_maze()

    def solve_maze(self):
        if self.drawer and self.maze:
            solver = MazeSolver(self.maze, self.drawer)
            solver.solve()
        else:
            showerror(title="Error", message="Must draw maze before solving it")

    def reset_maze(self):
        self.canvas_frame.clear_canvas()


class CanvasFrame(Frame):
    """
    Behavior class that handles interactions between maze and canvas

    Methods
    -----
    - draw_line(line : Line, fill_color ?: str) -> None : Draws line to canvas
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.__root = master
        self.maze = None
        self.canvas = None
        self.create_canvas()

    def create_canvas(self):
        self.canvas = Canvas(self, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)

    def draw_line(self, line, fill_color="black"):
        point1, point2 = line.get_points()
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        self.canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)

    def clear_canvas(self):
        self.canvas.delete("all")

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


if __name__ == "__main__":
    root = Tk()
    app = Window(master=root)
    app.mainloop()
