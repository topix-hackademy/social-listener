import logging, os, sys
from configparser import ConfigParser

class Config(object):

    _instance = None
    pm_data = {}
    log = {}
    mongo = {}

    def __init__(self, path):
        # singleton init
        if not self._instance:
            self._instance = super(Config, self).__init__()
        # load configuration from file
        try:
            parser = ConfigParser()
            parser.read(os.path.expanduser(path))

            self.pm_data['data_file'] = parser.get('pm_data', 'data_file')

            self.log['path'] = parser.get('log', 'path')
            self.log['name'] = parser.get('log', 'name')
            self.log['level'] = parser.get('log', 'level')

            self.mongo['uri'] = parser.get('mongo', 'uri')
            self.mongo['db'] = parser.get('mongo', 'db')
        except Exception, message:
            sys.exit(message.message + "\n" + self.configuration_error_message())

    def print_configuration(self):
        logging.info("""
[pm_data]
data_file = {data_file}

[log]
path = {path}
name = {name}
level = {level}

[mongo]
uri = {uri}
db = {db}
""".format(data_file=self.pm_data['data_file'],
           path=self.log['path'],
           name=self.log['name'],
           level=self.log['level'],
           uri=self.mongo['uri'],
           db=self.mongo['db']))

    def configuration_error_message(self):
        return """
Your configuration file is absent or incorrect.
Please create a config.ini file with the following structure:

[pm_data]
data_file = data_file

[log]
path = path
name = name
level = level

[mongo]
uri = uri
db = db
"""