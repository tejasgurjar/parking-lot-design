import constants
from feemodel.fee_model import FeeModel
from feemodel.interval_fee_model import IntervalHourlyFeeModel
from feemodel.flat_fee_model import FlatDailyFeeModel
from math import ceil
from datetime import timedelta


class DailyFeeModel(FeeModel):

    # Use the interval (24, None) to represent daily flat rate
    DAILY_FLAT_RATE_INTERVAL = (24, None)

    def __init__(self):
        self.interval_hourly_feemodel = IntervalHourlyFeeModel()
        self.flat_daily_feemodel = FlatDailyFeeModel()

    @classmethod
    def get_daily_rate(cls, rates, slot_type):
        return rates[slot_type][cls.DAILY_FLAT_RATE_INTERVAL]

    def set_rate(self, rates):
        # set hourly interval based rates
        self.interval_hourly_feemodel.set_rate(rates)

        # set flat daily rates
        daily_flat_rates = dict()
        for slot_type in rates.keys():
            daily_flat_rates[slot_type] = self.get_daily_rate(rates, slot_type)
        self.flat_daily_feemodel.set_rate(daily_flat_rates)

    def calculate_fee(self, duration, lot, slot_type):
        num_of_hours = ceil(duration.seconds/constants.SECONDS_IN_HOUR)

        if duration.days is None or duration.days == 0:
            self.interval_hourly_feemodel.set_rate(self.rates)
            return self.interval_hourly_feemodel.calculate_fee(timedelta(duration.seconds), lot, slot_type)
        elif num_of_hours > 0:
            return self.flat_daily_feemodel.calculate_fee(duration + timedelta(hours=1), lot, slot_type)
        else:
            return self.flat_daily_feemodel.calculate_fee(duration, lot, slot_type)
