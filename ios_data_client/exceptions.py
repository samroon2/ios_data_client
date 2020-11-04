"""
ios_data_client.exceptions
~~~~~~~~~~~~~
This module contains custom exceptions.
"""


class UndefinedGenre(Exception):
    """
    Exception for when a cardholder attempts to overdraw an account.
    """

    def __init__(self, genre, genres):
        self.message = f"The genre: {genre} is not offered by the store, please enter one of the following: {[x + ' \n ' for x in genres.keys()]}"

    def __str__(self):
        return repr(self.message)