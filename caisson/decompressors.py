from abc import ABCMeta, abstractmethod, abstractproperty
import subprocess
import shutil
import re


class Decompressor(metaclass=ABCMeta):
    command = None

    @abstractproperty
    def name(self):
        pass

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
    name = "unzip"

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
    name = "unrar"

    def can_decompress(self, path):
        path = path.lower()
        return (re.match(r"\.r0+1$", path)
                or path.endswith(".part1.rar")
                or (not re.match(r"part[0-9]+\.rar$", path)
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
    name = "7z"

    def can_decompress(self, path):
        return path.lower().endswith('.7z')

    def decompress(self, path, destination):
        args = [self.command,
                'x', '-o' + destination,
                path]
        print(args)
        result = subprocess.run(args)
        result.check_returncode()


DECOMPRESSORS = list(Decompressor.__subclasses__())
AVAILABLE_DECOMPRESSORS = [decompressor
                           for decompressor in DECOMPRESSORS
                           if decompressor.is_available()]


def get_decompressors(configuration):
    return [decompressor(configuration)
            for decompressor in AVAILABLE_DECOMPRESSORS]


def availability():
    return [(decompressor, decompressor in AVAILABLE_DECOMPRESSORS)
            for decompressor in DECOMPRESSORS]
