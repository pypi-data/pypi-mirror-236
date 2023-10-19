import inspect
from ._constants_manager import RuntimeConstants

def print_output(message):
    '''based on the output flag, print out the param passed in'''
    if RuntimeConstants.VERBOSE_MODE:
        # Get the name of the calling method
        caller_frame = inspect.currentframe().f_back
        caller_name = caller_frame.f_code.co_name

        # Get the name of the calling class (if available)
        try:
            caller_class = caller_frame.f_locals['self'].__class__.__name__
            print(f"{caller_class}.{caller_name}: {message}")
        except KeyError:
            # If 'self' is not defined in the calling method, print only the method name
            print(f"{caller_name}: {message}")