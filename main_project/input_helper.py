"""
This module provides a set of helper functions, to:
get_valid_input: validate user input that returns a number
get_valid_float_input: validate user input that returns a float
get_valid_string_input: validate user input that returns a string

Requirements
------------
Python 3.7 or higher.

Notes
-----
This module created as material for the phase 2 project for DM857, DS830 (2023). 
"""
import os
from typing import Optional

def get_valid_input(prompt: str, valid_input: str = None,  min: int=None, max: int=None) -> int:
    """This function checks to if the user input integer is valid. (To be used in input parameters)

    Parameters
    ----------
    prompt: str
        Prompt message for receiving user input. 
    valid_input_msg: Optional[str], default = None
        Will specify to the user, what input will be valid for where function is called
    min: Optional[int], default = None
        If provided, function will keep prompting user until user input > minimum
    max: Optional[int], default = None
        If provided, function will keep prompting user until user input < maximum
    """
    user_input = None
    getting_input = False

    while not getting_input:
        try:
            user_input = int(input(prompt))

            # Check for min
            if min:
                assert user_input >= min, f"Input is less than minimum ({min}). Please provide value between {min}-{max}"
                
            # Check for max
            if max:
                assert user_input <= max, f"Input is greater than maximum ({max}). Please provide value between {min}-{max}"
            
            # If everything is okay, break loop.
            getting_input = True

        except ValueError:
            print("Invalid input.")
            if valid_input: print(f"Valid input is: {valid_input}")
            print("Please try again.")
        except TypeError:
            print("Invalid operation.")
            if valid_input: print(f"Valid input is: {valid_input}")
            print("Please try again.")
        except KeyboardInterrupt:
            print("\nOperation interrupted by the user.")
            print("Do you want to exit program?")
            user_exit = get_valid_string_input("Yes or no (y/n): ", "Yes or no (y/n)", True)
            if user_exit == "yes" or user_exit == "y" or user_exit == "no" or user_exit == "n":
                quit()
            else:
                print("\n...Redirecting")
        except AssertionError as e:
            print(e)  # Print the error message from the failed assertion
            if valid_input: 
                print(f"Valid input is: {valid_input}")
            print("Please try again.")

    return user_input

def get_valid_float_input(prompt: str, valid_input: str = None, min: float=None, max: float=None) -> float:
    """This function checks if the user input float is valid. (To be used in input parameters)
    
    Parameters
    ----------
    prompt: str
        Prompt message for receiving user input. 
    valid_input_msg: Optional[str], default = None
        Will specify to the user, what input will be valid for where function is called
    min: Optional[float], default = None
        If provided, function will keep prompting user until user input > minimum
    max: Optional[float], default = None
        If provided, function will keep prompting user until user input < maximum
    """
    user_input = None
    getting_input = False

    while not getting_input:
        try:
            user_input = float(input(prompt))
            #if user_input.isdigit() == False: raise ValueError
            #round(float(user_input), 1)

            # Check for min
            if min:
                assert user_input >= min, f"Input is less than minimum ({min}). Please provide value between {min}-{max}"
                
            # Check for max
            if max:
                assert user_input <= max, f"Input is greater than maximum ({max}). Please provide value between {min}-{max}"
            
            # If everything is okay, break loop.
            getting_input = True

        except ValueError:
            print("Invalid input.")
            if valid_input: print(f"Valid input is: {valid_input}")
            print("Please try again.")
        except TypeError:
            print("Invalid operation.")
            if valid_input: print(f"Valid input is: {valid_input}")
            print("Please try again.")
        except KeyboardInterrupt:
            print("\nOperation interrupted by the user.")
            print("Do you want to exit program?")
            user_exit = get_valid_string_input("Yes or no (y/n): ", "Yes or no (y/n)", True)
            if user_exit == "yes" or user_exit == "y" or user_exit == "no" or user_exit == "n":
                quit()
            else:
                print("\n...Redirecting")
        except AssertionError as e:
            print(e)  # Print the error message from the failed assertion
            if valid_input: 
                print(f"Valid input is: {valid_input}")
            print("Please try again.")

    return user_input

def get_valid_string_input(prompt: str, valid_input: str = None, yes_no: bool=False) -> str:
    """This function checks if the user input string is valid.
    
    Parameters
    ----------
    prompt: str
        Prompt message for receiving user input. 
    valid_input_msg: Optional[str], default = None
        Will specify to the user, what input will be valid for where function is called
    yes_no: bool=False, default = None
        If True, function validates input as either yes or no answer (y/n).
    """
    getting_input = False
    user_input = None

    while not getting_input:
        try:
            user_input = input(prompt).strip().lower()
            assert isinstance(user_input, str), valid_input     # Check input is string
            assert not user_input.isdigit(), valid_input        # Check input is not a digit

            # Check yes_no
            if yes_no:
                correct = ["yes", "y", "no", "n"]
                assert user_input in correct, "Answer must be yes or no (y/n)"
                
            getting_input = True
        except ValueError:
            print("Invalid input.")
            if valid_input: print(f"Valid input is: {valid_input}")
            print("Please try again.")
        except TypeError:
            print("Invalid operation.")
            if valid_input: print(f"Valid input is: {valid_input}")
            print("Please try again.")
        except KeyboardInterrupt:
            print("\nOperation interrupted by the user.")
            print("Do you want to exit program?")
            user_exit = get_valid_string_input("Yes or no (y/n): ", "Yes or no (y/n)", True)
            if user_exit == "yes" or user_exit == "y" or user_exit == "no" or user_exit == "n":
                quit()
            else:
                print("\n...Redirecting")
        except AssertionError as e:
            print(e)  # Print the error message from the failed assertion
            if valid_input: 
                print(f"Valid input is: {valid_input}")
            print("Please try again.")

    return user_input

def get_valid_file(prompt: str, file_req: Optional[str]=None) -> str:
    """Keep prompting user for filepath until a valid filepath is provided
    
    Parameters
    ---------
    prompt: str
        prompt message to display to user while getting input
    file_req: Optional[str], default = None
        If provided, will let user know the requirements for the file they are prompted for
    """

    getting_file = True

    while getting_file:
        file_path = input(prompt)

        if os.path.isfile(file_path):
            print(f"The filepath '{file_path}' is a valid file.")
            getting_file = False
        else:
            print(f"The filepath '{file_path}' is not a valid file.")
            if file_req: print("File must adhere to the following:", file_req)
 