//$(document).ready(function(){
//    console.log("hi andrew")    
//});

$(".file").change(getFile);
$(".button-submit-ct").click(submitCT);
$(".button-submit-key").click(modKey);
$(".button-submit-swap").click(swapByFreq);

function swapByFreq()
{
    $.ajax({
        type: 'POST',
        url: '/swapByFreq',
        contentType: 'application/JSON',
        data: "",
        success: function(data){
            swapKeyCol(data["key"]);
            $("#modified").text(data["plaintext"]);
        }
    });
}

function swapKeyCol(key)
{
    var keyVals = key.split("\n");
    var table = document.getElementById("keyHere")
    var trs = table.getElementsByTagName("tr");
    var tds = null;
    for (var i=0; i<trs.length; i++)
    {
        document.getElementById("keyVal-" + String(i)).value = keyVals[i][2];
    }

}

function modKey()
{
    var table = document.getElementById("keyHere")
    var trs = table.getElementsByTagName("tr");
    var tds = null;
    var firstCol = "";
    var secondCol = "";
    var getValRegex = /value=\"(.)\"/;
    for (var i=0; i<trs.length; i++)
    {
        tds = trs[i].getElementsByTagName("td");
        firstCol += tds[0].innerHTML[0] + " ";
        secondCol += document.getElementById("keyVal-" + String(i)).value + " ";
    }

    $.ajax({
        type: 'POST',
        url: '/modKey',
        contentType: 'application/JSON',
        data: JSON.stringify({"first": firstCol, "second": secondCol}),
        success: function(data){
            $("#modified").text(data);
        }
    });
}



function getFile()
{
    var file = this.files[0];

    var reader = new FileReader();
    reader.onload = function(progressEvent)
    {
        $("#ct").val(this.result);
    };
    reader.readAsText(file);
    
}

function submitCT()
{
    var text = $("#ct").val();
    if (text === "")
    {
        alert("Error: no ciphertext submitted");
    }
    else
    {
        $.ajax({
            type: 'POST',
            url: '/sendCT',
            contentType: 'application/JSON',
            data: JSON.stringify(text),
            success: function(data){
                swapInputs(data);
            }
        });
    }
}

function swapInputs(data)
{
    var keyLines = data["key"].split("\n");
    var line = ""
    $("#keyHere").text("");
    for (var i = 0; i < keyLines.length - 1; i++)
    {
        line = "<tr><td>" + keyLines[i][0] + "&nbsp;&rarr;</td><td><input type='text' id='keyVal-" + String(i) + "' name='keyTD' value='" +  keyLines[i][2] + "' maxlength='1' size='1' style='text-align:center'></td></tr>"
        $("#keyHere").append(line);

    }
    $("#modified").text(data["orig"]);
    $("#original").text(data["orig"]);
    $(".submit-ct").css("display", "none");
    $(".main").css("display", "block");
}