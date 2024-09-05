class RiskManagement:
    def __init__(self, capital, max_daily_loss=0.025, max_risk_per_trade=0.025, break_even_capital=0.01):
        self.capital = capital
        self.max_daily_loss = max_daily_loss
        self.max_risk_per_trade = max_risk_per_trade
        self.break_even_capital = break_even_capital
        self.current_losses = 0
        self.current_wins = 0
        self.daily_loss = 0
        self.initial_capital = capital
        self.current_risk = self.break_even_capital
        self.daily_trades = 0
        self.last_trade_date = None

    def calculate_trade_risk(self, stop_loss_distance, trade_date):
        """Calculate the amount of capital to risk per trade based on stop loss distance."""
        if self.last_trade_date == trade_date.date():
            print("Maximum of 1 trade per day reached. No further trades today.")
            return None
        
        if self.daily_loss >= self.max_daily_loss * self.initial_capital:
            print("Daily loss limit reached. No further trades today.")
            return None
        
        risk_amount = self.capital * self.current_risk
        position_size = risk_amount / stop_loss_distance
        return position_size

    def update_after_trade(self, result, trade_date):
        """Update the capital and loss/win streak counters after a trade."""
        if self.last_trade_date == trade_date.date():
            print("Error: Attempt to process multiple trades in one day.")
            return

        self.last_trade_date = trade_date.date()
        
        if result < 0:
            self.capital += result  # Subtract loss
            self.daily_loss += abs(result)
            self.current_losses += 1
            self.current_wins = 0
        else:
            self.capital += result  # Add profit
            self.current_wins += 1
            self.current_losses = 0
        
        self.daily_trades += 1

        # Handle daily loss limit
        if self.daily_loss >= self.max_daily_loss * self.initial_capital:
            print("Daily loss limit reached. No further trades today.")
            return

        # Handle losing streak and risk adjustment
        if self.current_losses >= 2:
            self.current_risk = max(self.current_risk / 2, self.break_even_capital)
            self.current_losses = 0  # Reset streak after adjustment
        else:
            self.current_risk = min(self.current_risk * 1.5, self.max_risk_per_trade)

        # Ensure risk per trade is within bounds
        self.current_risk = max(self.break_even_capital, min(self.current_risk, self.max_risk_per_trade))

    def get_capital(self):
        return self.capital

    def get_current_risk(self):
        return self.current_risk

    def reset_daily_values(self):
        """Reset daily values. Call this at the start of each trading day."""
        self.daily_loss = 0
        self.daily_trades = 0
        self.last_trade_date = None