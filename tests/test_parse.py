import ast
import pytest

from functools import partial

from src.parse import PyFile


class TestPyFile:

    @pytest.mark.parametrize("node, inner, expected", [
        (ast.parse('from module import func\nn = 1'),
         False,
         [(ast.ImportFrom, False), (ast.Assign, False)]),
        (ast.parse('from module import func\nn = 1'),
         True,
         [(ast.ImportFrom, True), (ast.Assign, True)]),
        (ast.Attribute(attr='attr_one', value=ast.Name(id='name', ctx=ast.Load())),
         False,
         [(ast.Name, False)]),
        (ast.Attribute(attr='attr_one', value=ast.Name(id='name', ctx=ast.Load())),
         True,
         [(ast.Name, True)])
    ])
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

    @pytest.mark.parametrize("initial, expected", [
        ({'level': 0, 'module': 'django.conf.urls'}, 'django.conf.urls'),
        ({'level': 1, 'module': 'views'}, 'apps.core.views'),
        ({'level': 2, 'module': 'models'}, 'apps.models'),
        ({'level': 1, 'module': None}, 'apps.core'),
        ({'level': 3, 'module': 'admin'}, 'admin'),
        ({'level': 4, 'module': 'utils', 'lineno': 1}, 'error'),
    ])
    def test_get_relpath_from_import(self, pyfile, initial, expected):
        node = ast.ImportFrom(**initial)
        if expected == 'error':
            with pytest.raises(SystemExit):
                pyfile.get_relpath_from_import(node)
        else:
            assert pyfile.get_relpath_from_import(node) == expected

    @pytest.mark.parametrize("ast_used, ast_imported, ast_defined, used, defined", [
        (
            [
                ['func_one', 'attr_one', 'class_one'],
                ['func_two', 'attr_three', 'attr_two', 'class_two'],
                ['func_three', 'attr_four', 'class_three']
            ],
            {
                'class_one': 'module_one.file_one.class_one',
                'class_two.attr_two': 'class_two.attr_two',
                'class_three.attr_four.func_three': 'class_three.attr_four.func_three'
            },
            {
                'class': [{'path': 'apps.core.module.class_one'}],
                'function': [{'path': 'apps.core.module.function_one'}],
                'name': [{'path': 'apps.core.module.name_one'}]
            },
            {
                'module_one.file_one.class_one',
                'module_one.file_one.class_one.attr_one',
                'module_one.file_one.class_one.attr_one.func_one',
                'class_two.attr_two',
                'class_two.attr_two.attr_three',
                'class_two.attr_two.attr_three.func_two',
                'class_three.attr_four.func_three'
            },
            None
        ), (
            [
                ['func_four', 'attr_five', 'class_four']
            ],
            {},
            {
                'class': [{'path': 'apps.core.module.class_four'}],
                'function': [{'path': 'apps.core.module.function_one'}],
                'name': [{'path': 'apps.core.module.name_one'}]
            },
            set(),
            {
                'class': [],
                'function': [{'path': 'apps.core.module.function_one'}],
                'name': [{'path': 'apps.core.module.name_one'}]
            }
        ), (
            [
                ['func_four', 'attr_five', 'class_four']
            ],
            {},
            {
                'class': [{'path': 'apps.core.module.class_one'}],
                'function': [{'path': 'apps.core.module.function_one'}],
                'name': [{'path': 'apps.core.module.name_one'}]
            },
            set(),
            None
        ), (
            ['class_five'],
            {'class_five': 'module_two.file_two.class_five'},
            {
                'class': [{'path': 'apps.core.module.class_one'}],
                'function': [{'path': 'apps.core.module.function_one'}],
                'name': [{'path': 'apps.core.module.name_one'}]
            },
            set(['module_two.file_two.class_five']),
            None
        ),
        (
            ['function_six', 'name_one'],
            {},
            {
                'class': [{'path': 'apps.core.module.class_one'}],
                'function': [{'path': 'apps.core.module.function_six'},
                             {'path': 'apps.core.module.function_seven'}],
                'name': [{'path': 'apps.core.module.name_one'},
                         {'path': 'apps.core.module.name_two'},
                         {'path': 'apps.core.module.name_three'}]
            },
            set(),
            {
                'class': [{'path': 'apps.core.module.class_four'}],
                'function': [{'path': 'apps.core.module.function_seven'}],
                'name': [{'path': 'apps.core.module.name_two'},
                         {'path': 'apps.core.module.name_three'}]
            }
        )
    ])
    def test_process_items(self, pyfile, ast_used, ast_imported, ast_defined, used, defined):
        pyfile.ast_used = ast_used
        pyfile.ast_imported = ast_imported
        pyfile.defined = ast_defined
        pyfile.process_items()
        assert pyfile.used == used
        assert pyfile.defined == ast_defined if defined is None else defined
        assert pyfile.ast_imported == ast_imported

    @pytest.mark.parametrize("node, inner, visited, generic", [
        (ast.Ellipsis(), False, [], [(ast.Ellipsis, False)]),
        (ast.Ellipsis(), True, [], [(ast.Ellipsis, True)]),
        (ast.Attribute(), False, [(ast.Attribute, False)], []),
        (ast.Attribute(), True, [(ast.Attribute, True)], []),
        (ast.ClassDef(), False, [(ast.ClassDef, False)], [(ast.ClassDef, True)]),
        (ast.ClassDef(), True, [(ast.ClassDef, True)], [(ast.ClassDef, True)]),
        (ast.FunctionDef(), False, [(ast.FunctionDef, False)], [(ast.FunctionDef, True)]),
        (ast.FunctionDef(), True, [(ast.FunctionDef, True)], [(ast.FunctionDef, True)]),
        (ast.Name(), False, [(ast.Name, False)], [(ast.Name, False)]),
        (ast.Name(), True, [(ast.Name, True)], [(ast.Name, True)])
    ])
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

    @pytest.mark.parametrize("value, ctx, expected", [
        (ast.Attribute(attr='attr', value=ast.Name(id='self')), ast.Store(), []),
        (ast.Attribute(attr='attr', value=ast.Name(id='self')), ast.Load(), []),
        (ast.Attribute(attr='attr', value=ast.Name(id='class')), ast.Load(), [
         ['func', 'attr', 'class']]),
        (ast.Name(id='class'), ast.Load(), [['func', 'class']]),
        (ast.Attribute(attr='attr', value=ast.Load()), ast.Load(), []),
    ])
    def test_visit_attribute(self, pyfile, value, ctx, expected):
        node = ast.Attribute(attr='func', ctx=ctx, value=value)
        pyfile.visit_attribute(node)
        assert pyfile.ast_used == expected

    @pytest.mark.parametrize("col_offset, defined_exist", [(0, True), (1, False), (2, False)])
    def test_visit_classdef(self, pyfile, col_offset, defined_exist):
        node = ast.ClassDef(name='class_one', col_offset=col_offset)
        pyfile.visit_classdef(node)
        defined = {'function': [], 'name': [], 'class': []}
        if defined_exist:
            defined['class'].append({'path': 'apps.core.module.class_one', 'node': node})
        assert pyfile.defined == defined

    @pytest.mark.parametrize("col_offset, defined_exist", [(0, True), (1, False), (2, False)])
    def test_visit_functiondef(self, pyfile, col_offset, defined_exist):
        node = ast.FunctionDef(name='function_one', col_offset=col_offset)
        pyfile.visit_functiondef(node)
        defined = {'function': [], 'name': [], 'class': []}
        if defined_exist:
            defined['function'].append({'path': 'apps.core.module.function_one', 'node': node})
        assert pyfile.defined == defined

    def test_visit_import(self, pyfile):
        node = ast.Import(names=[ast.alias(name='Foo', asname='Bar')])
        pyfile.visit_import(node)
        assert pyfile.ast_imported == {'Bar': 'Foo'}

    @pytest.mark.parametrize("name, asname, module, expected", [
        ('Foo', 'Bar', 'apps.app.module', {'Bar': 'apps.app.module.Foo'}),
        ('Foo', None, None, {'Foo': 'Foo'})
    ])
    def test_visit_importfrom(self, pyfile, name, asname, module, expected):
        node = ast.ImportFrom(names=[ast.alias(name=name, asname=asname)],
                              module=module, level=0)
        pyfile.visit_importfrom(node)
        assert pyfile.ast_imported == expected

    def test_visit_importfrom_invalid(self, pyfile):
        node = ast.ImportFrom(names=[ast.alias(name='*', asname='')],
                              module='apps.app.module', level=0)
        with pytest.raises(SystemExit):
            pyfile.visit_importfrom(node)

    @pytest.mark.parametrize("ctx, inner, defined, used", [
        (ast.Load(), True, [], ['name']),
        (ast.Load(), False, [], ['name']),
        (ast.Store(), True, [], []),
        (ast.Store(), False, [{'path': 'apps.core.module.name'}], [])
    ])
    def test_visit_name(self, pyfile, ctx, inner, defined, used):
        node = ast.Name(ctx=ctx, id='name')
        pyfile.visit_name(node, inner)
        for i in defined:
            i['node'] = node
        assert pyfile.defined == {'name': defined, 'function': [], 'class': []}
        assert pyfile.ast_used == used
