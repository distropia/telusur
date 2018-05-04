#! /usr/bin/env python
from django.core.management.base import BaseCommand, CommandError
from telusur.settings import DATABASES
import MySQLdb

class Command(BaseCommand):
    help = 'Handle MySQL unicode problem.'

    def handle(self, *args, **options):
        db_credential = DATABASES.get('default')
        dbname = db_credential.get('NAME')

        db = MySQLdb.connect(
            host='localhost', 
            user=db_credential.get('USER'), 
            passwd=db_credential.get('PASSWORD'), 
            db=dbname)
        cursor = db.cursor()

        cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'" % dbname)

        sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % dbname
        cursor.execute(sql)

        results = cursor.fetchall()
        for row in results:
            sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
            cursor.execute(sql)
        db.close()