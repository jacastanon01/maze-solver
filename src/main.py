from tkinter import Tk

from src.screen import App


def main():
    root = Tk()
    app = App(master=root)
    app.start()
    app.wait_for_close()


if __name__ == "__main__":
    main()
