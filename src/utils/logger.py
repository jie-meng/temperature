# coding: utf-8

from abc import ABC, abstractmethod
from typing import Final


class PrintColors:
    HEADER: Final = '\033[95m'
    OKBLUE: Final = '\033[94m'
    OKCYAN: Final = '\033[96m'
    OKGREEN: Final = '\033[92m'
    WARNING: Final = '\033[93m'
    FAIL: Final = '\033[91m'
    ENDC: Final = '\033[0m'
    BOLD: Final = '\033[1m'
    UNDERLINE: Final = '\033[4m'


class Logger(ABC):
    @abstractmethod
    def verbose(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def debug(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def info(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def warn(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def error(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def wtf(self, message: str):
        raise NotImplementedError


class DefaultLogger(Logger):
    def verbose(self, message: str):
        print(f'[VERBOSE] {message}')

    def debug(self, message: str):
        print(f'[DEBUG] {message}')

    def info(self, message: str):
        print(f'[INFO] {message}')

    def warn(self, message: str):
        print(f'{PrintColors.WARNING}[WARN] {message}{PrintColors.ENDC}')

    def error(self, message: str):
        print(f'{PrintColors.FAIL}[ERROR] {message}{PrintColors.ENDC}')

    def wtf(self, message: str):
        print(f'{PrintColors.FAIL}[WTF] {message}{PrintColors.ENDC}')
