# coding: utf-8

from dataclasses import dataclass
from typing import List


@dataclass
class Data:
    image_name: str = ''
    is_ok: bool = False
    point_count: int = 0
    min_value: float = 0.0
    max_value: float = 0.0
    mean: float = 0.0
    var: float = 0.0
    std: float = 0.0
    coefficient_of_variation: float = 0.0
    data_array: List[float] = None
