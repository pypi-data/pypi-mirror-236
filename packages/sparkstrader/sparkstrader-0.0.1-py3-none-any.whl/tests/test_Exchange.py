#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/7/21 18:16
Desc: To test intention, just write test code here!
"""
import sys

sys.path.insert(0, f"{sys.path[0]}/..")
from tests.testApiClient import *


def test_GetList():
    df = api.Exchange.GetList()
    print(df)
    # assert df.shape[0] > 0


if __name__ == "__main__":
    test_GetList()
