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

        // list of possible inputs
        const inputs = ["name", "filepath", "numOfCatagories", "catagoryDict", "sqlSucess"];

        // show any error messages sent by PHP script
        for (let i=0; i<inputs.length; i++) {
          $("#"+inputs[i]+"Help").text(jsonResult[inputs[i]+"Error"]);
        }

        // show success
        $("#success").text(jsonResult["sqlSucess"]);
      },
      error: function() {
        console.log("Ajax failed post, check JavaScript file");
      }
    });
  });
});
