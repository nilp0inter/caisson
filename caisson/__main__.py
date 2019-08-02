import logging

from caisson.decompressors import get_decompressors
from caisson.parser import build_arg_parser
from caisson.io import decompress, remove_compressed_files


def caisson(sources, destination, configuration):
    decompressors = get_decompressors(configuration)
    decompress(sources, destination, decompressors)
    decompress([destination], destination, decompressors, subdir=False)
    remove_compressed_files(destination, decompressors)


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.quiet:
        logging.basicConfig(level=logging.CRITICAL, format="%(message)s")
    elif args.verbose:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
    elif args.debug:
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")

    caisson(sources=args.source,
            destination=args.destination[0],
            configuration=args)


if __name__ == "__main__":
    main()
