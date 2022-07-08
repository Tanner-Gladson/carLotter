# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 17:23:21 2022

@author: tanne
"""

class AdminUI():
    '''
    A static class containing actions executable by user.
    
    Methods
    --------
    @class
    initiateUI(self) -> None:
        Initiate the console user interface
    
    @class
    help(self) -> str:
        Return a pre-defined string of commands executable by user
    
    @class
    dayList(self) -> str:
        Return a formatted list of filenames (day IDs) in the ./days directory
    
    @class
    dayView (self, ID: str) -> str:
        Return a formatted view of a specific day's timeslot data 
    
    @class
    accountList(self) -> str:
        Returns a formatted list of filenames (usernames) in the ./accounts
        directory.
    
    @class
    accountView(self, username: str) -> str:
        Returns a formatted view of a specific account's data
        
    @class
    accountCreate(self, username: str, password: str) -> str:
        Create a new account. Return str giving confirmation and account view
    
    @class
    accountChangePassword \
        (self: str, username: str, old_pass: str, new_pass: str) -> str:
        Change the password of an account. Return a str giving confirmation
    
    @class
    reservationCreate \
        (self, username: str, day: str, s_time: str:, e_time, str) -> str:
        Attempt to create a reservation. Return confirmation and the Res view
    
    @class
    reservationView(self, ID: str) -> str:
        Return a formatted string of a reservation's data
    
    @class
    reservationRequestModify \
        (self, ID: str, new_d: str, new_s: str, new_e: str) -> str:
        Attempt to modify the day, start, and end of a reservation. Return
        string with confirmtion & reservation view
        
    
    @class
    reservationCancel(self, ID: str) -> str
        Cancel a reservation. Return a string giving confirmation and Res view
    
    '''
    pass


if __name__ == '__main__':
    AdminUI.initiateUI()