# -*- coding: utf-8 -*-

import sys
import os
from PIL import Image


def raw_diff(color1, color2):
    return abs(color1[0] - color2[0]) + abs(color1[1] - color2[1]) + abs(color1[2] - color2[2]) + abs(color1[3] - color2[3])

def load_color_bar(root_path: str):
    bar_im = Image.open(root_path + '/bar.png')
    pix = bar_im.load()

    color_bar = []
    for i in range(bar_im.size[1] - 1, -1, -1):
        color_bar.append(pix[4, i])

    return color_bar

if __name__ == '__main__':
    root_path = os.path.dirname(os.path.realpath(__file__))

    color_bar = load_color_bar(root_path)

    image_name = input('Please input image name:\n')
    image_file = '{0}/images/{1}'.format(root_path, image_name)
    if not os.path.isfile(image_file):
        print('{0} does not exist!'.format(image_file))
        sys.exit(-1)

    min_value = float(input('Please input min value:\n'))
    max_value = float(input('Please input max value:\n'))

    all_value_array = []

    target_im = Image.open(image_file)
    pix = target_im.load()

    print('Calculating ...')

    for i in range(0, target_im.size[0]):
        for j in range(0, target_im.size[1]):
            # Only calculate non-transparent pixels
            if pix[i, j][0] != 0 or pix[i, j][1] != 0 or pix[i, j][2] != 0 or pix[i, j][3] != 0:
                idx = color_bar.index(min(color_bar, key = lambda x: raw_diff(x, pix[i, j])))
                value = (idx / len(color_bar)) * (max_value - min_value) + min_value
                all_value_array.append(value)

    print('mean = {0}'.format(sum(all_value_array) / len(all_value_array)))

