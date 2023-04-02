import constants
from feemodel.fee_model import FeeModel


class FlatFeeModel(FeeModel):
    def __init__(self):
        self.rates = None

    def calculate_fee(self, duration, lot, slot_type):
        # flat rate num of hours * hourly rate based on place, vehicle

        hours = duration.seconds/constants.SECONDS_IN_HOUR
        hourly_rate = self.rates[slot_type]
        return hourly_rate * hours

