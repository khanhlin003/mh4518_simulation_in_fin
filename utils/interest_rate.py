from __future__ import annotations
import typing
from datetime import date, timedelta, datetime
import numpy as np
import pandas as pd
import os 

def get_period(key: str):
    """
    Helper function to convert period strings to fractions of a year.
    """
    map = {
        '1-Week': 1/52,
        '1-Month': 1/12,
        '2-Month': 2/12,
        '3-Month': 3/12,
        '6-Month': 1/2,
        '1-Year': 1,
        '2-Year': 2,
    }
    return map[key]

def read_bond_data(data_dir):
    """
    Read bond yield data from the provided directory and return a consolidated DataFrame.
    """
    bond_data = pd.DataFrame()
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(data_dir, filename))
            period = filename.split(' ')[1]
            df['period'] = get_period(period)
            bond_data = pd.concat([bond_data, df], ignore_index=True)
    return bond_data

class VasicekModel(object):
    def __init__(self, data: pd.DataFrame, params: typing.Dict):
        """
        b: long term mean level: All future trajectories of r will evolve around a mean level b in the long run.
        a: speed of reversion: A characterizes the velocity at which such trajectories will regroup around b.
        sigma: instantaneous volatility: measures instant by instant the amplitude of randomness
        """
        self.data = data
        self.a = params.get('speed of reversion')   
        self.b = params.get('long term mean level')
        self.sigma = params.get('sigma')
        self.maturity_date = params.get('maturity_date')
        self.dt = 1/252
    
    def generate_path(self, current_date: str)->pd.DataFrame:
        """
            N: the number steps in the path
        """
        N = (pd.to_datetime(self.maturity_date) - pd.to_datetime(current_date)).days + 1
        Rt = [0]*(N+1)
        prev_date = pd.to_datetime(current_date) - pd.DateOffset(days=1)
        Rt[0] = self.data.loc[prev_date]['Price']
        for i in range(1, N+1):
            Rt[i] = self.a*(self.b-Rt[i-1]) * self.dt + self.sigma * np.random.normal(0, np.sqrt(self.dt)) + Rt[i-1]
        Rt = Rt[1:]
        return pd.DataFrame(data=Rt, index=pd.date_range(current_date, self.maturity_date), columns=['Rate'])