//$(document).ready(function(){
//    console.log("hi andrew")    
//});

$(".file").change(getFile);
$(".button-submit-ct").click(submitCT)



function getFile()
{
    var file = this.files[0];

    var reader = new FileReader();
    reader.onload = function(progressEvent)
    {
        // Entire file
        //console.log(this.result);
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
        var result;
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
        line = "<tr><td>" + keyLines[i][0] + "&nbsp;&rarr;</td><td><input type='text' id='keyTD' name='keyTD' value='" +  keyLines[i][2] + "' maxlength='1' size='1' style='text-align:center'></td></tr>"
        $("#keyHere").append(line);

    }
    $(".submit-ct").css("display", "none");
    $(".main").css("display", "block");
}
