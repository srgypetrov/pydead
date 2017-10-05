import os

from src.search import search, fix_extensions


def test_fix_extensions():
    extensions = ['.py', 'txt']
    fix_extensions(extensions)
    assert extensions == ['.py', '.txt']


def test_search(test_files):
    path = '/fs/'
    files = search(['.py', 'txt'], ['*bar*'], path)
    assert sorted(files.keys()) == ['.py', '.txt']
    assert sorted(files['.py']) == [os.path.join(path, 'file1.py'),
                                    os.path.join(path, 'foo/file2.py')]
    assert files['.txt'] == [os.path.join(path, 'file1.txt')]
