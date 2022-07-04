# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 17:27:21 2022

@author: tanne
"""

from ReservationsModule import Res
from TimeUtilities import TimeRange
import numpy as np
import sys
import json


class Day():
    '''
    Class Attributes
    -----------------
    days_initiated : list [int]
        list of the days that have already been initiated & saved as files
    
    
    Attributes
    ----------
    day_num : Int
        The current day
    
    n_lifts : Int
        Number of lifts (depth of ReservedSlots array)
        
    ReservedSlots : npArray (num_lifts x 24) # Optional
        All times slots in a day. 
        - First axis is lift #
        - Second axis is start hour
        
    res_locs : dict {str : int} # Optional
        A dictionary mapping reservation IDs to lift number
        
    Methods
    ---------
    remove_res(self, c_res) -> None 
        Removes all entries of a Res from ReservedSlots
        
    write_res(self, c_res) -> None
        Inserts Res ID into appropriate self.ReservedSlots locations
        
    findBestLift(self, tRange, modifying=None or Res) -> int
        returns the best lift to insert place Res in. 
        - If type(modifying)==Res, then accounts for placing in current loc.
            Only != None when called by liftManager class
        - If no spot available, return == 0
        
    findLift(c_res: Res) -> int
        Return the index of the lift in which a reservation resides
        
    __str__(self) -> String
        Return data from Day as a readable string
        
    writeSelf(self) -> None
        Write data from self into a file titled self.ID.txt * self.ID.npy
    
    @static
    read(day_num) -> Day
        Read the files titled 'day_num.txt' & 'day_num.npy' to 
        construct/return a Day instance
        
    @class
    save_days_init(Day) -> None
        Save (pickle) list of days that have been initiated
        
    
    '''
    
    days_initiated = json.load(open('days/initiated_days.json'))
    
    @classmethod
    def update_days_init(self, day):
        '''
        Update and save list of days that already have corresponding file
        '''
        if day not in Day.days_initiated:
            self.days_initiated.append(day)
            json.dump(self.days_initiated,  open('days/initiated_days.json', 'w'))
        
    
    
    def __init__(self, day_num, num_lifts, reservedSlots=None, res_locs=None, fileName=None):
        '''
        Initialize values of new instance
        
        Parameters
        ----------
        day_n : Int
        
        n_lifts : Int
            Number of lifts (depth Reserved slots).
            
        ReservedSlots : 2d ndarray, optional
        
        res_locs : dict {ID str : int}, optional
        '''
        
        self.day = day_num
        
        if fileName == None:
            self.fileName = str(day_num)
        else:
            self.fileName = fileName
            
        
        self.n_lifts = num_lifts
        
        if type(reservedSlots) == np.ndarray:
            self.reservedSlots = reservedSlots
        else:
            self.reservedSlots = np.full((num_lifts, 24), None)
            
        if res_locs != None:
            self.res_locs = res_locs
        else:
            self.res_locs = {}
            
        self.save()
        Day.update_days_init(day_num)
        
            
    
    def remove_res(self, c_res: Res) -> None:
        '''
        Removes all entries of a Res from ReservedSlots
        '''
        ID = c_res.ID
        self.reservedSlots[self.reservedSlots == ID] = None
        self.save()
        
        
    def write_res(self, c_res: Res) -> None:
        '''
        Inserts Res ID into appropriate self.ReservedSlots locations
        '''
        # Find the best lift. Insert string into appropriate coordinates
        tRange = c_res.tRange
        lift = self.findBestLift(tRange)
        
        if lift == -1:
            raise ValueError(f'The following reservation does not fit in {self.day}:\n{c_res}')
        
        # TODO Indexing only works if start & end times are multiples of hours
        self.reservedSlots[lift, int(tRange.start):int(tRange.end)] = c_res.ID
        self.save()
        
        
    def findBestLift(self, tRange: TimeRange):
        '''
        returns the best lift to insert place Res in. If no contiguous time 
        slots are available, returns -1.
        
        Parameters
        ----------
        tRange : TimeRange
            The time range over contiguous slots in question.

        Returns
        -------
        int
            The lift (index of reservedSlots) where the reservation should be
            inserted. Returns -1 if not possible to insert.
        '''
        s = int(tRange.start)
        e = int(tRange.end)
        res_times = np.arange(s, e)
        b_lift = -1
        min_score = sys.maxsize
        
        # Iterate through each lift, and determine if the reservation will fit
        # in that lift. If it does, calculate the score.
        for k in range(self.n_lifts):
            opens = np.where(self.reservedSlots[k] == None)[0]
            
            # If fit, find score. Else, continue
            if np.all(np.isin(res_times, opens)):
                # Find the gap between current res and nearest reservations.
                # Calculate score, and assign new best lift & score
                i = s
                j = e-1
                while self.reservedSlots[k, i] == None and i > 0:
                    i -= 1
                while self.reservedSlots[k, j] == None and j < 23:
                    j += 1
                
                d1 = s - i
                d2 = j - e
                score = (d1 - (d1**2)/48 )  + (d2 - (d2**2)/48 )
                
                if score < min_score:
                    min_score = score
                    b_lift = k
        
        return b_lift
        
    def findLift(self, c_res: Res) -> int:
        '''
        Return the index of the lift in which a reservation resides
        
        Parameters
        ----------
        c_res : Res
            The reservation in question
        '''
        # Find the first coordinate of the first 'ID' value in reservedSlots
        return np.where(self.reservedSlots == c_res.ID)[0][0]
        
        
    
    def __str__(self) -> str:
        
        # Create string: day, number lifts, location dictionary, and np array
        s1 = f'Day {self.day}'
        s2 = f'{self.n_lifts} Lifts'
        s3 = str(self.res_locs)
        s4 = np.array2string(self.reservedSlots, max_line_width=sys.maxsize)
        
        return f'{s1}\n{s2}\n{s3}\n\n{s4}'
        
    def save(self) -> None:
        '''
        Write all data from self to text file & numpy file
        '''
        filename = f'days/{self.fileName}.txt'
        
        with open(filename, mode='w') as file:
            file.write(str(self))
            
        np.save(f'days/{self.fileName}', self.reservedSlots)
        
        Day.update_days_init(self.day)
    
    @staticmethod
    def fromFiles(fileName):
        '''
        Read the file titled 'day_num.txt' and construct/return a Day instance

        Parameters
        ----------
        day_num : int
            What day to read.

        Returns
        -------
        Day
            A Day instance containing all the data from the appropriate file.

        '''
        filename = f'days/{fileName}.txt'
        
        # Open the file, and parse out each attribute
        with open(filename, mode='r') as file:
            raw = file.read().split('\n') #split by line
            
            # Find the number of lifts (2nd line, all chars before first space)
            # Find res_locs by using handy-dandy eval function
            day_num = int(raw[0].split(' ')[-1])
            num_lifts = int(raw[1].split(' ')[0])
            res_locs = eval(raw[2])
            
        reservedSlots = np.load(f'days/{fileName}.npy', allow_pickle=True)
        
        return Day(day_num, num_lifts, reservedSlots, res_locs)

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
    
    findLift(c_res: Res) -> int:
        Return the index of the lift in which a reservation resides
        
    Class Attributes
    ----------------
    default_num_lifts : int
        Number of lifts that each day has.
    '''
    
    default_num_lifts = 2

    @classmethod
    def check_if_available(self, day_ID, tRange: TimeRange, res_modifiying=None) -> bool:
        '''
        TODO #1 Does not consider shifting reservations around
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
    
    @classmethod
    def findLift(self, c_res: Res) -> int:
        '''
        Return the index of the lift in which a reservation resides
        
        Parameters
        ----------
        c_res : Res
            The reservation in question
        '''
        
        c_day = self.load_day(c_res.day)
        return c_day.findLift(c_res)
    
    
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