(function() {
    var imageBrowse = eid("imageBrowse");
    imageBrowse.addEventListener('change', handleImage, false);

    var mainCanvas = fx.canvas();
    var mainTexture;
    var mainCanvasContainer = eid("canvascontainer");

    mainCanvas.id = "c-photo";
    mainCanvasContainer.appendChild(mainCanvas);

    var btnSave = eid("btn-save");
    btnSave.onclick = function() {
        window.open(renderer.domElement.toDataURL("image/png"), 'DNA_Screen');
    }

    var slider1;
    var slider2;
    var slider3;


    $('#sl1').slider({
        formatter: function(value) {
            return 'Current value: ' + value;
        }
    });

    eid("effects").addEventListener('click', function(e) {
        var vfx = e.target.getAttribute("data-effect");
        if(vfx) {
            switch(vfx) {
                case "ink":
                    reset().ink(0.25).update();
                    break;
                case "edge":
                    reset().edgeWork(5).update();
                    break;
                case "hex":
                    reset().hexagonalPixelate(320, 239.5, 20).update();
                    break;
                case "dot":
                    reset().dotScreen(320, 239.5, 1.1, 3).update();
                    break;
                case "dot-color":
                    reset().colorHalftone(320, 239.5, 0.25, 4).update();
                    break;
            }
        }

    });

    function slider(id, slide) {
        var slider = new Slider('#' + id);
        slider.on("slide", slide);

        return slider;
    }

    function reset() {
        return mainCanvas.draw(mainTexture);
    }

    function handleImage(e){
        var reader = new FileReader();
        reader.onload = function(event){
            var img = new Image();
            img.onload = function(){
                mainCanvas.width = img.width;
                mainCanvas.height = img.height;
                mainTexture = mainCanvas.texture(img);
                reset().ink(0.25).update();
            }
            img.src = event.target.result;
        }
        reader.readAsDataURL(e.target.files[0]);     
    }

    function eid(id) {
        return document.getElementById(id);
    }
})();