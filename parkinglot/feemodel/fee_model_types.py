from enum import Enum

class FeeModelTypes(Enum):
    FLAT_HOURLY=1
    INTERVAL_HOURLY=2
    INTERVAL_DAILY=3