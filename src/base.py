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
    unused, maybe_unused = find_unused(*parsed)
    report(unused, maybe_unused)


def parse_files(basedir, paths):
    defined, used = set(), set()
    with click.progressbar(paths) as bar:
        for path in bar:
            pyfile = PyFile(basedir, path)
            pyfile.parse()
            defined.update(pyfile.defined)
            used.update(pyfile.used)
    return defined, used


def find_unused(defined, used):
    maybe_unused = find_duplicate_endings(defined, used)
    unused = [node for node in defined if not node.path.endswith(tuple(used))]
    return unused, maybe_unused


def find_duplicate_endings(defined, used):
    overall = {}
    maybe_unused = []
    for used_path in used:
        for node in defined:
            if node.path.endswith(used_path):
                overall.setdefault(used_path, set()).add(node)

    for _, value in overall.items():
        if len(value) > 1:
            maybe_unused.append(value)
    return maybe_unused
