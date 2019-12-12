/*
Updated on 12/9/2018 
Features:
1. Can upload image, video and audio from local drive.
2. Can upload image, video and audio from web.
   i). Can upload youtube video using link and embed youtube video code .
   ii). Can upload dailymotion video using link and embed the dailymotion video code 
   iii). Can upload vimeo video using link and embed the vimeo video code 
   iv). Can delete the audio/image/video file from the wysiswyg editor. 
   v). wistia video => haven't done the video upload testing yet !! 
   vi). google map video => not working ... 
   vii). facebook/twitter => not working ...
*/

(function (document) {

  var REGEX_TYPE_VIDEO = /video\/*/;
  var REGEX_TYPE_IMAGE = /image\/*/;
  var REGEX_TYPE_AUDIO = /audio\/*/;
  var REGEX_URL = /^https?:\/\//;
  var REGEX_VIDEO = /\.(webm|ogg|mp4)$/i;
  var REGEX_IMAGE = /\.(jpe?g|png|gif)$/i;
  var REGEX_AUDIO = /\.(wav|mp3)$/i;
  var REGEX_YOUTUBE = /^https?:\/\/www.youtube.com\/watch\?v=(.+)|^https?:\/\/youtu.be\/(.+)/;
  var REGEX_YOUTUBE_EMBED = /youtube.com\/embed\/([a-z0-9\-_]+(?:\?.+)?)/i; // pky - copied from the media plugin regex there 
  //var REGEX_FACEBOOK = /^(https?:\/\/)?(www\.)?facebook.com\/[a-zA-Z0-9(\.\?)?]/; // pky - check facebook link -- need facebook developer integration ... 
  var REGEX_DAILYMOTION = /dailymotion\.com\/video\/([^_]+)/; // pky - copied from the media regex there 
  var REGEX_DAILYMOTION_EMBED = /dailymotion.com\/embed\/video\/([a-z0-9\-_]+(?:\?.+)?)/i; // pky dailymotion embed link -- still testing 
  
  // pky 12/9/2018 take reference from this web, https://www.regextester.com/96504
  // still testing - not working 
  //var REGEX_GOOGLE_EMBED = /(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))?/;  
  var REGEX_VIMEO = /^https?:\/\/vimeo.com\/(\d+(\?.+)*)/;
  var REGEX_VIMEO_EMBED = /\/player.vimeo.com\/video\/([a-z0-9\-_]+)/;  // pky check embed vimeo video regex 
  var REGEX_WISTIA = /^https?:\/\/\w+\.wistia\.com\/medias\/(.+)/;
  var REGEX_MESSAGE_TOKEN = /\*(.*?)\*/g;
  var DEFAULT_BUTTON_TEXT = '▶♫';

  var iframesrc;  // pky global variable 
	
  //--------------------------------------------------
  // Plugin
  //--------------------------------------------------

  // Register media uploader plugin with TinyMCE
  tinymce.PluginManager.add('mediauploader', function (editor, url) {
    var image = getParam(editor, 'button_image');
    var text = getMessage(editor, 'button_text', DEFAULT_BUTTON_TEXT);

    editor.addCommand('InsertMediaUploader', function() {

      //console.log('triggered - 1 ');
      var element = getDOMNode(editor);
      
	  // fix Only allow one at a time
	  if (element) {
         element.focus();
         return;
      }

      renderComponent(editor);
      componentDidMount(editor); 

    });

    editor.addButton('mediauploader', {
      image: image,
      title: getMessage(editor, 'button_title', 'Upload Media'),
      text: (image && text === DEFAULT_BUTTON_TEXT) ? null : text,
      onclick: function () {
        editor.execCommand('InsertMediaUploader');
        //console.log('triggered - 2 ');
      }
    });
  });

  //--------------------------------------------------
  // Component API
  //--------------------------------------------------

  /**
   * Render the component to the TinyMCE editor DOM
   *
   * @param {object} editor TinyMCE editor
   */
  function renderComponent(editor) {
    var msgAddMedia = getMessage(editor, 'msg_add_media', 'Add a video, image, or audio file');
    var msgPasteUrl = getMessage(editor, 'msg_paste_url', 'Paste URL');
    var msgDragDrop = getMessage(editor, 'msg_drag_drop', 'Drag and drop or *Upload a File*');

    editor.insertContent(
      '<div contenteditable="false" class="media-uploader" tabindex="-1" id="media-uploader">' +
        '<i class="media-uploader__close">&nbsp;</i>' +
        '<div class="media-uploader__type">' + msgAddMedia + '</div>' +
        '<div class="media-uploader__urlbox">' +
          '<input type="text" class="media-uploader__url" placeholder="' + msgPasteUrl + '" aria-label="' + msgPasteUrl + '"/>' +
          '<p class="error"></p>' +
        '</div>' +
        '<span class="media-uploader__prompt">' +
          msgDragDrop.replace(REGEX_MESSAGE_TOKEN,
            '<label tabindex="0">$1' +
              '<span class="media-uploader__file">' +
                '<input type="file" id="file-id" style="display: none;" accept="video/*,image/*,audio/*"/>' +
              '</span>' +
            '</label>' +
			'<button type="button" id="media-uploader-remove__file">Remove file(s)</button>' 
          ) +
        '</span>' +
      '</div>'
    );
  }

  
  /**
   * Remove the component from the TinyMCE editor DOM
   *
   * @param {object} editor TinyMCE editor
   */
  function unmountComponent(editor) {
    var element = getDOMNode(editor);
    componentWillUnmount(editor);
    element.parentNode.removeChild(element);
  }

  /**
   * Lifecycle method to handle the component being removed from the DOM
   *
   * @param {object} editor TinyMCE editor
   */
  function componentWillUnmount(editor) {
    var element = getDOMNode(editor);

    element.ondragover = null;
    element.ondragend = null;
    element.ondrop = null;
    document.removeEventListener('dragover', eventPreventDefault);
    document.removeEventListener('drop', eventPreventDefault);

    try {
      element.querySelector('input[type=file]').onchange = null;
      element.querySelector('input[type=text]').onpaste = null;
    } catch (e) {
      // Error is probably from upload file modifying the DOM
    }
  }

  /**
   * Lifecycle method to handle the component being inserted to the DOM
   *
   * @param {object} editor TinyMCE editor
   */
  function componentDidMount(editor) {
    var doc = editor.iframeElement.contentDocument;
	console.log('doc=> ', doc);
	
    var element = getDOMNode(editor);
	//console.log('element=> ', element);
    element.focus();

    document.addEventListener('dragover', eventPreventDefault);
    document.addEventListener('drop', eventPreventDefault);

    element.ondragover = function () {
      element.classList.add('media-uploader--dragover');
      return false;
    };

    element.ondragend = function () {
      element.classList.remove('media-uploader--dragover');
      return false;
    };

    element.ondrop = function (e) {
      element.classList.remove('media-uploader--dragover');
      e.preventDefault();

      uploadFile(editor, e.dataTransfer.files[0]);

      return false;
    };

    element.querySelector('.media-uploader__close').onclick = function () {
      unmountComponent(editor);
    };

	
	// pky - add border to the media plugin 
	var tinymce_id = doc.getElementById('media-uploader');
	tinymce_id.style.border = "1px solid black";
	
	// pky add the media-uploader-remove__file css style 
	var get_button_uploaded_remove_file = doc.getElementById('media-uploader-remove__file');
	//style="float:right;border: 1px solid black;margin-right:20px; font-size:20px;
	//console.log('get_button_uploaded_remove_file', get_button_uploaded_remove_file);
	get_button_uploaded_remove_file.style.float="right";
	get_button_uploaded_remove_file.style.border="1px solid black";
	get_button_uploaded_remove_file.style.marginRight="20px";
	get_button_uploaded_remove_file.style.fontSize="20px";
		
	/* pky - delete the media */
	element.querySelector('#media-uploader-remove__file').onclick = function(){
	console.log('remove media file is triggred!');
	//console.log('remove media file => ', editor);
	
		  /* pky - get video element*/
        function getPDomForVideo(editor){
			return doc.getElementsByTagName("video");
       }
	   
	   /* pky - get the audio element */
	   function getPDomForAudio(editor){
			return doc.getElementsByTagName("audio");
       }
	   
	   /* pky - get the image element */
	   function getPDomForImage(editor){
			return doc.getElementsByTagName("img");
	   }

	   /* pky - get the iframe element */
	   function getPDomForEmbed(editor){
			return doc.getElementsByTagName("iframe");
	   }
		var getPDomVideo = getPDomForVideo(editor);
		var getPDomAudio = getPDomForAudio(editor);
		var getPDomImage = getPDomForImage(editor);
		var getPDomEmbed = getPDomForEmbed(editor);

		if(getPDomVideo.length!=0 || getPDomAudio.length!=0 || getPDomImage.length!=0 || getPDomEmbed.length!=0){
		//console.log('getPDomVideo=> ', getPDomVideo);
		//console.log('getPDomAudio=> ', getPDomAudio);
		//console.log('getPDomVideo - length=> ', getPDomVideo.length); // length increases because of inserting media 
		//console.log('getPDomVideo[0]=> ', getPDomVideo[0]); //  get full <video src=''> ...... </video>
		//console.log('getPDomVideo src => ', getPDomVideo[0].src); // video src 
			if(getPDomVideo.length > 0 && REGEX_VIDEO.test(getPDomVideo[0].src)){  // logic problem here handler!!
				getPDomVideo[0].remove(); // remove the video file 
			}else
			if(getPDomAudio.length > 0 && REGEX_AUDIO.test(getPDomAudio[0].src)){
				getPDomAudio[0].remove(); // remove the audio file 
			}else
			if(getPDomImage.length > 0 && REGEX_IMAGE.test(getPDomImage[0].src)){
				getPDomImage[0].remove(); // remove the image file 
			}else
			if(getPDomEmbed.length > 0){
				getPDomEmbed[0].remove();  // remove the embed file 
			}
		}

	}
	element.focus();
	
	/* end of pky */
    var fileInput = element.querySelector('input[type=file]');
	fileInput.onchange = function (e) {
	   console.log('e=> ', e.target.files);
	  uploadFile(editor, e.target.files[0]);
    };

    var urlInput = element.querySelector('input[type=text]');
    urlInput.onpaste = function (e) {
      clearError(editor);
      setTimeout(function () {
        embedMedia(editor, urlInput.value);
      }, 0);
    };
    // keep the editor from hijacking key strokes
    urlInput.onkeydown = function (e) {
      e.stopPropagation();
    };
  }

  /**
   * Get the media uploader plugin widget's DOM node
   *
   * @param {object} editor TinyMCE editor
   * @return {element}
   */
  function getDOMNode(editor) {
    var doc = editor.iframeElement.contentDocument;
    return doc.getElementById('media-uploader');
  }

  /**
   * Replace the plugin widget with another element
   *
   * @param {object} editor TinyMCE editor
   * @param {element} newChild The child to replace plugin widget with
   */
  function replaceComponent(editor, newChild) {
    var element = getDOMNode(editor);
    componentWillUnmount(editor);
    element.parentNode.replaceChild(newChild, element);
  }

  //--------------------------------------------------
  // Upload/embed media
  //--------------------------------------------------

  // List of matchers to handle embedding media
  var matchers = (function () {
    function EmbedMatcher(regex, embed) {
      this.regex = regex;
      this.embed = embed;
    }

    function createMedia(tagName, src) {
	  var create_div = document.createElement('div'); // create div element 
	  //console.log('div=> ', create_div);
	  create_div.setAttribute('id', 'video-controls');
	  
      var media = document.createElement(tagName);
	  console.log('media - create element => ', media);
	  
	if(REGEX_VIDEO.test(src)== true || REGEX_IMAGE.test(src) == true || REGEX_AUDIO.test(src) == true){
		 /* pky 7/9/2018 - add in the local media location */  
		var loc = window.location.pathname; // loc 
		var dir = loc.substring(0, loc.lastIndexOf('/')); // dir 
		//src = dir + '/media/' + src; 
		//src = {{ STATIC_URL }} + '/media/' + src;
		console.log('video & image & audio are triggered!');
	  }
	  if(REGEX_VIDEO.test(src)==true){  // video media 
	  console.log('video layout is displayed!');
	  media.src = src; 
	  media.controls = true;
	  media.width = 400;
	  media.height= 400;
	  media.id = 'media-uploader-video'; // video id 
	  }
	  // display the image layout 
	  else if(REGEX_IMAGE.test(src) == true){
		  console.log('image layout is displayed !');
		  media.src = src; 
		  media.height = 400; 
		  media.width = 400;
	  // display the audio layout 
	  }else if(REGEX_AUDIO.test(src) == true){
		  console.log('audio layout is displayed!');
		  media.src = src;
		  media.controls = true;
		  media.id = 'media=uploader-audio';
	  }else{
      media.src = src;  // web src only 
	  }
	  
      return media;
    }
	
    function createIFrame(src, parentNode) {
	  console.log('createIFrame - src => ', src);
	/* if(REGEX_VIDEO.test(src)== true ){
		var embed = document.createElement('embed');
		 pky 7/9/2018 get the media location
		var loc = window.location.pathname; // loc 
		var dir = loc.substring(0, loc.lastIndexOf('/')); // dir 
		src = dir + '/media/' + src;
		console.log('src123=> ', src);
		console.log('embed=> ', embed);
		console.log('video iframe are triggered!');
		embed.src = src; 
		embed.width = 400;
		embed.height=400;
		embed.id = "iframe-test";
		embed.type="video/mp4";
		return embed;
	  */
	  var iframe = document.createElement('iframe');
	  console.log('iframe=> ', iframe);
	  var width = parentNode.offsetWidth;
      var height = Math.floor((width / 16) * 9);
      iframe.src = src;
      iframe.width = width;
      iframe.height = height;
      iframe.frameborder = 0;
      iframe.allowfullscreen = true;
	   return iframe;
    }

    return [
        new EmbedMatcher(REGEX_VIDEO, function (mediaUrl) {
        return createMedia('video', mediaUrl);
      }), 
      new EmbedMatcher(REGEX_IMAGE, function (mediaUrl) {
        return createMedia('img', mediaUrl);
      }),
      new EmbedMatcher(REGEX_AUDIO, function (mediaUrl) {
        return createMedia('audio', mediaUrl);
      }),
	  /* pky - facebook link is not working  */
      /*new EmbedMatcher(REGEX_FACEBOOK, function (mediaUrl) {
        return createMedia('video', mediaUrl);
      }),*/
      new EmbedMatcher(REGEX_YOUTUBE, function (mediaUrl, parentNode) {
        var matches = mediaUrl.match(REGEX_YOUTUBE);
        return createIFrame('//www.youtube.com/embed/' + (matches[1] || matches[2]), parentNode);
      }),
	  /* pky add in the embed youtube video  */
	  new EmbedMatcher(REGEX_YOUTUBE_EMBED, function (mediaUrl, parentNode) {
        var matches = mediaUrl.match(REGEX_YOUTUBE_EMBED);
        return createIFrame('//www.youtube.com/embed/' + (matches[1] || matches[2]), parentNode);
      }),
	  /* pky add in the dailymotion video link  */
	  new EmbedMatcher(REGEX_DAILYMOTION, function (mediaUrl, parentNode) {
        var matches = mediaUrl.match(REGEX_DAILYMOTION);
        return createIFrame('//www.dailymotion.com/embed/video/' + (matches[1] || matches[2]), parentNode);
      }),
	  /* pky add in the embed dailymotion video */
	  new EmbedMatcher(REGEX_DAILYMOTION_EMBED, function (mediaUrl, parentNode){
        var matches = mediaUrl.match(REGEX_DAILYMOTION_EMBED);
		//console.log('dailymotion matches=> ', matches[1] );
		//console.log('dailymotion matches22334=> ', matches.input);
		return createIFrame('//www.dailymotion.com/embed/video/' + matches[1], parentNode);
	  }),

      new EmbedMatcher(REGEX_VIMEO, function (mediaUrl, parentNode) {
        var id = mediaUrl.match(REGEX_VIMEO)[1];
        return createIFrame('//player.vimeo.com/video/' + id, parentNode);
      }),
	  
	  /* pky add in the embed vimeo video code */
      new EmbedMatcher(REGEX_VIMEO_EMBED, function (mediaUrl, parentNode) {
        var id = mediaUrl.match(REGEX_VIMEO_EMBED)[1];
		//console.log('vimeo_embed_id=> ', id);
        return createIFrame('//player.vimeo.com/video/' + id, parentNode);
      }),
	  
	  /* pky add in the embed google map code */
	  /*new EmbedMatcher(REGEX_GOOGLE_EMBED, function (mediaUrl, parentNode) {
        //var id = mediaUrl.match(REGEX_GOOGLE_EMBED)[1];
		//console.log('vimeo_embed_id=> ', id);
        return createIFrame(mediaUrl, parentNode);
      }),*/
	  
      new EmbedMatcher(REGEX_WISTIA, function (mediaUrl, parentNode) {
        var id = mediaUrl.match(REGEX_WISTIA)[1];
        return createIFrame('//fast.wistia.com/embed/iframe/' + id, parentNode);
      })
    ];
  })();

  /**
   * Upload a file from file input, or dragdrop behavior
   *
   * @param {object} editor TinyMCE editor
   * @param {File} file The file to be uploaded
   */
  function uploadFile(editor, file) {
    // Validate file type
    if (!REGEX_TYPE_VIDEO.test(file.type) &&
        !REGEX_TYPE_IMAGE.test(file.type) &&
        !REGEX_TYPE_AUDIO.test(file.type)) {
      alert(getParam(editor, 'msg_invalid_file', "That doesn't appear to be an accepted media file."));
      return;
    }

    var upload_file = getParam(editor, 'upload_file');
    if (typeof upload_file === 'function') {
      upload_file(getDOMNode(editor), file, function (fileUrl, error) {
        if (!error) {
          embedMedia(editor, fileUrl);
        } else {
          alert(error.message || error);
        }
      });
    } else {
      console.warn('Missing option "mediauploader_upload_file"');
    }
  }

  /**
   * Embed a media URL into TinyMCE
   *
   * @param {object} editor TinyMCE editor
   * @param {string} mediaUrl URL of the media to embed
   */
  function embedMedia(editor, mediaUrl) {
	var urlInput = getDOMNode(editor).querySelector('input[type=text]');
	console.log('embedMedia - mediaFile678 => ', mediaUrl);
	
	///////////////////////////////////////////////
	// pky 12/9/2018 - doing the ajax call to the media upload here!
	 
	
	// DOING SOMETHING HERE !!! 
	// end of pky 
	//////////////////////////////////////////////
	
	
	
	//var type_video = REGEX_TYPE_VIDEO.test(mediaUrl);
	//console.log('type_video=> ', type_video);
	//var regex_video = REGEX_VIDEO.test(mediaUrl);
	//console.log('regex_video=> ', regex_video);
	//var dailymotion_embed = REGEX_DAILYMOTION_EMBED.test(mediaUrl);
	//console.log('regex_video_dailymotion => ', dailymotion_embed);
	//var regex_video_2 = REGEX_VIMEO_EMBED.test(mediaUrl);
	//console.log('regex_vimeo_embed=> ', regex_video_2);
	
    // Validate media url
    if (!REGEX_URL.test(mediaUrl) &&
        !REGEX_YOUTUBE.test(mediaUrl) &&
        !REGEX_VIMEO.test(mediaUrl) &&
        !REGEX_WISTIA.test(mediaUrl) &&
		!REGEX_VIDEO.test(mediaUrl) &&  /* pky add video regex */
		!REGEX_IMAGE.test(mediaUrl) &&  /* pky add image regex */ 
		!REGEX_AUDIO.test(mediaUrl) && /* pky add audio regex */
		!REGEX_YOUTUBE_EMBED.test(mediaUrl) &&  /* pky add youtube embed regex */ 
		!REGEX_DAILYMOTION.test(mediaUrl) && /* pky add dailymotion url regex */
		!REGEX_DAILYMOTION_EMBED.test(mediaUrl) && /* pky add dailymotion embed regex */
		!REGEX_VIMEO_EMBED.test(mediaUrl)  /* pky add vimeo embed code regex */
		/*!REGEX_GOOGLE_EMBED.test(mediaUrl)*/ /* pky add google map embed code regex */
		/*!REGEX_FACEBOOK.test(mediaUrl)*/ /* pky add facebook video */
		){
      markError(editor, getMessage(editor, 'msg_invalid_url', "That doesn't appear to be a URL."));
      return;
    }

    var element = getDOMNode(editor);
    var media = null;

    for (var i=0, l=matchers.length; i<l; i++) {
      var matcher = matchers[i];
      if (matcher.regex.test(mediaUrl)) { 
        media = matcher.embed(mediaUrl, element);
        break;
      }
    }

    if (!media) {
      markError(editor, getMessage(editor, 'msg_invalid_media', "That doesn't appear to be an embeddable URL."));
      urlInput.select();
    }

    replaceComponent(editor, media);

    var embed_media = getParam(editor, 'embed_media');
    if (typeof embed_media === 'function') {
      // embed_media(media);
       embed_media(media, editor); // pky 12/9/2018 - add in editor object 
    }
  }
  

  /**
   * Clear any error messages
   *
   * @param {object} editor TinyMCE editor
   */
  function clearError(editor) {
    var input = getDOMNode(editor).querySelector('.media-uploader__url');
    input.classList.remove('error');
    input.parentNode.querySelector('p').innerHTML = '&nbsp;';
  }

  /**
   * Indicate that an error occured
   *
   * @param {object} editor TinyMCE editor
   * @param {string} message The error message to display
   */
  function markError(editor, message) {
    var input = getDOMNode(editor).querySelector('.media-uploader__url');
	console.log('input=> ', input);
    input.classList.add('error');
    input.parentNode.querySelector('p').innerHTML = message;
    input.select();
  }

  /**
   * Get a plugin param value
   *
   * @param {object} editor TinyMCE editor
   * @param {string} key The key of the message param
   * @param {object} [fallback] The default value if the param is empty
   * @return {object} The plugin param value
   */
  function getParam(editor, key, fallback) {
    return editor.getParam('mediauploader_' + key) || fallback;
  }

  /**
   * Get an HTML safe message from plugin params
   *
   * @param {object} editor TinyMCE editor
   * @param {string} key The key of the message param
   * @param {string} [fallback] The default value if param is empty
   * @return {string} The plugin message
   */
  function getMessage(editor, key, fallback) {
    return escapeHTML(getParam(editor, key, fallback));
  }

  //--------------------------------------------------
  // Helpers
  //--------------------------------------------------

  // borrowed from handlebars.js
  var escapeHTML = (function () {
    var escape = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#x27;',
      '`': '&#x60;'
    };

    var badChars = /[&<>"'`]/g;
    var possible = /[&<>"'`]/;

    function escapeChar(chr) {
      return escape[chr];
    }

    /**
     * Escape unsafe XSS characters from a string
     *
     * @param {string} string The string to escape
     * @return {string} The escaped string
     */
    return function (string) {
      if (typeof string !== 'string') {
        return string;
      }

      if (!possible.test(string)) { return string; }
      return string.replace(badChars, escapeChar);
    };
  })();

  /**
   * Prevent the default behavior for an event
   *
   * @param {object} e The event that needs to be preventDefault'd
   */
  function eventPreventDefault(e) {
    e.preventDefault();
  }

})(document);
