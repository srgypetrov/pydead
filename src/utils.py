import os


def get_dot_relpath(basedir, path):
    cutted_path, _ = os.path.splitext(path)
    assert os.path.commonprefix([basedir, cutted_path]) == basedir
    relpath = os.path.relpath(cutted_path, basedir)
    return relpath.replace('/', '.')
