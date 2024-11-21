from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    def apply_indicators(self, data):
        pass

    @abstractmethod
    def generate_signal(self, data):
        pass

    @abstractmethod
    def get_name(self):
        pass
