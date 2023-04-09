class Ticket(object):
    def __init__(self, id, slot_id, slot_type, vehicle, lot, entry_datetime):
        self.id = id
        self.slot_id = slot_id
        self.slot_number_formatted = Ticket.create_formatted_slot_number(slot_type.name, slot_id)
        self.ticket_number = Ticket._get_ticket_number(id)
        self.ticket_number_formatted = Ticket.create_formatted_ticket_number(id)
        self.vehicle = vehicle
        self.slot_type = slot_type
        self.lot = lot
        self.start_datetime = entry_datetime
        self.end_datetime = None
        self.paid_status = False

    def get_ticket_number_formatted(self):
        return self.ticket_number_formatted

    @classmethod
    def create_formatted_slot_number(cls, slot_type, slot_id):
        return "-".join(["S", slot_type, "%05d" % slot_id])

    @classmethod
    def _get_ticket_number(cls, id):
        return "-".join(["%06d" % id])

    @classmethod
    def create_formatted_ticket_number(cls, id):
        return "-".join(["T", cls._get_ticket_number(id)])

    def get_slot_type(self):
        return self.slot_type

    def get_ticket_number(self):
        return self.ticket_number

    def print(self):
        print("Ticket:" + self.ticket_number_formatted)
        print("  Parking Lot:" + self.lot.get_location())
        print("  Slot number:" + self.slot_number_formatted)
        print("  Vehicle Type: " + self.vehicle)
        print("  Entry date time:" + self.start_datetime.isoformat())
