from vehicle.vehicle_lv import VehicleLV
from vehicle.vehicle_twowheeler import VehicleTwoWheeler
from vehicle.vehicle_hv import VehicleHV
from lot.vehicle_slot import SlotType


class VehicleFactory(object):
    factory_instance = None

    def __init__(self):
        self.vehicle_class_map = {
            SlotType.LV : VehicleLV,
            SlotType.TWO_WHEELER: VehicleTwoWheeler,
            SlotType.HV: VehicleHV
        }

        self.vehicle_slot_type_map = {
            'car': SlotType.LV,
            'suv': SlotType.LV,
            'electric_suv': SlotType.LV,
            'motorcycle': SlotType.TWO_WHEELER,
            'scooter': SlotType.TWO_WHEELER,
            'truck': SlotType.HV,
            'bus': SlotType.HV
        }

    @classmethod
    def get_instance(cls):
        if cls.factory_instance is None:
            cls.factory_instance = VehicleFactory()

        return cls.factory_instance

    def is_vehicle_type_valid(self, vehicle_type):
        return vehicle_type in self.vehicle_slot_type_map

    def get_slot_type(self, vehicle_type):
        return self.vehicle_slot_type_map[vehicle_type]


    def get_valid_vehicles(self):
        return sorted(self.vehicle_slot_type_map.keys())

    def get_vehicle(self, vehicle_type, lot):
        #if vehicle_type not in vehicle_slot_type_map:
        if not self.is_vehicle_type_valid(vehicle_type):
            raise Exception (f"Vehicle type {vehicle_type} not recognized. Supported vehicles are:", vehicle_slot_type_map.keys())

        slot_type = self.get_slot_type(vehicle_type)
        vehicle_klass = self.vehicle_class_map[slot_type]

        return vehicle_klass(vehicle_type, lot)
