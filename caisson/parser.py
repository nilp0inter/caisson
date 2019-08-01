import argparse
import sys

from caisson import constants
from caisson import decompressors


class ListDecompressorsAction(argparse.Action):
    def __call__(self, *_, **__):
        for decompressor, available in decompressors.availability():
            print(decompressor.name + ':', decompressor.command)
        sys.exit(0)


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog=constants.PROGRAM_NAME,
        description=constants.PROGRAM_DESCRIPTION)
    parser.add_argument("--list", action=ListDecompressorsAction, nargs=0)
    parser.add_argument("source", nargs="+")
    parser.add_argument("destination", nargs=1)
    return parser
