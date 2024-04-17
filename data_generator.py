import numpy as np
from SudokuGame import SudokuGame
from SudokuSolver import SudokuSolver

def generate_data(num_samples):
    puzzles, solutions = [], []
    for _ in range(num_samples):
        game = SudokuGame()
        game.generate_puzzle()
        puzzle = [cell for row in game.grid for cell in row]
        solver = SudokuSolver(game)
        solver.solve()
        solution = [cell for row in game.grid for cell in row]
        puzzles.append(puzzle)
        solutions.append(solution)
    return np.array(puzzles), np.array(solutions)

if __name__ == "__main__":
    num_samples = 1000
    puzzles, solutions = generate_data(num_samples)
    np.save("puzzles.npy", puzzles)
    np.save("solutions.npy", solutions)
    print("Data saved successfully.")
