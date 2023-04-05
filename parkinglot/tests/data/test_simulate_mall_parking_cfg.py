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
                    "fee_model": "crazy_expensive",
                    "slots": {
                        "two_wheeler": 100,
                        "light_vehicle": 500,
                        "heavy_vehicle": 10
                    },
                    "rates" : {
                        "two_wheeler" : {
                            (0,  4): 50,
                            (4,  7): 100,
                            (7,  12): 500,
                            (12, 24): 500,
                            (24, None): 1000
                        },
                        "light_vehicle" : {
                            (0, 4): 150,
                            (4, 7): 600,
                            (7, 12): 1500,
                            (12, 24): 1800,
                            (24, None): 2000
                        },
                        "heavy_vehicle" : {
                            (0, 4): 650,
                            (4, 7): 900,
                            (7, 12): 2500,
                            (12, 24): 3000,
                            (24, None): 4000
                        },
                    },
        },
        "stadium": {
            "fee_model": "tres_cher",
            "slots": {
                "two_wheeler": 100,
                "light_vehicle": 500,
                "heavy_vehicle": 10
            },
            "rates": {
                "two_wheeler": {
                    (0, 4): 50,
                    (4, 7): 100,
                    (7, 12): 500,
                    (12, None): 600
                },
                "light_vehicle": {
                    (0, 4): 150,
                    (4, 7): 600,
                    (7, 12): 1500,
                    (12, None): 1800
                },
                "heavy_vehicle": {
                    (0, 4): 650,
                    (4, 11): 900,
                    (11, 14): 2500,
                    (14, None): 3000
                },
            },
        },
    }
}
