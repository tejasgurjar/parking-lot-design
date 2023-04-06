import os
from enum import Enum
from lot.lot import Lot
from feemodel.fee_model_types import FeeModelTypes
from feemodel.flat_fee_model import FlatFeeModel, FlatHourlyFeeModel
from feemodel.interval_fee_model import IntervalHourlyFeeModel
from feemodel.daily_fee_model import DailyFeeModel


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
        FeeModelTypes.FLAT_HOURLY.value: FlatHourlyFeeModel(),
        FeeModelTypes.INTERVAL_HOURLY.value: IntervalHourlyFeeModel(),
        FeeModelTypes.INTERVAL_DAILY.value: DailyFeeModel()
     }
    )

    def __init__(self, config):
        self.config = config

    @classmethod
    def load_config(cls, configfilepath):
        if not os.path.exists(configfilepath):
            raise Exception("Parking lot config file " + configfilepath + " does not exist")
        try:
            cfg_code = []
            with open(configfilepath, "r") as cfg:
                #cfg_obj = json.load(cfg)
                for code_line in cfg.readlines():
                    cfg_code.append(code_line)
            cfg_obj = eval("".join(cfg_code))
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

    def get_fee_model(self, place):
        if place in self.config["lot_config"]:
            fee_model_type = self.config["lot_config"][place]["fee_model"]
            fee_model = self.fee_model_map[fee_model_type.lower()]
            fee_model.set_rate(self.config["lot_config"][place]["rates"])
            return fee_model
        else:
            raise Exception("Invalid place specified:" + place + " Legal places are:" + Places.get_legal_values())

    def get_parking_lot(self, place):
        lot = Lot(self.get_fee_model(place),
                  self.config["lot_config"][place]["slots"],
                  place=place)
        return lot
