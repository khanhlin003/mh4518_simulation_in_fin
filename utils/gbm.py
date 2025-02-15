import numpy as np
import pandas as pd
from tqdm.auto import tqdm
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
    drift=0.01107,
    n_paths=100,
    last_id=287,
    current_id=187,
    window_size=30,
    implied_volatility=False,
    h=0
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
    if h!=0:
        result = np.zeros((3, len(tickers), n_paths, n_steps))
    np.random.seed(42)
    choleskyMatrix = np.linalg.cholesky(volatility)

    e = np.random.normal(size=(len(tickers), n_paths, n_steps)) # Generate RV for steps

    for j in tqdm(range(n_steps)):
        for k in range(len(tickers)):
            if(j==0):
                if h==0:
                    result[k, :, j] = s0[tickers[k]]
                else:
                    result[0, k, :, j] = s0[tickers[k]]
                    result[1, k, :, j] = s0[tickers[k]] * (1 + h)
                    result[2, k, :, j] = s0[tickers[k]] * (1 - h)
            else:
                if isinstance(drift, np.ndarray):
                    d = drift[j]
                else:
                    d = drift
                if h==0:
                    result[k, :, j] = result[k, :, j-1] * np.exp(
                        (d -  1/2 * volatility.iloc[k, k]) * dt + 
                        np.sqrt(dt) * choleskyMatrix[k, k] * e[k, :, j]) 
                else:
                    result[:, k, :, j] = result[:, k, :, j-1] * np.exp(
                        (d -  1/2 * volatility.iloc[k, k]) * dt + 
                        np.sqrt(dt) * choleskyMatrix[k, k] * e[k, :, j]) 
    
    discount = drift

    return result, tickers, discount

def MultivariateGBMSimulationAV(
    s0, 
    tickers=tickers,
    dt=dt,
    log_returns=log_returns,
    drift=0.01107,
    n_paths=100,
    last_id=287,
    current_id=187,
    window_size=30,
    implied_volatility=False,
    h=0
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
    if h!=0:
        result = np.zeros((3, len(tickers), n_paths, n_steps))
    np.random.seed(42)
    choleskyMatrix = np.linalg.cholesky(volatility)
    e = np.random.normal(size=(len(tickers), n_paths//2, n_steps)) # Generate RV for steps
    e_tilde = -e
    for j in tqdm(range(n_steps)):
        for k in range(len(tickers)):
            if(j==0):
                if h==0:
                    result[k, :n_paths//2, j] = s0[tickers[k]]
                    result[k, n_paths//2:, j] = s0[tickers[k]]
                else:
                    result[0, k, :, j] = s0[tickers[k]]
                    result[1, k, :, j] = s0[tickers[k]] * (1 + h)
                    result[2, k, :, j] = s0[tickers[k]] * (1 - h)

            else:
                if isinstance(drift, np.ndarray):
                    d = drift[j]
                else:
                    d = drift

                if h==0:
                    result[k, :n_paths//2, j] = result[k, :n_paths//2, j-1] * np.exp(
                        (d -  1/2 * volatility.iloc[k, k]) * dt + 
                        np.sqrt(dt) * choleskyMatrix[k, k] * e[k, :, j]) 
                    result[k, n_paths//2:, j] = result[k, n_paths//2:, j-1] * np.exp(
                        (d -  1/2 * volatility.iloc[k, k]) * dt + 
                        np.sqrt(dt) * choleskyMatrix[k, k] * e_tilde[k, :, j]) 
                else:
                    result[:, k, :n_paths//2, j] = result[:, k, :n_paths//2, j-1] * np.exp(
                        (d -  1/2 * volatility.iloc[k, k]) * dt + 
                        np.sqrt(dt) * choleskyMatrix[k, k] * e[k, :, j]) 
                    result[:, k, n_paths//2:, j] = result[:, k, n_paths//2:, j-1] * np.exp(
                        (d -  1/2 * volatility.iloc[k, k]) * dt + 
                        np.sqrt(dt) * choleskyMatrix[k, k] * e_tilde[k, :, j]) 
    
    discount = drift

    return result, tickers, discount

def MultivariateGBMSimulationEMS(
    s0, 
    tickers=tickers,
    dt=dt,
    log_returns=log_returns,
    drift=0.01107,
    n_paths=100,
    last_id=287,
    current_id=187,
    window_size=30,
    implied_volatility=False,
    h=0
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
    if h!=0:
        result = np.zeros((3, len(tickers), n_paths, n_steps))
    np.random.seed(42)
    choleskyMatrix = np.linalg.cholesky(volatility)
    e = np.random.normal(size=(len(tickers), n_paths, n_steps)) # Generate RV for steps

    for j in tqdm(range(n_steps)):
        for k in range(len(tickers)):
            if(j==0):
                if h==0:
                    result[k, :, j] = s0[tickers[k]]
                else:
                    result[0, k, :, j] = s0[tickers[k]]
                    result[1, k, :, j] = s0[tickers[k]] * (1 + h)
                    result[2, k, :, j] = s0[tickers[k]] * (1 - h)
            else:
                if isinstance(drift, np.ndarray):
                    d = drift[j]
                else:
                    d = drift
                if h==0:
                    result[k, :, j] = result[k, :, j-1] * np.exp(
                        (d -  1/2 * volatility.iloc[k, k]) * dt + 
                        np.sqrt(dt) * choleskyMatrix[k, k] * e[k, :, j]) 
                else:
                    result[:, k, :, j] = result[:, k, :, j-1] * np.exp(
                        (d -  1/2 * volatility.iloc[k, k]) * dt + 
                        np.sqrt(dt) * choleskyMatrix[k, k] * e[k, :, j]) 
    for k in range(len(tickers)):  
            # path, step
        correction_factor = result[:, k, -1, :].mean() / result[:, k, -1, :]
        result[:, k, :, :] = result[:, k, :, :] * correction_factor 

    discount = drift
    
    return result, tickers, discount

def MultivariateGBMSimulationTS(
    s0, 
    tickers=tickers,
    dt=dt,
    log_returns=log_returns,
    drift=0.01107,
    n_paths=100,
    last_id=287,
    current_id=187,
    window_size=30,
    implied_volatility=False,
    h=0
    ):

    volatility=log_returns.iloc[(current_id - window_size):current_id, :].cov() * n_days 
    corr_matrix = log_returns.iloc[(current_id - window_size):current_id, :].corr()

    T = dt * (last_id - current_id)
    # print(f'GBM days: {last_id - current_id}')

    n_steps = int(T / dt)
    result = np.zeros((len(tickers), n_paths, n_steps))
    if h!=0:
        result = np.zeros((3, len(tickers), n_paths, n_steps))
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

    choleskyMatrix = np.linalg.cholesky(volatility)

    drift_list = []
    for j in range(n_steps):
        # print(spline(0))
        drift = spline(j/252) / spline((j+1)/252) 
        drift_list.append(drift)
    
    e = np.random.normal(size=(len(tickers), n_paths, n_steps)) # Generate RV for steps

    for j in tqdm(range(n_steps)):
        for k in range(len(tickers)):
            if(j==0):
                if h==0:
                    result[k, :, j] = s0[tickers[k]]
                else:
                    result[0, k, :, j] = s0[tickers[k]]
                    result[1, k, :, j] = s0[tickers[k]] * (1 + h)
                    result[2, k, :, j] = s0[tickers[k]] * (1 - h)
            else:
                d = drift_list[j]
                if h==0:
                    result[k, :, j] = result[k, :, j-1] * d * np.exp(
                        (- 1/2 * volatility.iloc[k, k]) * dt + 
                        np.sqrt(dt) * choleskyMatrix[k, k] * e[k, :, j]) 
                else:
                    result[:, k, :, j] = result[:, k, :, j-1] * d * np.exp(
                        (-  1/2 * volatility.iloc[k, k]) * dt + 
                        np.sqrt(dt) * choleskyMatrix[k, k] * e[k, :, j])  
    return result, tickers, discounts

# MultivariateGBMSimulationTS(s0=close.iloc[187], n_paths=100, current_id=187, window_size=30)