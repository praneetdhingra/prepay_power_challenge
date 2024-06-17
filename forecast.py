import pandas as pd
from dataloader import DataLoader, LoadProfile, GasUsage


class Forecast:
    def __init__(self, current_customers, growth_rate, seasonality, monthly_demand, forecast_period):
        self.current_customers = current_customers
        self.growth_rate = growth_rate
        self.seasonality = seasonality
        self.monthly_demand = monthly_demand
        self.forecast_period = forecast_period

    def generate_forecast(self):
        forecast = pd.DataFrame(columns=['Month', 'Customers', 'Demand (kWh)'])
        for month in range(self.forecast_period):
            customers = self.current_customers * (1 + self.growth_rate) ** month
            demand = self.monthly_demand * customers * self.seasonality[month % 12]
            forecast = forecast.append({
                'Month': month + 1,
                'Customers': round(customers),
                'Demand (kWh)': demand.round()
            }, ignore_index=True)
        return forecast


def main():
    data_loader = DataLoader('data/load_profile.csv', 'data/degree_days.csv')
    electricity_profile = LoadProfile(data_loader)
    gas_usage = GasUsage(data_loader)

    electricity_forecast = Forecast(
        current_customers=60000,
        growth_rate=0.03,
        seasonality=electricity_profile.seasonality,
        monthly_demand=electricity_profile.monthly_demand,
        forecast_period=24
    ).generate_forecast()

    gas_forecast = Forecast(
        current_customers=35000,
        growth_rate=0.015,
        seasonality=gas_usage.seasonality,
        monthly_demand=gas_usage.monthly_demand,
        forecast_period=24
    ).generate_forecast()

    electricity_forecast.to_csv('results/electricity_forecast_base.csv', index=False)
    gas_forecast.to_csv('results/gas_forecast_base.csv', index=False)

    print("Electricity and gas demand forecasts have been generated.")


if __name__ == "__main__":
    main()
