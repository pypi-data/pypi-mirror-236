import importlib.resources
import importlib.util
import os
import re
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path
from unittest import mock

import pytest
from wsgi_shim import check_path_is_not_world_readable
from wsgi_shim import check_path_is_world_readable
from wsgi_shim import Config
from wsgi_shim import get_app
from wsgi_shim import is_path_world_readable
from wsgi_shim import load_config
from wsgi_shim import WSGIConfigException
from wsgi_shim.wsgi_shim import check_venv_path
from wsgi_shim.wsgi_shim import cli_backend
from wsgi_shim.wsgi_shim import cli_parse
from wsgi_shim.wsgi_shim import create_new_file
from wsgi_shim.wsgi_shim import is_path_world_or_unsafe_gid_writable
from wsgi_shim.wsgi_shim import is_safe_gid

from tests.conftest import run_app
from tests.conftest import run_passenger_wsgi_py


def test_safe_gid_false(monkeypatch):
    @dataclass
    class PasswordEntry:
        pw_gid: int = 9999
        pw_name: str = 'username'

    @dataclass
    class GroupEntry:
        gr_name: str = 'groupname'

    monkeypatch.setattr('os.getuid', lambda: 9999)
    monkeypatch.setattr('pwd.getpwuid', lambda _: PasswordEntry())
    monkeypatch.setattr('grp.getgrgid', lambda _: GroupEntry())
    assert not is_safe_gid(9999)


@pytest.mark.parametrize(
    'uid,gid,uname,gname,file_gid',
    [
        pytest.param(
            9999, 8888, 'username', 'groupname', 1111, id='differ_gid',
        ),
        pytest.param(
            9999, 8888, 'name', 'name', 8888, id='same_name',
        ),
    ],
)
def test_safe_gid_true(uid, gid, uname, gname, file_gid, monkeypatch):
    @dataclass
    class PasswordEntry:
        pw_gid: int = gid
        pw_name: str = uname

    @dataclass
    class GroupEntry:
        gr_name: str = gname

    monkeypatch.setattr('os.getuid', lambda: uid)
    monkeypatch.setattr('pwd.getpwuid', lambda _: PasswordEntry())
    monkeypatch.setattr('grp.getgrgid', lambda _: GroupEntry())
    assert is_safe_gid(file_gid)  # noqa


def test_is_path_world_readable_no_file():
    with pytest.raises(WSGIConfigException, match=r'does not exist'):
        is_path_world_readable(Path('/dev/null/not_a_file'))


def test_is_path_world_readable_true(tmp_path_world_readable):
    file_path = tmp_path_world_readable / 'foo'
    create_new_file(file_path)
    assert is_path_world_readable(file_path)


def test_check_path_is_world_readable_fail():
    file = Path('/root')
    with pytest.raises(WSGIConfigException, match=r'not world readable'):
        check_path_is_world_readable(file)


def test_check_path_is_not_world_readable_fail():
    file = Path('/')
    with pytest.raises(WSGIConfigException, match=r'is world readable'):
        check_path_is_not_world_readable(file)


def test_is_path_world_or_unsafe_gid_writable_no_path():
    with pytest.raises(WSGIConfigException, match=r'does not exist'):
        is_path_world_or_unsafe_gid_writable(Path('/dev/null/no_exist'))


def test_is_path_world_or_unsafe_gid_writable_file(tmp_path_world_readable):
    tmp_path_world_readable.chmod(tmp_path_world_readable.stat().st_mode | 0o003)
    file_path = tmp_path_world_readable / 'foo'
    create_new_file(file_path)
    file_path.chmod(file_path.stat().st_mode | 0o002)
    assert is_path_world_or_unsafe_gid_writable(file_path)


def test_is_path_world_or_unsafe_gid_writable_dir(tmp_path_world_readable):
    tmp_path_world_readable.chmod(tmp_path_world_readable.stat().st_mode | 0o003)
    dir_path = tmp_path_world_readable / 'foo'
    dir_path.mkdir()
    dir_path.chmod(dir_path.stat().st_mode | 0o003)
    assert is_path_world_or_unsafe_gid_writable(dir_path)


def test_check_venv_path_not_in_venv(monkeypatch):
    monkeypatch.setattr('sys.base_prefix', sys.prefix)
    with pytest.raises(WSGIConfigException, match=r'from inside a virtual'):
        check_venv_path(Path(), Path())


def test_check_venv_path_mismatch():
    with pytest.raises(WSGIConfigException, match=r'does not match'):
        check_venv_path(
            passenger_python=Path('/dev/null/nonexistent/nonexistent'),
            passenger_app_root=Path(),
        )


def test_check_venv_path_error_inside():
    with pytest.raises(WSGIConfigException, match=r'cannot be inside'):
        check_venv_path(
            passenger_python=Path(sys.prefix) / 'bin' / 'python',
            passenger_app_root=Path('/'),
        )


def test_load_config_empty():
    path = Path('/dev/null')
    data = load_config(path)
    assert isinstance(data, dict)
    assert len(data) == 0


def test_load_config_valid_1(tmp_path):
    file = tmp_path / 'config.toml'
    file.write_text("""
    [wsgi]
    """)
    data = load_config(file)
    assert isinstance(data, dict)
    assert data == {'wsgi': {}}


def test_load_config_fail_perms(tmp_path):
    file = tmp_path / 'config.toml'
    file.write_text("""
    [wsgi]
    """)
    file.chmod(0o200)
    with pytest.raises(WSGIConfigException, match=r'Permission denied'):
        load_config(file)


def test_load_config_fail_missing(tmp_path):
    file = tmp_path / 'config.toml'
    with pytest.raises(WSGIConfigException, match=r'file not found'):
        load_config(file)


def test_load_config_fail_toml_syntax(tmp_path):
    file = tmp_path / 'config.toml'
    file.write_text("""
    [
    """)
    with pytest.raises(WSGIConfigException, match=r'syntax error'):
        load_config(file)


def test_load_config_fail_toml_duplicated_section(tmp_path):
    file = tmp_path / 'config.toml'
    file.write_text("""
    [wsgi]
    [wsgi]
    """)
    with pytest.raises(WSGIConfigException, match=r'syntax error'):
        load_config(file)


@pytest.mark.parametrize(
    'section',
    [
        'wsgi',
        'secret_files',
        'environment',
    ],
)
def test_load_config_fail_toml_not_section(section, tmp_path):
    file = tmp_path / 'config.toml'
    file.write_text(f"""
    {section} = "foo"
    [passenger]
    """)
    with pytest.raises(WSGIConfigException, match=r'not a section'):
        data = load_config(file)
        Config.from_toml_dict(data, tmp_path)


@pytest.mark.parametrize(
    'section,key',
    [
        ('wsgi', 'module'),
        ('wsgi', 'app'),
    ],
)
def test_load_config_fail_toml_values_not_str_1(section, key):
    data = {section: {key: 1}}
    if section != 'passenger':
        data['passenger'] = {}
    with pytest.raises(WSGIConfigException, match=fr'{section}.{key} not a string'):
        Config.from_toml_dict(data, Path())


@pytest.mark.parametrize(
    'section,key',
    [
        ('secret_files', 'filename'),
        ('environment', 'foobar'),
    ],
)
def test_load_config_fail_toml_values_not_str(section, key):
    data = {'passenger': {}, section: {key: 1}}
    with pytest.raises(WSGIConfigException, match=fr'{section}.{key} not a string'):
        Config.from_toml_dict(data, Path())


@pytest.mark.parametrize(
    'section,key',
    [
        ('secret_files', '0_key_leading_digit'),
        ('environment', 'key_$_special_char'),
    ],
)
def test_load_config_fail_toml_invalid_key(section, key):
    data = {'passenger': {}, section: {key: 1}}
    with pytest.raises(WSGIConfigException, match=fr'invalid key .* in \[{section}\]'):
        Config.from_toml_dict(data, Path())


def test_load_config_fail_toml_duplicate_keys():
    data = {
        'passenger': {},
        'wsgi': {},
        'secret_files': {'key': 'value1'},
        'environment': {'key': 'value2'},
    }
    with pytest.raises(WSGIConfigException, match=r'duplicated across sections'):
        Config.from_toml_dict(data, Path())


def test_update_os_environment_conflict(monkeypatch):
    data = {
        'passenger': {},
        'environment': {'FOOBAR': 'value'},
    }
    monkeypatch.setenv('FOOBAR', 'something')
    with pytest.raises(WSGIConfigException, match=r'already has key'):
        config = Config.from_toml_dict(data, Path())
        config.update_os_environment()


@mock.patch.dict(os.environ, {})
def test_update_os_environment_success():
    data = {
        'passenger': {},
        'environment': {'FOOBAR': 'value'},
    }
    config = Config.from_toml_dict(data, Path())
    assert 'FOOBAR' not in os.environ
    config.update_os_environment()
    assert os.environ['FOOBAR'] == 'value'


def test_check_secret_files_fail_missing(tmp_path):
    missing_file = tmp_path / 'not_there'
    data = {
        'passenger': {},
        'secret_files': {'SECRET': str(missing_file)},
    }
    config = Config.from_toml_dict(data, Path())
    with pytest.raises(WSGIConfigException, match=r'is missing or not readable'):
        config.check_secret_files()


def test_check_secret_files_fail_cant_read(tmp_path):
    unreadable_file = tmp_path / 'unreadable'
    unreadable_file.touch(mode=0o000)
    data = {
        'passenger': {},
        'secret_files': {'SECRET': str(unreadable_file)},
    }
    config = Config.from_toml_dict(data, Path())
    with pytest.raises(WSGIConfigException, match=r'is missing or not readable'):
        config.check_secret_files()


def test_check_secret_files_fail_too_permissive(tmp_path):
    permissive_file = tmp_path / 'permissive'
    permissive_file.touch()
    permissive_file.chmod(mode=0x777)
    data = {
        'passenger': {},
        'secret_files': {'SECRET': str(permissive_file)},
    }
    config = Config.from_toml_dict(data, Path())
    with pytest.raises(WSGIConfigException, match=r'not adequately protected'):
        config.check_secret_files()


def test_check_secret_files_fail_not_absolute():
    data = {
        'passenger': {},
        'secret_files': {'FOOBAR': 'not_absolute_path'},
    }
    config = Config.from_toml_dict(data, Path())
    with pytest.raises(WSGIConfigException, match=r'not an absolute path'):
        config.check_secret_files()


def test_hello_world():
    from src.wsgi_shim.hello_world import app_hello_world as app_under_test
    html, status, headers = run_app(app_under_test)
    assert re.search(r'Hello, World', html)
    assert status == '200 OK'
    assert len(headers) == 2


def test_main_maintenance_mode_normal(tmp_path, passenger_block):
    passenger_tmp_dir = tmp_path / 'tmp'
    passenger_tmp_dir.mkdir(mode=0o755)
    maint_file = passenger_tmp_dir / 'maint.txt'
    maint_file.touch()
    config_file = tmp_path / 'config.toml'
    config_file.write_text(f"""
    [passenger]
    {passenger_block}
    """)
    app = get_app(tmp_path)
    html, status, headers = run_app(app)
    assert re.search(r'put it into maintenance mode', html)
    assert status == '503 Service Unavailable'
    assert len(headers) == 3


def test_main_fail_venv_mismatch(tmp_path):
    config_file = tmp_path / 'config.toml'
    config_file.write_text(f"""
    [passenger]
    passenger_python="{'foo'}"
    [wsgi]
    module = "not_there"
    app = "unused"
    """)
    app = get_app(tmp_path)
    html, status, headers = run_app(app)
    assert re.search(r'does not match passenger_python', html)
    assert status == '503 Service Unavailable'
    assert len(headers) == 3


def test_main_fail_no_module(tmp_path, passenger_block):
    config_file = tmp_path / 'config.toml'
    config_file.write_text(f"""
    [passenger]
    {passenger_block}
    [wsgi]
    module = "not_there"
    app = "unused"
    """)
    app = get_app(tmp_path)
    html, status, headers = run_app(app)
    assert re.search(r'Cannot load not_there.unused: No module', html)
    assert status == '503 Service Unavailable'
    assert len(headers) == 3


def test_main_fail_module_perms(tmp_path, monkeypatch, passenger_block):
    unreadable_file = tmp_path / 'unreadable.py'
    unreadable_file.touch(mode=0o000)
    monkeypatch.syspath_prepend(tmp_path)
    config_file = tmp_path / 'config.toml'
    config_file.write_text(f"""
    [passenger]
    {passenger_block}
    [wsgi]
    module = "unreadable"
    app = "unused"
    """)
    app = get_app(tmp_path)
    html, status, headers = run_app(app)
    assert re.search(r'Cannot load .* Permission denied: ', html)
    assert status == '503 Service Unavailable'
    assert len(headers) == 3


def test_main_fail_no_app(tmp_path, monkeypatch, passenger_block):
    empty_file = tmp_path / 'empty_module.py'
    empty_file.touch()
    monkeypatch.syspath_prepend(tmp_path)
    config_file = tmp_path / 'config.toml'
    config_file.write_text(f"""
    [passenger]
    {passenger_block}
    [wsgi]
    module = "empty_module"
    app = "unused"
    """)
    app = get_app(tmp_path)
    html, status, headers = run_app(app)
    assert re.search(r'Cannot load .* module .* has no attribute', html)
    assert status == '503 Service Unavailable'
    assert len(headers) == 3


def test_main_normal_module_file(tmp_path, monkeypatch, passenger_block):
    with importlib.resources.files('wsgi_shim').joinpath('hello_world.py').open('r') as f:
        app_source = f.read()
    app_module_file = tmp_path / 'myapp.py'
    app_module_file.write_text(app_source)
    config_file = tmp_path / 'config.toml'
    config_file.write_text(f"""
    [passenger]
    {passenger_block}
    [wsgi]
    module = "{app_module_file}"
    app = "app_hello_world"
    """)
    monkeypatch.syspath_prepend(tmp_path)
    app = get_app(tmp_path)
    html, status, headers = run_app(app)
    assert re.search(r'Hello, World', html)
    assert status == '200 OK'
    assert len(headers) == 2


def test_main_normal_dir_module(tmp_path, passenger_block):
    root_path = tmp_path
    mysite_path = root_path / 'mysite'
    mysite_path.mkdir()
    mypackage_path = mysite_path / 'mypackage'
    mypackage_path.mkdir()
    init_path = mypackage_path / '__init__.py'
    init_path.touch()
    wsgi_py_path = mypackage_path / 'wsgi.py'
    wsgi_py_path.write_text(
        textwrap.dedent("""
            from wsgi_shim.hello_world import app_hello_world
            application = app_hello_world
        """),
    )
    www_path = root_path / 'www'
    www_path.mkdir()
    config_file = www_path / 'config.toml'
    config_file.write_text(f"""
    [passenger]
    {passenger_block}
    [wsgi]
    module = "{mypackage_path}"
    app = "wsgi.application"
    """)
    app = get_app(www_path)
    html, status, headers = run_app(app)
    assert re.search(r'Hello, World', html)
    assert status == '200 OK'
    assert len(headers) == 2


def test_main_normal_module_default(tmp_path, passenger_block):
    config_file = tmp_path / 'config.toml'
    config_file.write_text(f"""
    [passenger]
    {passenger_block}
    [wsgi]
    module = "wsgi_shim.hello_world"
    app = "app_hello_world"
    """)
    app = get_app(tmp_path)
    html, status, headers = run_app(app)
    assert re.search(r'Hello, World', html)
    assert status == '200 OK'
    assert len(headers) == 2


def test_cli_parse_help(monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['wsgi-shim', '--help'])
    with pytest.raises(SystemExit) as exc_info:
        cli_parse()
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert 'Usage:' in captured.err


def test_cli_parse_bad_argv_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['wsgi-shim'])
    with pytest.raises(SystemExit) as exc_info:
        cli_parse()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert 'Usage:' in captured.err


def test_cli_parse_bad_command(monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['wsgi-shim', 'bad_command', 'bad_option'])
    with pytest.raises(SystemExit) as exc_info:
        cli_parse()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert 'Usage:' in captured.err


def test_cli_parse_good_command(monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['wsgi-shim', 'install', '/dir/path'])
    command, passenger_app_root = cli_parse()
    assert command == 'install'
    assert passenger_app_root == Path('/dir/path')


def test_cli_backend_install(tmp_path_world_readable, monkeypatch, capsys):
    monkeypatch.setattr(
        'sys.argv',
        [
            'wsgi-shim',
            'install',
            str(tmp_path_world_readable),
        ],
    )
    cli_backend()
    captured = capsys.readouterr()
    assert 'Success' in captured.out
    passenger_tmp_path = tmp_path_world_readable / 'tmp'
    assert passenger_tmp_path.is_dir()
    restart_path = passenger_tmp_path / 'restart.txt'
    assert restart_path.is_file()
    maint_path = passenger_tmp_path / 'maint.txt'
    assert maint_path.is_file()


def test_cli_backend_check(tmp_path_world_readable, monkeypatch, capsys):
    monkeypatch.setattr(
        'sys.argv',
        [
            'wsgi-shim',
            'install',
            str(tmp_path_world_readable),
        ],
    )
    cli_backend()
    captured = capsys.readouterr()
    assert 'Success' in captured.out
    monkeypatch.setattr(
        'sys.argv',
        [
            'wsgi-shim',
            'check',
            str(tmp_path_world_readable),
        ],
    )
    cli_backend()
    captured = capsys.readouterr()
    assert 'Check passed' in captured.out


def test_install_passenger_wsgi_py_normal_maint(
        tmp_path_world_readable,
        monkeypatch,
):
    monkeypatch.setattr(
        'sys.argv',
        [
            'wsgi-shim',
            'install',
            str(tmp_path_world_readable),
        ],
    )
    cli_backend(quiet=True)
    monkeypatch.setenv('PWD', str(tmp_path_world_readable))
    html, status, headers = run_passenger_wsgi_py(tmp_path_world_readable)
    assert re.search(r'put it into maintenance mode', html)
    assert status == '503 Service Unavailable'
    assert len(headers) == 3


def test_install_passenger_wsgi_py_normal_default(
        tmp_path_world_readable,
        monkeypatch,
):
    monkeypatch.setattr(
        'sys.argv',
        [
            'wsgi-shim',
            'install',
            str(tmp_path_world_readable),
        ],
    )
    cli_backend(quiet=True)
    maint_path = tmp_path_world_readable / 'tmp' / 'maint.txt'
    maint_path.unlink()
    monkeypatch.setenv('PWD', str(tmp_path_world_readable))
    html, status, headers = run_passenger_wsgi_py(tmp_path_world_readable)
    assert re.search(r'Hello, World', html)
    assert status == '200 OK'
    assert len(headers) == 2
