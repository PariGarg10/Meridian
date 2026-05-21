import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import warnings
warnings.filterwarnings("ignore")


class LSTMForecaster:
    """
    LSTM (Long Short-Term Memory) neural network.
    Best for: complex patterns, large datasets, non-linear relationships
    """

    def __init__(self, lookback: int = 12):
        """
        lookback: how many past months to look at to predict the next one
        12 = look at last 12 months to predict next month
        """
        self.lookback = lookback
        self.scaler   = MinMaxScaler(feature_range=(0, 1))
        self.model    = None
        self.mae      = None

    def _create_sequences(self, data: np.ndarray):
        """Convert flat array into (X, y) sequences for LSTM"""
        X, y = [], []
        for i in range(self.lookback, len(data)):
            X.append(data[i - self.lookback:i, 0])
            y.append(data[i, 0])
        return np.array(X), np.array(y)

    def _build_model(self) -> Sequential:
        model = Sequential([
            LSTM(50, return_sequences=True,
                 input_shape=(self.lookback, 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        model.compile(optimizer="adam", loss="mean_squared_error")
        return model

    def train_and_evaluate(self, df: pd.DataFrame, horizon: int) -> dict:
        """
        Train LSTM, evaluate on holdout set, forecast future.

        Args:
            df: DataFrame with columns 'ds' (date) and 'y' (value)
            horizon: number of future steps to forecast

        Returns:
            dict with predictions, upper/lower bounds, and MAE score
        """

        values = df["y"].values.reshape(-1, 1)

        # Scale data to 0-1 range (LSTM needs this)
        scaled = self.scaler.fit_transform(values)

        # Split 80/20
        split_idx    = int(len(scaled) * 0.8)
        train_scaled = scaled[:split_idx]
        test_scaled  = scaled[split_idx - self.lookback:]  # include lookback

        # Create sequences
        X_train, y_train = self._create_sequences(train_scaled)
        X_test,  y_test  = self._create_sequences(test_scaled)

        # Reshape for LSTM: (samples, timesteps, features)
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test  = X_test.reshape((X_test.shape[0],  X_test.shape[1],  1))

        # Train
        self.model = self._build_model()
        self.model.fit(
            X_train, y_train,
            epochs=50,
            batch_size=8,
            verbose=0  # silent training
        )

        # Evaluate
        test_preds_scaled = self.model.predict(X_test, verbose=0)
        test_preds        = self.scaler.inverse_transform(test_preds_scaled)
        actual            = self.scaler.inverse_transform(
                                y_test.reshape(-1, 1))
        self.mae          = mean_absolute_error(actual, test_preds)

        # Forecast future — rolling prediction
        last_sequence = scaled[-self.lookback:].flatten().tolist()
        future_preds  = []

        for _ in range(horizon):
            seq        = np.array(last_sequence[-self.lookback:]).reshape(1, self.lookback, 1)
            next_pred  = self.model.predict(seq, verbose=0)[0][0]
            future_preds.append(next_pred)
            last_sequence.append(next_pred)

        # Inverse scale
        future_preds_array  = np.array(future_preds).reshape(-1, 1)
        future_preds_actual = self.scaler.inverse_transform(
                                  future_preds_array).flatten()

        # Simple confidence interval (±10% for LSTM)
        upper = (future_preds_actual * 1.10).tolist()
        lower = (future_preds_actual * 0.90).tolist()

        # Generate future dates
        last_date    = pd.to_datetime(df["ds"].iloc[-1])
        future_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=horizon,
            freq="MS"
        )

        return {
            "model":       "lstm",
            "mae":         round(self.mae, 4),
            "dates":       future_dates.strftime("%Y-%m-%d").tolist(),
            "predictions": [round(x, 2) for x in future_preds_actual.tolist()],
            "upper_bound": [round(x, 2) for x in upper],
            "lower_bound": [round(x, 2) for x in lower],
        }