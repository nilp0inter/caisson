import argparse
import sys

from caisson import constants
from caisson import decompressors
from caisson.configuration import Overwrite


class ListDecompressorsAction(argparse.Action):
    def __call__(self, *_, **__):
        for decompressor, available in decompressors.availability():
            print(decompressor.name + ':', decompressor.command)
        sys.exit(0)


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog=constants.PROGRAM_NAME,
        description=constants.PROGRAM_DESCRIPTION)
    loglevel = parser.add_mutually_exclusive_group()
    loglevel.add_argument("-q", "--quiet", action="store_true")
    loglevel.add_argument("-v", "--verbose", action="store_true")
    loglevel.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--list", action=ListDecompressorsAction, nargs=0)

    parser.add_argument("-o", "--overwrite", default=Overwrite.ASK,
                        type=Overwrite,
                        action="store",
                        choices=list(Overwrite))

    parser.add_argument("source", nargs="*")
    parser.add_argument("destination", nargs=1)
    return parser
