import datetime
from unittest import TestCase, skip
from feemodel.flat_fee_model import FlatFeeModel, FlatHourlyFeeModel
from feemodel.interval_fee_model import IntervalHourlyFeeModel, HourlyFeeModel
from feemodel.daily_fee_model import DailyFeeModel
from lot.vehicle_slot import SlotType
from lot.lot import Lot
from lot.lot_factory import Places


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

        cls.hour_rates = {
            SlotType.TWO_WHEELER.value: {
                (0, 9): 20,
                (9, 19): 40,
                (19, None): 100
            },
            SlotType.LV.value: {
                (0, 6): 100,
                (6, 12): 150,
                (12, None): 250,
            },
            SlotType.HV.value : {
                (0, 11): 500,
                (11, 15): 700,
                (15, None): 900
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

        parking_space = Lot(fee_model, self.mall_slots, Places.MALL.value)
        fee = fee_model.calculate_fee(duration, SlotType.LV)
        self.assertEqual(60, fee)

    def test_interval_hourly(self):
        fee_model = IntervalHourlyFeeModel()
        fee_model.set_rate(self.interval_rates)

        entry_time = datetime.datetime.fromisoformat("2023-01-01 07:00:00")
        exit_time = datetime.datetime.fromisoformat("2023-01-01 18:10:53")
        duration = exit_time - entry_time

        parking_space = Lot(fee_model, self.stadium_slots, Places.STADIUM.value)
        two_wheel_fee = fee_model.calculate_fee(duration, SlotType.TWO_WHEELER)
        lmv_fee = fee_model.calculate_fee(duration, SlotType.LV)
        self.assertEqual(115, two_wheel_fee)
        self.assertEqual(225, lmv_fee)

    def test_hourly1(self):
        fee_model = HourlyFeeModel()
        fee_model.set_rate(self.hour_rates)

        entry_time = datetime.datetime.fromisoformat("2023-01-01 07:00:00")
        exit_time = datetime.datetime.fromisoformat("2023-01-02 06:10:53")
        duration = exit_time - entry_time

        parking_space = Lot(fee_model, self.stadium_slots, Places.STADIUM.value)
        two_wheel_fee = fee_model.calculate_fee(duration, SlotType.TWO_WHEELER)
        lmv_fee = fee_model.calculate_fee(duration, SlotType.LV)
        self.assertEqual(560, two_wheel_fee)
        self.assertEqual(3250, lmv_fee)

    def test_hourly2(self):
        fee_model = HourlyFeeModel()
        fee_model.set_rate(self.hour_rates)

        entry_time = datetime.datetime.fromisoformat("2023-01-01 07:00:00")
        exit_time = datetime.datetime.fromisoformat("2023-01-01 19:00:00")
        duration = exit_time - entry_time

        parking_space = Lot(fee_model, self.stadium_slots, Places.STADIUM.value)
        two_wheel_fee = fee_model.calculate_fee(duration, SlotType.TWO_WHEELER)
        lmv_fee = fee_model.calculate_fee(duration, SlotType.LV)
        self.assertEqual(60, two_wheel_fee)
        self.assertEqual(500, lmv_fee)

    def test_daily(self):
        fee_model = DailyFeeModel()
        fee_model.set_rate(self.daily_rates)

        entry_time = datetime.datetime.fromisoformat("2023-01-01 07:00:00")
        exit_time = datetime.datetime.fromisoformat("2023-01-04 18:00:00")
        duration = exit_time - entry_time
        print("Duration:", duration.seconds)

        parking_space = Lot(fee_model, self.airport_slots, Places.AIRPORT.value)

        two_wheel_fee = fee_model.calculate_fee(duration, SlotType.TWO_WHEELER)
        lmv_fee = fee_model.calculate_fee(duration, SlotType.LV)

        self.assertEqual(800, two_wheel_fee)
        self.assertEqual(1600, lmv_fee)