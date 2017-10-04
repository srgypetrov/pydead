import click
import pytest
import sys

from src import writer


def test_separated(monkeypatch, arguments, expected):

    result = None

    def mock_size():
        return (10, 15)

    def mock_secho(text, fg):
        nonlocal result
        result = (text, fg)

    monkeypatch.setattr(click, 'get_terminal_size', mock_size)
    monkeypatch.setattr(click, 'secho', mock_secho)
    writer.separated('text', *arguments)
    assert result == expected


def test_error(monkeypatch, code, str_args, expected):

    result = None

    def mock_secho(err_text, fg, err):
        nonlocal result
        result = err_text

    monkeypatch.setattr(click, 'secho', mock_secho)
    monkeypatch.setattr(sys, 'exit', lambda: None)

    if expected == 'error':
        with pytest.raises(AssertionError):
            writer.error(code, str_args)
    else:
        writer.error(code, str_args)
        assert result == expected


def test_report(monkeypatch, unused, sep_expected, expected):

    separated_text = None
    result = []

    def mock_echo(text):
        result.append(text)

    def mock_style(text, fg):
        return text + fg

    def mock_separated(text, fg):
        nonlocal separated_text
        separated_text = (text, fg)

    monkeypatch.setattr(click, 'echo', mock_echo)
    monkeypatch.setattr(click, 'style', mock_style)
    monkeypatch.setattr(writer, 'separated', mock_separated)
    writer.report(unused)
    assert separated_text == sep_expected
    assert result == expected
