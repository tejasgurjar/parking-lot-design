from abc import ABC, abstractmethod


class FeeModel(ABC):
    def set_rate(self, rates):
        self.rates = rates

    @abstractmethod
    def calculate_fee(self, duration, lot, slot_type):
        pass