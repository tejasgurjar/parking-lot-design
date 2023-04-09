Usage
-----
%>python3 parkinglot.py <activity json> [parking lot .py cfg]

Sample activity json file
-------------------------
{
    "location": "mall",
    "activity": [
        {
            "action": "park",
            "vehicle": "motorcycle",
            "datetime": "2022-04-01 13:00:01"
        },
        {
            "action": "park",
            "vehicle": "motorcycle",
            "datetime": "2022-04-01 13:10:34"
        },
        {
            "action": "unpark",
            "vehicle": "motorcycle",
            "datetime": "2022-04-01 16:30:01",
            "ticket_id": "1"
        },
        {
            "action": "unpark",
            "vehicle": "motorcycle",
            "datetime": "2022-04-01 19:06:12",
            "ticket_id": "2"
        },
    ]
}

Sample parking lot cfg
----------------------
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
                        "heavy_vehicle" : 50
                    },
        }
    }
}



To run unit tests
-----------------
%>python -m unittest discover


For code coverage
-----------------
%>coverage run -m unittest discover
%>coverage report -m

Coverage report with existing set of unit tests is included in coverage.txt
