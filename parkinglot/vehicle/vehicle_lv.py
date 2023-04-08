from vehicle.vehicle import Vehicle
from lot.vehicle_slot import SlotType


class VehicleLV(Vehicle):
    def __init__(self, vehicle_type, lot):
        self.ticket_number = None
        self.vehicle_type = vehicle_type
        self.lot = lot
        self.slot_type = SlotType.LV