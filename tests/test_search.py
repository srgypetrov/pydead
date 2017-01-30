import os

from src.search import search, fix_extensions


def test_fix_extensions():
    extensions = ['.py', 'txt']
    fix_extensions(extensions)
    assert extensions == ['.py', '.txt']


def test_search(filepath):
    files = search(['.py', 'txt'], ['*bar*'], filepath)
    assert files == {
        '.py': [
            os.path.join(filepath, 'file1.py'),
            os.path.join(filepath, 'foo/file2.py')
        ],
        '.txt': [
            os.path.join(filepath, 'file1.txt')
        ]
    }
