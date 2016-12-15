import logging

from application.processmanager import ProcessManager
from configuration import Config
from flask import Flask, render_template

app = Flask(__name__)

configuration = Config('config.ini')

logging.basicConfig(filename=configuration.log['path'] + configuration.log['name'],
                    level=configuration.log['level'],
                    format="%(asctime)s [%(levelname)-5.5s]  %(message)s")

logging.info("Configuration loaded")
configuration.print_configuration()

pm = ProcessManager(configuration.pm_data['data_file'])

'''
USAGE EXAMPLE

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