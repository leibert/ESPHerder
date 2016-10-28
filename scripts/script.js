var ESPs; //array of active ESP CHANNELSs {'IP','CH#', 'TYPE', {PARAM,REALNAME,VALUE}}



function loadIoSdevices() {
    var index;
    for (index = 0; index < initIPs.length; ++index) {
        console.log(initIPs[index]);
        espinit(initIPs[index]);


    }
}


function initESP(IP){
  window.console.log("initing"+IP);
  $.ajax({
      type: "GET",
      url: IP+'?init',
      success: addESP

});
}

function addESP(data){
//breakdown init data
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