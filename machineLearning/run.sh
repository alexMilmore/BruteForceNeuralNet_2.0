#!/bin/bash
# wait to start program to assure mysql server goes up first
sleep 30

# Continually run the file on loop. This is done because new data to test on
# could be uploaded to the server anytime
done=0
while [ $done -eq 0 ]
do
	echo "ML container querying the server for new tests"
  python3 src/classifier.py
  sleep 30
done
