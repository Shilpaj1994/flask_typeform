"""
validate_credentials.py: Module to validate the username and password of the user
Author: Shilpaj Bhalerao
Date: Aug 26, 2021
"""
# Standard Library Imports

# Third-Party Imports
import bcrypt

# Local Imports
from ..utilities import custom_exceptions as exceptions


def validate_username(username):
    with open('source_code/login/credentials.txt', 'r') as file:
        _username = file.readline()
    _username = _username.split("\n")[0]

    if bcrypt.checkpw(username, _username):
        return True
    raise exceptions.ValidationError("Invalid Username. Please check the Username")


def validate_password(password):
    with open('source_code/login/credentials.txt', 'r') as file:
        _ = file.readline()
        _password = file.readline()
    _password = _password.split("\n")[0]

    if bcrypt.checkpw(password, _password):
        return True
    raise exceptions.ValidationError("Invalid Password. Please check the Password")
