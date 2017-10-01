import click
import pytest

from src.writer import separated


@pytest.mark.parametrize("args, expected", [
    (('blue', '-'), ('---text---', 'blue')),
    (('red', '*'), ('***text***', 'red')),
    (('green',), ('===text===', 'green'))
])
def test_separated(monkeypatch, args, expected):

    result = None

    def mock_size():
        return (10, 15)

    def mock_secho(text, fg):
        nonlocal result
        result = (text, fg)

    monkeypatch.setattr(click, 'get_terminal_size', mock_size)
    monkeypatch.setattr(click, 'secho', mock_secho)
    separated('text', *args)
    assert result == expected
