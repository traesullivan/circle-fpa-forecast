import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Load financial data
file_path = "circle_financial_data.csv" 
df = pd.read_csv(file_path, parse_dates=['Date'])

# Extract Date
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Metrics to Forevasr
metrics = ['Subscribers', 'New Subscribers', 'Churned Subscribers', 'MRR', 'Expenses', 'Profit']

# Forecast Dataframe
forecast_horizon = 48  
future_dates = pd.date_range(start='2025-01-01', periods=forecast_horizon, freq='M')

# Initialize DataFrame with Date, Year, and Month
forecast_data = pd.DataFrame({'Date': future_dates})
forecast_data['Year'] = forecast_data['Date'].dt.year
forecast_data['Month'] = forecast_data['Date'].dt.month

# Forecasr each metric using Exponential Smoothing (ETS)
for metric in metrics:
    model = ExponentialSmoothing(df[metric], trend="add", seasonal="add", seasonal_periods=12)
    fitted_model = model.fit()
    forecast_values = fitted_model.forecast(steps=forecast_horizon)

    # Append forecasted values to DataFrame
    forecast_data[metric] = forecast_values.values

    # Plot Values
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df[metric], label=f'Actual {metric}', color='blue')
    plt.plot(forecast_data['Date'], forecast_data[metric], label=f'Forecast {metric} (2025-2028)', linestyle='dashed', color='grey')
    plt.title(f'{metric} Forecast (2025-2028)')
    plt.xlabel('Year')
    plt.ylabel(metric)
    plt.legend()
    plt.grid()
    plt.show()

# Combine actual + forecasted data
full_data = pd.concat([df, forecast_data], ignore_index=True)



