{
    "lot_config": {
        "stadium": {
                    "fee_model": "hourly",
                    "slots": {
                        "two_wheeler": 5,
                        "light_vehicle": 3,
                        "heavy_vehicle": 1
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
