/**
 * Created by leibert on 12/4/16.
 */
function loadDashboard(){
    $.ajax({
        type: "GET",
        url: appPath + '?mode=loadmacros',//get ESP Database
        success: buildDashboard //send database to UI builder

    });

}

function buildDashboard(result){
    window.console.log("Building Dashboard");
    window.console.log(result);
    UIhtml = "<center><h2>AVAILABLE MACROS:</h2><BR>";
    macrojson = jQuery.parseJSON(result);
    window.console.log(macrojson);
//    window.console.log(json.ESPDB);
//    window.console.log("breaking out individual elements");
//    window.console.log(ESPdb.ESPDB.length);
    for(var macro in macrojson)
    {
        window.console.log(macrojson[macro]);
        macrodef = macrojson[macro].split(':');
        UIhtml+=addMacro(macro, macrodef[0],macrodef[1]);



        window.console.log(macrodef);
        window.console.log(macrojson[macro][2]);

    }
    UIhtml+="</center>"
    $('#fallback').hide();
    $('#panel').html(UIhtml);
}

function execMacro(macroID){
        window.console.log("Running Macro"+macroID);
        $.ajax({
        type: "POST",
        url: appPath + '?mode=execmacro&macroID='+macroID,//get ESP Database
        success: function(data){window.console.log(data);}

    });

}

function addMacro(id, type, name){
    var HTML ="";
    switch (type){
        case "BTN":
        {
            HTML="<BR><br>" +
                "<a href='#' class='btn green' onclick='execMacro("+id+")'>"+name+"</a>"+
                "<BR>";

        }
            break

    }

    return HTML;
}




//loadDashboard();