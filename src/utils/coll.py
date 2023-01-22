# coding: utf-8

import os
from typing import List


def find_collections(root_path: str) -> List[str]:
    collections = list(filter(lambda x: os.path.isdir('{0}/images/{1}'.format(root_path, x)), os.listdir('{0}/images'.format(root_path))))
    collections.sort()

    return collections