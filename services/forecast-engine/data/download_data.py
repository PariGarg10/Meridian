import pandas as pd
import os

# Air passengers dataset — monthly data from 1949 to 1960
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"

df = pd.read_csv(url, header=0)
df.columns = ["ds", "y"]

# Prophet requires columns named exactly "ds" and "y"
# ds = date, y = value to forecast

# Convert to proper date format
df["ds"] = pd.to_datetime(df["ds"])

# Save locally
os.makedirs("data", exist_ok=True)
df.to_csv("data/passengers.csv", index=False)

print("Dataset downloaded successfully!")
print(df.head(10))
print(f"Total rows: {len(df)}")