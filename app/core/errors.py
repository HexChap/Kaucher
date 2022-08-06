from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Response


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


class HTTPException(KaucherException):
    def __init__(
            self,
            response: ["Response"],
    ):
        self.response = response
        self.code = response.status_code
        self.message = response.text


class Unauthorized(HTTPException):
    """
    Exception that's raised for when status code 401 occurs.

    Subclass of :exc:`HTTPException`
    """

    pass


class Forbidden(HTTPException):
    """
    Exception that's raised for when status code 403 occurs.

    Subclass of :exc:`HTTPException`
    """

    pass


class NotFound(HTTPException):
    """
    Exception that's raised for when status code 404 occurs.

    Subclass of :exc:`HTTPException`
    """

    pass


class ServerError(HTTPException):
    """
    Exception that's raised for when a 500 range status code occurs.

    Subclass of :exc:`HTTPException`.
    """

    pass


class UnprocessableEntity(HTTPException):
    """
    Exception that's raised for when a 422 range status code occurs.

    Subclass of :exc:`HTTPException`.
    """

    pass
