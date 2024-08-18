import re


def validate_input(user_input):
    """
    Validates that the input contains only letters, numbers, and 
    allowed non-dangerous symbols.
    
    Allowed symbols: . - _ @ ! # $ % & * ?

    Parameters:
        user_input (str): The input string to be validated.
    
    Returns:
        bool: True if the input is valid, False otherwise.
    """
    pattern = re.compile(r'^[\w\s.-_@!#$%&*?]*$')
    
    if pattern.match(user_input):
        return True
    return False