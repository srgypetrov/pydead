import pytest

from src.utils import get_dot_relpath
from src.exceptions import PathMismatchError


def test_get_dot_relpath(base, path, expected):
    if expected == 'error':
        with pytest.raises(PathMismatchError) as excinfo:
            get_dot_relpath(base, path)
        assert excinfo.value.args == (base, path)
    else:
        dot_path = get_dot_relpath(base, path)
        assert dot_path == expected
