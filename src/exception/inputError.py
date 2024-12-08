class ClientError(Exception):
    """
    Custom exception class for client errors.

    Attributes:
        message (str): The error message to display.
        status_code (int): The HTTP status code associated with the error (default is 400).
    """
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.name = "ClientError"

    def __str__(self):
        # Customize the string representation of the error
        return f"{self.name}: {self.message} (status_code: {self.status_code})"