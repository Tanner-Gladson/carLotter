from ReservationsAPI import ReservationsAPI
from AccountModule import AccountManager
from TimeUtilities import TimeRange


class AccountCommands():
    
    '''
    A static class for switching between several account-related commands.
    
    Methods
    --------
    switch_commands(self, user_command: List[str]) -> str:
        Acts as a relay, directing the user's command list to the appropriate
        command. Returns the resulting output string.
        
    account_list() -> str:
        returns a string of accounts that have been initiated. Or a string
        detailing why the command failed.
        
    view_account(username: str) -> str:
        Return a formatted string of an account's details or a failure string.
        
    create_account(username: str, password: str) -> str:
        Create an account. Returns a string giving the account details. 
        Or returns a string detailing why the command failed.
        
    change_account_password\
        (username: str, old_pass: str, new_pass: str) -> str:
        Changes an account password, returning confirmation or failure.
    
    '''
    @classmethod
    def switch_commands(self, user_command: list[str]) -> str:
        '''
        Acts as a relay, directing the user's command to the appropriate
        command. Returns the resulting output string.
        
        Parameters
        ----------
        user_command : list[str]
            The users command, split by spaces
        '''
        if len(user_command) < 2:
            out_string = 'Command not found. Type "help" for more info'
        
        elif user_command[1] == 'list':
            if len(user_command) == 2:
                out_string = self.account_list()
                
            else:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "account list"'
        
        elif user_command[1] == 'create':
            if len(user_command) == 4:
                out_string = self.create_account(user_command[2], user_command[3])
                
            else:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "account create [username] [password]"'
            
        elif user_command[1] == 'view':
            if len(user_command) == 3:
                out_string = self.view_account(user_command[2])
                
            else:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "Try: "account view [username] [password]"'
            
        elif user_command[1] == 'change' and user_command[2] == 'password':
            if len(user_command) == 6:
                out_string = self.change_account_password\
                    (user_command[3], user_command[4], user_command[5])
                    
            else:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "account change password [username] [old password] [new password]"'
            
        else: 
            out_string = f'Command not found. Type "help" for more info'
            
        return out_string
    
    @staticmethod
    def account_list() -> str:
        '''
        returns a string of accounts that have been initiated. Or a string
        detailing why the command failed.
        '''
        return AccountManager.list_accounts_initialized()
    
    
    @staticmethod
    def view_account(username: str) -> str:
        '''
        Return a formatted string of an account's details or a failure string.
        '''
        if AccountManager.account_exists(username):
            return str(AccountManager.load_acct_from_file(username))
        else:
            return f'Account with username "{username}" could not be found\n\n'\
                'To list the created accounts, use "account list"'
    
    
    @staticmethod
    def create_account(username: str, password: str) -> str:
        '''
        Create an account. Returns a string giving the account details. 
        Or returns a string detailing why the command failed.
        '''
        if password == '':
            return f'Error: account password must not be empty'
        elif not username.isalnum():
            return f'Error: username should be an alpha-numeric string'
        elif not password.isalnum():
            return f'Error: password should be an alpha-numeric string'
        elif username == '':
            return f'Error: account username must not be empty'
        elif AccountManager.account_exists(username):
            return f'Error: that account name is already taken'
        else:
            # Create account, file, and return a formatted string as confirm.
            return str(AccountManager.create_acct(username, password))
    
    
    @staticmethod
    def change_account_password\
        (username: str, old_pass: str, new_pass: str) -> str:
        '''
        Changes an account password, returning confirmation or failure.
        
        Parameters
        ----------
        username : str
            The username of the account you're changing
            
        old_pass : str
            The current password of the account
            
        new_pass : str
            The desired new password of the account
        '''
        # Input validation
        if not new_pass.isalnum():
                return f'Error: new password should be an alpha-numeric string'
        
        if AccountManager.account_exists(username):
            c_acct = AccountManager.load_acct_from_file(username)
            if AccountManager.try_change_password(c_acct, old_pass, new_pass):
                return f'Password successfully changed!'
            else:
                return f'Error: incorrect previous password'
        else:
            return f'Account with username "{username}" could not be found\n\n'\
                'To list the created accounts, use "account list"'


class ReservationCommands():
    '''
    A static class for switching between reservation related commands
    
    Methods
    --------
    switch_commands(self, user_command: List[str]) -> str:
        Acts as a relay, directing the user's command list to the appropriate
        command. Returns the resulting output string.
        
    create_reservation(username: str, start_time: str, end_time: str) -> str:
        Creates a new reservation and returns confirmation, or returns
        description of failure.
        
    view_reservation(ID: str) -> str:
        Returns a formatted string with reservation details, or returns a
        string describing failure.
        
    modify_reservation_time\
        (ID: str, new_day: str, new_start_time: str, new_end_time: str) -> str
        Modifies the time of a reservation & returns confirmation. Or, returns
        description of failure.
        
    cancel_reservation(ID: str) -> str:
        Cancels a reservation. Returns confirmation of failure.
    
    '''
    @classmethod
    def switch_commands(self, user_command: list[str]) -> str:
        '''
        Acts as a relay, directing the user's command to the appropriate
        command. Returns the resulting output string.
        
        Parameters
        ----------
        user_command : list[str]
            The users command, split by spaces
        '''
        
        if len(user_command) < 2:
            out_string = 'Command not found. Type "help" for more info'
        
        elif user_command[1] == 'create':
            if len(user_command) == 7:
                out_string = self.create_reservation\
                (user_command[2], user_command[3], user_command[4], user_command[5], user_command[6])
                
            else:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "reservation create [username] [ID] [day] [start time] [end time]"'
        
        elif user_command[1] == 'view':
            if len(user_command) == 3:
                out_string = self.view_reservation(user_command[2])
                
            else:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "reservation view [ID]"'
            
        elif user_command[1] == 'cancel':
            if len(user_command) == 3:
                out_string = self.cancel_reservation(user_command[2])
                
            else:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "reservation cancel [ID]"'
            
        elif user_command[1] == 'modify' and user_command[2] == 'time':
            if len(user_command) == 7:
                out_string = self.modify_reservation_time\
                (user_command[3], user_command[4], user_command[5], user_command[6])
                
            else:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "reservation modify time [ID] [new day] [new start time] [new end time]"'
            
        else: 
            out_string = f'Command not found. Type "help" for more info'
            
        return out_string
    
    
    @staticmethod
    def create_reservation\
            (username: str, res_ID: str, day: str, start_time: str, end_time: str) -> str:
        '''
        Creates a new reservation and returns confirmation, or returns
        description of failure.
        
        '''
        
        # Perform input validation
        if not AccountManager.account_exists(username):
            return f'Error: account with username "{username}" could not be found.\n\n'\
                'Try using "account list"'
        
        if ReservationsAPI.res_exists(res_ID):
            return f'Error: reservation with ID "{res_ID}" already exists'
        
        if len(res_ID) != 2:
            return f'Error: the reservation ID must be 2 characters. I am working\n'\
                'to remove this restriction.'
        
        if not res_ID.isalnum():
            return f'Error: reservation ID should be an alpha-numeric string'
        
        try:
            day = int(day)
            if day < 0 or day > 365:
                return 'You can only make reservations from days 0-365. Please try again.'
        except:
            return f'Error: day number "{day}" could not be converted to an integer.'
        
        # Ensure requested time range is valid
        try:
            s = int(start_time)
            e = int(end_time)
            
            if s > e:
                return f'Error: start time must be less than the end time'
            elif (s not in range(0, 24)) or (e not in range(1, 25)):
                return f'Error: The start and end times must be from 0-23 or 1-24, respectively.'
            
            tRange = TimeRange(string = None, start=s, end=e)
        except:
            return f'Error: a TimeRange could not be created from {start_time} to {end_time}.\n\n'\
                'The start and end times must be integers from 0-23 or 1-24, respectively.'
        
        # Attempt to create the reservation
        if ReservationsAPI.try_create_res(res_ID, username, day, tRange):
            
            c_acct = AccountManager.load_acct_from_file(username)
            c_res = ReservationsAPI.get_res_from_file(res_ID)
            AccountManager.add_reservation_to_acct(c_acct, c_res)
            
            return 'Successfully created the reservation! Details below.\n\n'\
                f'{ReservationsAPI.get_res_from_file(res_ID)}\n'\
                f'The availability on day {day} is now:\n\n'\
                f'{ReservationsAPI.get_day_from_file(day).timeslots_to_string()}'
        else:
            return 'Could not create reservation. Time slots likely unavailable.'
            
    
    
    @staticmethod
    def view_reservation(ID: str) -> str:
        '''
        Returns a formatted string with reservation details, or returns a
        string describing failure.
        '''
        if ReservationsAPI.res_exists(ID):
            return str(ReservationsAPI.get_res_from_file(ID))
        else:
            return f'Reservation with ID "{ID}" could not be found'
    
    
    @staticmethod
    def modify_reservation_time\
        (res_ID: str, new_day: str, new_start_time: str, new_end_time: str) -> str:
        '''
        Modifies the time of a reservation & returns confirmation. Or, returns
        description of failure.
        '''
        if not ReservationsAPI.res_exists(res_ID):
            return f'Error: reservation with ID "{res_ID}" does not exist.\n\n'\
        
        try:
            new_day = int(new_day)
            if new_day < 0 or new_day > 365:
                return 'You can only make reservations from days 0-365. Please try again.'
        except:
            return f'Error: day number "{new_day}" could not be converted to an integer.'
        
        # Ensure requested time range is valid
        try:
            s = int(new_start_time)
            e = int(new_end_time)
            
            if s > e:
                return f'Error: start time must be less than the end time'
            elif (s not in range(0, 24)) or (e not in range(1, 25)):
                return f'Error: The start and end times must be from 0-23 or 1-24, respectively.'
            
            new_tRange = TimeRange(string = None, start=s, end=e)
        except:
            return f'Error: a TimeRange could not be created from {new_start_time} to {new_end_time}.\n\n'\
                'The start and end times must be integers from 0-23 or 1-24, respectively.'
        
        if ReservationsAPI.try_modify_res(res_ID, new_day, new_tRange):
            return 'Successfully modified the reservation! Details below.\n\n'\
                f'{ReservationsAPI.get_res_from_file(res_ID)}\n'\
                f'The availability on day {new_day} is now:\n\n'\
                f'{ReservationsAPI.get_day_from_file(new_day).timeslots_to_string()}'
        else:
            return 'The reservation could not be modified to this time. Please\n'\
                'check if the requested time range is available using "day view [day].'
    
    
    @staticmethod
    def cancel_reservation(ID: str) -> str:
        '''
        Cancels a reservation. Returns confirmation of failure.
        '''
        if ReservationsAPI.res_exists(ID):
            ReservationsAPI.cancel_res(ID)
            return f'Reservation successfully cancelled!'
        else:
            return f'Reservation with ID "{ID}" could not be found'
    
    
class DayCommands():
    '''
    A static class for switching between day-related user commands.
    
    Methods
    --------
    switch_commands(self, user_command: List[str]) -> str:
        Acts as a relay, directing the user's command list to the appropriate
        command. Returns the resulting output string.
        
    day_list() -> str
        Returns a string of all the days that have files
        
    view_day(day_ID: str) -> str
        Returns a formatted view of a Day's details, or a failure string
    
    '''
    @classmethod
    def switch_commands(self, user_command: list[str]) -> str:
        '''
        Acts as a relay, directing the user's command to the appropriate
        command. Returns the resulting output string.
        
        Parameters
        ----------
        user_command : list[str]
            The users command, split by spaces
        '''
        if len(user_command) < 2:
            out_string = 'Command not found. Type "help" for more info'
        
        elif user_command[1] == 'list':
            if len(user_command) == 2:
                out_string = self.day_list()
                
            else:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "day list"'
        
        elif user_command[1] == 'view':
            if len(user_command) == 3:
                out_string = self.view_day(user_command[2])
                
            else:
                out_string = 'Wrong number of arguments for this command.\n\n' \
                    'Try: "day view [day]"'
                    
        else: 
            out_string = f'Command not found. Type "help" for more info'
            
        return out_string            
        
    @staticmethod
    def day_list() -> str:
        '''
        Returns a string of all the days that have files
        '''
        return ReservationsAPI.list_days_initialized()
    
    @staticmethod
    def view_day(day_ID: str) -> str:
        '''
        Returns a formatted view of a Day's details, or a failure string
        '''
        if ReservationsAPI.day_exists(day_ID):
            return str(ReservationsAPI.get_day_from_file(day_ID))
        else:
            return f'Day with ID "{day_ID}" could not be found.\n\n'\
                'To see days initialized, use "day list"'


class AdminUI():
    '''
    The primary class for initiating an admin interface.
    
    Methods
    -------
    initiate_administrator_UI(self) -> None
        A function that repeatedly prompts user for commands.
    
    switch_user_command(self, split_command_str) -> str:
        Relays user command to proper functions, and returns the response
        as a string
    
    get_ui_help() -> str:
        Returns a string of commands executable by user.
    
    '''
    @classmethod
    def initiate_administrator_UI(self) -> None:
        '''
        Repeatedly prompts user for command until quit. Relays user
        commands to appropriate categories for handling.
        '''
        
        ui_active = True
        print('=======================================================================')
        print('          Welcome to Car Lotter! Type "help" to see commands.')
        print('=======================================================================')
        print()
        
        while ui_active:
            print()
            print()
            user_in = input(f'>>> Enter command: ')
            print('-----------------------------------------------------------------------')
            print()
            command = user_in.split(' ')
            
            if command[0] == 'quit':
                break
            else:
                print(self.switch_user_command(command))
                print()
            
    @classmethod
    def switch_user_command(self, command) -> str:
        '''
        Relays user command to proper functions, and returns the response
        as a string
        
        Parameters
        -----------
        command : List[str]
            A list of the user's input strings, split by spaces
            
        '''
        
        if command[0] == 'help':
            return self.get_ui_help()
        
        elif command[0] == 'account':
            pass
            return AccountCommands.switch_commands(command)
        
        elif command[0] == 'reservation':
            pass
            return ReservationCommands.switch_commands(command)
        
        elif command[0] == 'day':
            pass
            return DayCommands.switch_commands(command)
        
        else:
            return 'Command not found. Type "help" for more info'
    
    @classmethod
    def get_ui_help(self) -> str:
        '''
        Returns a string of commands executable by user.
        '''
        return f'help\n    Print a list of commands.\n\n'\
            'account list\n' \
            '     List all the account usernames.\n\n' \
            'account create [username] [password]\n' \
            '    Create a new account.\n\n'  \
            'account view [username]\n' \
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
            '    View the timeslot data from a day'


if __name__ == '__main__':
    AdminUI.initiate_administrator_UI()