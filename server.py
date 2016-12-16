import logging
from application import globals

from application.configuration import Config
from application.processmanager import ProcessManager
from application.twitter.listener import TwitterListener
from flask import Flask, render_template, redirect, request, flash

app = Flask(__name__)
app.secret_key = 'social_manager'

globals.init()

configuration = globals.configuration = Config('config.ini')
logging.basicConfig(filename=configuration.log['path'] + configuration.log['name'],
                    level=configuration.log['level'],
                    format="%(asctime)s [%(levelname)-5.5s]  %(message)s")

pm = ProcessManager(configuration.pm_data['data_file'])
logging.info("Configuration loaded, Staring program.")


@app.route('/')
def index():
    """
    Index of all Available Services
    :return:
    """
    return render_template('index.html')


@app.route('/twitter')
def twitter():
    return render_template('twitter/index.html')


##################################################################################
#                          Twitter Listener Area                                 #
##################################################################################


@app.route('/twitter/listener', methods=['GET'])
def twitter_listener_index():
    data = pm.read_json_return_dict()
    return render_template('twitter/listener/index.html', data=data['data'][::-1], last_update=data['last_update'])


@app.route('/twitter/listener/create', methods=['POST'])
def twitter_listener_create():
    """
    Method used to create a new subprocess of a Twitter Listener object
    :return:
    """
    try:
        listener = TwitterListener(request.form['hashtags'].replace(" ", "").split(','),
                                   request.form['consumer_key'],
                                   request.form['secret_key'],
                                   request.form['access_token'],
                                   request.form['secret_access_token'])
        listener.start(pm)
    except:
        flash('Twitter Authentication FAILED! Please try again with new keys.',
              category='danger')
        return redirect('/twitter/listener')

    flash('Process Started!', category='success')
    return redirect('/twitter/listener')


@app.route('/twitter/listener/refresh', methods=['GET'])
def twitter_listener_refresh():
    """
    Refresh the process List
    :return:
    """
    pm.refersh_status()
    flash('List Refreshed!', category='success')
    return redirect('/twitter/listener')


@app.route('/twitter/listener/stop/<pid>', methods=['GET'])
def twitter_listener_stop(pid):
    """
    Stop a specific process
    :param pid:  Process ID
    :return:
    """
    flag, message = pm.stop_process(pid)
    flash(message, category='success' if flag else 'danger')
    return redirect('/twitter/listener/refresh')

if __name__ == '__main__':
    app.run()
