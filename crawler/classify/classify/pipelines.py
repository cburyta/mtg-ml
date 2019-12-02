# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
# import psycopg2
import records


class ClassifyPipeline(object):
    def open_spider(self, spider):
        db_conn_str = os.environ.get('DB_CONNECTION_STRING')
        self.db = records.Database(db_conn_str)

        # hostname = os.getenv('POSTGRES_HOSTNAME', 'localhost')
        # username = os.environ.get('POSTGRES_USER')
        # password = os.environ.get('POSTGRES_PASSWORD')
        # database = os.environ.get('POSTGRES_DB')
        # self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        # self.cur = self.connection.cursor()

        print('Pipeline Open: Type: %s' % ('ClassifyPipeline'))
        print('Database Hostname: %s' % (db_conn_str))

    def close_spider(self, spider):
        # self.cur.close()
        # self.connection.close()
        print('Pipeline: Close: %s' % ('ClassifyPipeline'))

    def process_item(self, item, spider):
        print('Item: Name: %s' % (item['name']))

        select_query = (
            'SELECT * FROM cards WHERE name = :name AND lang=:lang LIMIT 1'
        )
        rows = self.db.query(select_query, name=item['name'], lang='en')
        row = rows.first()

        upsert_query = (
            'INSERT INTO class_ramp (oracle_id) '
            'VALUES ( :oracle_id ) '
            'ON CONFLICT ON CONSTRAINT class_ramp_oracle_id_unique '
            'DO NOTHING; '
        )
        self.db.query(upsert_query, oracle_id=row['oracle_id'])

        # self.cur.execute('SELECT * FROM cards LIMIT 10')
        # item = self.cur.fetchone()
        print('Card.oracle_id: %s' % (row['oracle_id']))

        return item