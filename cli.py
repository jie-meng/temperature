# coding: utf-8

import os
import click
from src.utils.coll import find_collections
from src.logic.calc import Caculator


@click.command()
@click.option('--debug', prompt = 'Debug mode?', default = 'n', required = True, type=click.Choice(['y', 'n']), help = 'Enable debug or not')
def cli(debug: str):
    """temperature-cli - Command line tool to analyze temperature image data"""
    # Find current script absolute path
    root_path = os.path.dirname(os.path.realpath(__file__))

    calculator = Caculator()
    ruler = calculator.load_ruler(root_path)

    for coll in find_collections(f'{root_path}/images'):
        calculator.process_collection(debug == 'y', ruler, f'{root_path}/images/{coll}')

    print('\nDone!')

if __name__ == '__main__':
    cli() 
    