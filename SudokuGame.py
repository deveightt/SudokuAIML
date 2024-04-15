import random
from SudokuSolver import SudokuSolver


class SudokuGame:
    def __init__(self, grid=None):
        if grid is None:
            self.grid = [[0]*9 for _ in range(9)]
        else:
            self.grid = grid

    def print_board(self):
        for row in self.grid:
            print(" ".join(str(num) if num != 0 else '.' for num in row))

    def is_safe(self, row, col, num):
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        if any(self.grid[row][i] == num for i in range(9)):
            return False
        if any(self.grid[i][col] == num for i in range(9)):
            return False
        if any(self.grid[box_row + i // 3][box_col + i % 3] == num for i in range(9)):
            return False
        return True

    def fill_values(self):
        for i in range(81):
            row, col = divmod(i, 9)
            if self.grid[row][col] == 0:
                random.shuffle(num := list(range(1, 10)))
                for n in num:
                    if self.is_safe(row, col, n):
                        self.grid[row][col] = n
                        if self.fill_values():
                            return True
                        self.grid[row][col] = 0
                return False
        return True
    
    def generate_puzzle(self, clues):
        self.fill_values()
        empty_spots = 81 - clues
        while empty_spots > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.grid[row][col] != 0:
                self.grid[row][col] = 0
                empty_spots -= 1