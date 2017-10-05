import ast
import pytest

from functools import partial

from src.parse import PyFile


class TestPyFile:

    def test_create_pyfile(self):
        pyfile = PyFile('/home/project/', '/home/project/module1/file1.py')
        assert pyfile.path == '/home/project/module1/file1.py'
        assert pyfile.dot_path == 'module1.file1'
        assert pyfile.used == set()
        assert pyfile.ast_used == []
        assert pyfile.ast_imported == {}
        assert pyfile.defined == {'class': [], 'function': [], 'name': []}

    def test_generic_visit(self, monkeypatch, pyfile, node, inner, expected):

        pyfile.ast_visited = []

        def mock_visit(f, node, inner):
            f.ast_visited.append((type(node), inner))

        monkeypatch.setattr(pyfile, 'visit', partial(mock_visit, pyfile))
        pyfile.generic_visit(node, inner)
        assert pyfile.ast_visited == expected

    def test_get_node(self, test_files):
        pyfile = PyFile('/fs/', '/fs/file1.py')
        node = pyfile.get_node()
        assert isinstance(node, ast.Module)

    def test_get_node_invalid(self, test_files):
        pyfile = PyFile('/fs/', '/fs/foo/file2.py')
        with pytest.raises(SystemExit):
            pyfile.get_node()

    def test_get_relpath_from_import(self, pyfile, initial, expected):
        node = ast.ImportFrom(**initial)
        if expected == 'error':
            with pytest.raises(SystemExit):
                pyfile.get_relpath_from_import(node)
        else:
            assert pyfile.get_relpath_from_import(node) == expected

    def test_process_items(self, pyfile, ast_used, ast_imported, ast_defined, used, defined):
        pyfile.ast_used = ast_used
        pyfile.ast_imported = ast_imported
        pyfile.defined = ast_defined
        pyfile.process_items()
        assert pyfile.used == used
        assert pyfile.defined == ast_defined if defined is None else defined
        assert pyfile.ast_imported == ast_imported

    def test_visit(self, monkeypatch, pyfile, node, inner, visited, generic):

        pyfile.ast_visited = []
        pyfile.ast_generic = []

        def mock_visitor(f, node, inner):
            f.ast_visited.append((type(node), inner))

        def mock_generic_visit(f, node, inner):
            f.ast_generic.append((type(node), inner))

        monkeypatch.setattr(pyfile, 'visit_attribute', partial(mock_visitor, pyfile))
        monkeypatch.setattr(pyfile, 'visit_classdef', partial(mock_visitor, pyfile))
        monkeypatch.setattr(pyfile, 'visit_functiondef', partial(mock_visitor, pyfile))
        monkeypatch.setattr(pyfile, 'visit_name', partial(mock_visitor, pyfile))
        monkeypatch.setattr(pyfile, 'generic_visit', partial(mock_generic_visit, pyfile))
        pyfile.visit(node, inner)
        assert pyfile.ast_visited == visited
        assert pyfile.ast_generic == generic

    def test_visit_attribute(self, pyfile, node, expected):
        pyfile.visit_attribute(node)
        assert pyfile.ast_used == expected

    def test_visit_classdef(self, pyfile, node, defined_exist):
        pyfile.visit_classdef(node)
        defined = {'function': [], 'name': [], 'class': []}
        if defined_exist:
            defined['class'].append({'path': 'apps.core.module.class_one', 'node': node})
        assert pyfile.defined == defined

    def test_visit_functiondef(self, pyfile, node, defined_exist):
        pyfile.visit_functiondef(node)
        defined = {'function': [], 'name': [], 'class': []}
        if defined_exist:
            defined['function'].append({'path': 'apps.core.module.function_one', 'node': node})
        assert pyfile.defined == defined

    def test_visit_import(self, pyfile):
        node = ast.Import(names=[ast.alias(name='Foo', asname='Bar')])
        pyfile.visit_import(node)
        assert pyfile.ast_imported == {'Bar': 'Foo'}

    def test_visit_importfrom(self, pyfile, node, expected):
        pyfile.visit_importfrom(node)
        assert pyfile.ast_imported == expected

    def test_visit_importfrom_invalid(self, pyfile):
        node = ast.ImportFrom(names=[ast.alias(name='*', asname='')],
                              module='apps.app.module', level=0)
        with pytest.raises(SystemExit):
            pyfile.visit_importfrom(node)

    def test_visit_name(self, pyfile, node, inner, defined, used):
        pyfile.visit_name(node, inner)
        for i in defined:
            i['node'] = node
        assert pyfile.defined == {'name': defined, 'function': [], 'class': []}
        assert pyfile.ast_used == used
