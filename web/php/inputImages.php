<?php
$values = array();
$errors = array();

//////////////////////// POST data handling ///////////////////////////////////
if (!empty($_POST)) {
  // Check if any of the required fields are empty
  $required = array("name", "filepath", "numOfCatagories", "catagoryDict");

  foreach ($required as $form) {
    if (!empty($_POST[$form])) {$values[$form] = $_POST[$form];}
    else {$errors[$form."Error"] = $form." is empty";}
  }

  if (is_numeric($_POST["numOfCatagories"])) {$values["numOfCatagories"] = (int)$_POST["numOfCatagories"];}
  else {$errors["numOfCatagories"."Error"] = "numOfCatagories must be an integer";}

}
else {$errors["postError"] = "_POST is empty";}

//////////////////////////// Server handling /////////////////////////////////
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
    // send data to mysql container
    $sql = "INSERT INTO
            inputData (dataset, filepath, numOfCatagories, catagoryDict)
            VALUES('".$values["name"]."','".$values["filepath"]."','".$values["numOfCatagories"]."','".$values["catagoryDict"]."')";

    $sql = str_replace(array("\r", "\n"), '', $sql);
    $sql = stripslashes($sql);

    if ($conn->query($sql) === TRUE) {
      $errors["sqlSucess"] = "Input to mysql server was sucessful";
    }
    else {
      if (strpos($conn->error, 'Duplicate entry') !== false) {
        $errors["nameError"] = "This name has already been used";
      }
      else {
        $errors["sqlError"] = "Error in sql command" . $conn->error;
      }
    }
    $conn->close();
  }
}

// encode into json and echo error messages
$json = json_encode($errors);
echo $json;
?>
