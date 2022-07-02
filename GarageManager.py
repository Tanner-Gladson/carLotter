
from ReservationClass import Res
from TimeUtilities import TimeRange
from DayClass import Day

class GarageManager():
    '''
    Static class for interfacing (managing) Day instances & files. 
    
    Methods
    --------
    check_if_available(day, tRange, modifiying=None) -> boolean
        Check if the user-requested time range is available to insert a
        reservation. If modifying = Res class, the function will treat
        timeslots filled with ID == modifiying.ID as open timeslots. (I.e, can
        overwrite current reservation).

    remove_res(c_res: Res) -> None
        Clear a reservation from reserved slots (thereby opening that time
        range for another reservation)

    write_res(c_res: Res) -> None
        Write a reservation's ID into the appropriate day & time slots

    modify_res(old_res: Res, new_d, new_s, new_e) -> None
        1) removes reservation ID from all past days & times
        2) Write's reservation ID into new day, with new start & end
    
    load_day(day_ID: int) -> Day
        Creates Day instance from files with name 'ID' (integer).

    create_day(day: int, n_lifts: int) -> Day
        Constructs new Day instance with ID 'day'. Automatically saves to files
        
    reset_day(day_ID: int, n_lifts: int) -> None
        Resets all the data from a day.
        
        
    Class Attributes
    ----------------
    default_num_lifts : int
        Number of lifts that each day has.
    '''
    
    default_num_lifts = 2

    @classmethod
    def check_if_available(self, day_ID, tRange: TimeRange, res_modifiying=None) -> bool:
        '''
        Check if a reservation can be created for specified day, time range,
        and (optionally) by overwriting an existing reservation
        
        Parameters
        -----------
        day : int
        tRange : TimeRange
        
        Modifying : None | Res
            When modifying, provides best time by considering optional Res as 
            'open' time.
        
        Return
        -------
        bool
        
        '''
        c_day = self.load_day(day_ID)
        
        # If not modifying or original Res on different day, simply determine 
        # if there is a best lift for day_ID (current day)
        if res_modifiying == None or res_modifiying.day != day_ID:
            best_lift = c_day.findBestLift(tRange)
        
        # If new time slot & old reservation (modifying) are on same day: 
        # 1) remove old res,
        # 2) find best lift,
        # 3) replace old res.
        else:
            c_day.remove_res(res_modifiying)
            best_lift = c_day.findBestLift(tRange)
            c_day.write_res(res_modifiying)
        
        
        # If best lift == -1, then new time range is not available
        if best_lift == -1:
            return False
        else:
            return True
    
    
    @classmethod
    def remove_res(self, c_res: Res) -> None:
        '''
        Loads the correct day, and removes all time slots entries with ID ==
        c_res.ID
        '''
        c_day = self.load_day(c_res.day)
        c_day.remove_res(c_res)
    
    
    @classmethod
    def write_res(self, c_res: Res) -> None:
        '''
        Loads the correct day, and writes c_res.ID to appropriate time slots
        '''
        c_day = self.load_day(c_res.day)
        c_day.write_res(c_res)
    
    '''
    TODO
    @classmethod
    def modify_res(self, old_res: Res, new_d, TimeRange) -> None:
        
        1) removes reservation ID from previous days & times
        2) Write's reservation ID into new day, with new start & end
        - ASSUMES that writing the reservation is legal
        
        Parameters
        -----------
        old_res : Res
            The pre-modification reservation instance
            
        new_d, new_s, new_e : int, float, float
            The new day and start+end times
        
        ??? MOVE THIS FUNCTION UP TO A HIGHER LEVEL ????
        self.remove_res(old_res)
        self.write_res(??)
        
        
        pass
        '''
    
    @classmethod
    def load_day(self, day_ID: int) -> Day:
        '''
        Loads day 'day_id' if possible. Else, creates new Day instance 
        (and corresponding files).
        
        Return: Day instance
        '''
        if day_ID in Day.days_initiated:
            return Day.fromFiles(day_ID)
            
        else:
            return self.create_day(day_ID)
    
    
    @staticmethod
    def create_day(day_ID: int, n_lifts=default_num_lifts) -> Day:
        '''
        Constructs new Day instance with ID 'day'. Automatically saves to files
        
        Parameters
        -----------
        day : int
            The day # that needs to be created
        
        n_lifts : int
            the number of lifts that could be filled that day. Defaults to
            class attribute.
            
        Return: Day instance
        '''
        return (Day(day_ID, n_lifts))
    
    @classmethod
    def reset_day(self, day_ID: int, n_lifts=default_num_lifts) -> None:
        '''
        Resets all the data from a day.
        '''
        self.create_day(day_ID, self.default_num_lifts)
        
        
if __name__ == '__main__':
    
    GarageManager.reset_day(1)
    
    res1 = Res('1', 'smarthi', 1, start_time=1, end_time=3)
    GarageManager.write_res(res1)
    
    res2 = Res('2', 'smarthi', 1, start_time=1, end_time=3)
    GarageManager.write_res(res2)
    
    res3_tRange = TimeRange(start=1, end=2)
    can_fit = GarageManager.check_if_available(1, res3_tRange, res2)
    
    print('We can fit res3:', can_fit)
    
    print(GarageManager.load_day(1))
        