import click
import sys


ERRORS = {
    1: "\nSyntax error in file {0}: {1}.",
    2: "\nUnable to detect unused names, 'from {0} import *' used in file {1}.",
    3: "\nNo files found.",
    4: "\nRelative import goes beyond the scan directory: {0}:{1}."
}


def error(code, str_args=None):
    err = ERRORS[code]
    if isinstance(str_args, list):
        err = err.format(*str_args)
    click.secho(err, fg='red', err=True)
    sys.exit()


def separated(text, fg, sepchar='='):
    width = click.get_terminal_size()[0]
    text = text.center(width, sepchar)
    click.secho(text, fg=fg)


def report(unused):
    if unused:
        separated('UNUSED PYTHON CODE', fg='red')
        for name, items in unused.items():
            for item in sorted(items, key=lambda x: (x['path'].lower(), x['node'].lineno)):
                filepath, item_name = item['path'].rsplit('.', 1)
                click.echo('{}{}{}'.format(
                    click.style('- {}:'.format(filepath), fg='cyan'),
                    click.style('{}:'.format(item['node'].lineno), fg='red'),
                    click.style('Unused {} "{}"'.format(name, item_name), fg='yellow'),
                ))
    else:
        separated('NO UNUSED PYTHON CODE', fg='green')
