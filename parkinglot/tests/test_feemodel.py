import datetime
from unittest import TestCase
from feemodel.flat_fee_model import FlatFeeModel
from feemodel.interval_fee_model import HourlyIntervalFeeModel

from lot.vehicle_slot import SlotType
from lot.lot import Lot


class TestFeeModel(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.flat_hourly_rates =  {
            SlotType.TWO_WHEELER: 10,
            SlotType.LMV: 20,
            SlotType.HV: 100
        }

        cls.mall_slots = {
            SlotType.TWO_WHEELER: 100,
            SlotType.LMV: 200,
        }

        cls.interval_rates = {
            SlotType.TWO_WHEELER: {
                (0, 8): 40,
                (9, 18): 75,
                (19, 23): 100
            },
            SlotType.LMV: {
                (0, 6): 100,
                (7, 12): 125,
                (13, 23): 200
            },
            SlotType.HV : {
                (0, 11): 500,
                (12, 23): 1000
            },
        }

        cls.stadium_slots = {
            SlotType.TWO_WHEELER: 100,
            SlotType.LMV: 200,
            SlotType.HV : 50
        }

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_flat_hourly(self):
        fee_model = FlatFeeModel()
        fee_model.set_rate(self.flat_hourly_rates)

        entry_time = datetime.datetime.fromisoformat("2023-01-01 14:00:00")
        exit_time = datetime.datetime.fromisoformat("2023-01-01 16:10:00")
        duration = exit_time - entry_time

        parking_space = Lot(fee_model, self.mall_slots)
        fee = fee_model.calculate_fee(duration, parking_space, SlotType.LMV)
        self.assertEquals(60, fee)

    def test_interval_hourly(self):
        fee_model = HourlyIntervalFeeModel()
        fee_model.set_rate(self.interval_rates)

        entry_time = datetime.datetime.fromisoformat("2023-01-01 07:00:00")
        exit_time = datetime.datetime.fromisoformat("2023-01-01 18:10:53")
        duration = exit_time - entry_time

        parking_space = Lot(fee_model, self.stadium_slots)
        two_wheel_fee = fee_model.calculate_fee(duration, parking_space, SlotType.TWO_WHEELER)
        lmv_fee = fee_model.calculate_fee(duration, parking_space, SlotType.LMV)
        self.assertEquals(75, two_wheel_fee)
        self.assertEquals(125, lmv_fee)