import pandas as pd
import matplotlib.pyplot as plt


def plot_forecast(data, title, ylabel, filename=None):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Month'], data['Demand (kWh)'], marker='o')
    plt.title(title)
    plt.xlabel('Month')
    plt.ylabel(ylabel)
    plt.grid(True)

    if filename:
        plt.savefig(f'results/{filename}')

    plt.show()


def plot_comparison(base_data, adjusted_data, title, ylabel, filename=None):
    plt.figure(figsize=(10, 6))
    plt.plot(base_data['Month'], base_data['Demand (kWh)'], marker='o', label='Base Forecast')
    plt.plot(adjusted_data['Month'], adjusted_data['Demand (kWh)'], marker='x', label='Adjusted Forecast')
    plt.title(title)
    plt.xlabel('Month')
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    if filename:
        plt.savefig(f'results/{filename}')

    plt.show()


def main():
    electricity_forecast_base = pd.read_csv('results/electricity_forecast_base.csv')
    electricity_forecast_adjusted = pd.read_csv('results/electricity_forecast.csv')
    gas_forecast_base = pd.read_csv('results/gas_forecast_base.csv')
    gas_forecast_adjusted = pd.read_csv('results/gas_forecast.csv')

    plot_forecast(electricity_forecast_adjusted, 'Electricity Demand Forecast (kWh)', 'Demand (kWh)',
                  'electricity_demand_forecast.png')
    plot_forecast(gas_forecast_adjusted, 'Gas Demand Forecast (kWh)', 'Demand (kWh)', 'gas_demand_forecast.png')

    plot_comparison(electricity_forecast_base, electricity_forecast_adjusted, 'Electricity Demand Forecast Comparison (kWh)', 'Demand (kWh)',
                    'electricity_demand_forecast_comparison.png')
    plot_comparison(gas_forecast_base, gas_forecast_adjusted, 'Gas Demand Forecast Comparison (kWh)', 'Demand (kWh)',
                    'gas_demand_forecast_comparison.png')


if __name__ == "__main__":
    main()
