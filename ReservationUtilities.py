# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 17:27:21 2022

@author: tanne
"""

from TimeUtilities import TimeRange

class Res():
    '''
    Reservation class, shortened to Res
    
    Attributes
    ----------
    ID : string
        unique identification of reservation.
    owner : string
        Username of Res owner/creator.
    day : int
        Day (1-365) of the reservation.
    tRange : TimeRange
        Time range of reservation (attributes start & end)
    start : float
        Start time
    end : float
        End time
    active : Boolean, optional
        False if the reservation has been cancelled. The default is True.
        
    Methods
    --------
    __str__ : overloads 

    '''

    def __init__(self, ID, owner, day, time_range=None, active=True, start_time=None, end_time=None):
        '''
        Construct Res (reservation) instance

        Parameters
        ----------
        ID : str
        owner : str
        day : int
        time_range : TimeRange, optional
        
            start_time : float, optional
            end_time : float, optional
        
        active : bool, optional
        '''
        
        # Establish time range value. Add 'start' and 'end' attributes for
        #     convenience
        if time_range != None:
            self.tRange = time_range
        else:
            self.tRange = TimeRange(start=start_time, end=end_time)
        
        self.start = self.tRange.start
        self.end = self.tRange.end
        
        self.day = day
        self.owner = owner
        self.ID = ID
        self.active = active
    
    
    def __str__(self):
        return f'*Reservation*\nID:     {self.ID}\nOwner:  {self.owner}\nDay:    {self.day}\nTime:   {self.tRange}\nActive? {self.active}\n'

    def toString(self):
        return f'ID:     {self.ID}\nOwner:  {self.owner}\nDay:    {self.day}\nTimes:  {self.tRange.toString()}\nActive: {self.active}'
    
    def save(self):
        '''
        save reservation object as text file.
        '''
        fileName = f'reservations/{self.ID}.txt'

        with open(fileName, mode='w') as file:
            file.write(self.toString())
            
    
    @staticmethod
    def fromFile(ID):
        '''
        Creates a reservation (Res) instance from file named {ID}.txt

        Parameters
        ----------
        ID : string
            ID of reservation file to be read.

        Returns
        -------
        Res
            Reservation instance from file {ID}.txt

        '''
        
        # Read file
        with open(f'reservations/{ID}.txt') as file:
            lines = file.read().split('\n')

        # Go through each line and split key from values.
        # Clean up data for conversion. Gives 2d list of strings: 
        # [[key, val], ...]
        for i in range(len(lines)):
            lines[i] = lines[i].split(':')
            for j in range(len(lines[i])):
                lines[i][j] = lines[i][j].strip().lower()
        

        # Create dictionary of classes/constructors to clean up data.
        # 1) converts each value to correct type
        # 2) places each value in a new list, in ordered positions
        
        constructor = {'id': str,
                 'day': int,
                 'times': TimeRange,
                 'owner': str,
                 'active': bool}

        positions = {'id': 0,
                 'day': 2,
                 'times': 3,
                 'owner': 1,
                 'active': 4}

        d = [None] * 5
        
        for line in lines:
            key = line[0]
            d[positions[key]] = constructor[key](line[1])
        
        return Res(d[0], d[1], d[2], d[3], d[4])


if __name__ == '__main__':
    c_res = Res.fromFile('testRes')
    
    print(c_res)
    
    c_res.save()
    
    