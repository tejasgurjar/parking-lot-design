from abc import ABC, abstractmethod
from feemodel.interval_table.interval_table import  IntervalTable


class FeeModel(ABC):
    @abstractmethod
    def calculate_fee(self, duration, slot_type):
        pass