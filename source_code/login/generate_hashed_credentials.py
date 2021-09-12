"""
Module to generate the hashed Email ID and Password
Author: Shilpaj Bhalerao
Date: Aug 24, 2021
"""
# Standard Library Imports
from getpass import getpass

# Third-Party Imports
import bcrypt


def gen_hashed_mail_id():
    """
    Function to generate hashed Email ID
    :return: Hashed Email ID
    """
    master_key = getpass("Enter your Email Address: ")
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(master_key.encode('utf-8'), salt)
    return hashed_password


def gen_hashed_password():
    """
    Function to generate hashed Password
    :return: Hashed Password
    """
    master_key = getpass("Enter Password: ")
    salt = bcrypt.gensalt()

    hashed_id = bcrypt.hashpw(master_key.encode('utf-8'), salt)
    return hashed_id


if __name__ == '__main__':
    with open('credentials.txt', 'w') as file:
        mail_id = gen_hashed_mail_id()
        password = gen_hashed_password()
        file.write(mail_id + "\n")
        file.write(password)
