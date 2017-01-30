import sys
import os

from .config import conf
from .writer import colored, separated

ERRORS = {
    1: "Syntax error in file {0}: {1}\n",
    2: "Unable to detect unused names, 'from {0} import *' used in file {1}.\n"
}


def error(code, str_args):
    assert isinstance(str_args, list)
    colored(ERRORS[code].format(*str_args), 'red')
    sys.exit()


def get_dot_relpath(path):
    cutted_path, _ = os.path.splitext(path)
    relpath = os.path.relpath(cutted_path, conf.BASE_DIR)
    return relpath.replace('/', '.')


def report(unused, maybe_unused):
    if unused:
        separated('UNUSED PYTHON CODE')
        for item in sorted(unused, key=lambda x: (x.lower(), x.line)):
            colored('- {}:{}: '.format(item.filepath, item.line), 'cyan')
            colored('Unused {} "{}"\n'.format(item.node, item.name), 'yellow')
    else:
        separated('NO UNUSED PYTHON CODE', 'green')

    if maybe_unused:
        colored('\n\nIt is recommended to check the next groups of items, they may be unused:\n',
                'white')
        for group in maybe_unused:
            separated('-', 'white', '-')
            for item in group:
                colored('- {}:{}: '.format(item.filepath, item.line), 'white')
                colored('{} "{}"\n'.format(item.node, item.name), 'yellow')
        separated('-', 'white', '-')


class ParsedItem(str):

    def __new__(cls, path, name, filepath, node, line, module=None):
        item = str.__new__(cls, path)
        item.name = name
        item.filepath = filepath
        item.node = node
        item.line = line
        item.module = module
        return item
