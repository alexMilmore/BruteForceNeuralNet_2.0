<?php
$values = array();
$errors = array();
$error = false;

//////////////////////// POST data handling ///////////////////////////////////
if (!empty($_POST)) {
  // Check if any of the required fields are empty
  $required = array("name", "filepath", "numOfCatagories", "catagoryDict");

  foreach ($required as $form) {
    if (!empty($_POST[$form])) {
      $values[$form] = $_POST[$form];
      $errors[$form."Error"] = "";
    }
    else {
      $errors[$form."Error"] = $form." is empty";
      $error = true;
    }
  }

  if (is_numeric($_POST["numOfCatagories"])) {
    $values["numOfCatagories"] = (int)$_POST["numOfCatagories"];
    $errors["numOfCatagories"."Error"] = "";
  }
  else {
    $errors["numOfCatagories"."Error"] = "numOfCatagories must be an integer";
    $error = true;
  }

}
else {$errors["postError"] = "_POST is empty";}

//////////////////////////// Server handling /////////////////////////////////
// if no errors, send to server
// TODO This whole section is kinda spagetti code and needs to be refactored

if ($error == false) {
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
    $sql = "INSERT INTO inputData (dataset, filepath, numOfCatagories, catagoryDict) VALUES(?,?,?,?)";
    $stmt = $conn->prepare($sql);

    // Bind parameters to SQL prepared statment
    if (!$stmt->bind_param('ssis', $values["name"], $values["filepath"], $values["numOfCatagories"], $values["catagoryDict"])) {
      $errors["bindError"] = "mysqli failed to bind parameters";
    }
    // Attempt to execute the prepared statment
    if ($stmt->execute()) {
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
    $stmt->close();
    $conn->close();
  }
}

// encode into json and echo error messages
$json = json_encode(array_merge($errors, $values));
echo $json;
?>
