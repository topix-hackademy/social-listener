import logging, os, sys
from configparser import ConfigParser


class Config(object):

    _instance = None
    log = {}
    mongo = {}
    utils = {}

    def __init__(self, path):
        """
        Config Class Constructor. Used to create the Singleton and to setup the configuration object
        :param path:
        """
        # singleton init
        if not self._instance:
            self._instance = super(Config, self).__init__()
        # load configuration from file
        try:
            parser = ConfigParser()
            parser.read(os.path.expanduser(path))

            self.log['path'] = parser.get('log', 'path')
            self.log['name'] = parser.get('log', 'name')
            self.log['level'] = parser.get('log', 'level')

            self.mongo['uri'] = parser.get('mongo', 'uri')
            self.mongo['db'] = parser.get('mongo', 'db')

            self.utils['date_format'] = parser.get('utils', 'date_format')
        except Exception, message:
            sys.exit(message.message + "\n" + Config.configuration_error_message())

    def print_configuration(self):
        """
        Method used to print the actual configuration
        :return:
        """
        logging.info("""
[log]
path = {path}
name = {name}
level = {level}

[mongo]
uri = {uri}
db = {db}

[utils]
date_format = {date_format}
""".format(path=self.log['path'],
           name=self.log['name'],
           level=self.log['level'],
           uri=self.mongo['uri'],
           db=self.mongo['db'],
           date_format=self.utils['date_format']))

    @classmethod
    def configuration_error_message(cls):
        """
        Configuration Error Message
        :return:
        """
        return """
Your configuration file is absent or incorrect.
Please create a config.ini file with the following structure:

[log]
path = path
name = name
level = level

[mongo]
uri = uri
db = db

[utils]
date_format = %%Y/%%m/%%d-%%H:%%M:%%S
"""
