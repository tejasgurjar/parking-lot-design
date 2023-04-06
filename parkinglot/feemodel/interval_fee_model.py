import constants
from math import ceil
from datetime  import timedelta
from feemodel.fee_model import FeeModel
from feemodel.flat_fee_model import FlatHourlyFeeModel
from feemodel.intervaltable.intervaltable import IntervalTable


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

    def calculate_fee(self, duration, lot, slot_type):
        hours = ceil(duration.seconds/constants.SECONDS_IN_HOUR)
        try:
            interval_id = self.find_interval(slot_type, hours)

            fee_sum = 0
            for id in range(0, interval_id):
                fee_sum += self.rates[slot_type.value].get_value(id)  # Sum up fees from previous intervals

            remaining_charge = self.rates[slot_type.value].get_value(interval_id)

            return fee_sum + remaining_charge
        except Exception as e:
            print("Error in calculation of parking fee:" + str(e))
            raise


class IntervalHourlyNonCumulativeFeeModel(IntervalHourlyFeeModel):
    def __init__(self):
        self.rates = None

    def calculate_fee(self, duration, lot, slot_type):
        hours = ceil(duration.seconds/constants.SECONDS_IN_HOUR)
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
                #TODO: Add validation to ensure at least one interval with INF exists
                return rates[slot_type][interval]

    def set_rate(self, rates):
        # set hourly interval based rates
        self.interval_hourly_feemodel.set_rate(rates)

        # set flat hourly rates
        hourly_flat_rates = dict()
        for slot_type in rates.keys():
            hourly_flat_rates[slot_type] = self.get_hourly_rate(rates, slot_type)
        self.flat_hourly_feemodel.set_rate(hourly_flat_rates)

    def calculate_fee(self, duration, lot, slot_type):
        hours = ceil(duration.seconds/constants.SECONDS_IN_HOUR)
        try:
            interval_id = self.find_interval(slot_type, hours)

            fee_sum = 0
            for id in range(0, interval_id):
                fee_sum += self.rates[slot_type.value].get_value(id)  # Sum up fees from previous intervals

            lo, hi = self.rates[slot_type.value].get_interval(interval_id)

            # Calculate per hour charge if any
            if hi is None: # signifies 'Infinity'
                remaining_hours = (hours - lo) + 1
                flat_charge = self.flat_hourly_feemodel.calculate_fee(timedelta(hours=remaining_hours), lot, slot_type)
                fee_sum += remaining_hours * flat_charge
            else:
                fee_sum += self.rates[slot_type.value].get_value(interval_id)

            return fee_sum
        except Exception as e:
            print("Error in calculation of parking fee:" + str(e))
            raise