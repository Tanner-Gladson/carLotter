# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 17:27:21 2022

@author: tanne
"""


class Res():
    '''
    Attributes
    ----------
    start_time : tuple
        start time of reservation, (mo, day, hour)
    end_time : tuple
        end time of reservation, (mo, day, hour) .
    owner : string
        Username of Res owner/creator.
    ID : string
        unique identification of reservation.
    active : Boolean, optional
        False if the reservation has been cancelled. The default is True.

    '''

    def __init__(self, ID, owner, start_time, end_time, active=True):
        self.start_time = start_time
        self.end_time = end_time
        self.owner = owner
        self.ID = ID
        self.active = active
    
    
    def __str__(self):
        return f'*Reservation*\nID:     {self.ID}\nOwner:  {self.owner}\nStart:  {self.start_time}\nEnd:    {self.end_time}\nActive? {self.active}\n'

    def toString(self):
        return f'ID:     {self.ID}\nOwner:  {self.owner}\nStart:  {self.start_time}\nEnd:    {self.end_time}\nActive? {self.active}'


class Writer():

    '''
    Attributes
    --------------
    c_res: res
        the current reservation object being managed

    Methods
    ---------
    write_res: writes the information from a reservation into a CSV file

    '''
    @staticmethod
    def write(c_res):
        fileName = f'{c_res.ID}.txt'

        with open(fileName, mode='w') as file:
            file.write(c_res.toString())


class Reader():
    '''
    Methods
    ---------
    read: from a reservation id, read data into Res object
    __getData: given an ID, return an ordered list of attributes
    __tuple_floats: from a tuple-looking string, create a tuple of floats

    '''
    @staticmethod
    def read(ID):

        # Read data from file into list, return new Res instance
        d = Reader.__getData(ID)
        return Res(d[0], d[1], d[2], d[3], d[4])


    @staticmethod
    def __getData(ID):
        '''
        Open, read, & clean data from the given gile

        Parameters
        ----------
        ID : TYPE
            DESCRIPTION.

        Returns
        -------
        List
            Ordered list of values from the reservation file
            [ID, owner, start_time, end_time, active]

        '''

        # Read file
        with open(f'{ID}.txt') as file:
            lines = file.read().split('\n')

        # Go through each line and split key from values.
        # Clean up data for conversion
        for i in range(len(lines)):
            lines[i] = lines[i].split(':')
            for j in range(len(lines[i])):
                lines[i][j] = lines[i][j].strip()


        # Create dictionary of constructors to clean up data.
        constructor = {'ID': str,
                 'start_time': Reader.__tuple_floats,
                 'end_time': Reader.__tuple_floats,
                 'owner': str,
                 'active': bool}

        positions = {'ID': 0,
                 'start_time': 2,
                 'end_time': 3,
                 'owner': 1,
                 'active': 4}

        data = [None] * 5
        
        for line in lines:
            key = line[0]
            data[positions[key]] = constructor[key](line[1])

        return data

    @staticmethod
    def __tuple_floats(rawTuple):
        '''
        Takes a tuple-like string, and converts into tuple with d_type = float

        Returns
        -------
        Tuple of floats

        '''
        clean_string = rawTuple.strip().replace('(','').replace(')','')
        myList = clean_string.split(',')

        for i in range(len(myList)):
            try:
                myList[i] = float(myList[i])

            except ValueError:
                raise ValueError(f'Could not convert {myList} into tuple of floats')

        return tuple(myList)

if __name__ == '__main__':
    c_res = Reader.read('testRes')
    
    print(c_res)
    
    Writer.write(c_res)