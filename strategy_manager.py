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

    def enable_strategy(self, strategy_name):
        for strategy in self.strategies:
            if strategy.get_name() == strategy_name:
                strategy.enable()
                return True
        return False

    def disable_strategy(self, strategy_name):
        for strategy in self.strategies:
            if strategy.get_name() == strategy_name:
                strategy.disable()
                return True
        return False

    def update_strategy_params(self, strategy_name, new_params):
        for strategy in self.strategies:
            if strategy.get_name() == strategy_name:
                strategy.update_params(new_params)
                return True
        return False

    def run_strategies(self):
        for strategy in self.strategies:
            strategy.execute_strategy()
