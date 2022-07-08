class KaucherException(Exception):
    pass


class UserExists(KaucherException):
    """
    Raised after checking by username and email, if they are already in the database
    """
    pass
