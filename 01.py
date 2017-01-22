# -*- coding:utf-8 -*-
# 第 0001 题：**做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用**生成激活码**（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券)

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
