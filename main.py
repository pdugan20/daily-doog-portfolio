import cgi
import wsgiref.handlers
import os
import re
import os
import urllib
import json
import logging
import jinja2
import webapp2

from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.db import GqlQuery
from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# Global variable passed into empty templates  
emptyList = []

class ProjectEntry(db.Model):
  projectId = db.StringProperty()
  projectName = db.StringProperty()
  projectSummary = db.TextProperty()
  projectDates = db.StringProperty()
  projectCompany = db.StringProperty()
                    
class MainPage(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'emptyList': emptyList
    }
    path = jinja_environment.get_template('themes/templates/index.html')
    self.response.out.write(path.render(template_values))
    
class ProjectPage(webapp2.RequestHandler):
  def get(self):
    projectName = None   
    if self.request.get('projectName'):
      projectName = self.request.get('projectName')
    
    projectData = GqlQuery(
      "SELECT * FROM ProjectEntry WHERE projectId ='" + 
      str(projectName) + "'"
    )
    
    for project in projectData:
      projectName = project.projectName
      projectSummary = project.projectSummary
      projectDates = project.projectDates
      projectCompany = project.projectCompany
      
    template_values = {
      'projectName': projectName,
      'projectSummary': projectSummary,
      'projectDates': projectDates,
      'projectCompany': projectCompany
    }
    path = jinja_environment.get_template('themes/templates/project_view.html')
    self.response.out.write(path.render(template_values))
    
class BlogPage(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'emptyList': emptyList
    }
    path = jinja_environment.get_template('themes/templates/blog.html')
    self.response.out.write(path.render(template_values))
    
class AboutPage(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'emptyList': emptyList
    }
    path = jinja_environment.get_template('themes/templates/about.html')
    self.response.out.write(path.render(template_values))
    
class BooksPage(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'emptyList': emptyList
    }
    path = jinja_environment.get_template('themes/templates/books.html')
    self.response.out.write(path.render(template_values))

application = webapp2.WSGIApplication([
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
