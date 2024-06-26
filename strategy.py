import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf


class Strategy:

    def __init__(self, ticker: str, starting_date: str) -> None:
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.df = self.stock.history(start=starting_date, rounding=True)[['Close']].rename(columns={'Close': 'Price'})
        self.long: list[tuple[int, int]] = []    # intervals of holding long position
        self.short: list[tuple[int, int]] = []   # intervals of holding short position

    def generate_indicators(self) -> None:
        """
            currently only the SMAs for a simple strategy demonstration
        """
        self.df['SMA20'] = self.df['Price'].rolling(20).mean()
        self.df['SMA50'] = self.df['Price'].rolling(50).mean()
        self.df['SMA200'] = self.df['Price'].rolling(200).mean()

    def determine_position(self) -> None:
        """
            Assigns values according to the strategy

            1: long
            0: no position
           -1: short
        """
        # an elementary trend following strategy
        # long when SMA20 above SMA50 AND SMA50 above SMA200; short if SMA20 below SMA50 AND SMA50 below SMA200
        self.df['position'] = (self.df['SMA20'] > self.df['SMA50']).astype(int) + (self.df['SMA50'] > self.df['SMA200']).astype(int) - 1

    def find_trade_dates(self) -> None:
        """
            Find the dates when trades need to be executed
        """
        current_value = None
        start = None
        for i, value in enumerate(self.df.position):
            if value != current_value and value != 0:
                # found start of holding a position
                if start is not None:
                    # long|short switched with no break
                    if value == 1:
                        self.short.append((start, i - 1))  # previous position was short
                    else:
                        self.long.append((start, i - 1))   # previous position was long
                start = i
                current_value = value
            elif value == 0 and start is not None:
                # found end of holding a position
                if current_value == 1:
                    self.long.append((start, i - 1))
                else:
                    self.short.append((start, i - 1))
                start = None
                current_value = None
        if start is not None:
            # handle the last position if it reaches the end of the list
            if current_value == 1:
                self.long.append((start, len(self.df.position) - 1))
            else:
                self.short.append((start, len(self.df.position) - 1))

    def calculate_returns(self) -> None:
        self.df['log returns'] = np.log(self.df['Price'] / self.df['Price'].shift(1))
        self.df['cumulative market returns'] = np.exp(self.df['log returns'].cumsum())
        self.df['strategy returns'] = self.df['log returns'] * self.df['position']
        self.df['cumulative strategy returns'] = np.exp(self.df['strategy returns'].cumsum())

    def plot_results(self) -> None:
        plt.figure(figsize=(12, 5), dpi=80)
        plt.scatter(self.df.index, self.df['Price'], s=0.5, label='Close price')
        plt.plot(self.df.index, self.df['SMA20'], label='SMA20')
        plt.plot(self.df.index, self.df['SMA50'], label='SMA50')
        plt.plot(self.df.index, self.df['SMA200'], label='SMA200')
        for trade in self.long:
            plt.axvspan(self.df.index[trade[0]], self.df.index[trade[1]], alpha=0.3, color='green', zorder=0)
        for trade in self.short:
            plt.axvspan(self.df.index[trade[0]], self.df.index[trade[1]], alpha=0.3, color='red', zorder=0)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.title(self.ticker.upper())

        plt.figure(figsize=(12, 5), dpi=80)
        plt.plot(self.df.index, self.df['cumulative market returns'], label='market')
        plt.plot(self.df.index, self.df['cumulative strategy returns'], label='strategy')
        for trade in self.long:
            plt.axvspan(self.df.index[trade[0]], self.df.index[trade[1]], alpha=0.3, color='green', zorder=0)
        for trade in self.short:
            plt.axvspan(self.df.index[trade[0]], self.df.index[trade[1]], alpha=0.3, color='red', zorder=0)
        plt.legend()
        plt.title(self.ticker.upper())

        plt.show()
