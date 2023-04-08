{
    "lot_config": {
        "stadium": {
                    "fee_model": "hourly",
                    "slots": {
                        "two_wheeler": 100,
                        "light_vehicle": 500,
                        "heavy_vehicle": 0
                    },
                    "rates" : {
                        "two_wheeler" : {
                            (0,  4): 30,
                            (4,  12): 60,
                            (12, None): 100
                        },
                        "light_vehicle" : {
                            (0, 4): 60,
                            (4, 12): 120,
                            (12, None): 200
                        }
                    },
        }
    }
}
