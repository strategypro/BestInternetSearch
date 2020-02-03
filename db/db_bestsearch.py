#!/usr/bin/python3

import MySQLdb

import psycopg2
import psycopg2.extras

db = MySQLdb.connect(host="127.0.0.1",        # your host, usually localhost
                     user="",                 # your username
                     passwd="",               # your password
                     db="best")               # name of the database


def get_advertisement_form_code():
    html = f"""
    
<form id="ad_form" target="paypal" action="https://www.paypal.com/cgi-bin/webscr" method="post" >
<input type="hidden" name="cmd" value="_s-xclick">
<table>
<tr><td><input type="hidden" name="on0" value="Number of Months to Advertise">Number of Months to Advertise</td></tr><tr><td><select name="os0">
	<option value="4 Months">4 Months $799.00 USD</option>
	<option value="6 Months">6 Months $995.00 USD</option>
	<option value="8 Months">8 Months $1,200.00 USD</option>
	<option value="1 year">1 year $2,000.00 USD</option>
</select> </td></tr>
</table>
<input type="hidden" name="encrypted" value="-----BEGIN PKCS7-----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-----END PKCS7-----">
<input type="image" src="https://bestinternetsearch.com/bestsearch/page_img/Advertise_with_BestInternetSearch.png" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
<img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">
</form>

"""

    return html    


HOST = '127.0.0.1'
DATABASE = 'dictionary'
USERNAME = ''
PASSWORD = ''
pg_database = psycopg2.connect("dbname=%s user=%s password=%s host=%s" % (DATABASE, USERNAME, PASSWORD, HOST))

