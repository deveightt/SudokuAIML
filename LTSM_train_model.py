import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense, Reshape, Dropout
from keras.utils import to_categorical
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.models import load_model



def create_model():
    model = Sequential([
        LSTM(128, input_shape=(81, 1), return_sequences=True),
        Dropout(0.3),
        LSTM(128, return_sequences=True),
        Dropout(0.3),
        Dense(9, activation='softmax'),
        Reshape((81, 9))
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train_model(model_path=None):
    puzzles = np.load('puzzles.npy').reshape(-1, 9, 9, 1)
    solutions = np.load('solutions.npy').reshape(-1, 81)

    model = create_model() if model_path is None else load_model(model_path)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='min', restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.0001, verbose=1)

    model.fit(puzzles, to_categorical(solutions - 1, num_classes=9), epochs=500, validation_split=0.1,
              callbacks=[early_stopping, reduce_lr])

    model.save('sudoku_model.h5')
    print("Model saved as sudoku_model.h5")

if __name__ == "__main__":
    train_model()
