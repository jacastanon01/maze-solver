class Maze:
    """
    Class that contains a matrix of cell objects

    Attributes
    -----
    x : int
    y : int
    num_cols : int
    num_rows : int
    cell_size_x : int
    cell_size_y : int
    window : Screen

    Methods
    -----
    create_cells -> None
    draw_cell(i : int, j : int) -> None
    animate -> None
    """

    from screen import Cell, Screen

    def __init__(
        self,
        x: int,
        y: int,
        num_cols: int,
        num_rows: int,
        cell_size_x: int,
        cell_size_y: int,
        screen: Screen,
    ):
        self.x = x
        self.y = y
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._window = screen
        self._create_cells()

    def _create_cells(self):
        """Function that creates matrix of cells"""
        self._cells = [Cell(self._window) for i in range(self.num_cols + 1)]
