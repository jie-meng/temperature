# coding: utf-8

import os
import re
import numpy as np
from pathlib import Path
from PIL import Image
from typing import List, Dict
from src.models.data import Data
from src.export.excel import ExcelExporter


class Caculator:
    def __init__(self):
        self.__exporter = ExcelExporter()

    def raw_diff(self, color1: List[float], color2: List[float]) -> float:
        return abs(color1[0] - color2[0]) + abs(color1[1] - color2[1]) + abs(color1[2] - color2[2]) + abs(color1[3] - color2[3])


    def load_ruler(self, root_path: str) -> List[List[float]]:
        ruler_image = Image.open(root_path + '/ruler.png')
        pix = ruler_image.load()

        ruler = []
        for i in range(ruler_image.size[1] - 1, -1, -1):
            ruler.append(pix[4, i])

        ruler_image.close()

        return ruler


    def parse_config(self, config: str) -> Dict[str, str]:
        with open(config, 'r') as f:
            lines = list(filter(lambda y: re.match('\w+=-?\d+\.?\d*', y), map(lambda x: x.strip(), f.readlines())))

            config_data = {}
            for line in lines:
                result = line.split('=')
                config_data[result[0]] = result[1]

            return config_data


    def calc_image_data(self, debug: bool, ruler: List[List[float]], image: str, config: str) -> Data:
        config_data = self.parse_config(config)
        ruler_min = float(config_data['ruler_min'])
        ruler_max = float(config_data['ruler_max'])


        target_im = Image.open(image)
        pix = target_im.load()

        print('Calculating {0} (size {1}x{2}) ...'.format(image, target_im.size[0], target_im.size[1]))

        all_value_array = []
        for i in range(0, target_im.size[0]):
            for j in range(0, target_im.size[1]):
                # Only calculate non-transparent pixels
                if pix[i, j][3] != 0:
                    if debug:
                        print('Include>>> [{0},{1}] R:{2}, G:{3}, B:{4}, A:{5}'.format(i, j, pix[i, j][0], pix[i, j][1], pix[i, j][2], pix[i, j][3]))

                    idx = ruler.index(min(ruler, key = lambda x: self.raw_diff(x, pix[i, j])))
                    value = (idx / len(ruler)) * (ruler_max - ruler_min) + ruler_min
                    all_value_array.append(value)
                else:
                    if debug:
                        print('Exclude>>> [{0},{1}] R:{2}, G:{3}, B:{4}, A:{5}'.format(i, j, pix[i, j][0], pix[i, j][1], pix[i, j][2], pix[i, j][3]))


        
        if len(all_value_array) == target_im.size[0] * target_im.size[1]:
            print('Warning: this image does not cliped correctly!')

        target_im.close()

        data = Data(
            image_name = Path(image).stem,
            point_count = len(all_value_array),
            min_value = np.min(all_value_array),
            max_value = np.max(all_value_array),
            mean = np.mean(all_value_array),
            var = np.var(all_value_array),
            std = np.std(all_value_array),
            data_array = all_value_array,
        )

        data.coefficient_of_variation = data.std / data.mean
        data.is_ok = True

        return data


    def process_collection(self, debug: bool, ruler: List[List[float]], coll_path: str):
        coll = os.path.basename(coll_path)
        print(f'\nProcessing collection {coll_path} ...')

        # Find images
        images = list(filter(lambda x: x.endswith('.png'), os.listdir(coll_path)))
        images.sort()

        # Process each image
        data_array: List[Data] = []
        for image in images:
            image_path = '{0}/{1}'.format(coll_path, image)
            config_path = '{0}/{1}.txt'.format(coll_path, os.path.splitext(image)[0])

            if not os.path.isfile(config_path):
                print(f'Warning: cannot find {config_path}')
                continue

            try:
                data_array.append(self.calc_image_data(debug, ruler, image_path, config_path))
            except BaseException:
                data_array.append(Data(image_name = Path(image).stem, is_ok = False, data_array = []))
                continue

        # Write xlsx
        xlsx_file = f'{coll_path}/{coll}.xlsx'
        print(f'Generate {xlsx_file} ...')

        if len(data_array) > 0:
            self.__exporter.write_output(data_array, xlsx_file)
