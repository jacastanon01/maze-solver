# Deterministic Maze Generator

![maze_demo](https://github.com/jacastanon01/maze-solver/assets/24418510/afc3aed4-cdbf-4c79-89fd-8076d49685d4)

This is a small application that utilizes Tkinter as a GUI for a maze. The walls of the maze are randomly constructed and the maze is solved using a depth-first search, meaning you can watch as the algorithm traverses through the maze and backtrack until it finds the end.

## Demo

- Install python3 on your machine
- Clone this repo
- Run `./main.sh` to launch GUI application
- Enter a number for rows and columns in the text box at the top of the window
- Click the "Generate Maze" button or Enter to generate a new maze
- Click the "Solve Maze" button or Enter to solve the maze
- Click the "Reset Maze" button or Enter after solving maze to reset the maze

## Technologies Used

- Python 3.12.1
- Tkinter
- unittest library for tests
- random module to generate random directions
- Type hinting and docstrings to improve readability

## Learning opportunites

I wanted to keep the logic related to constructing the maze and solving it in a separate class so that they can be tested separately. This was also helpful for me as I learned how to use Tkinter's Canvas widget which is useful because you don't have to create new windows every time the maze needs to be drawn. I also wanted to learn more about using unittest and writing tests in python, so that I can keep my code DRY and maintainable. I utilized mock objects so when testing certain functionality, I could test it without actually creating a window or canvas object.

Another challenge was trying to keep certain sections segregated from each other and figuring out the best ways to structure them in my maze class so that the internal logic of the maze and the GUI could be in sync. My solution was to break the Maze module into three classes:

- Maze class which would contain the position, height, width and other properties related to the design
- MazeSolver class which would contain the logic for solving the maze
- MazeDrawer class which be the interface for actually drawing the maze on the canvas

My primary focus with this project was to use some data structures and algorithms in an actual project. For example, when the maze is being solved, if the path reaches a deadend, how does it know which valid direction it can move within the maze? I was able to define the coordinates of all the cells sorrounding a given cell and then check if any are blocked by a wall. If they are, it will check another random direction's coordinates. If they are not, then the path can move in that direction. In my solution's algorithm, I kept track of which cells had already been visited so that when backtracking, the path is not drawn in the same direction and it can continue to traverse until it reaches a logical end and then recursively backtrack until the end is reached.
