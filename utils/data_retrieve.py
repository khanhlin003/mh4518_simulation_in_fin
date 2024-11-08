import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, UnivariateSpline


def retrieve_data(
    start_date = '2023-10-25',
    end_date = '2024-10-25'
    ):
    # List of tickers
    tickers = ['rog', 'cfr', 'zurn']

    # Function to read and filter CSV files
    def read_and_filter_csv(file_path, date_col='Date', price_col='Last Price'):
        df = pd.read_csv(file_path)
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        return df[(df[date_col] >= start_date) & (df[date_col] <= end_date)]

    # Initialize the combined DataFrame
    combined_df = pd.DataFrame()

    # Process tickers for prices and implied volatility
    for t in tickers:
        # Read and filter price data
        price_df = read_and_filter_csv(f'../data/{t}.csv')
        price_df = price_df[['Date', 'Last Price']].rename(columns={'Last Price': f'{t.upper()}_Last_Price'})
        
        # Read and filter implied volatility data
        ivol_df = read_and_filter_csv(f'../data/{t}_ivol.csv', price_col='IVOL')
        ivol_column_name = ivol_df.columns[1]
        ivol_df = ivol_df[['Date', ivol_column_name]].rename(columns={ivol_column_name: f'{t.upper()}_IVOL'})

        # Merge the dataframes
        combined_df = pd.merge(combined_df, price_df, on='Date', how='outer') if not combined_df.empty else price_df
        combined_df = pd.merge(combined_df, ivol_df, on='Date', how='outer')

    # Read and filter risk-free rate data
    risk_free_df = read_and_filter_csv('../data/risk_free.csv')
    risk_free_column_name = risk_free_df.columns[1]
    risk_free_df = risk_free_df[['Date', risk_free_column_name]].rename(columns={risk_free_column_name: 'Risk_Free_Rate'})

    # Merge risk-free rate data
    combined_df = pd.merge(combined_df, risk_free_df, on='Date', how='outer')

    # Sort and reset index
    combined_df = combined_df.sort_values('Date').reset_index(drop=True)

    # Show the combined DataFrame
    return combined_df


def retrieve_bond():

    df_dict = dict()
    # sample_df = pd.DataFrame({
    #     'Date': pd.read_csv('../data/bond/bond_1Y.csv')['Date']
    # })
    # df_3m, df_6m = sample_df.copy(), sample_df.copy()
    # df_3m['Last Price'] = 100.4
    # df_6m['Last Price'] = 100.5

    # df_dict['df_3m'] = df_3m
    # df_dict['df_6m'] = df_6m
    df_dict['df_1y'] = pd.read_csv('../data/bond/bond_1Y.csv')[['Date', 'Last Price']]
    df_dict['df_2y'] = pd.read_csv('../data/bond/bond_2Y.csv')[['Date', 'Last Price']]
    df_dict['df_3y'] = pd.read_csv('../data/bond/bond_3Y.csv')[['Date', 'Last Price']]
    df_dict['df_4y'] = pd.read_csv('../data/bond/bond_4Y.csv')[['Date', 'Last Price']]
    df_dict['df_5y'] = pd.read_csv('../data/bond/bond_5Y.csv')[['Date', 'Last Price']]
    df_dict['df_6y'] = pd.read_csv('../data/bond/bond_6Y.csv')[['Date', 'Last Price']]
    df_dict['df_8y'] = pd.read_csv('../data/bond/bond_8Y.csv')[['Date', 'Last Price']]
    df_dict['df_10y'] = pd.read_csv('../data/bond/bond_10Y.csv')[['Date', 'Last Price']]

    for key in df_dict:
        df_dict[key]['Last Price'] = df_dict[key]['Last Price'].astype(float) / 100
        df_dict[key]['Date'] = pd.to_datetime(df_dict[key]['Date'])
        df_dict[key].columns = ['Date', key]

    df = df_dict['df_1y']
    for key in list(df_dict.keys())[1:]:
        df = pd.merge(df, df_dict[key], on='Date')

    return df

def retrieve_vol():
    df_dict = dict()
    for tickers in ['rog', 'cfr', 'zurn']:

        df_dict[tickers] = pd.read_csv(f'../data/{tickers}_ivol.csv')
        df_dict[tickers].columns = ['Date', tickers]
        df_dict[tickers][tickers] = df_dict[tickers][tickers].bfill()
        df_dict[tickers][tickers] = df_dict[tickers][tickers] / 100

    df = pd.DataFrame({
        'Date': df_dict[tickers]['Date']
    })
    for tickers in df_dict:
        df = pd.merge(df, df_dict[tickers], on='Date')
        df.sort_values(by='Date', inplace=True)
    
    return df

def interpolate_rate(df, date):
    df_filter = df[df['Date']==date].drop(columns='Date')
    # x = [1/4, 1/2, 1, 2, 3, 4, 5, 6, 8, 10]
    x = [1, 2, 3, 4, 5, 6, 8, 10]
    y = df_filter.values.flatten()

    spline = CubicSpline(x, y)
    # spline = UnivariateSpline(x, y, s=1.0)

    return spline

# df = retrieve_bond()
# spline = interpolate_rate(df, '2024-01-11')
# print(term_structure(spline, 10))
