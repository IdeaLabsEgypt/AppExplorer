from unittest import TestCase
import MySQLdb


class SQLQueryGenerator:
    def __init__(self):
        pass

    def generate_sql(self, table, term, language, category, cluster, downloads):
        sql = "SELECT * FROM appsdb.%s " % table
        _term = self.get_term(term)
        _language = self.get_language(language)
        _category = self.get_category(category)
        _cluster = self.get_cluster_id(cluster)
        _downloads = self.get_downloads(downloads)

        #not neat but... meh
        if len(_term+_language+_category+_cluster+_downloads)> 0:
            sql += "WHERE "
        if len(_term) > 0:
            sql += _term
        if len(_language) > 0:
            if len(_term) > 0:
                sql += " AND "
            sql += _language
        if len(_category) > 0:
            if len(_language) > 0 or len(_term) > 0:
                sql += " AND "
            sql += _category
        if len(_cluster) > 0:
            if len(_term) > 0 or len(_category) > 0 or len(_language) > 0:
                sql += " AND "
            sql += _cluster
        if len(_downloads) > 0:
            if len(_term) > 0 or len(_category) > 0 or len(_language) > 0 or len(_cluster) > 0:
                sql += " AND "
            sql += _downloads
        return sql

    def get_term(self, term):
        if len(term) != 0:
            return 'title like "%s%%"' % term
        return ""

    def get_language(self, lang):
        if len(lang) !=0:
            return 'lang_id = "%s"' % lang
        return ""

    def get_category(self, category):
        if len(category) !=0:
            return 'category = "%s"' % category
        return ""

    def get_cluster_id(self, cluster):
        if len(str(cluster)) != 0:
            return 'cluster_id = %d' % int(cluster)
        return ""

    def get_downloads(self, downloads):
        if len(downloads) != 0:
            return 'downloads = "%s"' % downloads
        return ""
        


class SQLQueryGeneratorTest(TestCase):
    def setUp(self):
        self.sqlgen = SQLQueryGenerator()
        pass

    # def test_connection(self):
    #     self.assertTrue(str(self.sqlgen.connection()).startswith("<_mysql.connection"))

    def test_generate_sql(self):
        self.assertEqual(self.sqlgen.generate_sql("clustered_apps_em_short", "kid", "en", "Educational", 1, "10-50"),
                         'SELECT * FROM appsdb.clustered_apps_em_short '
                         'WHERE title like "kid%" '
                         'AND lang_id = "en" '
                         'AND category = "Educational" '
                         'AND cluster_id = 1 '
                         'AND downloads = "10-50"')
        self.assertEqual(self.sqlgen.generate_sql("clustered_apps_em_short", "", "", "", "", ""),
                         'SELECT * FROM appsdb.clustered_apps_em_short ')

        self.assertEqual(self.sqlgen.generate_sql("clustered_apps_em_short", "kid", "", "", "", ""),
                         'SELECT * FROM appsdb.clustered_apps_em_short '
                         'WHERE title like "kid%"')

        self.assertEqual(self.sqlgen.generate_sql("clustered_apps_em_short", "kid", "", "Educational", "", ""),
                         'SELECT * FROM appsdb.clustered_apps_em_short '
                         'WHERE title like "kid%"'
                         ' AND category = "Educational"')
