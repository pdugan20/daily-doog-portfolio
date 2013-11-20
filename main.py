import cgi
import wsgiref.handlers
import os
import re
import os
import urllib
import json
import jinja2
import webapp2
import logging

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
  projectDesignProcess = db.TextProperty()
  screenShotList = db.StringProperty()
  artifactList = db.StringProperty()
                    
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
      projectScreenShotList = project.screenShotList
      projectDesignProcess = project.projectDesignProcess
      projectId = project.projectId
      projectArtifactList = project.artifactList
    
    # used to create a new container for formatted screenshots
    finalScreenShotList = []
    
    if len(projectScreenShotList) > 0:
      projectScreenShotList = [e.encode('utf-8') for e in projectScreenShotList.split('-')]
      urlPath = './resources/images/portfolio/' + projectId + '/'
      for item in projectScreenShotList:
        currentItem = item.split(',')
        newThumb = urlPath + 'sm/' + currentItem[0] + '_sm.png'
        modShot = urlPath + currentItem[0] + '.png'
        currentScreenShotList = [currentItem[1], modShot, newThumb]
        finalScreenShotList.append(currentScreenShotList)
        
    # use for testing purposes only
    # logging.info(finalScreenShotList)
    
    artifactList = []
    if len(projectArtifactList) > 0:
      projectArtifactList = [e.encode('utf-8') for e in projectArtifactList.split('-')]
      for artifact in projectArtifactList:
        currentItem = artifact.split(',')
        currentArtifactList = [currentItem[0], currentItem[1], currentItem[2]]
        artifactList.append(currentArtifactList)  
         
    template_values = {
      'projectName': projectName,
      'projectSummary': projectSummary,
      'projectDates': projectDates,
      'projectCompany': projectCompany,
      'projectDesignProcess': projectDesignProcess,
      'finalScreenShotList': finalScreenShotList,
      'artifactList': artifactList
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
    if self.request.get('bookShelfId'):
      bookShelfId = self.request.get('bookShelfId')
    else:
      bookShelfId = '115429583296661000087' 
    if self.request.get('startIndex'):
      startIndex = self.request.get('startIndex')
    else:
      startIndex = 0    
    if self.request.get('maxResults'):
      maxResults = self.request.get('maxResults')
    else:
      maxResults = 15
      
    myBooksDict = {
      '7skCmLdArBEC': 'military',
      'x7nsvKqGpQQC': 'usmc',
      'w8pM72p_dpoC': 'design',
      'FN5wMOZKTYMC': 'fiction',
      'Iw_gHtk4ghYC': 'fiction',
      'ahNbAAAAMAAJ': 'fiction',
      'AZ5J6B1-4BoC': 'fiction',
      'xvpUIomo_NkC': 'usmc',
      'VZz-ZVliw34C': 'military',
      'UvK1Slvkz3MC': 'fiction',
      'Yz8Fnw0PlEQC': 'fiction',
      'WrL9de30FDMC': 'fiction'
    };
      
    booksApiKey = 'AIzaSyA8cv2udFuAiC6sK_GBi0dZcBYQM5daSYg'
    bookShelfUrl = 'https://www.googleapis.com/books/v1/users/' + \
    bookShelfId + \
    '/bookshelves/1001/volumes?' + \
    'maxResults=' + str(maxResults) + \
    '&startIndex=' + str(startIndex) + \
    '&country=US' + \
    '&key=' + booksApiKey
    
    # actual url
    # https://www.googleapis.com/books/v1/users/115429583296661000087/bookshelves/1001/volumes?maxResults=18&startIndex=0&country=US&key=AIzaSyA8cv2udFuAiC6sK_GBi0dZcBYQM5daSYg
    
    bookProfileUrl = 'http://books.google.com/books?uid=' + bookShelfId 
    
    # userAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    # headers = {'User-Agent':userAgent,}
    # request = urllib2.Request(bookShelfUrl, None, headers)
    # bookShelfJsonRaw = urllib2.urlopen(request)    
    
    # bookShelfJsonRaw = urllib.urlopen(bookShelfUrl)
    # bookShelfJsonObject = json.load(bookShelfJsonRaw) 
    # logging.info(bookShelfJsonRaw)  
    
    # enable for testing on localserver
    # bookShelfUrl = 'http://localhost:8080/resources/testing/bookshelf.json'
    
    # alternative to urllib
    bookShelfJsonRaw = urlfetch.fetch(bookShelfUrl)
    # logging.info(bookShelfJsonRaw.content)
    
    bookShelfJsonObject = json.loads(bookShelfJsonRaw.content)
    # logging.info(bookShelfJsonObject)
    
    totalBooksInLibrary = int(bookShelfJsonObject['totalItems'])
    totalBooksInLibrary = 0
      
    parsedBookShelf = bookShelfJsonObject['items']
    bookShelfPageCount = 0
    bookShelfCombinedRatings = 0.0
    bookShelfAvgPubYear = 0
    booksPerQuery = 12
    booksOnShelfList = []
    
    navLinkStart = 0
    navLinkCount = 0
    bookShelfNavLinks = [[navLinkCount, navLinkStart]]
    
    while navLinkStart <= totalBooksInLibrary:
      navLinkStart += booksPerQuery
      navLinkCount += 1
      linkList = [navLinkCount, navLinkStart]
      bookShelfNavLinks.append(linkList)
      
    currentViewList = [startIndex, (int(startIndex) + 12)]
    
    for bookDescriptionDict in parsedBookShelf:
      if bookDescriptionDict['volumeInfo']:
        try:
          bookTitle = bookDescriptionDict[
          'volumeInfo']['title'
          ]
          # if len(str(bookTitle)) > 30:
          #   bookTitle = (bookTitle[:28] + '...')
        except KeyError:
          bookTitle = 'No title info.'
        try:
          bookAuthors = bookDescriptionDict[
          'volumeInfo']['authors'
          ]
        except KeyError:
          bookAuthors = 'Unknown author.'
        try:
          bookPublishDate = bookDescriptionDict[
          'volumeInfo']['publishedDate'
          ]
        except KeyError:
          pass
        try:
          bookThumbnail = bookDescriptionDict[
          'volumeInfo']['imageLinks']['thumbnail'
          ]
          bookThumbnail = bookThumbnail.replace('&edge=curl', '')
        except KeyError:
          bookThumbnail = 'No thumbnail.'
        try:
          bookPreviewLink = bookDescriptionDict[
          'volumeInfo']['previewLink'
          ]
        except KeyError:
          bookPreviewLink = 'No preview link.'
        try:
          bookInfoLink = bookDescriptionDict[
          'volumeInfo']['infoLink'
          ]
        except KeyError:
          bookInfoLink = 'No information link.'
        try:
          bookDescription  = bookDescriptionDict[
          'volumeInfo']['description'
          ]
        except KeyError:
          bookDescription  = 'No description available.'
        try:
          bookPageCount  = bookDescriptionDict[
          'volumeInfo']['pageCount'
          ]
        except KeyError:
          pass
        try:
          bookPublisher  = bookDescriptionDict[
          'volumeInfo']['publisher'
          ]
        except KeyError:
          bookPublisher  = 'Unknown publisher.'
        try:
          bookId  = bookDescriptionDict[
          'id'
          ]
        except KeyError:
          id  = 'Unknown book id.'
        try:
          bookRating = bookDescriptionDict[
          'volumeInfo']['averageRating'
          ]
        except KeyError:
          booksPerQuery = booksPerQuery - 1
        
        try:  
          bookPublishDate = datetime.strptime(bookPublishDate, '%Y-%m-%d').date()
          # logging.info(bookPublishDate.year)
          bookPublishDate = str(bookPublishDate.year)
        except ValueError:
          pass
          
        try:
          myBookCategory = myBooksDict[bookId]
        except:
          myBookCategory = 'none'
        
        currentBook = [
          bookTitle,
          bookAuthors,
          bookPublishDate,
          bookThumbnail,
          bookPreviewLink,
          bookInfoLink,
          bookDescription,
          bookPageCount,
          bookPublisher,
          myBookCategory
        ]
                  
        booksOnShelfList.append(currentBook)
        bookShelfPageCount += bookPageCount
        bookShelfCombinedRatings += bookRating
        # bookShelfAvgPubYear += bookPublishDate
    
    bookShelfCombinedRatings = (bookShelfCombinedRatings/booksPerQuery)
    bookShelfCombinedRatings = ("%.2f" % bookShelfCombinedRatings)
    # bookShelfAvgPubYear = (bookShelfAvgPubYear/booksPerQuery)
    
    template_values = {
      'booksOnShelfList': booksOnShelfList,
      'bookShelfPageCount': bookShelfPageCount,
      'bookShelfCombinedRatings': bookShelfCombinedRatings,
      'bookShelfAvgPubYear': bookShelfAvgPubYear,
      'bookShelfNavLinks': bookShelfNavLinks,
      'currentViewList': currentViewList,
      'bookShelfJsonObject': bookShelfJsonObject
    }

    path = jinja_environment.get_template('themes/templates/books-new.html')
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