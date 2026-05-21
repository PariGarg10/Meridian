import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_error


class ProphetForecaster:
    """
    Facebook Prophet model.
    Best for: data with strong seasonal patterns (weekly, yearly cycles)
    """

    def __init__(self):
        self.model = None
        self.mae = None

    def train_and_evaluate(self, df: pd.DataFrame, horizon: int) -> dict:
        """
        Train Prophet on 80% of data, evaluate on last 20%, then
        forecast future `horizon` days.

        Args:
            df: DataFrame with columns 'ds' (date) and 'y' (value)
            horizon: number of future days to forecast

        Returns:
            dict with predictions, upper/lower bounds, and MAE score
        """

        # Split into train (80%) and test (20%)
        split_idx = int(len(df) * 0.8)
        train_df = df.iloc[:split_idx]
        test_df  = df.iloc[split_idx:]

        # Train the model
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,  # monthly data, no weekly pattern
            daily_seasonality=False,
            interval_width=0.95        # 95% confidence interval
        )
        self.model.fit(train_df)

        # Evaluate on test set
        test_future   = self.model.make_future_dataframe(periods=len(test_df), freq="MS")
        test_forecast = self.model.predict(test_future)
        test_preds    = test_forecast["yhat"].iloc[split_idx:].values
        self.mae      = mean_absolute_error(test_df["y"].values, test_preds)

        # Now retrain on FULL data and forecast future
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            interval_width=0.95
        )
        self.model.fit(df)

        future   = self.model.make_future_dataframe(periods=horizon, freq="MS")
        forecast = self.model.predict(future)

        # Return only the future predictions (not historical)
        future_forecast = forecast.iloc[len(df):]

        return {
            "model":       "prophet",
            "mae":         round(self.mae, 4),
            "dates":       future_forecast["ds"].dt.strftime("%Y-%m-%d").tolist(),
            "predictions": future_forecast["yhat"].round(2).tolist(),
            "upper_bound": future_forecast["yhat_upper"].round(2).tolist(),
            "lower_bound": future_forecast["yhat_lower"].round(2).tolist(),
        }