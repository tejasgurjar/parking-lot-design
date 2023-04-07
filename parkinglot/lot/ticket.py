class Ticket(object):
    def __init__(self, id, slot_id, slot_type, vehicle, lot, entry_datetime):
        self.id = id
        self.slot_id = slot_id
        self.slot_number_formatted = Ticket.create_formatted_slot_number(slot_id)
        self.ticket_number_formatted = Ticket.create_formatted_ticket_number(slot_type, id)
        self.vehicle = vehicle
        self.slot_type = slot_type
        self.lot = lot
        self.start_datetime = entry_datetime
        self.end_datetime = None
        self.paid_status = False

    def get_ticket_number_formatted(self):
        return self.ticket_number_formatted

    @classmethod
    def create_formatted_slot_number(cls, slot_id):
        return "-".join(["S", "%5d" % slot_id])

    @classmethod
    def _get_ticket_number(cls, slot_type, id):
        return "-".join([slot_type.value,  "%06d" % id])

    @classmethod
    def create_formatted_ticket_number(cls, slot_type, id):
        return "-".join(["T", cls._get_ticket_number(slot_type, id)])

    def get_slot_type(self):
        return self.slot_type

    def print(self):
        print("Ticket:" + self.ticket_number_formatted)
        print("  Parking Lot:" + self.lot.place)
        print("  Slot number:" + self.slot_number_formatted)
        print("  Vehicle Type: " + self.vehicle)
        print("  Entry date time:" + self.start_datetime.isoformat())
