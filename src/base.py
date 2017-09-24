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
    parsed = parse_files(directory, files['.py'])
    unused = get_unused(*parsed)
    report(unused)


def parse_files(basedir, paths):
    defined, used = {}, set()
    with click.progressbar(paths) as bar:
        for path in bar:
            pyfile = PyFile(basedir, path)
            pyfile.parse()
            for name, items in pyfile.defined.items():
                defined.setdefault(name, []).extend(items)
            used.update(pyfile.used)
    return defined, used


def get_unused(defined, used):
    unused = {}
    for name, items in defined.items():
        unused[name] = [item for item in items if not item['path'].endswith(tuple(used))]
    return unused
