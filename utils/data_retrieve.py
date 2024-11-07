import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


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
    df_dict['df_1w'] = pd.read_csv('../data/bond/Switzerland 1-Week Bond Yield Historical Data.csv')[['Date', 'Price']]
    df_dict['df_1m'] = pd.read_csv('../data/bond/Switzerland 1-Month Bond Yield Historical Data.csv')[['Date', 'Price']]
    df_dict['df_2m'] = pd.read_csv('../data/bond/Switzerland 2-Month Bond Yield Historical Data.csv')[['Date', 'Price']]
    df_dict['df_3m'] = pd.read_csv('../data/bond/Switzerland 3-Month Bond Yield Historical Data.csv')[['Date', 'Price']]
    df_dict['df_6m'] = pd.read_csv('../data/bond/Switzerland 6-Month Bond Yield Historical Data.csv')[['Date', 'Price']]
    df_dict['df_1y'] = pd.read_csv('../data/bond/Switzerland 1-Year Bond Yield Historical Data-3.csv')[['Date', 'Price']]
    df_dict['df_2y'] = pd.read_csv('../data/bond/Switzerland 2-Year Bond Yield Historical Data.csv')[['Date', 'Price']]

    for key in df_dict:
        df_dict[key]['Price'] = df_dict[key]['Price'].astype(float)
        df_dict[key]['Date'] = pd.to_datetime(df_dict[key]['Date'])
        df_dict[key].columns = ['Date', key]

    df = df_dict['df_1w']
    for key in list(df_dict.keys())[1:]:
        df = pd.merge(df, df_dict[key], on='Date')

    return df

def interpolate_rate(df, date):
    df_filter = df[df['Date']==date].drop(columns='Date')
    x = [1/52, 1/12, 2/12, 3/12, 6/12, 1, 2]
    y = df_filter.values.flatten()

    spline = CubicSpline(x, y)

    return spline

# df = retrieve_bond()
# spline = interpolate_rate(df, '2024-01-11')
# print(term_structure(spline, 10))
