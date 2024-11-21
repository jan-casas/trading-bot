import importlib
from config.config import ACTIVE_STRATEGIES, STRATEGY_PARAMETERS

class StrategyManager:
    def __init__(self):
        self.strategies = []

    def load_strategies(self):
        for strategy_path in ACTIVE_STRATEGIES:
            module_name, class_name = strategy_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            strategy_class = getattr(module, class_name)
            params = STRATEGY_PARAMETERS.get(strategy_class(None).get_name(), {})
            strategy_instance = strategy_class(params)
            self.strategies.append(strategy_instance)

    def get_strategies(self):
        return self.strategies
