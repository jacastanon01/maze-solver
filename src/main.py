from window import Window, Point, Line


def main() -> None:
    screen = Window(800, 800)

    point1 = Point(0, 0)
    point2 = Point(400, 400)
    line = Line(point1, point2)
    screen.draw_line(line, "black")
    point1 = point2
    point2 = Point(800, 0)
    line = Line(point1, point2)
    screen.draw_line(line, "red")

    screen.wait_for_close()


if __name__ == "__main__":
    main()
