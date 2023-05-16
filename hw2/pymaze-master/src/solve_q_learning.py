from __future__ import absolute_import
from maze_manager import MazeManager


if __name__ == "__main__":

    # Create the manager
    manager = MazeManager()

    # Add 3 20x20 mazes to the manager
    maze = manager.add_maze(20, 20)
    maze2 = manager.add_maze(20, 20)
    maze3 = manager.add_maze(20, 20)

    # Solve mazes using the Q-Learning algorithm
    manager.solve_maze(maze.id, "QLearning")
    manager.solve_maze(maze2.id, "QLearning")
    manager.solve_maze(maze3.id, "QLearning")

    # Show how the maze was solved
    # manager.show_solution_animation(maze.id)

    # Display the maze with the solution overlaid
    manager.show_solution(maze.id)
    manager.show_solution(maze2.id)
    manager.show_solution(maze3.id)
