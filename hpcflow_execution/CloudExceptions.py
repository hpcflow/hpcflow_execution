class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class UserInputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class OneDriveAuthError(Error):
    """Exception raised if OneDrive not authorized"""
