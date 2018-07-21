"""
Secrets Manager

Read secrets from secrets file, overriding with environment variable if set
"""

import os
from configparser import ConfigParser


class SecretNotFoundException(Exception):
    """
    Thrown when secret does not exist in environment variables or secrets file
    """
    def __init__(self, env_var_name):
        message = 'Secret not found in environment variables or secrets file: {}'.format(env_var_name)
        super(SecretNotFoundException, self).__init__(message)


class Secrets(object):
    """
    Secrets Manager
    """
    DEFAULT_FILENAME = '~/.secrets'

    def __init__(self, filename: str = None):
        filename = os.path.expanduser(filename or self.DEFAULT_FILENAME)
        self.config = ConfigParser()
        self.config.read(filename)

    def get(self, section: str, parameter: str, raise_on_not_found: bool = True, default=None):
        """
        Get secret value

        :param section: as str
        :param parameter: as str
        :param raise_on_not_found: optional (default = True)
        :param default: optional (default = None)
        :return:
        """
        env_var_name = '{}_{}'.format(section, parameter)
        if env_var_name in os.environ:
            return os.environ.get(env_var_name)
        if self.config.has_option(section, parameter):
            return self.config.get(section, parameter)
        if default is None and raise_on_not_found:
            raise SecretNotFoundException(env_var_name)
        return default
