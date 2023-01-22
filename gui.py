# coding: utf-8

import os
import PySimpleGUI as sg
from typing import Final, List
from src.logic.calc import Caculator
from src.utils.coll import find_collections


ACTION_SINGLE_PROCESS: Final = '单组处理'
ACTION_BATCH_PROCESS: Final = '批量处理'

KEY_BROWSE_FOLDER: Final = '-BROWSE-'


calculator = Caculator()


def single_process(ruler: List[List[float]], dir: str):
    calculator.process_collection(False, ruler, dir)
    print('Done')


def batch_process(ruler: List[List[float]], dir: str):
    for coll in find_collections(dir):
        calculator.process_collection(False, ruler, f'{dir}/{coll}')
    print('Done')


if __name__ == '__main__':
    # Find current script absolute path
    root_path = os.path.dirname(os.path.realpath(__file__))

    ruler = calculator.load_ruler(root_path)

    sg.theme('LightGreen')

    font = ('Arial', 24)

    process_folder = f'{root_path}/images'

    layout = [
            [sg.Push(), sg.Text('温度数据分析系统', size=(40, 3), font=font, justification='center'), sg.Push()],
            [sg.Text('单组处理用于。。。。', size=(40, 1), justification='left')],
            [sg.Text('批量处理用于。。。。', size=(40, 1), justification='left')],
            [sg.VPush()],
            [sg.FolderBrowse('选择路径', initial_folder=process_folder, key=KEY_BROWSE_FOLDER), sg.Text(process_folder)],
            [sg.Push(), sg.Button(ACTION_SINGLE_PROCESS, size=(10, 2)), sg.Button(ACTION_BATCH_PROCESS, size=(10, 2)), sg.Push()],
        ]

    window = sg.Window('', layout, size=(640, 320))
    str = ''

    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
    
        if values[KEY_BROWSE_FOLDER] != '':
            process_folder = values[KEY_BROWSE_FOLDER]

        if event == ACTION_SINGLE_PROCESS:
            single_process(ruler, process_folder)
        elif event == ACTION_BATCH_PROCESS:
            batch_process(ruler, process_folder)

    window.close()
