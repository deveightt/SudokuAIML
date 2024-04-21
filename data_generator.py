import numpy as np
import time
from multiprocessing import Pool
from SudokuGame import SudokuGame

def generate_single_puzzle(clues):
    game = SudokuGame()
    game.generate_puzzle(clues)  # Generate the puzzle with missing clues
    puzzle = game.grid.copy()  # Make a copy of the puzzle grid before solving
    game.solve()  # Solve the puzzle
    solution = game.grid.copy()  # Make a copy of the solved grid
    
    operations = ['rotate', 'flip_h', 'flip_v']
    augmented_data = [(puzzle.flatten(), solution.flatten())]  # Include the original first
    for op in operations:
        aug_puzzle = augment_puzzle(puzzle, op)
        aug_solution = augment_puzzle(solution, op)
        augmented_data.append((aug_puzzle, aug_solution))
    
    return augmented_data  # Return a list of tuples

def augment_puzzle(puzzle, operation):
    grid = puzzle.reshape(9, 9)
    if operation == 'rotate':
        return np.rot90(grid).flatten()
    elif operation == 'flip_h':
        return np.flipud(grid).flatten()
    elif operation == 'flip_v':
        return np.fliplr(grid).flatten()
    return grid.flatten()

def generate_data(num_samples, clues=25):
    with Pool(processes=8) as pool:  
        results = pool.starmap(generate_single_puzzle, [(clues,) for _ in range(num_samples)])
    puzzles, solutions = zip(*[item for sublist in results for item in sublist])
    return np.array(puzzles), np.array(solutions)

if __name__ == "__main__":
    num_samples = 2000  
    start_time = time.time()
    puzzles, solutions = generate_data(num_samples)
    np.save("puzzles.npy", puzzles)
    np.save("solutions.npy", solutions)
    elapsed_time = time.time() - start_time
    print(f"Data saved successfully. Time taken: {elapsed_time:.2f} seconds.")
