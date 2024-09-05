import pandas as pd
import numpy as np

def calculate_sma(data, window):
    """Calculate Simple Moving Average"""
    return data['close'].rolling(window=window).mean()

def generate_signals(data, fast_window=10, slow_window=30):
    """Generate buy and sell signals based on SMA crossover"""
    data['fast_sma'] = calculate_sma(data, fast_window)
    data['slow_sma'] = calculate_sma(data, slow_window)
    
    data['signal'] = np.where(data['fast_sma'] > data['slow_sma'], 1, 0)
    data['position'] = data['signal'].diff()
    
    return data

def trading_strategy(df):
    """Main strategy logic using Simple Moving Average crossover"""
    results = []
    
    # Generate signals
    df = generate_signals(df)
    
    # Iterate through the data
    for i in range(1, len(df)):
        if df['position'].iloc[i] == 1:  # Buy signal
            entry_price = df['close'].iloc[i]
            stop_loss = entry_price * 0.99  # 1% stop loss
            take_profit = entry_price * 1.02  # 2% take profit
            results.append(('Buy', df.index[i], (entry_price, stop_loss, take_profit)))
            print(f"Buy Signal: Date: {df.index[i]}, Entry: {entry_price}, Stop Loss: {stop_loss}, Take Profit: {take_profit}")
        
        elif df['position'].iloc[i] == -1:  # Sell signal
            entry_price = df['close'].iloc[i]
            stop_loss = entry_price * 1.01  # 1% stop loss
            take_profit = entry_price * 0.98  # 2% take profit
            results.append(('Sell', df.index[i], (entry_price, stop_loss, take_profit)))
            print(f"Sell Signal: Date: {df.index[i]}, Entry: {entry_price}, Stop Loss: {stop_loss}, Take Profit: {take_profit}")
    
    if not results:
        print("No trades found.")
    
    return results

# You can remove these functions as they're not used in the new strategy
# def is_asian_range_high_taken(current_price, asian_high):
# def is_asian_range_low_taken(current_price, asian_low):
# def find_higher_low_break(df):
# def find_lower_high_break(df):
# def place_sell_order(df, break_index):
# def place_buy_order(df, break_index):