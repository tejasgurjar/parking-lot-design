import os
from unittest import TestCase
from tests.common import *
from lot.lot_factory import LotFactory, Places
from simulator.parking_simulator import ParkingSimulator


class TestParkingSimulator(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simulate_mall_parking(self):
        activity_cfgfile = os.path.join(TESTDIR, self._testMethodName + "_activity_cfg.json")
        parking_space_cfgfile = os.path.join(TESTDIR, self._testMethodName + "_cfg.py")

        lot_factory = LotFactory.get_instance(parking_space_cfgfile)
        lot = lot_factory.get_parking_lot(Places.MALL.value)
        sim = ParkingSimulator(lot, activity_cfgfile)
        sim.simulate()

        self.assertTrue(True)

    def test_simulate_airport_parking(self):
        activity_cfgfile = os.path.join(TESTDIR, self._testMethodName + "_activity_cfg.json")
        parking_space_cfgfile = os.path.join(TESTDIR, self._testMethodName + "_cfg.py")

        lot_factory = LotFactory.get_instance(parking_space_cfgfile)
        lot = lot_factory.get_parking_lot(Places.AIRPORT.value)
        sim = ParkingSimulator(lot, activity_cfgfile)
        sim.simulate()

        self.assertTrue(True)