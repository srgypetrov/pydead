import pytest

from src.utils import get_dot_relpath


def test_get_dot_relpath(base, path, expected):
    if expected == 'error':
        with pytest.raises(AssertionError):
            dot_path = get_dot_relpath(base, path)
    else:
        dot_path = get_dot_relpath(base, path)
        assert dot_path == expected
