import datetime
import heapq
from enum import Enum
from lot.vehicle_slot import VehicleSlot
from lot.ticket import Ticket


from lot.vehicle_slot import SlotType


class Lot(object):
    def __init__(self, fee_model, slot_capacity_cfg):
        self.fee_model = fee_model
        self.slot_capacity_cfg = slot_capacity_cfg
        self.next_ticket_number = 1

        self.slots = {
            SlotType.TWO_WHEELER : [],
            SlotType.LMV: [],
            SlotType.HV : []
        }

        self.available_slots = {
            SlotType.TWO_WHEELER : heapq.heapify(list(range(self.get_slot_capacity(SlotType.TWO_WHEELER)))),
            SlotType.LMV: heapq.heapify(list(range(self.get_slot_capacity(SlotType.LMV)))),
            SlotType.HV: heapq.heapify(list(range(self.get_slot_capacity(SlotType.HV)))),
        }

        self.available_slot_count = {
            SlotType.TWO_WHEELER : self.get_slot_capacity(SlotType.TWO_WHEELER),
            SlotType.LMV : self.get_slot_capacity(SlotType.LMV),
            SlotType.HV : self.get_slot_capacity(SlotType.HV)
        }

        self.tickets_created = dict()

    def increment_ticket_number(self):
        self.next_ticket_number += 1

    def get_fee_model(self):
        return self.fee_model

    def get_next_ticket_number(self):
        ticket_number = self.next_ticket_number
        self.increment_ticket_number()
        return ticket_number

    def get_next_available_slot(self, slot_type):
        if slot_type in self.available_slots and self.available_slots[slot_type]:
            return heapq.heappop(self.available_slots[slot_type])

    def get_num_of_available_slots(self, slot_type):
        return self.available_slot_count[slot_type]

    def get_slot_capacity(self, slot_type):
        return self.slot_capacity_cfg[slot_type]

    def generate_ticket(self, start_datetime):
        ticket_number = self.get_next_ticket_number()
        slot_number = self.get_next_available_slot(self.slot_type)
        ticket = Ticket(ticket_number,
                        slot_number,
                        self.slot_type,
                        self.lot.get_fee_model(),
                        datetime.datetime.fromisoformat(start_datetime))
        self.tickets_created[ticket.ticket_number] = ticket
        return ticket

    def occupy_slot(self, slot_type, start_datetime_string):
        num_available_slots = self.get_num_of_available_slots(slot_type)
        if num_available_slots > 0:
            #slot = VehicleSlot(self, slot_type)
            self.available_slot_count[slot_type] -= 1
            start_datetime = Lot.get_datetime(start_datetime_string)
            ticket = self.generate_ticket(start_datetime)
            return ticket
        else:
            raise Exception("No more slots available")

    def is_parking_empty(self, slot_type):
        num_available_slots = self.get_num_of_available_slots(slot_type)
        max_slots = self.get_slot_capacity()
        return num_available_slots == max_slots

    def calculate_fee(self, ticket, end_time):
        fee_model = ticket.lot.get_fee_model()
        duration = end_time - ticket.start_datetime
        fee = fee_model.calculate_fee(duration, self, ticket.get_slot_type())
        print("Fee: " + fee)

    @classmethod
    def get_datetime(cls, time_string):
        try:
            return datetime.datetime.fromisoformat(time_string)
        except Exception as e:
            print("Invalid time string specified: " + time_string + ".Error: " + str(e))
            raise

    def free_slot(self, ticket, end_time_string):
        slot_type = ticket.lot.get_slot_type()
        if self.is_parking_empty(slot_type):
            raise Exception("Parking slot capacity for type " + slot_type + " already at max capacity")

        self.available_slot_count[slot_type] += 1

        end_time = Lot.get_datetime(end_time_string)
        fee = self.calculate_fee(ticket, end_time)

        # Add slot back to available pool
        heapq.heappush(self.available_slots[slot_type], ticket.id)

        print(ticket.ticket_number + "\n")
        print("Parking entry:", ticket.start_datetime)
        print("Parking exit:", ticket.end_datetime)
        print("Fee: ", fee, "\n")