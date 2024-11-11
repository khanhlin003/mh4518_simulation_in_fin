import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def payoff_func(
        path_rog, 
        path_cfr, 
        path_zurn,
        start_date,
        risk_free,
        denomination=1000,
        # coupon=0.0875, 
        price_rog=257.65, 
        price_cfr=125.60, 
        price_zurn=412.30,
        risk_neutral=True,
        verbose=True
        ):
    
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

    # total_payoff = coupon_payoff + denomination_payoff
    # denomination_payoff = 1000

    coupon = 0.0175

    payment_dates = pd.to_datetime(['2023-12-11', '2024-03-11', '2024-06-11', '2024-09-11', '2024-12-11', '2024-12-11'])
    days_count = [len(pd.bdate_range(start=start_date, end=element)) for element in payment_dates]
    # print(payment_id)

    payment_amount = [1000 * coupon, 1000 * coupon, 1000 * coupon, 1000 * coupon, 1000 * coupon] + [denomination_payoff] 
    # days_count = [element.days for element in (payment_dates - pd.to_datetime(start_date))]
    # print(f'Payoff days: {days_count}')
    indicator_vars = (payment_dates >= pd.to_datetime(start_date))

    if risk_neutral:
        total_payoff = 0
        for amt, cnt, var in zip(payment_amount, days_count, indicator_vars):
            total_payoff += np.exp(-risk_free * cnt / 252) * amt * var
    else:
        total_payoff = 0
        for amt, cnt, var, ir in zip(payment_amount, days_count, indicator_vars, risk_free):
            total_payoff +=  amt / ir * var
    # print(total_payoff)
    return total_payoff

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

def evaluation_plot(
    backtest_start,
    backtest_end,
    combined_df,
    prices,
    ylim
):
    real_price = pd.read_csv('../data/product_price_full.csv')
    real_price['Date'] = pd.to_datetime(real_price['Date'], dayfirst=True)
    real_price = real_price.sort_values(by='Date', ascending=True)
    real_price['Product'] = 1000 * real_price['Product']

    actual = real_price[(real_price['Date'] >= combined_df.iloc[backtest_start]['Date']) & (real_price['Date'] <= combined_df.iloc[backtest_end - 1]['Date'])]['Product'].values
    dates = real_price[(real_price['Date'] >= combined_df.iloc[backtest_start]['Date']) & (real_price['Date'] <= combined_df.iloc[backtest_end - 1]['Date'])]['Date']

    # real_price[(real_price['Date'] >= combined_df.iloc[backtest_start]['Date']) & (real_price['Date'] <= combined_df.iloc[backtest_end - 1]['Date'])]

    plt.figure(figsize=(16, 4))
    for i in range(len(prices)):
        print(mean_squared_error(prices[i], actual))
        plt.plot(dates, prices[i], marker='o', label=f'Predicted Prices {i}')

    plt.plot(dates, actual, marker='o', label='Actual Prices')
    plt.title('Price Comparison Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.ylim(ylim[0], ylim[1])
    # plt.legend()
    # plt.show()

# payoff_func(
#         path_rog=None, 
#         path_cfr=None, 
#         path_zurn=None,
#         start_date='2024-07-25',
#         risk_free=[1, 1, 1, 1, 1, 1.25],
#         denomination=1000,
#         price_rog=257.65, 
#         price_cfr=125.60, 
#         price_zurn=412.30,
#         risk_neutral=False,
#         verbose=True
#         )
