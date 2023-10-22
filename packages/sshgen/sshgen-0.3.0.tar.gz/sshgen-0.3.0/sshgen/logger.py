#!/usr/bin/env python
import logging

from sshgen.models.loglevel import LogLevel


def init_logger(level: LogLevel) -> None:
    match level:
        case LogLevel.INFO:
            logging.basicConfig(level=logging.INFO,
                                format='[%(asctime)s] [%(levelname)s] - %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
        case LogLevel.DEBUG:
            logging.basicConfig(level=logging.DEBUG,
                                format='[%(asctime)s] [%(levelname)s] - %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
