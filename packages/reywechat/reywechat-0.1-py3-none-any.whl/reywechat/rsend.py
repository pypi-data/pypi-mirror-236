# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-22 22:50:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Send methods.
"""


from typing import Dict, Optional
from queue import Queue
from reytool.rsystem import rexc
from reytool.rtime import sleep
from reytool.rwrap import start_thread

from .rclient import RClient


__all__ = (
    "RSend",
)


class RSend(object):
    """
    Rey's `send` type.
    """


    def __init__(
        self,
        rclient: RClient
    ) -> None:
        """
        Build `send` instance.

        Parameters
        ----------
        rclient : 'RClient' instance.
        """

        # Set attribute.
        self.rclient = rclient
        self.queue: Queue[Dict] = Queue()
        self.started: bool = False

        # Start sender.
        self._add_sender()
        self.start_sender()


    @start_thread
    def _add_sender(self):
        """

        """

        while True:
            if self.started:
                params = self.queue.get()
                self.rclient.send(**params)
            sleep(1)


    def start_sender(self):
        """

        """

        self.started = True


    def pause_sender(self):
        """

        """

        self.started = False


    def send(
        self,
        receiver: str,
        text: Optional[str] = None,
        ats: Optional[str] = None,
        file: Optional[str] = None,
        timeout: Optional[float] = None
    ) -> None:
        """
        Queue add plan, waiting send `text` or `file` message.

        Parameters
        ----------
        receiver : WeChat user ID or room ID.
        text : Text message content. Conflict with parameter 'file'.
        ats : User ID to '@' of text message content, comma interval. Can only be use when parameter 'receiver' is room ID.
            - `None` : Not use '@'.
            - `str` : Use '@', parameter 'text' must have with ID same quantity '@' symbols.

        file : File message path. Conflict with parameter 'text'.
        timeout : Number of timeout seconds.

        Examples
        --------
        Send text.
        >>> receiver = 'uid_or_rid'
        >>> rclient.send(receiver, 'Hello!')

        Send text and '@'.
        >>> receiver = 'rid'
        >>> ats = ('uid1', 'uid2')
        >>> rclient.send(receiver, '@uname1 @uname2 Hello!', ats)

        Send file.
        >>> file = 'file_path'
        >>> rclient.send(receiver, file=file)
        """

        # Check parameter.

        ## "text" and "file".
        rexc.check_most_one(text, file)
        rexc.check_least_one(text, file)

        ## "ats".
        if (
            text is not None
            and ats is not None
        ):

            ## ID type.
            if "@chatroom" not in receiver:
                raise ValueError("when using parameter 'ats', parameter 'receiver' must be room ID.")

            ## Count "@" symbol.
            comma_n = ats.count(",")
            at_n = text.count("@")
            if at_n < comma_n:
                raise ValueError("when using parameter 'ats', parameter 'text' must have with ID same quantity '@' symbols")

        # Get parameter.
        params = {
            "receiver": receiver,
            "text": text,
            "ats": ats,
            "file": file,
            "check": False
        }

        # Add plan.
        self.queue.put(params, timeout=timeout)