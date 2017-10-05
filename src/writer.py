import click
import sys

from .exceptions import ArgumentError


ERRORS = {
    1: ("\nSyntax error in file {0}: {1}.", 2),
    2: ("\nUnable to detect unused names, 'from {0} import *' used in file {1}.", 2),
    3: ("\nNo files found.", 0),
    4: ("\nRelative import goes beyond the scan directory: {0}:{1}.", 2)
}


def error(code, str_args=None):
    str_args = str_args or []
    err, args_count = ERRORS[code]
    if not isinstance(str_args, (list, tuple)):
        raise ArgumentError('String arguments must be tuple or list', code, str_args)
    if len(str_args) != args_count:
        raise ArgumentError('Mismatch between error code and string arguments', code, str_args)
    err = err.format(*str_args)
    click.secho(err, fg='red', err=True)
    sys.exit(1)


def separated(text, fg, sepchar='='):
    width = click.get_terminal_size()[0]
    text = text.center(width, sepchar)
    click.secho(text, fg=fg)


def report(unused):
    if any(unused.values()):
        separated('UNUSED PYTHON CODE', fg='red')
        for name, items in sorted(unused.items()):
            for item in sorted(items, key=lambda x: (x['path'].lower(), x['node'].lineno)):
                filepath, item_name = item['path'].rsplit('.', 1)
                click.echo('{0}{1}{2}'.format(
                    click.style('- {0}:'.format(filepath), fg='cyan'),
                    click.style('{0}:'.format(item['node'].lineno), fg='red'),
                    click.style('Unused {0} "{1}"'.format(name, item_name), fg='yellow'),
                ))
    else:
        separated('NO UNUSED PYTHON CODE', fg='green')
