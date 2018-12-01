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

            //TODO:
            // socket.emit('test_img_upload', {'data': fr.result})
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