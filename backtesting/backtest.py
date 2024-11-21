# backtesting/backtest.py

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Add the parent directory to sys.path to import from strategies
sys.path.append(os.path.abspath('..'))

from strategies.strategy import apply_indicators, generate_signal

def backtest(symbol):
    # Load historical data
    data = pd.read_csv(f'historical_data/{symbol}_daily.csv', index_col='timestamp', parse_dates=True)
    data = apply_indicators(data)
    data['signal'] = data.apply(lambda row: generate_signal(data.loc[:row.name]), axis=1)
    data['position'] = data['signal'].replace({'buy': 1, 'sell': -1, 'hold': 0}).shift()
    data['position'].fillna(0, inplace=True)
    data['returns'] = data['close'].pct_change()
    data['strategy_returns'] = data['position'] * data['returns']
    data['cumulative_returns'] = (1 + data['strategy_returns']).cumprod()

    # Plot performance
    plt.figure(figsize=(12, 6))
    plt.plot(data['cumulative_returns'], label='Strategy Returns')
    plt.title(f'Backtesting Strategy Performance for {symbol}')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()

    # Save plot to file
    plot_filename = f'backtest_{symbol}.png'
    plt.savefig(plot_filename)
    plt.close()

    # Print performance metrics
    total_return = data['cumulative_returns'].iloc[-1] - 1
    print(f"Total Return: {total_return * 100:.2f}%")
    return total_return, plot_filename

if __name__ == "__main__":
    symbol = 'BTCUSDT'  # Change as needed
    backtest(symbol)
