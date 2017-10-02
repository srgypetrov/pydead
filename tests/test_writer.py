import ast
import click
import pytest
import sys

from src import writer


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
    writer.separated('text', *args)
    assert result == expected


@pytest.mark.parametrize("code, str_args, expected", [
    (1, ('filename', 'fatal'), "\nSyntax error in file filename: fatal."),
    (1, ['filename', 'fatal'], "\nSyntax error in file filename: fatal."),
    (2, ['module', 'filename'],
     "\nUnable to detect unused names, 'from module import *' used in file filename."),
    (2, None, 'error'),
    (3, None, "\nNo files found."),
    (3, ['filename'], 'error'),
    (4, ['filename', 15], "\nRelative import goes beyond the scan directory: filename:15."),
    (4, 'filename', "error"),
    (5, None, 'error'),
    (6, ['filename'], 'error')
])
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


@pytest.mark.parametrize("unused, sep_expected, expected", [
    (
        {
            'class': [
                {'path': 'module_1.file_1.class_1', 'node': ast.ClassDef(lineno=10)},
                {'path': 'module_7.file_7.class_7', 'node': ast.ClassDef(lineno=15)},
                {'path': 'module_2.file_2.class_2', 'node': ast.ClassDef(lineno=15)}
            ],
            'function': [
                {'path': 'module_4.file_4.func_4', 'node': ast.FunctionDef(lineno=25)},
                {'path': 'module_3.file_3.func_3', 'node': ast.FunctionDef(lineno=20)}
            ],
            'name': [
                {'path': 'module_9.file_9.name_9', 'node': ast.Name(lineno=30)}
            ]
        },
        ('UNUSED PYTHON CODE', 'red'),
        ['- module_1.file_1:cyan10:redUnused class "class_1"yellow',
         '- module_2.file_2:cyan15:redUnused class "class_2"yellow',
         '- module_7.file_7:cyan15:redUnused class "class_7"yellow',
         '- module_3.file_3:cyan20:redUnused function "func_3"yellow',
         '- module_4.file_4:cyan25:redUnused function "func_4"yellow',
         '- module_9.file_9:cyan30:redUnused name "name_9"yellow']
    ),
    (None, ('NO UNUSED PYTHON CODE', 'green'), [])
])
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
