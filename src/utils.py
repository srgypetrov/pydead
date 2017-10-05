import os

from .exceptions import PathMismatchError


def get_dot_relpath(basedir, path):
    cutted_path, _ = os.path.splitext(path)
    if os.path.commonprefix([basedir, cutted_path]) != basedir:
        raise PathMismatchError(basedir, path)
    relpath = os.path.relpath(cutted_path, basedir)
    return relpath.replace('/', '.')
