# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-23 20:55:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database methods.
"""


from reytool.rdatabase import REngine
from reytool.rprint import rprint


class RDatabase(object):
    """
    Rey's `database` type.
    """


    def __init__(
        self,
        rengine: REngine
    ) -> None:
        """
        Build `database` instance.

        Parameters
        ----------
        rengine : REngine instance.
        """

        # Set attribute.
        self.rengine = rengine




    def build_all(self): ...


class RDBBuild(object):
    """
    Rey's `database build` type.
    """


    def __init__(
        self,
        rengine: REngine
    ) -> None:
        """
        Build `database build` instance.

        Parameters
        ----------
        rengine : REngine instance.
        """

        # Set attribute.
        self.rengine = rengine


    def confirm_input(
        self,
        sql: str
    ) -> None:
        """
        `Print` tip text, and `confirm` execute SQL. If reject, throw exception.

        Parameters
        ----------
        sql : SQL.
        """

        # Confirm.
        command = rprint.rinput(sql, "Do you want to execute SQL to build the database? Otherwise stop program. (y/n): ", frame="top", title="SQL")

        # Check.
        command = command.lower()
        if command == "n":
            raise AssertionError("program stop")


    def build_wechat(self) -> None:
        """
        Build database `wechat`.
        """

        # Break.
        exist = self.rengine.build.exist(("wechat", None, None))
        if exist: return

        # Generate SQL.
        sql = self.rengine.build.create_database("wechat", execute=False)

        # Confirm.
        self.confirm_input(sql)

        # Excute.
        self.rengine(sql)

        # Report.
        print("Database build completed.")