import argparse
import logging
from config import Config
from logging.handlers import RotatingFileHandler
import signal
import os
import sys

# Defining arguments and creating the args object
parser = argparse.ArgumentParser(allow_abbrev=False, description='A tool to automate Dig lookup')
parser.add_argument('-if', '--input_file',
                    dest='input_file',
                    type=str,
                    help='Input file',
                    required=True)
parser.add_argument('-of', '--output_file',
                    dest='output_file',
                    type=str,
                    help='Output file',
                    required=False)

args = parser.parse_args()

# Define logging : file and console

if not os.path.exists('logs'):
    os.mkdir('logs')

if not os.path.exists('outputs'):
    os.mkdir('outputs')

# Logging
# create logger with 'spam_application'
logger = logging.getLogger('autodig')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
file_handler = logging.FileHandler('logs/{}'.format(Config.LOG_FILENAME))
file_handler.setLevel(Config.FILE_LOGGING_LEVEL)
# create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(Config.CONSOLE_LOGGING_LEVEL)
# create formatter and add it to the handlers
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
# console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
console_handler.setFormatter(console_formatter)
# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.debug('AutoDig app has started')


# Signal handler To exit on Ctrl+C
def signal_handler(sig, frame):
    logger.warning('You pressed Cnrtl+C. Proceeding to exit...')
    sys.exit('Bye!')


signal.signal(signal.SIGINT, signal_handler)

