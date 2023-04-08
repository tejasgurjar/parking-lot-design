class Receipt(object):
    def __init__(self, ticket, end_time, fee):
        self.ticket = ticket
        self.fee = fee
        self.end_datetime = end_time

    def format_ticket_number(self):
        return "-".join(["R", self.ticket.get_ticket_number()])

    def get_slot_type(self):
        return self.slot_type

    def print(self):
        print("Receipt: " + self.format_ticket_number())
        print("  Parking Lot:" + self.ticket.lot.get_location())
        print("  Vehicle Type: " + self.ticket.vehicle)
        print("  Entry date time:" + self.ticket.start_datetime.isoformat())
        print("  Exit date time:" + self.end_datetime.isoformat())
        print("  Fee: " + str(self.fee))


