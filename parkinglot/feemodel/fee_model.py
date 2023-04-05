from abc import ABC, abstractmethod
from feemodel.intervaltable.intervaltable import  IntervalTable


class FeeModel(ABC):
    @abstractmethod
    def calculate_fee(self, duration, lot, slot_type):
        pass