from lot.vehicle_slot import SlotType
from feemodel.fee_model_types import FeeModelTypes

default_config = {
    "lot_config": {
        "mall": {
                    "fee_model": FeeModelTypes.FLAT_HOURLY,
                    "slots": {
                        SlotType.TWO_WHEELER: 100,
                        SlotType.LV: 500,
                        SlotType.HV: 10
                    },
                    "rates" : {
                        SlotType.TWO_WHEELER : 10,
                        SlotType.LV : 20,
                        SlotType.HV : 100
                    },
        },
        "airport": {
                    "fee_model": FeeModelTypes.INTERVAL_DAILY,
                    "slots": {
                        SlotType.TWO_WHEELER: 100,
                        SlotType.LV: 500,
                        SlotType.HV: 0
                    },
                    "rates" : {
                        SlotType.TWO_WHEELER : {
                            (0,  4): 50,
                            (4,  7): 100,
                            (7,  12): 500,
                            (12, 24): 500,
                            (24, None): 1000
                        },
                        SlotType.LV : {
                            (0, 4): 150,
                            (4, 7): 600,
                            (7, 12): 1500,
                            (12, 24): 1800,
                            (24, None): 2000
                        },
                        SlotType.HV : {
                            (0, 4): 650,
                            (4, 7): 900,
                            (7, 12): 2500,
                            (12, 24): 3000,
                            (24, None): 4000
                        },
                    },

        },
        "stadium": {
            "fee_model": FeeModelTypes.INTERVAL_HOURLY,
            "slots": {
                SlotType.TWO_WHEELER: 100,
                SlotType.LV: 500,
                SlotType.HV: 10
            },
            "rates": {
                SlotType.TWO_WHEELER: {
                    (0, 4): 50,
                    (4, 7): 100,
                    (7, 12): 500,
                    (12, None): 600
                },
                SlotType.LV: {
                    (0, 4): 150,
                    (4, 7): 600,
                    (7, 12): 1500,
                    (12, None): 1800
                },
                SlotType.HV: {
                    (0, 4): 650,
                    (4, 11): 900,
                    (11, 14): 2500,
                    (14, None): 3000
                },
            },
        },
    }
}
