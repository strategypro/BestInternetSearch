#!/usr/bin/python3

import cgi
import sys
import json

sys.path.insert(0, "/var/www")

from db_bestsearch import *
cur = db.cursor(MySQLdb.cursors.DictCursor)

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

    cur.execute(f"""SELECT * from search WHERE LOWER(site_name) LIKE '%{query}%' OR LOWER(site_title) LIKE '%{query}%' """)
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


    #enc_print ( json.dumps(qq, separators=(',', ':')) )
    enc_print ( json.dumps(qq) )

