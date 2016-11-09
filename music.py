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


class Music(db.Model):
    
    music = blobstore.BlobReferenceProperty()
    title = db.StringProperty(multiline=False, required=True)
    content = db.TextProperty(required=True)
    published = db.BooleanProperty(default=True, required=True)
    owner = db.ReferenceProperty(User, collection_name='music_owners', required=True)
    created = db.DateTimeProperty(auto_now_add=True, required=True)
    updated = db.DateTimeProperty(auto_now=True, required=True)

    
class MusicAdd(TemplateAPI):
    
    def get(self):
        self.access_init()
        if self.access.check('music_add'):
            data = {'title': settings.music_add_title,
                    'content_editor': self.ckeditor.editor('music_content'),
                    'submit_url': blobstore.create_upload_url(self.get_redirect(settings.music_save_url)),
                    'cancel_url': self.get_redirect(settings.music_add_redirect_url)}
            self.render_html('music', 'music_add_form', data)
        else:
            self.render_error(403)


class MusicSave(blobstore_handlers.BlobstoreUploadHandler):
    
    def post(self):
        access = UserAccess(self.request.cookies)
        if access.check('music_add'):
            musics = self.get_uploads('music')
            blob_info = musics[0]
            if blob_info.content_type in settings.music_allowed_types:
                incorrect_type = False
            elif 'all' in settings.music_allowed_types:
                incorrect_type = False
            else:
                incorrect_type = True
            if blob_info.size > settings.music_max_upload_size:
                blobstore.delete(blob_info.key())
                if self.request.get('frame'):
                    self.redirect('%s?frame=%s' % (settings.music_error_url_string % settings.music_error_oversize_type, self.request.get('frame')))
                else:
                    self.redirect(settings.music_error_url_string % settings.music_error_oversize_type)
            elif incorrect_type:
                blobstore.delete(blob_info.key())
                if self.request.get('frame'):
                    self.redirect('%s?frame=%s' % (settings.music_error_url_string % settings.music_error_incorrect_type_type, self.request.get('frame')))
                else:
                    self.redirect(settings.music_error_url_string % settings.music_error_incorrect_type_type)
            else:
                music_reference = blob_info.key()
                title = unicode(self.request.get('title'))
                content = db.Text(unicode(self.request.get('music_content')))
                published = bool(self.request.get('published'))
                owner = access.current_user
                music = Music(music=music_reference, title=title, content=content, published=published, owner=owner)
                music.put()
                if self.request.get('frame'):
                    self.redirect('%s?frame=%s' % (settings.music_save_redirect_url, self.request.get('frame')))
                else:
                    self.redirect(settings.music_save_redirect_url)
        else:
            if self.request.query_string:
                self.redirect('%s?frame=%s' % (settings.music_error_url_string % settings.music_error_forbidden_type, self.request.get('frame')))
            else:
                self.redirect(settings.music_error_url_string % settings.music_error_forbidden_type)


class MusicEdit(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('music_edit'):
            try:
                music = Music.get_by_id(int(id))
                self.manipulator.formater(music, [{'name': 'title', 'type': 'unicode', 'trim': settings.music_title_trimmed},
                                                  {'name': 'content', 'type': 'html', 'escape': True}])
                data = {'title': settings.music_edit_title,
                        'music': music,
                        'content_editor': self.ckeditor.editor('music_content', music.content_formated),
                        'src': self.get_redirect(settings.music_output_url_string % (str(music.music.key()), str(music.music.filename))),
                        'submit_url': self.get_redirect(settings.music_edit_url_string % str(music.key().id())),
                        'cancel_url': self.get_redirect(settings.music_edit_redirect_url),}
                self.render_html('music', 'music_edit_form', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
        
    def post(self, id):
        self.access_init()
        if self.access.check('music_edit'):
            try:
                music = Music.get_by_id(int(id))
                music.title = unicode(self.request.get('title'))
                music.content = db.Text(unicode(self.request.get('music_content')))
                music.published = bool(self.request.get('published'))
                music.put()
                self.redirect_to(settings.music_edit_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

        
class MusicDelete(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('music_delete'):
            try:
                music = Music.get_by_id(int(id))
                self.manipulator.formater(music, [{'name': 'title', 'type': 'unicode', 'trim': settings.music_title_trimmed},
                                                  {'name': 'content', 'type': 'html', 'escape': False}])
                data = {'title': settings.music_delete_title,
                        'music': music,
                        'delete_question': settings.music_delete_form_label_question_string % music.title_formated,
                        'src': self.get_redirect(settings.music_output_url_string % (str(music.music.key()), str(music.music.filename))),
                        'submit_url': self.get_redirect(settings.music_delete_url_string % str(music.key().id())),
                        'cancel_url': self.get_redirect(settings.music_delete_redirect_url)} 
                self.render_html('music', 'music_delete_form', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
        
    def post(self, id):
        self.access_init()
        if self.access.check('music_delete'):
            try:
                music = Music.get_by_id(int(id))
                blobstore.delete(music.music.key())
                music.delete()
                self.redirect_to(settings.music_delete_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

            
class MusicManagement(TemplateAPI):

    def get(self):
        self.access_init()
        if self.access.check('music_edit') or self.access.check('music_delete'):
            query = Music.all()
            query.order('title')
            self.pager(query.count(), settings.musics_per_page, settings.music_management_url)
            musics = query.fetch(settings.musics_per_page, self.pager_offset())
            musics_extended = []
            for music in musics:
                self.manipulator.formater(music, [{'name': 'title', 'type': 'unicode', 'trim': settings.music_title_trimmed},
                                                  {'name': 'content', 'type': 'html', 'escape': False}])
                music.src = self.get_redirect(settings.music_output_url_string % (str(music.music.key()), str(music.music.filename))) 
                music.view_url = self.get_redirect(settings.music_view_url_string % str(music.key().id()))
                music.edit_url = self.get_redirect(settings.music_edit_url_string % str(music.key().id()))
                music.delete_url = self.get_redirect(settings.music_delete_url_string % str(music.key().id()))
                musics_extended.append(music)
            data = {'title': settings.music_management_title,
                    'musics': musics_extended,
                    'pager': self.render_pager(),
                    'add_url': self.get_redirect(settings.music_add_url),
                    'permissions_url': self.get_redirect(settings.music_permissions_url),
                    'music_add': self.access.check('music_add'),
                    'music_edit': self.access.check('music_edit'),
                    'music_delete': self.access.check('music_delete'),
                    'music_permissions': self.access.admin_user}
            self.render_html('music', 'music_management_form', data)
        else:
            self.render_error(403)


class MusicPermissions(UserPermissionAPI):
    
    def get(self):
        self.get_form(permissions=['music_view', 'music_add', 'music_edit', 'music_delete'], url=settings.music_permissions_url, title=settings.music_permissions_title)
        
    def post(self):
        values = self.request.get_all('user-permissions')
        self.save_permissions(permissions=['music_view', 'music_add', 'music_edit', 'music_delete'], values=values, url=settings.music_permissions_url)
                       

class MusicView(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('music_view') or self.access.check('music_edit') or self.access.check('music_delete'):
            try:
                music = Music.get_by_id(int(id))
                if music.published or self.access.check('music_edit') or self.access.check('music_delete'):
                    self.manipulator.formater(music, [{'name': 'title', 'type': 'unicode', 'trim': settings.music_title_trimmed},
                                                      {'name': 'content', 'type': 'html', 'escape': False}])
                    src = self.get_redirect(settings.music_output_url_string % (str(music.music.key()), str(music.music.filename)))
                    data = {'title': music.title_formated,
                            'music': music,
                            'src': src,
                            'like_url': self.get_redirect(settings.music_view_url_string % str(music.key().id()))}
                    self.render_html('music', 'music_view', data)
                else:
                    self.render_error(404)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

            
class MusicAPI():
    
    def __init__(self, templateapi):
        self.templateapi = templateapi
    
    def get_music(self, key, published_filter = True):
        if key:
            try:
                music = Music.get(key)
                if (published_filter and music.published) or not published_filter:
                    self.templateapi.manipulator.formater(music, [{'name': 'title', 'type': 'unicode', 'trim': settings.music_title_trimmed},
                                                                  {'name': 'content', 'type': 'html', 'escape': False}])
                    music.src = self.templateapi.get_redirect(settings.music_output_url_string % (str(music.music.key()), str(music.music.filename)))
                    music.view_url = self.templateapi.get_redirect(settings.music_view_url_string % str(music.key().id()))
                    music.like_url = self.templateapi.get_redirect(settings.music_view_url_string % str(music.key().id()))
                    return music
                else:
                    return None
            except:
                return None
        return None
    
    def get_musics(self, keys, published_filter = True, limit = settings.musics_per_page, offset = 0):
        if keys:
            try:
                musics = Music.get(keys[offset:limit + offset])
                musics_extended = []
                for music in musics:
                    if (published_filter and music.published) or not published_filter:
                        self.templateapi.manipulator.formater(music, [{'name': 'title', 'type': 'unicode', 'trim': settings.music_title_trimmed},
                                                                      {'name': 'content', 'type': 'html', 'escape': False}])
                        music.src = self.templateapi.get_redirect(settings.music_output_url_string % (str(music.music.key()), str(music.music.filename)))
                        music.view_url = self.templateapi.get_redirect(settings.music_view_url_string % str(music.key().id()))
                        music.like_url = self.templateapi.get_redirect(settings.music_view_url_string % str(music.key().id()))
                        musics_extended.append(music)
                return musics_extended
            except:
                return None
        return None
            
            
class MusicOutput(blobstore_handlers.BlobstoreDownloadHandler):
    
    def get(self, key, musicname):
        try:
            key = str(urllib.unquote(key))
            blob_info = blobstore.BlobInfo.get(key)
            self.send_blob(blob_info)
        except:
            self.redirect(settings.site_error_url_string % '404')
            
            
class MusicError(TemplateAPI):
    
    def get(self, type):
        if type == settings.music_error_oversize_type:
            title = settings.music_error_oversize_title
            error_message = settings.music_error_oversize_message_string % settings.music_max_upload_size
            self.render_error(403, title, error_message)
        elif type == settings.music_error_incorrect_type_type:
            title = settings.music_error_incorrect_type_title
            error_message = settings.music_error_incorrect_type_message_string % ', '.join(settings.music_allowed_types)
            self.render_error(403, title, error_message)
        elif type == settings.music_error_forbidden_type:
            self.render_error(403)
        else:
            self.render_error(404)

app = webapp.WSGIApplication(
        [(settings.music_error_url, MusicError),
        (settings.music_permissions_url, MusicPermissions),
        (settings.music_management_url, MusicManagement),
        (settings.music_add_url, MusicAdd),
        (settings.music_save_url, MusicSave),
        (settings.music_edit_url, MusicEdit),
        (settings.music_delete_url, MusicDelete),
        (settings.music_view_url, MusicView),
        (settings.music_output_url, MusicOutput),],
        debug=False)
'''def main():
    application = webapp.WSGIApplication(
        [(settings.music_error_url, MusicError),
        (settings.music_permissions_url, MusicPermissions),
        (settings.music_management_url, MusicManagement),
        (settings.music_add_url, MusicAdd),
        (settings.music_save_url, MusicSave),
        (settings.music_edit_url, MusicEdit),
        (settings.music_delete_url, MusicDelete),
        (settings.music_view_url, MusicView),
        (settings.music_output_url, MusicOutput),],
        debug=False)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()'''