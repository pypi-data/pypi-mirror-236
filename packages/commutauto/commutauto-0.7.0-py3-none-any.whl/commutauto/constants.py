from enum import Enum
from typing import Union

MINIMUM_SEARCH_RADIUS_KM = 0.3
# NOTE: shorter wait time for flex than for stations
# as the search is more time critical
FLEX_BASE_WAIT_TIME_SECOND=45 # 45 seconds
FLEX_WAIT_TIME_JITTER_SECOND=30 # 0 seconds
FLEX_EXPIRATION_TIME_SECOND=1*60*60 # 1 hour
MAX_FLEX_EXPIRATION_TIME_SECOND=3*60*60 # No more than 3 hours

STATION_BASE_WAIT_TIME_SECOND=2*60 # 2 minutes
STATION_WAIT_TIME_JITTER_SECOND=3*60 # 3 minutes
STATION_EXPIRATION_TIME_SECOND=1*24*60*60 # 1 day
MAX_STATION_EXPIRATION_TIME_SECOND=7*24*60*60 # No more than a week

class CommutautoEndpoint(Enum):
    ASP = "https://www.reservauto.net/Scripts/Client/Ajax/MobileApplication/Communauto/"
    LSI = "https://www.reservauto.net/WCF/LSI/LSIBookingServiceV3.svc/"

class AspScript(Enum):
    GET_CAR_DISPONIBILITY= "Get_Car_DisponibilityJSON.asp"
    BOOK_CAR = "ReservationAdd.asp"
    GET_BOOKING = "Get_Reservation.asp"
    GET_BOOKING_LIST = "ReservationList.asp"
    CANCEL_BOOKING= "ReservationModify.asp"

class LSIRoute(Enum):
    GET_FLEX_DISPONIBILITY= "GetAvailableVehicles"
    BOOK_FLEX = "CreateBookingPost"
    CANCEL_BOOKING_FLEX= "CancelBookingPost"
    GET_CURRENT_FLEX= "GetCurrentBooking"


MAP_ROUTE_ENDPOINT = {
    AspScript: CommutautoEndpoint.ASP,
    LSIRoute: CommutautoEndpoint.LSI
}

EnumRouteType = Union[AspScript, LSIRoute]


class Cities(Enum):
    MONTREAL = 59
    QUEBEC = 90
    SHERBROOKE = 89
    TROIS_RIVIERES = 110
    GATINEAU = 94
    OTTAWA = 93
    KINGSTON = 97
    SW_ONTARIO = 103
    TORONTO = 105
    HALIFAX = 92
    PARIS = 96
    EDMONTON = 106
    CALGARY = 107

CITIES_MAPPING_STR_ENUM = {
    "montreal": Cities.MONTREAL,
    "quebec": Cities.QUEBEC,
    "sherbrooke": Cities.SHERBROOKE,
    "trois_rivieres": Cities.TROIS_RIVIERES,
    "gatineau": Cities.GATINEAU,
    "ottawa": Cities.OTTAWA,
    "kingston": Cities.KINGSTON,
    "sw_ontario": Cities.SW_ONTARIO,
    "toronto": Cities.TORONTO,
    "halifax": Cities.HALIFAX,
    "paris": Cities.PARIS,
    "edmonton": Cities.EDMONTON,
    "calgary": Cities.CALGARY
}

class Branches(Enum):
    QUEBEC = 1
    ONTARIO = 2
    NOVA_SCOTIA = 3
    FRANCE = 4
    ALBERTA = 10

CitiesToBranchesMapping = {
    Cities.MONTREAL: Branches.QUEBEC,
    Cities.QUEBEC: Branches.QUEBEC,
    Cities.SHERBROOKE: Branches.QUEBEC,
    Cities.TROIS_RIVIERES: Branches.QUEBEC,
    Cities.GATINEAU: Branches.QUEBEC,
    Cities.OTTAWA: Branches.ONTARIO,
    Cities.KINGSTON: Branches.ONTARIO,
    Cities.SW_ONTARIO: Branches.ONTARIO,
    Cities.TORONTO: Branches.ONTARIO,
    Cities.HALIFAX: Branches.NOVA_SCOTIA,
    Cities.PARIS: Branches.FRANCE,
    Cities.EDMONTON: Branches.ALBERTA,
    Cities.CALGARY: Branches.ALBERTA
}

class CarSizes(Enum):
    COMPACT = 1
    MID_SIZE = 2
    FAMILY_CAR = 3
    UNKNOWN = 4

SIZES_MAPPING_STR_ENUM = {
    "compact": CarSizes.COMPACT,
    "midsize": CarSizes.MID_SIZE,
    "family": CarSizes.FAMILY_CAR
}