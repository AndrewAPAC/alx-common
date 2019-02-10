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
        appname = app.appname
        env = app.environment

        dirname = os.path.basename(os.path.dirname(sys.argv[0]))

        if env == 'prod' or env == 'test':
            # put in alx.ini
            if platform.system() == "Windows":
                prefix = "C:\\opt\\local"
            else:
                prefix = "/opt/local"

            self.root = os.path.join(prefix, env, dirname)
            oneup = os.path.abspath(os.path.join(self.root, ".."))
            self.data = os.path.join(oneup, "data", dirname)
            self.scripts = os.path.join()
            self.log = os.path.join(oneup, "log")
        else:
            self.root = os.path.abspath(os.path.dirname(sys.argv[0]))
            self.data = os.path.join(self.root, "data")
            self.log = os.path.join(self.root, "log")
            oneup = os.path.abspath(os.path.join(self.root, ".."))

        self.bin = os.path.join(oneup, "bin")
        self.lib = os.path.join(oneup, "lib", "alx")
        self.logfile = os.path.join(self.log, appname + ".log")
        self.etc = self.root

        if inifile:
            self.config = os.path.join(self.etc, inifile)
        else:
            self.config = os.path.join(self.etc, appname + ".ini")


class ALXApp:
    def __init__(self, description="Unknown App", args=None, appname=None,
                 inifile=None):

        if not appname:
            self.appname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        else:
            self.appname = appname

        parser = argparse.ArgumentParser(description)

        parser.add_argument("-e", "--environment", default='dev',
                            help="Runtime Environment, dev, test or prod")
        if args:
            for a in args:
                parser.add_argument(*a)

        self.logger = None

        self.arguments = parser.parse_args()
        self.environment = self.arguments.environment

        libhome = os.path.dirname(os.path.abspath(__file__))
        self.libconfigfile = os.path.join(libhome, 'alx.ini')
        self.libconfig = self.read_config(self.libconfigfile)

        self.paths = Paths(self, inifile=inifile)
        self.config = self.read_config(self.paths.config)

        if self.config:
            self.parse_config(self, self.config[self.environment])

        libdir = os.path.dirname(__file__)
        self.libconfig = self.read_config(os.path.join(libdir, 'alx.ini'))

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
    def read_config(filename):
        if not os.path.isfile(filename):
            return None

        config = configparser.ConfigParser()
        config.read(filename)

        return config

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

        logger.info("Starting application '{}'".format(self.appname))

    def is_dev(self):
        return self.environment == 'dev'

    def is_test(self):
        return self.environment == 'test'

    def is_prod(self):
        return self.environment == 'prod'

