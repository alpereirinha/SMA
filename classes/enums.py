from enum import Enum

class PlaneState(Enum):
    FLYING = 0
    LANDED = 1

class PlaneType(Enum):
    SHIPPING = 0
    PASSENGERS = 1

class Action(Enum):
    LANDING = 0
    TAKEOFF = 1
    MULTI = 2 # for runways that do landings and takeoffs