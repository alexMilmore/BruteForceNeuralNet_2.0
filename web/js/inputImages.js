// prevent html lines from showing undefined strings
function httpResult(str) {
  if (typeof(str) != 'undefined') {return "<p>" + str + "</p>"}
  return  "";
}

// AJAX stuff, uses .html commands to edit the error messages on the page
$(function () {

  $('#inputImages').on('submit', function (e) {

    e.preventDefault();
    name = $("#name").val();
    filepath = $("#filepath").val();
    numOfCatagories = $("#numOfCatagories").val();
    catagoryDict = $("#catagoryDict").val();

    $.ajax({
      type: 'POST',
      url: '../php/inputImages.php',
      data: {name:name, filepath:filepath, numOfCatagories:numOfCatagories, catagoryDict,catagoryDict},
      success: function (result) {
        console.log("PHP script returned: " + result);
        jsonResult = JSON.parse(result);
        var nameMsg = httpResult(jsonResult["nameError"]);
        var filepathMsg = httpResult(jsonResult["filepathError"]);
        var numOfCatagoriesMsg = httpResult(jsonResult["numOfCatagoriesError"]);
        var catagoryDictMsg = httpResult(jsonResult["catagoryDictError"]);
        var successMsg = httpResult(jsonResult["sqlSucess"]);

        $("#nameHelp").html(nameMsg);
        $("#filepathHelp").html(filepathMsg);
        $("#numOfCatagoriesHelp").html(numOfCatagoriesMsg);
        $("#catagoryDictHelp").html(catagoryDictMsg);
        $("#success").html(successMsg);
      },
      error: function() {
        console.log("Ajax failed post, check JavaScript file");
      }
    });
  });
});
