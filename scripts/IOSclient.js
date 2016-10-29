
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
<a href='#' class='btn green' onclick='lightsfullON()'>CLICK TO TURN LIGHTS ON</a> \
<BR><BR><BR><BR><BR><BR>\
<a href='#' class='btn red' onclick='lightsfullOFF()'>CLICK TO TURN LIGHTS OFF</a>\
\
<BR><br><BR><BR>\
<input type='range' onchange='lightsDIM(this.value)' min='1' max = '99' style='height: 50px' value='50'>\
<BR><BR><BR>\
";


var RGBcontroller=" \
<BR> \
<h2>CONTROLLER FOR BACKYARD INCANDESCENT STRING LIGHTS</h2> \
<a href='#' class='btn green' onclick='lightsfullON()'>CLICK TO TURN LIGHTS ON</a> \
<BR><BR><BR><BR><BR><BR>\
<a href='#' class='btn red' onclick='lightsfullOFF()'>CLICK TO TURN LIGHTS OFF</a>\
\
<BR><br><BR><BR>\
<input type='range' onchange='RedLightDIM(this.value)' min='1' max = '99' style='height: 50px' value='50'>\
<BR><BR><BR>\
<input type='range' onchange='BlueLightDIM(this.value)' min='1' max = '99' style='height: 50px' value='50'>\
<BR><BR><BR>\
<input type='range' onchange='GreenLightDIM(this.value)' min='1' max = '99' style='height: 50px' value='50'>\
<BR><BR><BR>\
";



function lightsfullON(){
    window.console.log("lights on");
    espcomm("LIGHTS=ON");
}
function lightsfullOFF(){
    espcomm("LIGHTS=OFF");
}
function lightsDIM(value){
    espcomm("DIM"+value);
}

function RedLightDIM(value){
    espcomm("RDIM"+value);
}

function GreenLightDIM(value){
    espcomm("GDIM"+value);
}

function BlueLightDIM(value){
    espcomm("BDIM"+value);
}






//run at load


$('#fallback').hide();
$('#panel').html(RGBcontroller);

//function getBaseUrl() {
var re = new RegExp(/^.*\//);
var controlleraddress= re.exec(window.location.href);
window.console.log("THIS IS UNIT"+controlleraddress);
//}



