from flask import Flask, render_template
from process_manager.processmanager import ProcessManager
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

pm = ProcessManager(configuration.pm_data['data_file'])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()