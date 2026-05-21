import pandas as pd
import json
from models.auto_forecaster import AutoForecaster


def main():
    # Load dataset
    df = pd.read_csv("data/passengers.csv")
    df["ds"] = pd.to_datetime(df["ds"])

    print("Dataset loaded:")
    print(df.tail(5))
    print()

    # Run AutoForecaster
    forecaster = AutoForecaster()
    result     = forecaster.forecast(df, horizon=12)  # forecast 12 months ahead

    # Print results nicely
    print("\n📊 FORECAST RESULTS")
    print("=" * 50)
    print(f"Model used    : {result['model'].upper()}")
    print(f"MAE score     : {result['mae']}")
    print(f"\nAll model scores:")
    for model, mae in result["all_scores"].items():
        winner = " 🏆" if model == result["model"] else ""
        print(f"  {model:<10} MAE = {mae}{winner}")

    print(f"\nForecast for next 12 months:")
    print(f"{'Date':<15} {'Predicted':>10} {'Lower':>10} {'Upper':>10}")
    print("-" * 50)
    for i in range(len(result["dates"])):
        print(f"{result['dates'][i]:<15} "
              f"{result['predictions'][i]:>10.1f} "
              f"{result['lower_bound'][i]:>10.1f} "
              f"{result['upper_bound'][i]:>10.1f}")

    # Save result to JSON
    with open("data/forecast_result.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n✅ Result saved to data/forecast_result.json")


if __name__ == "__main__":
    main()