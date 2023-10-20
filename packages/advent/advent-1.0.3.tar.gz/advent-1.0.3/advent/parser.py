from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from pathlib import Path


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        prog="advent",
        description="""
                 _                 _
        /\      | |               | |  
       /  \   __| |_   _____ _ __ | |_ 
      / /\ \ / _` \ \ / / _ \ '_ \| __|
     / ____ \ (_| |\ V /  __/ | | | |_ 
    /_/    \_\__,_| \_/ \___|_| |_|\__|

Get your puzzle input for a given year and day!

By default, the input data will be printed to the console.
However, you can specify the --output_file option to save 
the data to a file instead.""",
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "year",
        type=int,
        help="year of the puzzle",
    )
    parser.add_argument(
        "day",
        type=int,
        help="day of the puzzle",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        help="name of the output file",
    )
    args = parser.parse_args()
    return args
