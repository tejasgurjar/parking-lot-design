from abc import ABC, abstractmethod


class Vehicle(ABC):
    def park(self, datetime_string):
        ticket = self.lot.occupy_slot(self.slot_type, self.vehicle_type, datetime_string)
        return ticket

    def unpark(self, ticket, datetime_string):
        receipt = self.lot.free_slot(ticket, datetime_string)
        return receipt

    def set_ticket_number(self, ticket_number):
        self.ticket_number = ticket_number

    def get_slot_type(self):
        return self.slot_type