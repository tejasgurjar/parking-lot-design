{
    "lot_config": {
        "mall": {
                    "fee_model": "flat_hourly",
                    "slots": {
                        "two_wheeler": 100,
                        "light_vehicle": 500,
                        "heavy_vehicle": 10
                    },
                    "rates" : {
                        "two_wheeler" : 10,
                        "light_vehicle" : 20,
                        "heavy_vehicle" : 100
                    },
        },
        "airport": {
                    "fee_model": "daily",
                    "slots": {
                        "two_wheeler": 100,
                        "light_vehicle": 500,
                        "heavy_vehicle": 10
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
                        "heavy_vehicle" : {
                            (0, 4): 650,
                            (4, 7): 900,
                            (7, 12): 2500,
                            (12, 24): 3000,
                            (24, None): 4000
                        },
                    },
        }
    }
}
