#coding=UTF-8

'''
Created on Jan 7, 2011

@author: elvin
'''

import settings
from google.appengine.api import mail
from google.appengine.ext.webapp import util
from google.appengine.ext import webapp
from datetime import date
from core import TemplateAPI, User, UserAccess, UserPermissionAPI, Block, Blocks, SiteError


class FreePhotoSessionApplication():
    
    @staticmethod
    def get_permissions_url():
        return '/free-photo-session-application/permissions'
    
    @staticmethod
    def get_permissions_title():
        return 'Manage Free Photo Session Application Form Permissions'
    
    @staticmethod
    def get_permissions():
        return ['custom_fpsa_submit']
    
    @staticmethod
    def get_validation_message():
        return 'All fields marked with * are required!'
    
    @staticmethod
    def get_mail_sender():
        return "Elvin Kosova <elvinkosova@gmail.com>"
    
    @staticmethod
    def get_mail_to():
        return "Elvin Kosova Contact <contact@elvinkosova.com>"
    
    @staticmethod
    def get_mail_subject():
        return "Free Photo Session Application"
    
    @staticmethod
    def get_form():
        return 'custom_fpsa_form'
    
    @staticmethod
    def get_permission():
        return 'custom_fpsa_submit'
    
    @staticmethod
    def get_data(templateapi, fields):
        data = {'title': 'FREE PHOTO SESSION APPLICATION',
                'background': '/static/images/custom_fpsa_background.jpg',
                'fields': fields,
                'forbidden': False,
                'permissions_url': templateapi.get_redirect('/free-photo-session-application/permissions'),
                'form_permissions': templateapi.access.admin_user,
                'submit_url': templateapi.get_redirect('/free-photo-session-application'),}
        return data

    @staticmethod
    def get_fields(templateapi):
        days = range(1, 32)
        day_values = []
        day_values.append({'key': 'none', 'value': '', 'label': 'Day', 'selected': True})
        for day in days:
            day_values.append({'key': str(day), 'value': str(day), 'label': str(day), 'selected': False})
        months = range(1, 13)
        month_values = []
        month_values.append({'key': 'none', 'value': '', 'label': 'Month', 'selected': True})
        for month in months:
            month_values.append({'key': str(month), 'value': str(month), 'label': str(month), 'selected': False})
        today = date.today()
        years = range(today.year - 28, today.year - 17)
        year_values = []
        year_values.append({'key': 'none', 'value': '', 'label': 'Year', 'selected': True})
        for year in years:
            year_values.append({'key': str(year), 'value': str(year), 'label': str(year), 'selected': False})
        if templateapi.access.current_user.email != templateapi.access.anonymous_user.email:
            contact_email_value = templateapi.access.current_user.email
            contact_email_readonly = True
        else:
            contact_email_value = ''
            contact_email_readonly = False
        fields = {'residence_city': {'key': 'residence_city', 'weight': 0, 'name': 'residence_city', 'label': 'City: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'residence_area': {'key': 'residence_area', 'weight': 1, 'name': 'residence_area', 'label': 'Area: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'residence_country': {'key': 'residence_country', 'weight': 2, 'name': 'residence_country', 'label': 'Country: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'personal_first_name': {'key': 'personal_first_name', 'weight': 3, 'name': 'personal_first_name', 'label': 'First Name: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'personal_last_name': {'key': 'personal_last_name', 'weight': 4, 'name': 'personal_last_name', 'label': 'Last Name: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'personal_sex': {'key': 'personal_sex', 'weight': 5, 'name': 'personal_sex', 'label': 'Sex: ', 'type': 'select', 'multi': False, 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '', 
                  'items': [{'key': 'none', 'value': '', 'label': 'select...', 'selected': True},
                            {'key': 'female', 'value': 'female', 'label': 'Female', 'selected': False}]},
                  'birth_day': {'key': 'birth_day', 'weight': 6, 'name': 'birth_day', 'label': 'Day of Birth: ', 'type': 'select', 'multi': False, 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '', 'items': day_values},
                  'birth_month': {'key': 'birth_month', 'weight': 7, 'name': 'birth_month', 'label': 'Month of Birth: ', 'type': 'select', 'multi': False, 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '', 'items': month_values},
                  'birth_year': {'key': 'birth_year', 'weight': 8, 'name': 'birth_year', 'label': 'Year of Birth: ', 'type': 'select', 'multi': False, 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '', 'items': year_values},
                  'birth_city': {'key': 'birth_city', 'weight': 9, 'name': 'birth_city', 'label': 'City of Birth: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'birth_country': {'key': 'birth_country', 'weight': 10, 'name': 'birth_country', 'label': 'Country of Birth: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'contact_phone': {'key': 'contact_phone', 'weight': 11, 'name': 'contact_phone', 'label': 'Mobile Phone Number: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'contact_email': {'key': 'contact_email', 'weight': 12, 'name': 'contact_email', 'label': 'Email: ', 'type': 'email_authentication', 'format': 'unicode', 'required': True, 'required_validate': False, 'readonly': contact_email_readonly, 'value': contact_email_value},
                  'body_features_eyes': {'key': 'body_features_eyes', 'weight': 13, 'name': 'body_features_eyes', 'label': 'Eyes: ', 'type': 'select', 'multi': False, 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '', 
                  'items': [{'key': 'none', 'value': '', 'label': 'select...', 'selected': True},
                            {'key': 'amber', 'value': 'amber', 'label': 'Amber', 'selected': False},
                            {'key': 'blue', 'value': 'blue', 'label': 'Blue', 'selected': False},
                            {'key': 'brown', 'value': 'brown', 'label': 'Brown', 'selected': False},
                            {'key': 'gray', 'value': 'gray', 'label': 'Gray', 'selected': False},
                            {'key': 'green', 'value': 'green', 'label': 'Green', 'selected': False},
                            {'key': 'hazel', 'value': 'hazel', 'label': 'Hazel', 'selected': False},
                            {'key': 'red', 'value': 'red', 'label': 'Red', 'selected': False}]},
                  'body_features_hair': {'key': 'body_features_hair', 'weight': 14, 'name': 'body_features_hair', 'label': 'Hair: ', 'type': 'select', 'multi': False, 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '', 
                  'items': [{'key': 'none', 'value': '', 'label': 'select...', 'selected': True},
                            {'key': 'brown', 'value': 'brown', 'label': 'Brown', 'selected': False},
                            {'key': 'black', 'value': 'black', 'label': 'Black', 'selected': False},
                            {'key': 'blond', 'value': 'blond', 'label': 'Blond', 'selected': False},
                            {'key': 'auburn', 'value': 'auburn', 'label': 'Auburn', 'selected': False},
                            {'key': 'chestnut', 'value': 'chestnut', 'label': 'Chestnut', 'selected': False},
                            {'key': 'red', 'value': 'red', 'label': 'Red', 'selected': False}]},
                  'body_features_height': {'key': 'body_features_height', 'weight': 15, 'name': 'body_features_height', 'label': 'Height: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'body_features_bust': {'key': 'body_features_bust', 'weight': 16, 'name': 'body_features_bust', 'label': 'Bust: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'body_features_waist': {'key': 'body_features_waist', 'weight': 17, 'name': 'body_features_waist', 'label': 'Waist: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'body_features_hips': {'key': 'body_features_hips', 'weight': 18, 'name': 'body_features_hips', 'label': 'Hips: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'body_features_weight': {'key': 'body_features_weight', 'weight': 19, 'name': 'body_features_weight', 'label': 'Weight: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'spoken_languages': {'key': 'spoken_languages', 'weight': 20, 'name': 'spoken_languages', 'label': 'Spoken Languages: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'body_exposure_preference': {'key': 'body_exposure_preference', 'weight': 21, 'name': 'body_exposure_preference', 'label': 'I prefer to be photographed: ', 'type': 'checkboxes', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '',  
                  'items': [{'key': 'dressed', 'value': 'dressed', 'label': 'Dressed', 'checked': False},
                            {'key': 'in swimsuit', 'value': 'in swimsuit', 'label': 'In swimsuit', 'checked': False},
                            {'key': 'in lingerie', 'value': 'in lingerie', 'label': 'In lingerie', 'checked': False},
                            {'key': 'topless', 'value': 'topless', 'label': 'Topless', 'checked': False},
                            {'key': 'nude', 'value': 'nude', 'label': 'Nude', 'checked': False}]},
                  'preferred_styles': {'key': 'preferred_styles', 'weight': 22, 'name': 'preferred_styles', 'label': 'I prefer following photography styles: ', 'type': 'checkboxes', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '', 
                  'items': [{'key': 'fashion', 'value': 'fashion', 'label': 'Fashion', 'checked': False},
                            {'key': 'glamor', 'value': 'glamor', 'label': 'Glamor', 'checked': False},
                            {'key': 'fine art', 'value': 'fine art', 'label': 'Fine art', 'checked': False}]},
                  'note': {'key': 'note', 'weight': 23, 'name': 'note', 'label': 'Note: ', 'type': 'textarea', 'format': 'unicode', 'required': False, 'required_validate': False, 'value': ''}}
        return fields


class Contact():
    
    @staticmethod
    def get_permissions_url():
        return '/contact/permissions'
    
    @staticmethod
    def get_permissions_title():
        return 'Manage Contact Form Permissions'
    
    @staticmethod
    def get_permissions():
        return ['custom_contact_submit']
    
    @staticmethod
    def get_validation_message():
        return u'Sva polja označena sa * se moraju popuniti!'
    
    @staticmethod
    def get_mail_sender():
        return "EFC Admin <band@emir-frozencamels.com>"
    
    @staticmethod
    def get_mail_to():
        return "EFC Band <band@emir-frozencamels.com>"
    
    @staticmethod
    def get_mail_subject():
        return "EFC Message"
    
    @staticmethod
    def get_form():
        return 'custom_contact_form'
    
    @staticmethod
    def get_permission():
        return 'custom_contact_submit'
    
    @staticmethod
    def get_data(templateapi, fields):
        data = {'title': 'CONTACT',
                'background': '/static/images/custom_contact_background.jpg',
                'fields': fields,
                'forbidden': False,
                'permissions_url': templateapi.get_redirect('/contact/permissions'),
                'form_permissions': templateapi.access.admin_user,
                'submit_url': templateapi.get_redirect('/contact'),}
        return data

    @staticmethod
    def get_fields(templateapi):
        if templateapi.access.current_user.email != templateapi.access.anonymous_user.email:
            contact_email_value = templateapi.access.current_user.email
            contact_email_readonly = True
        else:
            contact_email_value = ''
            contact_email_readonly = False
        fields = {'contact_email': {'key': 'contact_email', 'weight': 0, 'name': 'contact_email', 'label': 'Email: ', 'type': 'email_authentication', 'format': 'unicode', 'required': True, 'required_validate': False, 'readonly': contact_email_readonly, 'value': contact_email_value},
                  'message': {'key': 'message', 'weight': 1, 'name': 'message', 'label': 'Poruka: ', 'type': 'textarea', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''}}
        return fields


class Casting():
    
    @staticmethod
    def get_permissions_url():
        return '/casting/permissions'
    
    @staticmethod
    def get_permissions_title():
        return 'Manage Casting Form Permissions'
    
    @staticmethod
    def get_permissions():
        return ['custom_casting_submit']
    
    @staticmethod
    def get_validation_message():
        return u'Sva polja označena sa * se moraju popuniti!'
    
    @staticmethod
    def get_mail_sender():
        return "Elvin Kosova <elvinkosova@gmail.com>"
    
    @staticmethod
    def get_mail_to():
        return "Miss Globe BIH Contact <contact@missglobebih.com>, Ema Alagić <ema@missglobebih.com>,"
    
    @staticmethod
    def get_mail_subject():
        return "Miss Globe BiH CASTING"
    
    @staticmethod
    def get_form():
        return 'custom_casting_form'
    
    @staticmethod
    def get_permission():
        return 'custom_casting_submit'
    
    @staticmethod
    def get_data(templateapi, fields):
        data = {'title': 'CASTING',
                'fields': fields,
                'forbidden': False,
                'permissions_url': templateapi.get_redirect('/casting/permissions'),
                'form_permissions': templateapi.access.admin_user,
                'submit_url': templateapi.get_redirect('/casting'),}
        return data

    @staticmethod
    def get_fields(templateapi):
        days = range(1, 32)
        day_values = []
        day_values.append({'key': 'none', 'value': '', 'label': 'Dan', 'selected': True})
        for day in days:
            day_values.append({'key': str(day), 'value': str(day), 'label': str(day), 'selected': False})
        months = range(1, 13)
        month_values = []
        month_values.append({'key': 'none', 'value': '', 'label': 'Mjesec', 'selected': True})
        for month in months:
            month_values.append({'key': str(month), 'value': str(month), 'label': str(month), 'selected': False})
        today = date.today()
        years = range(today.year - 23, today.year - 15)
        year_values = []
        year_values.append({'key': 'none', 'value': '', 'label': 'Godina', 'selected': True})
        for year in years:
            year_values.append({'key': str(year), 'value': str(year), 'label': str(year), 'selected': False})
        if templateapi.access.current_user.email != templateapi.access.anonymous_user.email:
            contact_email_value = templateapi.access.current_user.email
            contact_email_readonly = True
        else:
            contact_email_value = ''
            contact_email_readonly = False
        fields = {'residence_city': {'key': 'residence_city', 'weight': 0, 'name': 'residence_city', 'label': u'Grad: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'residence_area': {'key': 'residence_area', 'weight': 1, 'name': 'residence_area', 'label': u'Regija: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'residence_country': {'key': 'residence_country', 'weight': 2, 'name': 'residence_country', 'label': u'Zemlja: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'personal_first_name': {'key': 'personal_first_name', 'weight': 3, 'name': 'personal_first_name', 'label': u'Ime: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'personal_last_name': {'key': 'personal_last_name', 'weight': 4, 'name': 'personal_last_name', 'label': u'Prezime: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'birth_day': {'key': 'birth_day', 'weight': 5, 'name': 'birth_day', 'label': u'Dan Rođenja: ', 'type': 'select', 'multi': False, 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '', 'items': day_values},
                  'birth_month': {'key': 'birth_month', 'weight': 6, 'name': 'birth_month', 'label': u'Mjesec Rođenja: ', 'type': 'select', 'multi': False, 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '', 'items': month_values},
                  'birth_year': {'key': 'birth_year', 'weight': 7, 'name': 'birth_year', 'label': u'Godina Rođenja: ', 'type': 'select', 'multi': False, 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '', 'items': year_values},
                  'birth_city': {'key': 'birth_city', 'weight': 8, 'name': 'birth_city', 'label': u'Grad Rođenja: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'birth_country': {'key': 'birth_country', 'weight': 9, 'name': 'birth_country', 'label': u'Zemlja Rođenja: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'citizenship': {'key': 'citizenship', 'weight': 10, 'name': 'citizenship', 'label': u'Državljanstvo: ', 'type': 'select', 'multi': True, 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '', 
                  'items': [{'key': u'bosna i hercegovina', 'value': u'bosna i hercegovina', 'label': u'Bosna i Hercegovina', 'selected': False},
                            {'key': u'crna gora', 'value': u'crna gora', 'label': u'Crna Gora', 'selected': False},
                            {'key': u'hrvatska', 'value': u'hrvatska', 'label': u'Hrvatska', 'selected': False},
                            {'key': u'srbija', 'value': u'srbija', 'label': u'Srbija', 'selected': False},
                            {'key': u'makedonija', 'value': u'makedonija', 'label': u'Makedonija', 'selected': False},]},
                  'contact_phone': {'key': 'contact_phone', 'weight': 11, 'name': 'contact_phone', 'label': u'Broj Mobitela: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'contact_email': {'key': 'contact_email', 'weight': 12, 'name': 'contact_email', 'label': u'E-mail: ', 'type': 'email_authentication', 'format': 'unicode', 'required': True, 'required_validate': False, 'readonly': contact_email_readonly, 'value': contact_email_value},
                  'body_features_height': {'key': 'body_features_height', 'weight': 15, 'name': 'body_features_height', 'label': u'Visina: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'body_features_bust': {'key': 'body_features_bust', 'weight': 16, 'name': 'body_features_bust', 'label': u'Grudi: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'body_features_waist': {'key': 'body_features_waist', 'weight': 17, 'name': 'body_features_waist', 'label': u'Struk: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'body_features_hips': {'key': 'body_features_hips', 'weight': 18, 'name': 'body_features_hips', 'label': u'Bokovi: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'body_features_weight': {'key': 'body_features_weight', 'weight': 19, 'name': 'body_features_weight', 'label': u'Težina: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'high_school': {'key': 'high_school', 'weight': 20, 'name': 'high_school', 'label': u'Srednja Škola: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'university': {'key': 'university', 'weight': 21, 'name': 'university', 'label': u'Fakultet: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'spoken_languages': {'key': 'spoken_languages', 'weight': 22, 'name': 'spoken_languages', 'label': u'Strani Jezici: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'hobby': {'key': 'hobby', 'weight': 23, 'name': 'hobby', 'label': u'Hobi: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'model': {'key': 'model', 'weight': 24, 'name': 'model', 'label': u'Da li se bavite manekenstvom?: ', 'type': 'radios', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': '',  
                  'items': [{'key': u'da', 'value': u'da', 'label': u'Da', 'checked': False},
                            {'key': u'ne', 'value': u'ne', 'label': u'Ne', 'checked': False}]},
                  'agency': {'key': 'agency', 'weight': 25, 'name': 'agency', 'label': u'Agencija: ', 'type': 'text', 'format': 'unicode', 'required': False, 'required_validate': False, 'value': ''},
                  'talent': {'key': 'talent', 'weight': 26, 'name': 'talent', 'label': u'Talenat: ', 'type': 'text', 'format': 'unicode', 'required': True, 'required_validate': False, 'value': ''},
                  'note': {'key': 'note', 'weight': 27, 'name': 'note', 'label': u'Komentar: ', 'type': 'textarea', 'format': 'unicode', 'required': False, 'required_validate': False, 'value': ''}}
        return fields


class FormMailerDecisionMaker():
    
    def __init__(self, templateapi):
        if templateapi.request.path == '/free-photo-session-application' or templateapi.request.path == '/free-photo-session-application/permissions':
            self.mail_sender = FreePhotoSessionApplication.get_mail_sender()
            self.mail_to = FreePhotoSessionApplication.get_mail_to()
            self.mail_subject = FreePhotoSessionApplication.get_mail_subject()
            self.permission = FreePhotoSessionApplication.get_permission()
            self.form = FreePhotoSessionApplication.get_form()
            self.fields = FreePhotoSessionApplication.get_fields(templateapi)
            self.data = FreePhotoSessionApplication.get_data(templateapi, self.fields)
            self.validation_message = FreePhotoSessionApplication.get_validation_message()
            self.permissions = FreePhotoSessionApplication.get_permissions()
            self.permissions_url = FreePhotoSessionApplication.get_permissions_url()
            self.permissions_title = FreePhotoSessionApplication.get_permissions_title()
            
        if templateapi.request.path == '/contact' or templateapi.request.path == '/contact/permissions':
            self.mail_sender = Contact.get_mail_sender()
            self.mail_to = Contact.get_mail_to()
            self.mail_subject = Contact.get_mail_subject()
            self.permission = Contact.get_permission()
            self.form = Contact.get_form()
            self.fields = Contact.get_fields(templateapi)
            self.data = Contact.get_data(templateapi, self.fields)
            self.validation_message = Contact.get_validation_message()
            self.permissions = Contact.get_permissions()
            self.permissions_url = Contact.get_permissions_url()
            self.permissions_title = Contact.get_permissions_title()
            
        if templateapi.request.path == '/casting' or templateapi.request.path == '/casting/permissions':
            self.mail_sender = Casting.get_mail_sender()
            self.mail_to = Casting.get_mail_to()
            self.mail_subject = Casting.get_mail_subject()
            self.permission = Casting.get_permission()
            self.form = Casting.get_form()
            self.fields = Casting.get_fields(templateapi)
            self.data = Casting.get_data(templateapi, self.fields)
            self.validation_message = Casting.get_validation_message()
            self.permissions = Casting.get_permissions()
            self.permissions_url = Casting.get_permissions_url()
            self.permissions_title = Casting.get_permissions_title()
        

class FormMailer(TemplateAPI):
    
    def get(self):
        self.access_init()
        mailer = FormMailerDecisionMaker(self)
        if not self.access.check(mailer.permission):
            mailer.data['forbidden'] = True
        self.render_html('custom', mailer.form, mailer.data)
        
    def post(self):
        self.access_init()
        mailer = FormMailerDecisionMaker(self)
        if self.access.check(mailer.permission):
            try:
                results = self.mailer_form_validator(mailer.fields)
                field_required_alert = results['field_required_alert']
                fields = results['fields']
                if field_required_alert:
                    mailer.data['message'] = mailer.validation_message
                    mailer.data['message_class'] = 'error-message'
                    mailer.data['fields'] = fields
                else:
                    sorted_fields = sorted(fields.values(), key=lambda field: field['weight'])
                    body = '\n'
                    for field in sorted_fields:
                        body += field['label'] + field['value'] + '\n'
                    mail.send_mail(sender=mailer.mail_sender, to=mailer.mail_to, subject=mailer.mail_subject, body=body)
                    mailer.data['submitted'] = True
                    mailer.data['fields'] = fields
            except:
                self.render_error(404)
        else:
            mailer.data['fields'] = mailer.fields
            mailer.data['forbidden'] = True
        self.render_html('custom', mailer.form, mailer.data)
            
    def mailer_form_validator(self, fields):
        field_required_alert = False
        for field in fields.values():
            if field['type'] == 'text' or field['type'] == 'textarea':
                fields[field['key']]['value'] = self.manipulator.esc(unicode(self.request.get(field['name'])))
                if field['required'] and not fields[field['key']]['value']:
                    fields[field['key']]['required_validate'] = True
                    field_required_alert = True
            elif field['type'] == 'select':
                if field['multi']:
                    field_values = self.request.get_all(field['name'])
                    item_values = []
                    for item in field['items']:
                        if item['value'] in field_values:
                            fields[field['key']]['value'] = ', '.join(field_values)
                            item_values.append({'key': item['key'], 'value': item['value'], 'label': item['label'], 'selected': True})
                        else:
                            item_values.append({'key': item['key'], 'value': item['value'], 'label': item['label'], 'selected': False})
                    fields[field['key']]['items'] = item_values
                    if field['required'] and not fields[field['key']]['value']:
                        fields[field['key']]['required_validate'] = True
                        field_required_alert = True
                else:
                    field_value = self.manipulator.esc(unicode(self.request.get(field['name'])))
                    item_values = []
                    for item in field['items']:
                        if item['value'] == field_value:
                            fields[field['key']]['value'] = field_value
                            item_values.append({'key': item['key'], 'value': item['value'], 'label': item['label'], 'selected': True})
                        else:
                            item_values.append({'key': item['key'], 'value': item['value'], 'label': item['label'], 'selected': False})
                    fields[field['key']]['items'] = item_values
                    if field['required'] and not fields[field['key']]['value']:
                        fields[field['key']]['required_validate'] = True
                        field_required_alert = True
            elif field['type'] == 'checkboxes':
                field_values = self.request.get_all(field['name'])
                item_values = []
                for item in field['items']:
                    if item['value'] in field_values:
                        fields[field['key']]['value'] = ', '.join(field_values)
                        item_values.append({'key': item['key'], 'value': item['value'], 'label': item['label'], 'checked': True})
                    else:
                        item_values.append({'key': item['key'], 'value': item['value'], 'label': item['label'], 'checked': False})
                fields[field['key']]['items'] = item_values
                if field['required'] and not fields[field['key']]['value']:
                    fields[field['key']]['required_validate'] = True
                    field_required_alert = True
            elif field['type'] == 'radios':
                field_value = self.manipulator.esc(unicode(self.request.get(field['name'])))
                item_values = []
                for item in field['items']:
                    if item['value'] == field_value:
                        fields[field['key']]['value'] = field_value
                        item_values.append({'key': item['key'], 'value': item['value'], 'label': item['label'], 'checked': True})
                    else:
                        item_values.append({'key': item['key'], 'value': item['value'], 'label': item['label'], 'checked': False})
                fields[field['key']]['items'] = item_values
                if field['required'] and not fields[field['key']]['value']:
                    fields[field['key']]['required_validate'] = True
                    field_required_alert = True
            elif field['type'] == 'email_authentication':
                if self.access.current_user.email != self.access.anonymous_user.email:
                    fields[field['key']]['value'] = self.access.current_user.email
                    fields[field['key']]['readonly'] = True
                else:
                    fields[field['key']]['value'] = self.manipulator.esc(unicode(self.request.get(field['name'])))
                    fields[field['key']]['readonly'] = False
                if field['required'] and not fields[field['key']]['value']:
                    fields[field['key']]['required_validate'] = True
                    field_required_alert = True
        return {'field_required_alert': field_required_alert, 'fields': fields}


class FormMailerPermissions(UserPermissionAPI):
    
    def get(self):
        self.access_init()
        mailer = FormMailerDecisionMaker(self)
        self.get_form(permissions=mailer.permissions, url=mailer.permissions_url, title=mailer.permissions_title)
        
    def post(self):
        self.access_init()
        mailer = FormMailerDecisionMaker(self)
        values = self.request.get_all('user-permissions')
        self.save_permissions(permissions=mailer.permissions, values=values, url=mailer.permissions_url)

app = webapp.WSGIApplication(
        [('/free-photo-session-application/permissions', FormMailerPermissions),
         ('/free-photo-session-application', FormMailer),
         ('/contact/permissions', FormMailerPermissions),
         ('/contact', FormMailer),
         ('/casting/permissions', FormMailerPermissions),
         ('/casting', FormMailer),],
        debug=False)  
'''def main():
     application = webapp.WSGIApplication(
         [('/free-photo-session-application/permissions', FormMailerPermissions),
          ('/free-photo-session-application', FormMailer),
          ('/contact/permissions', FormMailerPermissions),
          ('/contact', FormMailer),
          ('/casting/permissions', FormMailerPermissions),
          ('/casting', FormMailer),],
         debug=False)
     util.run_wsgi_app(application)
 
 if __name__ == '__main__':
     main()   ''' 