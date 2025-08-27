# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# Description:
# Defines the ALXapp class and supporting infrastructure for application
# initialization, configuration, command-line parsing, and logging.

import configparser
import os
import sys
import argparse
from cryptography.fernet import Fernet
import json
import logging
import platform
from logging.handlers import TimedRotatingFileHandler
from collections import OrderedDict


class Paths:
    def __init__(self, appname: str, inifile: str = None) -> None:
        """
        A class to hold the default paths for the application

        If the `data` is needed, it must be created manually to avoid unnecessary
        data directories.

        :param appname: The application name
        :param inifile: If the inifile name is different from the default `app.ini` then it can be set here
        """

        basename = os.path.basename(os.path.dirname(sys.argv[0]))
        dirname = os.path.dirname(sys.argv[0])
        self.root = os.path.abspath(os.path.join(dirname, "..", ".."))
        """The root of the installation, perhaps `/opt/local/env` 
        (where *env* is *prod*, *test* or *dev*). Paths are calculated
         dynamically, based on file location"""
        self.bin = os.path.join(self.root, "bin")
        """The location of the start script: `root/bin`"""
        self.data = os.path.join(self.root, "data", basename)
        """The location of the application data: `root/data/app`"""
        self.etc = os.path.join(self.root, 'etc')
        """The location of the configuration files: `root/etc`"""
        self.log = os.path.join(self.root, "log", basename)
        """The location of the log files: `root/log/app`"""
        self.logfile = os.path.join(self.log, appname + ".log")
        """The log filename: `root/log/app/app.log`"""
        self.scripts = os.path.join(self.root, "scripts")
        """The location of the scripts: `root/scripts`"""
        self.top = os.path.join(self.root, "scripts", basename)
        """The location of the application scripts: `root/scripts/app`"""
        self.module_config_dir = self.get_module_config_dir()
        """The location of the module ini, key and env files"""
        self.keyfile = os.path.join(self.module_config_dir, "key")
        """The file from where to obtain the key: `~/.config/alx/key` or
        `%APPDATA%\\alx\\key` on Windows"""
        self.local_env = os.path.join(self.module_config_dir, "env")
        """The path to the venv in use: `~/.config/alx/env`"""
        self.local_config = os.path.join(self.module_config_dir, "alx.ini")
        """The path to the local configuration: `~/.config/alx/alx.ini`"""
        self.global_config = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "alx.ini")
        """The path to the module configuration: `<venv>/lib/.../site-packages/alx/alx.ini`"""

        self.config = os.path.join(self.etc, appname + ".ini")
        """The name of the config file determined from `self.etc`/app"""
        if inifile:
            self.config = os.path.join(self.etc, inifile)

    @staticmethod
    def get_module_config_dir():
        if platform.system() == "Windows":
            return os.path.join(os.environ['APPDATA'], "alx")
        else:
            return os.path.join(os.path.expanduser("~"), ".config", "alx")

    def __str__(self) -> str:
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items() if isinstance(v, str))


class ALXapp:
    logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])
    """The default logger used by all applications using `ALXapp`"""
    def __init__(self, description: str = "Unknown App",
                 args: list = None, appname: str = None,
                 inifile: str = None, epilog: str = None):
        """
        Initialise the `ALXapp` object which does a number of things:
        * Creates the application name from `sys.argv[0]` and stores it in
        `name` if not passed as a parameter
        * Adds a `--env` / `-e` argument and sets `self.environment`
        * Initialises the `Paths` class.
        * Reads the arguments provided in the `args` parameter.
        * Reads and parses the configuration file and stores the values in the ALXAppp object
        * Reads and parses the library configuration stored in `alx.ini`
        * Initialises and starts logging to `Paths.logfile`

        An example `alx.ini` or `$HOME/config/alx/alx.ini` or
        `%APPDATA%\alx` on Windows
        ```
        [DEFAULT]

        [logging]
        format:     %%(asctime)s: %%(levelname)s %%(module)s.%%(funcName)s:%%(lineno)d [%%(threadName)s] %%(message)s
        loglevel:   INFO
        days:       7
        maxsize:    10485760
        when:       midnight

        [mail]
        server:     mailhost
        from:       Super User <root@localhost>


        [html]
        css:
                p, h1, h2, h3, h4, h5, ul, ol, li {
                    font-family: Calibri, Arial, Helvetica
                }
                table {
                  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                  border-collapse: collapse;
                  width: 100%%;
                }
                td, th {
                  border: 1px solid #ddd;
                  padding: 5px;
                }
                tr:nth-child(even){background-color: #f2f2f2;}
                tr:hover {background-color: #ddd;}
                th {
                  padding-top: 8px;
                  padding-bottom: 8px;
                  text-align: left;
                  background-color: #0771af;
                  color: white;
                }
        ```
        :param description: A short description for the app - used with `--help`
        :param args: A list of arguments added with argparse.ArgumentParser.add_argument.  Example
        ```
        args = [
            ["-d", "--date", {"help": "store as '%%Y-%%m-%%d' date in database"}],
            ["-s", "--start", {"default": None, "type": str,
                               "help": "The first date from which to retrieve prices"}],
            ["-g", "--gui", {"action": "store_true", "default": False,
                             "help": "Display the browser."}]
        ]
        ```
        but you can just use this trimmed down version to store the
        arguments as strings
        ```
        args = [
            ["--date"],
            ["--start"],
         ]
        ```
        :param appname: The name of the application.  Default is the
         name of argv[0]
        :param inifile: The name of the configuration file.  Default
         is to create it from appname
        :param epilog: The text to use at the end of the help
         message when the app is called with `--help`
        """

        self.name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        """The name of the application from the parameter or calculated from `sys.argv`"""
        if appname:
            self.name = appname

        parser = argparse.ArgumentParser(description=description,
                                         epilog=epilog,
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument("-e", "--env", default='dev',
                            help="Runtime Environment, dev, test or prod")

        if args:
            for a in args:
                if type(a[-1]) is dict:
                    arg = a[:-1]
                    kwargs = a[-1]
                    parser.add_argument(*arg, **kwargs)
                else:
                    parser.add_argument(*a)

        self.arguments = parser.parse_args()
        """A namespace of the arguments as parsed by 
        `argparse.Arguments.parse_args`"""
        self.environment = 'dev'
        """The execution environment - default is `dev` but any of 
        * test || uat || tst: **test**
        * prod || production || prd: **production**
        
        can be used to set *prod* or *test*
        """
        if self.arguments.env in ('test', 'uat', 'tst'):
            self.environment = 'test'
        elif self.arguments.env in ('prd', 'prod', 'production'):
            self.environment = 'prod'

        self.paths = Paths(self.name, inifile)
        """The `Paths` namespace that holds path information"""

        self.config = self.read_config(self.paths.config)
        """The application configuration read from `Paths.config` from a 
        call to `ALXApp.read_config`. The configuration values are assigned
        to the `ALXApp` class with a call to `ALXApp.parse_config`"""
        if self.config and self.environment in self.config:
            self.parse_config(self, self.config[self.environment])

        self.key = None
        """The key to encrypt and decrypt encoded strings"""

        self.libconfig = self.read_lib_config()
        """The global library configuration from `alx.ini`"""

        # Start logging with all configured parameters
        self.start_logging()

    @staticmethod
    def parse_config(obj: object, config: configparser.SectionProxy):
        """
        Parses the `config` and stores in `obj` as the appropriate type.
        It works out if it is a boolean, float, integer or string. If
        the configuration value starts with a `[` or `{` then it is
        loaded using `json.loads` and stored in an `OrderedDict`

        The config file should be structured so there are sections named
        * `[DEFAULT]`
        * `[dev]`
        * `[test]`
        * `[prod]`
        This allows settings to be overridden simply by specifying
        `-e env`. If a setting is not specified in an environment
        section, then the value from `[DEFAULT]` is used. For example
        ```
        [DEFAULT]
        loglevel:   INFO

        [dev]
        loglevel:   DEBUG

        [test]
        loglevel:   INFO

        [prod]
        loglevel:   WARN
        ```
        All the config file elements are stored in the `ALXapp` object.
        If you define:
        ```
        foo: bar
        bar: 1
        baz: [1, 2, 3, 4]
        ```
        in the ini file, then your `ALXapp` object, say `app`, will have
        these elements defined (either from the `[DEFAULT]` section or the
        appropriate environment:
        ```
        app.foo = "bar"
        app.bar = 1
        app.baz = [1, 2, 3, 4]
        ```
        Additionally, if you specify `$data` in the value, it will be
        expanded to the data directory of the application.  For example
        ```
        output_file = $data/output.txt
        ```
        will result in:
        ```
        app.output_file = /opt/local/prod/data/app/output.txt
        ```

        :param obj: The object in which to store the configuration
         values (usually `self`)
        :param config: The `configparser` object.  It can be a section
        like `config[app.environment]`
        """

        try:
            for item in config:
                # Add all the config values as string values in the app
                value = config.get(item)
                if '$data' in value:
                    if hasattr(obj, 'paths'):
                        value = value.replace('$data', obj.paths.data)
                        setattr(obj, item, value)
                    else:
                        continue
                elif value in ('True', 'False', 'true', 'false'):
                    # Convert to boolean
                    setattr(obj, item, config.getboolean(item))
                else:
                    try:
                        # Is it an integer?
                        i = int(value)
                        setattr(obj, item, i)
                    except (ValueError, TypeError):
                        try:
                            # or a float?
                            f = float(value)
                            setattr(obj, item, f)
                        except (ValueError, TypeError):
                            # Only a string left....
                            if value.startswith('[') or value.startswith('{'):
                                try:
                                    setattr(obj, item, json.loads(
                                        value, object_pairs_hook=OrderedDict))  # type: ignore[arg-type]
                                except json.JSONDecodeError:
                                    setattr(obj, item, value)
                            else:
                                setattr(obj, item, value)
        except Exception:
            raise

    @staticmethod
    def read_config(filename: str, filename2: str = None):
        """
        Reads the configuration file in `filename` using the parser
        passed in `parser` which is typically the default

        :param filename: Name of the configuration file to read
        :param filename2: Name of a second config file to override first
        :return: The `configparser.ConfigParser` configuration
        """
        if not os.path.isfile(filename):
            return None

        config = configparser.ConfigParser()
        if filename2:
            config.read([filename, filename2])
        else:
            config.read(filename)

        return config

    def _create_configuration_files(self) -> None:
        """
        Create some initial configuration files

        :return: None
        """
        os.makedirs(self.paths.module_config_dir, exist_ok=True)

        if not os.path.isfile(self.paths.local_config):
            print("*** NOTE: Creating user config file '{}'".format(self.paths.local_config))
            gc = ALXapp.read_config(self.paths.global_config)
            with open(self.paths.local_config, 'w') as f:
                for s in gc.sections():
                    f.write("[%s]\n\n" % s)

        if not os.path.isfile(self.paths.keyfile):
            print("*** NOTE: Creating key file '{}'".format(self.paths.keyfile))
            # Create an initial fernet key.  User to adjust as required
            with open(self.paths.keyfile, 'w') as f:
                f.write("%s\n" % Fernet.generate_key().decode())
            # Ensure strict permissions
            os.chmod(self.paths.keyfile, 0o600)

        if not os.path.isfile(self.paths.local_env):
            print("*** NOTE: Creating local environment file: '{}'".format(self.paths.local_env))
            # Assume that the current python invocation is the path to the virtual env
            with open(self.paths.local_env, 'w') as f:
                venv = os.path.dirname(os.path.dirname(sys.executable))
                f.write("venv=%s\n" % venv)

    def read_lib_config(self) -> configparser.ConfigParser:
        """
        Reads and parses the module configuration file and the local
        configuration file (`~/.config/alx/alx.ini` or
        `%APPDATA%/alx/alx.ini`). The local configuration overrides
        any values in the module configuration file.

        On first invocation, the user files are checked and created if
        they don't exist.

        :return: The `configparser.ConfigParser` configuration
        """
        if not hasattr(self, 'paths'):
            self.paths = Paths("alx-common")

        # If the user configuration doesn't exist, create them
        if not all([
            os.path.isdir(self.paths.module_config_dir),
            os.path.isfile(self.paths.local_config),
            os.path.isfile(self.paths.keyfile),
            os.path.isfile(self.paths.local_env),]):
            self._create_configuration_files()

        merged_config = ALXapp.read_config(self.paths.global_config,
                                           self.paths.local_config)

        return merged_config

    def start_logging(self):
        """
        Sets up a standard logger using the configuration in `alx.ini`
        By default, log files are rolled at midnight and kept for the
        number of days configured in `alx.ini`.  The loglevel and
        format are also set in the config file.

        If the application is in development mode, a console logger
        is also added for convenience
        """
        days = self.libconfig.getint('logging', 'days')
        log_format = self.libconfig.get('logging', 'format')
        when = self.libconfig.get('logging', 'when')

        if hasattr(self, 'loglevel'):
            loglevel = self.loglevel
        else:
            loglevel = self.libconfig.get('logging', 'loglevel')

        self.logger.setLevel(loglevel)

        if not os.path.isdir(self.paths.log):
            os.makedirs(self.paths.log)

        fh = TimedRotatingFileHandler(self.paths.logfile, when=when,
                                      backupCount=days)
        formatter = logging.Formatter(log_format)
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        if self.is_dev():
            # Also log to console...
            ch = logging.StreamHandler()
            ch.setLevel(loglevel)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        self.logger.debug("Starting application '%s', logging at level '%s'",
                          format(self.name), format(loglevel))

    def set_log_level(self, level: str) -> None:
        """
        Change the logging level at runtime

        :param level: Log level string ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        """
        self.logger.setLevel(level)
        # Update all handlers to the new level
        for handler in self.logger.handlers:
            handler.setLevel(level)

        self.logger.info(f"Log level changed to {level}")

    def _read_key(self) -> Fernet:
        """Reads the key from `~/.config/alx/key` and uses it to encrypt and
         decrypt strings using the `cryptography` python module"""

        if not os.path.exists(self.paths.keyfile):
            self.logger.error("Could not open %s", self.keyfile)
            sys.exit(1)
        st = os.stat(self.paths.keyfile)
        if platform.system() != 'Windows' and int(oct(st.st_mode)[3:]) > 600:
            # Apologies to Windows users but your security is too messy
            self.logger.error("Check permissions on %s.  Too open", self.keyfile)
            sys.exit(1)

        with open(self.paths.keyfile) as k:
            key = k.read().strip()

        fernet = Fernet(key)

        return fernet

    def encrypt(self, string: str) -> str:
        """
        Encrypts the password using the key read from `~/.config/alx/key`. This
        function provides an easy way to avoid storing plain text passwords

        The keyfile needs to have permission `0600` and look something like
        ```
        P9H7kabcdefghijwlSrfVnKKqV5VCnW5RE8OT21eH5k=
        ```
        Please refer to `decrypt` for how to create a key.

        Note that due to the inconsistent implementation of permissions
        on Windows, this check is ignored

        :param string: The string to encrypt.
        :return: The encrypted string
        """
        if not self.key:
            self.key = self._read_key()
        encoded = self.key.encrypt(string.encode())
        return encoded.decode()

    def decrypt(self, string: str) -> str:
        """
        Decrypts the password using the key read from `~/.config/alx/key`. This
        function provides an easy way to avoid storing plain text passwords

        Your code will then look like:
        ```
        self.passwd = app.decrypt(app.config.get('mysql', 'password'))
        self.user = app.decrypt(app.config.get('mysql', 'user'))
        ```
        To generate a key, use this one-liner and place the ouput in `~/.config/alx/key`:
        ```
        python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
        ```

        If there are different users of an application using `ALXapp` then
        the key must be consistent or the string will fail to decrypt.

        :param string: The string to decrypt.
        :return: The decrypted string
        """
        if not self.key:
            self.key = self._read_key()
        decoded = self.key.decrypt(string.encode()).decode()
        return decoded

    def is_dev(self) -> bool:
        """
        :return: `True` if running in dev mode and `False` otherwise
        """
        return self.environment == 'dev'

    def is_test(self) -> bool:
        """
        :return: `True` if running in test mode and `False` otherwise
        """
        return self.environment == 'test'

    def is_prod(self) -> bool:
        """
        :return: `True` if running in prod mode and `False` otherwise
        """
        return self.environment == 'prod'
