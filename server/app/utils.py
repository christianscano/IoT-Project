def user_role_to_code(str_role):
    """
    Convert a string role to the integer part.
    """
    if str_role == 'admin':
        return 0
    elif str_role == 'security':
        return 1
    elif str_role == 'sysadmin':
        return 2
    else:
        return -1

def code_to_user_role(role):
    """
    Convert an integer role to the string part.
    """
    if role == 0:
        return 'admin'
    elif role == 1:
        return 'security'
    elif role == 2:
        return 'sysadmin'
    else:
        return 'unknown'