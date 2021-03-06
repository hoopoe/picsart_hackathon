const socket = io()
const inps = document.querySelectorAll('input')
const back_inp = inps[0]
const main_inp = inps[1]
const img = document.querySelector('#outImage')
const btn = document.querySelector('button')
const btn_def = document.querySelector("#def")

function ab2str(buf) {
    return String.fromCharCode.apply(null, new Uint8Array(buf));
  }

socket.on('respCombine', (data) => {
    console.log('Message received: respCombine');
    console.log(data['data']);
    //console.log(ab2str(data['data']))
    //img.src="data:image/jpeg;base64,"+ab2str(data['data'])
    if (data['data']) {
        var path = 'static/results/' + data['data'];
        console.log("image to update: " + path);

        var new_image = new Image();
        //set up the new image
        new_image.id = "outImage";
        new_image.src = path;           
        // insert new image and remove old
        img.parentNode.insertBefore(new_image,img);
        img.parentNode.removeChild(img);
    }
    else {
        console.log('failed to get new image');
    }
});

back_inp.onchange = function (evt) {
    var tgt = evt.target || window.event.srcElement,
        files = tgt.files;

    if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
            //console.log(fr.result)
            document.querySelector("#back").src = fr.result;
            socket.emit('back_img_upload', {'data': fr.result})
        }
        fr.readAsDataURL(files[0]);

    }
}

main_inp.onchange = function (evt) {
    var tgt = evt.target || window.event.srcElement,
        files = tgt.files;

    if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
            //console.log(fr.result)
            document.querySelector("#front").src = fr.result;
            socket.emit('main_img_upload', {'data': fr.result})
        }
        fr.readAsDataURL(files[0]);

    }
}

btn.onclick = function() {
    socket.emit('combine')
}

btn_def.onclick = function() {
    socket.emit('back_img_upload', {'data': '', 'src':'concrete.jpg'})
}

