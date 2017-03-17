# -*- coding:utf-8 -*-

import random


def random_series(count, len=10):
    str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    series_set = set()
    for i in range(0, count):
        series = []
        for j in range(0, len):
            series += random.choice(str)
            # 去重 -------------可以用set
            # if series not in series_set:
            series_set.append(series)
            print series

random_series(20)
