
window.console.log("SCRIPTS LOADED");


function ESPsuccess(data){
    window.console.log(data);
}



function espcomm(data){
  window.console.log("sending"+data);
  $.ajax({
      type: "GET",
      url: controlleraddress,
      data: data,
      success: ESPsuccess

});
}


var complexswitch=" \
<BR> \
<h2>CONTROLLER FOR BACKYARD INCANDESCENT STRING LIGHTS</h2> \
<a href='#' class='btn green' onclick='ON()'>CLICK TO TURN LIGHTS ON</a> \
<BR><BR><BR><BR><BR><BR>\
<a href='#' class='btn red' onclick='OFF()'>CLICK TO TURN LIGHTS OFF</a>\
\
<BR><br><BR><BR>\
<input type='range' onchange='lightsDIM(this.value)' min='1' max = '99' style='height: 50px' value='50'>\
<BR><BR><BR>\
";


var RGBcontroller="<BR>"+
            "<a href='#' class='btn green' onclick='ON(\""+espid + "\",\"" + 1 + "\")'>CLICK TO TURN LIGHTS</a>"+
            "<a href='#' class='btn red' onclick='OFF(\"" + espid + "\",\"" + 1 + "\")'>CLICK TO TURN LIGHTS OFF</a>"+
            "<BR><BR>"+
            "<input type='range' onchange='RedLightDIM(this.value,\"" + espid + "\",\"" + 1 + "\")' min='10' max = '99' style='height: 50px' value='50'>"+
            "<BR><BR>"+
            "<input type='range' onchange='GreenLightDIM(this.value,\"" + espid + "\",\"" + 1 + "\")' min='10' max = '99' style='height: 50px' value='50'>"+
            "<BR><BR>"+
            "<input type='range' onchange='BlueLightDIM(this.value,\"" + espid + "\",\"" + 1 + "\")' min='10' max = '99' style='height: 50px' value='50'>"+
            "<BR><BR>"+
            "<a href='#' class='btn green' onclick='ON(\""+espid + "\",\"" + 2 + "\")'>CLICK TO TURN LIGHTS</a>"+
            "<a href='#' class='btn red' onclick='OFF(\"" + espid + "\",\"" + 2 + "\")'>CLICK TO TURN LIGHTS OFF</a>"+
            "<BR><BR>"+
            "<input type='range' onchange='RedLightDIM(this.value,\"" + espid + "\",\"" + 2 + "\")' min='10' max = '99' style='height: 50px' value='50'>"+
            "<BR><BR>"+
            "<input type='range' onchange='GreenLightDIM(this.value,\"" + espid + "\",\"" + 2 + "\")' min='10' max = '99' style='height: 50px' value='50'>"+
            "<BR><BR>"+
            "<input type='range' onchange='BlueLightDIM(this.value,\"" + espid + "\",\"" + 2 + "\")' min='10' max = '99' style='height: 50px' value='50'>"+
            "<BR><BR>";



//Scripts loaded, built UI

function ON(espid, chid) {
    window.console.log("output on");
    espcomm("ACTION=SWITCHON", espid, chid);
}
function OFF(espid, chid) {
    window.console.log("output on")
    espcomm("ACTION=SWITCHOFF", espid, chid);
}
function lightsDIM(value, espid, chid) {
    espcomm(("ACTION=LIGHTDIM." + value), espid, chid);
}

function RedLightDIM(value, espid, chid) {
    espcomm(("ACTION=RGBSDIM.R" + value), espid, chid);
}

function GreenLightDIM(value, espid, chid) {
    espcomm(("ACTION=RGBSDIM.G" + value), espid, chid);
}

function BlueLightDIM(value, espid, chid) {
    espcomm(("ACTION=RGBSDIM.B" + value), espid, chid);
}


function ESPsuccess(data) {
    window.console.log(data);
}


function espcomm(data, espid, chid) {
    window.console.log("sending" + data);
    $.ajax({
        type: "GET",
        url: "CH=" + chid+"&"+data,
        success: ESPsuccess

    });
}


//run at load


$('#fallback').hide();
$('#panel').html(RGBcontroller);

//function getBaseUrl() {
var re = new RegExp(/^.*\//);
var controlleraddress= re.exec(window.location.href);
var espid=controlleraddress;
window.console.log("THIS IS UNIT"+controlleraddress);
//}



