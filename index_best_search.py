#!/usr/bin/python3

import os
import sys

import cgi

import math

import cgitb
OUTDIR = '/var/www/'
cgitb.enable(display=0, logdir=OUTDIR)

sys.path.insert(0, "/var/www")

from db_bestsearch import *
cur = db.cursor(MySQLdb.cursors.DictCursor)

from urllib import parse
from html import escape

def enc_print(string='', encoding='utf8'):
    sys.stdout.buffer.write(string.encode(encoding) + b'\n')
    
def strHTMLredirect(redirectURL):
    html = f"""
    <!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url={redirectURL}" /></head>
    <body><noscript><meta http-equiv="refresh" content="0; url={redirectURL}" /></noscript></body>
    </html>
    """
    return html
    
    
html = ''

strDomain = os.environ['HTTP_HOST'].lower()

title = ''
domain_name = ''

if strDomain == 'www.bestinternetsearch.com' or strDomain == 'bestinternetsearch.com':
    title = 'Best Internet Search'
    domain_name = 'BestInternetSearch.com'
    if os.environ['HTTP_X_FORWARDED_PROTO'] == 'http':
        html = strHTMLredirect('https://bestinternetsearch.com')
        enc_print(html)
        sys.exit()
        
elif strDomain == 'www.bestwwwsearch.com' or strDomain == 'bestwwwsearch.com':
    title = 'Best www Search'
    domain_name = 'BestwwwSearch.com'
    if os.environ['HTTP_X_FORWARDED_PROTO'] == 'http':
        html = strHTMLredirect('https://bestwwwsearch.com')
        enc_print(html)
        sys.exit()
    
elif strDomain == 'www.bestnetsearch.com' or strDomain == 'bestnetsearch.com':
    title = 'Best net Search'
    domain_name = 'BestnetSearch.com'
    if os.environ['HTTP_X_FORWARDED_PROTO'] == 'http':
        html = strHTMLredirect('https://bestnetsearch.com')
        enc_print(html)
        sys.exit()





arguments = cgi.FieldStorage()
q = '' if not arguments.getvalue( "q" ) else escape( arguments.getvalue( "q" ) )
q = q.lower()


request_uri = os.environ['REQUEST_URI'].lower()

def process_request(request_uri, params=None):
    
    if "?" in request_uri:
        req_uri = request_uri.split("?")[1]

        if "&" in req_uri:
            page = req_uri.split("&")[0]
        else:
            page = req_uri
        
        params = dict(parse.parse_qsl(parse.urlsplit(request_uri).query))
    else:
        page = request_uri
    return page, params

page_req, params = process_request(request_uri)


page = '' if not arguments.getvalue( "page" ) else escape( arguments.getvalue( "page" ) )
if page == "":                                                                        
    page = "1"                                                                        
else:                                                                                 
    if not page.isnumeric():                                                          
        page = "1"                                                                    
    elif not int(page) > 0:                                                           
        page = "1"



if page_req == 'finance':
    q = '*'
    page = 17
    
    

if not q == '':
    
    html += f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>{title}</title>
    
    <script>
        if (/Mobi/i.test(navigator.userAgent) || /Android/i.test(navigator.userAgent))
        {{
            document.write(
            `
                <style>
                    a {{ font-size:200%;}}
                    
                    #pagination {{margin-left:5px;white-space: nowrap;}}
                    
                </style>
            `);
        }}
        else // Desktop
        {{
            document.write(
            `
                <style>
                
                    #pagination {{margin:auto;width:60%;}}
                    
                </style>
            `);
        }}
    </script>
    
    <style>
         /* Mobile and Desktop */
        .items {{ margin: auto; width: 60%; }}
        .item {{ padding:5px; }}
        .link {{ color: black;text-decoration: none; }}
        .link:hover {{ color: blue; }}
        .active {{ color:black;text-decoration:none; }}
        .active_b {{ color:blue; }}
        .paginationlinks {{ font-size:200%; }}
        .nextprevious {{ color:#23ceec;text-decoration:none; }}
    </style>
    
    <link rel="icon" type="image/png" sizes="32x32" href="https://{strDomain}/bestsearch/page_img/favicon.png">
    <script src="https://{strDomain}/bestsearch/js/jquery-3.4.1.min.js"></script>
    </head>
    <body>
    """
    
    #html += f"""search results from ({q}) """
    
    limit = 10; # results per page
    
    total_records=0
    
    if q == '*':
        sql = f"""SELECT count(id) from search"""
        
        cur.execute(sql)
        row = cur.fetchone()      
        total_records = row['count(id)']
        
    else:
        sql = f"""SELECT count(id) from search WHERE LOWER(site_name) LIKE '%{q}%' OR LOWER(site_title) LIKE '%{q}%' ;"""
    
        sql2 = f"""SELECT count(search.id) FROM search INNER JOIN 
        (SELECT * from keywords WHERE LOWER(keyword) LIKE '%{q}%') AS keywords ON search.id = keywords.fk_search_id ; 
        """
        
        cur.execute(sql)
        row = cur.fetchone()      
        total_records = row['count(id)']

        cur.execute(sql2)
        row = cur.fetchone()      
        total_records += row['count(search.id)']
    
    total_pages = math.ceil(int(total_records) / int(limit))
    start_from = (int(page)-1) * limit 
    
    
    if q == '*':
        sql = f"""SELECT * from search ORDER BY id ASC LIMIT {start_from}, {limit}""";
    
        cur.execute(sql)
        res = cur.fetchall()
    
        results = [res]
    
    else:
        sql = f"""SELECT * from search WHERE LOWER(site_name) LIKE '%{q}%' OR LOWER(site_title) LIKE '%{q}%' ORDER BY id ASC LIMIT {start_from}, {limit} ;"""
    
        sql2 = f"""SELECT * FROM search INNER JOIN 
        (SELECT * from keywords WHERE LOWER(keyword) LIKE '%{q}%') AS keywords ON search.id = keywords.fk_search_id ; 
        """
        
        cur.execute(sql)
        res = cur.fetchall()
        
        cur.execute(sql2)
        res2 = cur.fetchall()       
    
        results = [res, res2]
        
    html += f"""<a href="https://{strDomain}">{domain_name}</a> created in 2020<br><br>"""
    for res_items in results:
    
        if res_items:
            

            html += f"""
            <div class="items">"""
            for row in res_items:
                address = row['site_address']
                name = row['site_name']
                title = row['site_title']
                uri = row['site_favicon_uri']
                
                favicon = ''
                
                #if uri != '':
                #    favicon = f""" ( <img style="vertical-align:bottom;width:20px" src="{uri}"> ) """
                    
                html += f"""
                <div class="item"><span style="font-size:small;"><a class="link" href="{address}">{address}</a></span>  <br> 
                <a href="{address}">{name}</a> {title} {favicon}</div>"""
            
            html += f"""
            </div>
            
            <div style="margin-top:20px"></div>
            
            """
        else:
            html += f""" no results for keyword(s) ( {q} )
            <br>
            <br>
            May I ask something from you?  How about a Wiki style, add a (favorite) link:
            <br>
            <br>
            <form id="add_a_link" method="post" action="https://{strDomain}/bestsearch/py/add_a_link.py">
                Site url address: <input type="text" id="send_good_link" name="url" value="http:// or https://" style="width:75%"><br>
                <br>
                <br>
                Suggest Title: <input type="text" name="title" style="width:50%">

                <input type="hidden" name="keywords" value="{q}">
                <br>
                <input id="send_good_link_submit" type="submit" value="Send">
            </form>
            <br>        
            If it's a good link (having good content), it will be approved and it will be added to the search results.  Thanks, the world benefits in a positive way from your help.
            <script>
                $("#send_good_link").focus(function() {{
                    $(this).val('');
                }});
                
                $('#send_good_link_submit').click(function(e){{
                    e.preventDefault();

                var form = $('#add_a_link');
                var action = form.attr('action');
                var data = form.serialize();

                $.ajax({{
                    type: 'POST',
                    url: action,
                    data: data,
                    success: function (data) {{
                        alert('form was sent: ' + data);
                    }}
                }});
                    
                }});
            </script>
            """
        
    html += f"""<div id="pagination">"""
    
    start = 1
    total = 10
    total_pages = total_pages
    page = int(page)
    
    if not q == '*':
        if page < total:
            total = total_pages
    
    if page >= 5:
        start = start + (page - 5)
        total = total + (page - 5)
        
        if total > total_pages:
            total = total_pages


    if page > 1:
        i = page - 1
        html += f"""<a class="nextprevious" href="/?q={q}&page={i}"><span>Previous</span> <span class="paginationlinks"">«</span></a>"""
    
    for i in range( start, total+1 ):
    
        if i == page:
            html +=  f"""<a class="active" href="/?q={q}&page={i}"><span class="active_b">[</span> {i} <span class="active_b">]</span></a>"""
        else:
            html +=  f"""<a href="/?q={q}&page={i}">[ {i} ]</a>""" 

    if total_pages > page:
        i=page+1
        html += f"""<a class="nextprevious" href="/?q={q}&page={i}"><span class="paginationlinks">»</span> <span>Next</span></a> """
    
    #html += f""" of {total_records} results"""
    
    html += f""" 
    </div>
    
    </body>
    </html>
    """
    
    
else:
    html += f"""    
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>{title}</title>

    <script>
        if (/Mobi/i.test(navigator.userAgent) || /Android/i.test(navigator.userAgent))
        {{
            document.write(
            `
                <style>
                    
                    #search_input {{
                        font-size: 150%;
                    }}
                    
                    #search_submit {{
                        font-size: 200%;
                    }}
                    
                </style>
            `);
        }}
        else // Desktop
        {{
            document.write(
            `
                <style>
    
                </style>
            `);
        }}
    </script>
    
    <style>
         /* Mobile and Desktop */

        html {{
            height: 100%;
        }}

        body {{
            position: relative;
            min-height: 100%;
        }}
        
        .center_title {{
            text-align: center;
        }}
        
        #search_form {{
            text-align: center;
        }}
         
        #search_input {{
            width:600px;
            height:35px;
        }}
        
        #search_img {{
            border-radius: 10px;
            vertical-align:bottom;
            border:1px solid grey;    
        }}
        
        .git_source_code {{
            text-align: right;
        }}  
        
        .interesting {{
            position: absolute;
            bottom: 0;
            left: 0;
            padding: 1rem;
            background-color: #efefef;
            text-align: center;
        }}
        
    </style>
    
    
    <link rel="icon" type="image/png" sizes="32x32" href="https://{strDomain}/bestsearch/page_img/favicon.png">
    <script src="https://{strDomain}/bestsearch/js/jquery-3.4.1.min.js"></script>
    
    <link rel="stylesheet" href="https://{strDomain}/bestsearch/js/awesomplete/awesomplete.css" />
    <script src="https://{strDomain}/bestsearch/js/awesomplete/awesomplete.min.js"></script>
    
    <script>    
        $(document).ready(function() {{
        
            $('#search_img').on('click',function() {{
                $('#search_submit').click();
            }});
            
        }});


        $(document).ready(function() {{
        
            var list = [];                                                                                 
            
            list.push({{label:"<h6 style='display:inline;'>suggestions - trending</h6>", value:"" }});
            list.push({{label:"EarthDay.Love", value:"https://EarthDay.Love" }}); 
            //list.push({{label:"TotalMart.US", value:"https://TotalMart.US" }}); 
            list.push({{label:"*", value:"all" }}); 

            var autocomplete = new Awesomplete(document.querySelector("#search_input"), {{
                        list:list,
                        minChars: 2,
                        maxItems: 20,
                        sort: false,
                        replace: function(suggestion) {{
                            //suggestion.value
                            if (suggestion.label == "<h6 style='display:inline;'>suggestions - trending</h6>") {{
                                suggestion.label = '';
                            }}
                            
                            var findit = suggestion.label.indexOf("--");
                            var len_label = suggestion.label.length;
                            if ( findit != -1){{
                                
                                var val = $( "#search_input" ).val();
                                if (  suggestion.label.substring(0,findit).toLowerCase().trim() == val.toLowerCase() ) {{
                                    this.input.value = suggestion.label.substring(0,findit-1);
                                }}
                                else {{
                                    this.input.value = suggestion.label.substring(findit + 3, len_label).trim();
                                }}
                            }}
                            else {{
                                this.input.value = suggestion.label;
                            }}
                        }}
                }}
                );
    
            $( "#search_input" ).val('  ');
    
            $( "#search_input" ).focus(function() {{
                
                autocomplete.list = list;                   
                autocomplete.open();                   
                $( this ).val('');
            }});         
    
            $("#search_input").keyup(function(e) {{
                
                if ( $(this).val().length < 2) {{
                    return;
                }}
                
                var code = (e.keyCode || e.which);  // get keycode of current keypress event
                if(code == 37 || code == 38 || code == 39 || code == 40) {{  // it's an arrow key
                    return;
                }}
            
                $.get( "https://{strDomain}/bestsearch/py/autocomplete_best_search.py?q=" + $("#search_input").val(), function( data ) {{
                    
                            var data = JSON.parse( data.trim() );				 
                            var list = [];                                                                                 
                            for (var i=0; i<data.length; i++) {{
                                list.push({{label:data[i].label, value:data[i].value }})
                            }}
                            
                            autocomplete.list = list;
                            
                }});
                
            }});     
    
        }});
    </script>    
    
    </head>
    <body>
    <div class="git_source_code"><a href="https://github.com/strategypro/BestInternetSearch" title="100% open source ❤">source code</a></div>
<pre>
<h1><a href="https://{strDomain}">{domain_name}</a></h1>
</pre>

    <h1 class="center_title">{title}</h1>
    
    <br>
    
    <form id="search_form" action="/" method="get">
    <div style="white-space:nowrap"><input id="search_input" type="text" name="q"><img id="search_img" src="https://{strDomain}/bestsearch/page_img/search.png"></div>

    <input id="search_submit" type="submit" value="Search">
    </form> 


    <div class="interesting">Interesting: <a href="https://videoflicktube.com/" title="VideoFlickTube.com - A video website, 100% open source ❤"><img src="https://{strDomain}/bestsearch/page_img/videoflicktube.png" /></a> 
    <a id="ad_img_a" href="#" title="Purchase Advertising (url_address, title, description (optional), and relevant keywords up to 40) ad will be displayed among search results labeled as an ad in the top search results 1 or 2 pages depending on amount of Internet material within BestInternetSearch on relevant keywords (Click Advertise to select advertisement duration to purchase)">
    <img id="ad_img" src="https://bestinternetsearch.com/bestsearch/page_img/Advertise_with_BestInternetSearch_purchase.png" />
    </a>

    """
    
    html += get_advertisement_form_code()
    
    html += f"""

    <script>
    $("#ad_form").hide();
    
    $("#ad_img").click(function(){{
        $("#ad_form").toggle();
     }});
    
    $("#ad_img_a").click(function(e){{
        e.preventDefault();
     }});    
    </script>
    
    </div>   
    </body>
    </html>
    """
    
if __name__ == '__main__':
    enc_print("Content-Type:text/html;charset=utf-8;")
    enc_print()
    enc_print(html)
