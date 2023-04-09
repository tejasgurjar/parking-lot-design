import json
from enum import Enum
from constants import *
from vehicle.vehicle_factory import VehicleFactory
class Action(Enum):
    PARK="park"
    UNPARK="unpark"


class Activity(object):
    def __init__(self, action, vehicle, datetime_string):
        self.action = action
        self.vehicle = vehicle
        self.datetime_string = datetime_string


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
        vehicle_factory = VehicleFactory.get_instance()
        assert vehicle_factory.is_vehicle_type_valid(vehicle.lower()), \
                                 "Illegal vehicle type: " + vehicle + \
                                  "must be one of " + ",".join(vehicle_factory.get_valid_vehicles())

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

        if LOCATION not in self.config:
            raise Exception(LOCATION + " not specified: Specify one of ", Locations.get_legal_values())

        common_mandatory_params = [ACTION, VEHICLE, DATETIME]
        errors = list()

        for act_id, activity in enumerate(self.config[ACTIVITY]):
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
        return self.config[ACTIVITY]


    def get_location(self):
        return self.config[LOCATION]

