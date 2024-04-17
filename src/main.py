from screen import Screen, Line, Point, Cell


def main() -> None:
    window = Screen(800, 800)
    render_grid(window)
    window.wait_for_close()


def render_grid(screen: Screen) -> None:
    for row in range(0, 800, 200):
        for col in range(0, 800, 200):
            start_x1 = col
            start_y1 = row
            end_x2 = col + 200
            end_y2 = row + 200
            cell = Cell(screen, start_x1, start_y1, end_x2, end_y2)
            cell.draw()


if __name__ == "__main__":
    main()
