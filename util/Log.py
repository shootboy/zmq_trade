# -*- coding: utf-8 -*-
"""
@Author: ShotBoy
@File: Log.py
@Time: 2019/12/18 15:31
@Motto：I have a bad feeling about this.
"""
from datetime import datetime
import logging
logging.basicConfig()

class Logger:
    logger = None

    @staticmethod
    def init_log(output=None):
        """
        Initialise the logger
        """
        Logger.logger = logging.getLogger('zmq_trade')
        Logger.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s \n%(message)s\n')
        if output is None:
            slogger = logging.StreamHandler()
            slogger.setFormatter(formatter)
            Logger.logger.addHandler(slogger)
        else:
            flogger = logging.FileHandler(output)
            flogger.setFormatter(formatter)
            Logger.logger.addHandler(flogger)

    @staticmethod
    def info(method, str):
        """
        Write info log
        :param method: Method name
        :param str: Log message
        """
        Logger.logger.info('[%s]\n%s\n' % (method, str))

    @staticmethod
    def error(method, str):
        """
        Write info log
        :param method: Method name
        :param str: Log message
        """
        Logger.logger.error('[%s]\n%s\n' % (method, str))