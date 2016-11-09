#coding=UTF-8
'''
Created on Jan 7, 2011

@author: elvin
'''

import settings
import urllib
import time
import datetime
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext import webapp
from core import TemplateAPI, User, UserAccess, UserPermissionAPI, Block, Blocks, SiteError


class Photo(db.Model):
    
    photo = blobstore.BlobReferenceProperty()
    description = db.StringProperty(multiline=True)   
    published = db.BooleanProperty(default=True, required=True)
    owner = db.ReferenceProperty(User, collection_name='photo_owners', required=True)
    created = db.DateTimeProperty(auto_now_add=True, required=True)
    updated = db.DateTimeProperty(auto_now=True, required=True)

    
class PhotoAdd(TemplateAPI):
    
    def get(self):
        self.access_init()
        if self.access.check('photo_add'):
            data = {'title': settings.photo_add_title,
                    'submit_url': blobstore.create_upload_url(self.get_redirect(settings.photo_save_url)),
                    'cancel_url': self.get_redirect(settings.photo_add_redirect_url)}
            self.render_html('photo', 'photo_add_form', data)
        else:
            self.render_error(403)


class PhotoSave(blobstore_handlers.BlobstoreUploadHandler):
    
    def post(self):
        unsupported_resolution = False
        access = UserAccess(self.request.cookies)
        if access.check('photo_add'):
            photos = self.get_uploads('photo')
            blob_info = photos[0]
            if blob_info.content_type in settings.photo_allowed_types:
                incorrect_type = False
            elif 'all' in settings.photo_allowed_types:
                incorrect_type = False
            else:
                incorrect_type = True
            if not incorrect_type:
                try:
                    img = images.Image(blob_key=str(blob_info.key()))
                    img.im_feeling_lucky()
                    img.execute_transforms(output_encoding=images.JPEG, quality=1)
                    if img.width >= img.height:
                        if img.width < settings.photo_low_limit_width:
                            unsupported_resolution = True
                        elif img.width > settings.photo_high_limit_width:
                            unsupported_resolution = True
                        else:
                            unsupported_resolution = False
                    elif img.width < img.height:
                        if img.height < settings.photo_low_limit_height:
                            unsupported_resolution = True
                        elif img.height > settings.photo_high_limit_height:
                            unsupported_resolution = True
                        else:
                            unsupported_resolution = False
                except:
                    pass
            if blob_info.size > settings.photo_max_upload_size:
                blobstore.delete(blob_info.key())
                if self.request.get('frame'):
                    self.redirect('%s?frame=%s' % (settings.photo_error_url_string % settings.photo_errors['oversize']['path'], self.request.get('frame')))
                else:
                    self.redirect(settings.photo_error_url_string % settings.photo_errors['oversize']['path'])
            elif incorrect_type:
                blobstore.delete(blob_info.key())
                if self.request.get('frame'):
                    self.redirect('%s?frame=%s' % (settings.photo_error_url_string % settings.photo_errors['incorrect_type']['path'], self.request.get('frame')))
                else:
                    self.redirect(settings.photo_error_url_string % settings.photo_errors['incorrect_type']['path'])
            elif unsupported_resolution:
                blobstore.delete(blob_info.key())
                if self.request.get('frame'):
                    self.redirect('%s?frame=%s' % (settings.photo_error_url_string % settings.photo_errors['unsupported_resolution']['path'], self.request.get('frame')))
                else:
                    self.redirect(settings.photo_error_url_string % settings.photo_errors['unsupported_resolution']['path'])
            else:
                photo_reference = blob_info.key()
                description = unicode(self.request.get('description'))
                published = bool(self.request.get('published'))
                owner = access.current_user
                photo = Photo(photo=photo_reference, description=description, published=published, owner=owner)
                photo.put()
                if self.request.get('frame'):
                    self.redirect('%s?frame=%s' % (settings.photo_save_redirect_url, self.request.get('frame')))
                else:
                    self.redirect(settings.photo_save_redirect_url)
        else:
            if self.request.query_string:
                self.redirect('%s?frame=%s' % (settings.photo_error_url_string % settings.photo_error_forbidden_type, self.request.get('frame')))
            else:
                self.redirect(settings.photo_error_url_string % settings.photo_error_forbidden_type)


class PhotoEdit(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('photo_edit'):
            try:
                photo = Photo.get_by_id(int(id))
                self.manipulator.formater(photo, [{'name': 'description', 'type': 'unicode'}])
                data = {'title': settings.photo_edit_title,
                        'photo': photo,
                        'src': self.get_redirect(settings.photo_output_url_string % str(photo.photo.key()), 'add_multi', [{'query': 'width', 'value': settings.photo_s_w}, {'query': 'height', 'value': settings.photo_s_h}]),
                        'submit_url': self.get_redirect(settings.photo_edit_url_string % str(photo.key().id())),
                        'cancel_url': self.get_redirect(settings.photo_edit_redirect_url),}
                self.render_html('photo', 'photo_edit_form', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
        
    def post(self, id):
        self.access_init()
        if self.access.check('photo_edit'):
            try:
                photo = Photo.get_by_id(int(id))
                photo.description = unicode(self.request.get('description'))
                photo.published = bool(self.request.get('published'))
                photo.put()
                self.redirect_to(settings.photo_edit_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

        
class PhotoDelete(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('photo_delete'):
            try:
                photo = Photo.get_by_id(int(id))
                self.manipulator.formater(photo, [{'name': 'description', 'type': 'unicode'}])
                data = {'title': settings.photo_delete_title,
                        'photo': photo,
                        'delete_question': settings.photo_delete_form_label_question,
                        'src': self.get_redirect(settings.photo_output_url_string % str(photo.photo.key()), 'add_multi', [{'query': 'width', 'value': settings.photo_s_w}, {'query': 'height', 'value': settings.photo_s_h}]),
                        'submit_url': self.get_redirect(settings.photo_delete_url_string % str(photo.key().id())),
                        'cancel_url': self.get_redirect(settings.photo_delete_redirect_url)} 
                self.render_html('photo', 'photo_delete_form', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
        
    def post(self, id):
        self.access_init()
        if self.access.check('photo_delete'):
            try:
                photo = Photo.get_by_id(int(id))
                blobstore.delete(photo.photo.key())
                photo.delete()
                self.redirect_to(settings.photo_delete_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

            
class PhotoManagement(TemplateAPI):

    def get(self):
        self.access_init()
        if self.access.check('photo_edit') or self.access.check('photo_delete'):
            query = Photo.all()
            query.order('-created')
            self.pager(query.count(), settings.photos_per_page, settings.photo_management_url)
            photos = query.fetch(settings.photos_per_page, self.pager_offset())
            photos_extended = []
            for photo in photos:
                self.manipulator.formater(photo, [{'name': 'description', 'type': 'unicode'}]) 
                photo.src = self.get_redirect(settings.photo_output_url_string % str(photo.photo.key()), 'add_multi', [{'query': 'width', 'value': settings.photo_s_w}, {'query': 'height', 'value': settings.photo_s_h}])
                photo.view_url = self.get_redirect(settings.photo_view_url_string % str(photo.key().id()))
                photo.edit_url = self.get_redirect(settings.photo_edit_url_string % str(photo.key().id()))
                photo.delete_url = self.get_redirect(settings.photo_delete_url_string % str(photo.key().id()))
                photos_extended.append(photo)
            data = {'title': settings.photo_management_title,
                    'photos': photos_extended,
                    'pager': self.render_pager(),
                    'settings' : settings,
                    'add_url': self.get_redirect(settings.photo_add_url),
                    'permissions_url': self.get_redirect(settings.photo_permissions_url),
                    'photo_add': self.access.check('photo_add'),
                    'photo_edit': self.access.check('photo_edit'),
                    'photo_delete': self.access.check('photo_delete'),
                    'photo_permissions': self.access.admin_user}
            self.render_html('photo', 'photo_management_form', data)
        else:
            self.render_error(403)


class PhotoPermissions(UserPermissionAPI):
    
    def get(self):
        self.get_form(permissions=['photo_view', 'photo_add', 'photo_edit', 'photo_delete'], url=settings.photo_permissions_url, title=settings.photo_permissions_title)
        
    def post(self):
        values = self.request.get_all('user-permissions')
        self.save_permissions(permissions=['photo_view', 'photo_add', 'photo_edit', 'photo_delete'], values=values, url=settings.photo_permissions_url)


class PhotoView(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('photo_view') or self.access.check('photo_edit') or self.access.check('photo_delete'):
            try:
                photo = Photo.get_by_id(int(id))
                if photo.published or self.access.check('photo_edit') or self.access.check('photo_delete'):
                    self.manipulator.formater(photo, [{'name': 'description', 'type': 'unicode'}])
                    src = self.get_redirect(settings.photo_output_url_string % str(photo.photo.key()))
                    data = {'title': photo.description_formated,
                            'photo': photo,
                            'src': src,
                            'like_url': self.get_redirect(settings.photo_view_url_string % str(photo.key().id()))}
                    self.render_html('photo', 'photo_view', data)
                else:
                    self.render_error(404)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
                       
            
class PhotoAPI():
    
    def __init__(self, templateapi):
        self.templateapi = templateapi
    
    def get_photo(self, key, published_filter = True, src_width = settings.photo_s_w, src_height = settings.photo_s_h):
        if key:
            try:
                photo = Photo.get(key)
                if (published_filter and photo.published) or not published_filter:
                    self.templateapi.manipulator.formater(photo, [{'name': 'description', 'type': 'unicode'}])
                    if settings.photo_get_serving_url:
                        if src_width > src_height:
                            src_size = src_width
                        else:
                            src_size = src_height
                        photo.src = images.get_serving_url(photo.photo.key(), src_size)
                        photo.view_url = images.get_serving_url(photo.photo.key(), settings.photo_l)
                    else:
                        photo.src = self.templateapi.get_redirect(settings.photo_output_url_string % str(photo.photo.key()), 'add_multi', [{'query': 'width', 'value': src_width}, {'query': 'height', 'value': src_height}])
                        photo.view_url = self.templateapi.get_redirect(settings.photo_output_url_string % str(photo.photo.key()), 'add_multi', [{'query': 'width', 'value': settings.photo_l_w}, {'query': 'height', 'value': settings.photo_l_h}])
                    photo.like_url = self.templateapi.get_redirect(settings.photo_view_url_string % str(photo.key().id()))
                    return photo
                else:
                    return None
            except:
                return None
        return None
    
    def get_photos(self, keys, published_filter = True, limit = settings.photos_per_page, offset = 0, src_width = settings.photo_s_w, src_height = settings.photo_s_h):
        try:
            if keys:
                photos = Photo.get(keys[offset:limit + offset])
            else:
                query = Photo.all()
                query.order('-created')
                photos = query.fetch(limit, offset)
            photos_extended = []
            for photo in photos:
                if (published_filter and photo.published) or not published_filter:
                    self.templateapi.manipulator.formater(photo, [{'name': 'description', 'type': 'unicode'}])
                    if settings.photo_get_serving_url:
                        if src_width > src_height:
                            src_size = src_width
                        else:
                            src_size = src_height
                        photo.src = images.get_serving_url(photo.photo.key(), src_size)
                        photo.view_url = images.get_serving_url(photo.photo.key(), settings.photo_l)
                    else:
                        photo.src = self.templateapi.get_redirect(settings.photo_output_url_string % str(photo.photo.key()), 'add_multi', [{'query': 'width', 'value': src_width}, {'query': 'height', 'value': src_height}])
                        photo.view_url = self.templateapi.get_redirect(settings.photo_output_url_string % str(photo.photo.key()), 'add_multi', [{'query': 'width', 'value': settings.photo_l_w}, {'query': 'height', 'value': settings.photo_l_h}])
                    photo.like_url = self.templateapi.get_redirect(settings.photo_view_url_string % str(photo.key().id()))
                    photos_extended.append(photo)
            return photos_extended
        except:
            return None
        
            
class PhotoOutput(webapp.RequestHandler):
    
    def get(self, key):
        try:
            key = str(urllib.unquote(key))
            
            if key:
               blobwo = blobstore.BlobInfo.get(key)
               if blobwo:
                  typex = blobwo.content_type
                  if typex not in ['image/jpeg', 'image/png', 'image/jpe']:
                     blob_reader = blobstore.BlobReader(blobwo.key()) 
                     self.response.headers['Content-Type'] = 'image/gif'
                     self.response.headers['Cache-Control'] = 'public, max-age=31536000'
                     future = datetime.datetime.fromtimestamp(time.time() + 31536000)
                     future_date = datetime.datetime(future.year, future.month, future.day)
                     self.response.headers['Expires'] = future_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
                     self.response.out.write(blob_reader.read())
                     return
                     
                     
            
            width = self.request.get('width')
            height = self.request.get('height')
            if width:
                if int(width) <= settings.photo_max_width:
                    width = int(width)
                else:
                    width = settings.photo_max_width
            else:
                width = settings.photo_default_width
            if height:
                if int(height) <= settings.photo_max_height:
                    height = int(height)
                else:
                    height = settings.photo_max_height
            else:
                height = settings.photo_default_height
            photo = images.Image(blob_key=key)
            photo.resize(width=width, height=height)
            enc = images.JPEG
            o = 'image/jpeg'
            blobwo = blobstore.BlobInfo.get(key)
            if blobwo.content_type not in ['image/png', 'image/jpeg', 'image/jpe']:
                enc = images.GIF
                o = 'image/gif'
                
                
            photo = photo.execute_transforms(output_encoding=enc, quality=settings.photo_quality)
            self.response.headers['Content-Type'] = o
            self.response.headers['Cache-Control'] = 'public, max-age=31536000'
            future = datetime.datetime.fromtimestamp(time.time() + 31536000)
            future_date = datetime.datetime(future.year, future.month, future.day)
            self.response.headers['Expires'] = future_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
            self.response.out.write(photo)
        except Exception, e:
            import logging
            logging.info(e)
            self.redirect(settings.site_error_url_string % '404')
            
            
class PhotoError(TemplateAPI):
    
    def get(self, path):
        if settings.photo_errors['photo_errors_url_types'].has_key(path):
            type = settings.photo_errors['photo_errors_url_types'][path]
            title = settings.photo_errors[type]['title']
            error_message = settings.photo_errors[type]['message']
            self.render_error(403, title, error_message)
        else:
            self.render_error(404)

app = webapp.WSGIApplication(
        [(settings.photo_error_url, PhotoError),
        (settings.photo_permissions_url, PhotoPermissions),
        (settings.photo_management_url, PhotoManagement),
        (settings.photo_add_url, PhotoAdd),
        (settings.photo_save_url, PhotoSave),
        (settings.photo_edit_url, PhotoEdit),
        (settings.photo_delete_url, PhotoDelete),
        (settings.photo_view_url, PhotoView),
        (settings.photo_output_url, PhotoOutput),],
        debug=True)
'''def main():
    application = webapp.WSGIApplication(
        [(settings.photo_error_url, PhotoError),
        (settings.photo_permissions_url, PhotoPermissions),
        (settings.photo_management_url, PhotoManagement),
        (settings.photo_add_url, PhotoAdd),
        (settings.photo_save_url, PhotoSave),
        (settings.photo_edit_url, PhotoEdit),
        (settings.photo_delete_url, PhotoDelete),
        (settings.photo_view_url, PhotoView),
        (settings.photo_output_url, PhotoOutput),],
        debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()'''