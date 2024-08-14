def user_role_to_code(role):
    """
    Convert a string role to the integer part.

    Parameters:
        str_role (str): The string role to be converted.
    
    Returns:
        int: The integer representation of the role.
    """
    if role == 'admin':
        return 0
    elif role == 'security':
        return 1
    elif role == 'sysadmin':
        return 2
    else:
        return -1

def code_to_user_role(role):
    """
    Convert an integer role to the string part.

    Parameters:
        role (int): The integer role to be converted.
    
    Returns:
        str: The string representation of the role.
    """
    if role == 0:
        return 'admin'
    elif role == 1:
        return 'security'
    elif role == 2:
        return 'sysadmin'
    else:
        return 'unknown'