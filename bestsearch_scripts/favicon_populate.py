#!/usr/bin/python3

import sys

from pyquery import PyQuery as pq
import requests
import favicon
import base64


sys.path.insert(0, "/var/www")

from db_bestsearch import *
cur = db.cursor(MySQLdb.cursors.DictCursor)

content = ''
uri =''
data = None
data2 = None
icons=[]


sql = f"""SELECT * from search WHERE site_favicon_uri = ''; """
cur.execute(sql)
res = cur.fetchall()

for row in res:

    varid = row['id']
    address = row['site_address']
    
    print (address)
    
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
    headers = {'User-Agent': user_agent}
    icons = favicon.get(address, headers=headers, timeout=5)
        
    #icons = favicon.get(address)

    if len(icons) > 0:
        icon = icons[0]

        headers = {
            "User-Agent": user_agent
        }
        response = requests.get(icon.url, headers=headers)
        
        
        uri = ("data:" + response.headers['Content-Type'] + ";" +
           "base64," + base64.b64encode(response.content).decode("utf-8"))
           
        sql = f"""
            UPDATE search SET site_favicon_uri = '{uri}' WHERE id = {varid};
        """   
        
        print (uri)
        
        cur.execute(sql)
        db.commit()
           
           
