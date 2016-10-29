var ESPs; //array of active ESP CHANNELSs {'IP','CH#', 'TYPE', {PARAM,REALNAME,VALUE}}
var appPath='/cgi-bin/IOS/ios.py'


function loadIoSdevices() {
    var index;
    for (index = 0; index < initIPs.length; ++index) {
        window.console.log(initIPs[index]);
        initESP(initIPs[index]);


    }
}


function initESP(IP){
  window.console.log("initing"+IP);
  $.ajax({
      type: "GET",
      url: appPath+'?mode=init&IP='+IP,
      success: addESP

});
}

function addESP(data){
    //breakdown init data
    window.console.log(data);
}

function updateIoSstatus(){
    //run through all ESPs and update their status
}

function qsESP(){
    //query status of ESP


}
function qsESPch(){
    //query status of ESP individual channel


}