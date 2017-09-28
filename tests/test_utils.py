import pytest

from src.utils import get_dot_relpath


@pytest.mark.parametrize("base, path, expected", [
    ('/apps/', '/apps/', '.'),
    ('/apps', '/apps/', '.'),
    ('/apps/', '/app/test.py', 'error'),
    ('/apps/', 'test.py', 'error'),
    ('/apps/', '/apps/test.py', 'test'),
    ('/apps/', '/apps/core/test.py', 'core.test'),
    ('/apps/', '/apps/core/module/', 'core.module'),
    ('/apps/core/module/', '/apps/', 'error')
])
def test_get_dot_relpath(base, path, expected):
    if expected == 'error':
        with pytest.raises(AssertionError):
            dot_path = get_dot_relpath(base, path)
    else:
        dot_path = get_dot_relpath(base, path)
        assert dot_path == expected
