#!/usr/bin/env python

import logging
import sys


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def create(name):
    logger = logging.getLogger(name)
    logger.propagate = False

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('[{}|%(asctime)s|%(module)s:%(lineno)d|%(levelname)s] %(message)s'.format(name), datefmt=DATE_FORMAT)

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    return logger

server_logger = create('epubify-server')
worker_logger = create('epubify-worker')

