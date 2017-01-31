from .search import search
from .parsers import py_parser
from .config import conf
from .utils import report


def check():
    files = search(conf.EXTENSIONS, conf.EXCLUDE, conf.BASE_DIR)
    parsed = parse_files(files['.py'], py_parser)
    unused, maybe_unused = find_unused(
        parsed['defined_objects'],
        parsed['used_objects']
    )
    report(unused, maybe_unused)


def parse_files(paths, parser):
    result = {}
    for path in paths:
        parsed = parser.parse(path)
        for key, value in parsed.items():
            result.setdefault(key, set()).update(value)
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
