import pymysql.cursors
import getpass
import logging

class dbCursor():

    def __init__(self):
        # Connect to the database
        self.conn = pymysql.connect(host="mysql",
                                     user="root",
                                     password="test_pass",
                                     db="dockerDB",
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor();
        # create log file
        self.logger = logging.getLogger('dbConnectLog')
        logging.basicConfig(filename='error.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    ########################## Insert data into database ###########################
    def inputIDKeyToServer(self, testID, modelArchitecture, dataSet, imageDimentions, epochs, batchSize):
        try:
            sqlCommand = 'INSERT INTO IDKey ( \
            testID, \
            modelArchitecture, \
            dataSet, \
            imageDimentions, \
            epochs, \
            batchSize, \
            tested, \
            error) \
            VALUES (%s, %s, %s, %s, %s, %s, false, false);' % \
            (testID , \
            '\'' + modelArchitecture +  '\'', \
            '\'' + dataSet +  '\'', \
            imageDimentions, \
            epochs,
            batchSize);

            self.cursor.execute(sqlCommand);
            self.conn.commit();
        except:
            print("Failed to update the server, check logs");
            self.logError("Error in command", sqlCommand);

    # Adds data to the overview table in the MySQL server
    def inputOverviewToServer(self, testID, loss, predictionAccuracy, catagoryAccuracies):
        try:
            sqlCommand = 'UPDATE IDKey \
                SET \
                loss = %s, \
                predictionAccuracy = %s \
                WHERE \
                testID = %s;' % \
                (loss, predictionAccuracy, testID);

            self.cursor.execute(sqlCommand);
            self.conn.commit();

            # Add individual catagory accuracies
            for i in range(0, len(catagoryAccuracies)):
                self.addToColumn(testID, "catagory" + str(i+1), catagoryAccuracies[i]);

        except:
            print("Failed to update the server, check logs");
            self.logError("Error in command", sqlCommand);

    # Adds a column if it does not exist
    def addToColumn(self, testID, columnName, data):
        try:
            # check if column exists in the table
            sqlCommand = 'SELECT COLUMN_NAME \
                          FROM information_schema.columns \
                          WHERE table_schema=\'dockerDB\' \
                          AND table_name=\'IDKey\' \
                          AND COLUMN_NAME LIKE \'%s\';' % (columnName);

            self.cursor.execute(sqlCommand);
            result = self.cursor.fetchall();


            # if result dict is empty, there is no column with that name. So we add one
            if (bool(result) == False):
                sqlCommand = 'ALTER TABLE IDKey ADD %s FLOAT(8);' % (columnName);

                self.cursor.execute(sqlCommand);
                result = self.conn.commit();

            # then we add the data into the column
            sqlCommand = 'UPDATE IDKey SET %s = %s WHERE testID = %s;' % \
                (columnName, data, testID);

            self.cursor.execute(sqlCommand);
            self.conn.commit();
        except:
            print("Failed to update the server, check logs");
            self.logError("Error in command", sqlCommand);

    # Adds data to the training data table in the MySQL server
    def inputTrainDataToServer(self, testID, fold, epoch, loss):
        try:
            sqlCommand = 'INSERT INTO trainingLogs ( \
              testID, \
              fold, \
              epoch, \
              loss) \
            VALUES (%s, %s, %s, %s);' % \
                (testID, fold, epoch, loss);

            self.cursor.execute(sqlCommand);
            self.conn.commit();
        except:
            print("Failed to update the server, check logs");
            self.logError("Error in command", sqlCommand);

    # Adds data to the test data table in the MySQL server
    def inputTestDataToServer(self, testID, fold, modelOutput, correctAnswer):
        try:
            sqlCommand = "INSERT INTO testingLogs ( \
              testID, \
              fold, \
              modelOutput, \
              correctAnswer) \
            VALUES (%s, %s, %s, %s);" % \
                (testID, fold, '\'' + modelOutput + '\'', '\'' + correctAnswer + '\'');

            self.cursor.execute(sqlCommand);
            self.conn.commit();
        except:
            print("Failed to update the server, check logs");
            self.logError("Error in command", sqlCommand);

    ############################ Query from database ###############################
    def readTests(self):
        sqlCommand = 'SELECT * FROM IDKey WHERE tested = false AND error = false;';
        self.cursor.execute(sqlCommand);
        result = self.cursor.fetchall();
        return result;

    def lookUpData(self, dataSet):
        sqlCommand = 'SELECT filepath, numOfCatagories, catagoryDict \
                    FROM inputData WHERE dataSet = \'%s\'' % (dataSet);
        self.cursor.execute(sqlCommand);
        result = self.cursor.fetchone();
        return result;

    def findMaxID(self):
        sqlCommand = 'SELECT MAX(testID) from IDKey'
        self.cursor.execute(sqlCommand);
        result = self.cursor.fetchone();

        if (result['MAX(testID)'] == None):
            return 0;

        return result['MAX(testID)'] + 1;

    def logError(self, message, errorCmd):
        self.logger.warning(message);
        cmd = errorCmd.strip();
        self.logger.warning(cmd);

    ######################### Change values in database ########################
    def markCompleted(self, ID):
        sqlCommand = 'UPDATE IDKey SET tested = 1 WHERE testID = %s;' % (ID);
        self.cursor.execute(sqlCommand);
        self.conn.commit();

    def markError(self, ID):
        sqlCommand = 'UPDATE IDKey SET error = 1 WHERE testID = %s;' % (ID);
        self.cursor.execute(sqlCommand);
        self.conn.commit();

# unit testing
if __name__ == "__main__":
    cursorTest = dbCursor();
    cursorTest.inputOverviewToServer(20, 'a', 'b', 'c', 'd');
