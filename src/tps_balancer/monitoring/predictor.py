import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from typing import List, Optional

class DemandPredictor:
    def __init__(self, look_back: int = 24):
        self.look_back = look_back
        self.model: Optional[Sequential] = None
        
    def build_model(self, n_features: int):
        self.model = Sequential([
            LSTM(50, input_shape=(self.look_back, n_features)),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mse')
        
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 50):
        if self.model is None:
            self.build_model(X.shape[2])
        self.model.fit(X, y, epochs=epochs, verbose=0)
        
    def predict(self, history: np.ndarray) -> float:
        if self.model is None:
            raise RuntimeError("Model not trained")
        return self.model.predict(history[np.newaxis, ...])[0,0]