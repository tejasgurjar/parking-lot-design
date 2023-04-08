from enum import Enum


class FeeModelTypes(Enum):
    FLAT_HOURLY='flat_hourly'
    INTERVAL_HOURLY='hourly'
    INTERVAL_DAILY='daily'
