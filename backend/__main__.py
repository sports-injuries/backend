from flask import Flask
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)

def main():
    logger.info('hello world')


if __name__ == '__main__':
    main()