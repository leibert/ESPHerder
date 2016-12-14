window.console.log("SCRIPTS LOADED");


function ESPsuccess(data) {
    window.console.log(data);
}


function espcomm(data) {
    window.console.log("sending" + data);
    $.ajax({
        type: "GET",
        url: controlleraddress,
        data: data,
        success: ESPsuccess

    });
}

var html = "";


function singlePWMcontrollerUIblock(ip, ch) {
    html = "<BR>" +
        "<a href='javascript:void(0)' class='btn green' onclick='ON(\"" + ip + "\",\"" + ch + "\")'>CLICK TO TURN LIGHTS</a>"+
        "<a href='javascript:void(0)' class='btn red' onclick='OFF(\"" + ip + "\",\"" + ch + "\")'>CLICK TO TURN LIGHTS OFF</a>"+
        "<BR><BR>" +
        "<input type='range' onchange='lightsDIM(this.value)' min='1' max = '99' style='height: 50px' value='50'>"+
        "<BR><BR>";
    return html;

}

function digitalcontrollerUIblock(ip, ch) {
    html = "<BR>" +
        "<a href='javascript:void(0)' class='btn green' onclick='ON(\"" + ip + "\",\"" + ch + "\")'>CLICK TO TURN LIGHTS</a>"+
        "<a href='javascript:void(0)' class='btn red' onclick='OFF(\"" + ip + "\",\"" + ch + "\")'>CLICK TO TURN LIGHTS OFF</a>"+
        "<BR><BR>";
    return html;

}

function RGBcontrollerUIblock(ip, ch) {
    html = "<BR>" +
        "<a href='javascript:void(0)' class='btn green' onclick='ON(\"" + ip + "\",\"" + ch + "\")'>CLICK TO TURN LIGHTS</a>" +
        "<a href='javascript:void(0)' class='btn red' onclick='OFF(\"" + ip + "\",\"" + ch + "\")'>CLICK TO TURN LIGHTS OFF</a>" +
        "<BR><BR>" +
        "<input type='range' onchange='RedLightDIM(this.value,\"" + ip + "\",\"" + ch + "\")' min='10' max = '99' style='height: 50px' value='50'>" +
        "<BR><BR>" +
        "<input type='range' onchange='GreenLightDIM(this.value,\"" + ip + "\",\"" + ch + "\")' min='10' max = '99' style='height: 50px' value='50'>" +
        "<BR><BR>" +
        "<input type='range' onchange='BlueLightDIM(this.value,\"" + ip + "\",\"" + ch + "\")' min='10' max = '99' style='height: 50px' value='50'>";
    return html
}


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

function ESPblackout(){
    espcomm(("ACTION=BLACKOUT"), espid);
}

function ESPinit() {
    $.ajax({
        type: "GET",
        url: "ACTION=init",
        dataType: "json",
        success: ESPUIpopulate


    });
}

function ESPUIpopulate(data) {
    window.console.log(data);
    window.console.log(data["espid"]);
    html = "<html><title>" + data["espid"] + "</title><body>";
    html += "<h2><b>" + data["espid"] + "</b>:&nbsp;&nbsp; " + data["desc"] + "</h2>";
    charray = data["channels"];

    for (var key in charray) {
        var ch = charray[key];
        html += "<h3><b>CH" + ch["CH"] + "</b>:&nbsp;&nbsp; " + ch["CHdesc"] + "</b></h3>";
        window.console.log(ch);
        switch (ch["type"]) {
            case "RGB":
                html += RGBcontrollerUIblock(data["espid"],ch["CH"]);
                break;
            case "PWM":
                html += singlePWMcontrollerUIblock(data["espid"],ch["CH"]);
                break;
            case "DIGITAL":
                html += digitalcontrollerUIblock(data["espid"],ch["CH"]);
                break;

        }
//        var attrValue = obj[key];


    }
    html+="<br><br><br><br><a href='javascript:void(0)' class='btn blkout' onclick='ESPblackout()'>BLACKOUT</a>";
    html+="</body></html>";
    $('#fallback').hide();
    $('#panel').html(html);




}


function ESPsuccess(data) {
    window.console.log(data);
}


function espcomm(data, espid, chid) {
    window.console.log("sending" + data);
    $.ajax({
        type: "GET",
        url: "CH=" + chid + "&" + data,
        success: ESPsuccess

    });
}


//run at load


ESPinit();


//function getBaseUrl() {
var re = new RegExp(/^.*\//);
var controlleraddress = re.exec(window.location.href);
var espid = controlleraddress;
window.console.log("THIS IS UNIT" + controlleraddress);
//}



