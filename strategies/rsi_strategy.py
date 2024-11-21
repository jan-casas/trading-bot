from .base_strategy import BaseStrategy
from .indicators import calculate_rsi

class RSIStrategy(BaseStrategy):
    def __init__(self, params):
        self.params = params

    def apply_indicators(self, data):
        data = calculate_rsi(data, period=self.params.get('rsi_period', 14))
        return data

    def generate_signal(self, data):
        latest = data.iloc[-1]
        if latest['rsi'] < self.params.get('buy_threshold', 30):
            return 'buy'
        elif latest['rsi'] > self.params.get('sell_threshold', 70):
            return 'sell'
        else:
            return 'hold'

    def get_name(self):
        return "RSI Strategy"
