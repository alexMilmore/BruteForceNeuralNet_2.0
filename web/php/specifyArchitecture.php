<?php
$obj = array();
$errors = array();

//////////////////////////// POST data handling //////////////////////////////

if (!empty($_POST)) {
  $required = array("resolution", "epochs", "batchSize", "dataset", "architecture");
  $mustBeInt = array("resolution", "epochs", "batchSize");

  // make sure that required fields are filled
  foreach ($required as $form) {
    if (!empty($_POST[$form])) {$obj[$form] = $_POST[$form];}
    else {$errors[$form."Error"] = $form." is empty";}
  }

  // make sure that certain sections are integers
  foreach ($mustBeInt as $form) {
    if (is_numeric($_POST[$form])) {$obj[$form] = (int)$_POST[$form];}
    else {$errors[$form."Error"] = $form." must be an integer";}
  }

}
else {echo "_POST is empty";}


//////////////////// create array of tests from architecture //////////////////
// takes string of possible architecture combinations and makes an array of
// architectures
function strToArray($str) {
  $data = array();
  // _ denotes layers, seperate these out
  $oneDimArray = explode('_', $str);
  foreach ($oneDimArray as $subArray) {
    // , denotes different settings inside layers
    $twoDimArray = explode(',', $subArray);
    foreach ($twoDimArray as $subSubArray) {
      $data = addToArrays($subSubArray, $data);
      $data = addToArrays(',', $data);
    }
    $data = addToArrays('_', $data);
  }
  return $data;
}

function addToArrays($input, $arrays) {
  $output = array();
  // if | charachter present, different options are possible
  // e.g.; a,b|c --->  a,b  a,c
  $possibilites = explode('|', $input);
  foreach ($possibilites as $possibility) {
    // add to arrays if they are not empty, otherwisem just add possibility
    if (!empty($arrays)) {
      foreach ($arrays as $array) {
        array_push($output, $array.$possibility);
      }
    }
    else {
      array_push($output, $possibility);
    }
  }
  return $output;
}

$obj['allArchitectures'] =  strToArray($obj["architecture"]);

/////////////////////////////// mysql /////////////////////////////////////////
// if no errors, send to server
// TODO This whole section is kinda spagetti code and needs to be refactored

if (empty((array)$errors)) {
  // Connect to mysql container
  $servername = "mysql";
  $username = "root";
  $password = "test_pass";
  $dbname = "dockerDB";

  // Create connection
  $conn = new mysqli($servername, $username, $password, $dbname);

  // Check connection
  if ($conn->connect_error) {
    $errors["connectError"] = "Connection failed: " . $conn->connect_error;
  }
  else {

    foreach($obj['allArchitectures'] as $arch) {
      // send data to mysql container
      $sql = "INSERT INTO
              IDKey (modelArchitecture, dataSet, imageDimentions, epochs, batchSize)
              VALUES('".$arch."','".$obj["dataset"]."','".$obj["resolution"]."','".$obj["epochs"]."','".$obj["batchSize"]."')";

      $sql = str_replace(array("\r", "\n"), '', $sql);
      $sql = stripslashes($sql);

      if ($conn->query($sql) === TRUE) {
        $obj["sqlSucess"] = "Input to mysql server was sucessful";
      }
      else {
        $errors["sqlError"] = "Error in sql command" . $conn->error;
      }
    }

    $conn->close();
  }
}

// encode into json and echo error messages
$json = json_encode(array_merge($obj, $errors));
echo $json;
?>
