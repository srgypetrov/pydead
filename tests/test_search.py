import os

from src.search import search, fix_extensions


def test_fix_extensions():
    extensions = ['.py', 'txt']
    fix_extensions(extensions)
    assert extensions == ['.py', '.txt']


def test_search(test_files):
    path = '/fs/'
    files = search(['.py', 'txt'], ['*bar*'], path)
    assert files == {
        '.py': [
            os.path.join(path, 'foo/file2.py'),
            os.path.join(path, 'file1.py')
        ],
        '.txt': [
            os.path.join(path, 'file1.txt')
        ]
    }
