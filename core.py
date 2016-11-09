#coding=UTF-8
'''
Created on Jan 7, 2011

@author: elvin
'''

import settings
#import sys
#sys.path.append(settings.app_dir + '/modules/')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_settings'
import re
import facebook
import datetime
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from django.utils import simplejson as json
from django.utils.text import truncate_words
from django.utils.html import escape
from vendor.BeautifulSoup import BeautifulSoup, NavigableString

core_template_path = os.path.join(settings.app_dir, 'templates', 'core')

class TemplateAPI(webapp.RequestHandler):
    
    def __init__(self, *args, **kwargs):
        super(TemplateAPI, self).__init__(*args, **kwargs)
        self.access = None
        self.ckeditor = CKEditor()
        self.manipulator = ContentManipulator()
        
    def access_init(self):
        self.access = UserAccess(self.request.cookies)
    
    def render(self, content_type, content, ajax = False):
        self.response.headers['Content-Type'] = content_type
        if ajax:
            self.response.out.write(json.dumps(content, indent = 4))
        else:
            self.response.out.write(content)

    def render_template(self, content_type, module_name, module_template_file, data=None):
        if not self.access:
            try:
                self.access_init()
            except:
                pass
        if data is None:
            data = {}
        data['settings'] = settings
        if self.access:
            data['signedin_user'] = self.access.signedin_user
        if not data.has_key('top'):
            data['top'] = ''
        if not data.has_key('bottom'):
            data['bottom'] = ''
        if not data.has_key('left'):
            data['left'] = ''
        if not data.has_key('right'):
            data['right'] = ''
        if not data.has_key('title'):
            data['title'] = ''
        module_template = os.path.join(settings.app_dir, 'templates', module_name, module_template_file)
        data['content'] = template.render(module_template, data)
        #data['content'] = unicode(data['content'], 'utf_8', 'ignore')
        headers = self.request.headers
        if headers.has_key('X-Requested-With'):
            if headers['X-Requested-With'].lower() == 'xmlhttprequest':
                output= {'title': data['title'], 'content': data['content'], 'options' : {}}
                content_type = 'application/json; charset=utf-8'
                self.render(content_type, output, ajax = True)
        elif (data.has_key('ajax') and data['ajax']) or self.request.get('ajax') == '1':
            output= {'title': data['title'], 'content': data['content'], 'options' : {}}
            content_type = 'application/json; charset=utf-8'
            self.render(content_type, output, ajax = True)
        elif (data.has_key('frame') and data['frame']) or self.request.get('frame') == '1':
            output = template.render(os.path.join(core_template_path, 'iframe.html'), data)
            #output = unicode(output, 'utf_8', 'ignore')
            self.render(content_type, output)
        else:
            menus = Menus(self.request.path)
            data['top'] += menus.top
            data['bottom'] += menus.bottom
            data['left'] += menus.left
            data['right'] += menus.right
            if self.access:
                blocks = Blocks(self)
                data['top'] += blocks.top
                data['bottom'] += blocks.bottom
                data['left'] += blocks.left
                data['right'] += blocks.right
            output = template.render(os.path.join(core_template_path, 'index.html'), data)
            #output = unicode(output, 'utf_8', 'ignore')
            self.render(content_type, output)

    def render_html(self, module_name, module_template_name, data=None):
        self.render_template('text/html', module_name, '%s.html' % module_template_name, data)

    def render_atom(self, module_name, module_template_name, data=None):
        self.render_template('application/atom+xml', module_name, '%s.xml' % module_template_name, data)
        
    def render_error(self, status_code, title = '', error_message = ''):
        data = {}
        data['title'] = title
        data['error_message'] = error_message
        if status_code == 403 and not title and not error_message:
            data['title'] = settings.template_api_render_errors['403']['title']
            data['error_message'] = settings.template_api_render_errors['403']['message']
        elif status_code == 404 and not title and not error_message:
            data['title'] = settings.template_api_render_errors['404']['title']
            data['error_message'] = settings.template_api_render_errors['404']['message']
        elif status_code == 500 and not title and not error_message:
            data['title'] = settings.template_api_render_errors['500']['title']
            data['error_message'] = settings.template_api_render_errors['500']['message']
        elif not title and not error_message:
            status_code = 404
            data['title'] = settings.template_api_render_errors['default']['title']
            data['error_message'] = settings.template_api_render_errors['default']['message']
            
        self.response.set_status(status_code)
        self.render_template('text/html', 'core', 'error.html', data)
        
    def redirect_to(self, url, op = 'none', data = []):
        self.redirect(self.get_redirect(url, op, data))
        
    def get_redirect(self, url, op = 'none', data = []):
        q = self.request.query_string
        if op == 'none':
            if q:
                return '%s?%s' % (url, q)
            else:
                return url
        elif op != 'none':
            if data:
                if data[0]['query']:
                    query = data[0]['query']
                    val = self.request.get(query)
                    if data[0]['value']:
                        v = data[0]['value']
                    else:
                        v = self.request.get(query)
        if op == 'add' and v:
            if q:
                q = '%s&%s=%s' % (q, query, v)
            else:
                q = '%s=%s' % (query, v)
            return '%s?%s' % (url, q)
        if op == 'add_multi' and v:
            if q:
                q = '%s&%s=%s' % (q, query, v)
            else:
                q = '%s=%s' % (query, v)
            for qs in data[1:]:
                q = '%s&%s=%s' % (q, qs['query'], qs['value'])
            return '%s?%s' % (url, q)
        if op == 'remove' and v:
            q = q.replace('%s=%s&' % (query, v), '')
            q = q.replace('&%s=%s' % (query, v), '')
            q = q.replace('%s=%s' % (query, v), '')
            if q:
                return '%s?%s' % (url, q)
            else:
                return url
        if op == 'arange_first' and v:
            q = q.replace('%s=%s&' % (query, val), '')
            q = q.replace('&%s=%s' % (query, val), '')
            q = q.replace('%s=%s' % (query, val), '')
            if q:
                q = '%s=%s&%s' % (query, v, q)
            else:
                q = '%s=%s' % (query, v)
            return '%s?%s' % (url, q)
        if op == 'arange_last' and v:
            q = q.replace('%s=%s&' % (query, val), '')
            q = q.replace('&%s=%s' % (query, val), '')
            q = q.replace('%s=%s' % (query, val), '')
            if q:
                q = '%s&%s=%s' % (q, query, v)
            else:
                q = '%s=%s' % (query, v)
            return '%s?%s' % (url, q)
            
    def pager(self, count, per_page = 10,  path = '/', page_query = 'page'):
        if page_query not in settings.template_api_pager_page_query_list:
            page_query = 'page' 
        page = self.request.get(page_query)
        page_count = (count / per_page) + (count % per_page and 1)
        if not page:
            page = 1
        else:
            try:
                page = int(page)
            except:
                self.redirect_to(settings.site_error_url_string % '404')
            if page > page_count:
                page = page_count
        self.page = page
        self.count = count
        self.per_page = per_page
        self.page_count = page_count
        self.page_query = page_query
        self.paginator = self._get_paginator(page, page_count, path, page_query)
        
    def _get_paginator(self, page, page_count, path, page_query):
        pagers = []
        if (page - settings.template_api_pager_devider) < 1:
            start = 1
        else:
            start = page - settings.template_api_pager_devider
        if (start + settings.template_api_pager_range) > page_count:
            end = page_count
            if (end - settings.template_api_pager_range) > 1:
                start = end - settings.template_api_pager_range 
        else:
            end = start + settings.template_api_pager_range
        for page_number in range(start, end + 1):
            if page_number != page:
                pagers.append({'title': page_number, 'href': self.get_redirect(path, 'arange_first', [{'query': page_query, 'value': str(page_number)}])})
            else:
                pagers.append({'title': page_number, 'href': False})
        if len(pagers) == 1:
            pagers = False
        return {'page_number': page,
                'pagers': pagers,
                'first_page': self.get_redirect(path, 'arange_first', [{'query': page_query, 'value': str(1)}]),
                'previous_page': self.get_redirect(path, 'arange_first', [{'query': page_query, 'value': str(page - 1)}]),
                'next_page': self.get_redirect(path, 'arange_first', [{'query': page_query, 'value': str(page + 1)}]),
                'last_page': self.get_redirect(path, 'arange_first', [{'query': page_query, 'value': str(page_count)}]),
                'has_previous_page': page - 1 >= 1,
                'has_next_page': page + 1 <= page_count,
                'num_pages': page_count,
                'page_counter_string': settings.template_api_pager_render_counter_string % (page, page_count),}
    
    def pager_offset(self):
        return (self.page - 1) * self.per_page
    
    def render_pager(self):
        output = template.render(os.path.join(core_template_path, 'pager.html'), {'paginator': self.paginator, 'settings': settings})
        return output       


class User(db.Model):
    
    uid = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    user = db.UserProperty(required=True)
    permissions = db.StringListProperty()
    active = db.BooleanProperty(default=True, required=True)
    registered = db.DateTimeProperty(auto_now_add=True, required=True)
    accessed = db.DateTimeProperty(auto_now=True, required=True)
    ip = db.StringProperty()


class UserAccess():
    
    def __init__(self, cookies):
        self.signedin_user = self._get_signedin_user(cookies)
        self.authenticated_user = self._get_authenticated_user()
        self.anonymous_user = self._get_anonymous_user()
        self.current_user = self._get_current_user()
        self.admin_user = users.is_current_user_admin()
        
    def check(self, permission, owner=None):
        if users.is_current_user_admin():
            return True
        if self.signedin_user:
            if not self.signedin_user.active:
                return False
        split_permission = permission.split('_')
        permission_end = split_permission.pop()
        if permission_end == 'own':
            if owner:
                if self.signedin_user:
                    if permission in self.signedin_user.permissions and owner.key() == self.signedin_user.key():
                        return True
                else:
                    if permission in self.anonymous_user.permissions and owner.key() == self.anonymous_user.key():
                        return True
            else:
                return False
        else:
            if self.signedin_user:
                if permission in self.signedin_user.permissions:
                    return True
                elif permission in self.authenticated_user.permissions:
                    return True
            else:
                if permission in self.anonymous_user.permissions:
                    return True
        return False

    def cache_user(self, uid):
        usr = User.get_by_key_name(str(uid))
        if usr:
            memcache.set(key=uid, value=usr, time=3600)
        else:
            user = users.User(email='%s@%s' % (uid, settings.site_domain))
            usr = User(key_name=str(uid), uid=uid, email=user.email(), user=user)
            usr.put()
            memcache.set(key=uid, value=usr, time=3600)
           
    def _get_current_user(self):
        if self.signedin_user:
            return self.signedin_user
        else:
            return self.anonymous_user
    
    def _get_signedin_user(self, cookies):
        user = users.get_current_user()
        cookie = facebook.get_user_from_cookie(cookies, settings.facebook_app_id, settings.facebook_app_secret)
        if user:
            usr = User.get_by_key_name(str(user.user_id()))
            if usr:
                usr.email = user.email()
                usr.ip = os.environ['REMOTE_ADDR']
                usr.put()
                return usr
            else:
                usr = User.gql("WHERE email = :1", user.email()).get()
                if usr:
                    new_usr = User(key_name=str(user.user_id()), uid=user.user_id(), email=user.email(), user=user, permissions=usr.permissions, active=usr.active, registered=usr.registered, ip=os.environ['REMOTE_ADDR'])
                    new_usr.put()
                    usr.delete()
                    return new_usr
                else:
                    usr = User(key_name=str(user.user_id()), uid=user.user_id(), email=user.email(), user=user, ip=os.environ['REMOTE_ADDR'])
                    usr.put()
                    return usr
        elif cookie:
            usr = User.get_by_key_name(cookie["uid"])
            if usr:
                usr.ip = os.environ['REMOTE_ADDR']
                usr.put()
                return usr
            else:
                graph = facebook.GraphAPI(cookie["access_token"])
                profile = graph.get_object("me")
                usr = User.gql("WHERE email = :1", profile["email"]).get()
                if usr:
                    user = users.User(email=profile["email"])
                    new_usr = User(key_name=str(cookie["uid"]), uid=cookie["uid"], email=user.email(), user=user, permissions=usr.permissions, active=usr.active, registered=usr.registered, ip=os.environ['REMOTE_ADDR'])
                    new_usr.put()
                    usr.delete()
                    return new_usr
                else:
                    user = users.User(email=profile["email"])
                    usr = User(key_name=str(cookie["uid"]), uid=cookie["uid"], email=user.email(), user=user, ip=os.environ['REMOTE_ADDR'])
                    usr.put()
                    return usr
        else:
            return None
        
    def _get_authenticated_user(self):
        authenticated_user = memcache.get(settings.user_authenticated)
        if not authenticated_user:
            self.cache_user(settings.user_authenticated)
            authenticated_user = memcache.get(settings.user_authenticated)
        return authenticated_user
        
    def _get_anonymous_user(self):
        anonymous_user = memcache.get(settings.user_anonymous)
        if not anonymous_user:
            self.cache_user(settings.user_anonymous)
            anonymous_user = memcache.get(settings.user_anonymous)
        return anonymous_user

    
class UserLogin(TemplateAPI):
    
    def get(self):
        url = self.request.get('destination')
        if url:
            self.redirect(users.create_login_url(dest_url=url))
        else:
            self.redirect(users.create_login_url(dest_url='/'))
        
        
class UserLogout(TemplateAPI):
    
    def get(self):
        url = self.request.get('destination')
        if url:
            self.redirect(users.create_logout_url(dest_url=url))
        else:
            self.redirect(users.create_logout_url(dest_url='/'))
            
            
class UserManagement(TemplateAPI):
    
    def get(self):
        if users.is_current_user_admin():
            self.access_init()
            query = User.all()
            query.order('email')
            self.pager(query.count(), settings.users_per_page, settings.user_management_url)
            usrs = query.fetch(settings.users_per_page, self.pager_offset())
            usrs_extended = []
            for usr in usrs:
                self.manipulator.formater(usr, [{'name': 'uid', 'type': 'string', 'trim': settings.user_uid_trimmed},
                                                {'name': 'email', 'type': 'string', 'trim': settings.user_email_trimmed},
                                                {'name': 'registered', 'type': 'datetime', 'format': settings.datetime_formated, 'trim': settings.datetime_trimmed},
                                                {'name': 'accessed', 'type': 'datetime', 'format': settings.datetime_formated, 'trim': settings.datetime_trimmed},])
                if usr.key().name() == settings.user_authenticated or usr.key().name() == settings.user_anonymous:
                    usr.checked = True
                    usr.disabled = True
                elif usr.active:
                    usr.checked = True
                    usr.disabled = False
                elif not usr.active:
                    usr.checked = False
                    usr.disabled = False
                usrs_extended.append(usr)
            data = {'title': settings.user_management_title,
                    'users': usrs_extended,
                    'pager': self.render_pager(),
                    'submit_url': self.get_redirect(settings.user_management_url)}
            self.render_html('core', 'user_management_form', data)
        else:
            self.render_error(403)
            
    def post(self):
        if users.is_current_user_admin():
            self.access_init()
            query = User.all()
            query.order('email')
            self.pager(query.count(), settings.users_per_page, settings.user_management_url)
            usrs = query.fetch(settings.users_per_page, self.pager_offset())
            for usr in usrs:
                if usr.key().name() != settings.user_authenticated or usr.key().name() != settings.user_anonymous:
                    usr.active = bool(self.request.get(str(usr.key())))
                    usr.put()
            self.access.cache_user(settings.user_anonymous)
            self.access.cache_user(settings.user_authenticated)
            self.redirect_to(settings.user_management_url)
        else:
            self.render_error(403)
            
                
class UserPermissionAPI(TemplateAPI):
    
    def get_form(self, permissions, url, title=settings.user_permissions_management_title):
        if users.is_current_user_admin():
            self.access_init()
            query = User.all()
            query.order('email')
            self.pager(query.count(), settings.users_per_page, url)
            usrs = query.fetch(settings.users_per_page, self.pager_offset())
            permissions_formated = []
            for permission in permissions:
                permission_trimmed = self.manipulator.trim_string(permission, settings.user_permission_trimmed)
                permissions_formated.append({'title_formated': permission, 'title_trimmed': permission_trimmed})
            usrs_extended = []
            for usr in usrs:
                self.manipulator.formater(usr, [{'name': 'email', 'type': 'string', 'trim': settings.user_email_trimmed}])
                permissions_extended = []
                for permission in permissions:
                    if permission in usr.permissions:
                        permission_extended = {'permission': permission, 'checked': True}
                    else:
                        permission_extended = {'permission': permission, 'checked': False}
                    permissions_extended.append(permission_extended)
                usr.permissions_extended = permissions_extended
                usrs_extended.append(usr)
            data = {'title': title,
                    'users': usrs_extended,
                    'permissions': permissions_formated,
                    'pager': self.render_pager(),
                    'submit_url': self.get_redirect(url)}
            self.render_html('core', 'user_permission_management_form', data)
        else:
            self.render_error(403)
            
    def save_permissions(self, permissions, values, url):
        if users.is_current_user_admin():
            self.access_init()
            query = User.all()
            query.order('email')
            self.pager(query.count(), settings.users_per_page, url)
            usrs = query.fetch(settings.users_per_page, self.pager_offset())
            for usr in usrs:
                key = str(usr.key())
                new_permissions = []
                new_usr_permissions = []
                for usr_permission in usr.permissions:
                    if usr_permission not in permissions:
                        new_usr_permissions.append(usr_permission)
                for value in values:
                    permission = value.split('-')
                    if permission[0] == key:
                        new_permissions.append(unicode(permission[1]))
                new_usr_permissions.extend(new_permissions)
                usr.permissions = new_usr_permissions
                usr.put()
            self.access.cache_user(settings.user_anonymous)
            self.access.cache_user(settings.user_authenticated)
            self.redirect_to(url)
        else:
            self.render_error(403)
            
            
class Menus():
    
    def __init__(self, url):
        self.top = self._get_menus(settings.top_menus, 'top', url)
        self.bottom = self._get_menus(settings.bottom_menus, 'bottom', url)
        self.left = self._get_menus(settings.left_menus, 'left', url)
        self.right = self._get_menus(settings.right_menus, 'right', url)
        
    def _get_menus(self, menus, position, url):
        menus_built = []
        if menus:
            for menu in menus:
                menu_active = []
                for item in menu:
                    if item['path'] == url:
                        item_active = {'path': item['path'], 'name': item['name'], 'description': item['description'], 'active': True}
                    else:
                        item_active = {'path': item['path'], 'name': item['name'], 'description': item['description'], 'active': False}
                    menu_active.append(item_active)
                menus_built.append({'items': menu_active, 'position': position})
            output = template.render(os.path.join(core_template_path, 'menus.html'), {'menus': menus_built, 'position': position})
            return output
        else:
            return ''
    

class Block(db.Model):
    
    title = db.StringProperty(multiline=False, required=True)
    position = db.StringProperty(choices=('top', 'bottom', 'left', 'right'), required=True)
    weight = db.IntegerProperty(default=0, required=True)
    content = db.TextProperty(required=True)
    published = db.BooleanProperty(default=True, required=True)
    owner = db.ReferenceProperty(User, collection_name='block_owners', required=True)
    created = db.DateTimeProperty(auto_now_add=True, required=True)
    updated = db.DateTimeProperty(auto_now=True, required=True)


class BlockCache():
    
    @staticmethod
    def cache_blocks(templateapi):
        blocks = BlockCache._get_db_blocks()
        block_keys_top = []
        block_keys_bottom = []
        block_keys_left = []
        block_keys_right = []
        block_cache = {}
        for block in blocks:
            templateapi.manipulator.formater(block, [{'name': 'title', 'type': 'unicode', 'trim': settings.block_title_trimmed},
                                                     {'name': 'content', 'type': 'html', 'escape': False}])
            if block.position == 'top':
                block_keys_top.append(str(block.key()))
            elif block.position == 'bottom':
                block_keys_bottom.append(str(block.key()))
            elif block.position == 'left':
                block_keys_left.append(str(block.key()))
            elif block.position == 'right':
                block_keys_right.append(str(block.key()))
            block_cache[str(block.key())] = block
        if block_keys_top:
            memcache.set(key='block_keys_top', value=block_keys_top, time=3600)
        else:
            memcache.set(key='block_keys_top', value='empty', time=3600)
        if block_keys_bottom:
            memcache.set(key='block_keys_bottom', value=block_keys_bottom, time=3600)
        else:
            memcache.set(key='block_keys_bottom', value='empty', time=3600)
        if block_keys_left:
            memcache.set(key='block_keys_left', value=block_keys_left, time=3600)
        else:
            memcache.set(key='block_keys_left', value='empty', time=3600)
        if block_keys_right:
            memcache.set(key='block_keys_right', value=block_keys_right, time=3600)
        else:
            memcache.set(key='block_keys_right', value='empty', time=3600)
        if block_cache:
            memcache.set_multi(block_cache, time=3600)
    
    @staticmethod        
    def _get_db_blocks():
        query = Block.all()
        query.filter('published = ', True)
        query.order('weight')
        return query.fetch(settings.blocks_per_request)
    
    
class Blocks():
    
    def __init__(self, templateapi):
        self.top = self._get_blocks('top', templateapi)
        self.bottom = self._get_blocks('bottom', templateapi)
        self.left = self._get_blocks('left', templateapi)
        self.right = self._get_blocks('right', templateapi)

    def _get_blocks(self, position, templateapi):
        blocks = []
        block_keys = memcache.get('block_keys_%s' % position)
        if block_keys == 'empty':
            return ''
        else:
            if not block_keys:
                BlockCache.cache_blocks(templateapi)
                block_keys = memcache.get('block_keys_%s' % position)
            cached_blocks = memcache.get_multi(block_keys)
            if not cached_blocks:
                BlockCache.cache_blocks(templateapi)
                cached_blocks = memcache.get_multi(block_keys)
            unsorted_blocks = []
            for block in cached_blocks.values():
                if templateapi.access.check('block_view_%s' % str(block.key().id())):
                    unsorted_blocks.append(block)
            filtered_blocks = sorted(unsorted_blocks, key=lambda block: block.weight)
            for filtered_block in filtered_blocks:
                blocks.append(filtered_block.content)
            output = template.render(os.path.join(core_template_path, 'blocks.html'), {'blocks': blocks})
            return output
        

class BlockAdd(TemplateAPI):
    
    def get(self):
        self.access_init()
        if self.access.check('block_add'):
            data = {'title': settings.block_add_title,
                    'weights': range(settings.blocks_per_request),
                    'positions': settings.block_positions,
                    'content_editor': self.ckeditor.editor('block_content'),
                    'submit_url': self.get_redirect(settings.block_add_url),
                    'cancel_url': self.get_redirect(settings.block_add_redirect_url),}
            self.render_html('core', 'block_add_form', data)
        else:
            self.render_error(403)
            
    def post(self):
        self.access_init()
        if self.access.check('block_add'):
            try:
                title = unicode(self.request.get('title'))
                position = unicode(self.request.get('position'))
                weight = int(self.request.get('weight'))
                content = db.Text(unicode(self.request.get('block_content')))
                published = bool(self.request.get('published'))
                owner = self.access.current_user
                block = Block(title=title, position=position, weight=weight, content=content, published=published, owner=owner)
                block.put()
                BlockCache.cache_blocks(self)
                self.redirect_to(settings.block_add_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)


class BlockEdit(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('block_edit'):
            try:
                block = Block.get_by_id(int(id))
                self.manipulator.formater(block, [{'name': 'title', 'type': 'unicode', 'trim': settings.block_title_trimmed},
                                                  {'name': 'content', 'type': 'html', 'escape': True}])
                weights = range(settings.blocks_per_request)
                weights_selected = []
                for weight in weights:
                    if weight == block.weight:
                        weight_selected = {'value': weight, 'selected': True}
                    else:
                        weight_selected = {'value': weight, 'selected': False}
                    weights_selected.append(weight_selected)
                positions_selected = []
                for position in settings.block_positions:
                    if position['value'] == block.position:
                        position_selected = {'value': position['value'], 'label': position['label'], 'selected': True}
                    else:
                        position_selected = {'value': position['value'], 'label': position['label'], 'selected': False}
                    positions_selected.append(position_selected)
                data = {'title': settings.block_edit_title,
                        'block': block,
                        'weights': weights_selected,
                        'positions': positions_selected,
                        'content_editor': self.ckeditor.editor('block_content', block.content_formated),
                        'submit_url': self.get_redirect(settings.block_edit_url_string % str(block.key().id())),
                        'cancel_url': self.get_redirect(settings.block_edit_redirect_url),}
                self.render_html('core', 'block_edit_form', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
        
    def post(self, id):
        self.access_init()
        if self.access.check('block_edit'):
            try:
                block = Block.get_by_id(int(id))
                block.title = unicode(self.request.get('title'))
                block.position = unicode(self.request.get('position'))
                block.weight = int(self.request.get('weight'))
                block.content = db.Text(unicode(self.request.get('block_content')))
                block.published = bool(self.request.get('published'))
                block.put()
                BlockCache.cache_blocks(self)
                self.redirect_to(settings.block_edit_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

        
class BlockDelete(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('block_delete'):
            try:
                block = Block.get_by_id(int(id))
                self.manipulator.formater(block, [{'name': 'title', 'type': 'unicode', 'trim': settings.block_title_trimmed},
                                                  {'name': 'content', 'type': 'html', 'escape': False}])
                data = {'title': settings.block_delete_title,
                        'block': block,
                        'delete_question': settings.block_delete_form_label_question_string % block.title_formated,
                        'submit_url': self.get_redirect(settings.block_delete_url_string % str(block.key().id())),
                        'cancel_url': self.get_redirect(settings.block_delete_redirect_url)}
                self.render_html('core', 'block_delete_form', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
        
    def post(self, id):
        self.access_init()
        if self.access.check('block_delete'):
            try:
                block = Block.get_by_id(int(id))
                block.delete()
                BlockCache.cache_blocks(self)
                self.redirect_to(settings.block_delete_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

            
class BlockManagement(TemplateAPI):

    def get(self):
        self.access_init()
        if self.access.check('block_edit') or self.access.check('block_delete'):
            query = Block.all()
            query.order('weight')
            self.pager(query.count(), settings.blocks_per_page, settings.block_management_url)
            blocks = query.fetch(settings.blocks_per_page, self.pager_offset())
            blocks_extended = []
            for block in blocks:
                self.manipulator.formater(block, [{'name': 'title', 'type': 'unicode', 'trim': settings.block_title_trimmed},
                                                  {'name': 'content', 'type': 'html', 'escape': False}])
                block.edit_url = self.get_redirect(settings.block_edit_url_string % str(block.key().id()))
                block.delete_url = self.get_redirect(settings.block_delete_url_string % str(block.key().id()))
                block.view_permissions_url = self.get_redirect(settings.block_view_permissions_url_string % str(block.key().id()))
                blocks_extended.append(block)
            data = {'title': settings.block_management_title,
                    'blocks': blocks_extended,
                    'pager': self.render_pager(),
                    'add_url': self.get_redirect(settings.block_add_url),
                    'permissions_url': self.get_redirect(settings.block_permissions_url),
                    'block_add': self.access.check('block_add'),
                    'block_edit': self.access.check('block_edit'),
                    'block_delete': self.access.check('block_delete'),
                    'block_permissions': self.access.admin_user}
            self.render_html('core', 'block_management_form', data)
        else:
            self.render_error(403)


class BlockPermissions(UserPermissionAPI):
    
    def get(self):
        self.get_form(permissions=['block_add', 'block_edit', 'block_delete'], url=settings.block_permissions_url, title=settings.block_permissions_title)
        
    def post(self):
        values = self.request.get_all('user-permissions')
        self.save_permissions(permissions=['block_add', 'block_edit', 'block_delete'], values=values, url=settings.block_permissions_url)


class BlockViewPermissions(UserPermissionAPI):
    
    def get(self, id):
        try:
            block = Block.get_by_id(int(id))
            self.get_form(permissions=['block_view_%s' % str(block.key().id())], url=settings.block_view_permissions_url_string % str(block.key().id()), title=settings.block_view_permissions_title_string % block.title)
        except:
            self.render_error(404)
        
    def post(self, id):
        try:
            block = Block.get_by_id(int(id))
            values = self.request.get_all('user-permissions')
            self.save_permissions(permissions=['block_view_%s' % str(block.key().id())], values=values, url=settings.block_view_permissions_url_string % str(block.key().id()))
        except:
            self.render_error(404)


class CKEditor():

    """
    Usage of this class is simple 
     Editor = CKEDITOR(path = 'path to the cke editor folder')
     editorHTML = Editor.editor('name of textarea that needs editor', 'a value string that should populate the textarea of editor', { an object of options for more info see cke documentation}, { textarea attributes, height, width etc})
     Note that you shouldnt instance multiple CKEDITOR since it may include already included .js files.
     you can use editor = CKEDITOR()  editor.editor(........) like in example above
     the editorHTML var now contains string html that you can pass to your template engine!
    @author Vertazzar
    """
    
    # please be advised that you must provide path to the ckeditor folder, in format '/somefolder/ckeditorfolder/'
    def __init__(self, path = '/static/add-ons/ckeditor/'):
        self.path = path
        self.loaded = False

    def load(self):
        if not self.loaded:
            str = self.script("window.CKEDITOR_BASEPATH='%s';" % (self.path))
            str += "<script type=\"text/javascript\" src=\"%sckeditor.js\"></script>\n" % (self.path);
            self.loaded = True
            return str
    
    def script(self, js):
        out = "<script type=\"text/javascript\">";
        out += "//<![CDATA[\n";
        out += js;
        out += "\n//]]>";
        out += "</script>\n";
        return out;
    
    def return_attrs(self, attributes = []):
        responser = []
        if len(attributes) != 0:
            for k,v in attributes.iteritems():
                responser.append(' %(key)s = "%(value)s" ' % {'key': k, 'value': v})
        return responser.join('')

    """ 
    @attention passing value must be html escaped to pervent script injections and whatsoever
    """
    def editor(self, textarea_name, value = '', options = {'resize_enabled' : 'false', 'height':'500px','removePlugins': 'forms,a11yhelp,scayt,about'}, textarea_attributes = []):
        html = ''
        js = ''
        attributes = ''      
        html += self.load()
        if len(textarea_attributes) != 0:
            attributes = self.return_attrs(textarea_attributes)
        html += '<textarea %(attr)s name="%(name)s">%(val)s</textarea>' % {'attr': attributes, 'val' : value, 'name' : textarea_name}
        if len(options) == 0:
            js += "CKEDITOR.replace('%s');" % (textarea_name)
        else:
            js += "CKEDITOR.replace('%(tname)s', %(opts)s);" % {'tname' : textarea_name, 'opts' : json.dumps(options)}
        html += self.script(js)
        return html
    

class ContentManipulator():
    
    @staticmethod
    def trim_string(string, limit, offset = 0, end = '...'):
        try:
            string = unicode(string)
            string_lenght = len(string)
            string = string[offset:limit+offset]
            if string_lenght != len(string):
                string += end
            return string
        except:
            return string
    
    @staticmethod    
    def truncate_string(value, limit = 80, offset = 0, end = ' ...'):
        """
        Truncates a string after a given number of chars keeping whole words.
        
        Usage:
            {{ string|truncatesmart }}
            {{ string|truncatesmart:50 }}
        """
        
        try:
            limit = int(limit)
        # invalid literal for int()
        except ValueError:
            # Fail silently.
            return value
        
        # Make sure it's unicode
        value = unicode(value)
        
        # Return the string itself if length is smaller or equal to the limit
        if len(value) <= limit:
            return value
        
        # Cut the string
        value = value[offset:limit+offset]
        
        # Break into words and remove the last
        if offset:
            words = value.split(' ')[1:-1]
        else:
            words = value.split(' ')[:-1]
        
        # Join the words and return
        return ' '.join(words) + end
    
    @staticmethod
    def trim_html(string, length, ellipsis = '...'):
        #skratiti "html" za dati "limit" poèevši od datog "offset-a", vodeæi raèuna da ne doðe do prekida tagova
        tag_end_re = re.compile(r'(\w+)[^>]*>')
        entity_end_re = re.compile(r'(\w+;)')
 
        """Truncate HTML string, preserving tag structure and character entities."""
        length = int(length)
        output_length = 0
        i = 0
        pending_close_tags = {}
        
        while output_length < length and i < len(string):
            c = string[i]
    
            if c == '<':
                # probably some kind of tag
                if i in pending_close_tags:
                    # just pop and skip if it's closing tag we already knew about
                    i += len(pending_close_tags.pop(i))
                else:
                    # else maybe add tag
                    i += 1
                    match = tag_end_re.match(string[i:])
                    if match:
                        tag = match.groups()[0]
                        i += match.end()
      
                        # save the end tag for possible later use if there is one
                        match = re.search(r'(</' + tag + '[^>]*>)', string[i:], re.IGNORECASE)
                        if match:
                            pending_close_tags[i + match.start()] = match.groups()[0]
                    else:
                        output_length += 1 # some kind of garbage, but count it in
                        
            elif c == '&':
                # possible character entity, we need to skip it
                i += 1
                match = entity_end_re.match(string[i:])
                if match:
                    i += match.end()
    
                # this is either a weird character or just '&', both count as 1
                output_length += 1
            else:
                # plain old characters
                
                skip_to = string.find('<', i, i + length)
                if skip_to == -1:
                    skip_to = string.find('&', i, i + length)
                if skip_to == -1:
                    skip_to = i + length
                    
                # clamp
                delta = min(skip_to - i,
                            length - output_length,
                            len(string) - i)
    
                output_length += delta
                i += delta
                            
        output = [string[:i]]
        if output_length == length:
            output.append(ellipsis)
    
        for k in sorted(pending_close_tags.keys()):
            output.append(pending_close_tags[k])
    
        return "".join(output)
    
    @staticmethod
    def extract_tags(html, tags, limit = 'all', offset = 0):
        BS = BeautifulSoup(html)
        tag_selection = []
        try:
            if limit == 'all':
                tag_selection = BS.findAll(tags)
            else:
                try:
                    limit = int(limit)
                    offset = int(offset)
                    for possition in range(offset, limit):
                        tag_selection.append(BS.findAll(tags)[possition])
                except:
                    pass
            return tag_selection
        except:
            return html
    
    @staticmethod
    def remove_tags(html, tags, limit = 'all', offset = 0):
        while True:
            BS = BeautifulSoup(html)
            removed = False
            tag_selection = []
            try:
                if limit == 'all':
                    tag_selection = BS.findAll(tags)
                else:
                    try:
                        limit = int(limit)
                        offset = int(offset)
                        for possition in range(offset, limit):
                            tag_selection.append(BS.findAll(tags)[possition])
                    except:
                        pass    
                for tag in tag_selection:
                    if isinstance(tags, list):
                        if tag.name in tags:
                            tag.extract()
                            removed = True
                    else:
                        tag.extract()
                        removed = True
                
                html = unicode(BS)
                
                if removed:
                    continue
                
                return html
            except:
                return ''
        
    @staticmethod
    def remove_attributes(html, tags, attributes, attribute_values = []):
        BS = BeautifulSoup(html)
        tag_selection = []
        try:
            tag_selection = BS.findAll(tags)
            for tag in tag_selection:
                attribute_selection = tag.attrs #tag._getAttrMap().keys()
                for attr in attribute_selection:
                    if attr[0] in attributes:
                        del tag[attr[0]]
                    elif attribute_values:
                        for attribute_value in attribute_values:
                            if re.search(attribute_value, attr[-1]):
                                del tag[attr[0]]
            
            return unicode(BS)
        except:
            return ''
        
    @staticmethod
    def hide_tags(html, tags, limit = 'all', offset = 0):
        while True:
            BS = BeautifulSoup(html)
            hidden = False
            tag_selection = []
            try:
                if limit == 'all':
                    tag_selection = BS.findAll(tags)
                else:
                    try:
                        limit = int(limit)
                        offset = int(offset)
                        for possition in range(offset, limit):
                            tag_selection.append(BS.findAll(tags)[possition])
                    except:
                        pass    
                for tag in tag_selection:
                    if isinstance(tags, list):
                        if tag.name in tags:
                            tag.hidden = True
                            hidden = True
                    else:
                        tag.hidden = True
                        hidden = True
                
                html = unicode(BS)
                
                if hidden:
                    continue
                
                return html
            except:
                return ''
    
    @staticmethod
    def esc(value):
        return escape(value)
    
    @staticmethod
    def formater(object, properties):
        for property in properties:
            if property['type'] == 'string':
                new_property = getattr(object, property['name'])
                #property_formated = escape(str(new_property))
                property_formated = str(new_property)
                setattr(object, property['name'] + '_formated', property_formated)
                if property.has_key('trim'):
                    property_trimmed = ContentManipulator.trim_string(property_formated, property['trim'])
                    setattr(object, property['name'] + '_trimmed', property_trimmed)
            elif property['type'] == 'unicode':
                new_property = getattr(object, property['name'])
                #property_formated = escape(unicode(new_property))
                property_formated = unicode(new_property)
                setattr(object, property['name'] + '_formated', property_formated)
                if property.has_key('trim'):
                    property_trimmed = ContentManipulator.trim_string(property_formated, property['trim'])
                    setattr(object, property['name'] + '_trimmed', property_trimmed)
            elif property['type'] == 'html':
                new_property = getattr(object, property['name'])
                if property['escape']:
                    property_formated = escape(unicode(new_property))
                    #property_formated = unicode(new_property)
                    setattr(object, property['name'] + '_formated', property_formated)
                else:
                    property_formated = ContentManipulator.remove_tags(unicode(new_property), settings.content_manipulator_formater_forbidden_tags)
                    property_formated = ContentManipulator.remove_attributes(property_formated, True, settings.content_manipulator_formater_forbidden_attributes, settings.content_manipulator_formater_forbidden_attribute_values) 
                    setattr(object, property['name'] + '_formated', property_formated)
            elif property['type'] == 'datetime':
                new_property = getattr(object, property['name'])
                property_formated = new_property.strftime(property['format'])
                setattr(object, property['name'] + '_formated', property_formated)
                property_trimmed = new_property.strftime(property['trim'])
                setattr(object, property['name'] + '_trimmed', property_trimmed)
    
    
class SiteError(TemplateAPI):
    
    def get(self, status_code):
        self.render_error(int(status_code))


app = webapp.WSGIApplication(
        [(settings.site_error_url, SiteError),
         (settings.user_management_url, UserManagement),
         (settings.user_login_url, UserLogin),
         (settings.user_logout_url, UserLogout),
         (settings.block_add_url, BlockAdd),
         (settings.block_edit_url, BlockEdit),
         (settings.block_delete_url, BlockDelete),
         (settings.block_management_url, BlockManagement),
         (settings.block_permissions_url, BlockPermissions),
         (settings.block_view_permissions_url, BlockViewPermissions),],
        debug=True)
        
'''def main():
    application = webapp.WSGIApplication(
        [(settings.site_error_url, SiteError),
         (settings.user_management_url, UserManagement),
         (settings.user_login_url, UserLogin),
         (settings.user_logout_url, UserLogout),
         (settings.block_add_url, BlockAdd),
         (settings.block_edit_url, BlockEdit),
         (settings.block_delete_url, BlockDelete),
         (settings.block_management_url, BlockManagement),
         (settings.block_permissions_url, BlockPermissions),
         (settings.block_view_permissions_url, BlockViewPermissions),],
        debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()      '''