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

html = ''

domain = os.environ['HTTP_HOST'].lower()

title = ''
heading1 = ''

if domain == 'www.bestinternetsearch.com' or domain == 'bestinternetsearch.com':
    title = 'Best Internet Search'
    heading1 = 'BestInternetSearch.com'
elif domain == 'www.bestwwwsearch.com' or domain == 'bestwwwsearch.com':
    title = 'Best www Search'
    heading1 = 'BestwwwSearch.com'
elif domain == 'www.bestnetsearch.com' or domain == 'bestnetsearch.com':
    title = 'Best net Search'
    heading1 = 'BestnetSearch.com'

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

                    .items {{ margin: auto; width: 60%; }}
                    .item {{ padding:5px; }}
                    
                </style>
            `);
        }}
        else // Desktop
        {{
            document.write(
            `
                <style>
    
                    .items {{ margin: auto; width: 60%; }}
                    .item {{ padding:5px; }}
                    
                </style>
            `);
        }}
    </script>
    
    
    <link rel="icon" type="image/png" sizes="32x32" href="http://{domain}/bestsearch/page_img/favicon.png">
    <script src="http://{domain}/bestsearch/js/jquery-3.4.1.min.js"></script>
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
        html += f"""Under construction, <a href="http://{domain}">{heading1}</a> created in 2020<br><br>"""

        html += f"""
        <div class="items">"""
        for i, row in enumerate(res, 1):
            address = row['site_address']
            name = row['site_name']
            html += f"""
            <div class="item"><span>({i})</span> <a href="{address}">{name}</a></div>"""
        
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

                    .center_title {{
                        text-align: center;
                    }}
                    
                    #search_form {{
                        text-align: center;
                    }}
                    
                    #search_img {{
                        border-radius: 10px;
                        vertical-align:bottom;
                        border:1px solid grey;    
                    }}
                    
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
    
                    .center_title {{
                        text-align: center;
                    }}
                    
                    #search_form {{
                        text-align: center;
                    }}
                    
                    #search_img {{
                        border-radius: 10px;
                        vertical-align:bottom;
                        border:1px solid grey;    
                    }}
                    
                </style>
            `);
        }}
    </script>



    

    
    <link rel="icon" type="image/png" sizes="32x32" href="http://{domain}/bestsearch/page_img/favicon.png">
    <script src="http://{domain}/bestsearch/js/jquery-3.4.1.min.js"></script>
    
    <link rel="stylesheet" href="http://{domain}/bestsearch/js/awesomplete/awesomplete.css" />
    <script src="http://{domain}/bestsearch/js/awesomplete/awesomplete.min.js"></script>
    
    <script>    
        $(document).ready(function() {{

            $('#search_img').on('click',function() {{
                $('#search_submit').click();
            }});

        }});
    </script>
    
        <script>
            
            $(document).ready(function() {{
            
                var list = [];                                                                                 
                
                list.push({{label:"<h6 style='display:inline;'>suggestions - trending</h6>", value:"" }});
                list.push({{label:"EarthDay.Love", value:"http://EarthDay.Love" }}); 
                //list.push({{label:"TotalMart.US", value:"http://TotalMart.US" }}); 

                var autocomplete = new Awesomplete(document.querySelector("#search_input"), {{
                            list:list,
                            minChars: 2,
                            maxItems: 20,
                            sort: false,
                            replace: function(suggestion) {{
                                //suggestion.value
                                this.input.value = suggestion.label;
                            }}
                    }}
                    );
        
                $( "#search_input" ).focus(function() {{

                    autocomplete.list = list;                   
                    autocomplete.open();                   

                }});         
        
                $("#search_input").keyup(function(e) {{
                    
                    //if ( $(this).val().length < 2) {{
                    //    return;
                    //}}
                    
                    var code = (e.keyCode || e.which);  // get keycode of current keypress event
                    if(code == 37 || code == 38 || code == 39 || code == 40) {{  // it's an arrow key
                        return;
                    }}
                
                    $.get( "http://{domain}/bestsearch/py/autocomplete_best_search.py?q=" + $("#search_input").val(), function( data ) {{
                        
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
<pre>
<h1><a href="http://{domain}">{heading1}</a></h1>
</pre>

    <h1 class="center_title">{title}</h1>
    
    <br>
    
    <form id="search_form" action="/" method="get">
    <input id="search_input" type="text" name="q" style="height:35px"><img id="search_img" src="http://{domain}/bestsearch/page_img/search.png" >
    <br>
    <input id="search_submit" type="submit" value="Search">
    </form> 

    </body>
    </html>
    """
    


if __name__ == '__main__':
    enc_print("Content-Type:text/html;charset=utf-8;")
    enc_print()
    enc_print(html)
