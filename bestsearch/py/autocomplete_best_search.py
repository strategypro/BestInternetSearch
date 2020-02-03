#!/usr/bin/python3

import cgi
import sys
import json

sys.path.insert(0, "/var/www")

from db_bestsearch import *
cur = db.cursor(MySQLdb.cursors.DictCursor)
pg_cursor = pg_database.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

from html import escape

def enc_print(string='', encoding='utf8'):
    sys.stdout.buffer.write(string.encode(encoding) + b'\n')

enc_print("Content-type:application/html;charset=utf-8;")
enc_print()

html = ''
args = cgi.FieldStorage()
query = '' if not args.getvalue( "q" ) else escape( args.getvalue( "q" ) )
query = query.lower()

if not query == '':

    qq = []
    sql = f"""SELECT * from search WHERE LOWER(site_name) LIKE '%{query}%' OR LOWER(site_title) LIKE '%{query}%' ORDER BY id ASC LIMIT 20; """
    cur.execute(sql)
    res = cur.fetchall()    
    for row in res:
        site_name = row['site_name']
        site_title = row['site_title']
        
        if site_title != '':
            site_name_output = f"""{site_name} -- {site_title} """
        else:
            site_name_output = site_name
            
        site_address = row['site_address']
        qq.append({"value": site_address, "label": site_name_output  })



    if len(qq) < 20:
        
        #qq_limit = 20 - len(qq)
        
        sql = f"""SELECT title FROM data WHERE title LIKE '%{query}%' ORDER BY CHAR_LENGTH(title) LIMIT {5};"""
        
        pg_cursor.execute(sql)
        res = pg_cursor.fetchall()
        for row in res:
            title = row['title']
            qq.append({"value": "", "label": title  })
        
    #enc_print ( json.dumps(qq, separators=(',', ':')) )
    enc_print ( json.dumps(qq) )

