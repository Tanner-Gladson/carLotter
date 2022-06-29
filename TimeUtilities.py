# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 16:46:55 2022

@author: tanne
"""

class TimeTools():
    '''
    Static class for manipulating time values
    '''
    
    @staticmethod
    def float_to_string(time):
        '''
        Converts the float to standard time (string, eg '12:00 to 13:00')
        '''
        hours = int(time//1)
        minutes = str(int((time % 1) * 60)).rjust(2, '0')
        return f'{hours}:{minutes}'
    
    
class TimeRange():
    '''
    Attributes
    ----------
    start_h : float
        start hour of time range
    end_time : float
        start hour of time range
        
    Methods
    ---------
    __str__
        overload to print in readable fashion
    
    toString
        convert end & start floats to tuple-like string 
        
    __fromString : private, static method
        convert tuple-like string to tuple of floats
        
    __contains__ : overloading operator
        Returns true if other can fit within self
    '''
    
    def __init__(self, string=None, start=None, end=None):
        '''
        Constructs time range object from start & end, or from string

        Parameters
        ----------
        start : float, optional
            Start time
        end : float, optional
            End time
        string : string, optional
            Tuple-like string of end and start time. The default is False.

        '''
        # Call fromString to assign start & end times
        
        
        if string != None:
            self.start, self.end = TimeRange.__fromString(string)
            
        else:
            self.start = float(start)
            self.end = float(end)
    
    def __contains__(self, other):
        '''
        For 'range1 in range 2', returns True if range1 can fit within range2
            (that is: other in self). Else false
            
        Parameters
        ------------
        self : TimeRange
        other : TimeRange
        '''
        can_fit = False
        
        if other.start >= self.start and other.end <= self.end:
            can_fit = True
        
        return can_fit
    
    
    def __str__(self):
        '''
        Overload string operator to print out readable version of TimeRange. 
        Utilizes TimeTools
        '''
        s = TimeTools.float_to_string(self.start)
        e = TimeTools.float_to_string(self.end)
        return f'{s} to {e}'
    
    def toString(self):
        '''
        Condenses object's data into form suitable for writing to file
        '''
        return str((self.start, self.end))
    
    @staticmethod
    def __fromString(string):
        '''
        Returns a tuple of floats from a similar-looking string
        '''
        clean_string = string.strip().replace('(','').replace(')','')
        myList = clean_string.split(',')

        for i in range(len(myList)):
            try:
                myList[i] = float(myList[i])

            except ValueError:
                raise ValueError(f'Could not convert {string} into tuple of floats')

        return tuple(myList)
    

if __name__ == '__main__':
    
    t1 = TimeRange(start=1, end=2)
    
    import numpy as np
    a = np.array([t1, None])
    print(a)