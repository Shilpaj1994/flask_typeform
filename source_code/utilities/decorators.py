"""
Module containing utility decorators used in the code
Author: Shilpaj Bhalerao
Date: Aug 24, 2021
"""
# Standard Library Imports
import os
from functools import wraps

# Third-Party Imports
from flask import session, redirect, url_for

# Local Imports


def add_method(cls):
    """
    Decorator Factory to add the function to a class
    :param cls: Class to which the function need to be added
    """
    def decorator(func):
        """
        Decorator for the decorator factory
        :param func: Function to be added to the class
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            """
            Wrapper to add function as method of the class
            :param self: Needed for class implementation
            :param args: Arguments of the function
            :param kwargs: Keyword arguments of the function
            :return: Function output
            """
            return func(*args, **kwargs)

        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        setattr(cls, func.__name__, wrapper)

        # returning func means func can still be used normally
        return func
    return decorator


def login_required(func):
    def inner(*args, **kwargs):
        if not session['logged_in']:
            return redirect(url_for('login'))
        else:
            return func(*args, **kwargs)
    inner.__name__ = func.__name__
    return inner


if __name__ == '__main__':
    pass
