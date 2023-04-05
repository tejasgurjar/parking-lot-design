from enum import Enum


class FeeModelTypes(Enum):
    FLAT_HOURLY='flat_hourly'
    INTERVAL_HOURLY='interval_hourly'
    INTERVAL_DAILY='daily'