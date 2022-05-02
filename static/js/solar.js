var intervalID = setInterval(update_values, 4000);
var j = 0;
var y = 0;
var m = 0;
var t = []
var x = []
// copy ip to clipboard
function copy(that){
    var inp = document.createElement('input');
    document.body.appendChild(inp)
    inp.value = that.textContent
    inp.select();
    document.execCommand('copy',false);
    inp.remove();
}

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
                // for multi points
                try {
                if (data.alldata[0][i].mode == "mp") {
                    if (data.alldata[0][i].status == "enable") {
                        if (data.alldata[0][i].ping == "Request timeout") {
                            document.getElementById(x[j].id).innerHTML += '<div class="nodes"><i class="fa fa-circle" style="background: -webkit-radial-gradient(#ff3000, #ff7800); -webkit-background-clip: text; -webkit-text-fill-color: transparent;""></i><div class="tooltip">' + data.alldata[0][i].device_name + '<span class="tooltiptext" style="top: -54px;">APN: ' + data.alldata[0][i].device_name + ' </br> Ping: ' + data.alldata[0][i].ping + '</br> IP: <a class="copy" onclick="copy(this)">' + data.alldata[0][i].ip + '</a></br>Radio: ' + data.alldata[0][i].models + '</br>OS: ' + data.alldata[0][i].os + '</br>Status: ' + data.alldata[0][i].status + '</br>Active: ' + data.alldata[0][i].time_active + '</br>Area: ' + data.alldata[0][i].area + '</span></div></div>';
                            i++;
                        } else {
                            document.getElementById(x[j].id).innerHTML += '<div class="nodes"><i class="fa fa-circle" style="background: -webkit-radial-gradient(#60e555, #60e555); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i><div class="tooltip">' + data.alldata[0][i].device_name + '<span class="tooltiptext" style="top: -50px;">APN: ' + data.alldata[0][i].device_name + ' </br> Ping: ' + data.alldata[0][i].ping + '</br> IP: <a class="copy" onclick="copy(this)">' + data.alldata[0][i].ip + '</a></br>Radio: ' + data.alldata[0][i].models + '</br>OS: ' + data.alldata[0][i].os + '</br>Status: Online</br>Area: ' + data.alldata[0][i].area + ' </span></div></div>';
                            i++;
                            }
                    } else {
                        document.getElementById(x[j].id).innerHTML += '<div class="nodes"><i class="fa fa-circle" style="background: -webkit-radial-gradient(#1E90FF, #1E90FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;""></i><div class="tooltip">' + data.alldata[0][i].device_name + '<span class="tooltiptext" style="top: -50px;">APN: ' + data.alldata[0][i].device_name + ' </br> Ping: Disable</br> IP: <a class="copy" onclick="copy(this)">' + data.alldata[0][i].ip + '</a></br>Radio: ' + data.alldata[0][i].models + '</br>OS: ' + data.alldata[0][i].os + '</br>Status: ' + data.alldata[0][i].status + '</br>Area: ' + data.alldata[0][i].area + '</span></div></div>';
                        i++;
                    }
                }
            } catch {}
            // for point to points
            try {
                if (data.alldata[0][i].mode == "ptp") {
                    if (data.alldata[0][i].status == "enable") {
                        if (data.alldata[0][i].ping == "Request timeout") {
                            document.getElementById(x[j].id).innerHTML += '<div class="nodes"><i class="fa fa-arrow-circle-up" style="background: -webkit-radial-gradient(#ff3000, #ff7800); -webkit-background-clip: text; -webkit-text-fill-color: transparent;""></i><div class="tooltip">' + data.alldata[0][i].device_name + '<span class="tooltiptext" style="top: -49px;">APN: ' + data.alldata[0][i].device_name + ' </br> Ping: ' + data.alldata[0][i].ping + '</br> IP: ' + data.alldata[0][i].ip + '</br>Radio: ' + data.alldata[0][i].models + '</br>OS: ' + data.alldata[0][i].os + '</br>Status: ' + data.alldata[0][i].status + '</br>Active: ' + data.alldata[0][i].time_active + '</span></div></div>';
                            i++;
                        } else {
                            document.getElementById(x[j].id).innerHTML += '<div class="nodes"><i class="fa fa-arrow-circle-up" style="background: -webkit-radial-gradient(#af59ff, #af59ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i><div class="tooltip">' + data.alldata[0][i].device_name + '<span class="tooltiptext" style="top: -41px;">APN: ' + data.alldata[0][i].device_name + ' </br> Ping: ' + data.alldata[0][i].ping + '</br> IP: ' + data.alldata[0][i].ip + '</br>Radio: ' + data.alldata[0][i].models + '</br>OS: ' + data.alldata[0][i].os + '</br>Status: Online</span></div></div>';
                            i++;
                        }
                    } else {
                        document.getElementById(x[j].id).innerHTML += '<div class="nodes"><i class="fa fa-arrow-circle-up" style="background: -webkit-radial-gradient(#1E90FF, #1E90FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i><div class="tooltip">' + data.alldata[0][i].device_name + '<span class="tooltiptext" style="top: -41px;">APN: ' + data.alldata[0][i].device_name + ' </br> Ping: Disabel</br> IP: ' + data.alldata[0][i].ip + '</br>Radio: ' + data.alldata[0][i].models + '</br>OS: ' + data.alldata[0][i].os + '</br>Status: Online</span></div></div>';
                        i++;
                    }
                }
        } catch {}
            // for towers back bones
            try{
                if (data.alldata[0][i].mode == "ptpt") {
                    if ("ups" + data.alldata[0][i].tower_name == t[j].id) {
                        if (data.alldata[0][i].status == "enable") {
                            if (data.alldata[0][i].ping == "Request timeout") {
                                document.getElementById(t[j].id).innerHTML += '<div class="tooltip"><i class="fa fa-link" aria-hidden="true" style="background: -webkit-radial-gradient(#ff3000, #ff7800); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i><span class="tooltiptext" style="top: -27px; left: 25px;">Ping: ' + data.alldata[0][i].ping + '</br>IP:' + data.alldata[0][i].ip + '</br>Model: ' + data.alldata[0][i].models + '</br>OS: ' + data.alldata[0][i].os + '</br>Status: ' + data.alldata[0][i].status + '</br>Active: ' + data.alldata[0][i].time_active + '</span></div></br>';
                                i++;
                            } else {
                                document.getElementById(t[j].id).innerHTML += '<div class="tooltip"><i class="fa fa-link" aria-hidden="true" style="background: -webkit-radial-gradient(#60e555, #60e555); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i><span class="tooltiptext" style="top: -20px; left: 25px;">Ping: ' + data.alldata[0][i].ping + '</br> IP: ' + data.alldata[0][i].ip + '</br>Model: ' + data.alldata[0][i].models + '</br>OS: ' + data.alldata[0][i].os + '</br>Status: Online</span></div></br>';
                                i++;
                            }
                        } else {
                            document.getElementById(t[j].id).innerHTML += '<div class="tooltip"><i class="fa fa-link" aria-hidden="true" style="background: -webkit-radial-gradient(#1E90FF, #1E90FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i><span class="tooltiptext" style="top: -20px; left: 25px;">Ping: Disable</br> IP: ' + data.alldata[0][i].ip + '</br>Model: ' + data.alldata[0][i].models + '</br>OS: ' + data.alldata[0][i].os + '</br>Status: Online</span></div></br>';
                            i++; 
                        }
                    }
                }
            } catch{}
            // for routers
            try {
                if (data.alldata[0][i].mode == "router") {
                    if ("ups" + data.alldata[0][i].tower_name == t[j].id) {
                        if (data.alldata[0][i].ping == "Request timeout") {
                            document.getElementById(t[j].id).innerHTML += '<div class="tooltip"><i class="fa fa-arrows-alt" aria-hidden="true" style="background: -webkit-radial-gradient(#ff3000, #ff7800); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i><span class="tooltiptext" style="top: -24px; left: 25px;">Ping: ' + data.alldata[0][i].ping + '</br> IP: ' + data.alldata[0][i].ip + '</br>Model: ' + data.alldata[0][i].models + '</br>OS: ' + data.alldata[0][i].os + '</br>Status: ' + data.alldata[0][i].status + '</br>Active: ' + data.alldata[0][i].time_active + '</span></div></br>';
                            i++;
                        } else {
                            document.getElementById(t[j].id).innerHTML += '<div class="tooltip"><i class="fa fa-arrows-alt" aria-hidden="true" style="background: -webkit-radial-gradient(#60e555, #60e555); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i><span class="tooltiptext" style="top: -24px; left: 25px;">Ping: ' + data.alldata[0][i].ping + '</br> IP: ' + data.alldata[0][i].ip + '</br>Model: ' + data.alldata[0][i].models + '</br>OS: ' + data.alldata[0][i].os + '</br>Status: Online</span></div></br>';
                            i++;
                        }
                    }
                }
            } catch {}
            // for towers batterys UPS
            try {
                if (data.alldata[0][i].mode == "ups") {
                    if ("ups" + data.alldata[0][i].tower_name == t[j].id) {
                        if (data.alldata[0][i].ping == "Request timeout") {
                            document.getElementById(t[j].id).innerHTML += '<div class="tooltip"><i class="fa-solid fa-car-battery" aria-hidden="true" style="background: -webkit-radial-gradient(#ff3000, #ff7800); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i><span class="tooltiptext" style="top: -10px; left: 25px;">Ping: ' + data.alldata[0][i].ping + '</br> IP: ' + data.alldata[0][i].ip + '</br>Status: ' + data.alldata[0][i].status + '</br>Active: ' + data.alldata[0][i].time_active + '</span></div></br>';
                            i++;
                        } else {
                            document.getElementById(t[j].id).innerHTML += '<div class="tooltip"><i class="fa-solid fa-car-battery" aria-hidden="true" style="background: -webkit-radial-gradient(#60e555, #60e555); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i><span class="tooltiptext" style="top: -10px; left: 25px;">Ping: ' + data.alldata[0][i].ping + '</br> IP: ' + data.alldata[0][i].ip + '</br>Status: Online</span></div></br>';
                            i++;
                        }
                    }
                }
            } catch(err) {}
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

// when screen load
function screen() { $.getJSON($SCRIPT_ROOT + '/_stuff', function(data) {
    document.getElementById('panzoom').innerHTML += '<div id="containment-wrapper" style="width: ' + data.alldata[1][0] + 'px; height: ' + data.alldata[1][1] + 'px;"></div>';
    var myVar;
    for (i = 0; i < data.alldata[2].length; i++) {
        document.getElementById('containment-wrapper').innerHTML += '<div id="solar" class="draggable" data-left="20px" data-top="20px" style="position: absolute; left:' + data.alldata[2][i].left + '; top:' + data.alldata[2][i].top + '"><div id="load' + data.alldata[2][i].id + '" class="loader"></div><div class="left"><div class="left_top"><a>' + data.alldata[2][i].tower_name + '</a><br><i style="--fa-animation-duration: 20s;" class="fa-solid fa-cog fa-spin"></i></div></br><div class="left_down" id="ups' + data.alldata[2][i].tower_name + '"></div></div><div class="right" id="' + data.alldata[2][i].tower_name + '"></div></div></div>';
    }
    t = document.getElementsByClassName("left_down");
    myVar = setTimeout(loading, 4000);
});}

function loading() { $.getJSON($SCRIPT_ROOT + '/_stuff', function(data) {
    for (i = 1; i <= data.alldata[2].length; i++) {
        id = "load" + i;
        document.getElementById(id).style.display = "none";
    }
    controll.call();
});}

// controll mouse
function controll() {
    try{
        const elem = document.getElementById('panzoom');
        const panzoom = Panzoom(elem);
        const parent = elem.parentElement
        parent.addEventListener('wheel', panzoom.zoomWithWheel);
        const resetButton = document.getElementById('reset');
        resetButton.addEventListener('click', panzoom.reset)
        const zoomInButton = document.getElementById('zoom-in');
        const zoomOutButton = document.getElementById('zoom-out');
        zoomInButton.addEventListener('click', panzoom.zoomIn)
        zoomOutButton.addEventListener('click', panzoom.zoomOut)
    } catch {}
}
