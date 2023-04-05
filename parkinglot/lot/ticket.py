class Ticket(object):
    def __init__(self, id, slot_id, slot_type, vehicle, lot, entry_datetime):
        self.id = id
        self.slot_id = slot_id
        self.slot_number = "-".join(["S", "%5d" % (slot_id)])
        self.ticket_number = Ticket.format_ticket_number(slot_type, id)
        self.vehicle = vehicle
        self.slot_type = slot_type
        self.lot = lot
        self.start_datetime = entry_datetime
        self.end_datetime = None
        self.paid_status = False

    @classmethod
    def format_ticket_number(cls, slot_type, id):
        return "-".join(["T", slot_type.value,  "%06d" % (id)])


    def get_slot_type(self):
        return self.slot_type

    def print(self):
        print("Date: " + self.end_datetime)
        print("Parking Lot:" + self.lot)
        print("Vehicle Type: " + self.vehicle)
        print("Entry date time:" + self.start_datetime)

