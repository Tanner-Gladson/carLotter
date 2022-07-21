from ReservationsAPI import ReservationsAPI
from AccountModule import AccountManager


class switchAccountCommands():
    
    '''
    A static class for switching between several account-related commands.
    
    Methods
    --------
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
    @staticmethod
    def account_list() -> str:
        '''
        returns a string of accounts that have been initiated. Or a string
        detailing why the command failed.
        '''
        pass
    
    
    @staticmethod
    def view_account(username: str) -> str:
        '''
        Return a formatted string of an account's details or a failure string.
        '''
        pass
    
    
    @staticmethod
    def create_account(username: str, password: str) -> str:
        '''
        Create an account. Returns a string giving the account details. 
        Or returns a string detailing why the command failed.
        '''
        pass
    
    
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
        pass



class switchReservationCommands():
    '''
    A static class for switching between reservation related commands
    
    Methods
    --------
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
    
    @staticmethod
    def create_reservation(username: str, start_time: str, end_time: str) -> str:
        '''
        Creates a new reservation and returns confirmation, or returns
        description of failure.
        '''
        pass
    
    
    
    @staticmethod
    def view_reservation(ID: str) -> str:
        '''
        Returns a formatted string with reservation details, or returns a
        string describing failure.
        '''
        pass
    
    
    @staticmethod
    def modify_reservation_time\
        (ID: str, new_day: str, new_start_time: str, new_end_time: str) -> str:
        '''
        Modifies the time of a reservation & returns confirmation. Or, returns
        description of failure.
        '''
        pass
    
    
    
    @staticmethod
    def cancel_reservation(ID: str) -> str:
        '''
        Cancels a reservation. Returns confirmation of failure.
        '''
        pass
    
    
class switchDayCommands():
    '''
    A static class for switching between day-related user commands.
    
    Methods
    --------
    day_list() -> str
        Returns a string of all the days that have files
        
    view_day(day_ID: str) -> str
        Returns a formatted view of a Day's details, or a failure string
    
    '''
    
    @staticmethod
    def day_list() -> str:
        '''
        Returns a string of all the days that have files
        '''
        pass
    
    
    
    @staticmethod
    def view_day(day_ID: str) -> str:
        '''
        Returns a formatted view of a Day's details, or a failure string
        '''
        pass

class AdminUI():
    '''
    The primary class for initiating an admin interface.
    
    Methods
    -------
    initiate_administrator_UI() -> None
        A function that repeatedly prompts user for commands.
    '''
    
    pass