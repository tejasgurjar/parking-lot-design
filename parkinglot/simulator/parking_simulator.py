import json
import datetime

from enum import Enum
from config.vehicle_slot_type_cfg import *
from lot.ticket import Ticket
from constants import *


class Action(Enum):
    PARK="park"
    UNPARK="unpark"


class Activity(object):
    def __init__(self, action, vehicle, datetime_string):
        self.action = action
        self.vehicle = vehicle
        self.datetime_string = datetime_string


class Park(Activity):
    def __init__(self, action, vehicle, datetime_string):
        super().__init__(action, vehicle, datetime_string)

    def do(self, parking_space, tickets):
        slot_type = vehicle_slot_type_map[self.vehicle]
        ticket = parking_space.occupy_slot(slot_type,
                                           self.vehicle,
                                           self.datetime_string)
        tickets[ticket.get_ticket_number_formatted()] = ticket
        ticket.print()


class UnPark(Activity):
    def __init__(self, action, vehicle, datetime_string):
        super().__init__(action, vehicle, datetime_string)
        self.ticket_id = None

    def set_ticket_id(self, tkt_id):
        self.ticket_id = tkt_id

    def do(self, parking_space, tickets):
        slot_type = vehicle_slot_type_map[self.vehicle]
        ticket_number = Ticket.create_formatted_ticket_number(int(self.ticket_id))
        if ticket_number in tickets:
            receipt = parking_space.free_slot(tickets[ticket_number],
                                              self.datetime_string)
            receipt.print()
        else:
            raise Exception(f"Ticket number {ticket_number} was never allotted")


class ActivityConfig(object):
    def __init__(self, configfilepath):
        self.configfilepath = configfilepath
        self.config = self.load(configfilepath)
        try:
            self.validate()
        except Exception as e:
            msg = f"Invalid activity configuration provided: {str(e)}"
            raise Exception(msg)

    @classmethod
    def load(cls, configfilepath):
        try:
            with open(configfilepath, "r") as cfg:
                activity_cfg = json.load(cfg)
            return activity_cfg
        except Exception as e:
            print("Could not load activity config from file:" + configfilepath + ":" + str(e))
            raise

    @classmethod
    def validate_action(cls, action):
        if action.upper() not in Action.__members__:
            err_msg = "Illegal action value: " + action + \
                      " must be one of " + ",".join(["'" + i.lower() + "'" for i in Action.__members__])
            raise Exception(err_msg)
        return True


    @classmethod
    def validate_vehicle(cls, vehicle):
        assert vehicle.lower() in vehicle_slot_type_map, \
                                 "Illegal vehicle type: " + vehicle + \
                                  "must be one of " + "".join(vehicle_slot_type_map.keys())

    @classmethod
    def validate_datetime(cls, datetimestring):
        try:
            datetime.datetime.fromisoformat(datetimestring)
            return True
        except Exception as e:
            msg = f"Activity timestamp {datetimestring} is not in expected ISO format i.e. YYYY-MM-DD HH:MM:SS"
            print(msg)
            return False

    def validate(self):
        common_mandatory_params = [ACTION, VEHICLE, DATETIME]
        errors = list()

        for act_id, activity in enumerate(self.config):
            mandatory_params = common_mandatory_params[:]

            if activity[ACTION].lower() == Action.UNPARK.value:
                mandatory_params.append(TICKET_ID)

            for mandatory_param in mandatory_params:
                if mandatory_param not in activity:
                    err_msg = f"Activity {act_id} needs to have '" + mandatory_param + "' keyword specified"
                    errors.append(err_msg)
            try:
                ActivityConfig.validate_action(activity[ACTION])
            except Exception as e:
                errors.append(str(e))

            try:
                ActivityConfig.validate_vehicle(activity[VEHICLE])
            except Exception as e:
                errors.append(str(e))

            try:
                ActivityConfig.validate_datetime(activity[DATETIME])
            except Exception as e:
                errors.append(str(e))

        if errors:
            raise Exception("Invalid activity config: " + "\n".join(errors))

    def get_activity(self):
        activity_objs = []

        for act_cfg in self.config:
            if act_cfg[ACTION].lower() == Action.PARK.value:
                activity_objs.append(Park(act_cfg[ACTION],
                                          act_cfg[VEHICLE],
                                          act_cfg[DATETIME]))

            elif act_cfg[ACTION].lower() == Action.UNPARK.value:
                activity_obj = UnPark(act_cfg[ACTION],
                                      act_cfg[VEHICLE],
                                      act_cfg[DATETIME])
                activity_obj.set_ticket_id(act_cfg[TICKET_ID])
                activity_objs.append(activity_obj)
        return activity_objs


class ParkingSimulator(object):
    def __init__(self, lot, activity_config_filepath):
        self.lot = lot

        activity_config = ActivityConfig(activity_config_filepath)
        activity_config.validate()
        self.activities = activity_config.get_activity()

    def simulate(self):
        tickets = dict()

        for activity in self.activities:
            activity.do(self.lot, tickets)



