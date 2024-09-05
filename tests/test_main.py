import unittest
import pandas as pd
from main import simulate_trade
from Riskmanagement import RiskManagement
from strategy import trading_strategy

class TestTradingSystem(unittest.TestCase):

    def setUp(self):
        self.data = {
            'open': [1.1000, 1.1050, 1.1100, 1.1150, 1.1130, 1.1080, 1.1020],
            'high': [1.1020, 1.1070, 1.1120, 1.1170, 1.1140, 1.1090, 1.1030],
            'low': [1.0980, 1.1030, 1.1080, 1.1130, 1.1100, 1.1050, 1.1000],
            'close': [1.1010, 1.1060, 1.1110, 1.1150, 1.1120, 1.1070, 1.1025],
        }
        index = pd.date_range(start='2024-08-16 00:00:00', periods=7, freq='h', tz='UTC')
        self.df = pd.DataFrame(self.data, index=index)
        
        self.asian_high = 1.1060
        self.risk_management = RiskManagement(capital=10000, max_daily_loss=0.025, max_risk_per_trade=0.025, break_even_capital=0.01)

    def test_simulate_trade(self):
        entry_price = 1.1100
        stop_loss = 1.1050
        take_profit = 1.1150
        position_size = 100  # Example size
        result = simulate_trade(entry_price, stop_loss, take_profit, position_size)
        expected_result = (take_profit - entry_price) * position_size
        self.assertEqual(result, expected_result)

    def test_trading_strategy(self):
        trade = trading_strategy(self.df, self.asian_high)
        if trade:
            entry_price, stop_loss, take_profit = trade
            self.assertIsInstance(trade, tuple)
            self.assertEqual(len(trade), 3)  # Expecting (entry_price, stop_loss, take_profit)
            # Add additional checks if you have expected values
            self.assertTrue(entry_price > 0, "Entry price should be positive.")
            self.assertTrue(stop_loss > entry_price, "Stop loss should be greater than entry price.")
            self.assertTrue(take_profit < entry_price, "Take profit should be less than entry price.")
        else:
            self.fail("No valid sell setup found.")

    def test_risk_management(self):
        # Test risk management calculations
        self.risk_management.update_after_trade(-250)  # Example trade result with loss
        self.assertLessEqual(self.risk_management.get_capital(), 10000)
        self.assertGreaterEqual(self.risk_management.get_current_risk(), 0.0)
        # Add additional checks if needed
        self.assertGreater(self.risk_management.get_capital(), 0, "Capital should be greater than zero after a loss.")
        # You can add more checks based on expected risk adjustments

if __name__ == '__main__':
    unittest.main()

