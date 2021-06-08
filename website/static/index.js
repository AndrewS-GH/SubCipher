$(".file").change(getFile);
$(".button-submit-ct").click(submitCT);
$(".button-submit-key").click(modKey);
$(".button-submit-swap").click(swapByFreq);
$(".button-submit-reset").click(resetCipher);
$("#subLenSS").click(genSS);
$("#subDupSS").click(genDup);

// reads user inputted text file and populates text area with contents
function getFile()
{
    var file = this.files[0]; // user inputted file
    var reader = new FileReader();

    reader.onload = function(progressEvent)
    {
        $("#ct").val(this.result);
    };
    reader.readAsText(file);
}

// ajax call sending the submitted ciphertext
function submitCT()
{
    var text = $("#ct").val(); // user submitted ciphertext

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

// swaps the submit ciphertext interface to the main tool
function swapInputs(data)
{
    var keyLines = data["key"].split("\n"); // gets the key from backend
    var line = "" // holds line of html that will be appended to the modify key section

    $("#keyHere").text("");
    for (var i = 0; i < keyLines.length - 1; i++)
    {
        line = "<tr><td>" + keyLines[i][0] + "&nbsp;&rarr;</td><td><input type='text' id='keyVal-" + String(i) + "' name='keyTD' value='" +  keyLines[i][2] + "' maxlength='1' size='1' style='text-align:center'></td></tr>"
        $("#keyHere").append(line);
    }
    $("#modified").text(data["orig"]); // initializes modified text section with original since no user modifications yet
    $("#original").text(data["orig"]); // initializes original text section
    $(".submit-ct").css("display", "none"); // removes submit field from view
    $(".main").css("display", "block"); // reveals main program interface
}

// ajax call to python with users key modifications, updates modified text
function modKey()
{
    var table = document.getElementById("keyHere") // table where modify key elements will go
    var trs = table.getElementsByTagName("tr"); // all tr elements in table
    var tds = null;
    var firstCol = ""; // the values in the original text
    var secondCol = ""; // the values in the modified text
    var checkMissing = "";

    // populates firstCol and secondCol to pass to python
    for (var i=0; i<trs.length; i++)
    {
        tds = trs[i].getElementsByTagName("td");
        firstCol += tds[0].innerHTML[0] + " ";
        checkMissing = document.getElementById("keyVal-" + String(i)).value;
        if (checkMissing === "") { alert("Error: cannot leave any inputs blank"); return;}
        else if (checkMissing === " ") { alert("Error: cannot leave any inputs with whitespace"); return; }
        secondCol += checkMissing + " ";
    }

    // passes to python to update the key for the cipher
    $.ajax({
        type: 'POST',
        url: '/modKey',
        contentType: 'application/JSON',
        data: JSON.stringify({"first": firstCol, "second": secondCol}),
        success: function(data){
            $("#modified").text(data); // the data passed back is the modified cipher
        }
    });
}

// ajax call to get results of swapping by English letter frequency from backend
function swapByFreq()
{
    $.ajax({
        type: 'POST',
        url: '/swapByFreq',
        contentType: 'application/JSON',
        data: "",
        success: function(data){
            swapKeyCol(data["key"]); // updates key
            $("#modified").text(data["plaintext"]); // updates modified text
        }
    });
}

// updates key in HTML
function swapKeyCol(key)
{
    var keyVals = key.split("\n"); // key pairs are separated by newlines
    var table = document.getElementById("keyHere") // table containing modify key elements
    var trs = table.getElementsByTagName("tr"); // all tr elements

    for (var i=0; i<trs.length; i++)
    {
        document.getElementById("keyVal-" + String(i)).value = keyVals[i][2]; // updates the value for all elements
    }
}

// resets all progress with cipher
function resetCipher()
{
    var table = document.getElementById("keyHere") // table containing modify key elements
    var trs = table.getElementsByTagName("tr"); // all tr elements
    var tds = null;

    // updates input elements with their original value
    for (var i=0; i<trs.length; i++)
    {
        tds = trs[i].getElementsByTagName("td");
        document.getElementById("keyVal-" + String(i)).value = tds[0].innerHTML[0];
    }

    // modified text set to original text
    $("#modified").text($("#original").text());

    // ajax call to reset cipher in backend
    $.ajax({
        type: 'POST',
        url: '/resetCipher',
        contentType: 'application/JSON',
        data: ""
    });
}

// generates the most common substrings of length gotten from user
function genSS()
{
    var lenSS = $("#lenSS").val(); // length inputted by user
    var errorLine = ""; // unique error sent to updateEngAttacks function

    // generates common substrings in the backend
    $.ajax({
        type: 'POST',
        url: '/genSS',
        contentType: 'application/JSON',
        data: JSON.stringify(lenSS),
        success: function(data){
            errorLine="<tr><td>No Values for substrings of length " + lenSS + "</td></tr>"
            updateEngAttacks(data, errorLine);
        }
    });
}

// generates the most common duplicate substrings of size 2
function genDup()
{
    var errorLine = ""; // unique error sent to updateEngAttacks function

    // generates common duplicate substrings in the backend
    $.ajax({
        type: 'POST',
        url: '/dupSS',
        contentType: 'application/JSON',
        data: "",
        success: function(data){
            errorLine="<tr><td>No duplicate value substrings</td></tr>";
            updateEngAttacks(data, errorLine);
        }
    });
}

// populates the section for substring rankings
function updateEngAttacks(data, errorLine)
{
    $("#engAttackTable tr").remove() // empties it first

    if (data.length === 0) // no values
    {
        $("#engAttackTable").append(errorLine)
    }

   for (var i=0; i < data.length; i++)
   {
       var line = "<tr><td>" + data[i][0] + "&nbsp;&rarr;</td><td>" + data[i][1] + "</td></tr>"
       $("#engAttackTable").append(line)
   }   
}

// Help menus
$("#keyTool").click(function(){
    $("#toolText").css("display", "none");
    $("#toolAttack").css("display", "none");

    var display = $("#toolKey").css("display");
    if (display === "block") { $("#toolKey").css("display", "none"); }
    else { $("#toolKey").css("display", "block"); }
});
$("#textTool").click(function(){
    $("#toolAttack").css("display", "none");
    $("#toolKey").css("display", "none");

    var display = $("#toolText").css("display");
    if (display === "block") { $("#toolText").css("display", "none"); }
    else { $("#toolText").css("display", "block"); }
});
$("#attackTool").click(function(){
    $("#toolKey").css("display", "none");
    $("#toolText").css("display", "none");

    var display = $("#toolAttack").css("display");
    if (display === "block") { $("#toolAttack").css("display", "none"); }
    else { $("#toolAttack").css("display", "block"); }
});
