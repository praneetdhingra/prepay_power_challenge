import pandas as pd


class DataLoader:
    def __init__(self, load_profile_path, degree_days_path):
        self.load_profile_path = load_profile_path
        self.degree_days_path = degree_days_path
        self.load_profile = self.load_electricity_data()
        self.degree_days_df = self.load_gas_data()

    def load_electricity_data(self):
        load_profile = pd.read_csv(self.load_profile_path)
        load_profile.drop(columns=load_profile.columns[1:-1], axis=1, inplace=True)
        load_profile.rename(columns=load_profile.iloc[0], inplace=True)
        load_profile.drop(index=[0, len(load_profile)-1], axis=0, inplace=True)
        load_profile.rename(columns={'From-date': 'date', 'Grand Total': 'value'}, inplace=True)
        load_profile['date'] = pd.to_datetime(load_profile['date'])
        load_profile['value'] = pd.to_numeric(load_profile['value'])
        return load_profile

    def calculate_monthly_load_profile(self):
        return self.load_profile.groupby(self.load_profile.date.dt.month)['value'].sum()

    def load_gas_data(self):
        degree_days_df = pd.read_csv(self.degree_days_path)
        degree_days_df = degree_days_df.loc[degree_days_df['Name'] == 'Adjusted Weight Degree-Days (AWDD)']
        degree_days_df.drop(['Name', 'Location', 'Unit'], axis=1, inplace=True)
        degree_days_df.rename(columns={'Date': 'date', 'Value': 'degree_days'}, inplace=True)
        degree_days_df['date'] = pd.to_datetime(degree_days_df['date'])
        degree_days_df['degree_days_sum'] = degree_days_df['degree_days'].cumsum()
        degree_days_df['gas_usage'] = (-1.6 * degree_days_df.index + 3.8 * degree_days_df.degree_days_sum)
        return degree_days_df

    def calculate_monthly_gas_usage(self):
        return self.degree_days_df.groupby(self.degree_days_df.date.dt.month)['gas_usage'].sum()


class LoadProfile:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.monthly_load_profile = self.data_loader.calculate_monthly_load_profile()
        self.monthly_usage_avg = self.monthly_load_profile.mean()
        self.seasonality = self.calculate_seasonality()
        self.monthly_demand = self.monthly_usage_avg / 0.35

    def calculate_seasonality(self):
        return (self.monthly_load_profile / self.monthly_usage_avg).tolist()


class GasUsage:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.monthly_gas_usage = self.data_loader.calculate_monthly_gas_usage()
        self.monthly_demand = self.monthly_gas_usage.mean()
        self.seasonality = self.calculate_seasonality()

    def calculate_seasonality(self):
        return (self.monthly_gas_usage / self.monthly_demand).tolist()
