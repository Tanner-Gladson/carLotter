# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 17:27:19 2022

@author: tanne
"""

import json
import os
import pickle

from numpy import nonzero
from ReservationsModule import Res

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
    The non-static class for containing information in a user's account. Saved
    to txt and pickle files in ../accounts/
    
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
        
        AcctsInitiliazed.update(c_filename=self.filename)


class AccountManager():
    '''
    Static class for creating, loading, and modifying accounts.
    
    Methods
    ------ 
    account_exists(username: ID) -> bool:
        Check if a username has a corresponding file.
    
    load_acct(filename: str) -> Acct:
        Loads and constructs an account instance from files
        
    create_acct(username: str, password: str, filename=None) -> Acct:
        Creates a new account instance and appropriate files
    
    add_reservation_to_acct(c_account: Acct, c_res: Res):
        Add a reservation to list of reservations. Update account files
        
    change_password\
        (c_account: Acct, old_password: str, new_password: str) -> None:
        Change the account's password
    
    smite_acct(username: str) -> None:
        Remove the files associated with username
        
    list_accounts_initialized() -> list
        Lists the account files that have been intiliazed
    
    @class
    unlist_reservations(username: str) -> None:
        Reset the list of reservations associated with this account.
        **for testing only
        
    
        
    '''
    @staticmethod
    def account_exists(username: str) -> bool:
        '''
        Check if a username has a corresponding file.
        '''
        if username in AcctsInitiliazed.accts:
            return True
        else:
            return False
    
    
    @staticmethod
    def load_acct_from_file(filename: str) -> Acct:
        '''
        Loads and constructs an account instance from files.
        
        Parameters
        ----------
        filename : str
            The filename associated with an account. Default is username
        '''
        #unpickle file
        with open(f'accounts/{filename}.pickle', 'rb') as file:
            c_account = pickle.load(file)
            
        return c_account
        
    @staticmethod
    def create_acct(username: str, password: str, filename=None) -> Acct:
        '''
        Creates a new account instance and appropriate files
        
        Parameters
        ----------
        username : str
            The username of the account
        password : str
            The password to log into the account
        filename : str (default None)
            The filename which points the account's save location
        '''
        return Acct(username, password, filename)
        
    
    @staticmethod
    def add_reservation_to_acct(c_account: Acct, c_res: Res) -> None:
        '''
        Append a reservation to list of reservations. Update account files
        
        Parameters
        ----------
        c_account : Acct
            The account to modify
            
        c_res : Res
            The reservation to modify
        '''
        c_account.reservations.append(c_res.ID)
        c_account.save()
        
        
    @staticmethod
    def change_password\
        (c_account: Acct, old_password: str, new_password: str) -> bool:
        '''
        Change the account's password. Returns True if successful
        
        Parameters
        ----------
        c_account : Acct
            The account we want to change the password for
        old_password : str
            The old password
        new_password : str
            The new password
        '''
        if old_password == c_account.password:
            c_account.password = new_password
            c_account.save()
            return True
        
        else:
            return False
    
    
    @staticmethod
    def smite_acct(filename=None) -> None:
        '''
        Remove the files associated with username. **For testing only.
        '''
        
        os.remove(f'./accounts/{filename}.txt')
        os.remove(f'./accounts/{filename}.pickle')
        AcctsInitiliazed.initialize()
    
    @staticmethod
    def list_accounts_initialized() -> list:
        '''
        Return a list of the accounts that have been initialized
        '''
        return AcctsInitiliazed.accts[:]
    
    @classmethod
    def unlist_reservations(self, filename: str) -> None:
        '''
        Reset the list of reservations associated with this account.
        **for testing only
        '''
        # TODO verify by testing
        c_account = self.load_acct_from_file(filename)
        c_account.reservations = []
        c_account.save()

    
    
if __name__ == '__main__':
    print(AcctsInitiliazed.accts)
    print(AccountManager.account_exists("Smarthi"))
    pass