from .base_strategy import BaseStrategy
from .indicators import calculate_atr

class BreakoutStrategy(BaseStrategy):
    def __init__(self, params):
        self.params = params

    def apply_indicators(self, data):
        data = calculate_atr(data, window=self.params.get('atr_window', 14))
        return data

    def generate_signal(self, data):
        latest = data.iloc[-1]
        resistance = data['high'].rolling(window=self.params.get('lookback_window', 20)).max().iloc[-2]
        support = data['low'].rolling(window=self.params.get('lookback_window', 20)).min().iloc[-2]

        if latest['close'] > resistance + latest['atr']:
            return 'buy'
        elif latest['close'] < support - latest['atr']:
            return 'sell'
        else:
            return 'hold'

    def get_name(self):
        return "Breakout Strategy"
