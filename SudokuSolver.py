import time
import os

class SudokuSolver:
    def __init__(self, game):
        self.game = game

    def print_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.game.grid:
            print(" ".join(str(num) if num != 0 else '.' for num in row))
        # time.sleep(0.00001)  

    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.game.grid[i, j] == 0:
                    return i, j
        return None
    
    def solve(self):
        empty = self.find_empty_location()
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            if self.game.is_safe(row, col, num):
                self.game.grid[row, col] = num
                if self.solve():
                    return True
                self.game.grid[row, col] = 0

        return False
