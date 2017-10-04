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
    init_imports, defined, used = parse_files(directory, files['.py'])
    fix_init_imports(used, init_imports)
    unused = get_unused(defined, used)
    report(unused)


def parse_files(basedir, paths):
    init_imports, defined, used = {}, {}, set()
    with click.progressbar(paths) as bar:
        for path in bar:
            pyfile = PyFile(basedir, path)
            pyfile.parse()
            used.update(pyfile.used)
            for name, items in pyfile.defined.items():
                defined.setdefault(name, []).extend(items)
            if path.endswith('__init__.py'):
                module = pyfile.dot_path.rstrip('.__init__')
                for item_name, item in pyfile.ast_imported.items():
                    key = '.'.join((module, item_name))
                    if key != item:
                        init_imports[key] = item
    return init_imports, defined, used


def fix_init_imports(used, init_imports):

    def get_correct_value(value):
        if value in init_imports:
            value = init_imports[value]
            return get_correct_value(value)
        return value

    for key, value in init_imports.items():
        if key in used:
            value = get_correct_value(value)
            used.remove(key)
            used.add(value)


def get_unused(defined, used):
    unused = {}
    for name, items in defined.items():
        unused[name] = [item for item in items if not item['path'] in used]
    return unused
