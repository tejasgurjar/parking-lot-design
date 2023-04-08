{
    "lot_config": {
        "mall": {
            "fee_model": "flat_hourly",
            "slots": {
                "two_wheeler": 100,
                "light_vehicle": 500,
                "heavy_vehicle": 10
            },
            "rates": {
                "two_wheeler": 10,
                "light_vehicle": 20,
                "heavy_vehicle": 50
            },
        },
        "stadium": {
            "fee_model": "hourly",
            "slots": {
                "two_wheeler": 1000,
                "light_vehicle": 1500,
                "heavy_vehicle": 0
            },
            "rates": {
                "two_wheeler": {
                    (0, 4): 30,
                    (4, 12): 60,
                    (12, None): 100
                },
                "light_vehicle": {
                    (0, 4): 60,
                    (4, 12): 120,
                    (12, None): 200
                }
            },
        },
        "airport": {
            "fee_model": "daily",
            "slots": {
                "two_wheeler": 200,
                "light_vehicle": 500,
                "heavy_vehicle": 0
            },
            "rates": {
                "two_wheeler": {
                    (0, 1): 0,
                    (1, 8): 40,
                    (8, 24): 60,
                    (24, None): 80
                },
                "light_vehicle": {
                    (0, 12): 60,
                    (12, 24): 80,
                    (24, None): 100
                },
            },
        }
    }
}


