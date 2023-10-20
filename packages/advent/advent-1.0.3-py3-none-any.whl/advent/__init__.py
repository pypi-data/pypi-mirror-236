import os

import dotenv

dotenv_path = dotenv.find_dotenv(usecwd=True)
dotenv.load_dotenv(dotenv_path)

__version__ = "1.0.3"

URL = "https://adventofcode.com/{}/day/{}/input"
SESSION_ID = os.environ["SESSION_ID"]
HEADERS = {
    "User-Agent": "https://github.com/ravilnicki/advent by ravilnicki@gmail.com",
    "Cookie": "session=" + SESSION_ID,
}
