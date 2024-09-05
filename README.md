Data folder : Contains the intraday data for EURUSD 5 Minute time frame, from 2023/01/01 to 2023/09/11
Also contains a file named : split_dataframe.py.py, this file's main goal is to transform a new csv file that you imported, for example if you import a csv file from another pair and the format is not:
(timestamp,time,open,high,low,close,volume
20230101,22:07:00,1.0681,1.0681,1.0681,1.0681,1) 
it transforms it into the desired format so it can run without any errors. 

src file : 
- Utils.py (Asian Range 19:00 - 00:00) calculates also the highest price point and lowest price point during this time which is used to know if we are going to buy for the day or sell for the day, and also turns timezone into UTC -4 (New york time) which
  is the desired time you want to use when trading to get used to the trading hours which are high in volatility and liquidity.

  - RiskManagement.py; Nothing to explain simple risk management rules, capped at 1 trade per day max daily loss of 2.5%, max risk per trade 2.5% // and if price is break even risk is 1%, everytime you lose a trade lot size is halved by 2 meaning 1 --> 0.5
    and when on a winning streak it goes from 1 --> 1.5 --> 2 --> 2.5 max 
