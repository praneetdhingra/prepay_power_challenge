import pandas as pd
from dataloader import DataLoader, LoadProfile, GasUsage


class Forecast:
    def __init__(self, current_customers, growth_rate, seasonality, monthly_demand, forecast_period, adjustments):
        self.current_customers = current_customers
        self.growth_rate = growth_rate
        self.seasonality = seasonality
        self.monthly_demand = monthly_demand
        self.forecast_period = forecast_period
        self.adjustments = adjustments

    def generate_forecast(self):
        forecast = pd.DataFrame(columns=['Month', 'Customers', 'Demand (kWh)'])
        for month in range(self.forecast_period):
            customers = self.current_customers * (1 + self.growth_rate) ** month
            demand = self.monthly_demand * customers * self.seasonality[month % 12]

            # Apply adjustments
            demand *= self.adjustments['temperature'][month % 12]
            demand *= self.adjustments['price']
            demand *= self.adjustments['demographic']
            demand *= self.adjustments['efficiency']

            forecast = forecast.append({
                'Month': month + 1,
                'Customers': customers,
                'Demand (kWh)': demand.round()
            }, ignore_index=True)
        return forecast


def main():
    data_loader = DataLoader('data/load_profile.csv', 'data/degree_days.csv')
    electricity_profile = LoadProfile(data_loader)
    gas_usage = GasUsage(data_loader)

    # Adjustments based on external factors
    adjustments = {
        'temperature': [1.1 if i < 3 or i > 8 else 0.9 for i in range(12)],  # Colder winters, warmer summers
        'price': 0.9975,  # 3% reduction due to high prices
        'demographic': 0.99875,  # 1.5% reduction due to young generation being energy efficient
        'efficiency': 0.9958  # 5% reduction due to energy efficiency improvements
    }

    electricity_forecast = Forecast(
        current_customers=60000,
        growth_rate=0.03,
        seasonality=electricity_profile.seasonality,
        monthly_demand=electricity_profile.monthly_demand,
        forecast_period=24,
        adjustments=adjustments
    ).generate_forecast()

    gas_forecast = Forecast(
        current_customers=35000,
        growth_rate=0.015,
        seasonality=gas_usage.seasonality,
        monthly_demand=gas_usage.monthly_demand,
        forecast_period=24,
        adjustments=adjustments
    ).generate_forecast()

    electricity_forecast.to_csv('results/electricity_forecast.csv', index=False)
    gas_forecast.to_csv('results/gas_forecast.csv', index=False)

    print("Electricity and gas demand forecasts have been generated with adjustments.")


if __name__ == "__main__":
    main()
