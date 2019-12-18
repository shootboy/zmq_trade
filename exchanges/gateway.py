# -*- coding: utf-8 -*-
"""
@Author: ShotBoy
@File: gateway.py
@Time: 2019/12/18 16:59
@Motto：I have a bad feeling about this.
"""
from threading import Lock
from datetime import datetime
from clients.csvClient import FileClient
from clients.zmqClient import ZmqClient
from util.market_data import L2Depth, Trade, Snapshot
from datetime import datetime
import pytz

class TradeExchangeGateway:
    """
       Exchange gateway
       """
    is_local_timestamp = True
    def __init__(self, api_socket, db_clients=[]):
        """
        Constructor
        :param exchange_name: Exchange name
        :param exchange_api: Exchange API
        :param db_client: Database client
        """
        self.db_clients = db_clients
        self.api_socket = api_socket
        self.lock = Lock()
        self.exch_snapshot_id = 0
        self.date_time = datetime.utcnow().date()

    @classmethod
    def get_exchange_name(cls):
        """
        Get exchange name
        :return: Exchange name string
        """
        return ''

    def get_instmt_trade_table_name(self, exchange, instmt_name, strategy_name):
        """
        Get instmt snapshot
        :param exchange: Exchange name
        :param instmt_name: Instrument name
        """
        # print exchange,instmt_name,strategy_name
        return 'exch_' + exchange.lower() + '_' + instmt_name.lower() + '_' + strategy_name.lower() + \
               '_trade_' + self.date_time.strftime("%Y%m%d")

    @classmethod
    def get_trade_table_name(cls):
        return 'exchanges_trade'

    @classmethod
    def is_allowed_snapshot(cls, db_client):
        return not isinstance(db_client, FileClient)

    @classmethod
    def is_allowed_instmt_record(cls, db_client):
        return not isinstance(db_client, ZmqClient)

    @classmethod
    def init_snapshot_table(cls, db_clients):
        for db_client in db_clients:
            db_client.create(cls.get_trade_table_name(),
                             Snapshot.columns(),
                             Snapshot.types(),
                             [0, 1], is_ifnotexists=True)

    def init_instmt_snapshot_table(self, instmt):
        table_name = self.get_instmt_trade_table_name(instmt.get_exchange_name(),
                                                         instmt.get_instmt_name(),
                                                      instmt.get_strategy_name())

        instmt.set_instmt_snapshot_table_name(table_name)
        for db_client in self.db_clients:
            db_client.create(table_name,
                             ['id'] + Trade.columns(),
                             ['int'] + Trade.types(),
                             [0], is_ifnotexists=True)

    def start(self, instmt):
        """
        Start the exchange gateway
        :param instmt: Instrument
        :return List of threads
        """
        return []

    def get_instmt_snapshot_id(self, instmt):
        with self.lock:
            self.exch_snapshot_id += 1

        return self.exch_snapshot_id

    def insert_trade(self, instmt, trade):
        """
        Insert trade row into the database client
        :param instmt: Instrument
        """
        # If the instrument is not recovered, skip inserting into the table
        if not instmt.get_recovered():
            return

        # If local timestamp indicator is on, assign the local timestamp again
        if self.is_local_timestamp:
            trade.date_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y%m%d %H:%M:%S.%f")
        date_time = datetime.strptime(trade.date_time, "%Y%m%d %H:%M:%S.%f").date()
        if date_time != self.date_time:
            self.date_time = date_time
            self.init_instmt_snapshot_table(instmt)
        instmt.set_last_trade(trade)
        # update
        if instmt.get_last_trade() is not None:
            id = self.get_instmt_snapshot_id(instmt)
            for db_client in self.db_clients:
                is_allowed_snapshot = self.is_allowed_snapshot(db_client)
                is_allowed_instmt_record = self.is_allowed_instmt_record(db_client)
                if is_allowed_snapshot:
                    db_client.insert(table=self.get_trade_table_name(),
                                     columns=Trade.columns(),
                                     values=Trade().values(),
                                     types=Trade.types(),
                                     primary_key_index=[0, 1],
                                     is_orreplace=True,
                                     is_commit=not is_allowed_instmt_record)