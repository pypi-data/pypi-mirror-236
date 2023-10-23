# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-17 20:27:16
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : WeChat methods.
"""


from .rclient import RClient
from .rsend import RSend


__all__ = (
    "RWeChat",
)


class RWeChat(object):
    """
    Rey's `WeChat` type.
    """


    def __init__(self) -> None:
        """
        Build `WeChat` instance.
        """

        # Set attribute.
        self.rclient = RClient()
        self.rsend = RSend(self.rclient)
        self.receive = self.rclient.receive
        self.send = self.rsend.send