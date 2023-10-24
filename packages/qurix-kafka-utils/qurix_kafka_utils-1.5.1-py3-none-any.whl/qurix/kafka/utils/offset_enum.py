from enum import Enum


class Offset(Enum):
    EARLIEST = "earliest"
    LATEST = "latest"
    LAST = "last"
    EXPLICIT = "exlipicit"
    TIMESTAMP = "timestamp"
