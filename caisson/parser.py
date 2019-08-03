import argparse
import sys

import caisson
from caisson import decompressors
from caisson.configuration import Overwrite


class ListDecompressorsAction(argparse.Action):
    def __call__(self, *_, **__):
        for decompressor, available in decompressors.availability():
            print(decompressor.name + ':', decompressor.command)
        sys.exit(0)


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog=caisson.__name__,
        description=caisson.__description__)
    loglevel = parser.add_mutually_exclusive_group()
    loglevel.add_argument("-q", "--quiet", action="store_true",
                          help="don't print any log")
    loglevel.add_argument("-v", "--verbose", action="store_true",
                          help="print a moderate log")
    loglevel.add_argument("-d", "--debug", action="store_true",
                          help="print a debugging log")
    parser.add_argument("--list", action=ListDecompressorsAction, nargs=0,
                        help="print list of available decompressors")

    parser.add_argument("-o", "--overwrite", default=Overwrite.ASK,
                        type=Overwrite,
                        action="store",
                        choices=list(Overwrite))

    parser.add_argument("source", nargs="*",
                        help="file or directory to be extracted")
    parser.add_argument("destination", nargs=1,
                        help="destination for extracted files")
    return parser
