""" get database connection info """

from logging import Logger
from typing import Dict

from configparser import ConfigParser

from iautil.log import configure_logging, trace # mypy: disable=import-untyped


logger:Logger = configure_logging(__name__)


class ConfigFileError(Exception):
    """ missing section """

@trace(logger)
def config(filename:str='etc/database.ini', section:str='postgresql')->Dict[str,str]:
    """ parse the config file """
    parser:ConfigParser = ConfigParser()            # create a parser
    parser.read(filename)              # read config file

    if not parser.has_section(section):
        raise ConfigFileError(
            f'Section {section} not found in the {filename} file')

    db:Dict[str,str] = {}                            # get section, default to postgresql
    params = parser.items(section)
    for param in params:
        db[param[0]] = param[1]

    return db
