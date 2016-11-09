/*
Copyright (c) 2003-2010, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.editorConfig = function( config )
{
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	
    config.extraPlugins = 'photo_manager,music_manager,file_manager';
    config.toolbar_Full.push (['Pmanager']);
    config.toolbar_Full.push (['Fmanager']);
    config.toolbar_Full.push (['Mmanager']);
    config.toolbar = 'Full';
};
