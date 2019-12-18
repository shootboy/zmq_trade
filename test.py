# -*- coding: utf-8 -*-
"""
@Author: ShotBoy
@File: test.py
@Time: 2019/12/18 15:53
@Motto：I have a bad feeling about this.
"""
class cal:
    cal_name = '计算器'
    def __init__(self,x,y):
        self.x=x
        self.y= y

    @property
    def cal_add(self):
        return self.x+self.y

    @classmethod
    def cal_info(cls):
        print cls.cal_name

    @staticmethod
    def cal_test(a, b,c):
        print a,b,c

cl=cal(10,11)
cal.cal_test(1,2,3)
cl.cal_info()
cal.cal_info()