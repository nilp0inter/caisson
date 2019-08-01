import argparse

from caisson import constants


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog=constants.PROGRAM_NAME,
        description=constants.PROGRAM_DESCRIPTION)
    parser.add_argument("source", nargs="+")
    parser.add_argument("destination", nargs=1)
    return parser
