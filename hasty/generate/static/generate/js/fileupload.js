$(".custom-file-input").on("change", function () {
    document.getElementById("upload").disabled=false;
    document.getElementById("upload").classList.remove('btn-outline-dark');
    document.getElementById("upload").classList.add('btn-outline-success');
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

function fileValidation() {
    var fileInput =
        document.getElementById('customFile');

    var filePath = fileInput.value;

    // Allowing file type
    var allowedExtensions = /(\.json)$/i;

    if (!allowedExtensions.exec(filePath)) {
        alert('Invalid file type.  Accepted types (.json)');
        fileInput.value = '';
        return false;
    }
    else {
        return true
    }
}
