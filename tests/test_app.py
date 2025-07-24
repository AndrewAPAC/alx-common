import os
import tempfile
import configparser
import pytest
from unittest import mock
from alx.app import ALXapp, Paths
from cryptography.fernet import Fernet, InvalidToken
import tempfile
import logging
import stat


def test_app_sets_environment_dev_by_default():
    with mock.patch("sys.argv", ["test_app.py"]):
        app = ALXapp("Test App")
    assert app.environment == "dev"
    assert app.is_dev()


@pytest.mark.parametrize("env_flag,expected", [
    ("test", "test"),
    ("uat", "test"),
    ("prd", "prod"),
    ("production", "prod"),
])
def test_environment_flags(monkeypatch, env_flag, expected):
    monkeypatch.setattr("sys.argv", ["test_app.py", "-e", env_flag])
    app = ALXapp("Test App")
    assert app.environment == expected


def test_paths_dirs_created(tmp_path):
    # Override sys.argv to use a path under tmp_path
    dummy_script = tmp_path / "scripts" / "myapp" / "myapp.py"
    dummy_script.parent.mkdir(parents=True)
    dummy_script.write_text("#!/usr/bin/env python3")
    os.chmod(dummy_script, 0o755)

    with mock.patch("sys.argv", [str(dummy_script)]):
        app = ALXapp("Test App", appname="myapp")

    assert os.path.exists(app.paths.data)
    assert os.path.exists(app.paths.log)
    assert "myapp" in str(app.paths.logfile)


def test_read_config_creates_attributes(tmp_path):
    cfg = tmp_path / "app.ini"
    cfg.write_text("""
[DEFAULT]
foo = bar
baz = 123
    """)

    config = ALXapp.read_config(str(cfg))
    app = type("Dummy", (), {})()
    ALXapp.parse_config(app, config["DEFAULT"])

    assert app.foo == "bar"
    assert app.baz == 123


def test_read_lib_config_creates_user_file(tmp_path, monkeypatch):
    # Point XDG_CONFIG_HOME to a temp dir
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    # Create default config where __file__ is located
    test_config = "[DEFAULT]\nfoo = bar\n"
    with tempfile.TemporaryDirectory() as lib_dir:
        default_path = os.path.join(lib_dir, "alx.ini")
        with open(default_path, "w") as f:
            f.write(test_config)

        with mock.patch("alx.app.__file__", os.path.join(lib_dir, "app.py")):
            config = ALXapp.read_lib_config()

        expected_config_path = tmp_path / "alx" / "alx.ini"
        assert expected_config_path.exists()
        assert config.get("DEFAULT", "foo") == "bar"


def test_encrypt_decrypt_roundtrip(tmp_path):
    with mock.patch("sys.argv", ["test_app.py"]):
        app = ALXapp("Encryption Test")

    # Generate key
    keyfile = tmp_path / "test.key"
    key = Fernet.generate_key()
    keyfile.write_bytes(key)
    keyfile.chmod(0o600)
    app.keyfile = str(keyfile)

    plaintext = "SecretMessage"
    encrypted = app.encrypt(plaintext)
    decrypted = app.decrypt(encrypted)

    assert decrypted == plaintext


def test_decrypt_invalid_token(tmp_path):
    with mock.patch("sys.argv", ["test_app.py"]):
        app = ALXapp("Test Decryption")
    keyfile = tmp_path / "test.key"
    keyfile.write_bytes(Fernet.generate_key())
    keyfile.chmod(0o600)
    app.keyfile = str(keyfile)

    # Use a bogus encrypted value
    with pytest.raises(InvalidToken):
        app.decrypt("gAAAAABbogus")


def test_encrypt_without_keyfile_exits(monkeypatch):
    with mock.patch("sys.argv", ["test_app.py"]):
        app = ALXapp("Test No Key")
        app.keyfile = "/non/existent/keyfile"
        app._key = None  # Ensure fallback doesn't interfere

        with pytest.raises(SystemExit) as exc_info:
            app.encrypt("Test123")

        assert exc_info.value.code == 1


def test_logging_creates_file(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    log_path = tmp_path / "logs"

    with mock.patch("sys.argv", ["test_app.py"]):
        app = ALXapp("Test Logger", appname="testlogger")

        app.paths.log = log_path
        app.paths.logfile = log_path / "test.log"
        app.start_logging()  # Re-initialize logging with new path

        app.logger.info("Test log entry")
        app.logger.handlers[0].flush()

        log_content = app.paths.logfile.read_text()
        assert "Test log entry" in log_content