# coding: utf-8

import os
from typing import List


def find_collections(path: str) -> List[str]:
    dir = os.path.dirname(path)
    base = os.path.basename(path)
    collections = list(filter(lambda x: os.path.isdir(f'{dir}/{base}/{x}'), os.listdir(path)))
    collections.sort()

    return collections
