import pandas as pd
from collections import defaultdict
from load_data import load_and_process_data
from strategy import trading_strategy
from Riskmanagement import RiskManagement
from Utils import get_asian_range, get_london_session
from datetime import timedelta

def simulate_trade(entry_price, stop_loss, take_profit, position_size):
    """Simulate a trade to calculate the result based on entry, SL, TP, and position size."""
    return (take_profit - entry_price) * position_size

def main():
    # Define the path to your CSV file
    csv_file_path = 'data/intraday_data.csv'
    
    # Load and process the data
    df = load_and_process_data(csv_file_path)

    # Filter data for the trading hours 2 AM to 5 AM
    df = df.between_time('02:00', '05:00')

    # Print Data Time Range and Timezone for Debugging
    print("Data Time Range:", df.index.min(), "to", df.index.max())
    print("DataFrame Index Timezone:", df.index.tzinfo)

    # Initialize risk management
    initial_capital = 10000
    risk_management = RiskManagement(initial_capital, max_daily_loss=0.025, max_risk_per_trade=0.025, break_even_capital=0.01)

    # Apply the trading strategy
    trades = trading_strategy(df)

    # Initialize counters
    total_trades = 0
    winning_trades = 0
    total_duration = timedelta(0)
    trades_per_day = defaultdict(int)
    daily_profit_loss = defaultdict(float)

    if trades:
        current_date = None
        open_trade = None
        for i, trade in enumerate(trades):
            if len(trade) == 3:
                trade_type, trade_date, trade_details = trade
                
                # Close previous trade if exists
                if open_trade:
                    entry_date, entry_price, stop_loss, take_profit = open_trade
                    trade_duration = trade_date - entry_date
                    total_duration += trade_duration

                    # Calculate trade result and store exit date
                    trade_result = simulate_trade(entry_price, stop_loss, take_profit, position_size)
                    daily_profit_loss[current_date] += trade_result

                    # Update risk management based on trade result
                    risk_management.update_after_trade(trade_result, trade_date)

                    # Update winning trades counter
                    if trade_result > 0:
                        winning_trades += 1

                    # Print trade details including exit date
                    print(f"Trade Type: {trade_type}")
                    print(f"Entry Date: {entry_date}")
                    print(f"Exit Date: {trade_date}")
                    print(f"Entry Price: {entry_price}")
                    print(f"Stop Loss: {stop_loss}")
                    print(f"Take Profit: {take_profit}")
                    print(f"Trade Result: {'Win' if trade_result > 0 else 'Loss'}")
                    print(f"Trade Duration: {trade_duration}")
                    print("---")

                    open_trade = None

                # Check if it's a new day
                if current_date != trade_date.date():
                    risk_management.reset_daily_values()
                    current_date = trade_date.date()
                    trades_per_day[current_date] = 0
                    daily_profit_loss[current_date] = 0

                # Check daily trade limit
                if trades_per_day[current_date] >= 1:
                    print("Maximum of 1 trade per day reached. No further trades today.")
                    continue

                # Check if daily loss limit is reached
                if daily_profit_loss[current_date] <= -risk_management.max_daily_loss * risk_management.get_capital():
                    print("Daily loss limit reached. No further trades today.")
                    continue

                entry_price, stop_loss, take_profit = trade_details
                stop_loss_distance = abs(entry_price - stop_loss)
                
                # Calculate position size
                position_size = risk_management.calculate_trade_risk(stop_loss_distance, trade_date)
                if position_size is None:
                    print("No trade taken due to risk management constraints.")
                    continue

                # Open new trade
                open_trade = (trade_date, entry_price, stop_loss, take_profit)
                trades_per_day[current_date] += 1
                total_trades += 1

                print(f"Opening Trade: {trade_type} at {entry_price}")
            else:
                print(f"Unexpected trade format: {trade}")

        # Close last trade if still open
        if open_trade:
            entry_date, entry_price, stop_loss, take_profit = open_trade
            trade_duration = df.index[-1] - entry_date
            total_duration += trade_duration

            # Calculate trade result and store exit date
            trade_result = simulate_trade(entry_price, stop_loss, take_profit, position_size)
            daily_profit_loss[current_date] += trade_result
            print(f"Last Trade Duration: {trade_duration}")

        # Final summary
        print("\nTrades per Day:")
        for day, count in sorted(trades_per_day.items()):
            print(f"{day}: {count} trade(s)")

        if total_trades > 0:
            total_profit_loss = risk_management.get_capital() - initial_capital
            average_duration = total_duration / total_trades

            print("\nFinal Summary:")
            print(f"Total Trades: {total_trades}")
            print(f"Winning Trades: {winning_trades}")
            print(f"Losing Trades: {total_trades - winning_trades}")
            print(f"Winning Rate: {(winning_trades / total_trades) * 100:.2f}%")
            print(f"Initial Balance: ${initial_capital:.2f}")
            print(f"Final Balance: ${risk_management.get_capital():.2f}")
            print(f"Total Profit/Loss: ${total_profit_loss:.2f}")
            print(f"Average Trade Duration: {average_duration}")
            print(f"\nAverage Trades per Day: {total_trades / len(trades_per_day):.2f}")
        else:
            print("\nNo trades were processed successfully.")
    else:
        print("No trades found.")

if __name__ == "__main__":
    main()
