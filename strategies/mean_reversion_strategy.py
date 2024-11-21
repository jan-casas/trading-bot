from .base_strategy import BaseStrategy
from .indicators import calculate_z_score

class MeanReversionStrategy(BaseStrategy):
    def __init__(self, params):
        self.params = params

    def apply_indicators(self, data):
        data = calculate_z_score(data, window=self.params.get('z_score_window', 20))
        return data

    def generate_signal(self, data):
        latest = data.iloc[-1]
        if latest['z_score'] <= self.params.get('buy_threshold', -2):
            return 'buy'
        elif latest['z_score'] >= self.params.get('sell_threshold', 2):
            return 'sell'
        else:
            return 'hold'

    def get_name(self):
        return "Mean Reversion Strategy"
