function toggle_hay() {

    document.getElementById("haystack").classList.remove('btn-outline-warning');
    document.getElementById("haystack").classList.add('btn-warning');
    document.getElementById("brick").classList.remove('btn-info');
    document.getElementById("brick").classList.add('btn-outline-info');

    var hay_table = document.getElementById("hay_table");
    var brick_table = document.getElementById("brick_table");

    brick_table.style.display = "none";
    hay_table.style.display = "block";

}

function toggle_brick() {

    document.getElementById("brick").classList.remove('btn-outline-info');
    document.getElementById("brick").classList.add('btn-info');
    document.getElementById("haystack").classList.remove('btn-warning');
    document.getElementById("haystack").classList.add('btn-outline-warning');

    var hay_table = document.getElementById("hay_table");
    var brick_table = document.getElementById("brick_table");

    hay_table.style.display = "none";
    brick_table.style.display = "block";

}
