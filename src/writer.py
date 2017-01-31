import termios
import fcntl
import struct
import os
import sys

colors = dict(red=31, green=32, yellow=33, blue=34, cyan=36, white=37)


def get_terminal_width():
    try:
        call = fcntl.ioctl(1, termios.TIOCGWINSZ, "\000" * 8)
        width = struct.unpack("hhhh", call)[1]
    except:
        width = int(os.environ.get('COLUMNS', 80))
    return width if width >= 40 else 80


def colored(text, color='white'):
    text = '\x1b[{0}m{1}\x1b[0m'.format(colors.get(color, 37), text)
    sys.stdout.write(text)


def separated(text, color='red', sepchar='='):
    fullwidth = get_terminal_width()
    if sys.platform == "win32":
        fullwidth -= 1
    n = (fullwidth - len(text) - 2) // (2 * len(sepchar))
    fill = sepchar * n
    line = "{} {} {}".format(fill, text, fill)
    if len(line) + len(sepchar.rstrip()) <= fullwidth:
        line += sepchar.rstrip()
    colored(line, color)


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
