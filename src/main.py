from tkinter import Tk

from src.screen import Window


def main():
    root = Tk()
    app = Window(master=root)
    app.start()
    app.wait_for_close()


if __name__ == "__main__":
    main()
