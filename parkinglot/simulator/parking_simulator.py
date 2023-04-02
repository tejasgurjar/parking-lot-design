from enum import Enum
from config.vehicle_slot_type.cfg import vehicle_slot_type_map


class Action(Enum):
    PARK="park"
    UNPARK="unpark"


class ParkingSimulator(object):
    def __init__(self, lot, activity_cfg):
        self.lot = lot
        self.activity_cfg = activity_cfg

    def simulate(self):
        tickets = dict()
        for e in self.activity_cfg:
            slot_type = vehicle_slot_type_map[e.vehicle]

            if e.action == Action.PARK.value:
                ticket = self.lot.occupy_slot(slot_type,
                                              e.datetime_string)
                tickets[ticket.ticket_number] = ticket
            elif e.action == Action.UNPARK.value:
                ticket_number = "-".join(["T", slot_type, str(e.slot_id)])
                self.lot.free_slot(tickets[ticket_number], e.datetime_string)

