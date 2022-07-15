import os
from ReservationsModule import Res, ResManager
from TimeUtilities import TimeRange
from GarageModule import GarageManager, Day, DaysIntiliazed

class ReservationAPI():
    '''
    Static class for creating and manipulating reservations.
    
    Methods
    --------
    attempt_create_res(ID: str, owner: str, day: int, rRange: TimeRange) -> Res
        Create and save a new Res instance / file. Fill appropriate 
        timeslots in 'days'
    
    query_res_exists(ID: str) -> bool:
        Query if the reservation exists.
    
    cancel_res(ID: str) -> None
        Remove the specified reservation from time slots & change active
        attribute in files.
    
    findLift(ID: str) -> int
        Find the lift in which a reservation has been placed. 
        
    get_res(ID: str) -> Res
        Return the reservation instance corresponding to ID.
        
    cancel_res(ID: str) -> None
        Set the active attribute of the reservation to False. Remove res ID
        from time slots.
        
    query_modify_res(ID: str, new_d: int, new_tRange: TimeRange) -> bool:
        Checks if possible to set a reservation's day and time range 
        to the new ranges. Returns true/false
        
    attempt_modify_res(ID: str, new_d: int, new_tRange: TimeRange) -> bool:
        Attempts to modify the reservation to the new day & times. Saves
        files. Returns true if successful
    
    get_day_from_file(day_ID: str) -> Day
        Load & initialize a day object from its corresponding file.
        
    list_days_initialized() -> list
        List the day files that have been initialized.
    
    query_if_available(day, tRange):
        Check if a time range is available on a certain day.
    
    '''
    @staticmethod
    def attempt_create_res(ID: str, owner: str, day: int, tRange: TimeRange, filename=None) -> bool:
        '''
        Create and save a new Res instance / file. Fill appropriate 
        timeslots in 'days'. Add that reservation to appropriate account
        
        Paramters
        ----------
        ID : str
            Unique ID of reservation
            
        owner : str 
            Username of owner/creator of reservation.
        
        day : int
            Which day does the reservation occupy
        
        tRange : TimeRange
            Time range spanned by new reservation.
        
        filename : str (optional)
            Optional filepath of the reservation's corresponding file
            
        Returns
        --------
        Res
            A new reservation instance.
        
        '''
        if GarageManager.check_if_available(day, tRange=tRange):
            c_res = ResManager.create_res(ID, owner, day, tRange, filename=filename)
            GarageManager.write_res(c_res)
            return True
        else:
            return False
    
    @staticmethod
    def query_if_res_exists(ID: str) -> bool:
        '''
        Query if the reservation file exists.
        '''
        if f'{ID}.txt' in os.listdir('./reservations'):
            return True
        else:
            return False
            
    @staticmethod
    def query_if_day_exists(day_ID: str) -> bool:
        '''
        Query if the reservation file exists.
        '''
        if f'{day_ID}.txt' in os.listdir('./days'):
            return True
        else:
            return False
        
    
    @staticmethod
    def cancel_res(ID: str) -> None:
        '''
        Remove the specified reservation from time slots & change active
        attribute in files.
        
        Parameters
        -------------
        ID : str
            The unique identifier of the reservation being modified.
        '''
        c_res = ResManager.load_res(filename=ID)
        GarageManager.remove_res(c_res)
        ResManager.cancel_res(c_res)
        
    @staticmethod
    def findLift(ID: str) -> int:
        '''
        Find the lift index of the reservation with ID == ID
        
        Parameters
        -----------
        ID : str
            The unique identifier of the reservation in question.
        '''
        c_res = ResManager.load_res(filename=ID)
        return GarageManager.findLift(c_res)
    
    @staticmethod
    def get_res(filename: str) -> Res:
        '''
        Loads Res object from file & returns. 
        
        Parameters
        ----------
        filename : str
            The reservation's file name. By default, filename == Res.ID.
        '''
        return ResManager.load_res(filename)
    
    @staticmethod
    def query_modify_res(res_ID: str, new_d: int, new_tRange: TimeRange) -> bool:
        '''
        Checks if a reservation can be moved to new time. Returns true/false

        Parameters
        -----------
        ID : str
            The pre-modification reservation instance
            
        new_d : int
            The new day
            
        new_tRange : TimeRange
            The new time range
            
        Returns : bool (true = can modify)
        
        '''
        
        c_res = ResManager.load_res(filename = res_ID)
        return GarageManager.check_if_available(new_d, new_tRange, res_modifiying=c_res)
    
    @staticmethod
    def attempt_modify_res(res_ID: str, new_d: int, new_tRange: TimeRange) -> bool:
        '''
        Attempts to modify the reservation to the new day & times. Saves files.
        Returns true if successful
        
        Parameters
        -----------
        ID : str
            The pre-modification reservation instance
            
        new_d : int
            The new day
            
        new_tRange : TimeRange
            The new time range
            
        Returns : bool (true = successfully modified)
        '''
        # Check if the time range is open
        c_res = ResManager.load_res(filename = res_ID)
        can_modify = GarageManager.check_if_available\
            (new_d, new_tRange, res_modifiying=c_res)
        
        # If possible, modify the Res files & day timeslots.
        if can_modify:
            GarageManager.remove_res(c_res)
            ResManager.change_date_n_time(c_res, new_d, new_tRange)
            GarageManager.write_res(c_res)
            return True
        else:
            return False
    
    @staticmethod
    def get_day_from_file(day_ID: str) -> Day:
        '''
        Load & initialize a day object from its corresponding file.
        '''
        return GarageManager.load_day(day_ID=day_ID)
    
    @staticmethod
    def list_days_initialized() -> list:
        '''
        List the day files that have been initialized.
        '''
        return DaysIntiliazed.days
        
    
    @staticmethod
    def query_if_available(day: int, tRange: TimeRange):
        '''
        Check if the requested time range is available on day. Return bool
        
        Parameters
        ------------
        day : int
            The day in question
        tRange : TimeRange
            The contigous time segments in question
        '''
        return GarageManager.check_if_available(day=day, tRange=tRange)
    
    
if __name__ == '__main__':
    
    #print(ReservationAPI.list_days_initialized())
    #print(ReservationAPI.get_day_from_file('1'))
    #print(ReservationAPI.query_if_day_exists('10')
    pass