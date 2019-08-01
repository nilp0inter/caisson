from abc import ABCMeta, abstractmethod, abstractstaticmethod
import argparse
import os
import re
import shlex
import shutil
import subprocess


PROGRAM_NAME = "caisson"
PROGRAM_DESCRIPTION = "Recursively decompress files"


class Decompressor(metaclass=ABCMeta):
    def __init__(self, configuration):
        self.configuration = configuration
        self.__configure__()

    def __configure__(self):
        pass

    @classmethod
    def is_available(cls):
        return cls.command is not None

    @abstractmethod
    def can_decompress(self, path):
        pass

    @abstractmethod
    def decompress(self, path, destination):
        pass


class Unzip(Decompressor):
    command = shutil.which("unzip")

    def can_decompress(self, path):
        return path.lower().endswith('.zip')

    def decompress(self, path, destination):
        args = [self.command,
                '-d', destination,
                path]
        print(args)
        result = subprocess.run(args)
        result.check_returncode()


class Unrar(Decompressor):
    command = shutil.which("unrar")

    def can_decompress(self, path):
        path = path.lower()
        return (re.match("\.r0+1$", path)
                or path.endswith(".part1.rar")
                or (not re.match("part[0-9]+\.rar$", path)
                    and path.endswith(".rar")))

    def decompress(self, path, destination):
        args = [self.command,
                'x', path,
                destination]
        print(args)
        result = subprocess.run(args)
        result.check_returncode()


class SevenZip(Decompressor):
    command = shutil.which("7z")

    def can_decompress(self, path):
        return path.lower().endswith('.7z')

    def decompress(self, path, destination):
        args = [self.command,
                'x', '-o' + destination,
                path]
        print(args)
        result = subprocess.run(args)
        result.check_returncode()


DECOMPRESSORS = [decompressor
                 for decompressor in Decompressor.__subclasses__()
                 if decompressor.is_available()]


def final_path(source, destination):
    return os.path.join(destination, os.path.basename(source))


def decompress_file(source, destination, decompressors):
    print(source, destination)
    for decompressor in decompressors:
        if decompressor.can_decompress(source):
            new_destination = final_path(source, destination) + ".content"
            os.makedirs(new_destination, exist_ok=True)
            try:
                decompressor.decompress(source, new_destination)
            except Exception as e:
                print(e)
            # os.unlink(source)
            break
    else:
        if source == final_path(source, destination):
            pass
        else:
            try:
                shutil.copy(source, destination)
            except PermissionError:
                pass



def decompress(sources, destination, decompressors, subdir=True):
    for source in sources:
        if os.path.isdir(source):
            if subdir:
                new_destination = final_path(source, destination)
                os.makedirs(new_destination, exist_ok=True)
            else:
                new_destination = destination
            for entry in os.scandir(source):
                if entry.is_file():
                    decompress_file(entry.path, new_destination, decompressors)
                else:
                    decompress([entry.path], new_destination, decompressors)
        else:
            decompress_file(source, destination, decompressors)


def remove_compressed_files(path, decompressors):
    for entry in os.scandir(path):
        if entry.is_file():
            for decompressor in decompressors:
                if decompressor.can_decompress(entry.path):
                    print("Removing", entry.path)
                    os.unlink(entry.path)
        elif entry.is_dir():
            remove_compressed_files(entry.path, decompressors)
        else:
            pass


def caisson(sources, destination, configuration):
    decompressors = [decompressor(configuration)
                     for decompressor in DECOMPRESSORS]
    decompress(sources, destination, decompressors)
    decompress([destination], destination, decompressors, subdir=False)
    remove_compressed_files(destination, decompressors)


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description=PROGRAM_DESCRIPTION)
    parser.add_argument("source", nargs="+")
    parser.add_argument("destination", nargs=1)
    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    caisson(sources=args.source,
            destination=args.destination[0],
            configuration=dict())


if __name__ == "__main__":
    main()
