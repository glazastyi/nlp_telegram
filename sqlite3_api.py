# -*- coding: utf-8 -*-
import sqlite3
import logging

class Sqlite3(object):
    def __init__(self, way, table_name, dummy):
        self.way = way
        self.set_values(get_request("create", table_name, dummy))

    def set_values(self, request, *argv):
        logger = logging.getLogger("Sqlite3.set_values")
        try:
            con = sqlite3.connect(self.way)
            cur = con.cursor()
            cur.execute(request, *argv)
            con.commit()
            con.close()
        except Exception as e:
            logger.error(e)

    def get_values(self, request):
        result = None
        logger = logging.getLogger("Sqlite3.get_values")
        try:
            con = sqlite3.connect(self.way)
            cur = con.cursor()
            cur.execute(request)
            result = cur.fetchall()
            con.commit()
            con.close()
        except Exception as e:
            logger.error(e)

        return result


def get_request(mode, table, dictionary):
    logger = logging.getLogger("Sqlite3.get_reqiest")
    try:
        columns = ", ".join(dictionary.keys())
        placeholders = ", ".join("?" * len(dictionary))
        values = ", ".join(["{} {}".format(x[0], x[1]) for x in dictionary.items()])


        base_requests = dict(
            create="CREATE TABLE IF NOT EXISTS {} ({})".format(table, values),
            insert="INSERT INTO {} ({}) values({})".format(table, columns, placeholders),
            replace="REPLACE INTO {} values({})".format(table, placeholders))
        return base_requests[mode]
    except Exception as e:
        logger.error(e)
        return None

