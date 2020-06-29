$(".custom-file-input").on("change", function () {
    document.getElementById("upload").disabled=false;
    document.getElementById("upload").classList.remove('btn-outline-dark');
    document.getElementById("upload").classList.add('btn-outline-success');
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});
