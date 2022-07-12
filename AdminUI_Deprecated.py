# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 17:23:21 2022

@author: tanne
"""
from TimeUtilities import TimeRange, TimeTools
from ReservationsAPI import ReservationAPI
from GarageModule import DaysIntiliazed, GarageManager, Day
from AccountModule import AccountManager, AcctsInitiliazed


class AdminUI():
    '''
    A static class containing actions executable by user.
    TODO #3 Refactor into more classes
    TODO #4 Re-do backend commands that might fail if wrong info given.
    
    Methods
    --------
    @classmethod
    initiateUI(self) -> None:
        Initiate the console user interface
    
    @classmethod
    help(self) -> str:
        Return a pre-defined string of commands executable by user
    
    @classmethod
    dayList(self) -> str:
        Return a formatted list of filenames (day IDs) in the ./days directory
    
    @classmethod
    dayView (self, ID: str) -> str:
        Return a formatted view of a specific day's timeslot data 
    
    @classmethod
    accountList(self) -> str:
        Returns a formatted list of filenames (usernames) in the ./accounts
        directory.
    
    @classmethod
    accountView(self, username: str) -> str:
        Returns a formatted view of a specific account's data
        
    @classmethod
    accountCreate(self, username: str, password: str) -> str:
        Create a new account. Return str giving confirmation and account view
    
    @classmethod
    accountChangePassword \
        (self: str, username: str, old_pass: str, new_pass: str) -> str:
        Change the password of an account. Return a str giving confirmation
    
    @classmethod
    reservationCreate \
        (self, username: str, day: str, s_time: str:, e_time, str) -> str:
        Attempt to create a reservation. Return confirmation and the Res view
    
    @classmethod
    reservationView(self, ID: str) -> str:
        Return a formatted string of a reservation's data
    
    @classmethod
    reservationRequestModifyTime \
        (self, ID: str, new_d: str, new_s: str, new_e: str) -> str:
        Attempt to modify the day, start, and end of a reservation. Return
        string with confirmtion & reservation view
        
    
    @classmethod
    reservationCancel(self, ID: str) -> str
        Cancel a reservation. Return a string giving confirmation and Res view
    
    '''
    
    @classmethod
    def initiateUI(self) -> None:
        '''
        Initiate the console user interface. Switch and manage all of the
        possible commands / printing the UI.
        '''
        quit = False
        print('=======================================================================')
        print('          Welcome to Car Lotter! Type "help" to see commands.')
        print('=======================================================================')
        print()
        
        while not quit:
            print()
            print()
            user_in = input(f'>>> Enter command: ')
            print('-----------------------------------------------------------------------')
            print()
            command = user_in.split(' ')
            
            # Switch according to value. 
            # Check that command has right number of words
            if command[0] == 'account':
                if len(command) < 2: print('Too few arguments for this command')
                else: print(self.switchAccountCommands(command))
            
            elif command[0] == 'reservation':
                if len(command) < 2: print('Too few arguments for this command')
                else: print(self.switchReservationCommands(command))
            
            elif command[0] == 'day':
                if len(command) < 2: print('Too few arguments for this command')
                else: print(self.switchDayCommands(command))
            
            elif command[0] == 'help':
                print(self.help())
            
            elif command[0] == 'quit':
                quit = True
            
            else:
                print('Command not found. Type "help" for more info')
            
        pass
    
    @classmethod
    def switchAccountCommands(self, command: list) -> str:
        '''
        Switch & manage the account commands
        
        Parameters
        -----------
        command : list[str]
            The user's input, split into list by spaces
        '''
        if command[1] == 'list':
            if len(command) != 2:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "account list"'
            else:
                out_string = self.accountList()
        
        elif command[1] == 'view':
            if len(command) != 4:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "account view [username] [password]"'
            else:
                out_string = self.accountView(command[2], command[3])
        
        elif command[1] == 'create':
            if len(command) != 4:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "account create [username] [password]"'
            else:
                out_string = self.accountCreate(command[2], command[3])
        
        elif command[1] == 'change' and command[2] == 'password':
            if len(command) != 6:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "account change password [username] [old password] [new password]"'
            else:
                out_string = self.accountChangePassword(command[3], command[4], command[5])
        
        else:
            out_string = 'Command not found. Type "help" for more info'
        
        return out_string
    
    @classmethod
    def switchReservationCommands(self, command: list) -> str:
        '''
        Switch & manage the reservation commands
        
        Parameters
        -----------
        command : list[str]
            The user's input, split into list by spaces
        '''
        if command[1] == 'create':
            if len(command) != 7:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "reservation create [username] [ID] [day] [start time] [end time]"'
            else:
                out_string = self.reservationCreate\
                    (command[3], command[4], command[5], command[6], command[7])
        
        elif command[1] == 'view':
            if len(command) != 3:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "reservation view [ID]"'
            else:
                out_string = self.reservationView(command[2])
        
        elif command[1] == 'modify' and command[2] == 'time':
            if len(command) != 7:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "reservation modify time [ID] [new day] [new start time] [new end time]"'
            else:
                out_string = self.reservationRequestModifyTime\
                    (command[3], command[4], command[5], command[6])
        
        elif command[1] == 'cancel':
            if len(command) != 3:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "reservation cancel [ID]"'
            else:
                out_string = self.reservationCancel(command[2])
        
        else:
            out_string = 'Command not found. Type "help" for more info'
        
        return out_string
    
    @classmethod
    def switchDayCommands(self, command: list) -> str:
        '''
        Switch & manage the day commands
        
        Parameters
        -----------
        command : list[str]
            The user's input, split into list by spaces
        '''
        if command[1] == 'list':
            if len(command) != 2:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "day list"'
            else:
                out_string = self.dayList()
                
        elif command[1] == 'view':
            if len(command) != 3:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "day view [day]"'
            else:
                out_string = self.dayView(command[2])
                
        else:
            out_string = 'Command not found. Type "help" for more info'
        
        return out_string
    
    @classmethod
    def help(self) -> str:
        '''
        Return a pre-defined string of commands executable by use
        
        '''
        return f'help\n    Print a list of commands.\n\n'\
            'account list\n' \
            '     List all the account usernames.\n\n' \
            'account create [username] [password]\n' \
            '    Create a new account.\n\n'  \
            'account view [username] [password]\n' \
            '    View the information of an account.\n\n'     \
            'account change password [username] [old password] [new password]\n' \
            '    Create a new account (will also overwrite).\n\n'    \
            'reservation create [username] [ID] [day] [start time] [end time]\n'     \
            '    Attempt to create a reservation at the specified time.\n\n'    \
            'reservation view [ID]\n'     \
            '    View a reservation.\n\n'    \
            'reservation modify time [ID] [new day] [new start time] [new end time]\n'     \
            '    Attempt to modify a reservation.\n\n'    \
            'reservation cancel [ID]\n'     \
            '    Cancel a reservation.\n\n'    \
            'day list\n'     \
            '    List all of the initiated days.\n\n'    \
            'day view [day]\n'     \
            '    View the timeslot data from a day'    \
    
    @classmethod
    def dayList(self) -> str:
        '''
        Return a formatted list of filenames (day IDs) in the ./days directory
        '''
        s = 'Days initialized:\n'
        for item in DaysIntiliazed.days:
            s += f'{item}\n'
            
        return s
    
    @classmethod
    def dayView(self, ID: str) -> str:
        '''
        Return a formatted view of a specific day's timeslot data 
        
        Parameters
        -----------
        ID : str
            By default, the day number
        '''
        c_day = GarageManager.load_day(ID)
        return str(c_day)
    
    @classmethod
    def accountList(self) -> str:
        '''
        Returns a formatted list of filenames (usernames) in the ./accounts
        directory.
        '''
        s = 'Accounts initialized:\n'
        for item in AcctsInitiliazed.accts:
            s += f'{item}\n'
            
        return s
    
    @classmethod
    def accountView(self, username: str, password: str) -> str:
        '''
        Returns a formatted view of a specific account's data
        
        Parameters
        -----------
        
        '''
        return str(AccountManager.load_acct(username, password))
        
    @classmethod
    def accountCreate(self, username: str, password: str) -> str:
        '''
        Create a new account. Return str giving confirmation and account view
        
        Parameters
        -----------
        username : str
            Account should have this username
            
        password : str
            Account should have this password
        '''
        pass
    
    @classmethod
    def accountChangePassword \
        (self, username: str, old_pass: str, new_pass: str) -> str:
        '''
        Change the password of an account. Return a str giving confirmation
        
        Parameters
        -----------
        username : str
            Username of current account
        old_pass : str
            Old password
        new_pass : str
            New password
        '''
        c_account = AccountManager.load_acct(username, old_pass)
        success = AccountManager.change_password(c_account, old_pass, new_pass)
        return success 
    
    @classmethod
    def reservationCreate \
        (self, username: str, ID: str, day: str, s_time: str, e_time: str) -> str:
        '''
        Attempt to create a reservation. Return confirmation and the Res view
        
        Parameters
        -----------
        username : str
            The new owner of the new reservation
        ID : str
            The TODO starting from here
        '''
        pass
         
    
    @classmethod
    def reservationView(self, ID: str) -> str:
        '''
        Return a formatted string of a reservation's data
        
        Parameters
        -----------
        
        '''
        pass
    
    @classmethod
    def reservationRequestModifyTime \
        (self, ID: str, new_d: str, new_s: str, new_e: str) -> str:
        '''
        Attempt to modify the day, start, and end of a reservation. Return
        string with confirmtion & reservation view
        
        Parameters
        -----------
        
        '''
        pass
        
    
    @classmethod
    def reservationCancel(self, ID: str) -> str:
        '''
        Cancel a reservation. Return a string giving confirmation and Res view
        
        Parameters
        -----------
        
        '''
        pass


if __name__ == '__main__':
    AdminUI.initiateUI()