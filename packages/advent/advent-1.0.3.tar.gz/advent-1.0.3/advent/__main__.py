import sys

from advent import functions, parser


def main():
    args = parser.parse_arguments()
    try:
        data = functions.get_puzzle_input(args.year, args.day)
        if args.output_file:
            args.output_file.write_text(data)
        else:
            print(data)
    except Exception as ex:
        print(ex)
        sys.exit(1)


if __name__ == "__main__":
    main()
