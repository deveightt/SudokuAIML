import numpy as np
from multiprocessing import Pool
from SudokuGame import SudokuGame

def generate_single_puzzle(clues):
    game = SudokuGame()
    game.generate_puzzle(clues)  # Generate the puzzle with missing clues
    puzzle = game.grid.copy()  # Make a copy of the puzzle grid before solving
    game.solve()  # Solve the puzzle
    solution = game.grid.copy()  # Make a copy of the solved grid
    return puzzle.flatten(), solution.flatten()

def generate_data(num_samples, clues=25):
    with Pool(processes=6) as pool:  # Utilize multiple processes for faster generation
        results = pool.starmap(generate_single_puzzle, [(clues,) for _ in range(num_samples)])
    puzzles, solutions = zip(*results)
    return np.array(puzzles), np.array(solutions)

if __name__ == "__main__":
    num_samples = 50
    puzzles, solutions = generate_data(num_samples)
    np.save("puzzles.npy", puzzles)
    np.save("solutions.npy", solutions)
    print("Data saved successfully.")
