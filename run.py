# -*- coding: utf-8 -*-

import os
import sys
import re
from dataclasses import dataclass
from typing import List, Dict
from PIL import Image

@dataclass
class Data:
    min_value: 0.0
    max_value: 0.0


def raw_diff(color1: List[float], color2: List[float]) -> float:
    return abs(color1[0] - color2[0]) + abs(color1[1] - color2[1]) + abs(color1[2] - color2[2]) + abs(color1[3] - color2[3])


def load_ruler(root_path: str) -> List[float]:
    ruler_image = Image.open(root_path + '/ruler.png')
    pix = ruler_image.load()

    ruler = []
    for i in range(ruler_image.size[1] - 1, -1, -1):
        ruler.append(pix[4, i])

    ruler_image.close()

    return ruler


def parse_config(config: str) -> Dict:
    with open(config, 'r') as f:
        lines = list(filter(lambda y: re.match('\w+=\d+\.?\d*', y), map(lambda x: x.strip(), f.readlines())))

        config_data = {}
        for line in lines:
            result = line.split('=')
            config_data[result[0]] = result[1]

        return config_data


def calc_image_data(ruler: List[float], image: str, config: str) -> Data:
    config_data = parse_config(config)
    ruler_min = float(config_data['ruler_min'])
    ruler_max = float(config_data['ruler_max'])

    all_value_array = []

    target_im = Image.open(image)
    pix = target_im.load()

    print('Calculating ...')

    for i in range(0, target_im.size[0]):
        for j in range(0, target_im.size[1]):
            # Only calculate non-transparent pixels
            if pix[i, j][0] != 0 or pix[i, j][1] != 0 or pix[i, j][2] != 0 or pix[i, j][3] != 0:
                idx = ruler.index(min(ruler, key = lambda x: raw_diff(x, pix[i, j])))
                value = (idx / len(ruler)) * (ruler_max - ruler_min) + ruler_min
                all_value_array.append(value)

    target_im.close()

    print('mean = {0}'.format(sum(all_value_array) / len(all_value_array)))

    return None


if __name__ == '__main__':
    root_path = os.path.dirname(os.path.realpath(__file__))

    ruler = load_ruler(root_path)

    images = list(filter(lambda x: x.endswith('.png'), os.listdir('{0}/images'.format(root_path))))
    images.sort()

    data_array = []
    for image in images:
        image_path = '{0}/images/{1}'.format(root_path, image)
        config_path = '{0}/images/{1}.txt'.format(root_path, os.path.splitext(image)[0])

        if not os.path.isfile(config_path):
            print('Warning: cannot find {0}'.format(config_path))
            continue

        data_array.append(calc_image_data(ruler, image_path, config_path))

