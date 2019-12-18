# -*- coding: utf-8 -*-
"""
@Author: ShotBoy
@File: suber.py
@Time: 2019/12/18 15:08
@Motto：I have a bad feeling about this.
"""
import zmq
context = zmq.Context()
socket=context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5000")
socket.setsockopt(zmq.SUBSCRIBE,'')
while True:
    print socket.recv_json()