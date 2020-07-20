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
        var resolutionMsg = httpResult(jsonResult["resolutionError"]);
        var epochMsg = httpResult(jsonResult["epochError"]);
        var batchSizeMsg = httpResult(jsonResult["batchSizeError"]);
        var datasetMsg = httpResult(jsonResult["datasetError"]);
        var architectureMsg = httpResult(jsonResult["architectureError"]);
        var successMsg = httpResult(jsonResult["sqlSucess"]);

        $("#resolutionHelp").html(resolutionMsg);
        $("#epochHelp").html(epochMsg);
        $("#batchSizeHelp").html(batchSizeMsg);
        $("#datasetHelp").html(datasetMsg);
        $("#architectureHelp").html(architectureMsg);
        $("#success").html(successMsg);
      },
      error: function() {
        console.log("Ajax failed post, check JavaScript file");
      }
    });

  });

});
