import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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