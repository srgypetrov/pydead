import click
import os
import re

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
    defined, used, init_imports = {}, set(), set()
    with click.progressbar(paths) as bar:
        for path in bar:
            pyfile = PyFile(basedir, path)
            pyfile.parse()
            for name, items in pyfile.defined.items():
                defined.setdefault(name, []).extend(items)
            used.update(pyfile.used)
            if path.endswith('__init__.py'):
                init_imports.update(pyfile.ast_imported.values())
    fix_init_imports(init_imports, used)
    return defined, used


def fix_init_imports(init_imports, used):
    for init_import in init_imports:
        module_import = re.sub(r'\..+\.', '.', init_import)
        if module_import in used:
            used.remove(module_import)
            used.add(init_import)


def get_unused(defined, used):
    unused = {}
    for name, items in defined.items():
        unused[name] = [item for item in items if not item['path'].endswith(tuple(used))]
    return unused
