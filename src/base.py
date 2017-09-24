import click
import os

from .parse import PyFile
from .search import search
from .writer import report, error


@click.command()
@click.option('--directory', '-d', default=os.getcwd(), help='Directory of your project.')
@click.option('--exclude', '-e', multiple=True, help='Exclude files and directories by the '
              'given pattern. Unix filename pattern matching used.')
def check(directory, exclude):
    files = search(['.py'], exclude or (), directory)
    if not files['.py']:
        error(3)
    defined, used = parse_files(directory, files['.py'])
    unused = [node for node in defined if not node.path.endswith(tuple(used))]
    report(unused)


def parse_files(basedir, paths):
    defined, used = set(), set()
    with click.progressbar(paths) as bar:
        for path in bar:
            pyfile = PyFile(basedir, path)
            pyfile.parse()
            defined.update(pyfile.defined)
            used.update(pyfile.used)
    return defined, used
