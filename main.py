from strategy import Strategy


if __name__ == '__main__':
    strategy = Strategy('goog', '2020-01-01')
    strategy.generate_indicators()
    strategy.determine_position()
    strategy.find_trade_dates()
    strategy.calculate_returns()
    strategy.plot_results()





