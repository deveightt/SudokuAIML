import random
import numpy as np
from tensorflow import keras
from keras.models import load_model

class SudokuGame:
    def __init__(self, grid=None, use_model=False):
        self.grid = [[0] * 9 for _ in range(9)] if grid is None else grid
        if use_model:
            self.model = load_model('sudoku_model.h5')
        else:
            self.model = None
            self.fill_values()  # Call fill_values() to randomize the board at initialization

    def print_board(self):
        for row in self.grid:
            print(" ".join(str(num) if num != 0 else '.' for num in row))
    
    def solve_with_model(self):
        if not self.model:
            print("Model not loaded")
            return False
        puzzle = np.array([cell for row in self.grid for cell in row]).reshape((1, 9, 9, 1))
        solution = self.model.predict(puzzle).argmax(axis=-1).reshape((9, 9)) + 1
        self.grid = solution.tolist()
        return True

    def fill_values(self):
        # Randomize the first row
        self.grid[0] = random.sample(range(1, 10), 9)
        # Attempt to solve it from the second row onwards
        if not self.backtrack(9):
            print("Failed to generate a valid board")

    def backtrack(self, position):
        if position == 81:
            return True  # Sudoku successfully filled
        row, col = divmod(position, 9)
        if self.grid[row][col] == 0:
            possible_numbers = list(range(1, 10))
            random.shuffle(possible_numbers)  # Shuffle numbers to ensure randomness
            for num in possible_numbers:
                if self.is_safe(row, col, num):
                    self.grid[row][col] = num
                    if self.backtrack(position + 1):
                        return True
                    self.grid[row][col] = 0
        else:
            return self.backtrack(position + 1)
        return False

    def is_safe(self, row, col, num):
        # Check row, column, and 3x3 box
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        if any(self.grid[row][x] == num for x in range(9)) or any(self.grid[x][col] == num for x in range(9)) or any(self.grid[box_row + x // 3][box_col + x % 3] == num for x in range(9)):
            return False
        return True

    def generate_puzzle(self):
        self.fill_values()  # Ensure the board is initially filled with a valid solution
        # Implement logic to remove numbers to form a puzzle
