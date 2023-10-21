# passenger_wsgi.py
"""
Phusion Passenger WSGI shim

Ultimately, the only thing this really needs to do is to define
a callable called "application" roughly like this:

    from WSGI_MODULE import WSGI_APP as application

However, because we assume users do not have direct access to the server logs
to debug their code, this bit of code (and the accompanying documentation)
helps catch many initial setup/configuration errors without users needing
to ask sysadmins to find snippets in the server error logs.

This is not WSGI middleware; it does not capture exceptions thrown by the
application.  It is up to the developer to log messages to an accessible
file to aid in further debugging and to gather site statistics.
(This could be a future enhancement for this project, though.)
"""
import datetime
import functools
import grp
import importlib.resources
import importlib.util
import os
import pwd
import re
import sys
import textwrap
import tomllib
from contextlib import contextmanager
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from types import ModuleType
from typing import cast
from typing import NoReturn
from typing import Self
from wsgiref.types import StartResponse
from wsgiref.types import WSGIApplication
from wsgiref.types import WSGIEnvironment


class WSGIConfigException(Exception):
    pass


def is_safe_gid(file_gid: int) -> bool:
    """Returns False (indicating an unsafe file_gid) when the file_gid
    matches the user's default group and that default group's name is
    not that same string as the username."""
    passwd_entry = pwd.getpwuid(os.getuid())
    if passwd_entry.pw_gid == file_gid:
        if passwd_entry.pw_name != grp.getgrgid(passwd_entry.pw_gid).gr_name:
            return False
    return True


def is_path_world_readable(path: Path) -> bool:
    if not path.exists():
        raise WSGIConfigException(f"does not exist: '{path}'")
    p = Path('/')
    for part in path.parts:
        p = p / part
        mode = 0o001 if p.is_dir() else 0o004
        if (p.stat().st_mode & mode) != mode:
            return False
    return True


def check_path_is_world_readable(path: Path) -> None:
    if not is_path_world_readable(path):
        raise WSGIConfigException(f"not world readable: '{path}'")


def check_path_is_not_world_readable(path: Path) -> None:
    if is_path_world_readable(path):
        raise WSGIConfigException(f"is world readable: '{path}'")


def is_path_world_or_unsafe_gid_writable(path: Path) -> bool:
    if not path.exists():
        raise WSGIConfigException(f"does not exist: '{path}'")
    p = Path('/')
    for part in path.parts:
        p = p / part
        p_stat = p.stat()
        mode = 0o003 if p.is_dir() else 0o002
        if (p_stat.st_mode & mode) == mode:
            return True
        if not is_safe_gid(p_stat.st_gid):
            mode = 0o030 if p.is_dir() else 0o020
            if (p.stat().st_mode & mode) == mode:
                return True
    return False


def check_path_is_not_world_or_unsafe_gid_writable(path: Path) -> None:
    if is_path_world_or_unsafe_gid_writable(path):
        raise WSGIConfigException(f"is world (or unsafe group) writable: '{path}'")


def perm_masks(path: Path, other_readable: bool = False) -> tuple[int, int]:
    path_stat = path.stat()
    if other_readable:
        if is_safe_gid(path_stat.st_gid):
            mask_bad, mask_need = 0o002, 0o005  # chmod o=rx
        else:
            mask_bad, mask_need = 0o022, 0o005  # chmod g-w,o=rx
    else:
        if is_safe_gid(path_stat.st_gid):
            mask_bad, mask_need = 0o007, 0o000  # chmod o=
        else:
            mask_bad, mask_need = 0o077, 0o000  # chmod g=,o=
    if not path.is_dir():
        mask_bad |= 0o111  # also, chmod ugo-x
        mask_need &= ~0o001  # don't need the o=x bit if not a dir
    return mask_bad, mask_need


def fix_perms(path: Path, other_readable: bool = False):
    mask_bad, mask_need = perm_masks(path, other_readable)
    path_stat = path.stat()
    old_mode = path_stat.st_mode
    new_mode = (old_mode & ~mask_bad) | mask_need
    if new_mode != old_mode:
        path.chmod(new_mode)


def check_venv_path(passenger_python: Path, passenger_app_root: Path):
    if sys.prefix == sys.base_prefix:
        raise WSGIConfigException('Must be run from inside a virtual environment')
    passenger_venv_path = passenger_python.parent.parent
    running_venv_path = Path(sys.prefix)
    if running_venv_path != passenger_venv_path:
        raise WSGIConfigException(
            'Running virtual environment does not match '
            'passenger_python in config.toml.',
        )
    if running_venv_path.is_relative_to(passenger_app_root):
        raise WSGIConfigException(
            'Virtual environment cannot be '
            'inside passenger_app_root',
        )
    venv_stat = os.stat(running_venv_path)
    venv_mask = 0o002 if is_safe_gid(venv_stat.st_gid) else 0o022
    if (venv_stat.st_mode & venv_mask) != 0:
        raise WSGIConfigException(
            f'virtual environment at {running_venv_path} '
            f'is not adequately write protected.',
        )


@dataclass
class Config:
    passenger_user: str = ''
    passenger_group: str = ''
    passenger_python: str = ''
    wsgi_module: str = ''
    wsgi_app: str = ''
    environment: dict[str, tuple[str, bool]] = field(default_factory=dict)
    maintenance_mode_path: Path = Path('/dev/null/nonexistent')
    passenger_python_path: Path = Path('/dev/null/nonexistent')

    @classmethod
    def from_toml_dict(cls, data, passenger_app_root: Path) -> Self:
        retval = cls()
        for section, required in [
            ('passenger', True),
            ('wsgi', False),
            ('secret_files', False),
            ('environment', False),
        ]:
            if not isinstance(data.get(section, {}), dict):
                raise WSGIConfigException(f'"{section}" is not a section')
            if required and section not in data:
                raise WSGIConfigException(f'Missing required [{section}]')
        for section, key, attrib in [
            ('passenger', 'passenger_user', 'passenger_user'),
            ('passenger', 'passenger_group', 'passenger_group'),
            ('passenger', 'passenger_python', 'passenger_python'),
            ('wsgi', 'module', 'wsgi_module'),
            ('wsgi', 'app', 'wsgi_app'),
        ]:
            value = data.get(section, {}).get(key, '')
            if not isinstance(value, str):
                raise WSGIConfigException(f'{section}.{key} not a string')
            setattr(retval, attrib, value)
        retval.maintenance_mode_path = passenger_app_root / 'tmp' / 'maint.txt'
        retval.passenger_python_path = Path(retval.passenger_python)
        environment_sections = [('secret_files', True), ('environment', False)]
        for section, is_secret_file in environment_sections:
            for key, value in data.get(section, {}).items():
                if re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', key) is None:
                    raise WSGIConfigException(f'invalid key "{key}" in [{section}]')
                if not isinstance(value, str):
                    raise WSGIConfigException(f'{section}.{key} not a string')
                if key in retval.environment:
                    raise WSGIConfigException(
                        f'key "{key}" duplicated across sections: '
                        f'{", ".join(name for name, _ in environment_sections)}',
                    )
                retval.environment[key] = (value, is_secret_file)
        return retval

    def check_user_group(self):
        running_user = pwd.getpwuid(os.getuid()).pw_name
        running_group = grp.getgrgid(os.getgid()).gr_name
        running = (running_user, running_group)
        configured = (self.passenger_user, self.passenger_group)
        if running != configured:
            raise WSGIConfigException(
                f'running user.group {running} does not '
                f'match config.toml settings {configured}.',
            )

    def check_secret_files(self):
        # Check that the secret_files exist and have appropriate permissions.
        # Note: Like ssh, we refuse to run if a secrets file is too widely
        # accessible.
        for key, (filename, is_secret_file) in self.environment.items():
            if is_secret_file:
                path = Path(filename)
                if not path.is_absolute():
                    raise WSGIConfigException(
                        f'secret_files.{key} '
                        f'is not an absolute path',
                    )
                if not os.access(path, os.R_OK):
                    raise WSGIConfigException(
                        f'secret_files.{key} '
                        f'is missing or not readable',
                    )
                config_stat = os.stat(path)
                config_mask = 0o007 if is_safe_gid(config_stat.st_gid) else 0o077
                if (config_stat.st_mode & config_mask) != 0:
                    raise WSGIConfigException(
                        f'secret_files.{key} '
                        f'is not adequately protected.',
                    )

    def update_os_environment(self) -> None:
        for key, (value, _) in self.environment.items():
            if key in os.environ:
                raise WSGIConfigException(f'os.environ already has key "{key}"')
            os.environ[key] = value

    def in_maintenance_mode(self) -> bool:
        return self.maintenance_mode_path.exists()


def load_config(file: Path):
    try:
        with open(file, "rb") as f:
            data = tomllib.load(f)  # assumes utf-8 encoding
    except FileNotFoundError as e:
        raise WSGIConfigException(f'Config file not found: {str(e)}')
    except PermissionError as e:
        raise WSGIConfigException(f'Config file error: {str(e)}')
    except tomllib.TOMLDecodeError as e:
        raise WSGIConfigException(f'Config file syntax error: {str(e)}')
    return data


def import_module_from_file_location(
        module_path: Path,
) -> ModuleType:
    # See: https://docs.python.org/3.11/library/importlib.html
    #      #importing-a-source-file-directly
    module_name = module_path.stem
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise WSGIConfigException(
            f'Cannot load {module_name} from {module_path}: '
            f'spec_from_file_location returned None.',
        )
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None  # keep mypy happy
    spec.loader.exec_module(module)
    return module


def application503(
        _environ: WSGIEnvironment,
        start_response: StartResponse,
        html: str,
) -> list[bytes]:
    html_as_bytes = html.encode('utf-8')
    start_response(
        '503 Service Unavailable',
        [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(html_as_bytes))),
            ('Retry-After', '60'),
        ],
    )
    return [html_as_bytes]


html_template = textwrap.dedent('''\
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8"/>
    <title>{title} (503)</title>
    </head>
    <body>
    <h1>{title}</h1>
    <p>{reason}</p>
    {details}</body>
    </html>
''')


def get_app(passenger_app_root: Path | None = None) -> WSGIApplication:
    """
    Returns the appropriate application callable to use.
    """
    try:
        if passenger_app_root is None:  # pragma: no cover
            if (working_dir := os.environ.get('PWD')) is None:
                raise WSGIConfigException('Cannot determine passenger_app_root')
            passenger_app_root = Path(working_dir)
        config_file = passenger_app_root / 'config.toml'
        toml_dict = load_config(config_file)
        config = Config.from_toml_dict(toml_dict, passenger_app_root)
        check_venv_path(config.passenger_python_path, passenger_app_root)
        config.check_user_group()
        if config.in_maintenance_mode():
            return cast(
                WSGIApplication,
                functools.partial(
                    application503,
                    html=html_template.format(
                        title='Maintenance',
                        reason='The developer of this site has put it into '
                               'maintenance mode.  Please try again later.',
                        details=f'<p>{datetime.datetime.now()}</p>',
                    ),
                ),
            )
        config.check_secret_files()
        config.update_os_environment()
        if config.wsgi_module.startswith('/'):
            module_path = Path(config.wsgi_module)
            if module_path.suffix == '.py':
                if module_path.is_dir():
                    raise WSGIConfigException(
                        f'[wsgi].module of "{module_path}" cannot be a '
                        f'directory ending with ".py"',
                    )
                app_name = config.wsgi_app
                try:
                    module = import_module_from_file_location(module_path)
                except ModuleNotFoundError as exc_info:
                    raise WSGIConfigException(
                        f'Cannot import {app_name} from {module_path}: '
                        f'{str(exc_info)}',
                    )
            else:
                if not module_path.is_dir():
                    raise WSGIConfigException(
                        f'[wsgi].module of "{module_path}" expected to be a directory',
                    )
                s = config.wsgi_app.rsplit('.', maxsplit=1)
                if len(s) != 2:
                    raise WSGIConfigException(
                        'When [wsgi].module is a directory, [wsgi].app must of '
                        'the form submodule.app_name',
                    )
                submodule_name, app_name = s
                package_path = module_path
                package_name = package_path.stem
                sys.path.insert(0, str(package_path.parent))
                importlib.import_module(package_name)
                sys.path.pop(0)
                try:
                    module = importlib.import_module(
                        name=f'.{submodule_name}',
                        package=package_name,
                    )
                except ModuleNotFoundError as exc_info:
                    raise WSGIConfigException(
                        f'Cannot import {config.wsgi_app} from {config.wsgi_module}: '
                        f'{str(exc_info)}',
                    )
            return getattr(module, app_name)
        else:
            # See: https://docs.python.org/3.11/library/importlib.html
            #      #importing-programmatically
            try:
                return getattr(
                    importlib.import_module(config.wsgi_module),
                    config.wsgi_app,
                )
            except (ModuleNotFoundError, PermissionError, AttributeError) as exc_info:
                raise WSGIConfigException(
                    f'Cannot load {config.wsgi_module}.{config.wsgi_app}: '
                    f'{str(exc_info)}',
                )
    except WSGIConfigException as exc_info:
        # Configuration Error Mode
        return cast(
            WSGIApplication,
            functools.partial(
                application503,
                html=html_template.format(
                    title='Error Page',
                    reason='This site has experienced a configuration '
                           'error or exception.',
                    details=textwrap.dedent(f'''\
                        <pre>
                        passenger_app_root: {passenger_app_root}
                               process uid: {pwd.getpwuid(os.getuid()).pw_name}
                               process gid: {grp.getgrgid(os.getgid()).gr_name}
                                 timestamp: {datetime.datetime.now()}

                        Exception Details
                        {{}}
                        </pre>
                    ''').format(str(exc_info)),
                ),
            ),
        )


def invoked_as() -> str:
    if sys.argv[0].endswith('__main__.py'):
        return 'python -m wsgi_shim'
    else:
        return 'wsgi_shim'


def usage(return_code: int = 1) -> NoReturn:
    """
    Print an error message to stderr and exit with return_code.
    """
    argv0 = invoked_as()
    print(
        textwrap.dedent(f"""
        Usage:
            {argv0} install passenger_app_root
                This will install a passenger_wsgi.py file, initial
                config.toml file, and create an empty tmp subdirectory
                in the given passenger_app_root directory.  Will not
                overwrite existing files.

            {argv0} check passenger_app_root
                Performs a check on the passenger_app_root directory.

            Where:
                passenger_app_root is an absolute path beginning with '/'.
        """)[1:-1],
        file=sys.stderr,
    )
    raise SystemExit(return_code)


def cli_parse() -> tuple[str, Path]:
    if '--help' in sys.argv:
        usage(return_code=0)
    argc = len(sys.argv)
    if argc != 3:
        usage()
    command, passenger_app_root = sys.argv[1], Path(sys.argv[2])
    if command not in ('install', 'check'):
        usage()
    if not passenger_app_root.is_absolute():
        usage()
    return command, passenger_app_root


@contextmanager
def temp_umask(mask: int):
    old_mask = os.umask(mask)
    try:
        yield
    finally:
        os.umask(old_mask)


def cleanup(items: list[Path]) -> None:
    for item in reversed(items):
        if item.is_dir():
            try:
                item.rmdir()
            except OSError as exc_info:
                if exc_info.strerror != 'Directory not empty':
                    raise
        else:
            item.unlink(missing_ok=True)


def create_new_file(path: Path, content: str = '', umask: int = 0o022) -> None:
    with temp_umask(umask):
        with open(path, mode='x') as f:
            f.write(content)


def cli_install(passenger_app_root: Path, quiet: bool = False) -> None:
    passenger_wsgi_py = passenger_app_root / 'passenger_wsgi.py'
    created_paths: list[Path] = list()
    try:
        create_new_file(
            path=passenger_wsgi_py,
            content=textwrap.dedent('''
                # Created with wsgi_shim
                import wsgi_shim

                application = wsgi_shim.get_app()
            ''')[1:],
        )
    except FileExistsError:
        cleanup(created_paths)
        raise WSGIConfigException(
            f"Error: will not overwrite existing: "
            f"'{passenger_wsgi_py}'",
        )
    created_paths.append(passenger_wsgi_py)
    fix_perms(passenger_wsgi_py, other_readable=True)

    config_toml = passenger_app_root / 'config.toml'
    with importlib.resources.files('wsgi_shim.templates').joinpath(
            'config.toml',
    ).open('r') as f:
        config_template = f.read()
    config_contents = config_template.format(
        user=passenger_app_root.owner(),
        group=passenger_app_root.group(),
        passenger_app_root=passenger_app_root,
        passenger_python=Path(sys.prefix) / 'bin' / 'python',
    )
    try:
        create_new_file(
            path=config_toml,
            content=config_contents,
            umask=0o077,
        )
    except FileExistsError:
        cleanup(created_paths)
        raise WSGIConfigException(
            f"Error: will not overwrite existing: "
            f"'{config_toml}'",
        )
    created_paths.append(config_toml)
    fix_perms(config_toml, other_readable=False)

    tmp_dir = passenger_app_root / 'tmp'
    try:
        tmp_dir.mkdir()
    except FileExistsError:
        cleanup(created_paths)
        raise WSGIConfigException(
            f"Error: will not overwrite existing: "
            f"'{tmp_dir}'",
        )
    created_paths.append(tmp_dir)
    fix_perms(tmp_dir, other_readable=True)

    restart_txt = tmp_dir / 'restart.txt'
    restart_txt.touch()
    created_paths.append(restart_txt)
    fix_perms(restart_txt, other_readable=True)

    maint_txt = tmp_dir / 'maint.txt'
    maint_txt.touch(mode=0o640)
    created_paths.append(maint_txt)
    fix_perms(maint_txt, other_readable=False)
    if not quiet:
        print('Success.  Created the following:')
        for path in created_paths:
            print(f'    {path}')


def cli_check(passenger_app_root: Path, quiet: bool = False) -> None:
    passenger_wsgi_py = passenger_app_root / 'passenger_wsgi.py'
    check_path_is_world_readable(passenger_wsgi_py)
    if not passenger_wsgi_py.is_file():
        raise WSGIConfigException(f"not a file: '{passenger_wsgi_py}'")
    contents = passenger_wsgi_py.read_text()
    try:
        compile(contents, str(passenger_wsgi_py), mode='exec')
    except (SyntaxError, ValueError) as exc_info:
        raise WSGIConfigException(f"Cannot parse: '{passenger_wsgi_py}': {exc_info}")
    except IsADirectoryError:
        raise WSGIConfigException(f"not a file: '{passenger_wsgi_py}'")
    tmp_dir = passenger_app_root / 'tmp'
    check_path_is_world_readable(tmp_dir)
    if not tmp_dir.is_dir():
        raise WSGIConfigException(f"not a directory: '{tmp_dir}'")
    restart_txt = tmp_dir / 'restart.txt'
    if restart_txt.exists():
        check_path_is_world_readable(restart_txt)
        if not restart_txt.is_file():
            raise WSGIConfigException(f"not a file: '{restart_txt}'")
    config_toml = passenger_app_root / 'config.toml'
    check_path_is_not_world_readable(config_toml)
    toml_dict = load_config(config_toml)
    config = Config.from_toml_dict(toml_dict, passenger_app_root)
    check_venv_path(config.passenger_python_path, passenger_app_root)
    config.check_secret_files()
    if not quiet:
        print('Check passed')


def cli_backend(quiet: bool = False):
    command, passenger_app_root = cli_parse()
    check_path_is_world_readable(passenger_app_root)
    if not passenger_app_root.is_dir():
        raise WSGIConfigException(f'not a directory: {passenger_app_root}')
    running_python_path = Path(sys.prefix) / 'bin' / 'python'
    check_venv_path(running_python_path, passenger_app_root)
    if command == 'install':
        cli_install(passenger_app_root, quiet)
    elif command == 'check':
        cli_check(passenger_app_root, quiet)


def cli():  # pragma no cover
    try:
        cli_backend()
        return_code = 0
    except WSGIConfigException as exc_info:
        print(f'{str(exc_info)}', file=sys.stderr)
        return_code = 1
    raise SystemExit(return_code)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
