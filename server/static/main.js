$(function() {
  const socket = io();
  // const button = document.querySelector('button')
  // const inp = document.querySelector('imgPrime')
  const img = document.querySelector("img");

  function ab2str(buf) {
    return String.fromCharCode.apply(null, new Uint8Array(buf));
  }

  socket.on("resp", data => {
    //console.log(data)
    //console.log(ab2str(data['data']))
    img.src = "data:image/jpeg;base64," + ab2str(data["data"]);
    updateImage();
  });

    function back_preset_emit(name) {
        socket.emit('back_img_upload', {'data': '', 'src':name+'.jpg'})
    }

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

  // var maxWidth = 500,
  //   maxHeight = 500,
  //   photo = $("#photo"),
  //   originalCanvas = null,
  //   filters = $("#filters li a"),
  //   filterContainer = $("#filterContainer");

  // // Listen for clicks on the filters

  // filters.click(function(e) {
  //   e.preventDefault();

  //   var f = $(this);

  //   if (f.is(".active")) {
  //     // Apply filters only once
  //     return false;
  //   }

  //   filters.removeClass("active");
  //   f.addClass("active");

  //   // Clone the canvas
  //   var clone = originalCanvas.clone();

  //   // Clone the image stored in the canvas as well
  //   clone[0].getContext("2d").drawImage(originalCanvas[0], 0, 0);

  //   // Add the clone to the page and trigger
  //   // the Caman library on it

  //   photo
  //     .find("canvas")
  //     .remove()
  //     .end()
  //     .append(clone);

  //   var effect = $.trim(f[0].id);

  //   Caman(clone[0], function() {
  //     // If such an effect exists, use it:

  //     if (effect in this) {
  //       this[effect]();
  //       this.render();

  //       // Show the download button
  //       showDownload(clone[0]);
  //     } else {
  //       hideDownload();
  //     }
  //   });
  // });

  // // Use the mousewheel plugin to scroll
  // // scroll the div more intuitively

  // filterContainer.find("ul").on("mousewheel", function(e, delta) {
  //   this.scrollLeft -= delta * 50;
  //   e.preventDefault();
  // });

  // var downloadImage = $("a.downloadImage");

  // function showDownload(canvas) {
  //   downloadImage
  //     .off("click")
  //     .click(function() {
  //       // When the download link is clicked, get the
  //       // DataURL of the image and set it as href:

  //       var url = canvas.toDataURL("image/png;base64;");
  //       downloadImage.attr("href", url);
  //     })
  //     .fadeIn();
  // }

  // function hideDownload() {
  //   downloadImage.fadeOut();
  // }
});
