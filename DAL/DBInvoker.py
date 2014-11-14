__author__ = 'skandeel'
# The brains is here, here the query gets made and excuted and results goes back
# TODO: (only in case we're gonna use json)
# Add interface for the JSON query that will come from the website
# Add wrapper to wrap the results in json objects and send it back

from unittest import TestCase
import MySQLdb
import SQLQueryGenerator


class DBInvoker:
    def __init__(self):
        self.db = self.connection()
        self.query_gen = SQLQueryGenerator.SQLQueryGenerator()

        pass

    def connection(self):
        return MySQLdb.connect("localhost", "root", "root", "appsdb", use_unicode=True, charset="utf8")

    def convert_to_sql(self, json):
        #does some stuff to the json input and parses it
        #return self.query_gen.generate_sql()
        pass

    def execute_sql(self, sql):
        list = []
        cur = self.db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        while row is not None:
            list.append(row)
            row = cur.fetchone()
        print len(list)
        return list


class DBInvokerTest(TestCase):
    def setUp(self):
        self.dbinvoker = DBInvoker()
        pass

    def test_excute_sql(self):
        self.assertEqual(len(self.dbinvoker.execute_sql('SELECT * FROM appsdb.clustered_apps_em_short '
                                                        'WHERE title like "kid%" '
                                                        'AND category = "Educational"')), 433)

        self.assertEqual(len(self.dbinvoker.execute_sql('SELECT * FROM appsdb.clustered_apps_em_short '
                                                        'WHERE title like "kid%" '
                                                        'AND lang_id = "en" '
                                                        'AND category = "Educational" '
                                                        'AND downloads = "0"')), 16)


    def tearDown(self):
        self.dbinvoker.db.close()
