import logging

from application.configuration import Config
from application.listener import TwitterInterface
from application.mongo import Connection
from application.processmanager import ProcessManager
from flask import Flask, render_template, redirect, request,flash

app = Flask(__name__)
app.secret_key = 'social_manager'

configuration = Config('config.ini')
logging.basicConfig(filename=configuration.log['path'] + configuration.log['name'],
                    level=configuration.log['level'],
                    format="%(asctime)s [%(levelname)-5.5s]  %(message)s")

pm = ProcessManager(configuration.pm_data['data_file'])
Connection.Instance().setup(configuration.mongo['uri'], configuration.mongo['db'])
logging.info("Configuration loaded, Staring program.")


@app.route('/')
def index():
    data = pm.read_json_return_dict()
    return render_template('index.html', data=data)


@app.route('/refresh')
def refresh():
    pm.refersh_status()
    flash('List Refreshed!' , category='success')
    return redirect('/')


@app.route('/twitter_listener', methods=['POST'])
def tw_comu():
    twitter_listener = TwitterInterface(request.form['consumer_key'],
                                        request.form['secret_key'],
                                        request.form['access_token'],
                                        request.form['secret_access_token'],
                                        request.form['hashtags'].replace(" ", "").split(','))
    if not twitter_listener.test_auth():
        flash('Twitter Authentication FAILED! Please try again with new keys.',
              category='danger')
        return redirect('/')

    twitter_listener.start(pm)
    flash('Process Started!', category='success')
    return redirect('/')

if __name__ == '__main__':
    app.run()
