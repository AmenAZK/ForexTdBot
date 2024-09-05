import pandas as pd

def load_and_process_data(csv_file_path):
    """Load and process the intraday data from a CSV file."""
    df = pd.read_csv(csv_file_path)
    df['Date_Time'] = pd.to_datetime(df['timestamp'].astype(str) + ' ' + df['time'], format='%Y%m%d %H:%M:%S')
    df.set_index('Date_Time', inplace=True)
    df.drop(columns=['timestamp', 'time'], inplace=True)
    df.columns = df.columns.str.lower()  # Convert column names to lowercase
    return df



