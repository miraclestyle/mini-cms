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
from music import Music, MusicAPI


class Feed(db.Model):
    
    title = db.StringProperty(multiline=False, required=True)
    path = db.StringProperty(multiline=False, required=True)
    type = db.StringProperty(choices=(settings.feed_types['types']), required=True)
    content = db.TextProperty()
    cover = db.ReferenceProperty(Photo, collection_name='feed_covers')
    background = db.ReferenceProperty(Photo, collection_name='feed_backgrounds')
    photos = db.ListProperty(db.Key)
    musics = db.ListProperty(db.Key)
    published = db.BooleanProperty(default=True, required=True)
    owner = db.ReferenceProperty(User, collection_name='feed_owners', required=True)
    created = db.DateTimeProperty(auto_now_add=True, required=True)
    updated = db.DateTimeProperty(auto_now=True, required=True)


class FeedAdd(TemplateAPI):
    
    def get(self):
        self.access_init()
        access = False
        for type in settings.feed_types['types']:
            if self.access.check('feed_%s_add' % type):
                access = True
                break
        if access:
            types = []
            for type in settings.feed_types['types']:
                types.append({'value': type, 'label': settings.feed_types[type]['label']})
            data = {'title': settings.feed_add_title,
                    'types': types,
                    'content_editor': self.ckeditor.editor('feed_content'),
                    'submit_url': self.get_redirect(settings.feed_add_url),
                    'cancel_url': self.get_redirect(settings.feed_add_redirect_url)}
            self.render_html('feed', 'feed_add_form', data)
        else:
            self.render_error(403)
            
    def post(self):
        self.access_init()
        if self.access.check('feed_%s_add' % self.request.get('type')):
            try:
                title = unicode(self.request.get('title'))
                original_path = unicode(self.request.get('path'))
                path = original_path
                feeds = Feed.gql("WHERE path = :1", path).get()
                i = 0
                while feeds:
                    path = '%s-%s' % (original_path, i)
                    i += 1
                    feeds = Feed.gql("WHERE path = :1", path).get()
                type = unicode(self.request.get('type'))
                content = db.Text(unicode(self.request.get('feed_content')))
                if self.request.get('feed-cover'):
                    cover = db.Key(encoded=self.request.get('feed-cover'))
                else:
                    cover = None
                if self.request.get('feed-background'):
                    background = db.Key(encoded=self.request.get('feed-background'))
                else:
                    background = None
                photos_encoded = self.request.get_all('feed-photos')
                photos = []
                if photos_encoded:
                    for photo_encoded in photos_encoded:
                        photos.append(db.Key(encoded=photo_encoded))
                musics_encoded = self.request.get_all('feed-musics')
                musics = []
                if musics_encoded:
                    for music_encoded in musics_encoded:
                        musics.append(db.Key(encoded=music_encoded))
                published = bool(self.request.get('published'))
                owner = self.access.current_user
                feed = Feed(title=title, path=path, type=type, content=content, cover=cover, background=background, photos=photos, musics=musics, published=published, owner=owner)
                feed.put()
                self.redirect_to(settings.feed_add_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)


class FeedEdit(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        feed = Feed.get_by_id(int(id))
        if self.access.check('feed_%s_edit' % feed.type):
            try:
                photo = PhotoAPI(self)
                music = MusicAPI(self)
                self.manipulator.formater(feed, [{'name': 'title', 'type': 'unicode', 'trim': settings.feed_types[feed.type]['title_trimmed']},
                                                 {'name': 'path', 'type': 'unicode'},
                                                 {'name': 'content', 'type': 'html', 'escape': True}])
                types_selected = []
                for type in settings.feed_types['types']:
                    if type == feed.type:
                        type_selected = {'value': type, 'label': settings.feed_types[type]['label'], 'selected': True}
                    else:
                        type_selected = {'value': type, 'label': settings.feed_types[type]['label'], 'selected': False}
                    types_selected.append(type_selected)
                feed_cover_src = ''
                try:
                    if feed.cover:
                        feed_cover = photo.get_photo(feed.cover.key(), False, settings.photo_s_w, settings.photo_s_h)
                        if feed_cover:
                            feed_cover_src = feed_cover.src
                except:
                    pass
                feed_background_src = ''
                try:
                    if feed.background:
                        feed_background = photo.get_photo(feed.background.key(), False, settings.photo_s_w, settings.photo_s_h)
                        if feed_background:
                            feed_background_src = feed_background.src
                except:
                    pass
                feed_photos = ''
                try:
                    if feed.photos:
                        feed_photos_photos = photo.get_photos(feed.photos, False, len(feed.photos), 0, settings.photo_s_w, settings.photo_s_h)
                        if feed_photos_photos:
                            feed_photos = feed_photos_photos
                except:
                    pass
                feed_musics = ''
                try:
                    if feed.musics:
                        feed_musics_musics = music.get_musics(feed.musics, False, len(feed.musics), 0)
                        if feed_musics_musics:
                            feed_musics = feed_musics_musics
                except:
                    pass
                data = {'title': settings.feed_edit_title,
                        'feed': feed,
                        'types': types_selected,
                        'content_editor': self.ckeditor.editor('feed_content', feed.content_formated),
                        'feed_cover_src': feed_cover_src,
                        'feed_background_src': feed_background_src,
                        'feed_photos': feed_photos,
                        'feed_musics': feed_musics,
                        'submit_url': self.get_redirect(settings.feed_edit_url_string % str(feed.key().id())),
                        'cancel_url': self.get_redirect(settings.feed_edit_redirect_url),}
                self.render_html('feed', 'feed_edit_form', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
        
    def post(self, id):
        self.access_init()
        feed = Feed.get_by_id(int(id))
        if self.access.check('feed_%s_edit' % feed.type):
            try:
                feed.title = unicode(self.request.get('title'))
                original_path = unicode(self.request.get('path'))
                if feed.path != original_path:
                    path = original_path
                    feeds = Feed.gql("WHERE path = :1", path).get()
                    i = 0
                    while feeds:
                        path = '%s-%s' % (original_path, i)
                        i += 1
                        feeds = Feed.gql("WHERE path = :1", path).get()
                    feed.path = path
                feed.type = unicode(self.request.get('type'))
                feed.content = db.Text(unicode(self.request.get('feed_content')))
                if self.request.get('feed-cover'):
                    feed.cover = db.Key(encoded=self.request.get('feed-cover'))
                else:
                    feed.cover = None
                if self.request.get('feed-background'):
                    feed.background = db.Key(encoded=self.request.get('feed-background'))
                else:
                    feed.background = None
                photos_encoded = self.request.get_all('feed-photos')
                photos = []
                if photos_encoded:
                    for photo_encoded in photos_encoded:
                        photos.append(db.Key(encoded=photo_encoded))
                feed.photos = photos
                musics_encoded = self.request.get_all('feed-musics')
                musics = []
                if musics_encoded:
                    for music_encoded in musics_encoded:
                        musics.append(db.Key(encoded=music_encoded))
                feed.musics = musics
                feed.published = bool(self.request.get('published'))
                feed.put()
                self.redirect_to(settings.feed_edit_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

        
class FeedDelete(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        feed = Feed.get_by_id(int(id))
        if self.access.check('feed_%s_delete' % feed.type):
            try:
                self.manipulator.formater(feed, [{'name': 'title', 'type': 'unicode', 'trim': settings.feed_types[feed.type]['title_trimmed']},
                                                 {'name': 'path', 'type': 'unicode'},
                                                 {'name': 'content', 'type': 'html', 'escape': False}])
                data = {'title': settings.feed_delete_title,
                        'feed': feed,
                        'delete_question': settings.feed_delete_form_label_question_string % (settings.feed_types[feed.type]['label'], feed.title_formated),
                        'submit_url': self.get_redirect(settings.feed_delete_url_string % str(feed.key().id())),
                        'cancel_url': self.get_redirect(settings.feed_delete_redirect_url)}
                self.render_html('feed', 'feed_delete_form', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
        
    def post(self, id):
        self.access_init()
        feed = Feed.get_by_id(int(id))
        if self.access.check('feed_%s_delete' % feed.type):
            try:
                feed.delete()
                self.redirect_to(settings.feed_delete_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

            
class FeedManagement(TemplateAPI):

    def get(self):
        self.access_init()
        access = False
        access_add = False
        for type in settings.feed_types['types']:
            if self.access.check('feed_%s_add' % type):
                access_add = True
            if self.access.check('feed_%s_edit' % type):
                access = True
            if self.access.check('feed_%s_delete' % type):
                access = True
        if access:
            query = Feed.all()
            query.order('-created')
            self.pager(query.count(), settings.feeds_per_page, settings.feed_management_url)
            feeds = query.fetch(settings.feeds_per_page, self.pager_offset())
            feeds_extended = []
            for feed in feeds:
                self.manipulator.formater(feed, [{'name': 'title', 'type': 'unicode', 'trim': settings.feed_types[feed.type]['title_trimmed']},
                                                 {'name': 'path', 'type': 'unicode'},
                                                 {'name': 'content', 'type': 'html', 'escape': False}])
                feed.type_label = settings.feed_types[feed.type]['label']
                feed.view_url = self.get_redirect(settings.feed_view_url_string % (settings.feed_types[feed.type]['feed_view_url'], feed.path_formated))
                feed.edit_url = self.get_redirect(settings.feed_edit_url_string % str(feed.key().id()))
                feed.delete_url = self.get_redirect(settings.feed_delete_url_string % str(feed.key().id()))
                feed.can_edit = self.access.check('feed_%s_edit' % feed.type)
                feed.can_delete = self.access.check('feed_%s_delete' % feed.type)
                feeds_extended.append(feed)
            data = {'title': settings.feed_management_title,
                    'feeds': feeds_extended,
                    'pager': self.render_pager(),
                    'add_url': self.get_redirect(settings.feed_add_url),
                    'permissions_url': self.get_redirect(settings.feed_permissions_url),
                    'feed_add': access_add,
                    'feed_permissions': self.access.admin_user}
            self.render_html('feed', 'feed_management_form', data)
        else:
            self.render_error(403)


class FeedPermissions(UserPermissionAPI):
    
    def get(self):
        permissions = []
        for type in settings.feed_types['types']:
            permissions.append('feed_%s_view' % type)
            permissions.append('feed_%s_add' % type)
            permissions.append('feed_%s_edit' % type)
            permissions.append('feed_%s_delete' % type)
        self.get_form(permissions=permissions, url=settings.feed_permissions_url, title=settings.feed_permissions_title)
        
    def post(self):
        permissions = []
        for type in settings.feed_types['types']:
            permissions.append('feed_%s_view' % type)
            permissions.append('feed_%s_add' % type)
            permissions.append('feed_%s_edit' % type)
            permissions.append('feed_%s_delete' % type)
        values = self.request.get_all('user-permissions')
        self.save_permissions(permissions=permissions, values=values, url=settings.feed_permissions_url)


class FeedSinglePathRouter(TemplateAPI):
    
    def get(self, path):
        canonical = ''
        if self.request.path == '/':
            path = settings.feeds_view_default_path
            canonical = path
        if settings.feed_types['feeds_view_url_types'].has_key(path):
            type = settings.feed_types['feeds_view_url_types'][path]
            FeedView.get_feeds(self, type, canonical)
        else:
            type = settings.feeds_view_default_type
            canonical = '%s/%s' % (type, path)
            type = settings.feed_types['feed_view_url_types'][type]
            FeedView.get_feed(self, type, path, canonical)

            
class FeedMultiPathRouter(TemplateAPI):
    
    def get(self, type, path):
        if settings.feed_types['feed_view_url_types'].has_key(type):
            type = settings.feed_types['feed_view_url_types'][type]
            FeedView.get_feed(self, type, path, '')
        else:
            self.render_error(404)
            

class FeedView():
    
    @staticmethod
    def get_feed(templateapi, type, path, canonical):  
        templateapi.access_init()
        if templateapi.access.check('feed_%s_view' % type) or templateapi.access.check('feed_%s_edit' % type) or templateapi.access.check('feed_%s_delete' % type):
            try:
                feed = Feed.gql("WHERE path = :1", path).get()
                if feed.published or templateapi.access.check('feed_%s_edit' % type) or templateapi.access.check('feed_%s_delete' % type):
                    templateapi.manipulator.formater(feed, [{'name': 'title', 'type': 'unicode', 'trim': settings.feed_types[type]['title_trimmed']},
                                                            {'name': 'path', 'type': 'unicode'},
                                                            {'name': 'content', 'type': 'html', 'escape': False},
                                                            {'name': 'created', 'type': 'datetime', 'format': settings.datetime_formated, 'trim': settings.datetime_trimmed}])
                    photo = PhotoAPI(templateapi)
                    music = MusicAPI(templateapi)
                    feed_cover_src = ''
                    try:
                        if feed.cover:
                            feed_cover = photo.get_photo(feed.cover.key(), True, settings.feed_types[type]['feed_view_cover_w'], settings.feed_types[type]['feed_view_cover_h'])
                            if feed_cover:
                                feed_cover_src = feed_cover.src
                    except:
                        pass
                    feed_background_src = ''
                    try:
                        if feed.background:
                            feed_background = photo.get_photo(feed.background.key(), True, settings.feed_types[type]['background_w'], settings.feed_types[type]['background_h'])
                            if feed_background:
                                feed_background_src = feed_background.src
                    except:
                        pass
                    feed_photos = ''
                    photos_pager = ''
                    try:
                        if feed.photos:
                            templateapi.pager(len(feed.photos), settings.feed_types[type]['photos_per_page'], settings.feed_view_url_string % (settings.feed_types[type]['feed_view_url'], feed.path_formated), 'photos_page')
                            feed_photos_photos = photo.get_photos(feed.photos, True, settings.feed_types[type]['photos_per_page'], templateapi.pager_offset(), settings.feed_types[type]['photos_w'], settings.feed_types[type]['photos_h'])
                            if feed_photos_photos:
                                feed_photos = feed_photos_photos
                            photos_pager = templateapi.render_pager()
                    except:
                        pass
                    feed_musics = ''
                    musics_pager = ''
                    try:
                        if feed.musics:
                            templateapi.pager(len(feed.musics), settings.feed_types[type]['musics_per_page'], settings.feed_view_url_string % (settings.feed_types[type]['feed_view_url'], feed.path_formated), 'musics_page')
                            feed_musics_musics = music.get_musics(feed.musics, True, settings.feed_types[type]['musics_per_page'], templateapi.pager_offset())
                            if feed_musics_musics:
                                feed_musics = feed_musics_musics
                            musics_pager = templateapi.render_pager()
                    except:
                        pass
                    if templateapi.request.path == '/':
                        title = settings.feed_view_default_title
                    else:
                        title = feed.title_formated
                    data = {'title': title,
                            'feed': feed,
                            'canonical': canonical,
                            'feed_cover_src': feed_cover_src,
                            'background': feed_background_src,
                            'photos': feed_photos,
                            'photos_per_row': settings.feed_types[type]['photos_per_row'],
                            'musics': feed_musics,
                            'musics_per_row': settings.feed_types[type]['musics_per_row'],
                            'like_url': templateapi.get_redirect(settings.feed_view_url_string % (settings.feed_types[type]['feed_view_url'], feed.path_formated)),
                            'photos_pager': photos_pager,
                            'musics_pager': musics_pager}
                    templateapi.render_html('feed_view', '%s_view' % type, data)
                else:
                    templateapi.render_error(404)
            except Exception, e:
                import logging
                logging.info(e)
                templateapi.render_error(404)
        else:
            templateapi.render_error(403)

    @staticmethod
    def get_feeds(templateapi, type, canonical):
        templateapi.access_init()
        if templateapi.access.check('feed_%s_view' % type) or templateapi.access.check('feed_%s_edit' % type) or templateapi.access.check('feed_%s_delete' % type):
            photo = PhotoAPI(templateapi)
            if templateapi.access.check('feed_%s_view' % type):
                published_filter = True
            if templateapi.access.check('feed_%s_edit' % type) or templateapi.access.check('feed_%s_delete' % type):
                published_filter = False
            query = Feed.all()
            query.filter('type = ', type)
            if published_filter:
                query.filter('published = ', True)
            query.order(settings.feed_types[type]['sort'])
            templateapi.pager(query.count(), settings.feed_types[type]['feeds_per_page'], settings.feeds_view_url_string % settings.feed_types[type]['feeds_view_url'])
            feeds = query.fetch(settings.feed_types[type]['feeds_per_page'], templateapi.pager_offset())
            feeds_extended = []
            for feed in feeds:
                templateapi.manipulator.formater(feed, [{'name': 'title', 'type': 'unicode', 'trim': settings.feed_types[type]['title_trimmed']},
                                                        {'name': 'path', 'type': 'unicode'},
                                                        {'name': 'content', 'type': 'html', 'escape': False},
                                                        {'name': 'created', 'type': 'datetime', 'format': settings.datetime_formated, 'trim': settings.datetime_trimmed}])
                stripped_content = templateapi.manipulator.hide_tags(feed.content, True)
                
                feed.content_hide_tags = templateapi.manipulator.truncate_string(stripped_content, settings.landing_page_trim)
                
                feed.content_trimmed = templateapi.manipulator.truncate_string(stripped_content, settings.feed_types[type]['content_trimmed'])
                feed_cover_src = ''
                try:
                    if feed.cover:
                        feed_cover = photo.get_photo(feed.cover.key(), True, settings.feed_types[type]['feeds_view_cover_w'], settings.feed_types[type]['feeds_view_cover_h'])
                        if feed_cover:
                            feed_cover_src = feed_cover.src
                except:
                    pass
                
                feed.cover_src = feed_cover_src
                feed.view_url = templateapi.get_redirect(settings.feed_view_url_string % (settings.feed_types[type]['feed_view_url'], feed.path_formated))
                feeds_extended.append(feed)
            if templateapi.request.path == '/':
                title = settings.feeds_view_default_title
            else:
                title = settings.feed_types[type]['title']
                
            is_page = templateapi.request.get('page', None)
            if is_page == 1:
               is_page = False
                   
            data = {'title': title,
                    'feeds': feeds_extended,
                    'canonical': canonical,
                    'feeds_per_row': settings.feed_types[type]['feeds_per_row'],
                    'background': settings.feed_types[type]['default_background_src'],
                    'canonical': canonical,
                    'current_request' : templateapi.request,
                    'is_pager' : is_page,
                    'pager': templateapi.render_pager()}
            templateapi.render_html('feed_view', '%s_view' % settings.feed_types[type]['feeds_view_template'], data)
        else:
            templateapi.render_error(403)

app = webapp.WSGIApplication(
        [(settings.feed_permissions_url, FeedPermissions),
         (settings.feed_management_url, FeedManagement),
         (settings.feed_add_url, FeedAdd),
         (settings.feed_edit_url, FeedEdit),
         (settings.feed_delete_url, FeedDelete),
         (settings.feed_view_url, FeedMultiPathRouter),
         (settings.feeds_view_url, FeedSinglePathRouter),],
        debug=False)   
'''def main():
    application = webapp.WSGIApplication(
        [(settings.feed_permissions_url, FeedPermissions),
         (settings.feed_management_url, FeedManagement),
         (settings.feed_add_url, FeedAdd),
         (settings.feed_edit_url, FeedEdit),
         (settings.feed_delete_url, FeedDelete),
         (settings.feed_view_url, FeedMultiPathRouter),
         (settings.feeds_view_url, FeedSinglePathRouter),],
        debug=False)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()'''