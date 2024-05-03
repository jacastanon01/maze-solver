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

## Project Design Overview

In addressing the challenge of maintaining separation between different components and structuring them effectively within the maze project, I adopted a design approach centered around modularity and encapsulation. The project architecture consists of several distinct classes, each with well-defined responsibilities and interfaces, contributing to a cohesive and maintainable codebase.

### Maze Module:

- **Maze Class**: This class encapsulates the properties of the maze, such as its dimensions, position, and other relevant attributes. It serves as the foundational representation of the maze structure.
- **MazeSolver Class**: Responsible for implementing the algorithms and logic required to solve the maze. By abstracting solving functionality into a separate class, the Maze class remains focused solely on representing the maze's static properties.
- **MazeDrawer Class**: This class facilitates the visualization of the maze by recursively drawing each cell and its walls. It operates on an instance of the Maze class, ensuring a clear separation between maze logic and rendering concerns.

### GUI Abstractions:

- **App Class**: Serving as the parent class, App encapsulates the Tkinter instance and provides methods for managing the application lifecycle. It establishes the entry point for the application and orchestrates interactions between different GUI components and maze logic.
- **AppConfig Class**: Responsible for configuring the canvas and creating various widgets necessary for the user interface. By delegating widget creation to AppConfig, the main application logic remains decoupled from GUI implementation details.
- **CanvasFrame Class**: Acting as an intermediary between user input and maze-related drawing operations, CanvasFrame abstracts away the complexities of coordinating maze visualization. It interfaces with both the GUI components and the MazeDrawer class, ensuring seamless integration between user interaction and maze rendering.

Through careful application of composition and abstraction, I achieved a design that promotes maintainability, scalability, and code reusability. Each class fulfills a specific role within the application architecture, contributing to a clear separation of concerns and facilitating the synchronization of GUI and maze logic. This modular design approach fosters extensibility, allowing for easy integration of additional features or enhancements in the future.

## Learning opportunites

I wanted to keep the logic related to constructing the maze and solving it in a separate class so that they can be tested separately. This was also helpful for me as I learned how to use Tkinter's Canvas widget which is useful because you don't have to create new windows every time the maze needs to be drawn. I also wanted to learn more about using unittest and writing tests in python, so that I can keep my code DRY and maintainable. I utilized mock objects so when testing certain functionality, I could test it without actually creating a window or canvas object.

My primary focus with this project was to use some data structures and algorithms in an actual project. For example, when the maze is being solved, if the path reaches a deadend, how does it know which valid direction it can move within the maze? I was able to define the coordinates of all the cells sorrounding a given cell and then check if any are blocked by a wall. If they are, it will check another random direction's coordinates. If they are not, then the path can move in that direction. In my solution's algorithm, I kept track of which cells had already been visited so that when backtracking, the path is not drawn in the same direction and it can continue to traverse until it reaches a logical end and then recursively backtrack until the end is reached.
