import abc
import argparse
import dotmap
import logging
import yaml
import sys

from . import colour as c
from . import exceptions
from . import logger
from . import configuration

log = logger.setup_log('root', timefmt='%H:%M:%S')


class Scala(metaclass=abc.ABCMeta):
    """
        Scala: Simple Console Application with Logging and Argparse
    """
    _app_name = "Default Scala"
    _description = "Simple Configurable Application with Logging and Argparse"
    _prog = "Scala"
    _success_message = f"{c.script(_prog)} finished successfully"

    def __init__(self, **kwargs):
        """ Optionally override the application name and description """
        self._ok = True
        self._description = kwargs.get('description', self._description)
        self._app_name = kwargs.get('app_name', self._app_name)
        self._prog = kwargs.get('app_name', self._prog)
        self._success_message = kwargs.get('success_message', self._success_message)

        self._argparser = None

    def _initialize(self):
        self._argparser = argparse.ArgumentParser(
            prog=self._prog,
            description=self._description
        )
        self._add_default_arguments()
        self.add_arguments()
        self.args = self._argparser.parse_args()

        self._configure()

    def add_argument(self, *args, **kwargs):
        """ Just a public wrapper so that we do not have to access _argparser directly """
        self._argparser.add_argument(*args, **kwargs)

    @abc.abstractmethod
    def add_arguments(self):
        """ Override this in your Scala derivative to add custom arguments """

    def _add_default_arguments(self):
        """ Add default arguments that are present in every instance of Scala """
        self.add_argument('-l', '--logfile', type=argparse.FileType('w'), help="Write log to file")
        self.add_argument('-d', '--debug', action='store_true', help="Turn on verbose logging")

    @abc.abstractmethod
    def main(self):
        """
        The main entry point of the program.
        Provide an implementation in your derivative of Scala.
        """

    def _configure(self):
        pass

    def _override_configuration(self):
        log.setLevel(logging.DEBUG if self.args.debug else logging.INFO)

        if self.args.logfile:
            log.addHandler(logging.FileHandler(self.args.logfile.name))
            log.debug(f"Added log output {c.path(self.args.logfile.name)}")

    def run(self):
        try:
            self._initialize()
            self.main()
            self._finalize()
        except exceptions.PrerequisiteError as e:
            log.error(f"Terminating due to missing prerequisites: {e}")
        except exceptions.ConfigurationError as e:
            log.error(f"Terminating due to a configuration error: {e}")
        finally:
            if self._ok:
                log.info(self._success_message)
            else:
                log.critical(f"{c.script(self._app_name)} aborted during runtime")

    def _finalize(self):
        self._ok = True
