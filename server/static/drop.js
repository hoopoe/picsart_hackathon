(function(){
    var $ = function( elem ){
        if (!(this instanceof $)){
            return new $(elem);
        }
        this.el = document.getElementById( elem );
    };
    window.$ = $;
    $.prototype = {
        onChange : function( callback ){
            this.el.addEventListener('change', callback );
            return this;
        }
    };
})();

var dragdrop = {
    init : function( elem ){
        elem.setAttribute('ondrop', 'dragdrop.drop(event)');
        elem.setAttribute('ondragover', 'dragdrop.drag(event)' );
    },
    drop : function(e){
        e.preventDefault();
        var file = e.dataTransfer.files[0];
        runUpload( file );
    },
    drag : function(e){
        e.preventDefault();
    }
};


function runUpload( file ) {
    if( file.type === 'image/png'  ||
        file.type === 'image/jpg'  ||
        file.type === 'image/jpeg' ||
        file.type === 'image/gif'  ||
        file.type === 'image/bmp'  ){
        var reader = new FileReader(),
            image = new Image();
        reader.readAsDataURL( file );
        reader.onload = function( _file ){
            $('imgPrime').el.src = _file.target.result;
            // $('imgPrime').el.style.display = 'inline';

            //TODO: call socket here
            // const socket = io();
            socket.emit('test_img_upload', {'data': _file.target.result})
        } // END reader.onload()
    } // END test if file.type === image
}

function initDrop() {
    if( window.FileReader ){
        // Connect the DIV surrounding the file upload to HTML5 drag and drop calls
        dragdrop.init( $('userActions').el );
        //	Bind the input[type="file"] to the function runUpload()
        $('fileUpload').onChange(function(){
            runUpload( this.files[0] );
            updateImage();
        });
    }else{
        // Report error message if FileReader is unavilable
        var p   = document.createElement( 'p' ),
            msg = document.createTextNode( 'Sorry, your browser does not support FileReader.' );
        p.className = 'error';
        p.appendChild( msg );
        $('userActions').el.innerHTML = '';
        $('userActions').el.appendChild( p );
    }
}

// =============================================================

// var	maxWidth = 500,
// 		maxHeight = 500,
// 		photo = $('#photo'),
// 		originalCanvas = null,
// 		filters = $('#filters li a'),
// 		filterContainer = $('#filterContainer');

// 	// Use the fileReader plugin to listen for
// 	// file drag and drop on the photo div:

// 	photo.fileReaderJS({
// 		on:{
// 			load: function(e, file){

// 				// An image has been dropped.

// 				var img = $('<img>').appendTo(photo),
// 					imgWidth, newWidth,
// 					imgHeight, newHeight,
// 					ratio;

// 				// Remove canvas elements left on the page
// 				// from previous image drag/drops.

// 				photo.find('canvas').remove();
// 				filters.removeClass('active');

// 				// When the image is loaded successfully,
// 				// we can find out its width/height:

// 				img.load(function() {

// 					imgWidth  = this.width;
// 					imgHeight = this.height;

// 					// Calculate the new image dimensions, so they fit
// 					// inside the maxWidth x maxHeight bounding box

// 					if (imgWidth >= maxWidth || imgHeight >= maxHeight) {

// 						// The image is too large,
// 						// resize it to fit a 500x500 square!

// 						if (imgWidth > imgHeight) {

// 							// Wide
// 							ratio = imgWidth / maxWidth;
// 							newWidth = maxWidth;
// 							newHeight = imgHeight / ratio;

// 						} else {

// 							// Tall or square
// 							ratio = imgHeight / maxHeight;
// 							newHeight = maxHeight;
// 							newWidth = imgWidth / ratio;

// 						}

// 					} else {
// 						newHeight = imgHeight;
// 						newWidth = imgWidth;
// 					}

// 					// Create the original canvas.

// 					originalCanvas = $('<canvas>');
// 					var originalContext = originalCanvas[0].getContext('2d');

// 					// Set the attributes for centering the canvas

// 					originalCanvas.attr({
// 						width: newWidth,
// 						height: newHeight
// 					}).css({
// 						marginTop: -newHeight/2,
// 						marginLeft: -newWidth/2
// 					});

// 					// Draw the dropped image to the canvas
// 					// with the new dimensions
// 					originalContext.drawImage(this, 0, 0, newWidth, newHeight);

// 					// We don't need this any more
// 					img.remove();

// 					filterContainer.fadeIn();

// 					// Trigger the default "normal" filter
// 					filters.first().click();
// 				});

// 				// Set the src of the img, which will
// 				// trigger the load event when done:

// 				img.attr('src', e.target.result);
// 			},

// 			beforestart: function(file){

// 				// Accept only images.
// 				// Returning false will reject the file.

// 				return /^image/.test(file.type);
// 			}
// 		}
// 	});