import random
from SudokuSolver import SudokuSolver

class SudokuGame:
    def __init__(self, grid=None):
        self.grid = [[0] * 9 for _ in range(9)]
        self.fill_values()

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
        def backtrack(position=0):
            if position == 81:
                return True
            row, col = divmod(position, 9)
            if self.grid[row][col] == 0:
                nums = random.sample(range(1, 10), 9)
                for num in nums:
                    if self.is_safe(row, col, num):
                        self.grid[row][col] = num
                        if backtrack(position + 1):
                            return True
                        self.grid[row][col] = 0
                return False
            return backtrack(position + 1)

        if not backtrack():
            print("Failed to fill the board. Retrying...")
            self.grid = [[0] * 9 for _ in range(9)]
            self.fill_values()

        
    def generate_puzzle(self):
        # Map each number to its positions on a fully solved board
        number_positions = {i: [] for i in range(1, 10)}
        for row in range(9):
            for col in range(9):
                num = self.grid[row][col]
                number_positions[num].append((row, col))

        # Select exactly one position for each number
        chosen_positions = set()
        for num in range(1, 10):
            valid_positions = [pos for pos in number_positions[num] if pos not in chosen_positions]
            if valid_positions:
                chosen_position = random.choice(valid_positions)
                chosen_positions.add(chosen_position)

        # Clear all cells except the chosen positions
        for row in range(9):
            for col in range(9):
                if (row, col) not in chosen_positions:
                    self.grid[row][col] = 0