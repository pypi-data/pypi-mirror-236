import argparse
import dotmap
import logging
import sys

import schema

from . import scala
from . import exceptions
from . import configuration
from . import colour as c


log = logging.getLogger("root")


class Scalyca(scala.Scala):
    """
        Simple Console Application with Logging, Yaml Configuration and Argparse
    """
    _app_name = 'Scalyca'
    _description = "Simple Configurable Application with Logging, Yaml file Configuration and Argparse"
    # Config validation schema, or None to skip validation
    _prog = "Scalyca"
    schema = None

    def _add_default_arguments(self):
        """ Scalyca adds one mandatory argument: the path to the config file """
        super()._add_default_arguments()
        self.add_argument('config', type=argparse.FileType('r'), help="main configuration file")

    def _configure(self):
        try:
            self._load_configuration()
            self._override_configuration()
            self._lock_configuration()
            self._debug_configuration()
            self._validate_configuration()

        except exceptions.FatalError:
            log.critical(f"{c.script(self.app_name)} aborting during configuration")
            sys.exit(-1)

    def _load_configuration(self):
        raw = configuration.load_YAML(self.args.config)
        self.config = dotmap.DotMap(raw, _dynamic=True)
        log.info(f"Configuration read from {c.path(self.args.config.name)}")

    def _lock_configuration(self):
        log.debug(f"Locking the configuration")
        configuration.make_static(self.config)

    def override_with_warning(self, parameter, new_value, name):
        log.warning(f"Overriding {c.param(name)} ({c.over(parameter)} -> {c.over(new_value)})")
        self.config[name] = new_value

    def _debug_configuration(self):
        if self.args.debug:
            log.debug("Full config is")
            self.config.pprint()

    def _validate_configuration(self):
        if self.schema is None:
            log.debug("No config validation schema provided, skipping validation")
        else:
            try:
                self.schema.validate(self.config)
            except schema.SchemaError as e:
                raise exceptions.ConfigurationError(e) from e
