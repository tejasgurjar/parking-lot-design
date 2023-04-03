import sys
from lot.lot_factory import LotFactory
from simulator.parking_simulator import ParkingSimulator

def manage_parking(lot_cfg, parking_activity_cfg):
    lot_factory = LotFactory(lot_cfg)
    lot = lot_factory.get_parking_lot()
    ps = ParkingSimulator(parking_activity_cfg)
    ps.simulate()


if __name__ == '__main__':
    lot_cfg = sys.argv[1]
    parking_activity_cfg = sys.argv[2]
    manage_parking(lot_cfg, parking_activity_cfg)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
