from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.canvas = Canvas(self.__root, bg="white")
        self.canvas.pack()
        self._is_window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self._is_window_running = True
        while self._is_window_running:
            self.redraw()

    def close(self):
        self._is_window_running = False
