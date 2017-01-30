import ast
import pytest

from src.utils import ParsedItem


class TestPyParser:

    def test_get_ast_node(self, pyparser_clear, filepath):
        node = pyparser_clear.get_ast_node(filepath)
        assert isinstance(node, ast.Module)

    def test_get_ast_node_invalid(self, pyparser_clear, filepath):
        with pytest.raises(SystemExit):
            pyparser_clear.get_ast_node(filepath)

    def test_prepare_results(self, pyparser_filled):
        assert pyparser_filled.prepare_results() == {
            'defined_objects': {'apps.core.module.function2'},
            'used_objects': {'django.conf.urls.url', 'apps.foo.views.FooView'}
        }

    def test_group_used_items(self, pyparser_filled):
        result = pyparser_filled.group_used_items()
        result[1].sort()
        assert result == (
            {'django.conf.urls.url', 'apps.foo.views.FooView'},
            ['apps.core.module.function1', 'apps.core.module.function3']
        )

    def test_remove_class_child_names(self, pyparser_filled):
        assert pyparser_filled.remove_class_child_names(pyparser_filled.used) == {
            'apps.core.module.url', 'apps.core.module.function1'}

    @pytest.mark.parametrize("initial, expected", [
        ({'level': 0, 'module': 'django.conf.urls'}, 'django.conf.urls'),
        ({'level': 1, 'module': 'views'}, 'apps.core.views'),
        ({'level': 2, 'module': 'models'}, 'apps.models'),
        ({'level': 1, 'module': None}, 'apps.core'),
    ])
    def test_get_relpath_from_import(self, pyparser_clear, initial, expected):
        node = ast.ImportFrom(**initial)
        assert pyparser_clear.get_relpath_from_import(node) == expected

    def test_get_item(self, pyparser_clear):
        node = ast.ClassDef(name='Foo', lineno=2)
        item = pyparser_clear.get_item(node, 'class')
        assert isinstance(item, ParsedItem)

    def test_get_node_path(self, pyparser_clear):
        name = pyparser_clear.get_node_path('Foo')
        assert name == 'apps.core.module.Foo'

    @pytest.mark.parametrize("node, expected", [
        (ast.ClassDef(name='FooClass'), 'FooClass'),
        (ast.Name(id='FooFunction'), 'FooFunction'),
        (ast.Attribute(attr='FooAttribute'), 'FooAttribute'),
    ])
    def test_get_name_value(self, pyparser_clear, node, expected):
        name = pyparser_clear.get_name_value(node)
        assert name == expected

    def test_visit_import(self, pyparser_clear):
        node = ast.Import(names=[ast.alias(name='Foo', asname='Bar')])
        pyparser_clear.visit_import(node)
        assert pyparser_clear.imported == {'Bar': 'Bar'}

    def test_visit_importfrom(self, pyparser_clear):
        node = ast.ImportFrom(names=[ast.alias(name='Foo', asname='Bar')],
                              module='apps.app.module', level=0)
        pyparser_clear.visit_importfrom(node)
        assert pyparser_clear.imported == {'Bar': 'apps.app.module.Foo'}

    def test_visit_importfrom_invalid(self, pyparser_clear):
        node = ast.ImportFrom(names=[ast.alias(name='*', asname='')],
                              module='apps.app.module', level=0)
        with pytest.raises(SystemExit):
            pyparser_clear.visit_importfrom(node)

    def test_visit_classdef(self):
        pass
