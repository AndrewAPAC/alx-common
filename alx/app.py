import configparser
import os
import sys
import argparse
import platform
import logging
from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])

class Paths:
    def __init__(self, app, inifile=None):
        """
        A class to hold the default paths for the application

        /opt/local/env
            - bin
            - data/app
            - lib
            - log
            - scripts/app

        :param app: The ALXApp objet
        :param inifile: If the inifile name is not the same as the
        """
        appname = app.name
        env = app.environment

        basename = os.path.basename(os.path.dirname(sys.argv[0]))
        dirname = os.path.dirname(sys.argv[0])
        self.root = os.path.abspath(os.path.join(dirname, "..", ".."))

        self.data = os.path.join(self.root, "data", basename)
        self.log = os.path.join(self.root, "log", basename)
        self.top = os.path.join(self.root, "scripts", basename)
        self.bin = os.path.join(self.root, "bin")
        self.scripts = os.path.join(self.root, "scripts")
        self.logfile = os.path.join(self.log, appname + ".log")
        self.etc = os.path.join(self.root, 'etc')

        if inifile:
            self.config = os.path.join(self.etc, inifile)
        else:
            self.config = os.path.join(self.etc, appname + ".ini")


class ALXApp:
    def __init__(self, description="Unknown App", args=None, appname=None,
                 inifile=None, mylogger=None, logging=True,
                 myparser=None, epilog=None,
                 formatter=None):

        if not appname:
            self.name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        else:
            self.name = appname

        parser = argparse.ArgumentParser(description=description,
                                         epilog=epilog)

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

        if self.arguments.env in ('test', 'uat', 'tst'):
            self.environment = 'test'
        elif self.arguments.env in ('prd', 'prod', 'production'):
            self.environment = 'prod'
        else:
            self.environment = 'dev'

        self.paths = Paths(self, inifile=inifile)
        self.config = self.read_config(self.paths.config, myparser)

        if self.config and self.environment in self.config:
            self.parse_config(self, self.config[self.environment])

        self.libconfig = self.read_lib_config()

        if mylogger:
            self.logger = mylogger

        if logging:
            self.start_logging()

    def parse_config(self, obj, config):
        try:
            for item in config:
                # Add all the config values as string values in the app
                value = config.get(item)
                setattr(obj, item, config.get(item))
        except:
            raise

    @staticmethod
    def read_config(filename, parser=None):
        if not os.path.isfile(filename):
            return None

        if not parser:
            config = configparser.ConfigParser()
        else:
            config = parser

        config.read(filename)

        return config

    @staticmethod
    def read_lib_config():
        libhome = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(libhome, 'alx.ini')
        return ALXApp.read_config(filename)

    def start_logging(self):
        days = self.libconfig.getint('logging', 'days')
        logformat = self.libconfig.get('logging', 'format')
        when = self.libconfig.get('logging', 'when')

        if hasattr(self, 'loglevel'):
            loglevel = self.loglevel
        else:
            loglevel = self.libconfig.get('logging', 'loglevel')

        logger.setLevel(loglevel)

        if not os.path.isdir(self.paths.log):
            os.makedirs(self.paths.log)

        fh = TimedRotatingFileHandler(self.paths.logfile, when=when,
                                      backupCount=days)
        formatter = logging.Formatter(logformat)
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        if self.is_dev():
            # Also log to console...
            ch = logging.StreamHandler()
            ch.setLevel(loglevel)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        logger.debug("Starting application '{}'".format(self.name))

    def is_dev(self):
        return self.environment == 'dev'

    def is_test(self):
        return self.environment == 'test'

    def is_prod(self):
        return self.environment == 'prod'
