#! /usr/bin/env python
from django.core.management.base import BaseCommand, CommandError
import MySQLdb

class Command(BaseCommand):
    help = 'Handle MySQL unicode problem.'

    def handle(self, *args, **options):
        host = "localhost"
        passwd = "566856"
        user = "root"
        dbname = "production_telusur"

        db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
        cursor = db.cursor()

        cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'" % dbname)

        sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % dbname
        cursor.execute(sql)

        results = cursor.fetchall()
        for row in results:
            sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
            cursor.execute(sql)
        db.close()