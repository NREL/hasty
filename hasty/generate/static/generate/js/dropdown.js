$(function () {
    $('#point_jstree').jstree({
        "core": {
            "animation": 0,
            "check_callback": true,
            "themes": {
                "stripes": false,
                "dots": false,
                "icons": false
            },
        },
    });
});

$(function () {
    $('#equip_jstree').jstree({
        "core": {
            "animation": 0,
            "check_callback": true,
            "themes": {
                "stripes": false,
                "dots": false,
                "icons": false
            },
        },
    }).bind("loaded.jstree", function(){
        $(this).jstree("open_all");
    });
});
