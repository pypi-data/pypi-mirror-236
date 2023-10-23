# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-22 22:50:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Send methods.
"""


from typing import Dict, Optional, overload
from queue import Queue
from os.path import getsize as os_getsize
from reytool.rsystem import rexc
from reytool.rtime import sleep
from reytool.rwrap import start_thread
from reytool.rnumber import randn
from reytool.rrequest import get_file_send_time

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
        rclient: RClient,
        bandwidth: float
    ) -> None:
        """
        Build `send` instance.

        Parameters
        ----------
        rclient : 'RClient' instance.
        bandwidth : Upload bandwidth, unit Mpbs.
        """

        # Set attribute.
        self.rclient = rclient
        self.bandwidth = bandwidth
        self.queue: Queue[Dict] = Queue()
        self.added: bool = False
        self.started: bool = False

        # Start sender.
        self._add_sender()
        self.start_sender()


    def get_interval(
        self,
        params: Dict,
        minimum: float = 0.8,
        maximum: float = 1.2,
    ) -> float:
        """
        Get message send `interval time`, unit seconds.

        Parameters
        ----------
        params : Message parameters.
            - `Has key 'file' and is not None` : Calculate file send time, but not less than random seconds.
            - `Other` : Calculate random seconds.

        minimum : Random minimum seconds.
        maximum : Random maximum seconds.

        Returns
        -------
        Send interval seconds.
        """

        # Get parameters.
        file = params.get("file")

        # Random.
        seconds = randn(minimum, maximum, precision=2)

        # File.
        if file is not None:
            file_seconds = get_file_send_time(file, self.bandwidth)
            if file_seconds > seconds:
                seconds = file_seconds

        return seconds


    @start_thread
    def _add_sender(self) -> None:
        """
        Add `sender`, it will get message parameters from queue and send.
        """

        # Check.
        if self.added:
            rexc(value=self.added)
        else:
            self.added = True

        # Loop.
        while True:

            ## Start.
            if self.started:
                params = self.queue.get()
                self.rclient.send(**params)
                seconds = self.get_interval(params)

            ## Pause.
            else:
                seconds = 0.1

            ## Interval.
            sleep(seconds)


    def start_sender(self) -> None:
        """
        Start `sender`.
        """

        # Start.
        self.started = True


    def pause_sender(self) -> None:
        """
        Pause `sender`.
        """

        # Pause.
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

        # Check.

        ## "text" and "file".
        rexc.check_most_one(text, file)
        rexc.check_least_one(text, file)

        ## "text".
        if text is not None:
            if ats is not None:

                ## ID type.
                if "@chatroom" not in receiver:
                    raise ValueError("when using parameter 'ats', parameter 'receiver' must be room ID.")

                ## Count "@" symbol.
                comma_n = ats.count(",")
                at_n = text.count("@")
                if at_n < comma_n:
                    raise ValueError("when using parameter 'ats', parameter 'text' must have with ID same quantity '@' symbols")

        ## "file".
        elif file is not None:
            rexc.check_file_found(file)

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