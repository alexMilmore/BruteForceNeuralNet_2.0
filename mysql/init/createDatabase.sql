CREATE DATABASE dockerDB;
USE dockerDB

CREATE TABLE inputData(
  dataset varchar(255) PRIMARY KEY,
  filepath varchar(255) NOT NULL,
  numOfCatagories int(8) NOT NULL,
  catagoryDict varchar(255) NOT NULL
);

CREATE TABLE IDKey(
  testID int(255) PRIMARY KEY AUTO_INCREMENT,
  modelArchitecture varchar(255) NOT NULL,
  dataSet varchar(255) NOT NULL,
  imageDimentions int(8) NOT NULL,
  epochs int(8) NOT NULL,
  batchSize int(8) NOT NULL,
  tested boolean DEFAULT 0,
  error boolean DEFAULT 0,
  loss float(8),
  predictionAccuracy float(8),
  FOREIGN KEY (dataSet) REFERENCES inputData(dataSet)
);

CREATE TABLE trainingLogs(
  testID int(255),
  fold int(8),
  epoch int(8),
  loss float(8),
  FOREIGN KEY (testID) REFERENCES IDKey(testID)
);

CREATE TABLE testingLogs(
  testID int(255),
  fold int(8),
  modelOutput varchar(255),
  correctAnswer varchar(255),
  FOREIGN KEY (testID) REFERENCES IDKey(testID)
  /*TODO; ADD REFERENCE TO SPECIFIC IMAGE IN TEST*/
);
