#coding=UTF-8

#---------------global settings-------------

site_name = ''
site_domain = ''
google_analytics_account = ''
facebook_app_id = ''
facebook_app_secret = ''
# app.yaml default_expiration: "365d"

import os
app_dir = os.path.dirname(__file__)

#---------------core module-------------

main_top_menu = [{'path': '/bio', 'name': 'BIO', 'description': 'BIOGRAPHY'},
                 {'path': '/news', 'name': 'NEWS', 'description': 'NEWS'},
                 {'path': '/music', 'name': 'MUSIC', 'description': 'MUSIC'},
                 {'path': '/videos', 'name': 'VIDEOS', 'description': 'VIDEOS'},
                 {'path': '/photos', 'name': 'PHOTOS', 'description': 'PHOTO'},
                 {'path': '/extras', 'name': 'EXTRAS', 'description': 'EXTRAS'},
                 {'path': '/contact', 'name': 'CONTACT', 'description': 'CONTACT'}]

main_bottom_menu = [{'path': '/terms-use', 'name': 'Terms of Use', 'description': 'Terms of Use'},
                    {'path': '/privacy', 'name': 'Privacy', 'description': 'Privacy'}]

top_menus = [main_top_menu]
bottom_menus = [main_bottom_menu]
left_menus = ''
right_menus = ''

template_api_render_errors = {'403': {'title': 'Forbidden', 'message': 'You are not authorized to access this page.'},
                              '404': {'title': 'Not Found', 'message': 'The requested page could not be found.'},
                              '500': {'title': 'Internal Server Error', 'message': 'The server encountered an unexpected condition which prevented it from fulfilling the request.'},
                              'default': {'title': 'Illegal operation', 'message': 'Illegal operation has been performed! Click <a href="/">here</a> to get back to home.'}}

template_api_pager_range = 6
template_api_pager_devider = 3
template_api_pager_render_firs_page = '‹‹ first'
template_api_pager_render_firs_page_title = 'First page'
template_api_pager_render_previous_page = 'prev'
template_api_pager_render_previous_page_title = 'Previous page'
template_api_pager_render_next_page = 'next'
template_api_pager_render_next_page_title = 'Next page'
template_api_pager_render_last_page = 'last ››'
template_api_pager_render_last_page_title = 'Last page'
template_api_pager_render_counter_string = '%s of %s'
template_api_pager_page_query_list = ['page', 'musics_page', 'photos_page']

content_manipulator_formater_forbidden_tags = ['script', 'input', 'form', 'link', 'blink', 'object'] #'iframe'
content_manipulator_formater_forbidden_attributes = ['onclick', 'onload']
content_manipulator_formater_forbidden_attribute_values = ['javascript:'] # 'display:\s*none'

site_error_url = '/error/([0-9]+)'
site_error_url_string = '/error/%s'

users_per_page = 10

user_authenticated = 'authenticated_user'
user_anonymous = 'anonymous_user'

user_uid_trimmed = 121
user_email_trimmed = 121
user_permission_trimmed = 121

datetime_formated = '%d.%m.%Y - %H:%M:%S'
datetime_trimmed = '%d.%m.%Y'

user_management_url = '/user/management'
user_management_title = 'Manage Users'

user_permissions_management_title = 'Manage Permissions'

user_login_url = '/user/login'

user_logout_url = '/user/logout'

user_management_form_label_uid = 'UID'
user_management_form_label_email = 'Email'
user_management_form_label_registered = 'Registered'
user_management_form_label_last_access = 'Last Access'
user_management_form_label_last_ip_address = 'Last IP Address'
user_management_form_label_active = 'Active'
user_management_form_label_submit = 'Update'

user_permission_management_form_label_user = 'User'
user_permission_management_form_label_submit = 'Update'

block_title_trimmed = 1000

blocks_per_request = 100
blocks_per_page = 10

block_positions = [{'value': 'top', 'label': 'Top'},
                   {'value': 'left', 'label': 'Left'},
                   {'value': 'right', 'label': 'Right'},
                   {'value': 'bottom', 'label': 'Bottom'}]

block_add_url = '/block/add'
block_add_title = 'Add Block'
block_add_redirect_url = '/block/management'

block_edit_url = '/block/([0-9]+)/edit'
block_edit_url_string = '/block/%s/edit'
block_edit_title = 'Edit Block'
block_edit_redirect_url = '/block/management'

block_delete_url = '/block/([0-9]+)/delete'
block_delete_url_string = '/block/%s/delete'
block_delete_title = 'Delete Block'
block_delete_redirect_url = '/block/management'

block_management_url = '/block/management'
block_management_title = 'Manage Blocks'

block_permissions_url = '/block/permissions'
block_permissions_title = 'Manage Block Permissions'

block_view_permissions_url = '/block/([0-9]+)/permissions'
block_view_permissions_url_string = '/block/%s/permissions'
block_view_permissions_title_string = 'Manage Block "%s" Permissions'

block_add_form_label_title = 'Title:'
block_add_form_label_position = 'Position:'
block_add_form_label_weight = 'Weight:'
block_add_form_label_content = 'Content:'
block_add_form_label_published = 'Published'
block_add_form_label_submit = 'Save'
block_add_form_label_cancel = 'Cancel'

block_edit_form_label_title = 'Title:'
block_edit_form_label_position = 'Position:'
block_edit_form_label_weight = 'Weight:'
block_edit_form_label_content = 'Content:'
block_edit_form_label_published = 'Published'
block_edit_form_label_submit = 'Save'
block_edit_form_label_cancel = 'Cancel'

block_delete_form_label_question = 'Are you sure you want to delete this block?'
block_delete_form_label_question_string = 'Are you sure you want to delete "%s" block?'
block_delete_form_label_submit = 'Yes'
block_delete_form_label_cancel = 'No'

block_management_form_label_title = 'Title'
block_management_form_label_position = 'Position'
block_management_form_label_weight = 'Weight'
block_management_form_label_published = 'Published'
block_management_form_label_management_links = 'Management Links'
block_management_form_label_view_permissions = 'Permissions'
block_management_form_label_view_permissions_title = 'Block View Permissions'
block_management_form_label_edit = 'Edit'
block_management_form_label_edit_title = 'Edit Block'
block_management_form_label_delete = 'Delete'
block_management_form_label_delete_title = 'Delete Block'
block_management_form_label_add = 'Add Block'
block_management_form_label_add_title = 'Add Block'
block_management_form_label_permissions = 'Permissions'
block_management_form_label_permissions_title = 'Block Permissions'

#---------------file module-------------

file_title_trimmed = 1000

file_max_upload_size = 104857600
file_allowed_types = ['all']
files_per_page = 50

file_add_url = '/file/add'
file_add_title = 'Add File'
file_add_redirect_url = '/file/management'

file_save_url = '/file/save'
file_save_redirect_url = '/file/management'

file_edit_url = '/file/([0-9]+)/edit'
file_edit_url_string = '/file/%s/edit'
file_edit_title = 'Edit File'
file_edit_redirect_url = '/file/management'

file_delete_url = '/file/([0-9]+)/delete'
file_delete_url_string = '/file/%s/delete'
file_delete_title = 'Delete File'
file_delete_redirect_url = '/file/management'

file_management_url = '/file/management'
file_management_title = 'Manage Files'

file_permissions_url = '/file/permissions'
file_permissions_title = 'Manage File Permissions'

file_output_url = '/file/([^/]+)?/([^/]+)?'
file_output_url_string = '/file/%s/%s'

file_error_url = '/file/error/([a-zA-Z0-9-_]+)'
file_error_url_string = '/file/error/%s'
file_error_oversize_type = 'oversize'
file_error_oversize_title = 'File Size Exceeded'
file_error_oversize_message_string = 'Maximum file size has been exceeded! Size limit is %s bytes.'
file_error_incorrect_type_type = 'incorrect-type'
file_error_incorrect_type_title = 'Unsupported Type'
file_error_incorrect_type_message_string = 'Unsupported File Type! Supported file types are %s.'
file_error_forbidden_type = 'forbidden'

file_add_form_label_file = 'File:'
file_add_form_label_title = 'Title:'
file_add_form_label_published = 'Published'
file_add_form_label_submit = 'Save'
file_add_form_label_cancel = 'Cancel'

file_edit_form_label_file = 'File:'
file_edit_form_label_title = 'Title:'
file_edit_form_label_published = 'Published'
file_edit_form_label_submit = 'Save'
file_edit_form_label_cancel = 'Cancel'

file_delete_form_label_question = 'Are you sure you want to delete this file?'
file_delete_form_label_question_string = 'Are you sure you want to delete "%s" file?'
file_delete_form_label_submit = 'Yes'
file_delete_form_label_cancel = 'No'

file_management_form_label_title = 'Title'
file_management_form_label_published = 'Published'
file_management_form_label_management_links = 'Management Links'
file_management_form_label_add = 'Add File'
file_management_form_label_add_title = 'Add File'
file_management_form_label_permissions = 'Permissions'
file_management_form_label_permissions_title = 'File Permissions'
file_management_form_label_view = 'View'
file_management_form_label_view_title = 'View File'
file_management_form_label_edit = 'Edit'
file_management_form_label_edit_title = 'Edit File'
file_management_form_label_delete = 'Delete'
file_management_form_label_delete_title = 'Delete File'

#---------------music module-------------

music_title_trimmed = 1000

music_max_upload_size = 104857600
musics_per_page = 50

music_allowed_types = ['audio/mp3']

music_add_url = '/track/add'
music_add_title = 'Add Music'
music_add_redirect_url = '/track/management'

music_save_url = '/track/save'
music_save_redirect_url = '/track/management'

music_edit_url = '/track/([0-9]+)/edit'
music_edit_url_string = '/track/%s/edit'
music_edit_title = 'Edit Music'
music_edit_redirect_url = '/track/management'

music_delete_url = '/track/([0-9]+)/delete'
music_delete_url_string = '/track/%s/delete'
music_delete_title = 'Delete Music'
music_delete_redirect_url = '/track/management'

music_management_url = '/track/management'
music_management_title = 'Manage Musics'

music_permissions_url = '/track/permissions'
music_permissions_title = 'Manage Music Permissions'

music_view_url = '/track/([0-9]+)'
music_view_url_string = '/track/%s'

music_output_url = '/track/([^/]+)?/([^/]+)?'
music_output_url_string = '/track/%s/%s'

music_error_url = '/track/error/([a-zA-Z0-9-_]+)'
music_error_url_string = '/track/error/%s'
music_error_oversize_type = 'oversize'
music_error_oversize_title = 'Music Size Exceeded'
music_error_oversize_message_string = 'Maximum music size has been exceeded! Size limit is %s bytes.'
music_error_incorrect_type_type = 'incorrect-type'
music_error_incorrect_type_title = 'Unsupported Type'
music_error_incorrect_type_message_string = 'Unsupported File Type! Supported file types are %s.'
music_error_forbidden_type = 'forbidden'

music_add_form_label_music = 'Music:'
music_add_form_label_title = 'Title:'
music_add_form_label_content = 'Content:'
music_add_form_label_published = 'Published'
music_add_form_label_submit = 'Save'
music_add_form_label_cancel = 'Cancel'

music_edit_form_label_music = 'Music:'
music_edit_form_label_title = 'Title:'
music_edit_form_label_content = 'Content:'
music_edit_form_label_published = 'Published'
music_edit_form_label_submit = 'Save'
music_edit_form_label_cancel = 'Cancel'

music_delete_form_label_question = 'Are you sure you want to delete this music?'
music_delete_form_label_question_string = 'Are you sure you want to delete "%s" music?'
music_delete_form_label_submit = 'Yes'
music_delete_form_label_cancel = 'No'

music_management_form_label_title = 'Title'
music_management_form_label_published = 'Published'
music_management_form_label_file = 'Sample'
music_management_form_label_management_links = 'Management Links'
music_management_form_label_add = 'Add Music'
music_management_form_label_add_title = 'Add Music'
music_management_form_label_permissions = 'Permissions'
music_management_form_label_permissions_title = 'Music Permissions'
music_management_form_label_view = 'View'
music_management_form_label_view_title = 'View Music'
music_management_form_label_edit = 'Edit'
music_management_form_label_edit_title = 'Edit Music'
music_management_form_label_delete = 'Delete'
music_management_form_label_delete_title = 'Delete Music'

#---------------photo module-------------

photo_l = 900
photo_l_w = 900
photo_l_h = 720

photo_m = 720
photo_m_w = 720
photo_m_h = 480

photo_s = 180
photo_s_w = 180
photo_s_h = 120

photo_xs = 90
photo_xs_w = 90
photo_xs_h = 60

photo_default_size = 900
photo_default_width = 600
photo_default_height = 720

photo_max_upload_size = 1048576
#photo_allowed_types = ['image/jpeg', 'image/png']
photo_allowed_types = ['all']
photo_max_size = 900
photo_max_width = 900
photo_max_height = 720

photo_low_limit_width = 0
photo_low_limit_height = 0

photo_high_limit_width = 1440
photo_high_limit_height = 960

photo_quality = 100

photos_per_page = 12
photos_per_row = 3

photo_get_serving_url = False

photo_l_watermark = 'static/images/watermark_426x106.png'
photo_m_watermark = 'static/images/watermark_320x80.png'

photo_add_url = '/photo/add'
photo_add_title = 'Add Photo'
photo_add_redirect_url = '/photo/management'

photo_save_url = '/photo/save'
photo_save_redirect_url = '/photo/management'

photo_edit_url = '/photo/([0-9]+)/edit'
photo_edit_url_string = '/photo/%s/edit'
photo_edit_title = 'Edit Photo'
photo_edit_redirect_url = '/photo/management'

photo_delete_url = '/photo/([0-9]+)/delete'
photo_delete_url_string = '/photo/%s/delete'
photo_delete_title = 'Delete Photo'
photo_delete_redirect_url = '/photo/management'

photo_management_url = '/photo/management'
photo_management_title = 'Manage Photos'

photo_permissions_url = '/photo/permissions'
photo_permissions_title = 'Manage Photo Permissions'

photo_view_url = '/photo/([0-9]+)'
photo_view_url_string = '/photo/%s'

photo_output_url = '/photo/output/([^/]+)?'
photo_output_url_string = '/photo/output/%s'

photo_error_url = '/photo/error/([a-zA-Z0-9-_]+)'
photo_error_url_string = '/photo/error/%s'
photo_errors = {'photo_errors_url_types': {'oversize': 'oversize', 'incorrect-type': 'incorrect_type', 'unsupported-resolution': 'unsupported_resolution', 'forbidden': 'forbidden'},
                'oversize': {'path': 'oversize', 'title': 'Photo Size Exceeded', 'message': 'Maximum photo size has been exceeded! Size limit is 1048576 bytes.'},
                'incorrect_type': {'path': 'incorrect-type', 'title': 'Unsupported Type', 'message': 'Unsupported File Type! Supported file types are image/jpeg, image/png.'},
                'unsupported_resolution': {'path': 'unsupported-resolution', 'title': 'Unsupported Resolution', 'message': 'Unsupported Resolution! Supported resolution is between 960x640 and 1200x800.'},
                'forbidden': {'path': 'forbidden', 'title': 'Forbidden', 'message': 'You are not authorized to access this page.'}}

photo_add_form_label_image = 'Image:'
photo_add_form_label_description = 'Description:'
photo_add_form_label_published = 'Published'
photo_add_form_label_submit = 'Save'
photo_add_form_label_cancel = 'Cancel'

photo_edit_form_label_image = 'Image:'
photo_edit_form_label_description = 'Description:'
photo_edit_form_label_published = 'Published'
photo_edit_form_label_submit = 'Save'
photo_edit_form_label_cancel = 'Cancel'

photo_delete_form_label_question = 'Are you sure you want to delete this photo?'
photo_delete_form_label_submit = 'Yes'
photo_delete_form_label_cancel = 'No'

photo_management_form_label_add = 'Add Photo'
photo_management_form_label_add_title = 'Add Photo'
photo_management_form_label_permissions = 'Permissions'
photo_management_form_label_permissions_title = 'Photo Permissions'
photo_management_form_label_view = 'View'
photo_management_form_label_view_title = 'View Photo'
photo_management_form_label_edit = 'Edit'
photo_management_form_label_edit_title = 'Edit Photo'
photo_management_form_label_delete = 'Delete'
photo_management_form_label_delete_title = 'Delete Photo'

#---------------feed module-------------

feeds_per_page = 50

feed_types = {'types': ['story', 'photo_album', 'music_album', 'page', 'video'],
              'feed_view_url_types': {'story': 'story', 'gallery': 'photo_album', 'album': 'music_album', 'page': 'page', 'video': 'video'},
              'feeds_view_url_types': {'news': 'story', 'photos': 'photo_album', 'music': 'music_album', 'pages': 'page', 'videos': 'video'},
              'story': {'feed_view_url': 'story', 
                        'feeds_view_url': 'news', 
                        'sort': '-created', 
                        'title': 'NEWS', 
                        'label': 'Story', 
                        'feeds_view_template': 'stories', 
                        'default_background_src': '/static/images/stories_view_background.jpg', 
                        'title_trimmed': 1000, 
                        'content_trimmed': 300, 
                        'feeds_per_page': 5, 
                        'feeds_per_row': 1, 
                        'feeds_view_cover': 150, 
                        'feeds_view_cover_w': 150, 
                        'feeds_view_cover_h': 150, 
                        'feed_view_cover': 180, 
                        'feed_view_cover_w': 180, 
                        'feed_view_cover_h': 120, 
                        'background': 900, 
                        'background_w': 900, 
                        'background_h': 552, 
                        'photos': 180, 
                        'photos_w': 180, 
                        'photos_h': 120, 
                        'photos_per_page': 12, 
                        'photos_per_row': 3, 
                        'musics_per_page': 50, 
                        'musics_per_row': 1},
              'page': {'feed_view_url': 'page', 
                        'feeds_view_url': 'pages', 
                        'sort': 'title', 
                        'title': 'PAGES', 
                        'label': 'Page', 
                        'feeds_view_template': 'pages', 
                        'default_background_src': '', 
                        'title_trimmed': 1000, 
                        'content_trimmed': 300, 
                        'feeds_per_page': 5, 
                        'feeds_per_row': 1, 
                        'feeds_view_cover': 180, 
                        'feeds_view_cover_w': 180, 
                        'feeds_view_cover_h': 120, 
                        'feed_view_cover': 180, 
                        'feed_view_cover_w': 180, 
                        'feed_view_cover_h': 120, 
                        'background': 900, 
                        'background_w': 900, 
                        'background_h': 600, 
                        'photos': 180, 
                        'photos_w': 180, 
                        'photos_h': 120, 
                        'photos_per_page': 12, 
                        'photos_per_row': 3, 
                        'musics_per_page': 50, 
                        'musics_per_row': 1},
                'photo_album': {'feed_view_url': 'gallery', 
                                 'feeds_view_url': 'photos', 
                                 'sort': '-created', 
                                 'title': 'PHOTOS', 
                                 'label': 'Gallery', 
                                 'feeds_view_template': 'photo_albums', 
                                 'default_background_src': '/static/images/photo_albums_view_background.jpg', 
                                 'title_trimmed': 1000, 
                                 'content_trimmed': 300, 
                                 'feeds_per_page': 9, 
                                 'feeds_per_row': 3, 
                                 'feeds_view_cover': 158, 
                                 'feeds_view_cover_w': 158, 
                                 'feeds_view_cover_h': 158, 
                                 'feed_view_cover': 180, 
                                 'feed_view_cover_w': 180, 
                                 'feed_view_cover_h': 120, 
                                 'background': 900, 
                                 'background_w': 900, 
                                 'background_h': 552, 
                                 'photos': 180, 
                                 'photos_w': 180, 
                                 'photos_h': 120, 
                                 'photos_per_page': 12, 
                                 'photos_per_row': 3, 
                                 'musics_per_page': 50, 
                                 'musics_per_row': 1},
              'music_album': {'feed_view_url': 'album', 
                              'feeds_view_url': 'music', 
                              'sort': '-created', 
                              'title': 'MUSIC', 
                              'label': 'Album', 
                              'feeds_view_template': 'music_albums', 
                              'default_background_src': '/static/images/music_albums_view_background.jpg', 
                              'title_trimmed': 1000, 
                              'content_trimmed': 300, 
                              'feeds_per_page': 9, 
                              'feeds_per_row': 3, 
                              'feeds_view_cover': 158, 
                              'feeds_view_cover_w': 158, 
                              'feeds_view_cover_h': 158, 
                              'feed_view_cover': 240, 
                              'feed_view_cover_w': 240, 
                              'feed_view_cover_h': 240, 
                              'background': 900, 
                              'background_w': 900, 
                              'background_h': 552, 
                              'photos': 180, 
                              'photos_w': 180, 
                              'photos_h': 120, 
                              'photos_per_page': 12, 
                              'photos_per_row': 3, 
                              'musics_per_page': 50, 
                              'musics_per_row': 1},
                'video': {'feed_view_url': 'video', 
                        'feeds_view_url': 'videos', 
                        'sort': '-created', 
                        'title': 'VIDEOS', 
                        'label': 'Video', 
                        'feeds_view_template': 'videos', 
                        'default_background_src': '/static/images/videos_view_background.jpg', 
                        'title_trimmed': 1000, 
                        'content_trimmed': 300, 
                        'feeds_per_page': 9, 
                        'feeds_per_row': 3, 
                        'feeds_view_cover': 158, 
                        'feeds_view_cover_w': 158, 
                        'feeds_view_cover_h': 158, 
                        'feed_view_cover': 180, 
                        'feed_view_cover_w': 180, 
                        'feed_view_cover_h': 120, 
                        'background': 900, 
                        'background_w': 900, 
                        'background_h': 552, 
                        'photos': 180, 
                        'photos_w': 180, 
                        'photos_h': 120, 
                        'photos_per_page': 12, 
                        'photos_per_row': 3, 
                        'musics_per_page': 50, 
                        'musics_per_row': 1},}


feed_view_url = '/([a-z-_]+)/([a-zA-Z0-9-_]+)'
feed_view_url_string = '/%s/%s'
feed_view_default_title = ''

feeds_view_url = '/([a-z-_]+)?'
feeds_view_url_string = '/%s'
feeds_view_default_path = 'news'
feeds_view_default_type = 'page'
feeds_view_default_title = ''

feed_add_url = '/feed/add'
feed_add_title = 'Add Feed'
feed_add_redirect_url = '/feed/management'

feed_edit_url = '/feed/([0-9]+)/edit'
feed_edit_url_string = '/feed/%s/edit'
feed_edit_title = 'Edit Feed'
feed_edit_redirect_url = '/feed/management'

feed_delete_url = '/feed/([0-9]+)/delete'
feed_delete_url_string = '/feed/%s/delete'
feed_delete_title = 'Delete Feed'
feed_delete_redirect_url = '/feed/management'

feed_management_url = '/feed/management'
feed_management_title = 'Manage Feeds'

feed_permissions_url = '/feed/permissions'
feed_permissions_title = 'Manage Feed Permissions'

feed_add_form_label_title = 'Title:'
feed_add_form_label_path = 'Path:'
feed_add_form_label_path_from_title = 'Get from title'
feed_add_form_label_type = 'Type:'
feed_add_form_label_cover = 'Select Cover'
feed_add_form_label_background = 'Select Background'
feed_add_form_label_photos = 'Attach Photos'
feed_add_form_label_musics = 'Attach Musics'
feed_add_form_label_content = 'Content:'
feed_add_form_label_published = 'Published'
feed_add_form_label_submit = 'Save'
feed_add_form_label_cancel = 'Cancel'

feed_edit_form_label_title = 'Title:'
feed_edit_form_label_path = 'Path:'
feed_edit_form_label_path_from_title = 'Get from title'
feed_edit_form_label_type = 'Type:'
feed_edit_form_label_cover = 'Select Cover'
feed_edit_form_label_background = 'Select Background'
feed_edit_form_label_photos = 'Attach Photos'
feed_edit_form_label_musics = 'Attach Musics'
feed_edit_form_label_content = 'Content:'
feed_edit_form_label_published = 'Published'
feed_edit_form_label_submit = 'Save'
feed_edit_form_label_cancel = 'Cancel'

feed_delete_form_label_question = 'Are you sure you want to delete this feed?'
feed_delete_form_label_question_string = 'Are you sure you want to delete %s "%s"?'
feed_delete_form_label_submit = 'Yes'
feed_delete_form_label_cancel = 'No'

feed_management_form_label_title = 'Title'
feed_management_form_label_type = 'Type'
feed_management_form_label_published = 'Published'
feed_management_form_label_management_links = 'Management Links'
feed_management_form_label_view = 'View'
feed_management_form_label_view_title = 'View Feed'
feed_management_form_label_edit = 'Edit'
feed_management_form_label_edit_title = 'Edit Feed'
feed_management_form_label_delete = 'Delete'
feed_management_form_label_delete_title = 'Delete Feed'
feed_management_form_label_add = 'Add Feed'
feed_management_form_label_add_title = 'Add Feed'
feed_management_form_label_permissions = 'Permissions'
feed_management_form_label_permissions_title = 'Feed Permissions'

#---------------sponsor module-------------

sponsor_title_trimmed = 1000

sponsor_logo = 180
sponsor_logo_w = 180
sponsor_logo_h = 120

sponsor_block_logo = 180
sponsor_block_logo_w = 260
sponsor_block_logo_h = 260

sponsor_probabilities = [{'value': 25, 'label': '1/4'},
                         {'value': 33, 'label': '1/3'},
                         {'value': 50, 'label': '1/2'},
                         {'value': 100, 'label': '1'},
                         {'value': 200, 'label': '2'},
                         {'value': 300, 'label': '3'},
                         {'value': 400, 'label': '4'}]

sponsors_per_request = 100
sponsors_per_page = 15
sponsors_per_row = 3
sponsors_per_block = 3

sponsor_record_clicks_message = 'Click statistics disabled.'
sponsor_record_impressions_message = 'Impression statistics disabled.'

sponsors_view_background = '/static/images/sponsors_view_background.jpg'

sponsor_add_url = '/sponsor/add'
sponsor_add_title = 'Create Sponsor'
sponsor_add_redirect_url = '/sponsor/management'

sponsor_edit_url = '/sponsor/([0-9]+)/edit'
sponsor_edit_url_string = '/sponsor/%s/edit'
sponsor_edit_title = 'Edit Sponsor'
sponsor_edit_redirect_url = '/sponsor/management'

sponsor_delete_url = '/sponsor/([0-9]+)/delete'
sponsor_delete_url_string = '/sponsor/%s/delete'
sponsor_delete_title = 'Delete Sponsor'
sponsor_delete_redirect_url = '/sponsor/management'

sponsor_management_url = '/sponsor/management'
sponsor_management_title = 'Manage Sponsors'

sponsor_permissions_url = '/sponsor/permissions'
sponsor_permissions_title = 'Manage Sponsor Permissions'

sponsor_view_url = '/sponsor/([0-9]+)'
sponsor_view_url_string = '/sponsor/%s'
sponsor_view_title = 'View Sponsor'

sponsor_redirect_url = '/sponsor/([0-9]+)/redirect'
sponsor_redirect_url_string = '/sponsor/%s/redirect'

sponsors_view_url = '/sponsors'
sponsors_view_title = 'SPONSORS'

sponsor_blocks_url = '/sponsor-blocks'

sponsor_view_label_title = 'View Sponsor'
sponsor_view_label_url = 'URL:'
sponsor_view_label_probability = 'Probability:'
sponsor_view_label_logo = 'Logo:'
sponsor_view_label_clicks = 'Clicks:'
sponsor_view_label_impressions = 'Impressions:'

sponsor_add_form_label_title = 'Title:'
sponsor_add_form_label_url = 'URL:'
sponsor_add_form_label_probability = 'Probability:'
sponsor_add_form_label_logo = 'Select Logo'
sponsor_add_form_label_published = 'Published'
sponsor_add_form_label_record_clicks = 'Record Clicks'
sponsor_add_form_label_record_impressions = 'Record Impressions'
sponsor_add_form_label_submit = 'Save'
sponsor_add_form_label_cancel = 'Cancel'

sponsor_edit_form_label_title = 'Title:'
sponsor_edit_form_label_url = 'URL:'
sponsor_edit_form_label_probability = 'Probability'
sponsor_edit_form_label_logo = 'Select Logo'
sponsor_edit_form_label_published = 'Published'
sponsor_edit_form_label_record_clicks = 'Record Clicks'
sponsor_edit_form_label_record_impressions = 'Record Impressions'
sponsor_edit_form_label_submit = 'Save'
sponsor_edit_form_label_cancel = 'Cancel'

sponsor_delete_form_label_question = 'Are you sure you want to delete this sponsor?'
sponsor_delete_form_label_question_string = 'Are you sure you want to delete "%s" sponsor?'
sponsor_delete_form_label_submit = 'Yes'
sponsor_delete_form_label_cancel = 'No'

sponsor_management_form_label_add = 'Add Sponsor'
sponsor_management_form_label_add_title = 'Add Sponsor'
sponsor_management_form_label_permissions = 'Permissions'
sponsor_management_form_label_permissions_title = 'Sponsor Permissions'
sponsor_management_form_label_view = 'View'
sponsor_management_form_label_view_title = 'View Sponsor'
sponsor_management_form_label_edit = 'Edit'
sponsor_management_form_label_edit_title = 'Edit Sponsor'
sponsor_management_form_label_delete = 'Delete'
sponsor_management_form_label_delete_title = 'Delete Sponsor'


landing_page_trim = 900
