import os
import json
from enum import Enum
from lot.lot import Lot
from feemodel.fee_model_types import FeeModelTypes
from feemodel.flat_fee_model import FlatFeeModel
from feemodel.interval_fee_model import IntervalFeeModel


class Places(Enum):
    AIRPORT="airport"
    MALL="mall"
    STADIUM="stadium"

    @classmethod
    def get_legal_values(cls):
        return [i for i in Places.__members__]


class LotFactory(object):
    factory_instance = None
    fee_model_map = dict({
        FeeModelTypes.FLAT_HOURLY: FlatFeeModel(),
        FeeModelTypes.INTERVAL_HOURLY: IntervalHourlyFeeModel(),
        FeeModelTypes.INTERVAL_DAILY: IntervalDailyFeeModel()
     }
    )

    def __init__(self, config):
        self.config = config

    @classmethod
    def load_config(cls, configfilepath):
        if not os.path.exists(configfilepath):
            raise Exception("Parking lot config file " + configfilepath + " does not exist")
        try:
            with open(configfilepath, "r") as cfg:
                cfg_obj = json.load(cfg)
        except Exception as e:
            print("Error reading parking lot configuration file " + configfilepath + " error: " + str(e))
            raise
        else:
            return cfg_obj

    @classmethod
    def get_instance(cls, configfilepath):
        if cls.factory_instance is None:
            config = LotFactory.load_config(configfilepath)
            cls.factory_instance = LotFactory(config)

        return cls.factory_instance

    @classmethod
    def get_fee_model(cls, place):
        if place in cls.config["lot_config"]:
            fee_model_type = cls.config["lot_config"][place]["model"]
            fee_model = LotFactory.fee_model_map[fee_model_type]
            fee_model.set_rate(cls.config["lot_config"][place]["rates"])
        else:
            raise Exception("Invalid place specified:" + place + " Legal places are:" + Places.get_legal_values())

    @classmethod
    def get_parking_lot(cls, place):
        lot = Lot(cls.get_fee_model(place),
                  cls.config[place]["slots"])
        return lot
