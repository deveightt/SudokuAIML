import time
from SudokuGame import SudokuGame
from SudokuSolver import SudokuSolver

def main():
    game = SudokuGame()
    game.generate_puzzle()  
    print("Initial Sudoku Board:")
    game.print_board()

    solver = SudokuSolver(game)

    start_time = time.time()
    if solver.solve():
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("\nSolved Sudoku Board (solved in {:.2f} seconds):".format(elapsed_time))
        game.print_board()
    else:
        print("No solution exists.")

if __name__ == "__main__":
    main()
