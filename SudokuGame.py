import random
import numpy as np
from keras.models import load_model

class SudokuGame:
    def __init__(self, grid=None, use_model=False):
        self.grid = np.zeros((9, 9), dtype=int) if grid is None else np.array(grid, dtype=int)
        if use_model:
            self.model = load_model('sudoku_model.h5')
        else:
            self.model = None
            self.solve()

    def print_board(self):
        for row in self.grid:
            print(" ".join(str(num) if num != 0 else '.' for num in row))

    def solve_with_model(self):
        if not self.model:
            print("Model not loaded")
            return False
        puzzle = self.grid.reshape((1, 9, 9, 1))
        solution = self.model.predict(puzzle).argmax(axis=-1).reshape((9, 9)) + 1
        self.grid = solution
        return True

    def solve(self):
        if not self.try_to_solve(0):
            print("Failed to generate a valid board")

    def try_to_solve(self, position):
        if position == 81:
            return True
        row, col = divmod(position, 9)
        if self.grid[row][col] == 0:
            for num in np.random.permutation(range(1, 10)):
                if self.is_safe(row, col, num):
                    self.grid[row][col] = num
                    if self.try_to_solve(position + 1):
                        return True
                    self.grid[row][col] = 0
        else:
            return self.try_to_solve(position + 1)
        return False

    def is_safe(self, row, col, num):
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        if num in self.grid[row, :] or num in self.grid[:, col] or num in self.grid[box_row:box_row+3, box_col:box_col+3]:
            return False
        return True

    def generate_puzzle(self, clues=25):
        self.solve()  # Ensure the board is solved first
        empty_cells = np.random.choice(81, 81-clues, replace=False)
        np.put(self.grid, empty_cells, 0)
