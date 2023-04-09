from lot.ticket import Ticket
from constants import *
from vehicle.vehicle_factory import VehicleFactory
from simulator.activity import Action


class ParkingSimulator(object):
    def __init__(self, lot, activity_config):
        self.lot = lot
        self.vehicleFactory = VehicleFactory.get_instance()
        self.activities = activity_config.get_activity()
        self.vehicles = dict()
        self.tickets = dict()

    def simulate(self):
        for activity in self.activities:
            vehicle_type = activity[VEHICLE]
            datetime_string = activity[DATETIME]

            if activity[ACTION] == Action.PARK.value:
                vhc = self.vehicleFactory.get_vehicle(vehicle_type, self.lot)

                ticket = vhc.park(datetime_string)
                ticket_number = ticket.get_ticket_number_formatted()
                self.tickets[ticket_number] = ticket
                self.vehicles[ticket_number] = vhc
                ticket.print()
            elif activity[ACTION] == Action.UNPARK.value:
                ticket_id = activity[TICKET_ID]
                ticket_number = Ticket.create_formatted_ticket_number(int(ticket_id))
                if ticket_number in self.tickets:
                    vhc = self.vehicles[ticket_number]
                    receipt = vhc.unpark(self.tickets[ticket_number], datetime_string)
                    receipt.print()
                else:
                    raise Exception(f"Ticket number {ticket_number} was never allotted")



