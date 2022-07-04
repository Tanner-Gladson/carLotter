# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 17:27:19 2022

@author: tanne
"""

import json
import os
import pickle

class AcctsInitiliazed():
    '''
    A static class for tracking what accounts have been initiliazed and
    saved. Accounts for async, manual deletion/modification of files.
    
    Attributes
    ----------
    accts : list [str]
        A list of the account usernames which have been initialized
    
    Methods
    ------ 
    @class
    initialize() -> None:
        Initializes self.accts. Implemented to safeguard against asyncronous
        (manual) modification of files.
        
    @class
    update() -> None:
        Update the self.accts attributes & corresponding file
    '''
    
    accts = []
    
    @classmethod
    def initialize(self) -> None:
        '''
        Initializes self.accts. Implemented to safeguard against asyncronous
        (manual) modification of files.
        '''
        
        all_files = os.listdir('./accounts')
        self.accts = \
            [filename[:-4] for filename in all_files if filename[-4:] == '.txt']
        json.dump(self.accts, open('./accounts/initialized_accounts.json', 'w'))
    
    @classmethod
    def update(self, c_filename) -> None:
        
        filename = f'{c_filename}.txt'
        
        if c_filename not in self.accts:
            self.accts.append(c_filename)
            json.dump(self.accts, open('./accounts/initialized_accounts.json', 'w'))


class Acct():
    '''
    The non-static class for containing information in a user's account.
    
    Attributes
    ----------
    fileName=None : str
        The filename that contains the saved account instance. Optional,
        defaults to username.
    
    username : str
        The username of the user
        
    password : str
        The user's password
        
    reservations : list [str]
        A list of the reservation IDs belonging to the user.
    
    
    Methods
    -------
    save(self) -> None:
        Save the isntance to a text file and json.
    
    __str__(self) -> str
        Overload string operator to print readable account summary.
        
    smite_acct(self) -> None:
        Remove the account file & update DaysIntiliazed.days. For testing only
    '''
    AcctsInitiliazed.initialize()
    
    
    def __init__(self, username: str, password: str, filename=None):
        '''
        Parameters
        ----------
        username : str
            The username of the account
        password : str
            The user's password
        filename : str (Optional, default None)
            The filename of the save location for this account
        '''
        
        self.username = username
        self.password = password
        if filename == None:
            self.filename = username
        else:
            self.filename = filename
            
        self.reservations = []
        
        self.save()
    
    def __str__(self) -> str:
        '''
        Convert self to readable string
        '''
        return f'**Account**\nUsername: {self.username}\nPassword: {self.password}\nFilename: {self.filename}\n\nReservations: {self.reservations}\n\n'
        
    
    def save(self) -> None:
        '''
        Save the isntance to a text file and json. Update DaysIntialized.days
        '''
        with open(f'accounts/{self.filename}.pickle', 'wb') as file:
            pickle.dump(self, file)
        
        with open(f'accounts/{self.filename}.txt', 'w+') as file:
            file.write(self.__str__())


class AccountManager():
    '''
    Static class for creating, loading, and modifying accounts.
    
    Attributes
    ----------
    
    
    Methods
    ------ 
    
    '''
    
if __name__ == '__main__':
    my_account = Acct('Smarthi', '')
    print(my_account)