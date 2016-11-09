#coding=UTF-8
'''
Created on Jan 7, 2011

@author: elvin
'''
import settings
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext import webapp
from core import TemplateAPI, User, UserAccess, UserPermissionAPI, Block, Blocks, SiteError
from photo import Photo, PhotoAPI


class PhotosView(TemplateAPI):
    
    def get(self):
        self.access_init()
        if self.access.check('photo_view'):
            try:
                photo = PhotoAPI(self)
                query = Photo.all()
                self.pager(query.count(), 15, '/gallery')
                photos = photo.get_photos([], True, 15, self.pager_offset(), 180, 120)
                data = {'title': 'GALLERY',
                        'photos': photos,
                        'pager': self.render_pager()}
                self.render_html('custom', 'custom_gallery_view', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

app =  webapp.WSGIApplication(
        [('/gallery', PhotosView),],
        debug=False)
'''def main():
    application = webapp.WSGIApplication(
        [('/gallery', PhotosView),],
        debug=False)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()'''