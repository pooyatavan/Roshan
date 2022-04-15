var intervalID = setInterval(update_values, 4000);
var j = 0;
var y = 0;
var m = 0;
var t = []
var x = []
function update_values() {$.getJSON($SCRIPT_ROOT + '/_stuff', function(data) {
    x = document.getElementsByClassName("right");
    j = 0;
    i = 0;
    for (m = 0; m < data.alldata[2].length; m++) {
        if (m == data.alldata[2].length) {
            break;
        } else {
            document.getElementById(x[m].id).innerHTML = "";
            document.getElementById(t[m].id).innerHTML = "";
        }
    }
    while (true) {
        if (j == data.alldata[2].length) {
            break;
        }
        if (x[j].id == data.alldata[0][i].tower_name) {
            if (data.alldata[0][i].mode == "mp") {
                document.getElementById(x[j].id).innerHTML += '<div class="nodes"><i class="fa fa-circle" style="background: -webkit-radial-gradient(#000000, #000000); -webkit-background-clip: text; -webkit-text-fill-color: transparent;""></i><div class="tooltip">' + data.alldata[0][i].device_name + '</div></div>';
                i++;
            }
            if (data.alldata[0][i].mode == "ptp") {
                document.getElementById(x[j].id).innerHTML += '<div class="nodes"><i class="fa fa-arrow-circle-up" style="background: -webkit-radial-gradient(#000000, #000000); -webkit-background-clip: text; -webkit-text-fill-color: transparent;""></i><div class="tooltip">' + data.alldata[0][i].device_name + '</div></div>';
                i++;
            }
            if (data.alldata[0][i].mode == "ptpt") {
                if ("ups" + data.alldata[0][i].tower_name == t[j].id) {
                    document.getElementById(t[j].id).innerHTML += '<div class="tooltip"><i class="fa fa-link" aria-hidden="true" style="background: -webkit-radial-gradient(#000000, #000000); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i></div></br>';
                    i++;
                }
            }
            if (data.alldata[0][i].mode == "router") {
                if ("ups" + data.alldata[0][i].tower_name == t[j].id) {
                        document.getElementById(t[j].id).innerHTML += '<div class="tooltip"><i class="fa fa-arrows-alt" aria-hidden="true" style="background: -webkit-radial-gradient(#000000, #000000); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i></div></br>';
                        i++;
                }
            }
            if (data.alldata[0][i].mode == "ups") {
                if ("ups" + data.alldata[0][i].tower_name == t[j].id) {
                    document.getElementById(t[j].id).innerHTML += '<div class="tooltip"><i class="fa fa-battery-full" aria-hidden="true" style="background: -webkit-radial-gradient(#000000, #000000); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i></div></br>';
                    i++;
                }
            }
        } else {
            i++;
        }
        if (j == data.alldata[2].length) {
            break;
        } else {
            if (data.alldata[0].length == i) {
            j++;
            i = 0;
            }
        }
    }
});}

function screen() { $.getJSON($SCRIPT_ROOT + '/_stuff',
    function(data) {
        for (i = 0; i < data.alldata[2].length; i++) {
            document.getElementById('containment-wrapper').innerHTML += '<div id="' + data.alldata[2][i].id + '" class="draggable" data-left="20px" data-top="20px" style="position: absolute; left:' + data.alldata[2][i].left + '; top:' + data.alldata[2][i].top + '"><div class="left"><div class="left_top"><a>' + data.alldata[2][i].tower_name + '</a><br><i style="--fa-animation-duration: 20s; color: black;" class="fa-solid fa-cog fa-spin"></i></div></br><div class="left_down" id="ups' + data.alldata[2][i].tower_name + '"></div></div><div class="right" id="' + data.alldata[2][i].tower_name + '"></div></div>';
        }
        t = document.getElementsByClassName("left_down");
        $( "#containment-wrapper .draggable" ).draggable();
    });}

function save(e, id) {
    var dict = [];
    var o = 1;
    var x = document.getElementsByClassName("draggable");
    while (true) {
        if (o == x.length + 1) {
                break;
        } else {
            var sum = "#" + o;
            var id = o;
            var top = $(sum).css("top");
            var left = $(sum).css("left");
            dict.push({'id': id, 'top': top, 'left': left});
            o++;
            }
        }
    
        $.ajax({
            url: '/_stuff',
            contentType: "application/json;charset=utf-8",
            data: JSON.stringify(dict),
            dataType: "json",
            type: 'POST'
        });
    }
