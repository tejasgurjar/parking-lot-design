import os
import sys
from lot.lot_factory import LotFactory
from simulator.parking_simulator import ParkingSimulator
from simulator.activity import ActivityConfig


def manage_parking(lot_cfgfile, parking_activity_cfgfile):
    activity_config = ActivityConfig(parking_activity_cfgfile)
    lot_factory = LotFactory.get_instance(lot_cfgfile, activity_config.get_location())
    lot = lot_factory.get_parking_lot()
    ps = ParkingSimulator(lot, activity_config)
    ps.simulate()


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + "<activity config json file> [parking lot config (.py) file]")
        sys.exit(1)

    parking_activity_cfg = sys.argv[1]
    command = sys.argv[0]
    location = os.path.dirname(command)
    lot_cfg  = os.path.join(location, "config", "default_parking_lot.py")

    if len(sys.argv) == 3:
        lot_cfg = sys.argv[2]

    manage_parking(lot_cfg, parking_activity_cfg)


