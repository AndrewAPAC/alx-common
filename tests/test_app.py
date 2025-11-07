# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# pytest routines for alx.app

import os
import pytest
from unittest import mock
from alx.app import ALXapp, Paths
from cryptography.fernet import Fernet, InvalidToken


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


def test_encrypt_decrypt_roundtrip(tmp_path):
    with mock.patch("sys.argv", ["test_app.py"]):
        app = ALXapp("Encryption Test")

    # Generate key
    keyfile = tmp_path / "test.key"
    key = Fernet.generate_key()
    keyfile.write_bytes(key)
    keyfile.chmod(0o600)
    app.keyfile = str(keyfile)

    plaintext = "SecretPassword"
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


# Fix test_parse_config_section_without_defaults
def test_parse_config_section_without_defaults(tmp_path):
    """Test parsing with include_defaults=False"""
    cfg = tmp_path / "test.ini"
    cfg.write_text("""
[DEFAULT]
default_value = from_default
shared_value = default_shared
loglevel = INFO

[test_section]
shared_value = section_override
section_only = test_value
""")

    with mock.patch("sys.argv", ["test_app.py"]):
        app = ALXapp("Test App")
        app.config = ALXapp.read_config(str(cfg))

        obj = type('TestObj', (), {})()
        result = app.parse_config_section(
            obj,
            app.config['test_section'],
            include_defaults=False
        )

        # Should NOT include default_value (only in DEFAULT)
        assert not hasattr(result, 'default_value')

        # shared_value is overridden in test_section, so it SHOULD be included
        assert hasattr(result, 'shared_value')
        assert result.shared_value == 'section_override'

        # Should include section-specific values
        assert result.section_only == 'test_value'

        # Should NOT include values only in DEFAULT
        assert not hasattr(result, 'loglevel')


# Fix test_parse_config_section_type_conversion - add import check
def test_parse_config_section_type_conversion(tmp_path):
    """Test that values are converted to correct types"""
    from collections import OrderedDict  # Add this line

    cfg = tmp_path / "test.ini"
    cfg.write_text("""
[test_section]
boolean_value = True
float_value = 3.14
int_value = 100
json_list = [1, 2, 3, 4]
json_dict = {"key": "value", "number": 123}
json_strings = ["percentage %%", "value1", "value2"]
string_value = hello
""")

    with mock.patch("sys.argv", ["test_app.py"]):
        app = ALXapp("Test App")
        app.config = ALXapp.read_config(str(cfg))

        obj = type('TestObj', (), {})()
        result = app.parse_config_section(
            obj,
            app.config['test_section'],
            include_defaults=False
        )

        # Boolean
        assert isinstance(result.boolean_value, bool)
        assert result.boolean_value is True

        # Float
        assert isinstance(result.float_value, float)
        assert result.float_value == 3.14

        # Integer
        assert isinstance(result.int_value, int)
        assert result.int_value == 100

        # JSON list
        assert isinstance(result.json_list, list)
        assert result.json_list == [1, 2, 3, 4]

        # JSON dict (should be OrderedDict)
        assert isinstance(result.json_dict, OrderedDict)
        assert result.json_dict['key'] == 'value'

        # String
        assert isinstance(result.string_value, str)
        assert result.string_value == 'hello'

        # Interpolation
        assert "percentage %" in result.json_strings


# Fix test_parse_config_section_data_path_expansion
def test_parse_config_section_data_path_expansion(tmp_path):
    """Test that $data is expanded correctly"""
    cfg = tmp_path / "test.ini"
    cfg.write_text("""
[test_section]
path_value = $data/output.txt
""")

    with mock.patch("sys.argv", ["test_app.py"]):
        app = ALXapp("Test App", appname="testapp")
        app.config = ALXapp.read_config(str(cfg))

        obj = type('TestObj', (), {})()
        obj.paths = app.paths

        result = app.parse_config_section(
            obj,
            app.config['test_section'],
            include_defaults=False
        )

        # Check that $data was replaced and path ends correctly
        assert '$data' not in result.path_value
        assert result.path_value.endswith('output.txt')
        # Check that it contains the data directory path
        assert str(app.paths.data) in result.path_value