from enum import Enum
from lot.ticket import Ticket
import datetime


class Status(Enum):
    VACANT = 0
    OCCUPIED = 1

class SlotType(Enum):
    TWO_WHEELER = "two_wheeler"
    LMV = "light_motor_vehicle"
    HV = "heavy_vehicle"


class VehicleSlot():
    def __init__(self, lot, slot_type):
        self.lot = lot
        self.slot_type = slot_type
        self.status = Status.VACANT

    def occupy(self, start_datetime):
        self.status = Status.OCCUPIED
        return self.generate_ticket(start_datetime)

    def free(self):
        self.status = Status.VACANT
