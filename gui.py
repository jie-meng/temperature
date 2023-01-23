# coding: utf-8

import os
import PySimpleGUI as sg
from concurrent.futures import ThreadPoolExecutor
from typing import Final, List
from src.logic.calc import Caculator
from src.utils.coll import find_collections
from src.utils.logger import Logger


ACTION_SINGLE_PROCESS: Final = '单组处理'
ACTION_BATCH_PROCESS: Final = '批量处理'

KEY_BROWSE_FOLDER: Final = '-BROWSE-'
KEY_OUTPUT: Final = '-OUTPUT-'


class GUILogger(Logger):
    def __init__(self):
        self.__output = ''
    
    def __concat_log(self, message: str):
        self.__output = f'{self.__output}\n{message}'
    
    def get_output(self):
        return self.__output 
    
    def clear(self):
        self.__output = ''

    def verbose(self, message: str):
        self.__concat_log(f'[VERBOSE] {message}')

    def debug(self, message: str):
        self.__concat_log(f'[DEBUG] {message}')

    def info(self, message: str):
        self.__concat_log(f'[INFO] {message}')

    def warn(self, message: str):
        self.__concat_log(f'[WARN] {message}')

    def error(self, message: str):
        self.__concat_log(f'[ERROR] {message}')

    def wtf(self, message: str):
        self.__concat_log(f'[WTF] {message}')


logger = GUILogger()
calculator = Caculator(logger)


def single_process(ruler: List[List[float]], dir: str):
    logger.clear()
    calculator.process_collection(False, ruler, dir)
    logger.info('Done')


def batch_process(ruler: List[List[float]], dir: str):
    logger.clear()
    for coll in find_collections(dir):
        calculator.process_collection(False, ruler, f'{dir}/{coll}')
    logger.info('Done')


if __name__ == '__main__':
    task_executor = ThreadPoolExecutor(max_workers=5)

    # Find current script absolute path
    root_path = os.path.dirname(os.path.realpath(__file__))

    ruler = calculator.load_ruler(root_path)

    sg.theme('LightGreen')

    font = ('Arial', 24)

    process_folder = f'{root_path}/images'

    layout = [
            [sg.Push(), sg.Text('温度数据分析系统', size=(40, 3), font=font, justification='center'), sg.Push()],
            [sg.Text('单组处理用于处理一组温度图片，选择目录中包含 PNG 图片和图片对应的上下限配置文件。', size=(100, 1), justification='left')],
            [sg.Text('批量处理用于处理多组温度图片，选择目录中包含多个子目录，每个子目录和单组处理的文件目录结构相同。', size=(100, 1), justification='left')],
            [sg.VPush()],
            [sg.Multiline(size=(100, 20), key=KEY_OUTPUT, disabled=True, autoscroll=True)],
            [sg.FolderBrowse('选择路径', initial_folder=process_folder, key=KEY_BROWSE_FOLDER), sg.Text(process_folder)],
            [sg.Push(), sg.Button(ACTION_SINGLE_PROCESS, size=(10, 2)), sg.Button(ACTION_BATCH_PROCESS, size=(10, 2)), sg.Push()],
        ]

    window = sg.Window('', layout, size=(640, 480))

    while True:
        event, values = window.read(timeout=100)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

        if values[KEY_BROWSE_FOLDER] != '':
            process_folder = values[KEY_BROWSE_FOLDER]

        if event == ACTION_SINGLE_PROCESS:
            task_executor.submit(single_process, ruler, process_folder)
        elif event == ACTION_BATCH_PROCESS:
            task_executor.submit(batch_process, ruler, process_folder)
        
        window[KEY_OUTPUT].update(logger.get_output())

    window.close()
