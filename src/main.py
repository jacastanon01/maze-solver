from random import randint, choice

from screen import Window


def main() -> None:
    window = Window(800, 800)
    render_maze(window)
    # render_grid(window)
    # c1 = Cell(window)
    # c1.has_right_wall = False
    # c1.draw(50, 50, 100, 100)

    # c2 = Cell(window)
    # c2.has_left_wall = False
    # c2.has_bottom_wall = False
    # c2.draw(100, 50, 150, 100)

    # c1.draw_move(c2)

    # c3 = Cell(window)
    # c3.has_top_wall = False
    # c3.has_right_wall = False
    # c3.draw(100, 100, 150, 150)

    # c2.draw_move(c3)

    # c4 = Cell(window)
    # c4.has_left_wall = False
    # c4.draw(150, 100, 200, 150)

    # c3.draw_move(c4, True)

    window.wait_for_close()


def render_maze(screen: Screen) -> None:
    n = randint(3, 8)
    x, y = 0, 0
    for i in range(n):
        c = Cell(screen)
        x2 = x + 50
        y2 = y + 50

        if i >> 1 == 0:
            x += 50
            x2 += 50
        else:
            y += 50
            y2 += 50
        c.draw(x, y, x2, y2)


def render_grid(screen: Screen) -> None:
    for row in range(0, 800, 200):
        for col in range(0, 800, 200):
            start_x1 = col
            start_y1 = row
            end_x2 = col + 200
            end_y2 = row + 200
            cell = Cell(screen)
            cell.draw(start_x1, start_y1, end_x2, end_y2)


if __name__ == "__main__":
    main()
