var appPath = '/cgi-bin/IOS/ios.py' //path to IOS master
var UIhtml = '' //holder for eventual html to buld client UI
var ESPdb //holder for ESP database

function initClient() {
    window.console.log("initing");
    $.ajax({
        type: "GET",
        url: appPath + '?mode=init',//get ESP Database
        success: buildUI //send database to UI builder

    });
}

function buildUI(data) {
    window.console.log("in build UI");
//    window.console.log(data);
    UIhtml = "DETECTED INTERNET OF SHIT"
    json = jQuery.parseJSON(data);
    window.console.log(json.ESPDB);
    window.console.log("breaking out individual elements");
//    window.console.log(ESPdb.ESPDB.length);

    for (var i = 0; i < json.ESPDB.length; i++) {
        var obj = json.ESPDB[i];
        console.log(obj.espid);
        if (!obj.espid.contains("IOS")) //check to see if this is an actual node with an IP address
            addESP(obj); //create a UI element based on this object

    }


    $('#panel').html(UIhtml);

}

function addESP(data) {
    window.console.log("adding ESP to UI");
    UIhtml += "<hr><h2>" + data.espid + " : " + data.desc + "</h2>";
    for (var i = 0; i < data.channels.length; i++) {
        addESPchannel(data.channels[i], data.espid);
    }
}

function addESPchannel(chobj, espid, chid) {
    window.console.log("CHANNEL DETECTED");
    UIhtml += "<h3>CH:" + chobj.CH + "- " + chobj.CHdesc + "</h3>";
    //now figure out what it is
    addUIelement(chobj.type, espid, chobj.CH);


}

function addUIelement(type, espid, chid) {
    if (type == "SWITCH") {
        window.console.log("SWITCH");
    }
    else if (type == "DIMLIGHT") {
        window.console.log("DIMMER LIGHT");
    }
    else if (type == "RGB") {
        window.console.log("RGB controller");
        UIhtml +=
            "<BR>"+
            "<a href='#' class='btn green' onclick='lightsfullON(\""+espid + "\",\"" + chid + "\")'>CLICK TO TURN LIGHTS</a>"+
            "<a href='#' class='btn red' onclick='lightsfullOFF(\"" + espid + "\",\"" + chid + "\")'>CLICK TO TURN LIGHTS OFF</a>"+
            "<BR><BR>"+
            "<input type='range' onchange='RedLightDIM(this.value,\"" + espid + "\",\"" + chid + "\")' min='1' max = '99' style='height: 50px' value='50'>"+
            "<BR><BR>"+
            "<input type='range' onchange='BlueLightDIM(this.value,\"" + espid + "\",\"" + chid + "\")' min='1' max = '99' style='height: 50px' value='50'>"+
            "<BR><BR>"+
            "<input type='range' onchange='GreenLightDIM(this.value,\"" + espid + "\",\"" + chid + "\")' min='1' max = '99' style='height: 50px' value='50'>"+
            "<BR><BR>";
    }
}

function updateIoSstatus() {
    //run through all ESPs and update their status
}

function qsESP() {
    //query status of ESP


}
function qsESPch() {
    //query status of ESP individual channel


}

//Scripts loaded, built UI

function lightsfullON(espid, chid) {
    window.console.log("lights on");
    espcomm("LIGHTS=ON", espid, chid);
}
function lightsfullOFF(espid, chid) {
    espcomm("LIGHTS=OFF", espid, chid);
}
function lightsDIM(value, espid, chid) {
    espcomm(("DIM" + value), espid, chid);
}

function RedLightDIM(value, espid, chid) {
    espcomm(("RDIM" + value), espid, chid);
}

function GreenLightDIM(value, espid, chid) {
    espcomm(("GDIM" + value), espid, chid);
}

function BlueLightDIM(value) {
    espcomm(("BDIM" + value), espid, chid);
}


function ESPsuccess(data) {
    window.console.log(data);
}


function espcomm(data, espid, chid) {
    window.console.log("sending" + data);
    $.ajax({
        type: "GET",
        url: appPath = "?mode=xact&espid=" + espid + "&ch=" + chid,
        data: data,
        success: ESPsuccess

    });
}


initClient();


$('#fallback').hide();
$('#panel').html("Looking for crappy things...probably everything is broken");

//function getBaseUrl() {
var re = new RegExp(/^.*\//);
var controlleraddress = re.exec(window.location.href);
window.console.log("THIS IS" + controlleraddress);
//}



