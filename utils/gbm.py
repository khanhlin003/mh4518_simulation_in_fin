import numpy as np
import pandas as pd
from tqdm import tqdm
from utils import *
from data_retrieve import *

combined_df = retrieve_data()
n_days = 252
dt = 1 / n_days
close = combined_df[['ROG_Last_Price', 'CFR_Last_Price', 'ZURN_Last_Price']]
tickers = close.columns
log_returns = np.log((close / close.shift(1)).dropna())
df_bond = retrieve_bond()
df_vol = retrieve_vol()
df_vol['Date'] = pd.to_datetime(df_vol['Date'])

def MultivariateGBMSimulation(
    s0, 
    tickers=tickers,
    dt=dt,
    log_returns=log_returns,
    drift=0.01,
    n_paths=100,
    last_id=287,
    current_id=187,
    window_size=30,
    implied_volatility=False
):
    volatility=log_returns.iloc[(current_id - window_size):current_id, :].cov() * n_days 
    corr_matrix = log_returns.iloc[(current_id - window_size):current_id, :].corr()

    if implied_volatility:
        # implied_vol = df_vol[df_vol['Date']==pd.to_datetime(date_str)].drop(columns='Date').values.flatten()
        implied_vol = df_vol.iloc[(current_id - window_size):current_id, 1:]
        implied_vol = implied_vol.mean().values
        diag_matrix = np.diag(implied_vol)
        volatility = diag_matrix @ corr_matrix @ diag_matrix
 
    T = dt * (last_id - current_id)
    n_steps = int(T / dt)
    result = np.zeros((len(tickers), n_paths, n_steps))
    np.random.seed(42)

    for i in tqdm(range(n_paths)):
            choleskyMatrix = np.linalg.cholesky(volatility)
            e = np.random.normal(size=(len(tickers), n_steps)) # Generate RV for steps

            for j in range(n_steps):
                for k in range(len(tickers)):
                    if(j==0):
                        result[k, i, j] = s0[tickers[k]]
                    else:
                        if isinstance(drift, np.ndarray):
                            result[k, i, j] = result[k, i, j-1] * np.exp(
                                (drift[j] -  1/2 * volatility.iloc[k, k]) * dt + 
                                np.sqrt(dt) * choleskyMatrix[k, k] * e[k, j]) 
                        else:
                            result[k, i, j] = result[k, i, j-1] * np.exp(
                                (drift -  1/2 * volatility.iloc[k, k]) * dt + 
                                np.sqrt(dt) * choleskyMatrix[k, k] * e[k, j])
    print('Hello')
    return result, tickers

def MultivariateGBMSimulationAV(
    s0, 
    tickers=tickers,
    dt=dt,
    log_returns=log_returns,
    drift=0.01,
    n_paths=100,
    last_id=287,
    current_id=187,
    window_size=30,
    implied_volatility=False
):
    volatility=log_returns.iloc[(current_id - window_size):current_id, :].cov() * n_days 
    corr_matrix = log_returns.iloc[(current_id - window_size):current_id, :].corr()

    if implied_volatility:
        # implied_vol = df_vol[df_vol['Date']==pd.to_datetime(date_str)].drop(columns='Date').values.flatten()
        implied_vol = df_vol.iloc[(current_id - window_size):current_id, 1:]
        implied_vol = implied_vol.mean().values
        diag_matrix = np.diag(implied_vol)
        volatility = diag_matrix @ corr_matrix @ diag_matrix

    T = dt * (last_id - current_id)
    n_steps = int(T / dt)
    result = np.zeros((len(tickers), n_paths, n_steps))
    np.random.seed(42)

    for i in tqdm(range(n_paths // 2)):
        choleskyMatrix = np.linalg.cholesky(volatility)
        e = np.random.normal(size=(len(tickers), n_steps)) # Generate RV for steps
        e_tilde = -e    

        for j in range(n_steps):
            for k in range(len(tickers)):
                if(j==0):
                    result[k, i, j] = s0[tickers[k]]
                    result[k, n_paths - i - 1, j] = s0[tickers[k]]

                else:
                    if isinstance(drift, np.ndarray):
                        result[k, i, j] = result[k, i, j-1] * np.exp(
                            (drift[j] -  1/2 * volatility.iloc[k, k]) * dt + 
                            np.sqrt(dt) * choleskyMatrix[k, k] * e[k, j])
                        result[k, n_paths - i - 1, j] = result[k, n_paths - i - 1, j-1] * np.exp(
                            (drift[j] -  1/2 * volatility.iloc[k, k]) * dt + 
                            np.sqrt(dt) * choleskyMatrix[k, k] * e_tilde[k, j])
                    else:
                        result[k, i, j] = result[k, i, j-1] * np.exp(
                            (drift -  1/2 * volatility.iloc[k, k]) * dt + 
                            np.sqrt(dt) * choleskyMatrix[k, k] * e[k, j])
                        result[k, n_paths - i - 1, j] = result[k, n_paths - i - 1, j-1] * np.exp(
                            (drift -  1/2 * volatility.iloc[k, k]) * dt + 
                            np.sqrt(dt) * choleskyMatrix[k, k] * e_tilde[k, j])
    return result, tickers

def MultivariateGBMSimulationEMS(
    s0, 
    tickers=tickers,
    dt=dt,
    log_returns=log_returns,
    drift=0.01,
    n_paths=100,
    last_id=287,
    current_id=187,
    window_size=30,
    implied_volatility=False
):
    volatility=log_returns.iloc[(current_id - window_size):current_id, :].cov() * n_days 
    corr_matrix = log_returns.iloc[(current_id - window_size):current_id, :].corr()

    if implied_volatility:
        # implied_vol = df_vol[df_vol['Date']==pd.to_datetime(date_str)].drop(columns='Date').values.flatten()
        implied_vol = df_vol.iloc[(current_id - window_size):current_id, 1:]
        implied_vol = implied_vol.mean().values
        diag_matrix = np.diag(implied_vol)
        volatility = diag_matrix @ corr_matrix @ diag_matrix

    T = dt * (last_id - current_id)
    n_steps = int(T / dt)
    result = np.zeros((len(tickers), n_paths, n_steps))
    np.random.seed(42)

    for i in tqdm(range(n_paths)):
        choleskyMatrix = np.linalg.cholesky(volatility)
        e = np.random.normal(size=(len(tickers), n_steps)) # Generate RV for steps

        for j in range(n_steps):
            for k in range(len(tickers)):
                if(j==0):
                    result[k, i, j] = s0[tickers[k]]
                else:
                    if isinstance(drift, np.ndarray):
                        result[k, i, j] = result[k, i, j-1] * np.exp(
                            (drift[j] -  1/2 * volatility.iloc[k, k]) * dt + 
                            np.sqrt(dt) * choleskyMatrix[k, k] * e[k, j])
                    else:
                        result[k, i, j] = result[k, i, j-1] * np.exp(
                            (drift -  1/2 * volatility.iloc[k, k]) * dt + 
                            np.sqrt(dt) * choleskyMatrix[k, k] * e[k, j])
    for k in range(len(tickers)):  
            # path, step
        correction_factor = result[k][-1, :].mean() / result[k][-1, :] 
        result[k] = result[k] * correction_factor 
    
    return result, tickers

def MultivariateGBMSimulationTS(
    s0, 
    tickers=tickers,
    dt=dt,
    log_returns=log_returns,
    drift=0.01,
    n_paths=100,
    last_id=287,
    current_id=187,
    window_size=30,
    implied_volatility=False
    ):

    volatility=log_returns.iloc[(current_id - window_size):current_id, :].cov() * n_days 
    corr_matrix = log_returns.iloc[(current_id - window_size):current_id, :].corr()

    T = dt * (last_id - current_id)
    # print(f'GBM days: {last_id - current_id}')

    n_steps = int(T / dt)
    result = np.zeros((len(tickers), n_paths, n_steps))
    np.random.seed(42)

    date_str = combined_df['Date'].iloc[current_id]
    payment_dates = pd.to_datetime(['2023-12-11', '2024-03-11', '2024-06-11', '2024-09-11', '2024-12-11', '2024-12-11'])    
    days_count = [len(pd.bdate_range(start=pd.to_datetime(date_str), end=element)) for element in payment_dates]

    spline = interpolate_rate(df_bond, date_str)
    discounts = [spline(element/252) for element in days_count]

    # print(date_str)
    if implied_volatility:
        # implied_vol = df_vol[df_vol['Date']==pd.to_datetime(date_str)].drop(columns='Date').values.flatten()
        implied_vol = df_vol.iloc[(current_id - window_size):current_id, 1:]
        implied_vol = implied_vol.mean().values
        diag_matrix = np.diag(implied_vol)
        volatility = diag_matrix @ corr_matrix @ diag_matrix 

    for i in tqdm(range(n_paths)):
        choleskyMatrix = np.linalg.cholesky(volatility)
        e = np.random.normal(size=(len(tickers), n_steps)) # Generate RV for steps

        drift_list = []
        for j in range(n_steps):
            # print(spline(0))
            drift = spline(j/252) / spline((j+1)/252) 
            drift_list.append(drift)

            for k in range(len(tickers)):
                if(j==0):
                    result[k, i, j] = s0[tickers[k]]
                else:
                    if isinstance(drift, np.ndarray):
                        result[k, i, j] = result[k, i, j-1] * drift[j] * np.exp(
                            (- 1/2 * volatility.iloc[k, k]) * dt + 
                            np.sqrt(dt) * choleskyMatrix[k, k] * e[k, j]) 
                    else:
                        result[k, i, j] = result[k, i, j-1] * drift * np.exp(
                            (- 1/2 * volatility.iloc[k, k]) * dt + 
                            np.sqrt(dt) * choleskyMatrix[k, k] * e[k, j])
    print(spline(T))
    return result, tickers, discounts

# MultivariateGBMSimulationTS(s0=close.iloc[187], n_paths=100, current_id=187, window_size=30)