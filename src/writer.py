import click
import sys


ERRORS = {
    1: "Syntax error in file {0}: {1}.",
    2: "Unable to detect unused names, 'from {0} import *' used in file {1}.",
    3: "No files found.",
    4: "Relative import goes beyond the scan directory: {0}:{1}."
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


def report(unused, maybe_unused):
    if unused:
        separated('UNUSED PYTHON CODE', fg='red')
        for node in sorted(unused, key=lambda x: (x.path.lower(), x.line)):
            click.echo('{}{}{}'.format(
                click.style('- {}:'.format(node.filepath), fg='cyan'),
                click.style('{}:'.format(node.line), fg='red'),
                click.style('Unused {} "{}"'.format(node.node_type, node.name), fg='yellow'),
            ))
    else:
        separated('NO UNUSED PYTHON CODE', fg='green')

    if maybe_unused:
        click.secho('It is recommended to check the next groups of items, they may be unused:',
                    fg='white')
        for group in maybe_unused:
            click.echo('-' * click.get_terminal_size()[0])
            for node in group:
                click.secho('- {}:{}: '.format(node.filepath, node.line), fg='white')
                click.secho('{} "{}"\n'.format(node.node_type, node.name), fg='yellow')
        click.echo('-' * click.get_terminal_size()[0])
