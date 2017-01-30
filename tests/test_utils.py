import os

from src.utils import get_dot_relpath


def test_get_dot_relpath_directory():
    relpath = get_dot_relpath(os.path.join(os.getcwd(), 'tests/test_utils/'))
    assert relpath == 'tests.test_utils'


def test_get_dot_relpath_file():
    relpath = get_dot_relpath(os.path.join(os.getcwd(), 'tests/test_utils/test.py'))
    assert relpath == 'tests.test_utils.test'
