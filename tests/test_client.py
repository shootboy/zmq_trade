# -*- coding: utf-8 -*-
"""
@Author: ShotBoy
@File: test_client.py
@Time: 2019/12/18 19:44
@Motto：I have a bad feeling about this.
"""
from exchanges.Deribit.deribit import ExchGwTradeDeribit
from util.instrument import Instrument
from util.Log import Logger
from clients.zmqClient import ZmqClient
from time import sleep
from datetime import datetime
import ast

Logger.init_log()
dbclient = ZmqClient()
dbclient.connect(addr='tcp://127.0.0.1:5000')
exchange_name = 'Deribit'
instmt_name = 'BTC'
instmt_code = 'BTC-20DEC19-7250-C'
instmt = Instrument(exchange_name, instmt_name, instmt_code)
exch = ExchGwTradeDeribit([dbclient])
exch.start(instmt)