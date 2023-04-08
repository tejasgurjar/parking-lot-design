from vehicle.vehicle_lv import VehicleLV
from vehicle.vehicle_twowheeler import VehicleTwoWheeler
from vehicle.vehicle_hv import VehicleHV
from lot.vehicle_slot import SlotType
from config.vehicle_slot_type_cfg import vehicle_slot_type_map


class VehicleFactory(object):
    factory_instance = None

    def __init__(self):
        self.vehicle_class_map = {
            SlotType.LV : VehicleLV,
            SlotType.TWO_WHEELER: VehicleTwoWheeler,
            SlotType.HV: VehicleHV
        }

    @classmethod
    def get_instance(cls):
        if cls.factory_instance is None:
            cls.factory_instance = VehicleFactory()

        return cls.factory_instance

    def get_vehicle(self, vehicle_type, lot):
        if vehicle_type not in vehicle_slot_type_map:
            raise Exception (f"Vehicle type {vehicle_type} not recognized. Supported vehicles are:", vehicle_slot_type_map.keys())

        slot_type = vehicle_slot_type_map[vehicle_type]
        vehicle_klass = self.vehicle_class_map[slot_type]

        return vehicle_klass(vehicle_type, lot)
