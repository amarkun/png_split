import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class Splitter:
    """
    Class used to crop an image file into a certain number of evenly dvided images
    """
    source: str
    target: str
    splits: int
    buffer: int
    isDir: bool
    dirContents: List[str] = field(default_factory=list)

    def __init__(self, source, target, splits, buffer):
        # TODO: check these explicitly and raise an exception
        assert os.path.isdir(os.path.abspath(source)) or os.path.isfile(os.path.abspath(source))

        if os.path.isdir(os.path.abspath(target)) is False:
            if os.path.isdir(os.path.abspath(os.path.split(target)[0])) is False:
                raise

        source = os.path.abspath(source)
        target = os.path.abspath(target)

        self.source = os.path.abspath(source)
        self.target = os.path.abspath(target)
        self.splits = splits
        self.buffer = buffer
        self.isDir = os.path.isdir(source)
        self.dirContents = os.listdir(source)
