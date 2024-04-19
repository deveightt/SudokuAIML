import numpy as np
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Input, Dense, Conv2D, Flatten
from keras.layers import Reshape
from keras.utils import to_categorical
from keras.losses import CategoricalCrossentropy

def create_model():
    model = Sequential([
        Input(shape=(9, 9, 1)),
        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        Conv2D(64, (3, 3), activation='relu'),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(81 * 9, activation='softmax'),  # 81 positions, each with 9 possible values
        Reshape((81, 9))  # Reshape the output to match 81 positions each with 9 probabilities
    ])
    model.compile(optimizer='adam', loss=CategoricalCrossentropy(), metrics=['accuracy'])
    return model

def train_model():
    puzzles = np.load('puzzles.npy').reshape(-1, 9, 9, 1)
    solutions = np.load('solutions.npy').reshape(-1, 81)  # Ensure solutions are integers 1-9 for each cell

    model = create_model()
    model.fit(puzzles, to_categorical(solutions - 1, num_classes=9), epochs=20, validation_split=0.1)

    model.save('sudoku_model.h5')
    print("Model saved as sudoku_model.h5")

if __name__ == "__main__":
    train_model()