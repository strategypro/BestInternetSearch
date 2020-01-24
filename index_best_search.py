#!/usr/bin/python3

import os
import sys

import cgi

import cgitb
OUTDIR = '/var/www/'
cgitb.enable(display=0, logdir=OUTDIR)

sys.path.insert(0, "/var/www")

from db_bestsearch import *
cur = db.cursor(MySQLdb.cursors.DictCursor)

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
        .items {{ margin: auto; width: 60%; }}
        .item {{ padding:5px; }}
        .link {{ color: black;text-decoration: none; }}
        .link:hover {{ color: blue; }}
    </style>
    
    <link rel="icon" type="image/png" sizes="32x32" href="https://{strDomain}/bestsearch/page_img/favicon.png">
    <script src="https://{strDomain}/bestsearch/js/jquery-3.4.1.min.js"></script>
    </head>
    <body>
    """
    
    html += f"""search results from ({q}) """
    
    cur.execute("SELECT count(id) from search;")
    row = cur.fetchone()      
    count = row['count(id)']
    
    cur.execute(f"""SELECT * from search WHERE LOWER(site_name) LIKE '%{q}%' ;""")
    res = cur.fetchall()   
    if res:
        html += f"""Under construction, <a href="https://{strDomain}">{domain_name}</a> created in 2020<br><br>"""

        html += f"""
        <div class="items">"""
        for i, row in enumerate(res, 1):
            address = row['site_address']
            name = row['site_name']
            html += f"""
            <div class="item"><span>({i})</span> <span style="font-size:small;"><a class="link" href="{address}">{address}</a></span><br>
            <a href="{address}">{name}</a></div>"""
        
        html += f"""
        </div>"""
    
    
    html += f"""    
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
                            this.input.value = suggestion.label;
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
    <div class="git_source_code"><a  href="https://github.com/strategypro/BestInternetSearch">source code</a></div>
<pre>
<h1><a href="https://{strDomain}">{domain_name}</a></h1>
</pre>

    <h1 class="center_title">{title}</h1>
    
    <br>
    
    <form id="search_form" action="/" method="get">
    <div style="white-space:nowrap"><input id="search_input" type="text" name="q"><img id="search_img" src="https://{strDomain}/bestsearch/page_img/search.png"></div>

    <input id="search_submit" type="submit" value="Search">
    </form> 

    </body>
    </html>
    """
    
if __name__ == '__main__':
    enc_print("Content-Type:text/html;charset=utf-8;")
    enc_print()
    enc_print(html)
