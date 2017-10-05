import pytest

from collections import namedtuple
from click.testing import CliRunner
from src.parse import PyFile

from .data import data


@pytest.fixture
def test_files(fs):
    fs.CreateFile('/fs/bar/file2.txt')
    fs.CreateFile('/fs/foo/file2.py', contents='a = 1\nprint a\n')
    fs.CreateFile('/fs/file1.txt')
    fs.CreateFile('/fs/file1.py', contents="import module1\n\n\nmodule1('string')\n")


@pytest.fixture
def pyfile():
    pyfile = PyFile('', 'apps/core/module/')
    return pyfile


@pytest.fixture
def mock_file():
    return namedtuple('MockFile', ['parse', 'used', 'defined', 'dot_path', 'ast_imported'])


@pytest.fixture
def runner():
    return CliRunner()


def pytest_generate_tests(metafunc):
    func_name = metafunc.function.__name__
    test_data = data.get(func_name, None)
    if test_data:
        metafunc.parametrize(test_data['names'], test_data['params'])
