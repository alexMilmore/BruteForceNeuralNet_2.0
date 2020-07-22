// prevent html lines from showing undefined strings
function httpResult(str) {
  if (typeof(str) != 'undefined') {return "<p>" + str + "</p>"}
  return  "";
}

$(function () {

  $('#specifyArchitecture').on('submit', function (e) {

    e.preventDefault();
    resolution = $("#resolution").val();
    epochs = $("#epochs").val();
    batchSize = $("#batchSize").val();
    dataset = $("#dataset").val();
    architecture = $("#architecture").val();

    $.ajax({
      type: 'POST',
      url: '../php/specifyArchitecture.php',
      data: {resolution:resolution, epochs:epochs, batchSize:batchSize, dataset:dataset, architecture:architecture},
      success: function (result) {
        console.log("PHP script returned: " + result);
        jsonResult = JSON.parse(result);

        // list of possible inputs
        const inputs = ["resolution", "epoch", "batchSize", "dataset", "architecture"];

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
