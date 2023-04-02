from lot.vehicle_slot import SlotType
from feemodel.fee_model_types import FeeModelTypes

default_config = {
    "lot_config": {
        "mall": {
                    "fee_model": FeeModelTypes.FLAT_HOURLY,
                    "slots": {
                        SlotType.TWO_WHEELER: 100,
                        SlotType.LMV: 500,
                        SlotType.HV: 10
                    },
                    "rates" : {
                        SlotType.TWO_WHEELER : 10,
                        SlotType.LMV : 20,
                        SlotType.HV : 100
                    },
        },
        "airport": {
                    "fee_model": FeeModelTypes.INTERVAL_DAILY,
                    "slots": {
                        SlotType.TWO_WHEELER: 100,
                        SlotType.LMV: 500,
                        SlotType.HV: 10
                    },
                    "rates" : {
                        SlotType.TWO_WHEELER : {
                            (0,  4): 50,
                            (5,  7): 100,
                            (8,  12): 500,
                            (13, 23): 500,
                            (24, None): 1000,
                        },
                        SlotType.LMV : {
                            (0, 4): 150,
                            (5, 7): 600,
                            (8, 12): 1500,
                            (13, 23): 1800,
                            (24, None): 2000,
                        },
                        SlotType.HV : {
                            (0, 4): 650,
                            (5, 7): 900,
                            (8, 12): 2500,
                            (13, 23): 3000,
                            (24, None): 4000,
                        },
                    },

        },
        "stadium": {
            "fee_model": FeeModelTypes.INTERVAL_HOURLY,
            "slots": {
                SlotType.TWO_WHEELER: 100,
                SlotType.LMV: 500,
                SlotType.HV: 10
            },
            "rates": {
                SlotType.TWO_WHEELER: {
                    (0, 4): 50,
                    (5, 7): 100,
                    (8, 12): 500
                },
                SlotType.LMV: {
                    (0, 4): 150,
                    (5, 7): 600,
                    (8, 12): 1500
                },
                SlotType.HV: {
                    (0, 4): 650,
                    (5, 7): 900,
                    (8, 12): 2500
                },
            },
        },
    }
}
