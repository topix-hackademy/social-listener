import logging

from application.configuration import Config
from application.processmanager import ProcessManager
from application.twitter.listener.listener import TwitterListener
from application.twitter.tweets.collector import TweetCollector
from application.twitter.follower.collector import FollowerCollector
from application.twitter.friends.collector import FriendsCollector
from application.twitter.api.api import TwitterAPI
from application.utils import globals
from flask import Flask, render_template, redirect, request, flash

import re
twitter_regex = re.compile(r'twitter_*')
facebook_regex = re.compile(r'facebook_*')

app = Flask(__name__)
app.secret_key = 'social_manager'

globals.init()

configuration = globals.configuration = Config('config.ini')
logging.basicConfig(filename=configuration.log['path'] + configuration.log['name'],
                    level=configuration.log['level'],
                    format="%(asctime)s [%(levelname)-5.5s]  %(message)s")

pm = ProcessManager()
logging.info("Configuration loaded, Staring program.")


@app.route('/')
def index():
    """
    Index of all Available Services
    :return:
    """
    return render_template('index.html')


##################################################################################
#                              Twitter Area                                      #
##################################################################################


@app.route('/twitter')
def twitter():
    return render_template('twitter/index.html',
                           data=pm.get_all_processes_with_condition({'ptype': twitter_regex}))


@app.route('/twitter/refresh', methods=['GET'])
def twitter_refresh():
    """
    Refresh the process List
    :return:
    """
    pm.refresh_status()
    flash('List Refreshed!', category='success')
    return redirect('/twitter')


@app.route('/twitter/stop/<pid>', methods=['GET'])
def twitter_stop(pid):
    """
    Stop a specific process
    :param pid:  Process ID
    :return:
    """
    flag, message = pm.stop_process(pid)
    flash(message, category='success' if flag else 'danger')
    return redirect('/twitter/refresh')


##################################################################################
#                        Twitter Listener Area                                   #
##################################################################################


@app.route('/twitter/listener', methods=['GET'])
def twitter_listener_index():
    return render_template('twitter/listener/index.html')


@app.route('/twitter/listener/create', methods=['POST'])
def twitter_listener_create():
    """
    Method used to create a new subprocess of a Twitter Listener object
    :return:
    """
    if not request.form['keywords'].replace(" ", "") and not request.form['username'].replace(" ", ""):
        flash('Please insert at least a keywords or an username.',
              category='danger')
        return redirect('/twitter/listener')

    try:
        listener = TwitterListener(request.form['keywords'].replace(" ", "").split(','),
                                   request.form['username'],
                                   request.form['consumer_key'],
                                   request.form['secret_key'],
                                   request.form['access_token'],
                                   request.form['secret_access_token'])
        listener.start(pm)
    except Exception as e:
        flash(e.message, category='danger')
        return redirect('/twitter/listener')

    flash('Process Started!', category='success')
    return redirect('/twitter')


@app.route('/api/v1/twitter/keywords', methods=['GET'])
def api_get_keywords():
    return TwitterAPI.get_keywords()


@app.route('/api/v1/twitter/search/<keyword>', methods=['GET'])
def api_search(keyword):
    return TwitterAPI.search(keyword)


@app.route('/api/v1/twitter/search/<keyword>/<page>', methods=['GET'])
def api_search_paginated(keyword, page):
    return TwitterAPI.search(keyword, page)


##################################################################################
#                        Twitter Collector Area                                  #
##################################################################################


@app.route('/twitter/collector', methods=['GET'])
def twitter_collector_index():
    """
    Twitter collector index page
    :return:
    """
    return render_template('twitter/collector/index.html')


@app.route('/twitter/collector/create', methods=['POST'])
def twitter_collector_create():
    """
    Method used to create a new subprocess of a Twitter Collector object
    :return:
    """
    try:
        collector = TweetCollector(request.form['user'],
                                   request.form['consumer_key'],
                                   request.form['secret_key'],
                                   request.form['access_token'],
                                   request.form['secret_access_token'])
        collector.start(pm)
    except Exception as e:
        flash(e.message, category='danger')
        return redirect('/twitter/collector')

    flash('Process Started!', category='success')
    return redirect('/twitter')


##################################################################################
#                        Follower Collector Area                                 #
##################################################################################


@app.route('/twitter/follower', methods=['GET'])
def twitter_follower_index():
    """
    Twitter collector index page
    :return:
    """
    return render_template('twitter/follower/index.html')


@app.route('/twitter/follower/create', methods=['POST'])
def twitter_follower_create():
    """
    Method used to create a new subprocess of a Follower Collector object
    :return:
    """
    try:
        collector = FollowerCollector(request.form['user'],
                                      request.form['consumer_key'],
                                      request.form['secret_key'],
                                      request.form['access_token'],
                                      request.form['secret_access_token'])
        collector.start(pm)
    except Exception as e:
        flash(e.message, category='danger')
        return redirect('/twitter/follower')

    flash('Process Started!', category='success')
    return redirect('/twitter')

##################################################################################
#                        Friends Collector Area                                  #
##################################################################################


@app.route('/twitter/friends', methods=['GET'])
def twitter_friends_index():
    """
    Twitter collector index page
    :return:
    """
    return render_template('twitter/friends/index.html')


@app.route('/twitter/friends/create', methods=['POST'])
def twitter_friends_create():
    """
    Method used to create a new subprocess of a Friends Collector object
    :return:
    """
    try:
        collector = FriendsCollector(request.form['user'],
                                     request.form['consumer_key'],
                                     request.form['secret_key'],
                                     request.form['access_token'],
                                     request.form['secret_access_token'])
        collector.start(pm)
    except Exception as e:
        flash(e.message, category='danger')
        return redirect('/twitter/friends')

    flash('Process Started!', category='success')
    return redirect('/twitter')


if __name__ == '__main__':
    app.run()
