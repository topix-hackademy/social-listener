import logging
from application import globals

from application.configuration import Config
from application.listener import TwitterInterface
from application.processmanager import ProcessManager
from flask import Flask, render_template, redirect, request,flash

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
    Index of the website with json process list and last update info
    :return:
    """
    data = pm.read_json_return_dict()
    return render_template('index.html', data=data['data'][::-1], last_update=data['last_update'])


@app.route('/refresh')
def refresh():
    """
    Refresh the process List
    :return:
    """
    pm.refersh_status()
    flash('List Refreshed!', category='success')
    return redirect('/')

@app.route('/stop/<pid>')
def stop(pid):
    """
    Stop a specific process
    :param pid:  Process ID
    :return:
    """
    flag, message = pm.stop_process(pid)
    flash(message, category='success' if flag else 'danger')
    return redirect('/refresh')


@app.route('/twitter_listener', methods=['POST'])
def twitter_listener():
    """
    Method used to create a new subprocess of a Twitter Listener object
    :return:
    """
    listener = TwitterInterface(request.form['consumer_key'],
                                request.form['secret_key'],
                                request.form['access_token'],
                                request.form['secret_access_token'],
                                request.form['hashtags'].replace(" ", "").split(','))
    if not listener.test_auth():
        flash('Twitter Authentication FAILED! Please try again with new keys.',
              category='danger')
        return redirect('/')

    listener.start(pm)
    flash('Process Started!', category='success')
    return redirect('/')

if __name__ == '__main__':
    app.run()
