from SudokuGame import SudokuGame
from SudokuSolver import SudokuSolver

def main():
    game = SudokuGame()
    game.generate_puzzle(clues=9)  # You can adjust the number of clues to change difficulty
    print("Initial Sudoku Board:")
    game.print_board()

    solver = SudokuSolver(game)
    if solver.solve():
        print("\nSolved Sudoku Board:")
        game.print_board()
    else:
        print("No solution exists.")

if __name__ == "__main__":
    main()
