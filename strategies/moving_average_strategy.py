from .base_strategy import BaseStrategy
from .indicators import calculate_moving_averages

class MovingAverageStrategy(BaseStrategy):
    def __init__(self, params):
        self.params = params

    def apply_indicators(self, data):
        data = calculate_moving_averages(
            data,
            short_window=self.params.get('short_window', 50),
            long_window=self.params.get('long_window', 200)
        )
        return data

    def generate_signal(self, data):
        latest = data.iloc[-1]
        previous = data.iloc[-2]
        if previous['ma_short'] < previous['ma_long'] and latest['ma_short'] >= latest['ma_long']:
            return 'buy'
        elif previous['ma_short'] > previous['ma_long'] and latest['ma_short'] <= latest['ma_long']:
            return 'sell'
        else:
            return 'hold'

    def get_name(self):
        return "Moving Average Strategy"
