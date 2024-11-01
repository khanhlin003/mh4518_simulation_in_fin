import random
import pandas as pd
def payoff_func(
        path_rog, 
        path_cfr, 
        path_zurn,
        denomination=1000,
        coupon=0.0875, 
        price_rog=257.65, 
        price_cfr=125.60, 
        price_zurn=412.30,
        verbose=True
        ):
    print('Hello')
    # print(f'Path ROG: {path_rog}')
    # print(f'Path CFR: {path_cfr}')
    # print(f'Path ZURN: {path_zurn}')

    coupon_payoff = denomination * coupon

    barrier_rog = price_rog * 0.6
    barrier_cfr = price_cfr * 0.6
    barrier_zurn = price_zurn * 0.6

    performance_rog = path_rog[-1] / price_rog
    performance_cfr = path_cfr[-1] / price_cfr
    performance_zurn = path_zurn[-1] / price_zurn
    worst_performance = min(performance_rog, performance_cfr, performance_zurn)

    if verbose:
        print(f'Worst performance: {worst_performance}')

    barrier = False

    for element in path_rog:
        if element <= barrier_rog:
            barrier = True
            break

    for element in path_cfr:
        if element <= barrier_cfr:
            barrier = True
            break

    for element in path_zurn:
        if element <= barrier_zurn:
            barrier = True
            break
     
    if verbose:
        print(f'Barrier event reached: {barrier}')
    
    above_initial = int((path_rog[-1] >= price_rog)) + \
                    int((path_cfr[-1] >= price_cfr)) + \
                    int((path_zurn[-1] >= price_zurn))
    if verbose:
        print(f'Close above initial: {above_initial}')

    if (barrier==False) or (barrier==True and above_initial==3):
        denomination_payoff = denomination
    elif (barrier==True and above_initial<3):
        denomination_payoff = denomination * worst_performance
    elif path_rog[-1]==0 or path_cfr[-1]==0 or path_zurn[-1]==0:
        denomination_payoff = 0

    total_payoff = coupon_payoff + denomination_payoff
    return total_payoff


def retrieve_data(start_date = '2023-10-25',
                  end_date = '2024-10-25'):
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