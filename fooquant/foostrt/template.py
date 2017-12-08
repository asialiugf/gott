# -*- coding: utf-8 -*-

# define your own import 

import sys
sys.path.append("..")

import pandas as pd
import numpy as np
import datetime
import math


# ------------------------------------------------------------
# 自定义变量区
ttt = 1000

# ------------------------------------------------------------
# 自定义函数区
def test():
    print("this is a test fun!!")

# ------------------------------------------------------------
from fooquant.base import StrategyBase

class Mystrategy(StrategyBase):
    def __init__(self, *args, **kwargs):
        super(Mystrategy, self).__init__(*args, **kwargs)
        pass


    def on_login(self):
        pass

    def on_error(self, code, msg):
        pass

    def on_tick(self, tick):
        pass

    def on_bar(self, bar):
        print(self.ccc)
        print(self.bbb)
        print(ttt)
        #print(xxx)
        print(self.mmm)
        print(bar)
        test()
        pass

    def on_execrpt(self, res):
        pass

    def on_order_status(self, order):
        pass

    def on_order_new(self, res):
        pass

    def on_order_filled(self, res):
        pass

    def on_order_partiall_filled(self, res):
        pass

    def on_order_stop_executed(self, res):
        pass

    def on_order_canceled(self, res):
        pass

    def on_order_cancel_rejected(self, res):
        pass


if __name__ == '__main__':
    myStrategy = Mystrategy(
        username='-',
        password='-',
        strategy_id='9c877be1-d96b-11e7-ac6d-68f7283cd5ae',
        subscribe_symbols='SHSE.600694.tick,SHSE.600694.bar.15,SHSE.600694.bar.60',
        mode=4,
        td_addr='127.0.0.1:8001'
    )
    myStrategy.__init__()
    ret = myStrategy.run()
    print('exit code: ', ret)
