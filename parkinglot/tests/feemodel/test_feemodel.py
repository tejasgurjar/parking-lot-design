import datetime
from unittest import TestCase, skip
from feemodel.flat_fee_model import FlatFeeModel, FlatHourlyFeeModel
from feemodel.interval_fee_model import IntervalHourlyFeeModel
from feemodel.daily_fee_model import DailyFeeModel
from lot.vehicle_slot import SlotType
from lot.lot import Lot


class TestFeeModel(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.flat_hourly_rates =  {
            SlotType.TWO_WHEELER.value: 10,
            SlotType.LV.value: 20,
            SlotType.HV.value: 100
        }

        cls.mall_slots = {
            SlotType.TWO_WHEELER.value: 100,
            SlotType.LV.value: 200,
        }

        cls.interval_rates = {
            SlotType.TWO_WHEELER.value: {
                (0, 9): 40,
                (9, 19): 75,
                (19, 24): 100,
                (24, None): 200
            },
            SlotType.LV.value: {
                (0, 6): 100,
                (6, 12): 125,
                (12, 24): 200,
                (24, None): 300
            },
            SlotType.HV.value : {
                (0, 11): 500,
                (11, 24): 1000,
                (24, None): 1200
            },
        }

        cls.stadium_slots = {
            SlotType.TWO_WHEELER.value: 100,
            SlotType.LV.value: 200,
            SlotType.HV.value : 50
        }

        cls.daily_rates = {
            SlotType.TWO_WHEELER.value: {
                (0, 9): 40,
                (9, 18): 75,
                (18, 24): 100,
                (24, None): 200
            },
            SlotType.LV.value: {
                (0, 6): 100,
                (7, 12): 125,
                (13, 24): 200,
                (24, None): 400
            },
            SlotType.HV.value : {
                (0, 11): 500,
                (12, 24): 1000,
                (24, None): 1500
            },
        }

        cls.airport_slots = {
            SlotType.TWO_WHEELER.value: 500,
            SlotType.LV.value: 2000,
            SlotType.HV.value : 250
        }

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_flat_hourly(self):
        fee_model = FlatHourlyFeeModel()
        fee_model.set_rate(self.flat_hourly_rates)

        entry_time = datetime.datetime.fromisoformat("2023-01-01 14:00:00")
        exit_time = datetime.datetime.fromisoformat("2023-01-01 16:10:00")
        duration = exit_time - entry_time

        parking_space = Lot(fee_model, self.mall_slots)
        fee = fee_model.calculate_fee(duration, parking_space, SlotType.LV)
        self.assertEqual(60, fee)

    def test_interval_hourly(self):
        fee_model = IntervalHourlyFeeModel()
        fee_model.set_rate(self.interval_rates)

        entry_time = datetime.datetime.fromisoformat("2023-01-01 07:00:00")
        exit_time = datetime.datetime.fromisoformat("2023-01-01 18:10:53")
        duration = exit_time - entry_time

        parking_space = Lot(fee_model, self.stadium_slots)
        import pdb
        pdb.set_trace()
        two_wheel_fee = fee_model.calculate_fee(duration, parking_space, SlotType.TWO_WHEELER)
        lmv_fee = fee_model.calculate_fee(duration, parking_space, SlotType.LV)
        self.assertEqual(115, two_wheel_fee)
        self.assertEqual(225, lmv_fee)

    def test_daily(self):
        fee_model = DailyFeeModel()
        fee_model.set_rate(self.daily_rates)

        entry_time = datetime.datetime.fromisoformat("2023-01-01 07:00:00")
        exit_time = datetime.datetime.fromisoformat("2023-01-02 18:00:00")
        duration = exit_time - entry_time
        print("Duration:", duration.seconds)

        parking_space = Lot(fee_model, self.airport_slots)

        two_wheel_fee = fee_model.calculate_fee(duration, parking_space, SlotType.TWO_WHEELER)
        lmv_fee = fee_model.calculate_fee(duration, parking_space, SlotType.LV)

        self.assertEqual(400, two_wheel_fee)
        self.assertEqual(800, lmv_fee)