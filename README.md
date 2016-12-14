# social-listener

Python project used to collect tweets and social-network data from Social's API

## Requirements

First of all create a Virtualenv

    virtualenv envSocial
    source envSocial/bin/activate

Install requirements:

    pip install -r requirements.txt


## How to Run

Create your own config file:

    cp config.ini.sample config.ini
    
Remember to edit the file with your settings.

In Development Mode:

    export FLASK_DEBUG=1
    export FLASK=server.py
    flask run
    
In Production Mode use WSGI with Apache/NGINX (documentation will be provided soon..).