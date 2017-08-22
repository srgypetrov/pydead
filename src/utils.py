import os


def get_dot_relpath(basedir, path):
    cutted_path, _ = os.path.splitext(path)
    relpath = os.path.relpath(cutted_path, basedir)
    return relpath.replace('/', '.')
