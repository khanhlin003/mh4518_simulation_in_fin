import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def is_trading_day(date):
    if date.weekday() in [5, 6]:  # 5 is Saturday, 6 is Sunday
        return False
    if date.strftime("%d%m%Y") == "01082024":
        return False
    return True

def get_trading_days(start_date, end_date):
    trading_days = []
    current_date = start_date
    while current_date <= end_date:
        if is_trading_day(current_date):
            trading_days.append(current_date.strftime("%d%m%Y"))
        current_date += timedelta(days=1)
    return trading_days

def create_folder_structure(base_path, trading_days):
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    for date_str in trading_days:
        date_folder = os.path.join(base_path, date_str)
        if not os.path.exists(date_folder):
            os.makedirs(date_folder)

def load_option_data(excel_path, sheet_name):
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"Error loading file '{excel_path}', sheet '{sheet_name}': {str(e)}")
        return None

def process_all_option_data(input_dir, output_dir):
    start_date = datetime(2024, 7, 25)
    end_date = datetime(2024, 10, 25)
    trading_days = get_trading_days(start_date, end_date)
    create_folder_structure(output_dir, trading_days)
    files = ['zurn_call.xlsx', 'rog_call.xlsx', 'cfr_call.xlsx']
    
    for date_str in trading_days:
        date_folder = os.path.join(output_dir, date_str)
        for file in files:
            excel_path = os.path.join(input_dir, file)
            df = load_option_data(excel_path, date_str)
            if df is not None:
                output_file = os.path.join(date_folder, file.replace('.xlsx', '.csv'))
                df.to_csv(output_file, index=False)
            else:
                print(f"Skipping '{file}' for date '{date_str}' due to loading error")

def clean_options_df(options_data: pd.DataFrame, curr_date: pd.Timestamp):
    try:
        options_data.dropna(subset=['ExDt'], inplace=True)
        options_data['ExDt'] = pd.to_datetime(options_data['ExDt'], format='%m/%d/%y')
        options_data['maturity'] = (options_data['ExDt'] - curr_date).dt.days / 365.25
        options_data = options_data[(options_data['Mid'] > 0) & (options_data['IVM'] > 0)].reset_index(drop=True)
        options_data = options_data[['maturity', 'Strike', 'Mid', 'IVM']]
        options_data.columns = ['maturity', 'strike', 'price', 'IV']
        options_data = options_data[options_data['maturity'] > 0.1]
        return options_data
    except Exception as e:
        print(f"Error cleaning data: {e}")
        return pd.DataFrame()

def process_and_save_cleaned_data(processed_folder, cleaned_folder):
    for date_folder in os.listdir(processed_folder):
        date_path = os.path.join(processed_folder, date_folder)
        if not os.path.isdir(date_path):
            continue
        cleaned_date_path = os.path.join(cleaned_folder, date_folder)
        os.makedirs(cleaned_date_path, exist_ok=True)
        curr_date = pd.to_datetime(date_folder, format='%d%m%Y')
        
        for csv_file in os.listdir(date_path):
            csv_path = os.path.join(date_path, csv_file)
            try:
                options_data = pd.read_csv(csv_path)
                cleaned_data = clean_options_df(options_data, curr_date)
                if not cleaned_data.empty:
                    cleaned_csv_path = os.path.join(cleaned_date_path, csv_file)
                    cleaned_data.to_csv(cleaned_csv_path, index=False)
                else:
                    print(f"No valid data in '{csv_file}' for date '{date_folder}'. Skipping save.")
            except Exception as e:
                print(f"Error processing file '{csv_path}' for date '{date_folder}': {e}")
