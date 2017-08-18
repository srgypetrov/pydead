import os


def get_dot_relpath(basedir, path):
    cutted_path, _ = os.path.splitext(path)
    relpath = os.path.relpath(cutted_path, basedir)
    return relpath.replace('/', '.')


class ParsedItem(str):

    def __new__(cls, path, name, filepath, node, line, module=None):
        item = str.__new__(cls, path)
        item.name = name
        item.filepath = filepath
        item.node = node
        item.line = line
        item.module = module
        return item
