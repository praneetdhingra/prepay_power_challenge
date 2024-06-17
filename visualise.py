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


def main():
    electricity_forecast = pd.read_csv('results/electricity_forecast.csv')
    gas_forecast = pd.read_csv('results/gas_forecast.csv')

    plot_forecast(electricity_forecast, 'Electricity Demand Forecast (kWh)', 'Demand (kWh)',
                  'electricity_demand_forecast.png')
    plot_forecast(gas_forecast, 'Gas Demand Forecast (kWh)', 'Demand (kWh)', 'gas_demand_forecast.png')


if __name__ == "__main__":
    main()
