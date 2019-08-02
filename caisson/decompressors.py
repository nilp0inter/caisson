from abc import ABCMeta, abstractmethod, abstractproperty
import subprocess
import shutil
import re

from caisson.configuration import Overwrite
from caisson import log


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
        options = []
        options.extend(['-d', destination])

        if self.configuration.overwrite is Overwrite.ALWAYS:
            options.extend(['-o'])
        elif self.configuration.overwrite is Overwrite.NEVER:
            options.extend(['-n'])
        elif self.configuration.overwrite is Overwrite.RENAME:
            log.warning(("%r decompressor doesn't support renaming, "
                         "using `--overwrite=never`"),
                        self.name)
            options.extend(['-n'])
        else:
            pass  # Default behavior of `unzip`

        args = [self.command] + options + [path]
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
        options = []

        if self.configuration.overwrite is Overwrite.ALWAYS:
            options.extend(['o+'])
        elif self.configuration.overwrite is Overwrite.NEVER:
            options.extend(['o-'])
        elif self.configuration.overwrite is Overwrite.RENAME:
            options.extend(['or'])
        else:
            pass  # Default behavior of `unrar`

        args = [self.command, 'x'] + options + [path, destination]
        result = subprocess.run(args)
        result.check_returncode()


class SevenZip(Decompressor):
    command = shutil.which("7z")
    name = "7z"

    def can_decompress(self, path):
        return path.lower().endswith('.7z')

    def decompress(self, path, destination):
        options = []
        options.extend(['-o' + destination])

        if self.configuration.overwrite is Overwrite.ALWAYS:
            options.extend(['-aoa'])
        elif self.configuration.overwrite is Overwrite.NEVER:
            options.extend(['-aos'])
        elif self.configuration.overwrite is Overwrite.RENAME:
            options.extend(['-aou'])
        else:
            pass  # Default behavior of `7z`


        args = [self.command, 'x'] + options + [path]
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
