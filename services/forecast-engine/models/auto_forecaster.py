import pandas as pd
import time
from models.prophet_model import ProphetForecaster
from models.arima_model   import ARIMAForecaster
from models.lstm_model    import LSTMForecaster


class AutoForecaster:
    """
    Runs all 3 models and picks the best one automatically.
    Selection criteria: lowest MAE on holdout set.
    """

    def forecast(self, df: pd.DataFrame, horizon: int) -> dict:
        """
        Run Prophet, ARIMA, and LSTM. Return best result.

        Args:
            df: DataFrame with 'ds' and 'y' columns
            horizon: number of future periods to forecast

        Returns:
            dict with best forecast + all model scores
        """

        print("\n🔮 Meridian AutoForecaster starting...")
        print(f"   Dataset size : {len(df)} rows")
        print(f"   Horizon      : {horizon} months ahead\n")

        results = {}

        # --- Run Prophet ---
        print("⏳ Running Prophet...")
        start = time.time()
        try:
            prophet    = ProphetForecaster()
            results["prophet"] = prophet.train_and_evaluate(df, horizon)
            elapsed    = round(time.time() - start, 2)
            print(f"   ✅ Prophet done — MAE: {results['prophet']['mae']} ({elapsed}s)")
        except Exception as e:
            print(f"   ❌ Prophet failed: {e}")

        # --- Run ARIMA ---
        print("⏳ Running ARIMA...")
        start = time.time()
        try:
            arima      = ARIMAForecaster()
            results["arima"] = arima.train_and_evaluate(df, horizon)
            elapsed    = round(time.time() - start, 2)
            print(f"   ✅ ARIMA done  — MAE: {results['arima']['mae']} ({elapsed}s)")
        except Exception as e:
            print(f"   ❌ ARIMA failed: {e}")

        # --- Run LSTM ---
        print("⏳ Running LSTM...")
        start = time.time()
        try:
            lstm       = LSTMForecaster()
            results["lstm"] = lstm.train_and_evaluate(df, horizon)
            elapsed    = round(time.time() - start, 2)
            print(f"   ✅ LSTM done   — MAE: {results['lstm']['mae']} ({elapsed}s)")
        except Exception as e:
            print(f"   ❌ LSTM failed: {e}")

        # --- Pick best model ---
        best_name   = min(results, key=lambda x: results[x]["mae"])
        best_result = results[best_name]

        print(f"\n🏆 Best model: {best_name.upper()} "
              f"(MAE: {best_result['mae']})\n")

        # Attach all scores for transparency
        best_result["all_scores"] = {
            name: res["mae"] for name, res in results.items()
        }

        return best_result
        