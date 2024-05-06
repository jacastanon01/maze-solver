# Deterministic Maze Generator 🔍

![maze_demo](https://github.com/jacastanon01/maze-solver/assets/24418510/afc3aed4-cdbf-4c79-89fd-8076d49685d4)

This is a small application that utilizes a Tkinter-powered GUI showcasing maze generation and solving. Embracing randomness, the maze's intricate walls are dynamically crafted. Witness the maze-solving journey unfold with a depth-first search algorithm, observing each step as it navigates and backtracks until reaching the elusive exit.

## Project Design Overview 📋

In addressing the challenge of maintaining separation between different components and structuring them effectively within the maze project, I adopted a design approach centered around modularity and encapsulation. The project architecture consists of several distinct classes, each with well-defined responsibilities and interfaces, contributing to a cohesive and maintainable codebase.

### Maze Module 🧩

- **Maze Class**: This class encapsulates the properties of the maze, such as its dimensions, position, and other relevant attributes. It serves as the foundational representation of the maze structure.
- **MazeSolver Class**: Responsible for implementing the algorithms and logic required to solve the maze. By abstracting solving functionality into a separate class, the Maze class remains focused solely on representing the maze's static properties.
- **MazeDrawer Class**: This class facilitates the visualization of the maze by recursively drawing each cell and its walls. It operates on an instance of the Maze class, ensuring a clear separation between maze logic and rendering concerns.

### GUI Abstractions 🖼️

- **App Class**: Serving as the parent class, App encapsulates the Tkinter instance and provides methods for managing the application lifecycle. It establishes the entry point for the application and orchestrates interactions between different GUI components and maze logic.
- **AppConfig Class**: Responsible for configuring the canvas and creating various widgets necessary for the user interface. By delegating widget creation to AppConfig, the main application logic remains decoupled from GUI implementation details.
- **CanvasFrame Class**: Acting as an intermediary between user input and maze-related drawing operations, CanvasFrame abstracts away the complexities of coordinating maze visualization. It interfaces with both the GUI components and the MazeDrawer class, ensuring seamless integration between user interaction and maze rendering.

Through careful application of composition and abstraction, I achieved a design that promotes maintainability, scalability, and code reusability. Each class fulfills a specific role within the application architecture, contributing to a clear separation of concerns and facilitating the synchronization of GUI and maze logic. This modular design approach fosters extensibility, allowing for easy integration of additional features or enhancements in the future.

## Learning opportunites 📓

Throughout this project, my focus was on applying data structures and algorithms in a practical setting. I structured the logic related to maze construction and solving into separate classes to facilitate modular testing. This separation also allowed me to delve into the usage of Tkinter's Canvas widget, which proved invaluable for drawing the maze without the need to create new windows each time. By leveraging the unittest framework and employing mock objects, I could test specific functionalities without instantiating actual window or canvas objects. This approach not only helped in ensuring the correctness of my code but also reinforced the principles of DRY (Don't Repeat Yourself) and maintainability.

One of the intriguing challenges I encountered was determining valid directions for path traversal during maze solving. I devised an algorithm that identifies surrounding cells' coordinates and evaluates their accessibility based on wall obstruction. If a direction is blocked, the algorithm explores alternate paths until finding an unobstructed route. By tracking visited cells and implementing recursive backtracking, the algorithm effectively navigates through the maze, ensuring thorough exploration and efficient pathfinding.

## Demo 🚀

- Install python3 on your machine
- Clone this repo
- Run `./main.sh` to launch GUI application
- Enter a number for rows and columns in the text box at the top of the window
- Click the "Generate Maze" button or Enter to generate a new maze
- Click the "Solve Maze" button or Enter to solve the maze
- Click the "Reset Maze" button or Enter after solving maze to reset the maze

## Technologies Used 🛠️

- Python 3.12.1
- Tkinter
- unittest library for tests
- random module to generate random directions
- Type hinting and docstrings to improve readability
