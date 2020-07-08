import os
import logging


basedir = os.getcwd()

class Config:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///'+os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    FILE_LOGGING_LEVEL = logging.DEBUG
    CONSOLE_LOGGING_LEVEL = logging.INFO
    LOG_FILENAME = 'autodig.log'

    # name servers
    NAME_SERVERS = os.environ.get('NAME_SERVERS') or ['8.8.8.8', '1.1.1.1']
