import urllib.error


class PuzzleNotFoundError(Exception):
    """Exception raised when a requested Advent of Code puzzle is not found."""


class InvalidSessionIDError(Exception):
    """Exception raised when an invalid session ID is provided."""


def handle_error(error: urllib.error.HTTPError) -> None:
    match error.code:
        case 404:
            raise PuzzleNotFoundError(
                "Puzzle input for a given year and day isn't found."
            )
        case 400:
            raise InvalidSessionIDError("Session ID has expired or is invalid.")
        case _:
            raise
