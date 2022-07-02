from ReservationsModule import Res, ResManager
from TimeUtilities import TimeRange
from GarageModule import GarageManager

class ReservationAPI():
    '''
    Static class for creating and manipulating reservations.
    
    Methods
    --------
    create_res(ID: str, owner: str, rRange: TimeRange) -> Res
        Create and save a new Res instance / file. Fill appropriate 
        timeslots in 'days'
    
    
    cancel_res
    
    '''