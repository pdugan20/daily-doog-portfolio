import cgi
import wsgiref.handlers
import os
import re
import os
import urllib
import json
import logging

from datetime import datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.db import GqlQuery
from google.appengine.api import urlfetch
                    
class MainPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'themes/templates/index.html')
    template_values = None
    self.response.out.write(template.render(path, template_values))
    
class ProjectPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'themes/templates/project_view.html')
    template_values = None
    self.response.out.write(template.render(path, template_values))
    
class BlogPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'themes/templates/blog.html')
    template_values = None
    self.response.out.write(template.render(path, template_values))
    
class AboutPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'themes/templates/about.html')
    template_values = None
    self.response.out.write(template.render(path, template_values))
    
class BooksPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'themes/templates/books.html')
    template_values = None
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
  ('/project', ProjectPage),
  ('/blog', BlogPage),
  ('/portfolio', MainPage),
  ('/books', BooksPage),
  ('/', AboutPage)
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
