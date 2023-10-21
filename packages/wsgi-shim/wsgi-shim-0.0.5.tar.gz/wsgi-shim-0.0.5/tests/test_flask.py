import re

from wsgi_shim.wsgi_shim import cli_backend

from tests.conftest import run_passenger_wsgi_py


def test_install_passenger_wsgi_py_normal_flask(
        tmp_path_world_readable,
        monkeypatch,
        passenger_block,
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
    log_file = tmp_path_world_readable / 'logfile'
    config_file = tmp_path_world_readable / 'config.toml'
    config_file.write_text(f"""
    [passenger]
    {passenger_block}
    [wsgi]
    module = "tests.flask_example"
    app = "app"
    [environment]
    LOG_FILENAME = "{log_file}"
    """)
    maint_path = tmp_path_world_readable / 'tmp' / 'maint.txt'
    maint_path.unlink()
    monkeypatch.setenv('PWD', str(tmp_path_world_readable))
    html, status, headers = run_passenger_wsgi_py(tmp_path_world_readable)
    log = log_file.read_text()
    assert re.search(r'Hello, World', html)
    assert status == '200 OK'
    assert len(headers) == 2
    assert "INFO tests.flask_example MainThread : Request: /" in log
