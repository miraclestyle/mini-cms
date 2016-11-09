#coding=UTF-8
'''
Created on Jan 7, 2011

@author: elvin
'''

import settings
import urllib
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext import webapp
from core import TemplateAPI, User, UserAccess, UserPermissionAPI, Block, Blocks, SiteError


class File(db.Model):
    
    file = blobstore.BlobReferenceProperty()
    title = db.StringProperty(multiline=False, required=True)
    published = db.BooleanProperty(default=True, required=True)
    owner = db.ReferenceProperty(User, collection_name='file_owners', required=True)
    created = db.DateTimeProperty(auto_now_add=True, required=True)
    updated = db.DateTimeProperty(auto_now=True, required=True)

    
class FileAdd(TemplateAPI):
    
    def get(self):
        self.access_init()
        if self.access.check('file_add'):
            data = {'title': settings.file_add_title,
                    'submit_url': blobstore.create_upload_url(self.get_redirect(settings.file_save_url)),
                    'cancel_url': self.get_redirect(settings.file_add_redirect_url)}
            self.render_html('file', 'file_add_form', data)
        else:
            self.render_error(403)


class FileSave(blobstore_handlers.BlobstoreUploadHandler):
    
    def post(self):
        access = UserAccess(self.request.cookies)
        if access.check('file_add'):
            files = self.get_uploads('file')
            blob_info = files[0]
            if blob_info.content_type in settings.file_allowed_types:
                incorrect_type = False
            elif 'all' in settings.file_allowed_types:
                incorrect_type = False
            else:
                incorrect_type = True
            if blob_info.size > settings.file_max_upload_size:
                blobstore.delete(blob_info.key())
                if self.request.get('frame'):
                    self.redirect('%s?frame=%s' % (settings.file_error_url_string % settings.file_error_oversize_type, self.request.get('frame')))
                else:
                    self.redirect(settings.file_error_url_string % settings.file_error_oversize_type)
            elif incorrect_type:
                blobstore.delete(blob_info.key())
                if self.request.get('frame'):
                    self.redirect('%s?frame=%s' % (settings.file_error_url_string % settings.file_error_incorrect_type_type, self.request.get('frame')))
                else:
                    self.redirect(settings.file_error_url_string % settings.file_error_incorrect_type_type)
            else:
                file_reference = blob_info.key()
                title = unicode(self.request.get('title'))
                published = bool(self.request.get('published'))
                owner = access.current_user
                file = File(file=file_reference, title=title, published=published, owner=owner)
                file.put()
                if self.request.get('frame'):
                    self.redirect('%s?frame=%s' % (settings.file_save_redirect_url, self.request.get('frame')))
                else:
                    self.redirect(settings.file_save_redirect_url)
        else:
            if self.request.query_string:
                self.redirect('%s?frame=%s' % (settings.file_error_url_string % settings.file_error_forbidden_type, self.request.get('frame')))
            else:
                self.redirect(settings.file_error_url_string % settings.file_error_forbidden_type)


class FileEdit(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('file_edit'):
            try:
                file = File.get_by_id(int(id))
                self.manipulator.formater(file, [{'name': 'title', 'type': 'unicode', 'trim': settings.file_title_trimmed}])
                data = {'title': settings.file_edit_title,
                        'file': file,
                        'src': self.get_redirect(settings.file_output_url_string % (str(file.file.key()), str(file.file.filename))),
                        'submit_url': self.get_redirect(settings.file_edit_url_string % str(file.key().id())),
                        'cancel_url': self.get_redirect(settings.file_edit_redirect_url),}
                self.render_html('file', 'file_edit_form', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
        
    def post(self, id):
        self.access_init()
        if self.access.check('file_edit'):
            try:
                file = File.get_by_id(int(id))
                file.title = unicode(self.request.get('title'))
                file.published = bool(self.request.get('published'))
                file.put()
                self.redirect_to(settings.file_edit_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

        
class FileDelete(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('file_delete'):
            try:
                file = File.get_by_id(int(id))
                self.manipulator.formater(file, [{'name': 'title', 'type': 'unicode', 'trim': settings.file_title_trimmed}])
                data = {'title': settings.file_delete_title,
                        'file': file,
                        'delete_question': settings.file_delete_form_label_question_string % file.title_formated,
                        'src': self.get_redirect(settings.file_output_url_string % (str(file.file.key()), str(file.file.filename))),
                        'submit_url': self.get_redirect(settings.file_delete_url_string % str(file.key().id())),
                        'cancel_url': self.get_redirect(settings.file_delete_redirect_url)} 
                self.render_html('file', 'file_delete_form', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
        
    def post(self, id):
        self.access_init()
        if self.access.check('file_delete'):
            try:
                file = File.get_by_id(int(id))
                blobstore.delete(file.file.key())
                file.delete()
                self.redirect_to(settings.file_delete_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

            
class FileManagement(TemplateAPI):

    def get(self):
        self.access_init()
        if self.access.check('file_edit') or self.access.check('file_delete'):
            query = File.all()
            query.order('title')
            self.pager(query.count(), settings.files_per_page, settings.file_management_url)
            files = query.fetch(settings.files_per_page, self.pager_offset())
            files_extended = []
            for file in files:
                self.manipulator.formater(file, [{'name': 'title', 'type': 'unicode', 'trim': settings.file_title_trimmed}])
                file.view_url = self.get_redirect(settings.file_output_url_string % (str(file.file.key()), str(file.file.filename)))
                file.edit_url = self.get_redirect(settings.file_edit_url_string % str(file.key().id()))
                file.delete_url = self.get_redirect(settings.file_delete_url_string % str(file.key().id()))
                files_extended.append(file)
            data = {'title': settings.file_management_title,
                    'files': files_extended,
                    'pager': self.render_pager(),
                    'add_url': self.get_redirect(settings.file_add_url),
                    'permissions_url': self.get_redirect(settings.file_permissions_url),
                    'file_add': self.access.check('file_add'),
                    'file_edit': self.access.check('file_edit'),
                    'file_delete': self.access.check('file_delete'),
                    'file_permissions': self.access.admin_user}
            self.render_html('file', 'file_management_form', data)
        else:
            self.render_error(403)


class FilePermissions(UserPermissionAPI):
    
    def get(self):
        self.get_form(permissions=['file_view', 'file_add', 'file_edit', 'file_delete'], url=settings.file_permissions_url, title=settings.file_permissions_title)
        
    def post(self):
        values = self.request.get_all('user-permissions')
        self.save_permissions(permissions=['file_view', 'file_add', 'file_edit', 'file_delete'], values=values, url=settings.file_permissions_url)
                       
            
class FileAPI():
    
    def __init__(self, templateapi):
        self.templateapi = templateapi
    
    def get_file(self, key, published_filter = True):
        if key:
            try:
                file = File.get(key)
                if (published_filter and file.published) or not published_filter:
                    self.templateapi.manipulator.formater(file, [{'name': 'title', 'type': 'unicode', 'trim': settings.file_title_trimmed}])
                    file.src = self.templateapi.get_redirect(settings.file_output_url_string % (str(file.file.key()), str(file.file.filename)))
                    return file
                else:
                    return None
            except:
                return None
        return None
    
    def get_files(self, keys, published_filter = True, limit = settings.files_per_page, offset = 0):
        if keys:
            try:
                files = File.get(keys[offset:limit + offset])
                files_extended = []
                for file in files:
                    if (published_filter and file.published) or not published_filter:
                        self.templateapi.manipulator.formater(file, [{'name': 'title', 'type': 'unicode', 'trim': settings.file_title_trimmed}])
                        file.src = self.templateapi.get_redirect(settings.file_output_url_string % (str(file.file.key()), str(file.file.filename)))
                        files_extended.append(file)
                return files_extended
            except:
                return None
        return None
            
            
class FileOutput(blobstore_handlers.BlobstoreDownloadHandler):
    
    def get(self, key, filename):
        try:
            key = str(urllib.unquote(key))
            blob_info = blobstore.BlobInfo.get(key)
            self.send_blob(blob_info)
        except:
            self.redirect(settings.site_error_url_string % '404')
            
            
class FileError(TemplateAPI):
    
    def get(self, type):
        if type == settings.file_error_oversize_type:
            title = settings.file_error_oversize_title
            error_message = settings.file_error_oversize_message_string % settings.file_max_upload_size
            self.render_error(403, title, error_message)
        elif type == settings.file_error_incorrect_type_type:
            title = settings.file_error_incorrect_type_title
            error_message = settings.file_error_incorrect_type_message_string % ', '.join(settings.file_allowed_types)
            self.render_error(403, title, error_message)
        elif type == settings.file_error_forbidden_type:
            self.render_error(403)
        else:
            self.render_error(404)

app = webapp.WSGIApplication(
        [(settings.file_error_url, FileError),
        (settings.file_permissions_url, FilePermissions),
        (settings.file_management_url, FileManagement),
        (settings.file_add_url, FileAdd),
        (settings.file_save_url, FileSave),
        (settings.file_edit_url, FileEdit),
        (settings.file_delete_url, FileDelete),
        (settings.file_output_url, FileOutput),],
        debug=False)
'''def main():
    application = webapp.WSGIApplication(
        [(settings.file_error_url, FileError),
        (settings.file_permissions_url, FilePermissions),
        (settings.file_management_url, FileManagement),
        (settings.file_add_url, FileAdd),
        (settings.file_save_url, FileSave),
        (settings.file_edit_url, FileEdit),
        (settings.file_delete_url, FileDelete),
        (settings.file_output_url, FileOutput),],
        debug=False)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()'''