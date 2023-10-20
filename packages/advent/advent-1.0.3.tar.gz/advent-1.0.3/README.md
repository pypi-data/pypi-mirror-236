# Advent

Advent is a Python package that contains useful functions for Advent of Code eg getting puzzle input or getting all integers present in a string.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install advent.

```bash
pip install advent
```

## Setup

To use this tool you need to create a .env file in your project directory and place there your session ID.

```
# .env file
SESSION_ID="your-session-id"
```
 It's stored in a cookie called session. You can find it by entering Inspect Mode in your browser, Application -> Cookies. Check out picture below:
![where to find session id](https://github.com/ravilnicki/advent/blob/main/session_id.png?raw=true)

## Usage

```python
from advent.functions import get_puzzle_input, get_ints

# returns "B X\nB Y\nA Y\nB Y\n..."
get_puzzle_input(2022, 22)

# returns [2, 3]
list(get_ints("Point x=2, y=3"))
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)