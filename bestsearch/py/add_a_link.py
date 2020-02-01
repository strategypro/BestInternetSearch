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
output_message=''

args = cgi.FieldStorage()

url = '' if not args.getvalue( "url" ) else escape( args.getvalue( "url" ) )
title = '' if not args.getvalue( "title" ) else escape( args.getvalue( "title" ) )
keywords = '' if not args.getvalue( "keywords" ) else escape( args.getvalue( "keywords" ) )

if url.endswith('/'):
    url = url[:-1]


sql = f"""SELECT url FROM add_a_link WHERE url = '{url}';"""
cur.execute(sql)
row = cur.fetchone()
if not row:
    sql = f"""
    INSERT INTO add_a_link (url, title, keywords) VALUES 
    ( '{url}', '{title}', '{keywords}' );
    """
    
    output_message = f"""thanks, the url has been added to be verified"""
    
    cur.execute(sql)
    db.commit()
    
else:
    output_message = f"""thanks, already added to be verified"""




enc_print ( output_message )

