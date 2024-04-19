import numpy as np

def view_npy_contents(file_path, num_examples=5):
    data = np.load(file_path)
    print(f"Shape of the data in '{file_path}': {data.shape}")
    print("Sample data:")
    for i in range(num_examples):
        print(f"Example {i+1}:")
        # Reshape each example into a 9x9 grid for display
        grid = data[i].reshape(9, 9)
        for row in grid:
            print(' '.join(map(str, row)))
        print("\n")  # Add a newline for better separation between examples

if __name__ == "__main__":
    view_npy_contents('puzzles.npy')
    view_npy_contents('solutions.npy')
