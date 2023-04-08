import os
from unittest import TestCase, skip
from tests.common import *
from lot.lot_factory import LotFactory, Places
from simulator.parking_simulator import ParkingSimulator, ActivityConfig


class TestParkingSimulator(TestCase):

    def setUp(self):
        self.activity_cfg = ActivityConfig(os.path.join(TESTDIR, self._testMethodName + "_activity_cfg.json"))


    def tearDown(self):
        LotFactory.factory_instance = None
        self.activity_cfg = None

    def test_simulate_mall_parking(self):
        parking_space_cfgfile = os.path.join(TESTDIR, self._testMethodName + "_cfg.py")

        lot_factory = LotFactory.get_instance(parking_space_cfgfile, Places.MALL.value)
        lot = lot_factory.get_parking_lot()
        sim = ParkingSimulator(lot, self.activity_cfg)
        sim.simulate()

        self.assertTrue(True)

    def test_simulate_airport_parking(self):
        parking_space_cfgfile = os.path.join(TESTDIR, self._testMethodName + "_cfg.py")

        lot_factory = LotFactory.get_instance(parking_space_cfgfile, Places.AIRPORT.value)
        lot = lot_factory.get_parking_lot()
        sim = ParkingSimulator(lot, self.activity_cfg)
        sim.simulate()
        self.assertTrue(True)

    def test_simulate_stadium_parking(self):
        parking_space_cfgfile = os.path.join(TESTDIR, self._testMethodName + "_cfg.py")
        lot_factory = LotFactory.get_instance(parking_space_cfgfile, Places.STADIUM.value)

        lot = lot_factory.get_parking_lot()
        sim = ParkingSimulator(lot, self.activity_cfg)

        sim.simulate()

        self.assertTrue(True)

    def test_simulate_parking_full(self):
        parking_space_cfgfile = os.path.join(TESTDIR, self._testMethodName + "_cfg.py")
        lot_factory = LotFactory.get_instance(parking_space_cfgfile, Places.STADIUM.value)

        lot = lot_factory.get_parking_lot()
        sim = ParkingSimulator(lot, self.activity_cfg)

        self.assertRaisesRegex(Exception, "No space available", sim.simulate)

    def test_simulate_parking_empty(self):
        parking_space_cfgfile = os.path.join(TESTDIR, self._testMethodName + "_cfg.py")
        lot_factory = LotFactory.get_instance(parking_space_cfgfile, Places.STADIUM.value)

        lot = lot_factory.get_parking_lot()
        sim = ParkingSimulator(lot, self.activity_cfg)

        self.assertRaisesRegex(Exception, "Ticket number T-\d+ was never allotted", sim.simulate)

