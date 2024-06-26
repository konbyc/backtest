Trading strategy backtest. Uses yfinance as price data source. To use:

1. Specify your ticker and starting date in main.py,
2. Specify your strategy in the determine_position method in strategy.py,
3. Run.

The output contains plots of cumulative strategy returns as compared to the market. The periods of holding long and short positions are highlighted.

Figure_1.png and Figure_2.png are example output files:

ticker: GOOG
period: 2020-01-01 till present
strategy: an elementary trend following strategy -- long when SMA20 above SMA50 AND SMA50 above SMA200; short if SMA20 below SMA50 AND SMA50 below SMA200