import constants
from math import ceil
from datetime  import timedelta
from feemodel.fee_model import FeeModel
from feemodel.flat_fee_model import FlatHourlyFeeModel
from feemodel.interval_table.interval_table import IntervalTable, OutOfRangeException


def seconds_to_hours(seconds):
    return seconds / constants.SECONDS_IN_HOUR


class IntervalHourlyFeeModel(FeeModel):
    def __init__(self):
        self.rates = None

    def set_rate(self, rates):
        self.rates = dict()
        for k in rates.keys():
            self.rates[k] = IntervalTable(rates[k])

    def find_interval(self, slot_type, num_of_hours):
        interval_table = self.rates[slot_type.value]
        return interval_table.find_interval(num_of_hours)

    def last_interval(self, slot_type):
        interval_table = self.rates[slot_type.value]
        return interval_table.get_last_interval()

    def get_interval_value(self, interval_id, slot_type):
        interval_table = self.rates[slot_type.value]
        return interval_table.get_interval(interval_id)

    def calculate_fee(self, duration, slot_type):
        hours = seconds_to_hours(duration.seconds)

        try:
            interval_id = self.find_interval(slot_type, hours)
            return self.calculate_fee_by_interval_id(interval_id, slot_type)
        except Exception as e:
            print("Error in calculation of parking fee:" + str(e))
            raise

    def calculate_fee_by_interval_id(self, interval_id, slot_type):
        try:
            fee_sum = 0
            for int_id in range(0, interval_id):
                fee_sum += self.rates[slot_type.value].get_value(int_id)  # Sum up fees from previous intervals

            remaining_charge = self.rates[slot_type.value].get_value(interval_id)

            return fee_sum + remaining_charge
        except Exception as e:
            print("Error in calculation of parking fee:" + str(e))
            raise


class IntervalHourlyNonCumulativeFeeModel(IntervalHourlyFeeModel):
    def __init__(self):
        self.rates = None

    def calculate_fee(self, duration, slot_type):
        hours = seconds_to_hours(duration.seconds)
        try:
            interval_id = self.find_interval(slot_type, hours)
            charge = self.rates[slot_type.value].get_value(interval_id)
            return charge
        except Exception as e:
            print("Error in calculation of parking fee:" + str(e))
            raise


class HourlyFeeModel(FeeModel):
    def __init__(self):
        self.interval_hourly_feemodel = IntervalHourlyFeeModel()
        self.flat_hourly_feemodel = FlatHourlyFeeModel()

    @classmethod
    def get_hourly_rate(cls, rates, slot_type):
        for interval in rates[slot_type]:
            if interval[1] is not None:
                continue
            else:
                return rates[slot_type][interval]

    def set_rate(self, rates):
        # set hourly interval based rates
        self.interval_hourly_feemodel.set_rate(rates)

        # set flat hourly rates
        hourly_flat_rates = dict()
        for slot_type in rates.keys():
            hourly_flat_rates[slot_type] = self.get_hourly_rate(rates, slot_type)
        self.flat_hourly_feemodel.set_rate(hourly_flat_rates)

    def calculate_fee(self, duration, slot_type):
        hours = seconds_to_hours(duration.seconds)

        try:
            interval_id = self.interval_hourly_feemodel.find_interval(slot_type, hours)
            return self.interval_hourly_feemodel.calculate_fee_by_interval_id(interval_id, slot_type)
        except OutOfRangeException:
            last_interval_id = self.interval_hourly_feemodel.last_interval(slot_type)
            lo, last_interval_id_hi = self.interval_hourly_feemodel.get_interval_value(last_interval_id, slot_type)
            interval_fee = self.interval_hourly_feemodel.calculate_fee_by_interval_id(last_interval_id, slot_type)

            remaining_hours = ceil(max(1, (hours - last_interval_id_hi)))
            per_hour_charge = self.flat_hourly_feemodel.calculate_fee(timedelta(hours=remaining_hours), slot_type)
            return interval_fee + per_hour_charge
        except Exception as e:
            print("Error in calculation of parking fee:" + str(e))
            raise
