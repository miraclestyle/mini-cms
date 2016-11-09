#coding=UTF-8
'''
Created on Jan 7, 2011

@author: elvin
'''
import settings
import os
import random
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import memcache
from core import TemplateAPI, User, UserAccess, UserPermissionAPI, Block, Blocks, SiteError
from photo import Photo, PhotoAPI


class Sponsor(db.Model):
    
    title = db.StringProperty(multiline=False, required=True)
    url = db.LinkProperty(required=True) #db.StringProperty(multiline=False, required=True)
    probability = db.IntegerProperty(required=True)
    logo = db.ReferenceProperty(Photo, collection_name='sponsor_logos')
    published = db.BooleanProperty(default=True, required=True)
    record_clicks = db.BooleanProperty(default=False, required=True)
    record_impressions = db.BooleanProperty(default=False, required=True)
    owner = db.ReferenceProperty(User, collection_name='sponsor_owners', required=True)
    created = db.DateTimeProperty(auto_now_add=True, required=True)
    updated = db.DateTimeProperty(auto_now=True, required=True)
    
class SponsorClick(db.Model):
    
    sponsor = db.ReferenceProperty(Sponsor, collection_name='sponsor_click_sponsors', required=True)
    user = db.ReferenceProperty(User, collection_name='sponsor_click_users', required=True)
    agent = db.StringProperty(multiline=False, required=True, default='')
    recorded = db.DateTimeProperty(auto_now_add=True, required=True)
    source = db.StringProperty()
    
class SponsorImpression(db.Model):
    
    sponsor = db.ReferenceProperty(Sponsor, collection_name='sponsor_impression_sponsors', required=True)
    user = db.ReferenceProperty(User, collection_name='sponsor_impression_users', required=True)
    agent = db.StringProperty(multiline=False, required=True, default='')
    recorded = db.DateTimeProperty(auto_now_add=True, required=True)
    source = db.StringProperty()
    

class SponsorAdd(TemplateAPI):
    
    def get(self):
        self.access_init()
        if self.access.check('sponsor_add'):
            data = {'title': settings.sponsor_add_title,
                    'probabilities': settings.sponsor_probabilities,
                    'submit_url': self.get_redirect(settings.sponsor_add_url),
                    'cancel_url': self.get_redirect(settings.sponsor_add_redirect_url)}
            self.render_html('sponsor', 'sponsor_add_form', data)
        else:
            self.render_error(403)
            
    def post(self):
        self.access_init()
        if self.access.check('sponsor_add'):
            try:
                title = unicode(self.request.get('title'))
                url = db.Link(self.request.get('url'))
                probability = int(self.request.get('probability'))
                if self.request.get('sponsor-logo'):
                    logo = db.Key(encoded=self.request.get('sponsor-logo'))
                else:
                    logo = None
                published = bool(self.request.get('published'))
                record_clicks = bool(self.request.get('record-clicks'))
                record_impressions = bool(self.request.get('record-impressions'))
                owner = self.access.current_user
                sponsor = Sponsor(title=title, url=url, probability=probability, logo=logo, published=published, record_clicks=record_clicks, record_impressions=record_impressions, owner=owner)
                sponsor.put()
                SponsorCache.cache_sponsors(self)
                self.redirect_to(settings.sponsor_add_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)


class SponsorEdit(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('sponsor_edit'):
            try:
                photo = PhotoAPI(self)
                sponsor = Sponsor.get_by_id(int(id))
                self.manipulator.formater(sponsor, [{'name': 'title', 'type': 'unicode', 'trim': settings.sponsor_title_trimmed},
                                                    {'name': 'url', 'type': 'unicode'}])
                probabilities_selected = []
                for probability in settings.sponsor_probabilities:
                    if probability['value'] == sponsor.probability:
                        probability_selected = {'value': probability['value'], 'label': probability['label'], 'selected': True}
                    else:
                        probability_selected = {'value': probability['value'], 'label': probability['label'], 'selected': False}
                    probabilities_selected.append(probability_selected)
                sponsor_logo_src = ''
                try:
                    if sponsor.logo:
                        sponsor_logo = photo.get_photo(sponsor.logo.key(), False, settings.sponsor_logo_w, settings.sponsor_logo_h)
                        if sponsor_logo:
                            sponsor_logo_src = sponsor_logo.src
                except:
                    pass
                data = {'title': settings.sponsor_edit_title,
                        'sponsor': sponsor,
                        'probabilities': probabilities_selected,
                        'sponsor_logo_src': sponsor_logo_src,
                        'submit_url': self.get_redirect(settings.sponsor_edit_url_string % str(sponsor.key().id())),
                        'cancel_url': self.get_redirect(settings.sponsor_edit_redirect_url)}
                self.render_html('sponsor', 'sponsor_edit_form', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
        
    def post(self, id):
        self.access_init()
        if self.access.check('sponsor_edit'):
            try:
                sponsor = Sponsor.get_by_id(int(id))
                sponsor.title = unicode(self.request.get('title'))
                sponsor.url = db.Link(self.request.get('url'))
                sponsor.probability = int(self.request.get('probability'))
                if self.request.get('sponsor-logo'):
                    sponsor.logo = db.Key(encoded=self.request.get('sponsor-logo'))
                else:
                    sponsor.logo = None
                sponsor.published = bool(self.request.get('published'))
                sponsor.record_clicks = bool(self.request.get('record-clicks'))
                sponsor.record_impressions = bool(self.request.get('record-impressions'))
                sponsor.put()
                SponsorCache.cache_sponsors(self)
                self.redirect_to(settings.sponsor_edit_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

        
class SponsorDelete(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('sponsor_delete'):
            try:
                photo = PhotoAPI(self)
                sponsor = Sponsor.get_by_id(int(id))
                self.manipulator.formater(sponsor, [{'name': 'title', 'type': 'unicode', 'trim': settings.sponsor_title_trimmed},
                                                    {'name': 'url', 'type': 'unicode'}])
                sponsor_logo_src = ''
                try:
                    if sponsor.logo:
                        sponsor_logo = photo.get_photo(sponsor.logo.key(), False, settings.sponsor_logo_w, settings.sponsor_logo_h)
                        if sponsor_logo:
                            sponsor_logo_src = sponsor_logo.src
                except:
                    pass
                data = {'title': settings.sponsor_delete_title,
                        'sponsor': sponsor,
                        'sponsor_logo_src': sponsor_logo_src,
                        'delete_question': settings.sponsor_delete_form_label_question_string % sponsor.title_formated,
                        'submit_url': self.get_redirect(settings.sponsor_delete_url_string % str(sponsor.key().id())),
                        'cancel_url': self.get_redirect(settings.sponsor_delete_redirect_url)}
                self.render_html('sponsor', 'sponsor_delete_form', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)
        
    def post(self, id):
        self.access_init()
        if self.access.check('sponsor_delete'):
            try:
                sponsor = Sponsor.get_by_id(int(id))
                sponsor.delete()
                SponsorCache.cache_sponsors(self)
                self.redirect_to(settings.sponsor_delete_redirect_url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

            
class SponsorManagement(TemplateAPI):

    def get(self):
        self.access_init()
        if self.access.check('sponsor_view') or self.access.check('sponsor_edit') or self.access.check('sponsor_delete'):
            photo = PhotoAPI(self)
            query = Sponsor.all()
            query.order('-created')
            self.pager(query.count(), settings.sponsors_per_page, settings.sponsor_management_url)
            sponsors = query.fetch(settings.sponsors_per_page, self.pager_offset())
            sponsors_extended = []
            for sponsor in sponsors:
                self.manipulator.formater(sponsor, [{'name': 'title', 'type': 'unicode', 'trim': settings.sponsor_title_trimmed},
                                                    {'name': 'url', 'type': 'unicode'}])
                sponsor.logo_src = ''
                try:
                    if sponsor.logo:
                        sponsor_logo = photo.get_photo(sponsor.logo.key(), False, settings.sponsor_logo_w, settings.sponsor_logo_h)
                        if sponsor_logo:
                            sponsor.logo_src = sponsor_logo.src
                except:
                    pass
                sponsor.view_url = self.get_redirect(settings.sponsor_view_url_string % str(sponsor.key().id()))
                sponsor.edit_url = self.get_redirect(settings.sponsor_edit_url_string % str(sponsor.key().id()))
                sponsor.delete_url = self.get_redirect(settings.sponsor_delete_url_string % str(sponsor.key().id()))
                sponsors_extended.append(sponsor)
            data = {'title': settings.sponsor_management_title,
                    'sponsors': sponsors_extended,
                    'pager': self.render_pager(),
                    'add_url': self.get_redirect(settings.sponsor_add_url),
                    'permissions_url': self.get_redirect(settings.sponsor_permissions_url),
                    'sponsor_view': self.access.check('sponsor_view'),
                    'sponsor_add': self.access.check('sponsor_add'),
                    'sponsor_edit': self.access.check('sponsor_edit'),
                    'sponsor_delete': self.access.check('sponsor_delete'),
                    'sponsor_permissions': self.access.admin_user}
            self.render_html('sponsor', 'sponsor_management_form', data)
        else:
            self.render_error(403)


class SponsorPermissions(UserPermissionAPI):
    
    def get(self):
        self.get_form(permissions=['sponsor_view_ads', 'sponsor_view', 'sponsor_add', 'sponsor_edit', 'sponsor_delete'], url=settings.sponsor_permissions_url, title=settings.sponsor_permissions_title)
        
    def post(self):
        values = self.request.get_all('user-permissions')
        self.save_permissions(permissions=['sponsor_view_ads', 'sponsor_view', 'sponsor_add', 'sponsor_edit', 'sponsor_delete'], values=values, url=settings.sponsor_permissions_url)

            
class SponsorView(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('sponsor_view') or self.access.check('sponsor_edit') or self.access.check('sponsor_delete'):
            try:
                sponsor = Sponsor.get_by_id(int(id))
                self.manipulator.formater(sponsor, [{'name': 'title', 'type': 'unicode', 'trim': settings.sponsor_title_trimmed},
                                                    {'name': 'url', 'type': 'unicode'}])
                photo = PhotoAPI(self)
                probability_selected = ''
                for probability in settings.sponsor_probabilities:
                    if probability['value'] == sponsor.probability:
                        probability_selected = {'value': probability['value'], 'label': probability['label'], 'selected': True}
                sponsor_logo_src = ''
                try:
                    if sponsor.logo:
                        sponsor_logo = photo.get_photo(sponsor.logo.key(), True, settings.sponsor_logo_w, settings.sponsor_logo_h)
                        if sponsor_logo:
                            sponsor_logo_src = sponsor_logo.src
                except:
                    pass
                if sponsor.record_clicks:
                    query = SponsorClick.all()
                    query.filter('sponsor = ', sponsor)
                    clicks = query.count()
                else:
                    clicks = settings.sponsor_record_clicks_message
                if sponsor.record_impressions:
                    query = SponsorImpression.all()
                    query.filter('sponsor = ', sponsor)
                    impressions = query.count()
                else:
                    impressions = settings.sponsor_record_impressions_message
                data = {'title': settings.sponsor_view_title,
                        'sponsor': sponsor,
                        'noindex': True,
                        'clicks': clicks,
                        'impressions': impressions,
                        'probability': probability_selected,
                        'sponsor_logo_src': sponsor_logo_src}
                self.render_html('sponsor', 'sponsor_view', data)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

            
class SponsorsView(TemplateAPI):

    def get(self):
        self.access_init()
        if self.access.check('sponsor_view_ads'):
            photo = PhotoAPI(self)
            query = Sponsor.all()
            query.filter('published = ', True)
            query.order('title')
            self.pager(query.count(), settings.sponsors_per_page, settings.sponsors_view_url)
            sponsors = query.fetch(settings.sponsors_per_page, self.pager_offset())
            sponsors_extended = []
            for sponsor in sponsors:
                self.manipulator.formater(sponsor, [{'name': 'title', 'type': 'unicode', 'trim': settings.sponsor_title_trimmed},
                                                    {'name': 'url', 'type': 'unicode'}])
                sponsor.logo_src = ''
                try:
                    if sponsor.logo:
                        sponsor_logo = photo.get_photo(sponsor.logo.key(), True, settings.sponsor_logo_w, settings.sponsor_logo_h)
                        if sponsor_logo:
                            sponsor.logo_src = sponsor_logo.src
                except:
                    pass
                sponsor.redirect_url = self.get_redirect(settings.sponsor_redirect_url_string % str(sponsor.key().id()))
                sponsors_extended.append(sponsor)
                if sponsor.record_impressions:
                    user = self.access.current_user
                    agent = os.environ['HTTP_USER_AGENT']
                    source = os.environ['REMOTE_ADDR']
                    sponsorimpression = SponsorImpression(sponsor=sponsor, user=user, agent=agent, source=source)
                    sponsorimpression.put()
            data = {'title': settings.sponsors_view_title,
                    'sponsors': sponsors_extended,
                    'background': settings.sponsors_view_background,
                    'pager': self.render_pager()}
            self.render_html('sponsor', 'sponsors_view', data)
        else:
            self.render_error(403)

class SponsorCache():
    
    @staticmethod
    def cache_sponsors(templateapi):
        sponsors = SponsorCache._get_db_sponsors()
        sponsor_keys = []
        sponsor_cache = {}
        for sponsor in sponsors:
            templateapi.manipulator.formater(sponsor, [{'name': 'title', 'type': 'unicode', 'trim': settings.sponsor_title_trimmed},
                                                       {'name': 'url', 'type': 'unicode'}])
            sponsor_keys.append(str(sponsor.key()))
            sponsor_cache[str(sponsor.key())] = sponsor
        if sponsor_keys:
            memcache.set(key='sponsor_keys', value=sponsor_keys, time=3600)
        else:
            memcache.set(key='sponsor_keys', value='empty', time=3600)
        if sponsor_cache:
            memcache.set_multi(sponsor_cache, time=3600)
    
    @staticmethod        
    def _get_db_sponsors():
        query = Sponsor.all()
        query.filter('published = ', True)
        query.order('-probability')
        sponsors = query.fetch(settings.sponsors_per_request)
        return sponsors
    
    
class SponsorBlocks(TemplateAPI):
            
    def get(self):
        self.access_init()
        if self.access.check('sponsor_view_ads'):
            sponsors = []
            sponsor_keys = memcache.get('sponsor_keys')
            if sponsor_keys == 'empty':
                return ''
            else:
                if not sponsor_keys:
                    SponsorCache.cache_sponsors(self)
                    sponsor_keys = memcache.get('sponsor_keys')
                cached_sponsors = memcache.get_multi(sponsor_keys)
                if not cached_sponsors:
                    SponsorCache.cache_sponsors(self)
                    cached_sponsors = memcache.get_multi(sponsor_keys)
                selected_sponsors = self._select_sponsors(cached_sponsors, settings.sponsors_per_block)
                photo = PhotoAPI(self)
                for sponsor in selected_sponsors:
                    sponsor.logo_src = ''
                    try:
                        if sponsor.logo:
                            sponsor_logo = photo.get_photo(sponsor.logo.key(), True, settings.sponsor_block_logo_w, settings.sponsor_block_logo_h)
                            if sponsor_logo:
                                sponsor.logo_src = sponsor_logo.src
                    except:
                        pass
                    sponsor.redirect_url = self.get_redirect(settings.sponsor_redirect_url_string % str(sponsor.key().id()))
                    sponsors.append(sponsor)
                    if sponsor.record_impressions:
                        user = self.access.current_user
                        agent = os.environ['HTTP_USER_AGENT']
                        source = os.environ['REMOTE_ADDR']
                        sponsorimpression = SponsorImpression(sponsor=sponsor, user=user, agent=agent, source=source)
                        sponsorimpression.put()
                data = {'sponsors': sponsors,
                        'ajax': True}
                self.render_html('sponsor', 'sponsor_blocks', data)
        else:
            return ''
    
    def _select_sponsors(self, sponsors, quantity = 1):
        weighted_sponsors = self._build_sponsors_weight(sponsors)
        selectable = weighted_sponsors
        select = 0
        selected = []
        for weighted_sponsor in weighted_sponsors:
            available = len(selectable)
            select += 1
            sponsor = 0
            if sponsor == 0:
                if available > 1:
                    sponsor = selectable[random.randint(0, available - 1)]
                else:
                    sponsor = selectable[0]
                selected.append(sponsor)
                selectable = self._strip_sponsors(selectable, sponsor)
            if quantity == select or len(selectable) == 0:
                break
        return selected
                
    def _strip_sponsors(self, strip_sponsors, sponsor):
        selectable = []
        for strip_sponsor in strip_sponsors:
            if str(sponsor.key()) != str(strip_sponsor.key()):
                selectable.append(strip_sponsor)
        return selectable
    
    def _build_sponsors_weight(self, sponsors):
        display = []
        probabilities = []
        for sponsor in sponsors.values():
            probabilities.append(sponsor.probability)
        gcd = self._calculate_gcd(probabilities)
        for sponsor in sponsors.values():
            weight = sponsor.probability / gcd
            for i in range(1, weight + 1):
                display.append(sponsor)
        return display
    
    def _calculate_gcd(self, integers = []):
        gcd = integers.pop(0)
        while (0 != len(integers)):
            gcd = self._gcd(gcd, integers.pop(0))
        return gcd
    
    def _gcd(self, x, y):
        while x%y != 0:
            r=x%y
            x=y
            y=r
        return y
    
    
class SponsorRedirect(TemplateAPI):
    
    def get(self, id):
        self.access_init()
        if self.access.check('sponsor_view_ads'):
            try:
                sponsor = Sponsor.get_by_id(int(id))
                if sponsor.record_clicks:
                    user = self.access.current_user
                    agent = os.environ['HTTP_USER_AGENT']
                    source = os.environ['REMOTE_ADDR']
                    sponsorclick = SponsorClick(sponsor=sponsor, user=user, agent=agent, source=source)
                    sponsorclick.put()
                self.redirect(sponsor.url)
            except:
                self.render_error(404)
        else:
            self.render_error(403)

app = webapp.WSGIApplication(
        [(settings.sponsor_permissions_url, SponsorPermissions),
        (settings.sponsor_management_url, SponsorManagement),
        (settings.sponsor_add_url, SponsorAdd),
        (settings.sponsor_edit_url, SponsorEdit),
        (settings.sponsor_delete_url, SponsorDelete),
        (settings.sponsor_view_url, SponsorView),
        (settings.sponsors_view_url, SponsorsView),
        (settings.sponsor_redirect_url, SponsorRedirect),
        (settings.sponsor_blocks_url, SponsorBlocks),],
        debug=False)
'''
def main():
    application = webapp.WSGIApplication(
        [(settings.sponsor_permissions_url, SponsorPermissions),
        (settings.sponsor_management_url, SponsorManagement),
        (settings.sponsor_add_url, SponsorAdd),
        (settings.sponsor_edit_url, SponsorEdit),
        (settings.sponsor_delete_url, SponsorDelete),
        (settings.sponsor_view_url, SponsorView),
        (settings.sponsors_view_url, SponsorsView),
        (settings.sponsor_redirect_url, SponsorRedirect),
        (settings.sponsor_blocks_url, SponsorBlocks),],
        debug=False)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()'''