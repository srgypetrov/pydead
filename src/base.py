import click
import os

from .search import search
from .parsers import py_parser
from .writer import report, error


@click.command()
@click.option('--directory', '-d', default=os.getcwd(), help='Directory of your project.')
@click.option('--exclude', '-e', multiple=True, help='Exclude files and directories by the '
              'given pattern. Unix filename pattern matching used.')
def check(directory, exclude):
    files = search(['.py'], exclude or (), directory)
    if not files['.py']:
        error(3)
    parsed = parse_files(directory, files['.py'], py_parser)
    unused, maybe_unused = find_unused(
        parsed['defined_objects'],
        parsed['used_objects']
    )
    report(unused, maybe_unused)


def parse_files(basedir, paths, parser):
    result = {
        'defined_objects': set(),
        'used_objects': set()
    }
    with click.progressbar(paths) as bar:
        for path in bar:
            parsed = parser.parse(basedir, path)
            for key, value in parsed.items():
                result[key].update(value)
    return result


def find_unused(defined, used):
    maybe_unused = find_duplicate_endings(defined, used)
    unused = [item for item in defined if not item.endswith(tuple(used))]
    return unused, maybe_unused


def find_duplicate_endings(defined, used):
    overall = {}
    maybe_unused = []
    for used_item in used:
        for defined_item in defined:
            if defined_item.endswith(used_item):
                overall.setdefault(used_item, set()).add(defined_item)

    for _, value in overall.items():
        if len(value) > 1:
            maybe_unused.append(value)
    return maybe_unused
