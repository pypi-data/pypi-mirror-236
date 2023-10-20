import re
import urllib.request
from functools import cache
from typing import Iterator

import advent
from advent.errors import handle_error


@cache
def get_puzzle_input(year: int, day: int) -> str:
    """Get your puzzle input for a given year and day"""

    req = urllib.request.Request(advent.URL.format(year, day), headers=advent.HEADERS)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
        handle_error(err)
    data = response.read().decode()
    return data


def get_ints(string: str) -> Iterator[int]:
    """Extract and yield integers from a given string"""

    for n in re.finditer(r"-?\d+", string):
        yield int(n.group())
