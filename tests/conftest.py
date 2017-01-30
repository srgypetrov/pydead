import os
import pytest

from src.parsers import PyParser
from src.utils import ParsedItem


@pytest.fixture
def filepath(request):

    def get_path(filename=''):
        return os.path.join(os.path.dirname(__file__), 'test_files/', filename)

    paths = {
        'test_get_ast_node': get_path('file1.py'),
        'test_get_ast_node_invalid': get_path('foo/file2.py'),
        'test_search': get_path()
    }

    return paths.get(request.node.name)


@pytest.fixture
def pyparser_filled():
    parser = PyParser()
    parser.relpath = 'apps.core.module'
    parser.imported = {
        'url': 'django.conf.urls.url',
        'FooView': 'apps.foo.views.FooView',
        'os': 'os',
    }
    parser.defined = set([
        'apps.core.module.function1', 'apps.core.module.function2'
    ])
    parser.used = set([
        ParsedItem('apps.core.module.url', 'url', '', '', '10'),
        ParsedItem('apps.core.module.FooView', 'FooView', '', '', '20'),
        ParsedItem('apps.core.module.function1', 'function1', '', '', '30'),
        ParsedItem('apps.core.module.function3', 'function3', '', '', '40'),
    ])
    parser.class_child_names = set([
        'function3_40', 'FooView_20'
    ])
    return parser


@pytest.fixture
def pyparser_clear():
    parser = PyParser()
    parser.relpath = 'apps.core.module'
    parser.imported = {}
    parser.defined = set()
    parser.used = set()
    return parser


@pytest.fixture
def result_items():
    defined = {
        'apps.core.shortcuts.short',
        'apps.profile.shortcuts.short',
        'apps.core.shortcuts.get_object_or_none',
        'apps.core.templatetags.core.profile_tag',
        'apps.profile.templatetags.profile.profile_tag',
        'apps.profile.templatetags.user.profile_tag',
        'apps.core.templatetags.core.user_tag',
        'apps.profile.templatetags.profile.user_tag',
    }
    used = {
        'get_current_timezone',
        'apps.core.shortcuts.get_object_or_none',
        'profile_tag',
        'django.core.context_processors.request',
        'os',
        'core.user_tag',
    }
    return defined, used
