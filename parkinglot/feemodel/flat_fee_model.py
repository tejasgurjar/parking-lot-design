import constants
from math import ceil
from feemodel.fee_model import FeeModel


class FlatFeeModel(FeeModel):
    def __init__(self):
        self.rates = None

    def set_rate(self, rates):
        self.rates = rates

    def calculate_fee(self, duration, slot_type):
        # flat rate time spent *  rate based on place, vehicle
        time_units = self.get_time_units(duration)
        rate = self.rates[slot_type.value]
        return rate * time_units


class FlatHourlyFeeModel(FlatFeeModel):
    def __init__(self):
        super().__init__()

    def get_time_units(self, duration):
        return ceil(duration.seconds/constants.SECONDS_IN_HOUR)


class FlatDailyFeeModel(FlatFeeModel):
    def __init__(self):
        super().__init__()

    def set_rate(self, rates):
        self.rates = rates

    def get_time_units(self, duration):
        return duration.days + ceil(duration.seconds/constants.SECONDS_IN_DAY)