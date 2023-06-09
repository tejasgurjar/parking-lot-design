{
    "lot_config": {

        "airport": {
                    "fee_model": "daily",
                    "slots": {
                        "two_wheeler": 100,
                        "light_vehicle": 500,
                        "heavy_vehicle": 0
                    },
                    "rates" : {
                        "two_wheeler" : {
                            (0,  1): 0,
                            (1,  8): 40,
                            (8, 24): 60,
                            (24, None): 80
                        },
                        "light_vehicle" : {
                            (0, 12): 60,
                            (12, 24): 80,
                            (24, None): 100
                        },
                    },
        }
    }
}
