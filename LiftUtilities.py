# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 17:27:21 2022

@author: tanne
"""

from ReservationUtilities import Res
from TimeUtilities import TimeTools, TimeRange
import numpy as np
from typing import Union
import sys

class Day():
    '''
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
        
    __str__(self) -> String
        Return data from Day as a readable string
        
    writeSelf(self) -> None
        Write data from self into a file titled self.ID.txt * self.ID.npy
    
    @static
    read(day_num) -> Day
        Read the files titled 'day_num.txt' & 'day_num.npy' to 
        construct/return a Day instance
    
    '''
    def __init__(self, day_num, num_lifts, reservedSlots=None, res_locs=None):
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
        self.n_lifts = num_lifts
        
        if type(reservedSlots) == np.ndarray:
            self.reservedSlots = reservedSlots
        else:
            self.reservedSlots = np.full((num_lifts, 24), None)
            
        if res_locs != None:
            self.res_locs = res_locs
        else:
            self.res_locs = {}
            
    
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
        
        
    def findBestLift(self, tRange: TimeRange, modifying=None):
        '''
        returns the best lift to insert place Res in. 
            If type(modifying)==Res, then accounts for placing in current loc.
                Only != None when called by liftManager class
            If no spot available, return == 0
        
        Parameters
        ----------
        tRange : TimeRange
            The time range in question.
        
        Modifying : None | Res
            When modifying, provides best time by considering optional Res as 
            'open' time.

        Returns
        -------
        int
            The lift (index of reservedSlots) where the reservation should be
            inserted
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
        filename = f'days/{self.day}.txt'
        
        with open(filename, mode='w') as file:
            file.write(str(self))
            
        np.save(f'days/{self.day}', self.reservedSlots)
    
    @staticmethod
    def fromFiles(day_num):
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
        filename = f'days/{day_num}.txt'
        
        # Open the file, and parse out each attribute
        with open(filename, mode='r') as file:
            raw = file.read().split('\n') #split by line
            
            # Find the number of lifts (2nd line, all chars before first space)
            # Find res_locs by using handy-dandy eval function
            num_lifts = int(raw[1].split(' ')[0])
            res_locs = eval(raw[2])
            
        reservedSlots = np.load(f'days/{day_num}.npy', allow_pickle=True)
        
        return Day(day_num, num_lifts, reservedSlots, res_locs)

if __name__ == '__main__':
    res1 = Res('abcd', 'Smarthi', 1, start_time=1, end_time=2)
    res2 = Res('jdhf', 'Smarthi', 1, start_time=1, end_time=3)
    res3 = Res('gdfg', 'Smarthi', 1, start_time=1, end_time=3)
    
    # Read a file, change instance's day so you don't overwrite
    myDay = Day.fromFiles('test')
    myDay.day = 1
    myDay.write_res(res1)
    print(myDay)
    
    
    myDay.write_res(res2)
    print('\n')
    print(myDay)
    
    myDay.write_res(res3)
    print('\n')
    print(myDay)
    
    
    
    
    