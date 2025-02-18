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
    def __init__(self, _app: str, inifile: str = None):
        """
        A class to hold the default paths for the application

        If the `data` or `log` directory does not exist, it will be created even if not used.

        :param _app: The ALXApp objet
        :param inifile: If the inifile name is not the same as the default `app.ini` then it can be set here
        """
        appname = _app.name
        env = _app.environment
        """The execution environment: `prod`, `test` or `dev` (default)"""
        basename = os.path.basename(os.path.dirname(sys.argv[0]))
        dirname = os.path.dirname(sys.argv[0])
        self.root = os.path.abspath(os.path.join(dirname, "..", ".."))
        """The root of the installation, typically `/opt/local/env` (where *env* is *prod*, *test* or *dev*) """
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

        if not os.path.isdir(self.data):
            os.makedirs(self.data)
        if not os.path.isdir(self.log):
            os.makedirs(self.log)

        self.config = os.path.join(self.etc, appname + ".ini")
        """The name of the config file determined from `self.etc`/app"""
        if inifile:
            self.config = os.path.join(self.etc, inifile)


class ALXapp:
    logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])

    def __init__(self, description: str = "Unknown App",
                 args: list = None, appname: str = None,
                 inifile: str = None, epilog: str = None):
        """
        Initialise the `ALXapp` object which does a number of things:
        * Creates the application name from `sys.argv[0]` and stores it in `ALXApp.name` if not passed as a parameter
        * Adds a `--env` / `-e` argument and sets `self.environment`
        * Initialises the `Paths` class.
        * Reads the arguments provided in the `args` parameter.
        * Reads and parses the configuration file and stores the values in the ALXAppp object
        * Reads and parses the library configuration stored in `alx.ini`
        * Initialises and starts logging to `Paths.logfile`

        An example `alx.ini`
        ```
        [DEFAULT]
        root:       /opt/local

        [logging]
        format:     %%(asctime)s: %%(levelname)s %%(module)s.%%(funcName)s:%%(lineno)d [%%(threadName)s] %%(message)s
        loglevel:   INFO
        days:       7
        maxsize:    10485760
        when:       midnight

        [mail]
        server:     localhost
        from:       Andrew Lister <a.lister.hk@gmail.com>


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

        self.paths = Paths(self, inifile=inifile)
        """The `Paths` namespace that holds path information"""
        self.config = self.read_config(self.paths.config)
        """The application configuration read from `Paths.config` from a 
        call to `ALXApp.read_config`. The configuration values are assigned
        to the `ALXApp` class with a call to `ALXApp.parse_config`"""
        if self.config and self.environment in self.config:
            self.parse_config(self, self.config[self.environment])

        self.libconfig = self.read_lib_config()
        """The global library configuration from `alx.ini`"""

        self.start_logging()

        self.key = None
        """The key to encrypt and decrypt data, stored in `~/.key.username`"""

    @staticmethod
    def parse_config(obj: object, config: configparser.ConfigParser):
        """
        Parses the `config` and stores in `obj` as the appropriate type.
        It works out if it is a boolean, float, integer or string. If
        the configuration value starts with a `[` or `{` then it is
        loaded using `json.loads` and stores in an `OrderredDict`

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
                            if (value.startswith('[') or
                                    value.startswith('{')):
                                od = OrderedDict
                                setattr(obj, item,
                                        json.loads(
                                            value, object_pairs_hook=od))
                            else:
                                setattr(obj, item, value)
        except Exception:
            raise

    @staticmethod
    def read_config(filename: str) -> configparser.ConfigParser:
        """
        Reads the configuration file in `filename` using the parser
        passed in `parser` which is typically the default

        :param filename: Name of the configuration file to read
        :return: The `configparser.ConfigParser` configuration
        """
        if not os.path.isfile(filename):
            return None

        config = configparser.ConfigParser()
        config.read(filename)

        return config

    @staticmethod
    def read_lib_config() -> configparser.ConfigParser:
        """
        Reads the global `alx.ini` file using ALXApp.read_config

        :return: The configuration
        """
        libhome = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(libhome, 'alx.ini')
        return ALXapp.read_config(filename)

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
        logformat = self.libconfig.get('logging', 'format')
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
        formatter = logging.Formatter(logformat)
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        if self.is_dev():
            # Also log to console...
            ch = logging.StreamHandler()
            ch.setLevel(loglevel)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        self.logger.debug("Starting application '{}'".format(self.name))

    def _read_key(self) -> str:
        """Reads the key from `~/.key.user` and uses it to encrypt and
         decrypt strings using the `cryptography` python module"""

        keyfile = os.path.join(os.path.expanduser('~'), '.key.' +
                               os.getlogin())
        if not os.path.exists(keyfile):
            self.logger.error("Could not open %s", keyfile)
            sys.exit(1)
        st = os.stat(keyfile)
        if platform.system() != 'Windows' and int(oct(st.st_mode)[3:]) > 600:
            self.logger.error("Check permissions on %s.  Too open", keyfile)
            sys.exit(1)

        with open(keyfile) as k:
            key = k.read().strip()

        fernet = Fernet(key)

        return fernet

    def encrypt(self, string: str) -> str:
        """
        Encrypts the password using the key read from `~/.key.username`

        :param string: The string to encrypt.
        :return: the encrypted string
        """
        if not self.key:
            self.key = self._read_key()
        encoded = self.key.encrypt(string.encode())
        return encoded.decode()

    def decrypt(self, string: str) -> str:
        """
        Decrypts the password using the key read from `~/.key.username`

        :param string: The string to decrypt.
        :return: the decrypted string
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


if __name__ == "__main__":
    args = [
        ["-d", "--date", {"help": "store as '%%Y-%%m-%%d' date in database"}],
        ["-s", "--start", {"default": None, "type": str,
                           "help": "The first date from which to retrieve prices"}],
        ["-g", "--gui", {"action": "store_true", "default": False,
                         "help": "Display the browser."}]
    ]

    app = ALXApp("test application", args=args, appname="account_info")
    mail = ALXmail()


