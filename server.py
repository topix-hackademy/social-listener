import logging
from configuration import Config
from flask import Flask, render_template
from application.mongo import Connection
from application.processmanager import ProcessManager
from application.listener import TwitterInterface

app = Flask(__name__)

configuration = Config('config.ini')

logging.basicConfig(filename=configuration.log['path'] + configuration.log['name'],
                    level=configuration.log['level'],
                    format="%(asctime)s [%(levelname)-5.5s]  %(message)s")

logging.info("Configuration loaded")
configuration.print_configuration()

pm = ProcessManager(configuration.pm_data['data_file'])

Connection.Instance().setup(configuration.mongo['uri'], configuration.mongo['db'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/twitter')
def tw_comu():
    CONSUMER_KEY = "asd"
    SECRET_KEY = "asd"
    ACCESS_TOKEN = "asd"
    SECRET_ACCESS_TOKEN = "asd"

    hashtags = ['#python']

    comu_tw = TwitterInterface(CONSUMER_KEY,
                               SECRET_KEY,
                               ACCESS_TOKEN,
                               SECRET_ACCESS_TOKEN,
                               hashtags)
    comu_tw.start(pm)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
