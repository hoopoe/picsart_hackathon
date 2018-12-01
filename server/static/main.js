const socket = io()
// const button = document.querySelector('button')
// const inp = document.querySelector('imgPrime')
// const img = document.querySelector('img')

function ab2str(buf) {
    return String.fromCharCode.apply(null, new Uint8Array(buf));
  }

socket.on('resp', (data) => {
    //console.log(data)
    //console.log(ab2str(data['data']))
    image.src="data:image/jpeg;base64,"+ab2str(data['data'])
    updateImage();
})

// inp.onchange = function (evt) {
//     var tgt = evt.target || window.event.srcElement,
//         files = tgt.files;
//
//     if (FileReader && files && files.length) {
//         var fr = new FileReader();
//         fr.onload = function () {
//             //console.log(fr.result)
//             //img.src = fr.result;
//             socket.emit('test_img_upload', {'data': fr.result})
//         }
//         fr.readAsDataURL(files[0]);
//
//     }
// }