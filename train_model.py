import numpy as np
from tensorflow import keras
from keras.models import Sequential, load_model
from keras.layers import Input, Dense, Conv2D, Flatten
from keras.layers import Reshape, Dropout, BatchNormalization
from keras.utils import to_categorical
from keras.losses import CategoricalCrossentropy
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import Adam
from keras.optimizers.schedules import ExponentialDecay
from keras.regularizers import l2

def create_model():
    model = Sequential([
        Input(shape=(9, 9, 1)),
        Conv2D(128, kernel_size=(3, 3), activation='relu', kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        Dropout(0.3),
        Conv2D(128, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),
        Dropout(0.3),
        Flatten(),
        Dense(256, activation='relu', kernel_regularizer=l2(0.001)),
        Dropout(0.3),
        Dense(81 * 9, activation='softmax'),
        Reshape((81, 9))
    ])
    model.compile(optimizer='adam', loss=CategoricalCrossentropy(), metrics=['accuracy'])
    return model

def train_model(model_path=None):
    puzzles = np.load('puzzles.npy').reshape(-1, 9, 9, 1)
    solutions = np.load('solutions.npy').reshape(-1, 81)  # Ensure solutions are integers 1-9 for each cell

    lr_schedule = ExponentialDecay(
        initial_learning_rate=0.001,
        decay_steps=10000,
        decay_rate=0.9,
        staircase=True
    )

    if model_path:
        try:
            model = load_model(model_path)
            # Recompile the model to reset the optimizer
            model.compile(optimizer=Adam(learning_rate=lr_schedule), loss=CategoricalCrossentropy(), metrics=['accuracy'])
            print("Model loaded and recompiled successfully.")
        except Exception as e:
            print(f"Failed to load model. A new model will be created. Error: {e}")
            model = create_model()
    else:
        model = create_model()

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    )

    model_checkpoint = ModelCheckpoint(
        'best_sudoku_model.keras',
        save_best_only=True,
        monitor='val_accuracy',
        mode='max'
    )

    model.fit(puzzles, to_categorical(solutions - 1, num_classes=9), epochs=500, validation_split=0.1, callbacks=[early_stopping, model_checkpoint])

    model.save('sudoku_model.keras')
    print("Model saved as sudoku_model.keras")

if __name__ == "__main__":
    # train_model('sudoku_model.h5')
    train_model()