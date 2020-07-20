# bruteForceNeuralNet_2.0
Improved version of brute force neural net code running in docker containers

# What this is for
While doing my masters project I had to classify healthy and sick patients using a relativly small dataset. Because of the small dataset and high signal to noise ratio in the image it was vital that the correct architecture for a neural net was chosen. Instead of hand testing architectures this program was built. Allowing the user to set the broad strokes of neural nets to be tested, and the program would autonomously test hundereds of variations architectures.

# How to use
1) Place labelled images in mlData folder
2) Run docker images with docker-compose
3) Open a web browser and type in localhost (NOTE, very little consideration has been taken towards security. DO NOT RUN THIS ON A PUBLIC NETWORK!!!!)
4) In website specify settings for the data in the mlData folder (e.g. number of catagories, naming convention). Instructions on the page should guide you.
5) Use website to specify the architectures that will be tested. This is done by typing the different possibilites for example;
  * "conv2d,64,relu|tanh_dense,2,sigmoid" will test 2 models, one with the relu activation layer and the tanh activation layer. Once again further instructions are on the website.
6) The Python backend will check the SQL database for new entries and will autonomously run tests
7) Currently there is no front end for viewing results. To view results, use the command
  docker exec -it mysql mysql -u root -p
Then use the password specified in the docker-compose.yml file. By default this is "test_pass"

# Considerations
This has only been tested using the images from my master project. While this is an attempt at a generalised method for testing neural net classifier architectures, there are still fixes required before this is achived. Currently these are required
* All images in mlData must be labelled correctly, any images that are not also understood by the classifier will break the program
  * This is because the importer was designed for general imports of any datatype and imports images and catagories seperatly. This causes the arrays to be mismatched if there are a different number loaded by each.
* Colour images are unsupported
* Images of different sizes in mlData can cause issues

* Incorrect architectures specified will not be caught by the front end. They will be marked as error when they fail to run, however the user is not notified.


# Planned fixes
* Mismatched data
* Prevent incorrect architectures from being input in the first place
* Security fixes allowing remote connection

# Future planned upgrades
* Allow importing of csv data as well as images
* More types of layers for program to test.
  * Current short list; Batch normalization layers, resnet layers, leaky relu activation function support
