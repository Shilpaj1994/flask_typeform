"""
Module containing Custom Exceptions for the application
Author: Shilpaj Bhalerao
Date: Aug 24, 2021
"""
# Standard Library Imports


class ValidationError(Exception):
    def __init__(self, message="Invalid Credentials"):
        super().__init__(message)
