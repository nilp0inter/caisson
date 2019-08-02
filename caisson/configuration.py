from collections import namedtuple
from enum import Enum


class Overwrite(Enum):
    ALWAYS = 'always'
    NEVER = 'never'
    ASK = 'ask'
    RENAME = 'rename'

    def __str__(self):
        return self.value
