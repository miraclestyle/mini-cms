if (window.Elvin) Elvin = {}




Elvin = {
		// here are dialog options
		
		dialog_defaults : {
				autoOpen : false,
				modal : true,
				width : '960px',
				height : 'auto',
				close: function(event, ui) {Elvin.create_dialog();}	
		},
		init : function () {
			Elvin.create_dialog();	   
		},
		create_dialog: function () { $( "#ajax_dialog" ).dialog(this.dialog_defaults); },
		// this is used if you want to re-configure the dialog before it gets open
	    configure : function (o) {
			 if (typeof (o) == 'object') {
				    for(var p in o) {
				    	if (p == 'content') $("#ajax_dialog").html(o[p]);
				    	$("#ajax_dialog").dialog('option', p, o[p]);
				    }
			 }
	    },
        log : function (a) {
            if (window.Debug && window.Debug.writeln) {
                 window.Debug.writeln(a);
             } else if (window.console) window.console.log(a);	
         },
        /// usage : <a href="/path" onclick="return Elvin.dialog(this.href, { success: function (data)  { alert(data); } }, { .. if you want dialog options});"
        dialog: function (url, ajax_options, dialog_options) {
        	if (ajax_options == undefined) ajax_options = {}
        	if (dialog_options == undefined) dialog_options = {}
        	var opts = {
        		 url: url,
        		 dataType: 'json',
        		 success : function (data) {
        			 $("#ajax_dialog").html(data.content); 
        		 }
        	 }
        	for (prop in ajax_options) {
        		opts[prop] = ajax_options[prop];
        	}
        	Elvin.configure(dialog_options);
        	$.ajax(opts);
        	$("#ajax_dialog").dialog('open');
        	return false;
        },
       filemanager : {
        	instance : false,
        	poptions : {},
        	selected : {},
          
        	open : function (options) {
        		// create fresh dialog and close current instance of filemanager
        		var brofist = '<iframe src="/file/management?frame=1" style="width:960px;min-height:650px;border:none;"></iframe>';
        		Elvin.filemanager.close();
        		if (!options['ckeditor']) {  		
        		Elvin.create_dialog();
        		Elvin.configure({'width' : '990px'});
        		$("#ajax_dialog").html(brofist)
        		$("#ajax_dialog").dialog('open');
        		}
        		this.instance = true;
        		this.poptions = options;
        		return brofist;
        	},
       
        	close: function () {
        		if (this.instance == true) {
        		if (!this.poptions['ckeditor']) {
        		 Elvin.create_dialog(); 	
        		$("#ajax_dialog").dialog('close'); }
        	 
        		this.instance = false;
        		this.poptions = {};
        		this.selected = {}
        		return false;	
        		
        		}
        	},
        	
   
        	select : function (file) {
        		if (!Elvin.filemanager.instance) return false;
        		
        	  	var rel = $(file).attr('data-key');	
            	if ($(file).hasClass('selected-file')) {
            		 delete this.selected[rel];
            		 
            		 Elvin.log('deselected: '+ rel);
            		 
            		 $(file).removeClass('selected-file');
            		
            		
            	} else {
            		file['data-file-view'] = $(file).attr('data-src');
            		file['data-file-title'] = $(file).find('.file-title').html();
            		this.selected[rel] = file;
            		$(file).addClass('selected-file');
            		
            		Elvin.log('selected: '+ rel);
            		
            		
            	}
     
            	return false;
        	},
        	
       
        	deselectAll: function () {
        		
        		$('.files-grid .selected-file').each (function (index) {
    				
     		          $(this).removeClass('selected-file');
            		
       	        });
        		
        		this.selected = {}
        		
        		
        		Elvin.log('deselected all');
        		
        	},
        	
           ckeditorHandle : function () {
        	var files = [];
         
        	
	       		for (var rel in this.selected)
	    			
	    		{
	        	
	       			files.push('<a target="_blank" href="'+this.selected[rel]['data-file-view']+'" class="file-selected-inform">'+this.selected[rel]['data-file-title']+'</a>')
	    	 
	    	        
	    	     }
        	   
             
                return files.join('');
        	   
           },
        	
       
        	handleSelecteds: function () {
        		
        		if (this.poptions['custom'] || this.poptions['ckeditor']) return;
        		
        		    var files = [];
	        		
	        		if (this.poptions['size'] != 0) size = 1; else size = 'all';
	        		
	        	var i = 0;	
	    		for (var rel in this.selected)
	    			
	    		{
                    i++;
                    if (size == 1 && i > 1) { break; }
            
   
	    	        if ($('#'+this.poptions['type']+'').find('#file-'+rel+'').length < 1) {
	    	        	
	    	        	files.push('<div id="file-'+this.poptions['type']+'-'+rel+'" rel="'+rel+'" class="selected-files-box"><input type="hidden" name="'+this.poptions['type']+'" value="'+rel+'" /><div class="file-view"><a href="'+this.selected[rel]['data-file-view']+'" class="file-selected-inform">'+this.selected[rel]['data-file-title']+'</a><a class="deleteimg" onclick="$(\'#file-'+this.poptions['type']+'-'+rel+'\').remove();" href="javscript:;">X</a></div></div>')
	    	       
	    	        }
	    	        
	    	        
	    	        }
	    		if (size == 1) { 
	    		$('#'+this.poptions['type']+'').html(files.join(''));
	    		} else {
	    			
	    			$('#'+this.poptions['type']+'').append(files.join(''));
	    		}
	    		
        	},

        
        	insertAll : function () {
        		try {
                if (this.poptions['custom']) {
                	
                	eval(this.poptions['custom']);
                	
                } else {
                	
                	Elvin.filemanager.handleSelecteds();
                }
        		Elvin.filemanager.close();
 
        		 
        	    } catch (e) {
        			
        			Elvin.log('cannot process insertAll function because the array of files selected is empty');
        		}
        	}
	
        },
        photomanager : {
        	instance : false,
        	poptions : {},
        	selected : {},
            /**
             * @usage onclick="return Elvin.photomanager.open('#input_id_that_recives_values');"
             */
        	open : function (options) {
        		// create fresh dialog and close current instance of photomanager
        		var brofist = '<iframe src="/photo/management?frame=1" style="width:960px;min-height:700px;border:none;"></iframe>';
        		Elvin.photomanager.close();
        		if (!options['ckeditor']) {  		
        		Elvin.create_dialog();
        		Elvin.configure({'width' : '990px'});
        		$("#ajax_dialog").html(brofist)
        		$("#ajax_dialog").dialog('open');
        		}
        		this.instance = true;
        		this.poptions = options;
        		return brofist;
        	},
        	/**
        	 * @usage onclick="return Elvin.photomanager.close();" this closes the photomanager dialog
        	 * correctly, please use this function instead $("#ajax_dialog").dialog('close');
        	 */
        	close: function () {
        		if (this.instance == true) {
        		if (!this.poptions['ckeditor']) {
        		 Elvin.create_dialog(); 	
        		$("#ajax_dialog").dialog('close'); }
        	 
        		this.instance = false;
        		this.poptions = {};
        		this.selected = {}
        		return false;	
        		
        		}
        	},
        	
        	/**
        	 * @usage this goes on <img> tags, so it goes like this
        	 * @notice for the record, the "selected_image" is the class used to define the style for "selected image"
        	 * <img onclick="return Elvin.photomanager.select(this);" rel="the_key_of_image" />
        	 */
        	select : function (image) {
        		if (!Elvin.photomanager.instance) return false;
        		
        	  	var rel = $(image).attr('rel');	
            	if ($(image).hasClass('selected-photo')) {
            		 delete this.selected[rel];
            		 
            		 Elvin.log('deselected: '+ rel);
            		 
            		 $(image).removeClass('selected-photo');
            		
            		
            	} else {
            		
            		this.selected[rel] = image;
            		$(image).addClass('selected-photo');
            		
            		Elvin.log('selected: '+ rel);
            		
            		
            	}
     
            	return false;
        	},
        	
        	/**
        	 * @usage the function that is used to deselect all images onclick="return Elvin.photomanager.deselectAll();"
        	 */
        	deselectAll: function () {
        		
        		$('.photos-grid .photo img.selected-photo').each (function (index) {
    				
     		          $(this).removeClass('selected-photo');
            		
       	        });
        		
        		this.selected = {}
        		
        		
        		Elvin.log('deselected all');
        		
        	},
        	
           ckeditorHandle : function () {
        	var images = [];
        	
	       		for (var rel in this.selected)
	    			
	    		{
	        	
	    			images.push('<img src="'+this.selected[rel].src+'" />')
	    	 
	    	        
	    	     }
        	   
 
                return images.join('');
        	   
           },
        	
        /**
         * @usage will handle the selected images based on params
         */
        	handleSelecteds: function () {
        		
        		if (this.poptions['custom'] || this.poptions['ckeditor']) return;
        		
        		    var images = [];
	        		
	        		if (this.poptions['size'] != 0) size = 1; else size = 'all';
	        		
	        	var i = 0;	
	    		for (var rel in this.selected)
	    			
	    		{
                    i++;
                    if (size == 1 && i > 1) { break; }
                    Elvin.log('finding #img-'+rel+' in #'+this.poptions['type']+'');
   
	    	        if ($('#'+this.poptions['type']+'').find('#img-'+rel+'').length < 1) {
	    	        	
	    			images.push('<div id="img-'+this.poptions['type']+'-'+rel+'" rel="'+rel+'" class="photo-selected"><input type="hidden" name="'+this.poptions['type']+'" value="'+rel+'" /><div class="photo"><img src="'+this.selected[rel].src+'" /><a class="deleteimg" onclick="$(\'#img-'+this.poptions['type']+'-'+rel+'\').remove();" href="javscript:;">X</a></div></div>')
	    	       
	    	        }
	    	        
	    	        
	    	        }
	    		if (size == 1) { 
	    		$('#'+this.poptions['type']+'').html(images.join(''));
	    		} else {
	    			
	    			$('#'+this.poptions['type']+'').append(images.join(''));
	    		}
	    		
        	},

        	/**
        	 * @usage this function inserts list of selected items, IF no images is selected it wont do anything 
        	 * @notice calling this function will deselect images after inserting values into the input field
        	 * @usage the html usage is onclick="return Elvin.photomanager.insertAll();"
        	 */
        	insertAll : function () {
        		try {
                if (this.poptions['custom']) {
                	
                	eval(this.poptions['custom']);
                	
                } else {
                	
                	Elvin.photomanager.handleSelecteds();
                }
        		Elvin.photomanager.close();
 
        		 
        	    } catch (e) {
        			
        			Elvin.log('cannot process insertAll function because the array of images selected is empty');
        		}
        	}
	
        },
        musicmanager : {
        	instance : false,
        	poptions : {},
        	selected : {},
            /**
             * @usage onclick="return Elvin.photomanager.open('#input_id_that_recives_values');"
             */
        	open : function (options) {
        		// create fresh dialog and close current instance of photomanager
        		var brofist = '<iframe src="/track/management?frame=1" style="width:960px;min-height:650px;border:none;"></iframe>';
        		Elvin.musicmanager.close();
        		if (!options['ckeditor']) {  		
        		Elvin.create_dialog();
        		Elvin.configure({'width' : '990px'});
        		$("#ajax_dialog").html(brofist)
        		$("#ajax_dialog").dialog('open');
        		}
        		this.instance = true;
        		this.poptions = options;
        		return brofist;
        	},
        	/**
        	 * @usage onclick="return Elvin.photomanager.close();" this closes the photomanager dialog
        	 * correctly, please use this function instead $("#ajax_dialog").dialog('close');
        	 */
        	close: function () {
        		if (this.instance == true) {
        		if (!this.poptions['ckeditor']) {
        		 Elvin.create_dialog(); 	
        		$("#ajax_dialog").dialog('close'); }
        	 
        		this.instance = false;
        		this.poptions = {};
        		this.selected = {}
        		return false;	
        		
        		}
        	},
       
        	select : function (music) {
        		if (!Elvin.musicmanager.instance) return false;
        		
        	  	var rel = $(music).attr('data-key');	
            	if ($(music).hasClass('selected-music-file')) {
            		 delete this.selected[rel];
            		 
            		 Elvin.log('deselected: '+ rel);
            		 
            		 $(music).removeClass('selected-music-file');
            		
            		
            	} else {
            		
            		this.selected[rel] = {
            				
            				id : $(music).attr('data-id'),
            				file : $(music).attr('data-src'),
            				html : $(music).find('.music-file').html(),
            				title : $(music).find('.music-title')
            		};
            		 
            		$(music).addClass('selected-music-file');
            		
            		Elvin.log('selected: '+ rel);
            		
            		
            	}
     
            	return false;
        	},
        	
        	/**
        	 * @usage the function that is used to deselect all images onclick="return Elvin.photomanager.deselectAll();"
        	 */
        	deselectAll: function () {
        		
        		$('.musics-grid .list-item').each (function (index) {
    				
     		          $(this).removeClass('selected-music-file');
            		
       	        });
        		
        		this.selected = {}
        		
        		
        		Elvin.log('deselected all');
        		
        	},
        	
           ckeditorHandle : function () {
        	var music = [];
        	
	       		for (var rel in this.selected)
	    			
	    		{
	        	   // var skeleton = '<object type="application/x-shockwave-flash" name="audioplayer-'+this.selected[rel]['id']+'" style="outline: none" data="/static/add-ons/audio-player/player.swf" width="290" height="24" id="audioplayer-'+this.selected[rel]['id']+'"><param name="bgcolor" value="#FFFFFF"><param name="wmode" value="transparent"><param name="menu" value="false"><param name="flashvars" value="soundFile='+this.selected[rel]['file']+'&amp;playerID=audioplayer-'+this.selected[rel]['id']+'"></object>';
                    
	       			 var skeleton2 = '<div id="audioplayer-'+this.selected[rel]['id']+'" class="music-file"><a href="'+this.selected[rel]['file']+'" title="'+this.selected[rel]['title']+'" alt="'+this.selected[rel]['title']+'">'+this.selected[rel]['title_trimmed']+'</a></div>'
									  + '<script type="text/javascript">'
									  + 'if (!typeof(CKEDITOR) != "object")  {	AudioPlayer.embed("audioplayer-'+this.selected[rel]['id']+'", {soundFile: "'+this.selected[rel]['file']+'", titles: "'+this.selected[rel]['title']+'"});  }'
									  + '</script>';
	       			music.push('<div class="music-file-ckeditor-attached" id="music-file-'+rel+'>'+this.selected[rel]['html']+'</div>')
	    	 
	    	        
	    	     }
        	   
 
                 return music.join('');
        	   
           },
        	
        /**
         * @usage will handle the selected images based on params
         */
        	handleSelecteds: function () {
        		
        		if (this.poptions['custom'] || this.poptions['ckeditor']) return;
        		
        		    var music = [];
	        		
	        		if (this.poptions['size'] != 0) size = 1; else size = 'all';
	        		
	        	var i = 0;	
	    		for (var rel in this.selected)
	    			
	    		{
                    i++;
                    if (size == 1 && i > 1) { break; }
                    
   
	    	        if ($('#'+this.poptions['type']+'').find('#audio-'+rel+'').length < 1) {
	    	        	
	    	        	music.push('<div id="audio-'+this.poptions['type']+'-'+rel+'" rel="'+rel+'" class="music-selected"><input type="hidden" name="'+this.poptions['type']+'" value="'+rel+'" /><div class="music">'+this.selected[rel]['html']+'<a class="deleteaudio" onclick="$(\'#audio-'+this.poptions['type']+'-'+rel+'\').remove();" href="javscript:;">X</a></div></div>')
	    	       
	    	        }
	    	        
	    	        
	    	        }
	    		if (size == 1) { 
	    		$('#'+this.poptions['type']+'').html(music.join(''));
	    		} else {
	    			
	    			$('#'+this.poptions['type']+'').append(music.join(''));
	    		}
	    		
        	},
 
        	insertAll : function () {
        		try {
                if (this.poptions['custom']) {
                	
                	eval(this.poptions['custom']);
                	
                } else {
                	
                	Elvin.musicmanager.handleSelecteds();
                }
        		Elvin.musicmanager.close();
 
        		 
        	    } catch (e) {
        			
        			Elvin.log('cannot process insertAll function because the array of images selected is empty');
        		}
        	}
	
        }
}

AppearanceUtils = {
		
		verticalAlign : function(parent, element) {
			var parentheight = $(parent).height();
			var elementheight = $(element).height();
			var elementposition = (parentheight - elementheight)/2;
			var elementpositionvalue = 'padding-top: ' + elementposition + 'px;';
			var elementoldattributes = $(element).attr('style');
			if (elementoldattributes != undefined) {
				var elementattributes = elementoldattributes + ' ' + elementpositionvalue;
			}
			else {
				var elementattributes = elementpositionvalue;
			}
			$(element).attr('style', elementattributes);
		},

		horizontalAlign : function(parent, element) {
			var parentwidth = $(parent).width();
			var elementwidth = $(element).width();
			var elementposition = (parentwidth - elementwidth)/2;
			var elementpositionvalue = 'padding-left: ' + elementposition + 'px;';
			var elementoldattributes = $(element).attr('style');
			if (elementoldattributes != undefined) {
				var elementattributes = elementoldattributes + ' ' + elementpositionvalue;
			}
			else {
				var elementattributes = elementpositionvalue;
			}
			$(element).attr('style', elementattributes);
		},
		
		showHide : function(triggerclass, triggeridprefix, hiddenclass, hiddenidprefix, shownclass) {
			$('.'+triggerclass).click(function() {
				var id = $(this).attr("show-hide-id");
				var trigger = "#" + triggeridprefix + id;
			    var hidden = "#" + hiddenidprefix + id;
			    $('.'+hiddenclass).hide();
			    if ($(this).hasClass(shownclass)) {
			    	$(this).removeClass(shownclass);
				}
			    else {
			    	$('.'+triggerclass).removeClass(shownclass);
			    	$(trigger).addClass(shownclass);
			    	$(hidden).show();
			    }
			    return false;
			  });
		},
		
		hoverInOut : function(hoverclass, hoverinclass) {
			$('.'+hoverclass).hover(
			  function () {
				  $(this).addClass(hoverinclass);
			  }, 
			  function () {
				  $(this).removeClass(hoverinclass);
			  }
			);
		},
}

StringManipulation = {
		setPath : function(title_id, slug_id) {

		    var slug = document.getElementById(title_id).value;
		
		    var slug = slug.replace(/^\s+|\s+$/g, ''); // trim
		    var slug = slug.replace(/[^a-zA-Z0-9 -]/g, ''); // remove invalid chars
		    var slug = slug.replace(/\s+/g, '-'); // collapse whitespace and replace by -
		
		    document.getElementById(slug_id).value = slug.toLowerCase();
		}
}


$(document).ready(function() {
	
	
	Elvin.init();
	$("a.fancybox").fancybox({
		'padding'			:	0,
		'margin'			:	20,
		'overlayColor'		:	'#CCCCCC',
		'overlayOpacity'	:	'0.5',
		FBlike 				:   '<fb:like href="[URL]" layout="button_count" show_faces="false" width="100" colorscheme="dark"></fb:like><script>FB.XFBML.parse();</script>'
		//ajax 				: {
									//type : "GET",
							        //dataType: 'json',
							        //success : function (a, data)
							        //{
							        	//return data.content;
							        //}
								//}


		});
});
