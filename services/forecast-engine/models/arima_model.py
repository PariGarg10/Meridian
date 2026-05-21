import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings("ignore")


class ARIMAForecaster:
    """
    ARIMA model.
    Best for: smooth, stable trends without strong seasonality
    """

    def __init__(self):
        self.mae   = None
        self.order = (2, 1, 2)

    def train_and_evaluate(self, df: pd.DataFrame, horizon: int) -> dict:

        # Extract values as plain numpy array
        values = np.array(df["y"].values, dtype=float)

        # Split 80/20
        split_idx  = int(len(values) * 0.8)
        train_vals = values[:split_idx]
        test_vals  = values[split_idx:]

        # Walk-forward evaluation
        predictions = []
        history     = list(train_vals)

        for i in range(len(test_vals)):
            try:
                model     = ARIMA(history, order=self.order)
                model_fit = model.fit()
                yhat      = float(model_fit.forecast(steps=1)[0])
            except:
                yhat = float(history[-1])  # fallback to last value
            predictions.append(yhat)
            history.append(float(test_vals[i]))

        self.mae = mean_absolute_error(test_vals, predictions)

        # Retrain on full data
        full_model     = ARIMA(values, order=self.order)
        full_model_fit = full_model.fit()
        forecast_obj   = full_model_fit.get_forecast(steps=horizon)

        forecast_mean = np.array(forecast_obj.predicted_mean, dtype=float)
        conf_int      = forecast_obj.conf_int(alpha=0.05)
        conf_int_array = np.array(conf_int, dtype=float)
        upper = conf_int_array[:, 1]
        lower = conf_int_array[:, 0]

        # Generate future dates
        last_date    = pd.to_datetime(df["ds"].iloc[-1])
        future_dates = pd.date_range(
            start  = last_date + pd.DateOffset(months=1),
            periods= horizon,
            freq   = "MS"
        )

        return {
            "model":       "arima",
            "mae":         round(float(self.mae), 4),
            "dates":       future_dates.strftime("%Y-%m-%d").tolist(),
            "predictions": [round(float(x), 2) for x in forecast_mean],
            "upper_bound": [round(float(x), 2) for x in upper],
            "lower_bound": [round(float(x), 2) for x in lower],
        }