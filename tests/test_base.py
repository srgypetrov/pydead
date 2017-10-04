from src import base


def test_get_unused(defined, used, expected):
    unused = base.get_unused(defined, used)
    assert unused == expected


def test_fix_init_imports(init_imports, used, expected):
    base.fix_init_imports(used, init_imports)
    assert used == expected


def test_parse_files(monkeypatch, mock_file, data, exp_defined, exp_used, exp_imports):

    def mock_file_create(basedir, path):
        file_data = data[path]
        return mock_file(lambda: None, **file_data)

    monkeypatch.setattr(base, 'PyFile', mock_file_create)

    init_imports, defined, used = base.parse_files('/basedir/', data.keys())
    assert defined == exp_defined
    assert used == exp_used
    assert init_imports == exp_imports


def test_check_error(runner):
    result = runner.invoke(base.check, ['-d', '.', '-e', '*'])
    assert isinstance(result.exception, SystemExit)
