import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from datetime import timedelta
import numpy as np

class WeightPredictor:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def predict(self, output_csv, output_plot, days_ahead):
        df = pd.read_csv(self.csv_path)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').drop_duplicates('date')
        df['days_elapsed'] = (df['date'] - df['date'].min()).dt.days

        poly = PolynomialFeatures(degree=4)
        X = poly.fit_transform(df[['days_elapsed']])
        model = LinearRegression().fit(X, df['weight'])

        future_range = [df['days_elapsed'].max() + i for i in range(1, days_ahead + 1)]
        future_dates = [df['date'].max() + timedelta(days=i) for i in range(1, days_ahead + 1)]
        future_df = pd.DataFrame(future_range, columns=['days_elapsed'])
        future_X = poly.transform(future_df)
        forecast = model.predict(future_X)

        lower_bound = forecast - 0.5
        upper_bound = forecast + 0.5

        plt.figure(figsize=(12, 6))
        plt.plot(df['date'], df['weight'], label='History', marker='o')
        plt.plot(df['date'], model.predict(X), label='Trend', color='orange')
        plt.plot(future_dates, forecast, label=f'Forecast ({days_ahead}d)', linestyle='--', color='green')
        plt.fill_between(future_dates, lower_bound, upper_bound, color='green', alpha=0.2, label='±0.5kg')
        plt.title(f'Weight Forecast ({days_ahead} days)')
        plt.xlabel('Date')
        plt.ylabel('Weight (kg)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_plot)

        forecast_df = pd.DataFrame({
            'date': future_dates,
            'predicted_weight': forecast,
            'min': lower_bound,
            'max': upper_bound
        })

        forecast_df.to_csv(output_csv, index=False)

        print(f"Saved plot: {output_plot}")
        print(f"Saved forecast: {output_csv}")
