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

- Strategy.py : Simple moving average crossover file used in correlation with utils.py which dictates today's sentiment if we are shorting or longing a position. Capped at 1 trade per day (This needs to be optimized.)

- Main.py : Runs all of the files (riskmanagement, strategy, utils) all in one file by importing them (i see all the other files as indicators and i run them on a main file, that way is easier to import branches of code and apply them to another strategy
  or bot, instead of having to copy paste everytime. Mainly gives the output, and you can choose which csv file to run and capital to run by changing (Lines 15, and 28) 

- load_data.py : processes the intraday data from the csv file . 

The test folder was just tests i was starting with nothing important. 

Also added the trading report on pdf which showcases the result of this strategy and most importantly tells us how to optimize it, yes it did show great results but its far from being something to be deployed, many optimizations have to be made
before risking any capital such as described in the trading report, (i would optimize risk management mainly so its more consistent with the wins as with other csv files it didnt do as well even if still profitable very slow profits). 

My plan for optimizing it was the following : 
Current Situation: The strategy currently has a win rate of 50.59% with an average Risk-Reward (RR) ratio of 2:1. The goal is to increase the win rate while maintaining or improving the RR ratio.

Goals:

Increase Win Rate: Target a 60% win rate while keeping the current 2:1 RR ratio.
Maximize Winning Trades: Implement trailing stop losses to lock in profits and allow winning trades to run longer, thus maximizing gains.
Risk Management Focus: Keep stop losses consistent, but improve overall risk management to minimize losses and maximize profits.
Optimize Losses: Set a clear rule to minimize losses after trades exceed a certain threshold (e.g., when risk exceeds 1R), while maximizing returns after the trade moves in your favor (e.g., greater than 1R).
Key Focus:

Risk Management: The real differentiator is not just the RR ratio or win rate but disciplined risk management. Even with a 51% win rate and a 2:1 RR ratio over 20 years, profits are limited due to suboptimal risk management. Proper strategies should focus on improving this aspect.
List of Risk Management Strategies to Try:

Position Sizing: Adjust position sizes dynamically based on the current volatility or market conditions.
Fixed vs. Trailing Stop Losses: Use fixed stop losses for limiting losses and trailing stop losses for capturing larger profits as the trade moves in your favor.
Cut Losses Early: Set predefined levels (like 1R) where you automatically cut a trade if it starts turning unfavorable.
Risk Multiple Monitoring: Closely monitor the risk multiple and adjust your strategy as needed once the trade reaches 1R or higher.
Diversification Across Timeframes: Test the strategy on different timeframes (e.g., 1-minute, 5-minute, 10-minute) to find the most optimal settings for risk and reward.
Market Condition Adaptation: Adapt the strategy depending on the overall market condition (trending vs. ranging).

This is my first time coding anything and i have to break down the code proprely and understand it like its second nature and i would recomend anyone transitionning from trading to coding to do as i did, hands on project with AI and then breaking down code to learn which is the hardest and then redoing it yourself by limiting the usage of AI. I wish everyone the best when starting your coding journey even if i just started i would say its essential you will need it one day. 
