class KaucherException(Exception):
    pass


class UserExistsError(KaucherException):
    """
    Raised after checking by username and email, if they are already in the database
    """
    pass


class WrongVersionError(KaucherException):
    pass


class ModpackDoesNotExists(KaucherException):
    pass
