/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function toggleButtons() {
    $('#up-img-btn').toggle();
    $('#del-img-btn').toggle();
    $('#imageResult').toggleClass('d-none');
    $('#imageResult').toggleClass('d-block');
}

$(function () {
    $('#upload').on('change', function () {
        readURL(input);
        toggleButtons();
    });

    $('#del-img-btn').on({
        'click': function(){
            $('#imageResult').attr('src','');
            $("#upload").val(null);
            $("#delete-img").prop("checked", true);
            toggleButtons();
        }
    });

    $('#imageResult').on('error', function () { 
        console.log('img err');
    })
});

/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */
var input = document.getElementById( 'upload' );
// var infoArea = document.getElementById( 'upload-label' );

// input.addEventListener( 'change', showFileName );
// function showFileName( event ) {
//   var input = event.srcElement;
//   var fileName = input.files[0].name;
//   infoArea.textContent = 'File name: ' + fileName;
// }