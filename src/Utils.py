import pandas as pd
import pytz

# Define New York Time Zone
ny_tz = pytz.timezone('America/New_York')

def get_asian_range(df):
    """Retrieve the Asian session high and low based on daily data."""
    if df.index.tzinfo is None:
        df.index = df.index.tz_localize('UTC').tz_convert(ny_tz)
    asian_high = df['high'].max()
    asian_low = df['low'].min()
    return asian_high, asian_low

def get_london_session(df):
    """Retrieve London session data. Here, it just returns the DataFrame."""
    return df






