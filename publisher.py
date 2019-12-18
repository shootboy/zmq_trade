# -*- coding: utf-8 -*-
"""
@Author: ShotBoy
@File: publisher.py
@Time: 2019/12/18 14:56
@Motto：I have a bad feeling about this.
"""
import zmq

context=zmq.Context()
socket=context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5000")
while True:
    msg = input('input your data:')
    socket.send_json(msg)