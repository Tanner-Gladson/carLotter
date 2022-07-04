# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 17:27:21 2022

@author: tanne
"""

from calendar import c

from isort import file
from TimeUtilities import TimeRange
import os

class Res():
    '''
    Reservation class, shortened to Res. Does not auto save to file.
    
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

    def __init__(self, ID, owner, day, time_range=None, active=True, start_time=None, end_time=None, fileName=None):
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
        
        fileName : str
            The name of the file which stores the reservation. Defaults to ID
        
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
        
        if fileName != None:
            self.fileName = fileName
        else:
            self.fileName = ID
    
    
    def __str__(self):
        return f'*Reservation*\nID:     {self.ID}\nOwner:  {self.owner}\nDay:    {self.day}\nTime:   {self.tRange}\nActive? {self.active}\n'

    def toString(self):
        return f'ID:     {self.ID}\nOwner:  {self.owner}\nDay:    {self.day}\nTimes:  {self.tRange.toString()}\nActive: {self.active}'
    
    def save(self):
        '''
        save reservation object as text file.
        '''
        fileName = f'reservations/{self.fileName}.txt'.lower()

        with open(fileName, mode='w') as file:
            file.write(self.toString())



class ResManager():
    '''
    A static class for interfacing & managing Res instances (and objects).
    
    Methods
    --------
    load_res(ID: str) -> Res
        load the specified reservation from its file
        
    create_res(ID, owner, day, tRange) -> Res
        Create a Res instance. Auto saves to file
        
    change_date_n_time(c_res: Res, new_d: int, new_tRange: TimeRange) -> None
        Change the date and/or time of an existing reservation. Save.
        
    cancel_res(c_res: Res) -> None
        Set the 'active' member of an existing Res to False. Save
        
    smite_res(ID: str) -> None
        Deletes the file of an existing reservation. Only used for testing.
    
    '''
    
    @staticmethod
    def load_res(fileName: str) -> Res:
        '''
        Creates a reservation (Res) instance from file named {ID}.txt

        Parameters
        ----------
        fileName : string
            The file name (default ID) of reservation file to be read.

        Returns
        -------
        Res
            Reservation instance from file {ID}.txt

        '''
        
        # Read file
        with open(f'reservations/{fileName}.txt'.lower()) as file:
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
    
    @staticmethod
    def create_res(ID: str, owner: str, day: int, tRange: TimeRange, fileName=None) -> Res:
        '''
        Create a Res instance. Auto saves to file
        
        Parameters
        ----------
        ID : string
            A unique identification of reservation. Will be the file's prefix
        
        owner : string
            Username of Res owner/creator.
        
        day : int
            Day (1-365) of the reservation.
        
        tRange : TimeRange
            Time range of reservation (attributes start & end)
        '''
        
        c_res = Res(ID=ID, owner=owner, day=day, time_range=tRange, fileName=fileName)
        c_res.save()
        return c_res
    
    @staticmethod
    def change_date_n_time(c_res: Res, new_d: int, new_tRange: TimeRange) -> None:
        '''
        Update the date and time of a reservation instance. Overwrite file
        
        Parameters
        ----------
        c_res : Res
            The reservation instance & file to be modified
            
        new_d : int
            The new day value of the reservation
            
        new_rTange : TimeRange
            The new time range spanned by the reservation
        '''
        c_res.day = new_d
        c_res.tRange = new_tRange
        c_res.start = c_res.tRange.start
        c_res.end = c_res.tRange.end
        
        c_res.save()
    
    @staticmethod
    def cancel_res(c_res: Res) -> None:
        
        c_res.active = False
        c_res.save()
        
    
    @staticmethod
    def smite_res(ID: str) -> None:
        '''
        Delete the file of an existing reservation.
        '''
        filename = f'reservations/{ID}.txt'
        os.remove(filename)


if __name__ == '__main__':
    
    pass
    