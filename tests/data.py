import ast

data = {
    'test_fix_init_imports': {
        'names': ('init_imports', 'used', 'expected'),
        'params': [(
            {
                'module_1.fa.func_1': 'module_1.fa.fb.func_1',
                'module_1.fa.fb.func_1': 'module_1.fa.fb.fc.func_1',
                'module_2.class_2': 'module_2.file_2.class_2',
                'module_1.fa.fb.fc.func_1': 'module_1.fa.fb.fc.fd.func_1',
                'module_3.name_3': 'module_3.file_3.name_3',
                'module_3.file_3.name_3': 'module_3.file_3.file_3a.file_3b.name_3',
                'module_4.class_4': 'module_4.file_4.class_4',
                'module_4.file_4.class_4': 'module_4.file_4.file_4a.class_4',
                'module_5.name_5': 'module_5.file_5.name_5'
            },
            {
                'module_1.fa.func_1',
                'module_4.class_4',
                'module_5.name_5',
                'module_7.file_7.func_7',
                'module_9.func_9'
            },
            {
                'module_1.fa.fb.fc.fd.func_1',
                'module_4.file_4.file_4a.class_4', 'module_5.file_5.name_5',
                'module_7.file_7.func_7',
                'module_9.func_9'
            }
        )]
    },
    'test_get_unused': {
        'names': ('defined', 'used', 'expected'),
        'params': [(
            {
                'class': [{'path': 'module_1.file_1.class_1'},
                          {'path': 'module_7.file_7.class_7'},
                          {'path': 'module_2.file_2.class_2'}],
                'function': [{'path': 'module_4.file_4.func_4'},
                             {'path': 'module_3.file_3.func_3'}],
                'name': [{'path': 'module_9.file_9.name_9'}]
            },
            {
                'module_3.file_3.func_3',
                'module_2.file_2.class_2',
                'module_3.file_2.class_2',
                'module_3.file_1.class_7',
                'core.module_1.file_1.class_1'
            },
            {
                'class': [{'path': 'module_1.file_1.class_1'},
                          {'path': 'module_7.file_7.class_7'}],
                'function': [{'path': 'module_4.file_4.func_4'}],
                'name': [{'path': 'module_9.file_9.name_9'}]
            }
        )]
    },
    'test_parse_files': {
        'names': ('data', 'exp_defined', 'exp_used', 'exp_imports'),
        'params': [(
            {
                '/module2/file2.py': {
                    'dot_path': 'module2.file2',
                    'used': {
                        'module1.func1',
                        'module1.class1',
                        'module4.name4',
                        'module6.attr6a',
                        'module6.attr6a.class6',
                        'module6.attr6a.class6.attr6b',
                        'module6.attr6a.class6.attr6b.attr6c'
                    },
                    'defined': {
                        'class': [
                            {'path': 'module2.file2.class1'}
                        ],
                        'function': [
                            {'path': 'module2.file2.func1'}
                        ],
                        'name': [
                            {'path': 'module2.file2.name1'},
                            {'path': 'module2.file2.name2'}
                        ]
                    },
                    'ast_imported': {
                        'func1': 'module1.func1',
                        'class1': 'module1.class1',
                        'name4': 'module4.name4',
                        'attr6a': 'module6.attr6a',
                        'file2': 'module1.file2'
                    }
                },
                '/module1/__init__.py': {
                    'dot_path': 'module1.__init__',
                    'used': set(),
                    'defined': {
                        'class': [],
                        'function': [],
                        'name': []
                    },
                    'ast_imported': {
                        'func1': 'module1.file1.func1',
                        'name1': 'module1.file1.name1',
                        'class1': 'module1.dir1.file1.class1',
                        'models': 'module1.models'
                    }
                },
                '/module3/file3.py': {
                    'dot_path': 'module3.file3',
                    'used': {
                        'module6.func6',
                        'module7.class7'
                    },
                    'defined': {
                        'class': [{'path': 'module3.file3.class1'}],
                        'function': [],
                        'name': [{'path': 'module3.file3.name1'}]
                    },
                    'ast_imported': {
                        'func6': 'module6.func6',
                        'class7': 'module7.class7'
                    }
                }
            },
            {
                'class': [
                    {'path': 'module2.file2.class1'},
                    {'path': 'module3.file3.class1'}
                ],
                'function': [
                    {'path': 'module2.file2.func1'}
                ],
                'name': [
                    {'path': 'module2.file2.name1'},
                    {'path': 'module2.file2.name2'},
                    {'path': 'module3.file3.name1'}
                ]
            },
            {
                'module1.func1',
                'module1.class1',
                'module4.name4',
                'module6.attr6a',
                'module6.attr6a.class6',
                'module6.attr6a.class6.attr6b',
                'module6.attr6a.class6.attr6b.attr6c',
                'module6.func6',
                'module7.class7'
            },
            {
                'module1.func1': 'module1.file1.func1',
                'module1.name1': 'module1.file1.name1',
                'module1.class1': 'module1.dir1.file1.class1'
            }
        )]
    },
    'test_get_relpath_from_import': {
        'names': ('initial', 'expected'),
        'params': [
            ({'level': 0, 'module': 'django.conf.urls'}, 'django.conf.urls'),
            ({'level': 1, 'module': 'views'}, 'apps.core.views'),
            ({'level': 2, 'module': 'models'}, 'apps.models'),
            ({'level': 1, 'module': None}, 'apps.core'),
            ({'level': 3, 'module': 'admin'}, 'admin'),
            ({'level': 4, 'module': 'utils', 'lineno': 1}, 'error'),
        ]
    },
    'test_process_items': {
        'names': ('ast_used', 'ast_imported', 'ast_defined', 'used', 'defined'),
        'params': [(
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
        ), (
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
        )]
    },
    'test_generic_visit': {
        'names': ('node', 'inner', 'expected'),
        'params': [(
            ast.parse('from module import func\nn = 1'),
            False,
            [(ast.ImportFrom, False), (ast.Assign, False)]
        ), (
            ast.parse('from module import func\nn = 1'),
            True,
            [(ast.ImportFrom, True), (ast.Assign, True)]
        ), (
            ast.Attribute(attr='attr_one', value=ast.Name(id='name', ctx=ast.Load())),
            False,
            [(ast.Name, False)]
        ), (
            ast.Attribute(attr='attr_one', value=ast.Name(id='name', ctx=ast.Load())),
            True,
            [(ast.Name, True)]
        )]
    },
    'test_visit': {
        'names': ('node', 'inner', 'visited', 'generic'),
        'params': [
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
        ]
    },
    'test_visit_attribute': {
        'names': ('node', 'expected'),
        'params': [(
            ast.Attribute(value=ast.Attribute(attr='attr', value=ast.Name(id='self')),
                          attr='func', ctx=ast.Store()),
            []
        ), (
            ast.Attribute(value=ast.Attribute(attr='attr', value=ast.Name(id='self')),
                          attr='func', ctx=ast.Load()),
            []
        ), (
            ast.Attribute(value=ast.Attribute(attr='attr', value=ast.Name(id='class')),
                          attr='func', ctx=ast.Load()),
            [['func', 'attr', 'class']]
        ), (
            ast.Attribute(value=ast.Name(id='class'), attr='func', ctx=ast.Load()),
            [['func', 'class']]
        ), (
            ast.Attribute(value=ast.Attribute(attr='attr', value=ast.Load()),
                          attr='func', ctx=ast.Load()),
            []
        )]
    },
    'test_visit_classdef': {
        'names': ('node', 'defined_exist'),
        'params': [
            (ast.ClassDef(name='class_one', col_offset=0), True),
            (ast.ClassDef(name='class_one', col_offset=1), False),
            (ast.ClassDef(name='class_one', col_offset=2), False)
        ]
    },
    'test_visit_functiondef': {
        'names': ('node', 'defined_exist'),
        'params': [
            (ast.FunctionDef(name='function_one', col_offset=0), True),
            (ast.FunctionDef(name='function_one', col_offset=1), False),
            (ast.FunctionDef(name='function_one', col_offset=2), False)
        ]
    },
    'test_visit_importfrom': {
        'names': ('node', 'expected'),
        'params': [(
            ast.ImportFrom(names=[ast.alias(name='Foo', asname='Bar')],
                           module='apps.app.module', level=0),
            {'Bar': 'apps.app.module.Foo'}
        ), (
            ast.ImportFrom(names=[ast.alias(name='Foo', asname=None)],
                           module=None, level=0),
            {'Foo': 'Foo'}
        )]
    },
    'test_visit_name': {
        'names': ('node', 'inner', 'defined', 'used'),
        'params': [
            (ast.Name(ctx=ast.Load(), id='name'), True, [], ['name']),
            (ast.Name(ctx=ast.Load(), id='name'), False, [], ['name']),
            (ast.Name(ctx=ast.Store(), id='name'), True, [], []),
            (ast.Name(ctx=ast.Store(), id='name'), False, [{'path': 'apps.core.module.name'}], [])
        ]
    },
    'test_get_dot_relpath': {
        'names': ('base', 'path', 'expected'),
        'params': [
            ('/apps/', '/apps/', '.'),
            ('/apps', '/apps/', '.'),
            ('/apps/', '/app/test.py', 'error'),
            ('/apps/', 'test.py', 'error'),
            ('/apps/', '/apps/test.py', 'test'),
            ('/apps/', '/apps/core/test.py', 'core.test'),
            ('/apps/', '/apps/core/module/', 'core.module'),
            ('/apps/core/module/', '/apps/', 'error')
        ]
    },
    'test_separated': {
        'names': ('arguments', 'expected'),
        'params': [
            (('blue', '-'), ('---text---', 'blue')),
            (('red', '*'), ('***text***', 'red')),
            (('green',), ('===text===', 'green'))
        ]
    },
    'test_error': {
        'names': ('code', 'str_args', 'expected'),
        'params': [
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
        ]
    },
    'test_report': {
        'names': ('unused', 'sep_expected', 'expected'),
        'params': [
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
            (
                {'class': [], 'function': [], 'name': []},
                ('NO UNUSED PYTHON CODE', 'green'),
                []
            )
        ]
    }
}
