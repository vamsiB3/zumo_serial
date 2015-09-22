from matplotlib.pyplot import *
from numpy import *

import os, os.path
import random
import string
import cherrypy

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
        <head>
        <link href="/static/css/style.css" rel="stylesheet">
        </head>
        <body>
        <form method="get" action="calibrate">
        <button type="submit">Calibrate</button>
        </form>
        <form method="get" action="kraussfunc">
        Kp:<br>
        <input type="text" name="Kp">
        <br>
        Ki:<br>
        <input type="text" name="Ki"><br>
        Kd:<br>
        <input type="text" name="Kd"><br>
        <br>
        <button type="submit">Run Test</button>
        </form>
        </body>
        </html>"""

    @cherrypy.expose
    def calibrate(self):
        return "calibrating now"

    @cherrypy.expose
    def kraussfunc(self, **kwargs):
        str_out = ''
        first = 1
        for key, val in kwargs.iteritems():
            if first:
                first = 0
            else:
                str_out += ', '
            str_out += '%s:%s' % (key, val)
        return str_out
    
    @cherrypy.expose
    def generate(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']


    @cherrypy.expose 
    def showimage(self): 
        cherrypy.response.headers['Content-Type']= "image/png" 
        f = open("sin.png", "rb") 
        contents = f.read() 
        f.close() 
        return contents 


    @cherrypy.expose 
    def visu(self, alph=1.0): 
        _header = """ 
            <html> 
            <head> 
            <title>Random notes</<title> 
            <link rel="stylesheet" type="text/css" href="/style.css"></link> 
            </head> 
            <body> 
            <div class="container">""" 
        _footer = """ 
            </div> 
            </body> 
            </html>""" 
        ioff() 
        x = arange(0, 10, 0.01) 
        alpha = float(alph) 
        subplot(1,2,1), plot(x, sin(alpha*x), '.-') 
        subplot(1,2,2), plot(x,sin(alpha*x*cos(alpha*x)), 'o-') 
        savefig("sin.png", dpi=96) 
        cherrypy.response.headers['Content-Type']= 'text/html' 
        page = [_header] 
        page.append('<img src="/showimage/" width="800" height="400" />' ) 
        page.append(_footer) 
        return page
            
if __name__ == '__main__':
     conf = {
         '/': {
             'tools.sessions.on': True, \
             'tools.staticdir.root': os.path.abspath(os.getcwd()), \
             },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './public'
             }
         }
     cherrypy.config.update(conf)
     cherrypy.config.update({'server.socket_host':'192.168.0.111'})
     cherrypy.quickstart(StringGenerator(), '/', conf)
     #cherrypy.quickstart()
