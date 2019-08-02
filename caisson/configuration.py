from collections import namedtuple
from enum import Enum


class Overwrite(Enum):
    ALWAYS = 'always'
    NEVER = 'never'
    ASK = 'ask'
    RENAME = 'rename'
