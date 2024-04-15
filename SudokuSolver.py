class SudokuSolver:
    def __init__(self, game):
        self.game = game

    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.game.grid[i][j] == 0:
                    return i, j
        return None
    
    def solve(self):
        empty = self.find_empty_location()
        if not empty:
            return True  # Puzzle solved
        row, col = empty

        for num in range(1, 10):
            if self.game.is_safe(row, col, num):
                self.game.grid[row][col] = num
                if self.solve():
                    return True
                self.game.grid[row][col] = 0

        return False  # Trigger backtracking