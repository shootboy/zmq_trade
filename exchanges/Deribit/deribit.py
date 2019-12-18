# -*- coding: utf-8 -*-
"""
@Author: ShotBoy
@File: deribit.py
@Time: 2019/12/18 16:54
@Motto：I have a bad feeling about this.
"""
from api.ws_api_socket import WebsocketApiClient
from exchanges.gateway import ExchangeGateway
from util.market_data import L2Depth, Trade
from util.Log import Logger
from datetime import datetime, timedelta
import hashlib
import json
import re
from functools import partial
import time
from util.instrument import Instrument

class ExchTradeDeribitWs(WebsocketApiClient):

    """
    trade socket
    功能模块
    """
    def __init__(self):
        """
        Constructor
        """
        WebsocketApiClient.__init__(self, 'ExchApiTradeDeribit_Option')

    @classmethod
    def get_link(cls):
        return 'wss://testapp.deribit.com/ws/api/v2'

    @classmethod
    def get_last_trades_subscription_string(cls, instmt):
        d = {}
        d['method'] = "public/get_last_trades_by_instrument_and_time"
        d["jsonrpc"] = "2.0"
        d["id"] = 222
        d["params"] = {
            "instrument_name": instmt.instmt_code,
            "end_timestamp": time.time() * 1000,
            "count": 100
        }
        return json.dumps(d)

    @classmethod
    def get_ticker_subscription_string(cls, instmt):
        d = {}
        d['method'] = "public/ticker"
        d["jsonrpc"] = "2.0"
        d["id"] = 222
        d["params"] = {
            "instrument_name": instmt.instmt_code
        }
        return json.dumps(d)

    @classmethod
    def login(cls, params):
        # print "loginniii"
        # 生成请求
        d = {}
        d['event'] = 'login'
        d['parameters'] = params
        return json.dumps(d)

    @classmethod
    def trade(cls, channel, params):
        # 生成请求
        d = {}
        d['event'] = 'addChannel'
        d['channel'] = channel
        d['parameters'] = params
        return json.dumps(d)

class ExchGwTradeDeribit(ExchangeGateway):

    def __init__(self, db_clients):
        ExchangeGateway.__init__(self, ExchTradeDeribitWs(), db_clients)
        #self.apiKey = apiKey
        #self.secretKey = secretKey

    @classmethod
    def get_exchange_name(cls):
        """
        Get exchange name
        :return: Exchange name string
        """
        return 'Deribit'

    def on_open_handler(self, instmt, ws):
        """
        Socket on open handler
        :param instmt: Instrument
        :param ws: Web socket
        """
        Logger.info(self.__class__.__name__, "Instrument %s is subscribed in channel %s" % \
                    (instmt.get_instmt_name(), instmt.get_exchange_name()))
        if not instmt.get_subscribed():
            Logger.info(self.__class__.__name__,
                        'last trade string:{}'.format(self.api_socket.get_last_trades_subscription_string(instmt)))
            Logger.info(self.__class__.__name__,
                        'ticker string:{}'.format(self.api_socket.get_ticker_subscription_string(instmt)))
            #ws.send(self.api_socket.get_last_trades_subscription_string(instmt))
            ws.send(self.api_socket.get_ticker_subscription_string(instmt))
            instmt.set_subscribed(True)

    def on_close_handler(self, instmt, ws):
        """
        Socket on close handler
        :param instmt: Instrument
        :param ws: Web socket
        """
        Logger.info(self.__class__.__name__, "Instrument %s is unsubscribed in channel %s" % \
                    (instmt.get_instmt_name(), instmt.get_exchange_name()))
        instmt.set_subscribed(False)

    def on_message_handler(self, instmt, message):
        """
        Incoming message handler
        :param instmt: Instrument
        :param message: Message
        """
        print message

    def start(self, instmt):
        self.init_instmt_snapshot_table(instmt)
        Logger.info(self.__class__.__name__,
                    'instmt snapshot table: {}'.format(instmt.get_instmt_code()))
        return [self.api_socket.connect(self.api_socket.get_link(),
                                        on_message_handler=partial(self.on_message_handler, instmt),
                                        on_open_handler=partial(self.on_open_handler, instmt),
                                        on_close_handler=partial(self.on_close_handler, instmt))]

if __name__ == '__main__':
    import logging
    import websocket
    websocket.enableTrace(True)
    logging.basicConfig()
    Logger.init_log()
    exchange_name = 'Deribit'
    instmt_name = 'BTC'
    instmt_code = 'BTC-20DEC19-7250-C'
    instmt = Instrument(exchange_name, instmt_name, instmt_code)
    exch = ExchGwTradeDeribit([])
    exch.start(instmt)