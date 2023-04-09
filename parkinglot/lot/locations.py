from enum import Enum
class Locations(Enum):
    AIRPORT="airport"
    MALL="mall"
    STADIUM="stadium"

    @classmethod
    def get_legal_values(cls):
        return [i.lower() for i in Locations.__members__]

