from .base_strategy import BaseStrategy
from .rsi_strategy import RSIStrategy
from .moving_average_strategy import MovingAverageStrategy
from .mean_reversion_strategy import MeanReversionStrategy
from .breakout_strategy import BreakoutStrategy

class CombinedStrategy(BaseStrategy):
    def __init__(self, params):
        self.params = params
        # Initialize individual strategies
        self.strategies = [
            RSIStrategy(params.get('RSI Strategy', {})),
            MovingAverageStrategy(params.get('Moving Average Strategy', {})),
            MeanReversionStrategy(params.get('Mean Reversion Strategy', {})),
            BreakoutStrategy(params.get('Breakout Strategy', {})),
            # Add more strategies if needed
        ]

    def apply_indicators(self, data):
        # Apply indicators from all strategies
        for strategy in self.strategies:
            data = strategy.apply_indicators(data)
        return data

    def generate_signal(self, data):
        signals = []
        for strategy in self.strategies:
            signal = strategy.generate_signal(data)
            signals.append(signal)
        # Aggregate signals
        final_signal = self.aggregate_signals(signals)
        return final_signal

    def aggregate_signals(self, signals):
        # Example: Majority voting
        buy_count = signals.count('buy')
        sell_count = signals.count('sell')
        if buy_count > sell_count:
            return 'buy'
        elif sell_count > buy_count:
            return 'sell'
        else:
            return 'hold'

    def get_name(self):
        return "Combined Strategy"
