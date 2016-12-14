from flask import Flask, render_template
from process_manager.processmanager import ProcessManager
from twitter.listener import TwitterInterface
from configuration import Config
import logging

app = Flask(__name__)

configuration = Config('config.ini')

if configuration.log['level'] == 'INFO':
    print 'logging to %s%s' % (configuration.log['path'], configuration.log['name'])

logging.basicConfig(filename=configuration.log['path'] + configuration.log['name'],
                    level=configuration.log['level'],
                    format="%(asctime)s [%(levelname)-5.5s]  %(message)s")

logging.info("Configuration loaded")
configuration.print_configuration()


'''
USAGE EXAMPLE

pm = ProcessManager(configuration.pm_data['data_file'])

CONSUMER_KEY = "consumerKEY"
SECRET_KEY = "secretKEY"
ACCESS_TOKEN = "access_token"
SECRET_ACCESS_TOKEN = "secret_access_token"

hashtags = ['#python']

comu_tw = TwitterInterface(CONSUMER_KEY,
                           SECRET_KEY,
                           ACCESS_TOKEN,
                           SECRET_ACCESS_TOKEN,
                           hashtags
comu_tw.start(pm)


'''


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()