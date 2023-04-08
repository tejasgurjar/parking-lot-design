import datetime
import heapq
from lot.ticket import Ticket
from lot.receipt import Receipt
from lot.vehicle_slot import SlotType


class Lot(object):
    def __init__(self, fee_model, slot_capacity_cfg, place):
        self.fee_model = fee_model
        self.slot_capacity_cfg = slot_capacity_cfg
        self.next_ticket_number = 1

        self.slots = {
            SlotType.TWO_WHEELER : [],
            SlotType.LV: [],
            SlotType.HV : []
        }

        self.available_slots = {
            SlotType.TWO_WHEELER : list(range(self.get_slot_capacity(SlotType.TWO_WHEELER))),
            SlotType.LV: list(range(self.get_slot_capacity(SlotType.LV))),
            SlotType.HV: list(range(self.get_slot_capacity(SlotType.HV))),
        }

        self.available_slot_count = {
            SlotType.TWO_WHEELER : self.get_slot_capacity(SlotType.TWO_WHEELER),
            SlotType.LV : self.get_slot_capacity(SlotType.LV),
            SlotType.HV : self.get_slot_capacity(SlotType.HV)
        }

        self.tickets_created = dict()
        self.place = place

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
        if slot_type.value in self.slot_capacity_cfg:
            return self.slot_capacity_cfg[slot_type.value]
        else:
            return 0

    def generate_ticket(self, slot_type, vehicle, start_datetime):
        ticket_number = self.get_next_ticket_number()
        slot_number = self.get_next_available_slot(slot_type)
        ticket = Ticket(ticket_number,
                        slot_number,
                        slot_type,
                        vehicle,
                        self,
                        start_datetime)
        self.tickets_created[ticket.get_ticket_number_formatted()] = ticket
        return ticket

    def occupy_slot(self, slot_type, vehicle, start_datetime_string):
        num_available_slots = self.get_num_of_available_slots(slot_type)
        if num_available_slots > 0:
            self.available_slot_count[slot_type] -= 1
            start_datetime = Lot.get_datetime(start_datetime_string)
            ticket = self.generate_ticket(slot_type, vehicle, start_datetime)
            return ticket
        else:
            raise Exception("No space available")

    def is_parking_empty(self, slot_type):
        num_available_slots = self.get_num_of_available_slots(slot_type)
        max_slots = self.get_slot_capacity(slot_type)
        return num_available_slots == max_slots

    def calculate_fee(self, ticket, end_time):
        duration = end_time - ticket.start_datetime
        fee = self.fee_model.calculate_fee(duration, ticket.get_slot_type())
        return fee

    @classmethod
    def get_datetime(cls, time_string):
        try:
            return datetime.datetime.fromisoformat(time_string)
        except Exception as e:
            print("Invalid time string specified: " + time_string + ".Error: " + str(e))
            raise

    def free_slot(self, ticket, end_time_string):
        slot_type = ticket.get_slot_type()
        if self.is_parking_empty(slot_type):
            raise Exception("Parking slot capacity for type " + slot_type + " already at max capacity")

        self.available_slot_count[slot_type] += 1

        end_time = Lot.get_datetime(end_time_string)
        fee = self.calculate_fee(ticket, end_time)

        # Add slot back to available pool
        heapq.heappush(self.available_slots[slot_type], ticket.id)
        return Receipt(ticket, end_time, fee)
